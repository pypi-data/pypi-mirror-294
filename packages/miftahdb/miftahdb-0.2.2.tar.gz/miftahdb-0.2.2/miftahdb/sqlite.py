import sqlite3
import logging

from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from sys import version_info
from time import time

logger = logging.getLogger(__name__)


class REQUEST:
    GET = "GET"
    SET = "SET"
    DELETE = "DELETE"
    COMMIT = "COMMIT"
    EXISTS = "EXISTS"
    GET_TTL = "GET_TTL"
    SET_TTL = "SET_TTL"
    RENAME = "RENAME"
    COUNT = "COUNT"
    COUNT_EXPIRE = "COUNT_EXPIRE"
    KEYS = "KEYS"
    PAGINATION = "PAGINATION"
    CLEANUP = "CLEANUP"
    FLUSH_DB = "FLUSH_DB"
    CLOSE = "CLOSE"


class Sqlite:
    def __init__(
        self,
        database: str,
        table_name: str,
        autocommit: bool,
        journal_mode: str,
        synchronous: str,
        encoder,
        workers: int,
    ) -> None:
        assert isinstance(database, str), "database must be str"
        assert isinstance(table_name, str), "table_name must be str"
        assert isinstance(autocommit, bool), "autocommit must be bool"
        assert isinstance(journal_mode, str), "journal_mode must be str"
        assert isinstance(synchronous, str), "synchronous must be str"

        self.database = database
        self.table_name = table_name
        self.autocommit = autocommit
        self.journal_mode = journal_mode
        self.synchronous = synchronous
        self.__encoder = encoder
        self.__workers = ThreadPoolExecutor(workers, "miftahdb")
        self.__lock = Lock()

        self.is_running = True

        self.__table_statement = 'CREATE TABLE IF NOT EXISTS "{}" (k VARCHAR(4096) PRIMARY KEY, v BLOB, expire_time INTEGER DEFAULT NULL) WITHOUT ROWID'.format(
            self.table_name
        )
        self.__index_statement = (
            'CREATE INDEX IF NOT EXISTS idx_expire_time ON "{}" (expire_time)'.format(
                self.table_name
            )
        )
        self.__get_statement = (
            'SELECT v, expire_time FROM "{}" WHERE k = ? LIMIT 1'.format(
                self.table_name
            )
        )
        self.__set_statement = (
            'INSERT OR REPLACE INTO "{}" (k, v, expire_time) VALUES(?,?,?)'.format(
                self.table_name
            )
        )
        self.__delete_statement = 'DELETE FROM "{}" WHERE k = ?'.format(self.table_name)
        self.__exists_statement = (
            'SELECT EXISTS (SELECT 1 FROM "{}" WHERE k = ? LIMIT 1)'.format(
                self.table_name
            )
        )
        self.__get_ttl_statement = (
            'SELECT expire_time FROM "{}" WHERE k = ? LIMIT 1'.format(self.table_name)
        )
        self.__set_ttl_statement = 'UPDATE "{}" SET expire_time = ? WHERE k = ?'.format(
            self.table_name
        )
        self.__rename_statement = 'UPDATE OR IGNORE "{}" SET k = ? WHERE k = ?'.format(
            self.table_name
        )
        self.__count_statement = 'SELECT COUNT(*) FROM "{}" where k LIKE ?'.format(
            self.table_name
        )
        self.__count_expire_statement = 'SELECT COUNT(*) as count FROM "{}" WHERE (expire_time IS NOT NULL AND expire_time <= ?) AND k LIKE ?'.format(
            self.table_name
        )
        self.__keys_statement = 'SELECT k FROM "{}" WHERE k LIKE ?'.format(
            self.table_name
        )
        self.__partition_statement = (
            'SELECT k FROM "{}" WHERE k LIKE ? LIMIT ? OFFSET ?'.format(self.table_name)
        )
        self.__cleanup_statement = 'DELETE FROM "{}" WHERE expire_time IS NOT NULL AND expire_time <= ?'.format(
            self.table_name
        )
        self.__flush_db_statement = 'DROP TABLE "{}"'.format(self.table_name)

        self.__connection: sqlite3.Connection = self.__connect()

    def request(self, request, key: str = None, value=None):
        return self.__workers.submit(self.procces_request, request, key, value)

    def procces_request(self, request, key: str = None, value=None):
        if not self.is_running:
            raise RuntimeError("Database is closed")

        logger.debug("Request={}, key={}".format(request, key))

        if request == REQUEST.GET:
            return self.__get(key)
        elif request == REQUEST.SET:
            return self.__set(key, value)
        elif request == REQUEST.DELETE:
            return self.__delete(key)
        elif request == REQUEST.COMMIT:
            return self.__commit()
        elif request == REQUEST.EXISTS:
            return self.__exists(key)
        elif request == REQUEST.GET_TTL:
            return self.__get_ttl(key)
        elif request == REQUEST.SET_TTL:
            return self.__set_ttl(key, value)
        elif request == REQUEST.RENAME:
            return self.__rename(key, value)
        elif request == REQUEST.COUNT:
            return self.__count(value)
        elif request == REQUEST.COUNT_EXPIRE:
            return self.__count_expire(value)
        elif request == REQUEST.KEYS:
            return self.__keys(value)
        elif request == REQUEST.PAGINATION:
            return self.__pagination(value)
        elif request == REQUEST.CLEANUP:
            return self.__cleanup()
        elif request == REQUEST.FLUSH_DB:
            return self.__flush_db()
        elif request == REQUEST.CLOSE:
            return self.__close(value)
        else:
            raise ValueError("Unknown request {}".format(request))

    def __connect(self):
        try:
            if self.autocommit:
                connection = sqlite3.connect(
                    self.database, isolation_level=None, check_same_thread=False
                )
            else:
                connection = sqlite3.connect(self.database, check_same_thread=False)

            # connection.row_factory = sqlite3.Row
            logger.info("Connected to {}".format(self.database))
        except Exception as e:
            logger.exception(
                "Error while opening sqlite3 for database: {}".format(self.database)
            )
            raise e

        try:
            connection.execute("PRAGMA journal_mode = {}".format(self.journal_mode))
            connection.execute("PRAGMA synchronous = {}".format(self.synchronous))
            connection.execute("PRAGMA temp_store = MEMORY")
            connection.execute("PRAGMA cache_size = -64000")
            connection.execute("PRAGMA mmap_size = 30000000000")
        except Exception as e:
            logger.exception("Error while executing PRAGMA statement")
            raise e

        try:
            self.__check_table(connection)
        except Exception as e:
            logger.exception("Error while checking table")
            raise e

        return connection

    def __get(self, key: str):
        try:
            query = self.__connection.execute(
                self.__get_statement,
                (key,),
            ).fetchone()
            if query:
                print(query)
                expiration_time = query[1]
                if expiration_time is not None and expiration_time < time():
                    self.__delete(key)
                    return None
                return self.__encoder.decode(query[0])
            return None
        except Exception as e:
            logger.exception("GET command exception")
            raise e

    def __set(self, key: str, value):
        with self.__lock:
            try:
                query = self.__connection.execute(
                    self.__set_statement,
                    (
                        key,
                        self.__encoder.encode(value[0]),
                        time() + value[1] if value[1] else None,
                    ),
                )
                if query.rowcount > 0:
                    return True
                else:
                    return False
            except Exception as e:
                logger.exception("SET command exception")
                raise e

    def __delete(self, key: str):
        with self.__lock:
            try:
                query = self.__connection.execute(
                    self.__delete_statement,
                    (key,),
                )
                if query.rowcount > 0:
                    return True
                else:
                    return False
            except Exception as e:
                logger.exception("DELETE command exception")
                raise e

    def __commit(self):
        with self.__lock:
            try:
                self.__connection.commit()
                return True
            except Exception as e:
                logger.exception("COMMIT command exception")
                raise e

    def __exists(self, key: str):
        try:
            query = self.__connection.execute(
                self.__exists_statement,
                (key,),
            ).fetchone()

            return bool(query[0])
        except Exception as e:
            logger.exception("EXISTS command exception")
            raise e

    def __get_ttl(self, key: str):
        try:
            query = self.__connection.execute(
                self.__get_ttl_statement,
                (key,),
            ).fetchone()

            if query:
                return query[0] - time()
            else:
                return 0
        except Exception as e:
            logger.exception("TTL command exception")
            raise e

    def __set_ttl(self, key: str, ttl: int):
        with self.__lock:
            try:
                query = self.__connection.execute(
                    self.__set_ttl_statement,
                    (time() + ttl, key),
                )

                if query.rowcount > 0:
                    return True
                else:
                    return False
            except Exception as e:
                logger.exception("EXPIRE command exception")
                raise e

    def __rename(self, key: str, new_key: str):
        try:
            # TODO: key, new_key NOT new_key, key
            query = self.__connection.execute(
                self.__rename_statement,
                (new_key, key),
            )

            if query.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            logger.exception("RENAME command exception")
            raise e

    def __count(self, like: str):
        try:
            query = self.__connection.execute(
                self.__count_statement,
                (like,),
            ).fetchone()
            if query:
                return query[0]
            else:
                return 0
        except Exception as e:
            logger.exception("COUNT command exception")
            raise e

    def __count_expire(self, like: str):
        try:
            query = self.__connection.execute(
                self.__count_expire_statement,
                (time(), like),
            ).fetchone()
            if query:
                return query[0]
            else:
                return 0
        except Exception as e:
            logger.exception("COUNT command exception")
            raise e

    def __keys(self, like: str):
        try:
            query = self.__connection.execute(
                self.__keys_statement,
                (like,),
            ).fetchall()
            if query:
                return query
            else:
                return None
        except Exception as e:
            logger.exception("KEYS command exception")
            raise e

    def __pagination(self, value):
        limit, page, like = value
        try:
            offset = (page - 1) * limit
            query = self.__connection.execute(
                self.__partition_statement,
                (like, limit, offset),
            ).fetchall()
            if query:
                return query
            else:
                return None
        except Exception as e:
            logger.exception("PARTITION command exception")
            raise e

    def __cleanup(self):
        with self.__lock:
            try:
                self.__connection.execute(
                    self.__cleanup_statement,
                    (time(),),
                )

                return True
            except Exception as e:
                logger.exception("CLEANUP command exception")
                raise e

    def __flush_db(self):
        with self.__lock:
            try:
                self.__connection.execute(self.__flush_db_statement)
                self.__connection.execute(self.__table_statement)
                self.__connection.execute(self.__index_statement)
                return True
            except Exception as e:
                logger.exception("FLUSH_DB command exception")
                raise e

    def __close(self, optimize: bool):
        with self.__lock:
            try:
                if optimize:
                    self.__connection.execute("PRAGMA optimize")
                self.__connection.close()
                logger.info("Connection to {} closed".format(self.database))

                if version_info.minor > 8:
                    self.__workers.shutdown(False, cancel_futures=True)
                else:
                    self.__workers.shutdown(False)

                self.is_running = False
                return True
            except Exception as e:
                logger.exception("CLOSE command exception")
                raise e

    def __check_table(self, connection: sqlite3.Connection):
        try:
            table_exists = (
                connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
                    (self.table_name,),
                ).fetchone()
                is not None
            )

            if table_exists:
                query = connection.execute(
                    "PRAGMA table_info({})".format((self.table_name))
                )
                columns = [row[1] for row in query.fetchall()]

                if "expire_time" not in columns:
                    connection.execute(
                        "ALTER TABLE '{}' ADD COLUMN expire_time INTEGER DEFAULT NULL".format(
                            self.table_name
                        )
                    )
            else:
                connection.execute(self.__table_statement)
                connection.execute(self.__index_statement)

        except Exception:
            logger.exception("Check table error")
