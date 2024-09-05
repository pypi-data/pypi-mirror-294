from typing import Any, Dict, List, TypedDict

from .constants import LOG_LEVELS


class SlackMessage(TypedDict):
    title: str
    text: str
    link: str
    users_list: List[str]  # format : ["<@U018E5C3B2Q>"]
    log_level: str


def get_section_schema(text: str) -> Dict[Any, Any]:
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text,
        },
    }


def get_header_schema(text: str) -> Dict[Any, Any]:
    return {
        "type": "header",
        "text": {"type": "plain_text", "text": text, "emoji": True},
    }


def generate_blocks(title: str, text: str, users: str, link: str) -> List[Any]:
    blocks = []
    if title:
        header_section = get_header_schema(text=title)
        blocks.append(header_section)
        blocks.append({"type": "divider"})
    if text:
        text_section = get_section_schema(text)
        blocks.append(text_section)
    if link:
        blocks.append(get_section_schema(link))
    if users:
        blocks.append(get_section_schema(users))
    return blocks


def get_log_message(message_dict: SlackMessage) -> List[Any]:
    log_level = LOG_LEVELS[message_dict.get("log_level", "DEBUG")]
    title = message_dict.get("title", "")
    link = message_dict.get("link", "")
    users_list = message_dict.get("users_list", [])
    text = message_dict.get("text", "")

    users = " ".join(users_list)
    link = f"<{link}|View Request>".format(link=link) if link else ""
    return [{"color": log_level, "blocks": generate_blocks(title, text, users, link)}]
