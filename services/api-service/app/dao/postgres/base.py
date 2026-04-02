from asyncpg import Connection


class SqlDaoBase:
    """Base class for all sql daos"""

    def __init__(self, db_connection: Connection):
        self.db = db_connection
