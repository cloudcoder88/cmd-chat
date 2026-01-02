from typing import Optional
from .models import Message, UserSession
from .logger import logger


class MessageStore:
    def __init__(self):
        self._messages: list[Message] = []

    def add(self, message: Message) -> None:
        self._messages.append(message)
        logger.info(f"Message added: {message.id} from {message.username}")

    def get_all(self) -> list[Message]:
        return self._messages.copy()

    def clear(self) -> None:
        count = len(self._messages)
        self._messages.clear()
        logger.info(f"Cleared {count} messages")

    def count(self) -> int:
        return len(self._messages)


class UserSessionStore:
    def __init__(self):
        self._sessions: dict[str, UserSession] = {}

    def add(self, session: UserSession) -> None:
        self._sessions[session.user_id] = session
        logger.info(f"Session created: {session.user_id} ({session.username})")

    def get(self, user_id: str) -> Optional[UserSession]:
        return self._sessions.get(user_id)

    def update_activity(self, user_id: str) -> None:
        if session := self._sessions.get(user_id):
            session.update_activity()

    def remove(self, user_id: str) -> None:
        if user_id in self._sessions:
            del self._sessions[user_id]
            logger.info(f"Session removed: {user_id}")

    def cleanup_stale(self, timeout_seconds: int = 3600) -> int:
        stale_ids = [
            uid for uid, s in self._sessions.items() if s.is_stale(timeout_seconds)
        ]
        for uid in stale_ids:
            del self._sessions[uid]
        if stale_ids:
            logger.info(f"Cleaned up {len(stale_ids)} stale sessions")
        return len(stale_ids)

    def get_all(self) -> list[UserSession]:
        return list(self._sessions.values())

    def count(self) -> int:
        return len(self._sessions)

    def username_exists(self, username: str) -> bool:
        return any(s.username == username for s in self._sessions.values())
