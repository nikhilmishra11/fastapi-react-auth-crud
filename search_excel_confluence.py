"""
Dependencies to run this script:
pip install atlassian-python-api pandas openpyxl xlrd
"""
import os
import pandas as pd
from atlassian import Confluence
import warnings

# Suppress openpyxl warnings if excel files have default styles
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def search_text_in_confluence_excels(
    url: str,
    username: str,
    api_token: str,
    page_id: str,
    search_text: str,
    exact_match: bool = False
):
    """
    Downloads Excel files attached to a Confluence page and checks if a specific 
    text is present in Column 2 of any of the files.
    """
    print("Connecting to Confluence...")
    # 1. Initialize Confluence API client
    # Note: For Confluence Cloud, the base url shouldn't generally include /wiki. 
    # Example: https://your-domain.atlassian.net
    confluence = Confluence(
        url=url,
        username=username,
        password=api_token,
        cloud=True
    )
    
    print(f"Fetching attachments for page ID: {page_id}")
    
    # 2. Get all attachments for the page
    attachments = confluence.get_attachments_from_content(page_id=page_id, start=0, limit=50)
    
    if not attachments or 'results' not in attachments or len(attachments['results']) == 0:
        print("No attachments found on this page.")
        return

    excel_files = []
    
    # 3. Filter and download Excel files
    for attachment in attachments['results']:
        file_name = attachment['title']
        if file_name.lower().endswith('.xlsx') or file_name.lower().endswith('.xls'):
            download_url = attachment['_links']['download']
            download_path = os.path.join(".", file_name)
            
            print(f"Downloading {file_name}...")
            # The atlassian API wraps requests and handles auth natively
            response = confluence.request(path=download_url, method="GET", advanced_mode=True)
            
            with open(download_path, 'wb') as f:
                f.write(response.content)
            
            excel_files.append((file_name, download_path))
            
    if not excel_files:
        print("No Excel files found attached to this page.")
        return
        
    print(f"\nSuccessfully downloaded {len(excel_files)} Excel file(s).")
    print(f"Searching for text: '{search_text}' in Column 2 (Index B)...")
    print("-" * 60)
    
    # 4. Read Excel files and search for the text
    for file_name, file_path in excel_files:
        try:
            # Read excel file (engine is auto-detected by pandas based on extension)
            df = pd.read_excel(file_path)
            
            # Check if dataframe has at least 2 columns
            if len(df.columns) < 2:
                print(f"  [-] {file_name}: Skipped (Has less than 2 columns)")
                continue
                
            # Column 2 corresponds to index 1 (0-indexed)
            col_2_name = df.columns[1]
            
            # 5. Search in column 2
            # We convert everything to string to safely search
            col_data = df[col_2_name].astype(str)
            
            if exact_match:
                # Exact match
                matching_rows = df[col_data.str.strip().str.lower() == search_text.lower()]
            else:
                # Partial match (contains)
                matching_rows = df[col_data.str.contains(search_text, case=False, na=False)]
            
            # 6. Print Results
            if not matching_rows.empty:
                print(f"  [+] FOUND in '{file_name}':")
                for index, row in matching_rows.iterrows():
                    # Print the row number (adding 2 because header is row 1, and pandas index is 0-based)
                    row_number = index + 2 
                    col_2_value = row[col_2_name]
                    print(f"      -> Row {row_number}: Text in Col 2 is '{col_2_value}'")
            else:
                print(f"  [-] {file_name}: No match found.")
                
        except Exception as e:
            print(f"  [!] Error reading {file_name}: {e}")
        finally:
            # 7. Clean up downloaded file so they don't clog up your directory
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    # --- Configuration Variables ---
    # Update these with your real details (or populate from env variables)
    
    # Note: Do not include /wiki at the end for the pure Atlassian API
    CONFLUENCE_URL = "https://your-domain.atlassian.net" 
    CONFLUENCE_USERNAME = "your-email@domain.com"
    CONFLUENCE_API_TOKEN = "your-confluence-api-token"
    
    PAGE_ID = "123456789"
    
    # The text you are looking for in Column 2
    SEARCH_TEXT = "Target phrase"
    
    try:
        search_text_in_confluence_excels(
            url=CONFLUENCE_URL,
            username=CONFLUENCE_USERNAME,
            api_token=CONFLUENCE_API_TOKEN,
            page_id=PAGE_ID,
            search_text=SEARCH_TEXT,
            # Set to True if you only want exact cell matches
            exact_match=False 
        )
    except Exception as e:
        print(f"\nCritical Error occurred: {e}")
