import sqlite3
from threading import Lock


class DB:
    def __init__(self, name="skin.db"):
        self._db = sqlite3.connect(name, check_same_thread=False)
        self._db.execute("CREATE TABLE IF NOT EXISTS skin ( "
                         "username VARCHAR(64),"
                         "sha VARCHAR(64)"
                         ") ")
        self._db.commit()
        self._lock = Lock()

    def get_skin_by_user(self, username: str) -> str:
        result = self._db.execute("SELECT sha FROM skin WHERE username = ?", (username,)).fetchall()
        if len(result) == 0:
            return ""
        else:
            return result[0][0]

    def insert_skin(self, username: str, skin: str) -> bool:
        self._lock.acquire()
        user = self._db.execute("SELECT * FROM skin WHERE username = ?", (username,)).fetchall()
        update = False
        if len(user) == 0:
            self._db.execute("INSERT INTO skin (username, sha) VALUES (?, ?)", (username, skin))
        else:
            self._db.execute("UPDATE skin SET sha = ? WHERE username = ?", (skin, username))
            update = True
        self._db.commit()
        self._lock.release()
        return update
