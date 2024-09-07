# SPDX-FileCopyrightText: 2017-2023 Ivan Habunek et al <ivan@habunek.com>
# SPDX-FileCopyrightText: 2023-2024 Ngô Ngọc Đức Huy <huyngo@disroot.org>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Implement status cache using sqlite."""
import json
import sqlite3
import time
from os import makedirs, path

from witchie import get_cache_path


def get(conn: sqlite3.Connection, table: str, _id: str) -> str | None:
    cur = conn.cursor()
    cur.execute(f'SELECT value FROM {table} WHERE id = ?', (_id,))
    row = cur.fetchone()
    if row is None:
        return None
    return row[0]


def set_cache(conn: sqlite3.Connection, table: str, _id: str, value: str, expiry: float) -> None:
    query_str = f"""INSERT INTO {table}(id, value, expire) VALUES(:id, :value, :expire)
    ON CONFLICT(id) DO UPDATE SET value = :value, expire = :expire
    WHERE id = :id
    """
    with conn:
        conn.execute(query_str, {'id': _id, 'value': value, 'expire': expiry})


def expire(conn: sqlite3.Connection, table: str) -> None:
    query_str = f'DELETE FROM {table} WHERE expire <= ?'
    now = time.monotonic()
    with conn:
        conn.execute(query_str, (now,))


def connect() -> sqlite3.Connection:
    cache_path = get_cache_path()
    if not path.exists(cache_path):
        makedirs(path.dirname(cache_path), exist_ok=True)
        initiate_cache()
    return sqlite3.connect(cache_path)


def cache_status(status: dict):
    table = 'status'
    conn = connect()
    value = json.dumps(status)
    # TODO: make this configurable
    expiry = time.monotonic() + 60  # 1 minute
    set_cache(conn, table, status['id'], value, expiry)


def get_cached_status(status_id: str) -> dict | None:
    table = 'status'
    conn = connect()
    expire(conn, table)
    value = get(conn, table, status_id)
    if value is None:
        return None
    return json.loads(value)


def initiate_cache():
    schema = """
DROP TABLE IF EXISTS status;

CREATE TABLE status(
    id TEXT PRIMARY KEY,
    value TEXT,
    expire FLOAT
);
    """
    cache_path = get_cache_path()
    with sqlite3.connect(cache_path) as conn:
        conn.executescript(schema)
