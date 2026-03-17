#Create AI Webcrapping tool
#Search the web
import http.client
import json
import os
import httpx
import asyncio
from dotenv import load_dotenv

from utils import clean_html_to_txt
from mcp.server.fastmcp import FastMCP


load_dotenv()



mcp = FastMCP("docs")

SERPER_URL = "https://google.serper.dev/search"
async def search_web(query: str) -> dict | None:

    payload = json.dumps({
    "q": query,
    "num": 2
    })
    headers = {
    'X-API-KEY': os.getenv("SERPER_API_KEY"),
    'Content-Type': 'application/json'
    }
    #conn = http.client.HTTPSConnection("google.serper.dev")
    async with httpx.AsyncClient() as client:
        try:
            print(f"DEBUG: Searching Serper for: {query}")
            response = await client.post(
                SERPER_URL,
                headers=headers,
                data=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"DEBUG: Serper Search Error: {e}")
            raise e

        #conn.request("POST", "/search", payload, headers)
        
    
    



#step 2 Open official document

async def fetch_url(url: str):
    #client
    async with httpx.AsyncClient() as client:
        # Most documentation sites require GET, not POST
        print(f"DEBUG: Fetching URL: {url}")
        response = await client.get(
            url,
            timeout=30.0,
            follow_redirects=True
        )
        #parse and clean data
        cleaned_response = clean_html_to_txt(response.text)
        #return clean data
        return cleaned_response

# Step Read documentation and write code accordingly
docs_urls = {
    "langchain": "https://python.langchain.com/docs/",
    "llama-index": "https://docs.llamaindex.ai/en/stable/",
    "openai": "https://platform.openai.com/docs/",
    "uv":"https://docs.astral.sh/uv/",
}

@mcp.tool()
async def get_docs(query: str, library: str ):
    if library not in docs_urls:
        raise ValueError(f"Library {library} not found!")

    query = f"site:{docs_urls[library]} {query}"

    results = await search_web(query)

    if len(results["organic"]) == 0:
        return "No Result found!"

    tex_parts = []

    for result in results["organic"]:
        link = result.get("link", "")

        raw = await fetch_url(link)
        if raw:
            labeled = f"SOURCE: {link}\n{raw}"
            print("SOURCE", link)
            tex_parts.append(labeled)
    return "\n\n".join(tex_parts)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()


    
    

