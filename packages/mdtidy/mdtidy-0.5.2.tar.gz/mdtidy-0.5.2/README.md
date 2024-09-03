# mdtidy

**mdtidy** is a Python library designed to process conversational AI outputs (specifically GPT and Gemini) into Jupyter Notebooks (.ipynb), while also counting code errors within the content. It's an intuitive tool for transforming raw markdown, code blocks, and conversation data into well-structured Jupyter notebooks, specifically tailored for reviewing AI-generated conversation data and integrating with Google Drive and Google Sheets for enhanced data management.

## Features

- **Markdown to Jupyter Notebook**: Convert markdown content with embedded Python code blocks into a Jupyter Notebook file.
- **Error Counting**: Identify and count common Python error types within the content.
- **Conversation Analysis**: Supports parsing and formatting conversation data from both GPT and Gemini models.
- **Google Drive Integration**: Upload processed notebooks to Google Drive.
- **Google Sheets Integration**: Update Google Sheets with processed conversation data and error counts.

## Installation

Install mdtidy using pip:

```sh
pip install mdtidy
```

## Usage

### Setting Up Chrome Profiles for Gemini and GPT

To use `mdtidy` effectively, you need to set up Chrome profiles for both Gemini and GPT. This allows Selenium to use your Chrome profile for scraping data.

#### Manually Create a New Chrome Profile

1. **Create a New Profile Folder:**
   - Navigate to the Chrome User Data directory:
     - **Windows:** `C:\Users\<Your Username>\AppData\Local\Google\Chrome\User Data`
     - **macOS:** `~/Library/Application Support/Google/Chrome`
     - **Linux:** `~/.config/google-chrome`

2. **Create a New Folder for the Profile:**
   - Inside the `User Data` directory, create a new folder, for example, `Profile 2 Gemini` and `Profile 2 GPT`.

3. **Start Chrome with the New Profile:**
   - Open a terminal or command prompt and start Chrome with the new profile:

     - **Windows:**
       ```sh
       "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\<Your Username>\AppData\Local\Google\Chrome\User Data\Profile 2 Gemini"
       ```

       ```sh
       "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\Users\<Your Username>\AppData\Local\Google\Chrome\User Data\Profile 2 GPT"
       ```

     - **macOS:**
       ```sh
       /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --user-data-dir="~/Library/Application Support/Google/Chrome/Profile 2 Gemini"
       ```

       ```sh
       /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --user-data-dir="~/Library/Application Support/Google/Chrome/Profile 2 GPT"
       ```

     - **Linux:**
       ```sh
       google-chrome --user-data-dir="~/.config/google-chrome/Profile 2 Gemini"
       ```

       ```sh
       google-chrome --user-data-dir="~/.config/google-chrome/Profile 2 GPT"
       ```

4. **Set Up the New Profile:**
   - When Chrome opens, set up the new profile by signing in and configuring it as needed.

After setting up your Chrome profiles and updating the configuration, you can proceed with running the scripts.

### Combined Processor

This example shows how to process both GPT and Gemini conversation data into a structured Jupyter notebook all at once.

```python
from mdtidy.combined_processor import process_conversation

# Trigger the processing of a conversation for both models combined, prompting for required details
process_conversation()
```

### Convert GPT Conversations to Notebook

This example shows how to process GPT conversation data into a structured Jupyter notebook.

```python
from mdtidy.gpt_processor import process_gpt_conversation

# Trigger the processing of a GPT conversation, prompting for required details
process_gpt_conversation()
```

### Convert Gemini Conversations to Notebook

This example details processing Gemini model conversations into a notebook format, integrating error analysis.

```python
from mdtidy.gemini_processor import process_gemini_conversation

# Trigger the processing of a Gemini conversation, prompting for required details
process_gemini_conversation()
```

### Count Code Errors

This function identifies and counts typical Python errors within given content.

```python
from mdtidy.gemini_processor import count_code_errors

# Example content with typical Python errors
input_strings_with_errors = [
    """
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'variable' is not defined

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
"""
]

# Count and display code errors
error_counts = count_code_errors(input_strings_with_errors)
print(error_counts)
```

### Update Google Sheets

This feature is currently under development and will be available in a future release.

Once implemented, it will allow you to update Google Sheets with processed conversation data and error counts.

```python
from mdtidy.update_google_sheets import update_google_sheet

# Update the Google Sheet
update_google_sheet()
```

The `update_google_sheet` function will automatically use the default directory `comp_ana_json` for JSON files and the stored Google Sheets credentials and spreadsheet name from the configuration file (`google_sheets.ini`).

## License

This project is licensed under the MIT License.
