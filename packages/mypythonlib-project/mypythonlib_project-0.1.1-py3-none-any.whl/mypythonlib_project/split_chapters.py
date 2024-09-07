#!/usr/bin/env python3
import os
import re

def split_into_chapters(text):
    # Split the text by chapter markers, retaining the markers
    chapter_splits = re.split(r'(@@.*?@@)', text, flags=re.DOTALL)
    chapters = []

    # We don't need to remove the first split part as we're retaining the full content with markers
    # Iterate over the chapter splits and merge titles with their content
    for i in range(1, len(chapter_splits), 2):
        chapter_title = chapter_splits[i].strip()
        chapter_content = chapter_splits[i + 1].strip() if (i + 1) < len(chapter_splits) else ''
        # Concatenate the title and content
        formatted_chapter = f"{chapter_title}\n\n{chapter_content}"
        chapters.append(formatted_chapter)

    return chapters

def process_text_file(input_file_path, output_directory, info_output_directory):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # If no @@ markers are found, export the full text to the next folder
    if '@@' not in text:
        output_file_path = os.path.join(output_directory, os.path.basename(input_file_path))
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text.strip())
        print(f"No chapter markers found. Full text exported to: {output_file_path}")
        return

    # Extract and save book info before the first @@ marker
    book_info = text.split('@@', 1)[0].strip()
    info_file_path = os.path.join(info_output_directory, os.path.basename(input_file_path).replace('.txt', '_info.txt'))
    with open(info_file_path, 'w', encoding='utf-8') as info_file:
        info_file.write(book_info)
    print(f"Book info saved to: {info_file_path}")

    # Start processing from the first @@ marker
    text = text.split('@@', 1)[1]
    text = '@@' + text  # Add the marker back to the beginning

    chapters = split_into_chapters(text)

    for index, chapter in enumerate(chapters):
        output_file_name = f"Chapitre_{index + 1}.txt"  # Keep the original file naming format
        output_file_path = os.path.join(output_directory, output_file_name)
        
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(chapter.strip())
        print(f"Processed file saved to: {output_file_path}")

def process_directory(input_directory, output_directory, info_output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    if not os.path.exists(info_output_directory):
        os.makedirs(info_output_directory)

    for file_name in sorted(os.listdir(input_directory)):  # Sort files to process them in order
        if file_name.endswith('.txt'):
            input_file_path = os.path.join(input_directory, file_name)
            print(f"Processing {file_name}...")
            process_text_file(input_file_path, output_directory, info_output_directory)
            print(f"Processed file: {file_name}")

if __name__ == "__main__":
    input_directory = os.path.join("../", 'txt_processed/1-page_nb_cln')
    output_directory = os.path.join("../", 'txt_processed/2-chapter_split')
    info_output_directory = os.path.join("../", 'txt_processed/10-book_info')

    process_directory(input_directory, output_directory, info_output_directory)
    print("Script completed")
