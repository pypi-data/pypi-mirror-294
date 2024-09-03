import asyncio
import base64
import hashlib
import io
import json
import logging
import math
import os
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from enum import Enum
from functools import partial
from random import random
from typing import (
    Annotated,
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import cron_descriptor
import openai
import pytz
import requests
from apscheduler.job import Job
from apscheduler.triggers.cron import CronTrigger
from asgiref.sync import sync_to_async
from fastapi import Depends, Header, HTTPException, Request, UploadFile
from PIL import Image
from starlette.authentication import has_required_scope
from starlette.requests import URL

from khoj.database import adapters
from khoj.database.adapters import (
    AgentAdapters,
    AutomationAdapters,
    ConversationAdapters,
    EntryAdapters,
    create_khoj_token,
    get_khoj_tokens,
    get_user_name,
    get_user_notion_config,
    get_user_subscription_state,
    run_with_process_lock,
)
from khoj.database.models import (
    ChatModelOptions,
    ClientApplication,
    Conversation,
    GithubConfig,
    KhojUser,
    NotionConfig,
    ProcessLock,
    Subscription,
    TextToImageModelConfig,
    UserRequests,
)
from khoj.processor.content.docx.docx_to_entries import DocxToEntries
from khoj.processor.content.github.github_to_entries import GithubToEntries
from khoj.processor.content.images.image_to_entries import ImageToEntries
from khoj.processor.content.markdown.markdown_to_entries import MarkdownToEntries
from khoj.processor.content.notion.notion_to_entries import NotionToEntries
from khoj.processor.content.org_mode.org_to_entries import OrgToEntries
from khoj.processor.content.pdf.pdf_to_entries import PdfToEntries
from khoj.processor.content.plaintext.plaintext_to_entries import PlaintextToEntries
from khoj.processor.conversation import prompts
from khoj.processor.conversation.anthropic.anthropic_chat import (
    anthropic_send_message_to_model,
    converse_anthropic,
)
from khoj.processor.conversation.offline.chat_model import (
    converse_offline,
    send_message_to_model_offline,
)
from khoj.processor.conversation.openai.gpt import converse, send_message_to_model
from khoj.processor.conversation.utils import (
    ThreadedGenerator,
    generate_chatml_messages_with_context,
    save_to_conversation_log,
)
from khoj.processor.speech.text_to_speech import is_eleven_labs_enabled
from khoj.routers.email import is_resend_enabled, send_task_email
from khoj.routers.storage import upload_image
from khoj.routers.twilio import is_twilio_enabled
from khoj.search_type import text_search
from khoj.utils import state
from khoj.utils.config import OfflineChatProcessorModel
from khoj.utils.helpers import (
    LRU,
    ConversationCommand,
    ImageIntentType,
    is_none_or_empty,
    is_valid_url,
    log_telemetry,
    mode_descriptions_for_llm,
    timer,
    tool_descriptions_for_llm,
)
from khoj.utils.rawconfig import LocationData

logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=1)


NOTION_OAUTH_CLIENT_ID = os.getenv("NOTION_OAUTH_CLIENT_ID")
NOTION_OAUTH_CLIENT_SECRET = os.getenv("NOTION_OAUTH_CLIENT_SECRET")
NOTION_REDIRECT_URI = os.getenv("NOTION_REDIRECT_URI")


def is_query_empty(query: str) -> bool:
    return is_none_or_empty(query.strip())


def validate_conversation_config():
    default_config = ConversationAdapters.get_default_conversation_config()

    if default_config is None:
        raise HTTPException(status_code=500, detail="Contact the server administrator to set a default chat model.")

    if default_config.model_type == "openai" and not default_config.openai_config:
        raise HTTPException(status_code=500, detail="Contact the server administrator to set a default chat model.")


async def is_ready_to_chat(user: KhojUser):
    user_conversation_config = (await ConversationAdapters.aget_user_conversation_config(user)) or (
        await ConversationAdapters.aget_default_conversation_config()
    )

    if user_conversation_config and user_conversation_config.model_type == "offline":
        chat_model = user_conversation_config.chat_model
        max_tokens = user_conversation_config.max_prompt_size
        if state.offline_chat_processor_config is None:
            logger.info("Loading Offline Chat Model...")
            state.offline_chat_processor_config = OfflineChatProcessorModel(chat_model, max_tokens)
        return True

    if (
        user_conversation_config
        and (user_conversation_config.model_type == "openai" or user_conversation_config.model_type == "anthropic")
        and user_conversation_config.openai_config
    ):
        return True

    raise HTTPException(status_code=500, detail="Set your OpenAI API key or enable Local LLM via Khoj settings.")


def update_telemetry_state(
    request: Request,
    telemetry_type: str,
    api: str,
    client: Optional[str] = None,
    user_agent: Optional[str] = None,
    referer: Optional[str] = None,
    host: Optional[str] = None,
    metadata: Optional[dict] = None,
):
    user: KhojUser = request.user.object if request.user.is_authenticated else None
    client_app: ClientApplication = request.user.client_app if request.user.is_authenticated else None
    subscription: Subscription = user.subscription if user and hasattr(user, "subscription") else None
    user_state = {
        "client_host": request.client.host if request.client else None,
        "user_agent": user_agent or "unknown",
        "referer": referer or "unknown",
        "host": host or "unknown",
        "server_id": str(user.uuid) if user else None,
        "subscription_type": subscription.type if subscription else None,
        "is_recurring": subscription.is_recurring if subscription else None,
        "client_id": str(client_app.name) if client_app else "default",
    }

    if metadata:
        user_state.update(metadata)

    state.telemetry += [
        log_telemetry(
            telemetry_type=telemetry_type, api=api, client=client, app_config=state.config.app, properties=user_state
        )
    ]


def get_next_url(request: Request) -> str:
    "Construct next url relative to current domain from request"
    next_url_param = urlparse(request.query_params.get("next", "/"))
    next_path = "/"  # default next path
    # If relative path or absolute path to current domain
    if is_none_or_empty(next_url_param.scheme) or next_url_param.netloc == request.base_url.netloc:
        # Use path in next query param
        next_path = next_url_param.path
    # Construct absolute url using current domain and next path from request
    return urljoin(str(request.base_url).rstrip("/"), next_path)


def construct_chat_history(conversation_history: dict, n: int = 4, agent_name="AI") -> str:
    chat_history = ""
    for chat in conversation_history.get("chat", [])[-n:]:
        if chat["by"] == "khoj" and chat["intent"].get("type") in ["remember", "reminder"]:
            chat_history += f"User: {chat['intent']['query']}\n"
            chat_history += f"{agent_name}: {chat['message']}\n"
        elif chat["by"] == "khoj" and ("text-to-image" in chat["intent"].get("type")):
            chat_history += f"User: {chat['intent']['query']}\n"
            chat_history += f"{agent_name}: [generated image redacted for space]\n"
    return chat_history


