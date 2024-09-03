import sys
from chatsnip.extractor import extract_chat_from_json_stream  # Import from extractor.py
import logging

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_chat.py <html_file> <chat_name> [output_file]")
    else:
        html_file = sys.argv[1]
        chat_name = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None

        extracted_text = extract_chat_from_json_stream(html_file, chat_name)

        if extracted_text:
            extracted_text_str = "\n\n".join(extracted_text)
            if output_file:
                try:
                    with open(output_file, 'w', encoding='utf-8') as out_file:
                        out_file.write(extracted_text_str)
                    print(f"Chat content saved to {output_file}")
                except Exception as e:
                    logging.error(f"Failed to save chat content: {e}")
            else:
                print(extracted_text_str)  # Output to console if no output file is specified
        else:
            print(f"Chat named '{chat_name}' was not found in the JSON data.")