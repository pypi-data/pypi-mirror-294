from typing import Literal
from typing_extensions import assert_never

from aijson import register_action

LIST_FORMAT = Literal["comma", "newline", "space", "bullet points"]


@register_action
def extract_list(
    text: str,
    valid_values: list[str] | None = None,
    list_format: LIST_FORMAT = "bullet points",
) -> list[str]:
    """
    Extract `text` into a list of strings, splitting it by either commas, newlines, spaces, or bullet points.
    """
    if list_format == "comma":
        candidates = text.split(",")
    elif list_format == "newline":
        candidates = text.split("\n")
    elif list_format == "space":
        candidates = text.split(" ")
    elif list_format == "bullet points":
        candidates = text.split("-")
    else:
        assert_never(list_format)
        # raise ValueError(f"Invalid list_format: {inputs.list_format}")

    choices = []
    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate:
            continue
        if valid_values and candidate not in valid_values:
            continue
        choices.append(candidate)
    return choices
