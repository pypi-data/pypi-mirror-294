#!/usr/bin/env python3
import os
import re
from num2words import num2words

def replace_numbers_with_words(text):
    log_entries = []
    text, additional_log_entries = process_text_before_replacement(text)
    log_entries.extend(additional_log_entries)

    def replace_number(match):
        number = int(match.group())
        words = num2words(number, lang='fr')
        log_entries.append(f"{number}: {words}")
        return words

    text = re.sub(r'\b([0-9]{1,6})\b', replace_number, text)
    return text, log_entries


def process_text_before_replacement(text):
    log_entries = []
    text = re.sub(r'(\d+)[\s]*?(h|hr)', lambda match: f"{match.group(1)} heure", text)
    log_entries.append("Replaced 'h' or 'hr' with 'heure' when preceded by a number")
    return text, log_entries


def process_text_file(input_file_path, output_file_path, log_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    cleaned_text, log_entries = replace_numbers_with_words(text)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write("\n".join(log_entries))


def process_directory(input_directory, output_directory, log_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.txt'):
            input_file_path = os.path.join(input_directory, file_name)
            output_file_path = os.path.join(output_directory, file_name)
            log_file_path = os.path.join(log_directory, f'log_{os.path.splitext(file_name)[0]}.txt')

            print(f"Processing {file_name}...")
            process_text_file(input_file_path, output_file_path, log_file_path)
            print(f"Processed file saved as {output_file_path}")


if __name__ == "__main__":
    input_directory = os.path.join("../", "txt_processed/3-paragraph_fix")
    output_directory = os.path.join("../", "txt_processed/4-numbers_replaced")
    log_directory = os.path.join(output_directory, "logs")

    process_directory(input_directory, output_directory, log_directory)
    print("Script completed")
