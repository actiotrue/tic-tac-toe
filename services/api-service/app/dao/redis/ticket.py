from datetime import timedelta
import uuid

from app.dao.redis.base import RedisDaoBase


class TicketDao(RedisDaoBase):
    async def create(self, user_id: uuid.UUID, ticket: str) -> None:
        """Create a new ticket for a user"""
        await self.redis.setex(
            self.key_schema.ticket_key(ticket), timedelta(minutes=1), str(user_id)
        )
