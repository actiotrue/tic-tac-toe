class KeySchema:
    """
    Methods to generate key names for Redis data structures.

    These key names are used by the DAO classes. This class therefore contains
    a reference to all possible key names used by this application.
    """

    def leaderboard_key(self) -> str:
        return "leaderboard"

    def ticket_key(self, ticket: str) -> str:
        return f"ws_ticket:{ticket}"