def get_conversation_command(query: str, any_references: bool = False) -> ConversationCommand:
    if query.startswith("/notes"):
        return ConversationCommand.Notes
    elif query.startswith("/help"):
        return ConversationCommand.Help
    elif query.startswith("/general"):
        return ConversationCommand.General
    elif query.startswith("/online"):
        return ConversationCommand.Online
    elif query.startswith("/webpage"):
        return ConversationCommand.Webpage
    elif query.startswith("/image"):
        return ConversationCommand.Image
    elif query.startswith("/automated_task"):
        return ConversationCommand.AutomatedTask
    elif query.startswith("/summarize"):
        return ConversationCommand.Summarize
    # If no relevant notes found for the given query
    elif not any_references:
        return ConversationCommand.General
    else:
        return ConversationCommand.Default


async def agenerate_chat_response(*args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, generate_chat_response, *args)


async def acreate_title_from_query(query: str) -> str:
    """
    Create a title from the given query
    """
    title_generation_prompt = prompts.subject_generation.format(query=query)

    with timer("Chat actor: Generate title from query", logger):
        response = await send_message_to_model_wrapper(title_generation_prompt)

    return response.strip()


async def aget_relevant_information_sources(query: str, conversation_history: dict, is_task: bool, subscribed: bool):
    """
    Given a query, determine which of the available tools the agent should use in order to answer appropriately.
    """

    tool_options = dict()
    tool_options_str = ""

    for tool, description in tool_descriptions_for_llm.items():
        tool_options[tool.value] = description
        tool_options_str += f'- "{tool.value}": "{description}"\n'

    chat_history = construct_chat_history(conversation_history)

    relevant_tools_prompt = prompts.pick_relevant_information_collection_tools.format(
        query=query,
        tools=tool_options_str,
        chat_history=chat_history,
    )

    with timer("Chat actor: Infer information sources to refer", logger):
        response = await send_message_to_model_wrapper(
            relevant_tools_prompt, response_type="json_object", subscribed=subscribed
        )

    try:
        response = response.strip()
        # Remove any markdown json codeblock formatting if present (useful for gemma-2)
        if response.startswith("```json"):
            response = response[7:-3]
        response = json.loads(response)
        response = [q.strip() for q in response["source"] if q.strip()]
        if not isinstance(response, list) or not response or len(response) == 0:
            logger.error(f"Invalid response for determining relevant tools: {response}")
            return tool_options

        final_response = [] if not is_task else [ConversationCommand.AutomatedTask]
        for llm_suggested_tool in response:
            if llm_suggested_tool in tool_options.keys():
                # Check whether the tool exists as a valid ConversationCommand
                final_response.append(ConversationCommand(llm_suggested_tool))

        if is_none_or_empty(final_response):
            final_response = [ConversationCommand.Default]
        return final_response
    except Exception as e:
        logger.error(f"Invalid response for determining relevant tools: {response}")
        return [ConversationCommand.Default]


async def aget_relevant_output_modes(query: str, conversation_history: dict, is_task: bool = False):
    """
    Given a query, determine which of the available tools the agent should use in order to answer appropriately.
    """

    mode_options = dict()
    mode_options_str = ""

    for mode, description in mode_descriptions_for_llm.items():
        # Do not allow tasks to schedule another task
        if is_task and mode == ConversationCommand.Automation:
            continue
        mode_options[mode.value] = description
        mode_options_str += f'- "{mode.value}": "{description}"\n'

    chat_history = construct_chat_history(conversation_history)

    relevant_mode_prompt = prompts.pick_relevant_output_mode.format(
        query=query,
        modes=mode_options_str,
        chat_history=chat_history,
    )

    with timer("Chat actor: Infer output mode for chat response", logger):
        response = await send_message_to_model_wrapper(relevant_mode_prompt, response_type="json_object")

    try:
        response = json.loads(response.strip())

        if is_none_or_empty(response):
            return ConversationCommand.Text

        output_mode = response["output"]
        if output_mode in mode_options.keys():
            # Check whether the tool exists as a valid ConversationCommand
            return ConversationCommand(output_mode)

        logger.error(f"Invalid output mode selected: {output_mode}. Defaulting to text.")
        return ConversationCommand.Text
    except Exception:
        logger.error(f"Invalid response for determining output mode: {response}")
        return ConversationCommand.Text


async def infer_webpage_urls(
    q: str, conversation_history: dict, location_data: LocationData, user: KhojUser
) -> List[str]:
    """
    Infer webpage links from the given query
    """
    location = f"{location_data.city}, {location_data.region}, {location_data.country}" if location_data else "Unknown"
    username = prompts.user_name.format(name=user.get_full_name()) if user.get_full_name() else ""
    chat_history = construct_chat_history(conversation_history)

    utc_date = datetime.utcnow().strftime("%Y-%m-%d")
    online_queries_prompt = prompts.infer_webpages_to_read.format(
        current_date=utc_date,
        query=q,
        chat_history=chat_history,
        location=location,
        username=username,
    )

    with timer("Chat actor: Infer webpage urls to read", logger):
        response = await send_message_to_model_wrapper(online_queries_prompt, response_type="json_object")

    # Validate that the response is a non-empty, JSON-serializable list of URLs
    try:
        response = response.strip()
        urls = json.loads(response)
        valid_unique_urls = {str(url).strip() for url in urls["links"] if is_valid_url(url)}
        if is_none_or_empty(valid_unique_urls):
            raise ValueError(f"Invalid list of urls: {response}")
        return list(valid_unique_urls)
    except Exception:
        raise ValueError(f"Invalid list of urls: {response}")


async def generate_online_subqueries(
    q: str, conversation_history: dict, location_data: LocationData, user: KhojUser
) -> List[str]:
    """
    Generate subqueries from the given query
    """
    location = f"{location_data.city}, {location_data.region}, {location_data.country}" if location_data else "Unknown"
    username = prompts.user_name.format(name=user.get_full_name()) if user.get_full_name() else ""
    chat_history = construct_chat_history(conversation_history)

    utc_date = datetime.utcnow().strftime("%Y-%m-%d")
    online_queries_prompt = prompts.online_search_conversation_subqueries.format(
        current_date=utc_date,
        query=q,
        chat_history=chat_history,
        location=location,
        username=username,
    )

    with timer("Chat actor: Generate online search subqueries", logger):
        response = await send_message_to_model_wrapper(online_queries_prompt, response_type="json_object")

    # Validate that the response is a non-empty, JSON-serializable list
    try:
        response = response.strip()
        # Remove any markdown json codeblock formatting if present (useful for gemma-2)
        if response.startswith("```json") and response.endswith("```"):
            response = response[7:-3]
        response = json.loads(response)
        response = [q.strip() for q in response["queries"] if q.strip()]
        if not isinstance(response, list) or not response or len(response) == 0:
            logger.error(f"Invalid response for constructing subqueries: {response}. Returning original query: {q}")
            return [q]
        return response
    except Exception as e:
        logger.error(f"Invalid response for constructing subqueries: {response}. Returning original query: {q}")
        return [q]


