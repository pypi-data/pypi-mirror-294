import re
import json
import logging
import sys
import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from configparser import ConfigParser
from typing import Optional, List, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_FILE = 'config.ini'
SCOPES = ['https://www.googleapis.com/auth/drive']

def log_error(error_message):
    with open('process_gemini_conversation_error_log.txt', 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_message}\n")

def get_input(prompt: str) -> str:
    try:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            raise SystemExit
        return user_input
    except KeyboardInterrupt:
        raise SystemExit

def get_persisted_value(key: str) -> Optional[str]:
    if not os.path.exists(CONFIG_FILE):
        return None
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config.get('DEFAULT', key, fallback=None)

def save_persisted_value(key: str, value: str) -> None:
    config = ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    config['DEFAULT'][key] = value
    try:
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        logging.info(f"{key} saved to config file.")
    except IOError as e:
        logging.error(f"Error saving {key}: {e}")

def get_valid_input(prompt: str, validation_fn: callable, error_message: str) -> str:
    while True:
        user_input = get_input(prompt)
        if validation_fn(user_input):
            return user_input
        else:
            logging.error(error_message)

def setup_selenium_driver(profile_key: str):
    chrome_profile_path = get_persisted_value(profile_key)
    if not chrome_profile_path:
        chrome_profile_path = get_valid_input(
            f"Please enter the path to your Chrome profile for {profile_key}: ",
            lambda x: os.path.exists(x),
            "Invalid path. Please enter a valid Chrome profile path."
        )
        save_persisted_value(profile_key, chrome_profile_path)

    options = Options()
    options.add_argument(f'user-data-dir={chrome_profile_path}')
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    service = Service("chromedriver.exe")
    return webdriver.Chrome(service=service, options=options)

