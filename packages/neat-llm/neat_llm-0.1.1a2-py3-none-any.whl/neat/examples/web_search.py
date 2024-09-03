import asyncio
import json
import re
import textwrap
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from loguru import logger

from neat import neat
from neat.types import LLMModel

ddgs = DDGS()
region = "wt-wt"
safesearch = "moderate"


# In this script we will define a tool that can be used by the LLM to perform a web search using DuckDuckGo. The tool can also fetch the content of a URL.

# First we need to define our functions and wrap them using the `@neat.tool()` decorator.


# Define a tool to search Duck Duck Go and register it using the `@neat.tool()` decorator
@neat.tool()
def search(query: str, max_results: int = 5) -> str:
    """
    Perform a web search using DuckDuckGo and format the results for LLM consumption.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return. Defaults to 5.

    Returns:
        str: A formatted string containing search results.
    """
    results = ddgs.text(
        keywords=query,
        region=region,
        safesearch=safesearch,
        max_results=max_results,
    )
    return _format_web_results(list(results))


def _format_web_results(results: List[Dict[str, str]]) -> str:
    """Format web search results for LLM consumption."""
    formatted_results = []
    for i, result in enumerate(results, 1):
        formatted_result = f"{i}. Title: {result['title']}\n   URL: {result['href']}\n   Summary (Fetch visit link to learn more): {result['body']}\n"
        formatted_results.append(formatted_result)
    return "\n".join(formatted_results)


class ArticleFetcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def fetch_article(self, url: str) -> str:
        """
        Fetch and parse an article from the given URL.

        Args:
            url (str): The URL of the article to fetch.

        Returns:
            Dict[str, Any]: A dictionary containing the parsed article data.
        """
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                response = await client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                return self.format_for_llm(
                    {
                        "url": url,
                        "title": self._extract_title(soup),
                        "content": self._extract_content(soup),
                        "summary": self._generate_summary(self._extract_content(soup)),
                        "domain": self._extract_domain(url),
                    }
                )
        except httpx.HTTPStatusError as e:
            return f"HTTP error occurred: {e}"
        except httpx.RequestError as e:
            return f"An error occurred while requesting {url}: {e}"
        except Exception as e:
            logger.exception(e)
            return f"An unexpected error occurred: {e}"

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the title of the article."""
        title = soup.find("h1")
        return title.text.strip() if title else "No title found"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract the main content of the article."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Find the main content (this is a simplified approach and may need adjustment for different sites)
        main_content = (
            soup.find("article")
            or soup.find("main")
            or soup.find("div", class_="content")
        )

        if main_content:
            paragraphs = main_content.find_all("p")
            content = " ".join(p.text for p in paragraphs)
        else:
            content = soup.get_text()

        return self._clean_text(content)

    def _clean_text(self, text: str) -> str:
        """Clean the extracted text."""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()
        # Remove special characters
        text = re.sub(r"[^\w\s.,!?-]", "", text)
        return text

    def _generate_summary(self, content: str, max_length: int = 200) -> str:
        """Generate a simple summary of the content."""
        sentences = content.split(".")
        summary = ""
        for sentence in sentences:
            if len(summary) + len(sentence) > max_length:
                break
            summary += sentence + "."
        return summary.strip()

    def _extract_domain(self, url: str) -> str:
        """Extract the domain from the URL."""
        parsed_uri = urlparse(url)
        return "{uri.netloc}".format(uri=parsed_uri)

    def format_for_llm(self, article_data: Dict[str, Any]) -> str:
        """
        Format the article data for LLM consumption.

        Args:
            article_data (Dict[str, Any]): The article data to format.

        Returns:
            str: A formatted string representation of the article data.
        """
        if "error" in article_data:
            return f"Error fetching article: {article_data['error']}"

        formatted_data = f"Title: {article_data['title']}\n"
        formatted_data += f"URL: {article_data['url']}\n"
        formatted_data += f"Domain: {article_data['domain']}\n"
        formatted_data += f"Summary: {article_data['summary']}\n\n"
        formatted_data += (
            f"Content: {article_data['content']}..."  # Truncate content for brevity
        )

        return formatted_data


# Class methods must be wrapped in a function.
async def fetch_article_wrapper(url: str) -> str:
    """
    A wrapper tool that fetches and parses an article from the given URL.

    This function acts as a high-level interface to the ArticleFetcher class,
    which is responsible for the actual fetching and parsing of the article.
    The function creates an instance of the ArticleFetcher class and calls
    its fetch_article method with the provided URL. The result is then returned.

    Args:
        url (str): The URL of the article to fetch. The URL should be a valid
            HTTP or HTTPS URL.

    Returns:
        str: A formatted string containing the parsed article data. The string
            includes the title, URL, domain, summary, and content of the article.
            If an error occurs during the fetching or parsing process, the string
            will contain an error message.
    """
    article_fetcher = ArticleFetcher()
    return await article_fetcher.fetch_article(url)


# Add the fetch_article tool using the `add_tool()` method.
neat.add_tool(fetch_article_wrapper)


# use the @neat.alm decorator to define the async assistant
@neat.alm(
    model=LLMModel.GPT_4O_MINI,
    max_iterations=10,
    tools=[
        search,
        fetch_article_wrapper,
    ],
    temperature=0.2,
    enable_conversation=True,
)
async def web_search_assistant():
    return [
        neat.system(
            textwrap.dedent(
                """
            You are an excellent web search assistant that is given the ability to search the web for information and read teh contents of webpages. Please assist the user with their question using your tools.
            
            Your process is this:
            1. Search for a query. You'll then receive a list of results and a brief summary.
            2. Fetch articles from the links that you think are most relevant. You may request to fetch more than one article if you have to. 
            3. IF there are no results that look relevant to the user's question, then please try generating and searching for a new query.
            4. Do 2-4 until you have a satisfying answer.
            5. If you cannot do it within your 10 iterations, then please stop and say that you cannot find an answer.
            
            It's now time to start the conversation.
            
            """
            ).strip()
        ),
    ]


async def main():
    conversation = await web_search_assistant()
    print("Weather Small Talk:")
    print(conversation)


if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(main())
