import logging
from psycopg2 import connect
from psycopg2.extras import DictCursor


LOG = logging.getLogger(__name__)

class DatabaseAccessor:
    def __init__(self, host, port, database, user, password):
        self._cur = None
        self._db = None
        self.db_host = host
        self.db_port = port
        self.db_database = database
        self.db_user = user
        self.db_pass = password

    def _connect(self):
        if self._db is None:
            self._db = self._make_connection()
            self._db.set_session(readonly=False, autocommit=True)
        return self._db

    def _cursor(self):
        if self._cur is None or self._db is None:
            self._cur = self._connect().cursor(cursor_factory=DictCursor)
        return self._cur

    def _create_cursor(self):
        return self._connect().cursor(cursor_factory=DictCursor)

    def execute(self, sql, paras=None):
        """Execute an insertion"""
        self._cursor().execute(sql, paras)

    def do_fetch(self, sql, paras=None):
        cur = self._cursor()
        cur.execute(sql, paras)
        return cur.fetchall()

    def commit_changes(self):
        """Commit changes made to the DB"""
        if self._db:
            LOG.info('Saving changes to %s', self._db.dsn)
            self._db.commit()

    def _make_connection(self):
        LOG.debug(
            "Connecting to DB as %s at %s", self.db_user, self.db_host)
        conn = connect(
            host=self.db_host,
            dbname=self.db_database,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass
            )
        return conn

    def __enter__(self):
        return self

    def __exit__(self, *args):
        try:
            if self._db:
                self._db.close()
        except Exception as err:  # pylint: disable=broad-except
            LOG.error(err)
        self._db = None