def get_conversation_html(driver, url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    page_source = driver.page_source
    driver.quit()
    return BeautifulSoup(page_source, 'html.parser')

def parse_and_order_elements(elements):
    return sorted(elements, key=lambda x: int(re.search(r'^(\d+):', x.attrs['data-sourcepos']).group(1)))

def convert_code_to_backticks(text):
    return text.replace('<code>', '`').replace('</code>', '`')

def clean_response(response):
    for caution in response.find_all("div", class_="code-block-decoration footer"):
        caution.decompose()
    return response

def format_table(table):
    rows = table.find_all('tr')
    formatted_table = "| " + " | ".join([th.get_text(strip=True) for th in rows[0].find_all('th')]) + " |\n"
    formatted_table += "|---" * len(rows[0].find_all('th')) + "|\n"
    for row in rows[1:]:
        formatted_table += "| " + " | ".join([td.get_text(strip=True) for td in row.find_all('td')]) + " |\n"
    return formatted_table

def extract_list_items(ul):
    items = ul.find_all('li')
    return "\n".join([f"- `{item.find('code').get_text(strip=True)}`" for item in items])

def extract_and_save_charts(response, conversation_index, folder_path):
    chart_res = response.find_all('vega-lite-chart', class_='ng-star-inserted')
    saved_images = []
    saved_image_data = []
    for image_index, chart in enumerate(chart_res, start=1):
        img_tag = chart.find('img')
        if img_tag and img_tag.get('src') and 'base64,' in img_tag['src']:
            base64_str = img_tag['src'].split('base64,')[1]
            img_data = base64.b64decode(base64_str)
            filename = os.path.join(folder_path, f"output_image_{conversation_index}_{image_index}.png")
            with open(filename, "wb") as file:
                file.write(img_data)
            logging.info(f"Image saved successfully as {filename}")
            saved_images.append(filename)
            saved_image_data.append(f"data:image/png;base64,{base64_str}")
    return saved_images, saved_image_data

def extract_conversations(soup, folder_path):
    user_queries = soup.find_all('div', class_='query-content')
    queries = [query.find('h2', class_='query-text').text.strip() for query in user_queries]
    assistant_responses = soup.find_all('div', class_='response-container-content')
    
    conversations = []
    code_outputs = []
    all_saved_images = []
    all_saved_image_data = []
    
    for i, response in enumerate(assistant_responses):
        response = clean_response(response)
        elements = parse_and_order_elements(response.find_all(attrs={"data-sourcepos": True}))

        response_elements = []
        for element in elements:
            position = int(re.search(r'^(\d+):', element.attrs['data-sourcepos']).group(1))
            if element.name == 'code' and element.has_attr('data-test-id') and element['data-test-id'] == 'code-content' and element['role'] == 'text':
                response_elements.append({'type': 'code', 'content': element.get_text(), 'position': position})
            elif element.name == 'p':
                text_content = BeautifulSoup(convert_code_to_backticks(str(element)), 'html.parser').get_text()
                response_elements.append({'type': 'text', 'content': text_content, 'position': position})
            elif element.name == 'ul':
                response_elements.append({'type': 'list', 'content': extract_list_items(element), 'position': position})
            elif element.name == 'table':
                response_elements.append({'type': 'table', 'content': format_table(element), 'position': position})

        saved_images, saved_image_data = extract_and_save_charts(response, i+1, folder_path)
        all_saved_images.extend(saved_images)
        all_saved_image_data.extend(saved_image_data)
        
        # Extract code outputs
        code_output_spans = response.find_all('span', text='Code output')
        turn_code_output = ""
        for span in code_output_spans:
            output_pre = span.find_next('pre')
            if output_pre:
                output = output_pre.find('code').text.strip()
                turn_code_output += output + "\n\n"
        code_outputs.append(turn_code_output)
        
        conversations.append({
            'query': queries[i],
            'responses': response_elements,
            'images': saved_images,
            'image_data': saved_image_data
        })
    
    return conversations, code_outputs, all_saved_images, all_saved_image_data

def count_code_errors(input_strings):
    error_types = [
        'AttributeError', 'ValueError', 'ModuleNotFoundError',
        'FileNotFoundError', 'KeyError', 'TypeError',
        'NameError', 'SyntaxError', 'CouldNotFindError'
    ]

    total_error_counts = {error: 0 for error in error_types}
    turn_error_counts = []

    for idx, input_string in enumerate(input_strings):
        error_counts = {error: 0 for error in error_types}
        tracebacks = re.findall(r'Traceback \(most recent call last\):.*?(?=\n\n|\Z)', input_string, re.DOTALL)

        for traceback in tracebacks:
            for error in error_types:
                if f"{error}:" in traceback:
                    error_counts[error] += 1
                    total_error_counts[error] += 1

        turn_error_counts.append((f"Turn {idx + 1}", error_counts))

    error_title = "Error Counts Across {} Turn{}".format(len(input_strings), "s" if len(input_strings) > 1 else "")
    error_table = pd.DataFrame(
        {error: [turn_error_counts[i][1][error] for i in range(len(input_strings))] for error in error_types},
        index=[f"Turn {i+1}" for i in range(len(input_strings))]
    ).T
    error_table_md = error_table.to_markdown(index=True, numalign="left", stralign="left")

    print(f"\n{error_title}")
    print("-" * len(error_title))
    print(error_table_md)

    if all(count == 0 for count in total_error_counts.values()):
        summary = "\nNo errors found across all turns.\n"
    else:
        summary = "\nSummary of Total Error Counts\n" + "-" * 30 + "\n"
        summary += "\n".join([f"- {error}: {count}" for error, count in total_error_counts.items() if count > 0])

    print(summary)

    return total_error_counts

def create_notebook(conversations, documents, output_file, all_saved_images, all_saved_image_data):
    logging.info("Creating Google Colab notebook...")
    cells = []
    title = "MULTI-TURN" if len(conversations) > 1 else "SINGLE-TURN"
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [title + '\n']})

    chart_index = 0
    for idx, conversation in enumerate(conversations):
        turn_number = idx + 1
        turn_markdown = f"Turn {turn_number}\n\nQuery {turn_number}: {conversation['query']}\n\n"
        query_data_markdown = ""
        for i, link in enumerate(documents):
            query_data_markdown += f"Data {i+1}: {link}\n" if len(documents) > 1 else f"Data: {link}\n"

        cells.append({"cell_type": "markdown", "metadata": {}, "source": [turn_markdown + query_data_markdown]})

        for element in sorted(conversation['responses'], key=lambda x: x['position']):
            if element['type'] == 'code':
                cells.append({
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [element['content']]
                })
            elif element['type'] in ['text', 'list', 'table']:
                content = element['content']
                if "table_charteditcontent_copydownload" in content:
                    if chart_index < len(all_saved_image_data):
                        content = content.replace("table_charteditcontent_copydownload", f"![Chart Image]({all_saved_image_data[chart_index]})")
                        chart_index += 1
                    else:
                        content = content.replace("table_charteditcontent_copydownload", "[[CHART_PLACEHOLDER]]")
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [content + '\n']
                })

    if chart_index < len(all_saved_image_data):
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": ["Additional charts that were not explicitly placed in the conversation:\n"]
        })
        for i in range(chart_index, len(all_saved_image_data)):
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"![Additional Chart Image]({all_saved_image_data[i]})\n"]
            })

    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8",
                "name": "python",
                "version": "3.8.5",
                "mimetype": "text/x-python",
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "file_extension": ".py"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(notebook_content, file, ensure_ascii=False, indent=2)
        logging.info(f"Notebook '{output_file}' has been created successfully.")
    except IOError as e:
        logging.error(f"Error writing notebook file: {e}")
        raise

