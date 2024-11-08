"""Custom data structures for managing message chunks with priority."""

from queue import PriorityQueue
from typing import Generator

from .enums import Signal


class MessageChunksQueue:
    """A class to manage a queue of message chunks with priority handling."""

    def __init__(self):
        """Initialize the MessageChunksQueue with default values."""
        self.in_progress_message_priority = 0
        self.priority_queue = PriorityQueue()

    def __head_message_priority(self) -> int:
        """Retrieve the priority of the head message in the queue.

        Returns:
            int: The priority of the head message.
        """
        return self.priority_queue.queue[0][0]

    def push(self, chunk: str, message_priority: int, chunk_priority: int) -> None:
        """Add a new chunk to the priority queue.

        Args:
            chunk (str): The message chunk to be added.
            message_priority (int): The priority of the message.
            chunk_priority (int): The priority of the chunk.
        """
        self.priority_queue.put((message_priority, chunk_priority, chunk))

    def flush(self) -> Generator[str]:
        """Retrieve chunks from the queue based on their priority.

        Yields:
            str: The next chunk in the queue that matches the current message priority.
        """
        while not self.priority_queue.empty():
            if self.__head_message_priority() != self.in_progress_message_priority:
                return

            chunk = self.priority_queue.get()[-1]

            if chunk == Signal.END.value:
                self.in_progress_message_priority += 1  # ready to progress to the next message
                continue

            yield chunk