async def schedule_query(q: str, conversation_history: dict) -> Tuple[str, ...]:
    """
    Schedule the date, time to run the query. Assume the server timezone is UTC.
    """
    chat_history = construct_chat_history(conversation_history)

    crontime_prompt = prompts.crontime_prompt.format(
        query=q,
        chat_history=chat_history,
    )

    raw_response = await send_message_to_model_wrapper(crontime_prompt, response_type="json_object")

    # Validate that the response is a non-empty, JSON-serializable list
    try:
        raw_response = raw_response.strip()
        response: Dict[str, str] = json.loads(raw_response)
        if not response or not isinstance(response, Dict) or len(response) != 3:
            raise AssertionError(f"Invalid response for scheduling query : {response}")
        return response.get("crontime"), response.get("query"), response.get("subject")
    except Exception:
        raise AssertionError(f"Invalid response for scheduling query: {raw_response}")


async def extract_relevant_info(q: str, corpus: str, subscribed: bool) -> Union[str, None]:
    """
    Extract relevant information for a given query from the target corpus
    """

    if is_none_or_empty(corpus) or is_none_or_empty(q):
        return None

    extract_relevant_information = prompts.extract_relevant_information.format(
        query=q,
        corpus=corpus.strip(),
    )

    chat_model: ChatModelOptions = await ConversationAdapters.aget_default_conversation_config()

    with timer("Chat actor: Extract relevant information from data", logger):
        response = await send_message_to_model_wrapper(
            extract_relevant_information,
            prompts.system_prompt_extract_relevant_information,
            chat_model_option=chat_model,
            subscribed=subscribed,
        )
    return response.strip()


async def extract_relevant_summary(q: str, corpus: str, subscribed: bool = False) -> Union[str, None]:
    """
    Extract relevant information for a given query from the target corpus
    """

    if is_none_or_empty(corpus) or is_none_or_empty(q):
        return None

    extract_relevant_information = prompts.extract_relevant_summary.format(
        query=q,
        corpus=corpus.strip(),
    )

    chat_model: ChatModelOptions = await ConversationAdapters.aget_default_conversation_config()

    with timer("Chat actor: Extract relevant information from data", logger):
        response = await send_message_to_model_wrapper(
            extract_relevant_information,
            prompts.system_prompt_extract_relevant_summary,
            chat_model_option=chat_model,
            subscribed=subscribed,
        )
    return response.strip()


async def generate_better_image_prompt(
    q: str,
    conversation_history: str,
    location_data: LocationData,
    note_references: List[Dict[str, Any]],
    online_results: Optional[dict] = None,
    model_type: Optional[str] = None,
    subscribed: bool = False,
) -> str:
    """
    Generate a better image prompt from the given query
    """

    today_date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d, %A")
    model_type = model_type or TextToImageModelConfig.ModelType.OPENAI

    if location_data:
        location = f"{location_data.city}, {location_data.region}, {location_data.country}"
        location_prompt = prompts.user_location.format(location=location)
    else:
        location_prompt = "Unknown"

    user_references = "\n\n".join([f"# {item['compiled']}" for item in note_references])

    simplified_online_results = {}

    if online_results:
        for result in online_results:
            if online_results[result].get("answerBox"):
                simplified_online_results[result] = online_results[result]["answerBox"]
            elif online_results[result].get("webpages"):
                simplified_online_results[result] = online_results[result]["webpages"]

    if model_type == TextToImageModelConfig.ModelType.OPENAI:
        image_prompt = prompts.image_generation_improve_prompt_dalle.format(
            query=q,
            chat_history=conversation_history,
            location=location_prompt,
            current_date=today_date,
            references=user_references,
            online_results=simplified_online_results,
        )
    elif model_type == TextToImageModelConfig.ModelType.STABILITYAI:
        image_prompt = prompts.image_generation_improve_prompt_sd.format(
            query=q,
            chat_history=conversation_history,
            location=location_prompt,
            current_date=today_date,
            references=user_references,
            online_results=simplified_online_results,
        )

    chat_model: ChatModelOptions = await ConversationAdapters.aget_default_conversation_config()

    with timer("Chat actor: Generate contextual image prompt", logger):
        response = await send_message_to_model_wrapper(
            image_prompt, chat_model_option=chat_model, subscribed=subscribed
        )
        response = response.strip()
        if response.startswith(('"', "'")) and response.endswith(('"', "'")):
            response = response[1:-1]

    return response


async def send_message_to_model_wrapper(
    message: str,
    system_message: str = "",
    response_type: str = "text",
    chat_model_option: ChatModelOptions = None,
    subscribed: bool = False,
):
    conversation_config: ChatModelOptions = (
        chat_model_option or await ConversationAdapters.aget_default_conversation_config()
    )

    chat_model = conversation_config.chat_model
    max_tokens = (
        conversation_config.subscribed_max_prompt_size
        if subscribed and conversation_config.subscribed_max_prompt_size
        else conversation_config.max_prompt_size
    )
    tokenizer = conversation_config.tokenizer

    if conversation_config.model_type == "offline":
        if state.offline_chat_processor_config is None or state.offline_chat_processor_config.loaded_model is None:
            state.offline_chat_processor_config = OfflineChatProcessorModel(chat_model, max_tokens)

        loaded_model = state.offline_chat_processor_config.loaded_model
        truncated_messages = generate_chatml_messages_with_context(
            user_message=message,
            system_message=system_message,
            model_name=chat_model,
            loaded_model=loaded_model,
            tokenizer_name=tokenizer,
            max_prompt_size=max_tokens,
        )

        return send_message_to_model_offline(
            messages=truncated_messages,
            loaded_model=loaded_model,
            model=chat_model,
            streaming=False,
            response_type=response_type,
        )

    elif conversation_config.model_type == "openai":
        openai_chat_config = conversation_config.openai_config
        api_key = openai_chat_config.api_key
        api_base_url = openai_chat_config.api_base_url
        truncated_messages = generate_chatml_messages_with_context(
            user_message=message,
            system_message=system_message,
            model_name=chat_model,
            max_prompt_size=max_tokens,
            tokenizer_name=tokenizer,
        )

        openai_response = send_message_to_model(
            messages=truncated_messages,
            api_key=api_key,
            model=chat_model,
            response_type=response_type,
            api_base_url=api_base_url,
        )

        return openai_response
    elif conversation_config.model_type == "anthropic":
        api_key = conversation_config.openai_config.api_key
        truncated_messages = generate_chatml_messages_with_context(
            user_message=message,
            system_message=system_message,
            model_name=chat_model,
            max_prompt_size=max_tokens,
            tokenizer_name=tokenizer,
        )

        return anthropic_send_message_to_model(
            messages=truncated_messages,
            api_key=api_key,
            model=chat_model,
        )
    else:
        raise HTTPException(status_code=500, detail="Invalid conversation config")


