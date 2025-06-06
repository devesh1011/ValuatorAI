from typing import Annotated, Dict
from helper.helpers import _crawl_talent_agency
from llama_index.core.tools import FunctionTool


def crawl_talent_agency(
    agency_url: str,
    limit: int = 50,
) -> Dict:
    """
    Crawl a talent agency website to extract information about their talents/influencers.

    Args:
        agency_url (str): The URL of the talent agency website
        limit (int): Maximum number of pages to crawl (default: 50)

    Returns:
        Dict: A dictionary containing:
            - agency_name: Name of the talent agency
            - talents: List of talent information including:
                - name: Talent's name
                - social_links: Dictionary of social media links
                - bio: Short biography
                - categories: List of talent categories
                - stats: Dictionary of social media statistics
    """
    return _crawl_talent_agency(agency_url, limit)


crawl_talent_agency_tool = FunctionTool.from_defaults(crawl_talent_agency)
