import ijson
import logging
import sys
from decimal import Decimal

# Set up logging to a file and suppress output to the UI
logging.basicConfig(filename='chatsnip.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Redirect stderr to the logging file
sys.stderr = open('chatsnip.log', 'a')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def extract_chat_from_json_stream(html_file, chat_name):
    logging.info(f"Starting extraction for chat name: {chat_name}")
    
    json_data_str = ''
    capturing = False

    with open(html_file, 'r', encoding='utf-8') as file:
        for line in file:
            if 'var jsonData =' in line:
                logging.info("Found JSON data start in the HTML file.")
                capturing = True
                json_data_start = line.split('var jsonData =', 1)[1].strip()
                json_data_str += json_data_start
                logging.debug(f"Initial JSON data: {json_data_start}")
            elif capturing:
                json_data_str += line.strip()
                if line.strip().endswith('];'):
                    logging.info("Reached the end of JSON data.")
                    json_data_str = json_data_str[:-2] + ']'
                    logging.debug(f"Final JSON data: {json_data_str}")
                    break

    if not json_data_str:
        logging.error("No JSON data found or failed to extract JSON data.")
        return None

    # Log the complete JSON data before attempting to parse
    logging.debug(f"Complete JSON data to be parsed: {json_data_str[:500]}...")

    try:
        chat_data = ijson.items(json_data_str, 'item')
        for item in chat_data:
            title = item.get("title")
            logging.info(f"Checking item with title: {title}")
            
            # Match chat name exactly with the title
            if isinstance(item, dict) and title and title.strip().lower() == chat_name.lower():
                logging.info(f"Found chat with exact title match: {chat_name}")
                return extract_text_content_with_author(item)
    except Exception as e:
        logging.error(f"Failed to decode JSON: {e}")
        return None

    logging.warning(f"Chat named '{chat_name}' was not found in the JSON data.")
    return None

def extract_text_content_with_author(chat_item):
    extracted_text = []

    def recursive_extract(mapping):
        if isinstance(mapping, dict):
            for key, value in mapping.items():
                if key == 'message':
                    if isinstance(value, dict):
                        author_role = value.get('author', {}).get('role', 'unknown')
                        content = value.get('content')
                        if isinstance(content, dict) and 'parts' in content:
                            for part in content['parts']:
                                extracted_text.append(f"{author_role.capitalize()}: {part}")
                        else:
                            logging.warning(f"Skipping message with missing or malformed content: {value}")
                    else:
                        logging.warning(f"Skipping non-dict message value: {type(value)}")
                elif isinstance(value, (dict, list)):
                    recursive_extract(value)
                else:
                    logging.warning(f"Unexpected data type for key '{key}': {type(value)}")
        elif isinstance(mapping, list):
            for item in mapping:
                if isinstance(item, (dict, list)):
                    recursive_extract(item)
                else:
                    logging.warning(f"Skipping non-dict/list item in list: {type(item)}")
        else:
            logging.warning(f"Unexpected data type at top level: {type(mapping)}")

    if isinstance(chat_item.get('mapping'), dict):
        recursive_extract(chat_item['mapping'])
    else:
        logging.warning("No valid 'mapping' found in the chat item.")

    return "\n\n".join(extracted_text)