def send_message_to_model_wrapper_sync(
    message: str,
    system_message: str = "",
    response_type: str = "text",
):
    conversation_config: ChatModelOptions = ConversationAdapters.get_default_conversation_config()

    if conversation_config is None:
        raise HTTPException(status_code=500, detail="Contact the server administrator to set a default chat model.")

    chat_model = conversation_config.chat_model
    max_tokens = conversation_config.max_prompt_size

    if conversation_config.model_type == "offline":
        if state.offline_chat_processor_config is None or state.offline_chat_processor_config.loaded_model is None:
            state.offline_chat_processor_config = OfflineChatProcessorModel(chat_model, max_tokens)

        loaded_model = state.offline_chat_processor_config.loaded_model
        truncated_messages = generate_chatml_messages_with_context(
            user_message=message, system_message=system_message, model_name=chat_model, loaded_model=loaded_model
        )

        return send_message_to_model_offline(
            messages=truncated_messages,
            loaded_model=loaded_model,
            model=chat_model,
            streaming=False,
            response_type=response_type,
        )

    elif conversation_config.model_type == "openai":
        api_key = conversation_config.openai_config.api_key
        truncated_messages = generate_chatml_messages_with_context(
            user_message=message, system_message=system_message, model_name=chat_model
        )

        openai_response = send_message_to_model(
            messages=truncated_messages, api_key=api_key, model=chat_model, response_type=response_type
        )

        return openai_response

    elif conversation_config.model_type == "anthropic":
        api_key = conversation_config.openai_config.api_key
        truncated_messages = generate_chatml_messages_with_context(
            user_message=message,
            system_message=system_message,
            model_name=chat_model,
            max_prompt_size=max_tokens,
        )

        return anthropic_send_message_to_model(
            messages=truncated_messages,
            api_key=api_key,
            model=chat_model,
        )
    else:
        raise HTTPException(status_code=500, detail="Invalid conversation config")


def generate_chat_response(
    q: str,
    meta_log: dict,
    conversation: Conversation,
    compiled_references: List[Dict] = [],
    online_results: Dict[str, Dict] = {},
    inferred_queries: List[str] = [],
    conversation_commands: List[ConversationCommand] = [ConversationCommand.Default],
    user: KhojUser = None,
    client_application: ClientApplication = None,
    conversation_id: int = None,
    location_data: LocationData = None,
    user_name: Optional[str] = None,
) -> Tuple[Union[ThreadedGenerator, Iterator[str]], Dict[str, str]]:
    # Initialize Variables
    chat_response = None
    logger.debug(f"Conversation Types: {conversation_commands}")

    metadata = {}
    agent = AgentAdapters.get_conversation_agent_by_id(conversation.agent.id) if conversation.agent else None

    try:
        partial_completion = partial(
            save_to_conversation_log,
            q,
            user=user,
            meta_log=meta_log,
            compiled_references=compiled_references,
            online_results=online_results,
            inferred_queries=inferred_queries,
            client_application=client_application,
            conversation_id=conversation_id,
        )

        conversation_config = ConversationAdapters.get_valid_conversation_config(user, conversation)
        if conversation_config.model_type == "offline":
            loaded_model = state.offline_chat_processor_config.loaded_model
            chat_response = converse_offline(
                references=compiled_references,
                online_results=online_results,
                user_query=q,
                loaded_model=loaded_model,
                conversation_log=meta_log,
                completion_func=partial_completion,
                conversation_commands=conversation_commands,
                model=conversation_config.chat_model,
                max_prompt_size=conversation_config.max_prompt_size,
                tokenizer_name=conversation_config.tokenizer,
                location_data=location_data,
                user_name=user_name,
                agent=agent,
            )

        elif conversation_config.model_type == "openai":
            openai_chat_config = conversation_config.openai_config
            api_key = openai_chat_config.api_key
            chat_model = conversation_config.chat_model
            chat_response = converse(
                compiled_references,
                q,
                online_results=online_results,
                conversation_log=meta_log,
                model=chat_model,
                api_key=api_key,
                api_base_url=openai_chat_config.api_base_url,
                completion_func=partial_completion,
                conversation_commands=conversation_commands,
                max_prompt_size=conversation_config.max_prompt_size,
                tokenizer_name=conversation_config.tokenizer,
                location_data=location_data,
                user_name=user_name,
                agent=agent,
            )

        elif conversation_config.model_type == "anthropic":
            api_key = conversation_config.openai_config.api_key
            chat_response = converse_anthropic(
                compiled_references,
                q,
                online_results,
                meta_log,
                model=conversation_config.chat_model,
                api_key=api_key,
                completion_func=partial_completion,
                conversation_commands=conversation_commands,
                max_prompt_size=conversation_config.max_prompt_size,
                tokenizer_name=conversation_config.tokenizer,
                location_data=location_data,
                user_name=user_name,
                agent=agent,
            )

        metadata.update({"chat_model": conversation_config.chat_model})

    except Exception as e:
        logger.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    return chat_response, metadata


