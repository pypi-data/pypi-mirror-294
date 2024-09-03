import re
import logging

def golden_response(response_text):
    """
    Processes markdown text to remove output blocks and tag Python code blocks sequentially.

    Parameters:
        response_text (str): The markdown text to be processed.

    Returns:
        str: The processed markdown text with modifications.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Regular expression to find code blocks and stdout blocks
    pattern_code = re.compile(r"```python\?.*?```", re.DOTALL)
    pattern_stdout = re.compile(r"```text\?.*?```", re.DOTALL)

    try:
        # Log the start of processing
        logging.info("Starting to process the response text for modifications.")

        # Remove stdout blocks
        cleaned_text = re.sub(pattern_stdout, '', response_text)
        logging.info("Standard output blocks removed.")

        # Replace code blocks with <Code n>
        code_count = 1
        def replace_code(match):
            nonlocal code_count
            replacement = f"<Code {code_count}>"
            code_count += 1
            return replacement

        final_text = re.sub(pattern_code, replace_code, cleaned_text)
        logging.info("Code blocks replaced with sequential tags.")

        # Log the successful end of processing
        logging.info("Processing completed successfully.")
        return final_text

    except Exception as e:
        # Log an error if something goes wrong
        logging.error(f"An error occurred during processing: {e}")
        raise