"""
Dependencies to run this script:
pip install langchain langchain-google-genai langchain-community atlassian-python-api beautifulsoup4 lxml
"""
import os
from langchain_community.document_loaders.confluence import ConfluenceLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter

def summarize_confluence(
    confluence_url: str,
    confluence_username: str,
    confluence_api_token: str,
    gemini_api_key: str,
    page_ids: list[str] = None,
    space_key: str = None
):
    """
    Reads data from Confluence and summarizes it using Google Gemini and LangChain.
    """
    # 1. Provide Gemini API key to the environment so the Langchain Module can pick it up
    os.environ["GOOGLE_API_KEY"] = gemini_api_key

    print("Authenticating and loading data from Confluence...")
    
    # 2. Initialize Confluence Loader class
    loader = ConfluenceLoader(
        url=confluence_url,
        username=confluence_username,
        api_key=confluence_api_token
    )
    
    # 3. Load documents (by page ID or Space Key)
    if page_ids:
        docs = loader.load(page_ids=page_ids, include_attachments=False, limit=50)
    elif space_key:
        docs = loader.load(space_key=space_key, include_attachments=False, limit=50)
    else:
        raise ValueError("Either page_ids or space_key must be provided")
        
    print(f"Successfully loaded {len(docs)} document(s) from Confluence.")

    # 4. Split the documents into manageable chunks to respect Gemini token limits and avoid huge blocks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000
    )
    split_docs = text_splitter.split_documents(docs)

    print("Initializing Google Gemini model...")
    # 5. Initialize Google Gemini 1.5 Pro via LangChain integration
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro", 
        temperature=0.3,
        max_retries=2
    )
    
    # 6. Set up the summarization chain. 
    # 'map_reduce' chain type is ideal here: summarizes chunks individually and then summarizes those summaries.
    print("Starting summarization process...")
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    
    # 7. Execute the chain
    result = chain.invoke(split_docs)
    
    return result["output_text"]

if __name__ == "__main__":
    # --- Configuration Variables ---
    # Update these with your real details (or populate from env variables like python-dotenv)
    
    CONFLUENCE_URL = "https://your-domain.atlassian.net/wiki"
    CONFLUENCE_USERNAME = "your-email@domain.com"
    CONFLUENCE_API_TOKEN = "your-confluence-api-token" # Generate via Atlassian Account Settings -> Security
    
    GEMINI_API_KEY = "your-gemini-api-key" # Generate via Google AI Studio
    
    # Find the Page ID in your Confluence URL or Page Information properties
    PAGE_IDS = ["123456789"] 
    
    try:
        summary = summarize_confluence(
            confluence_url=CONFLUENCE_URL,
            confluence_username=CONFLUENCE_USERNAME,
            confluence_api_token=CONFLUENCE_API_TOKEN,
            gemini_api_key=GEMINI_API_KEY,
            page_ids=PAGE_IDS
        )
        print("\n" + "="*50)
        print("CONFLUENCE PAGE SUMMARY:")
        print("="*50)
        print(summary)
        
    except Exception as e:
        print(f"Error occurred during generation: {e}")