async def text_to_image(
    message: str,
    user: KhojUser,
    conversation_log: dict,
    location_data: LocationData,
    references: List[Dict[str, Any]],
    online_results: Dict[str, Any],
    subscribed: bool = False,
    send_status_func: Optional[Callable] = None,
):
    status_code = 200
    image = None
    response = None
    image_url = None
    intent_type = ImageIntentType.TEXT_TO_IMAGE_V3

    text_to_image_config = await ConversationAdapters.aget_user_text_to_image_model(user)
    if not text_to_image_config:
        # If the user has not configured a text to image model, return an unsupported on server error
        status_code = 501
        message = "Failed to generate image. Setup image generation on the server."
        yield image_url or image, status_code, message, intent_type.value
        return

    text2image_model = text_to_image_config.model_name
    chat_history = ""
    for chat in conversation_log.get("chat", [])[-4:]:
        if chat["by"] == "khoj" and chat["intent"].get("type") in ["remember", "reminder"]:
            chat_history += f"Q: {chat['intent']['query']}\n"
            chat_history += f"A: {chat['message']}\n"
        elif chat["by"] == "khoj" and "text-to-image" in chat["intent"].get("type"):
            chat_history += f"Q: Prompt: {chat['intent']['query']}\n"
            chat_history += f"A: Improved Prompt: {chat['intent']['inferred-queries'][0]}\n"

    if send_status_func:
        async for event in send_status_func("**Enhancing the Painting Prompt**"):
            yield {ChatEvent.STATUS: event}
    improved_image_prompt = await generate_better_image_prompt(
        message,
        chat_history,
        location_data=location_data,
        note_references=references,
        online_results=online_results,
        model_type=text_to_image_config.model_type,
        subscribed=subscribed,
    )

    if send_status_func:
        async for event in send_status_func(f"**Painting to Imagine**:\n{improved_image_prompt}"):
            yield {ChatEvent.STATUS: event}

    if text_to_image_config.model_type == TextToImageModelConfig.ModelType.OPENAI:
        with timer("Generate image with OpenAI", logger):
            if text_to_image_config.api_key:
                api_key = text_to_image_config.api_key
            elif text_to_image_config.openai_config:
                api_key = text_to_image_config.openai_config.api_key
            elif state.openai_client:
                api_key = state.openai_client.api_key
            auth_header = {"Authorization": f"Bearer {api_key}"} if api_key else {}
            try:
                response = state.openai_client.images.generate(
                    prompt=improved_image_prompt,
                    model=text2image_model,
                    response_format="b64_json",
                    extra_headers=auth_header,
                )
                image = response.data[0].b64_json
                decoded_image = base64.b64decode(image)
            except openai.OpenAIError or openai.BadRequestError or openai.APIConnectionError as e:
                if "content_policy_violation" in e.message:
                    logger.error(f"Image Generation blocked by OpenAI: {e}")
                    status_code = e.status_code  # type: ignore
                    message = f"Image generation blocked by OpenAI: {e.message}"  # type: ignore
                    yield image_url or image, status_code, message, intent_type.value
                    return
                else:
                    logger.error(f"Image Generation failed with {e}", exc_info=True)
                    message = f"Image generation failed with OpenAI error: {e.message}"  # type: ignore
                    status_code = e.status_code  # type: ignore
                    yield image_url or image, status_code, message, intent_type.value
                    return

    elif text_to_image_config.model_type == TextToImageModelConfig.ModelType.STABILITYAI:
        with timer("Generate image with Stability AI", logger):
            try:
                response = requests.post(
                    f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
                    headers={"authorization": f"Bearer {text_to_image_config.api_key}", "accept": "image/*"},
                    files={"none": ""},
                    data={
                        "prompt": improved_image_prompt,
                        "model": text2image_model,
                        "mode": "text-to-image",
                        "output_format": "png",
                        "aspect_ratio": "1:1",
                    },
                )
                decoded_image = response.content
            except requests.RequestException as e:
                logger.error(f"Image Generation failed with {e}", exc_info=True)
                message = f"Image generation failed with Stability AI error: {e}"
                status_code = e.status_code  # type: ignore
                yield image_url or image, status_code, message, intent_type.value
                return

    with timer("Convert image to webp", logger):
        # Convert png to webp for faster loading
        image_io = io.BytesIO(decoded_image)
        png_image = Image.open(image_io)
        webp_image_io = io.BytesIO()
        png_image.save(webp_image_io, "WEBP")
        webp_image_bytes = webp_image_io.getvalue()
        webp_image_io.close()
        image_io.close()

    with timer("Upload image to S3", logger):
        image_url = upload_image(webp_image_bytes, user.uuid)
    if image_url:
        intent_type = ImageIntentType.TEXT_TO_IMAGE2
    else:
        intent_type = ImageIntentType.TEXT_TO_IMAGE_V3
        image = base64.b64encode(webp_image_bytes).decode("utf-8")

    yield image_url or image, status_code, improved_image_prompt, intent_type.value


class ApiUserRateLimiter:
    def __init__(self, requests: int, subscribed_requests: int, window: int, slug: str):
        self.requests = requests
        self.subscribed_requests = subscribed_requests
        self.window = window
        self.slug = slug

    def __call__(self, request: Request):
        # Rate limiting disabled if billing is disabled
        if state.billing_enabled is False:
            return

        # Rate limiting is disabled if user unauthenticated.
        # Other systems handle authentication
        if not request.user.is_authenticated:
            return

        user: KhojUser = request.user.object
        subscribed = has_required_scope(request, ["premium"])

        # Remove requests outside of the time window
        cutoff = datetime.now(tz=timezone.utc) - timedelta(seconds=self.window)
        count_requests = UserRequests.objects.filter(user=user, created_at__gte=cutoff, slug=self.slug).count()

        # Check if the user has exceeded the rate limit
        if subscribed and count_requests >= self.subscribed_requests:
            raise HTTPException(status_code=429, detail="Slow down! Too Many Requests")
        if not subscribed and count_requests >= self.requests:
            if self.requests >= self.subscribed_requests:
                raise HTTPException(
                    status_code=429,
                    detail="Slow down! Too Many Requests",
                )
            raise HTTPException(
                status_code=429,
                detail="We're glad you're enjoying Khoj! You've exceeded your usage limit for today. Come back tomorrow or subscribe to increase your usage limit via [your settings](https://app.khoj.dev/settings).",
            )

        # Add the current request to the cache
        UserRequests.objects.create(user=user, slug=self.slug)


class ConversationCommandRateLimiter:
    def __init__(self, trial_rate_limit: int, subscribed_rate_limit: int, slug: str):
        self.slug = slug
        self.trial_rate_limit = trial_rate_limit
        self.subscribed_rate_limit = subscribed_rate_limit
        self.restricted_commands = [ConversationCommand.Online, ConversationCommand.Image]

    async def update_and_check_if_valid(self, request: Request, conversation_command: ConversationCommand):
        if state.billing_enabled is False:
            return

        if not request.user.is_authenticated:
            return

        if conversation_command not in self.restricted_commands:
            return

        user: KhojUser = request.user.object
        subscribed = has_required_scope(request, ["premium"])

        # Remove requests outside of the 24-hr time window
        cutoff = datetime.now(tz=timezone.utc) - timedelta(seconds=60 * 60 * 24)
        command_slug = f"{self.slug}_{conversation_command.value}"
        count_requests = await UserRequests.objects.filter(
            user=user, created_at__gte=cutoff, slug=command_slug
        ).acount()

        if subscribed and count_requests >= self.subscribed_rate_limit:
            raise HTTPException(status_code=429, detail="Slow down! Too Many Requests")
        if not subscribed and count_requests >= self.trial_rate_limit:
            raise HTTPException(
                status_code=429,
                detail=f"We're glad you're enjoying Khoj! You've exceeded your `/{conversation_command.value}` command usage limit for today. Subscribe to increase your usage limit via [your settings](https://app.khoj.dev/settings).",
            )
        await UserRequests.objects.acreate(user=user, slug=command_slug)
        return