def get_drive_credentials_path() -> str:
    credentials_path = get_persisted_value('DriveCredentialsPath')
    if not credentials_path:
        credentials_path = get_valid_input("Enter the path to your Google Drive API credentials file: ", os.path.exists, "Invalid path. Please enter a valid file path.")
        save_persisted_value('DriveCredentialsPath', credentials_path)
    return credentials_path

def upload_folder_to_drive(folder_path: str, raters_id: str, credentials_path: str) -> None:
    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
        drive_service = build('drive', 'v3', credentials=credentials)
        logging.info("Successfully authenticated with Google Drive.")

        raters_folder_name = f"rater_{raters_id}"
        raters_folder_id = get_drive_folder_id(drive_service, raters_folder_name)

        if not raters_folder_id:
            raters_folder_id = create_drive_folder(drive_service, raters_folder_name)

        logging.info(f"Rater's folder ID for '{raters_folder_name}': {raters_folder_id}")

        folder_name = os.path.basename
        folder_name = os.path.basename(folder_path)
        logging.info(f"Uploading folder '{folder_name}' to Google Drive under folder ID '{raters_folder_id}'...")

        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [raters_folder_id]
        }
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        logging.info(f"Created folder '{folder_name}' on Google Drive with ID: {folder_id}")

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                logging.info(f"Uploading file '{file_path}' to Google Drive...")
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)
                drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                logging.info(f"Uploaded file '{file_name}' to Google Drive.")

        logging.info(f"Uploaded folder '{folder_name}' to Google Drive successfully!")

    except Exception as e:
        logging.error(f"An error occurred while uploading the folder to Google Drive: {e}")
        raise

def create_drive_folder(drive_service, folder_name: str, parent_id: Optional[str] = None) -> str:
    try:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            folder_metadata['parents'] = [parent_id]

        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
        logging.info(f"Folder '{folder_name}' created on Google Drive with ID: {folder.get('id')}")
        return folder.get('id')
    except Exception as e:
        logging.error(f"An error occurred while creating the folder on Google Drive: {e}")
        raise

