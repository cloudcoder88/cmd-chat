from abc import ABC, abstractmethod


class ClientRenderer(ABC):

    @abstractmethod
    def print_message(self, message: str) -> str:
        raise NotImplementedError("Need to implement print_message")

    @abstractmethod
    def clear_console(self) -> None:
        """Clear the client console (platform-specific)."""
        raise NotImplementedError("Need to implement clear_console")

    @abstractmethod
    def print_ip(self, ip: str) -> str:
        raise NotImplementedError("Need to implement print_ip")

    @abstractmethod
    def print_username(self, username: str) -> str:
        raise NotImplementedError("Need to implement print_username")

    @abstractmethod
    def print_chat(self, response) -> None:
        """Render chat payload (response is expected to be a mapping with 'messages' and 'users_in_chat')."""
        raise NotImplementedError("Need to implement print_chat")