class ApiIndexedDataLimiter:
    def __init__(
        self,
        incoming_entries_size_limit: float,
        subscribed_incoming_entries_size_limit: float,
        total_entries_size_limit: float,
        subscribed_total_entries_size_limit: float,
    ):
        self.num_entries_size = incoming_entries_size_limit
        self.subscribed_num_entries_size = subscribed_incoming_entries_size_limit
        self.total_entries_size_limit = total_entries_size_limit
        self.subscribed_total_entries_size = subscribed_total_entries_size_limit

    def __call__(self, request: Request, files: List[UploadFile] = None):
        if state.billing_enabled is False:
            return

        subscribed = has_required_scope(request, ["premium"])
        incoming_data_size_mb = 0.0
        deletion_file_names = set()

        if not request.user.is_authenticated or not files:
            return

        user: KhojUser = request.user.object

        for file in files:
            if file.size == 0:
                deletion_file_names.add(file.filename)

            incoming_data_size_mb += file.size / 1024 / 1024

        num_deleted_entries = 0
        for file_path in deletion_file_names:
            deleted_count = EntryAdapters.delete_entry_by_file(user, file_path)
            num_deleted_entries += deleted_count

        logger.info(f"Deleted {num_deleted_entries} entries for user: {user}.")

        if subscribed and incoming_data_size_mb >= self.subscribed_num_entries_size:
            raise HTTPException(status_code=429, detail="Too much data indexed.")
        if not subscribed and incoming_data_size_mb >= self.num_entries_size:
            raise HTTPException(
                status_code=429, detail="Too much data indexed. Subscribe to increase your data index limit."
            )

        user_size_data = EntryAdapters.get_size_of_indexed_data_in_mb(user)
        if subscribed and user_size_data + incoming_data_size_mb >= self.subscribed_total_entries_size:
            raise HTTPException(status_code=429, detail="Too much data indexed.")
        if not subscribed and user_size_data + incoming_data_size_mb >= self.total_entries_size_limit:
            raise HTTPException(
                status_code=429, detail="Too much data indexed. Subscribe to increase your data index limit."
            )


class CommonQueryParamsClass:
    def __init__(
        self,
        client: Optional[str] = None,
        user_agent: Optional[str] = Header(None),
        referer: Optional[str] = Header(None),
        host: Optional[str] = Header(None),
    ):
        self.client = client
        self.user_agent = user_agent
        self.referer = referer
        self.host = host


CommonQueryParams = Annotated[CommonQueryParamsClass, Depends()]


def should_notify(original_query: str, executed_query: str, ai_response: str) -> bool:
    """
    Decide whether to notify the user of the AI response.
    Default to notifying the user for now.
    """
    if any(is_none_or_empty(message) for message in [original_query, executed_query, ai_response]):
        return False

    to_notify_or_not = prompts.to_notify_or_not.format(
        original_query=original_query,
        executed_query=executed_query,
        response=ai_response,
    )

    with timer("Chat actor: Decide to notify user of automation response", logger):
        try:
            response = send_message_to_model_wrapper_sync(to_notify_or_not)
            should_notify_result = "no" not in response.lower()
            logger.info(f'Decided to {"not " if not should_notify_result else ""}notify user of automation response.')
            return should_notify_result
        except:
            logger.warning(f"Fallback to notify user of automation response as failed to infer should notify or not.")
            return True


def scheduled_chat(
    query_to_run: str,
    scheduling_request: str,
    subject: str,
    user: KhojUser,
    calling_url: URL,
    job_id: str = None,
    conversation_id: int = None,
):
    logger.info(f"Processing scheduled_chat: {query_to_run}")
    if job_id:
        # Get the job object and check whether the time is valid for it to run. This helps avoid race conditions that cause the same job to be run multiple times.
        job = AutomationAdapters.get_automation(user, job_id)
        last_run_time = AutomationAdapters.get_job_last_run(user, job)

        # Convert last_run_time from %Y-%m-%d %I:%M %p %Z to datetime object
        if last_run_time:
            last_run_time = datetime.strptime(last_run_time, "%Y-%m-%d %I:%M %p %Z").replace(tzinfo=timezone.utc)

            # If the last run time was within the last 6 hours, don't run it again. This helps avoid multithreading issues and rate limits.
            if (datetime.now(timezone.utc) - last_run_time).total_seconds() < 21600:
                logger.info(f"Skipping scheduled chat {job_id} as the next run time is in the future.")
                return

    # Extract relevant params from the original URL
    scheme = "http" if not calling_url.is_secure else "https"
    query_dict = parse_qs(calling_url.query)

    # Pop the stream value from query_dict if it exists
    query_dict.pop("stream", None)

    # Replace the original scheduling query with the scheduled query
    query_dict["q"] = [query_to_run]

    # Replace the original conversation_id with the conversation_id
    if conversation_id:
        query_dict["conversation_id"] = [conversation_id]

    # Construct the URL to call the chat API with the scheduled query string
    encoded_query = urlencode(query_dict, doseq=True)
    url = f"{scheme}://{calling_url.netloc}/api/chat?{encoded_query}"

    # Construct the Headers for the chat API
    headers = {"User-Agent": "Khoj"}
    if not state.anonymous_mode:
        # Add authorization request header in non-anonymous mode
        token = get_khoj_tokens(user)
        if is_none_or_empty(token):
            token = create_khoj_token(user).token
        else:
            token = token[0].token
        headers["Authorization"] = f"Bearer {token}"

    # Call the chat API endpoint with authenticated user token and query
    raw_response = requests.get(url, headers=headers)

    # Stop if the chat API call was not successful
    if raw_response.status_code != 200:
        logger.error(f"Failed to run schedule chat: {raw_response.text}, user: {user}, query: {query_to_run}")
        return None

    # Extract the AI response from the chat API response
    cleaned_query = re.sub(r"^/automated_task\s*", "", query_to_run).strip()
    is_image = False
    if raw_response.headers.get("Content-Type") == "application/json":
        response_map = raw_response.json()
        ai_response = response_map.get("response") or response_map.get("image")
        is_image = False
        if type(ai_response) == dict:
            is_image = ai_response.get("image") is not None
    else:
        ai_response = raw_response.text

    # Notify user if the AI response is satisfactory
    if should_notify(original_query=scheduling_request, executed_query=cleaned_query, ai_response=ai_response):
        if is_resend_enabled():
            send_task_email(user.get_short_name(), user.email, cleaned_query, ai_response, subject, is_image)
        else:
            return raw_response


async def create_automation(
    q: str, timezone: str, user: KhojUser, calling_url: URL, meta_log: dict = {}, conversation_id: int = None
):
    crontime, query_to_run, subject = await schedule_query(q, meta_log)
    job = await schedule_automation(query_to_run, subject, crontime, timezone, q, user, calling_url, conversation_id)
    return job, crontime, query_to_run, subject


async def schedule_automation(
    query_to_run: str,
    subject: str,
    crontime: str,
    timezone: str,
    scheduling_request: str,
    user: KhojUser,
    calling_url: URL,
    conversation_id: int,
):
    # Disable minute level automation recurrence
    minute_value = crontime.split(" ")[0]
    if not minute_value.isdigit():
        # Run automation at some random minute (to distribute request load) instead of running every X minutes
        crontime = " ".join([str(math.floor(random() * 60))] + crontime.split(" ")[1:])

    user_timezone = pytz.timezone(timezone)
    trigger = CronTrigger.from_crontab(crontime, user_timezone)
    trigger.jitter = 60
    # Generate id and metadata used by task scheduler and process locks for the task runs
    job_metadata = json.dumps(
        {
            "query_to_run": query_to_run,
            "scheduling_request": scheduling_request,
            "subject": subject,
            "crontime": crontime,
            "conversation_id": conversation_id,
        }
    )
    query_id = hashlib.md5(f"{query_to_run}_{crontime}".encode("utf-8")).hexdigest()
    job_id = f"automation_{user.uuid}_{query_id}"
    job = await sync_to_async(state.scheduler.add_job)(
        run_with_process_lock,
        trigger=trigger,
        args=(
            scheduled_chat,
            f"{ProcessLock.Operation.SCHEDULED_JOB}_{user.uuid}_{query_id}",
        ),
        kwargs={
            "query_to_run": query_to_run,
            "scheduling_request": scheduling_request,
            "subject": subject,
            "user": user,
            "calling_url": calling_url,
            "job_id": job_id,
            "conversation_id": conversation_id,
        },
        id=job_id,
        name=job_metadata,
        max_instances=2,  # Allow second instance to kill any previous instance with stale lock
    )
    return job


