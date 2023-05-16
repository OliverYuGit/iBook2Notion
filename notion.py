import requests

from config import Config

cfg = Config()

BASE_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {cfg.notion_token}",
    "Notion-Version": cfg.notion_version,
    "Content-Type": "application/json",
}

ICON = {
    "type": "external",
    "external": {
        "url": "https://www.notion.so/icons/book_gray.svg"
    }
}
PARENT = {"database_id": cfg.note_db_id}

CACHE = {}
RETRIES = 0


def get_note_props():
    global RETRIES
    global CACHE
    if RETRIES < 3:
        RETRIES += 1
        url = f"{BASE_URL}/databases/{cfg.note_db_id}"
        response = requests.get(url, headers=HEADERS)
        if response.ok:
            CACHE = response.json()['properties']
        else:
            print("Get note properties failed!")


def get_type(key: str) -> str:
    global CACHE
    if key in CACHE:
        return CACHE[key]['type']
    get_note_props()
    if key in CACHE:
        return CACHE[key]['type']
    else:
        print("Not this property type.")
        return ''


def set_by_type(type, content: str):
    result = None
    if type == "title" or type == "rich_text":
        result = {
            type: [{
                "type": "text",
                "text": {
                    "content": content,
                },
            }]
        }
    if type == "multi_select":
        result = {type: [{"name": value} for value in content.split(',')]}
    if type == "select":
        result = {type: {"name": content}}
    return result


def set_quote_block(highlight: str) -> dict:
    return {
        "object": "block",
        "type": "quote",
        "quote": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": highlight,
                }
            }],
            "color": "default"
        }
    }


def set_empty_block() -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [],
            "color": "default"
        }
    }


def set_callout_block(content: str) -> dict:
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": content
                }
            }],
            "icon": {
                "type": "emoji",
                "emoji": "💡"
            },
            "color": "gray_background"
        }
    }


def create_note(note: dict):
    url = f"{BASE_URL}/pages"

    title_type = get_type(cfg.note_title_field)
    title_content = note['title'] or 'no title'
    location_type = get_type(cfg.note_location_field)
    location_content = note['location'] or '0'

    properties = {
        cfg.note_title_field: set_by_type(title_type, title_content),
        cfg.note_location_field: set_by_type(location_type, location_content)
    }

    custom_fields = cfg.note_custom_fields
    if not custom_fields == {}:
        for key, value in custom_fields.items():
            prop_type = get_type(key)
            if not prop_type == '':
                properties[key] = set_by_type(prop_type, value)

    body = {
        "icon": ICON,
        "parent": PARENT,
        "properties": properties,
        "children": [
            set_quote_block(note['highlight'] or 'No highlight.'),
            set_empty_block(),
            set_callout_block(note['note'] or 'No note.')
        ]
    }
    response = requests.post(url, json=body, headers=HEADERS)
    if response.ok:
        print(f"Note created successfully! Title: {title_content}")
    else:
        print(f"Failed to create note.\n Message: {response.text}")


def get_options(key: str) -> dict:
    if key in CACHE:
        prop = CACHE.get(key, {})
        prop_type = prop.get('type', '')
        if prop_type != '':
            options_d = prop.get(prop_type, {}).get('options', [])
            if any('name' in item for item in options_d):
                return {key + f'({prop_type})': [item.get('name') for item in options_d]}
    return {}        