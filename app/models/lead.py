from typing_extensions import NotRequired, TypedDict


class Lead(TypedDict):
    name: str
    signal: list[int]
    sample_count: NotRequired[int]