def construct_automation_created_message(automation: Job, crontime: str, query_to_run: str, subject: str):
    # Display next run time in user timezone instead of UTC
    schedule = f'{cron_descriptor.get_description(crontime)} {automation.next_run_time.strftime("%Z")}'
    next_run_time = automation.next_run_time.strftime("%Y-%m-%d %I:%M %p %Z")
    # Remove /automated_task prefix from inferred_query
    unprefixed_query_to_run = re.sub(r"^\/automated_task\s*", "", query_to_run)
    # Create the automation response
    automation_icon_url = f"/static/assets/icons/automation.svg"
    return f"""
    ### ![]({automation_icon_url}) Created Automation
- Subject: **{subject}**
- Query to Run: "{unprefixed_query_to_run}"
- Schedule: `{schedule}`
- Next Run At: {next_run_time}

Manage your automations [here](/automations).
    """.strip()


class ChatEvent(Enum):
    START_LLM_RESPONSE = "start_llm_response"
    END_LLM_RESPONSE = "end_llm_response"
    MESSAGE = "message"
    REFERENCES = "references"
    STATUS = "status"


class MessageProcessor:
    def __init__(self):
        self.references = {}
        self.raw_response = ""

    def convert_message_chunk_to_json(self, raw_chunk: str) -> Dict[str, Any]:
        if raw_chunk.startswith("{") and raw_chunk.endswith("}"):
            try:
                json_chunk = json.loads(raw_chunk)
                if "type" not in json_chunk:
                    json_chunk = {"type": "message", "data": json_chunk}
                return json_chunk
            except json.JSONDecodeError:
                return {"type": "message", "data": raw_chunk}
        elif raw_chunk:
            return {"type": "message", "data": raw_chunk}
        return {"type": "", "data": ""}

    def process_message_chunk(self, raw_chunk: str) -> None:
        chunk = self.convert_message_chunk_to_json(raw_chunk)
        if not chunk or not chunk["type"]:
            return

        chunk_type = ChatEvent(chunk["type"])
        if chunk_type == ChatEvent.REFERENCES:
            self.references = chunk["data"]
        elif chunk_type == ChatEvent.MESSAGE:
            chunk_data = chunk["data"]
            if isinstance(chunk_data, dict):
                self.raw_response = self.handle_json_response(chunk_data)
            elif (
                isinstance(chunk_data, str) and chunk_data.strip().startswith("{") and chunk_data.strip().endswith("}")
            ):
                try:
                    json_data = json.loads(chunk_data.strip())
                    self.raw_response = self.handle_json_response(json_data)
                except json.JSONDecodeError:
                    self.raw_response += chunk_data
            else:
                self.raw_response += chunk_data

    def handle_json_response(self, json_data: Dict[str, str]) -> str | Dict[str, str]:
        if "image" in json_data or "details" in json_data:
            return json_data
        if "response" in json_data:
            return json_data["response"]
        return json_data


async def read_chat_stream(response_iterator: AsyncGenerator[str, None]) -> Dict[str, Any]:
    processor = MessageProcessor()
    event_delimiter = "␃🔚␗"
    buffer = ""

    async for chunk in response_iterator:
        # Start buffering chunks until complete event is received
        buffer += chunk

        # Once the buffer contains a complete event
        while event_delimiter in buffer:
            # Extract the event from the buffer
            event, buffer = buffer.split(event_delimiter, 1)
            # Process the event
            if event:
                processor.process_message_chunk(event)

    # Process any remaining data in the buffer
    if buffer:
        processor.process_message_chunk(buffer)

    return {"response": processor.raw_response, "references": processor.references}


def get_user_config(user: KhojUser, request: Request, is_detailed: bool = False):
    user_picture = request.session.get("user", {}).get("picture")
    is_active = has_required_scope(request, ["premium"])
    has_documents = EntryAdapters.user_has_entries(user=user)

    if not is_detailed:
        return {
            "request": request,
            "username": user.username if user else None,
            "user_photo": user_picture,
            "is_active": is_active,
            "has_documents": has_documents,
            "khoj_version": state.khoj_version,
        }

    user_subscription_state = get_user_subscription_state(user.email)
    user_subscription = adapters.get_user_subscription(user.email)
    subscription_renewal_date = (
        user_subscription.renewal_date.strftime("%d %b %Y")
        if user_subscription and user_subscription.renewal_date
        else (user_subscription.created_at + timedelta(days=7)).strftime("%d %b %Y")
    )
    given_name = get_user_name(user)

    enabled_content_sources_set = set(EntryAdapters.get_unique_file_sources(user))
    enabled_content_sources = {
        "computer": ("computer" in enabled_content_sources_set),
        "github": ("github" in enabled_content_sources_set),
        "notion": ("notion" in enabled_content_sources_set),
    }

    notion_oauth_url = get_notion_auth_url(user)
    current_notion_config = get_user_notion_config(user)
    notion_token = current_notion_config.token if current_notion_config else ""

    selected_chat_model_config = (
        ConversationAdapters.get_conversation_config(user) or ConversationAdapters.get_default_conversation_config()
    )
    chat_models = ConversationAdapters.get_conversation_processor_options().all()
    chat_model_options = list()
    for chat_model in chat_models:
        chat_model_options.append({"name": chat_model.chat_model, "id": chat_model.id})

    search_model_options = adapters.get_or_create_search_models().all()
    all_search_model_options = list()
    for search_model_option in search_model_options:
        all_search_model_options.append({"name": search_model_option.name, "id": search_model_option.id})

    current_search_model_option = adapters.get_user_search_model_or_default(user)

    selected_paint_model_config = ConversationAdapters.get_user_text_to_image_model_config(user)
    paint_model_options = ConversationAdapters.get_text_to_image_model_options().all()
    all_paint_model_options = list()
    for paint_model in paint_model_options:
        all_paint_model_options.append({"name": paint_model.model_name, "id": paint_model.id})

    voice_models = ConversationAdapters.get_voice_model_options()
    voice_model_options = list()
    for voice_model in voice_models:
        voice_model_options.append({"name": voice_model.name, "id": voice_model.model_id})

    if len(voice_model_options) == 0:
        eleven_labs_enabled = False
    else:
        eleven_labs_enabled = is_eleven_labs_enabled()

    selected_voice_model_config = ConversationAdapters.get_voice_model_config(user)

    return {
        "request": request,
        # user info
        "username": user.username if user else None,
        "user_photo": user_picture,
        "is_active": is_active,
        "given_name": given_name,
        "phone_number": str(user.phone_number) if user.phone_number else "",
        "is_phone_number_verified": user.verified_phone_number,
        # user content settings
        "enabled_content_source": enabled_content_sources,
        "has_documents": has_documents,
        "notion_token": notion_token,
        # user model settings
        "search_model_options": all_search_model_options,
        "selected_search_model_config": current_search_model_option.id,
        "chat_model_options": chat_model_options,
        "selected_chat_model_config": selected_chat_model_config.id if selected_chat_model_config else None,
        "paint_model_options": all_paint_model_options,
        "selected_paint_model_config": selected_paint_model_config.id if selected_paint_model_config else None,
        "voice_model_options": voice_model_options,
        "selected_voice_model_config": selected_voice_model_config.model_id if selected_voice_model_config else None,
        # user billing info
        "subscription_state": user_subscription_state,
        "subscription_renewal_date": subscription_renewal_date,
        # server settings
        "khoj_cloud_subscription_url": os.getenv("KHOJ_CLOUD_SUBSCRIPTION_URL"),
        "billing_enabled": state.billing_enabled,
        "is_eleven_labs_enabled": eleven_labs_enabled,
        "is_twilio_enabled": is_twilio_enabled(),
        "khoj_version": state.khoj_version,
        "anonymous_mode": state.anonymous_mode,
        "notion_oauth_url": notion_oauth_url,
    }