def get_drive_folder_id(drive_service, folder_name: str) -> Optional[str]:
    try:
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        if items:
            logging.info(f"Found existing folder '{folder_name}' on Google Drive.")
            return items[0]['id']
        else:
            logging.info(f"Folder '{folder_name}' does not exist on Google Drive.")
            return None
    except Exception as e:
        logging.error(f"An error occurred while checking for the folder on Google Drive: {e}")
        return None

def validate_gemini_url(url):
    pattern = r'^https://g.co/gemini/share/[a-zA-Z0-9]+$'
    return bool(re.match(pattern, url))

def process_gemini_conversation(url: str = None):
    try:
        if url is None:
            url = get_valid_input(
                "Enter the Gemini conversation URL (or type 'exit' to quit): ",
                validate_gemini_url,
                "Invalid URL. Please enter a valid Gemini conversation URL in the format 'https://g.co/gemini/share/{id}'."
            )

        raters_id = get_persisted_value('RatersID')
        if raters_id:
            while True:
                use_stored_id = get_input(f"Continue with stored rater's ID '{raters_id}'? (yes/no): ").strip().lower()
                if use_stored_id in {'yes', 'no'}:
                    break
                else:
                    logging.error("Please enter 'yes' or 'no'.")
            if use_stored_id == 'no':
                raters_id = None

        while not raters_id:
            rater_id = get_input("Enter the rater's ID (numbers only): ")
            if rater_id.isdigit():
                save_persisted_value('RatersID', rater_id)
                raters_id = rater_id
            else:
                logging.error("Invalid rater's ID. Please enter numbers only.")

        while True:
            row_id = get_input("Enter the row ID (numbers only): ")
            if row_id.isdigit():
                break
            else:
                logging.error("Invalid row ID. Please enter numbers only.")

        folder_path = f"ID_{row_id}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        logging.info("Fetching conversation data...")
        driver = setup_selenium_driver('gemini_chrome_profile_path')
        soup = get_conversation_html(driver, url)
        logging.info("Successfully fetched data from URL.")

        logging.info("Successfully parsed conversation data.")
        conversations, code_outputs, all_saved_images, all_saved_image_data = extract_conversations(soup, folder_path)

        num_turns = len(conversations)
        logging.info(f"Number of conversation turns is {num_turns}.")

        while True:
            try:
                num_documents = int(get_input("Enter the number of documents used: "))
                if num_documents > 0:
                    break
                else:
                    logging.error("Number of documents must be a positive integer.")
            except ValueError:
                logging.error("Invalid input. Please enter a positive integer.")

        documents = []
        for i in range(num_documents):
            while True:
                document_link = get_input(f"Enter link for Document {i+1} (must be a valid Google Drive link): ")
                if re.match(r'^https://drive\.google\.com/file/d/[\w-]+/view\?usp=sharing$', document_link):
                    documents.append(document_link)
                    break
                else:
                    logging.error("Invalid document link. Please enter a valid Google Drive URL in the format 'https://drive.google.com/file/d/{file_id}/view?usp=sharing'.")

        output_file = os.path.join(folder_path, f"Gemini_rater_{raters_id}_ID_{row_id}.ipynb")
        create_notebook(conversations, documents, output_file, all_saved_images, all_saved_image_data)

        logging.info("\n")
        count_code_errors(code_outputs)

        while True:
            upload_to_drive_prompt = get_input("Do you want to upload the folder to Google Drive now? (yes/no): ").strip().lower()
            if upload_to_drive_prompt in {'yes', 'no'}:
                break
            else:
                logging.error("Please enter 'yes' or 'no'.")

        if upload_to_drive_prompt == 'yes':
            drive_credentials_path = get_drive_credentials_path()
            upload_folder_to_drive(folder_path, raters_id, drive_credentials_path)

        print("Thank you for using the Gemini conversation processor. Goodbye!")

    except SystemExit:
        log_error("Process exited normally.")
        print("You have exited the process. You can start again later if you wish.")
    except Exception as e:
        log_error(f"An unexpected error occurred: {str(e)}")
        print("An unexpected error occurred. Please check the error log for details.")
