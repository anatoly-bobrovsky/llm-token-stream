"""Pydantic schema for message representation."""

from pydantic import BaseModel


class Message(BaseModel):
    """
    Schema representing a message.

    Attributes:
        id (int): Unique identifier for the message.
        text (str): Content of the message.
    """

    id: int
    text: str
