from typing import Union, List
from helper.helpers import _sentiment_score
from llama_index.core.tools import FunctionTool


def sentiment_score(texts: Union[str, List[str]]) -> float:
    """
    Calculate the average sentiment score for a single text or a list of texts using TextBlob.
    The sentiment score ranges from -1.0 (most negative) to 1.0 (most positive).

    Args:
        texts (Union[str, List[str]]): A single text string or a list of text strings to analyze

    Returns:
        float: Average sentiment score for the given text(s)

    Example:
        >>> sentiment_score("Great video!")
        0.8
        >>> comments = ["Great video!", "This was terrible", "I learned a lot"]
        >>> sentiment_score(comments)
        -0.06666666666666667
    """
    return _sentiment_score(texts)


sentiment_score_tool = FunctionTool.from_defaults(sentiment_score)