def configure_content(
    files: Optional[dict[str, dict[str, str]]],
    regenerate: bool = False,
    t: Optional[state.SearchType] = state.SearchType.All,
    user: KhojUser = None,
) -> bool:
    success = True
    if t == None:
        t = state.SearchType.All

    if t is not None and t in [type.value for type in state.SearchType]:
        t = state.SearchType(t)

    if t is not None and not t.value in [type.value for type in state.SearchType]:
        logger.warning(f"🚨 Invalid search type: {t}")
        return False

    search_type = t.value if t else None

    no_documents = all([not files.get(file_type) for file_type in files])

    if files is None:
        logger.warning(f"🚨 No files to process for {search_type} search.")
        return True

    try:
        # Initialize Org Notes Search
        if (search_type == state.SearchType.All.value or search_type == state.SearchType.Org.value) and files["org"]:
            logger.info("🦄 Setting up search for orgmode notes")
            # Extract Entries, Generate Notes Embeddings
            text_search.setup(
                OrgToEntries,
                files.get("org"),
                regenerate=regenerate,
                user=user,
            )
    except Exception as e:
        logger.error(f"🚨 Failed to setup org: {e}", exc_info=True)
        success = False

    try:
        # Initialize Markdown Search
        if (search_type == state.SearchType.All.value or search_type == state.SearchType.Markdown.value) and files[
            "markdown"
        ]:
            logger.info("💎 Setting up search for markdown notes")
            # Extract Entries, Generate Markdown Embeddings
            text_search.setup(
                MarkdownToEntries,
                files.get("markdown"),
                regenerate=regenerate,
                user=user,
            )

    except Exception as e:
        logger.error(f"🚨 Failed to setup markdown: {e}", exc_info=True)
        success = False

    try:
        # Initialize PDF Search
        if (search_type == state.SearchType.All.value or search_type == state.SearchType.Pdf.value) and files["pdf"]:
            logger.info("🖨️ Setting up search for pdf")
            # Extract Entries, Generate PDF Embeddings
            text_search.setup(
                PdfToEntries,
                files.get("pdf"),
                regenerate=regenerate,
                user=user,
            )

    except Exception as e:
        logger.error(f"🚨 Failed to setup PDF: {e}", exc_info=True)
        success = False

    try:
        # Initialize Plaintext Search
        if (search_type == state.SearchType.All.value or search_type == state.SearchType.Plaintext.value) and files[
            "plaintext"
        ]:
            logger.info("📄 Setting up search for plaintext")
            # Extract Entries, Generate Plaintext Embeddings
            text_search.setup(
                PlaintextToEntries,
                files.get("plaintext"),
                regenerate=regenerate,
                user=user,
            )

    except Exception as e:
        logger.error(f"🚨 Failed to setup plaintext: {e}", exc_info=True)
        success = False

    try:
        if no_documents:
            github_config = GithubConfig.objects.filter(user=user).prefetch_related("githubrepoconfig").first()
            if (
                search_type == state.SearchType.All.value or search_type == state.SearchType.Github.value
            ) and github_config is not None:
                logger.info("🐙 Setting up search for github")
                # Extract Entries, Generate Github Embeddings
                text_search.setup(
                    GithubToEntries,
                    None,
                    regenerate=regenerate,
                    user=user,
                    config=github_config,
                )

    except Exception as e:
        logger.error(f"🚨 Failed to setup GitHub: {e}", exc_info=True)
        success = False

    try:
        if no_documents:
            # Initialize Notion Search
            notion_config = NotionConfig.objects.filter(user=user).first()
            if (
                search_type == state.SearchType.All.value or search_type == state.SearchType.Notion.value
            ) and notion_config:
                logger.info("🔌 Setting up search for notion")
                text_search.setup(
                    NotionToEntries,
                    None,
                    regenerate=regenerate,
                    user=user,
                    config=notion_config,
                )

    except Exception as e:
        logger.error(f"🚨 Failed to setup Notion: {e}", exc_info=True)
        success = False

    try:
        # Initialize Image Search
        if (search_type == state.SearchType.All.value or search_type == state.SearchType.Image.value) and files[
            "image"
        ]:
            logger.info("🖼️ Setting up search for images")
            # Extract Entries, Generate Image Embeddings
            text_search.setup(
                ImageToEntries,
                files.get("image"),
                regenerate=regenerate,
                user=user,
            )
    except Exception as e:
        logger.error(f"🚨 Failed to setup images: {e}", exc_info=True)
        success = False
    try:
        if (search_type == state.SearchType.All.value or search_type == state.SearchType.Docx.value) and files["docx"]:
            logger.info("📄 Setting up search for docx")
            text_search.setup(
                DocxToEntries,
                files.get("docx"),
                regenerate=regenerate,
                user=user,
            )
    except Exception as e:
        logger.error(f"🚨 Failed to setup docx: {e}", exc_info=True)
        success = False

    # Invalidate Query Cache
    if user:
        state.query_cache[user.uuid] = LRU()

    return success


def get_notion_auth_url(user: KhojUser):
    if not NOTION_OAUTH_CLIENT_ID or not NOTION_OAUTH_CLIENT_SECRET or not NOTION_REDIRECT_URI:
        return None
    return f"https://api.notion.com/v1/oauth/authorize?client_id={NOTION_OAUTH_CLIENT_ID}&redirect_uri={NOTION_REDIRECT_URI}&response_type=code&state={user.uuid}"
