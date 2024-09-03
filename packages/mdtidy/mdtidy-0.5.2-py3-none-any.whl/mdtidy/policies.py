import re
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_code_blocks(text):
    if not isinstance(text, str):
        logging.error("Invalid input type. Expected string.")
        raise ValueError("Input text must be a string.")
    
    code_blocks = []
    
    try:
        if "-----------" in text:
            logging.info("Found '-----------' delimiters in text.")
            sections = re.split(r"-----------", text)
            code_blocks += [sec for sec in sections if "CODE:" in sec]
            code_blocks = [re.search(r"CODE:\n(.*?)(?:OUTPUT_TO_USER|CODE:|$)", sec, re.DOTALL).group(1) for sec in code_blocks if re.search(r"CODE:\n(.*)", sec, re.DOTALL)]
        
        code_blocks += re.findall(r"```python.*?\n(.*?)```", text, re.DOTALL)
        
        # Comprehensive cleaning
        code_blocks = [re.sub(r"`+", "", block).strip() for block in code_blocks]
        logging.info(f"Extracted {len(code_blocks)} code blocks.")
    except Exception as e:
        logging.error(f"An error occurred while extracting code blocks: {e}")
        raise RuntimeError(f"An error occurred while extracting code blocks: {e}")
    
    return code_blocks

def analyze_code(text):
    if not isinstance(text, str):
        logging.error("Invalid input type. Expected string.")
        raise ValueError("Input text must be a string.")
    
    try:
        code_blocks = extract_code_blocks(text)
        last_visualization_snippet = None
        unnecessary_head_info = "NA"
        vizsplit_policy = "NA"
        initial_head_info_checked = False
        last_head_info_index = -1
        last_code_block_index = len(code_blocks) - 1
        
        logging.info("Analyzing code for VizSplit policy compliance and unnecessary .head()/.info()...")

        manipulation_keywords = re.compile(
            r"""
            \b(\.groupby|\.merge|\.join|\.concat|\.pivot|\.sort_values|\.sum|\.filter|\.apply|\.transform|\.agg|\.drop|
            \.fillna|\.replace|\.melt|\.rename|\.astype|.query|\.loc|\.iloc|\.reset_index|\.to_datetime|
            \.duplicated|\.drop_duplicates|\.mask|\.where|\.diff|\.isin|\.between|\.nlargest|\.nsmallest|\.where|\.mask|
            \.explode|\.clip|\.round|\.abs|\.pct_change|\.sample|\.eval|\.stack|\.unstack|\.pivot_table|\.rolling|\.expanding|
            \.cumsum|\.cumprod|\.cummax|\.cummin|\.dropna|\.interpolate|\.resample|\.shift|\.str|\.cat|\.swaplevel|
            \.reorder_levels|\.rank|\.assign|\.value_counts)\b
            """,
            re.VERBOSE | re.IGNORECASE
        )

        visualization_keywords = re.compile(r"\b(plot|chart|figure|hist|histogram|scatter|bar|line|pie|altair|matplotlib|seaborn|heatmap|boxplot|violinplot|jointplot|pairplot|displot|kdeplot|distplot|countplot|factorplot|lmplot|catplot|stripplot|swarmplot|regplot|ecdfplot|areaplot|densityplot|treemap|bubble|bubbleplot|geoplot|choropleth|plotly|ggplot|bokeh|vegalite|viz|visualization|graph|box|facet|facetgrid|subplot|subplots)\b", re.IGNORECASE)
        head_info_pattern = re.compile(r"\.head\(\)|\.info\(\)")
        
        for i, block in enumerate(code_blocks):
            cleaned_block = re.sub(r"```python|```", "", block)
            
            # Check for visualization block
            if visualization_keywords.search(cleaned_block):
                logging.info("Visualization code block found.")
                last_visualization_snippet = cleaned_block
                
                # Detect inline data manipulation patterns
                if manipulation_keywords.search(cleaned_block) or "df[" in cleaned_block or ".loc[" in cleaned_block or ".iloc[" in cleaned_block:
                    logging.warning("Data manipulation found in the same block as visualization.")
                    vizsplit_policy = "No"
                else:
                    vizsplit_policy = "Yes"
            
            # Check for head/info calls
            if head_info_pattern.search(cleaned_block):
                if not initial_head_info_checked:
                    initial_head_info_checked = True
                    last_head_info_index = i
                else:
                    last_head_info_index = i

        # Check for unnecessary .head() and .info()
        if last_head_info_index != -1:
            if last_visualization_snippet and last_head_info_index < len(code_blocks) - 1:
                unnecessary_head_info = "No"
            elif last_head_info_index == last_code_block_index:
                unnecessary_head_info = "Yes"
            else:
                unnecessary_head_info = "No"

        # If no plotting code snippet exists, VizSplit Policy is "NA"
        if last_visualization_snippet is None:
            vizsplit_policy = "NA"

        # Prepare the results as a dictionary
        result = {
            "VizSplit Policy Compliance": vizsplit_policy,
            "Unnecessary .head()/.info()": unnecessary_head_info
        }
        
        return result

    except Exception as e:
        logging.error(f"An error occurred while analyzing the code: {e}")
        return {
            "VizSplit Policy Compliance": "NA",
            "Unnecessary .head()/.info()": "NA"
        }
