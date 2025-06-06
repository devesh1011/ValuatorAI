from typing import List, Tuple
from .helper.helpers import _predict_next_video_views
from llama_index.core.tools import FunctionTool


def predict_next_video_views(
    historical_views: List[int],
    confidence_level: float = 0.90,
    interval_type: str = "two-sided",
) -> Tuple[float, float]:
    """
    Predict a one‑ or two‑sided confidence interval for the next video's view count,
    assuming a log‑normal model.

    Args:
        historical_views (List[int]): Past view counts (must be >0)
        confidence_level (float): Coverage for the bound(s) (default 0.90)
        interval_type (str):
            - "lower"      → one‑sided lower bound (L, ∞)
            - "upper"      → one‑sided upper bound (-∞, U)
            - "two-sided" → central interval (L, U)

    Returns:
        Tuple[float, float]:
            Depending on `interval_type`:
              - "lower":      (L, ∞)  with  P(X ≥ L) = confidence_level
              - "upper":      (-∞, U) with  P(X ≤ U) = confidence_level
              - "two-sided": (L, U)  with  P(L ≤ X ≤ U) = confidence_level

    Raises:
        ValueError: if list is empty, contains non‑positive values, or invalid `interval_type`
    """
    return _predict_next_video_views(historical_views, confidence_level, interval_type)


predict_next_video_views_tool = FunctionTool.from_defaults(predict_next_video_views)
