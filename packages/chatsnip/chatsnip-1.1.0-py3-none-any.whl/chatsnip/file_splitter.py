import os

def split_text_into_files(text, max_lines=2000, output_dir="output", base_filename="split_file"):
    """Splits a large text into multiple files, each containing up to max_lines lines."""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    lines = text.splitlines()
    file_count = 0
    
    for i in range(0, len(lines), max_lines):
        chunk = lines[i:i + max_lines]
        file_count += 1
        output_file_path = os.path.join(output_dir, f"{base_filename}_{file_count}.txt")
        
        try:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write("\n".join(chunk))
            print(f"Created {output_file_path} with {len(chunk)} lines.")  # Debugging output
        except Exception as e:
            print(f"Failed to write to {output_file_path}: {e}")  # Debugging output
            raise
    
    return file_count

def split_and_save_chat(chat_content, output_dir="output", base_filename="split_chat"):
    """Splits a chat content into multiple files if it's too long."""
    print(f"Splitting chat content. Total length: {len(chat_content)} characters.")  # Debugging output
    
    try:
        total_files_created = split_text_into_files(chat_content, max_lines=2000, output_dir=output_dir, base_filename=base_filename)
        print(f"Total files created: {total_files_created}")  # Debugging output
    except Exception as e:
        print(f"Error splitting chat content: {e}")  # Debugging output
        raise

    return total_files_created