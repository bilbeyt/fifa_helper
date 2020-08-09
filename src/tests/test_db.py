"""Tests for db related operations in this module"""
from src.db import PlayerAdapter


def test_db_connect_error():
    """Case: Connection error"""
    adapter = PlayerAdapter()
    adapter.host = "loremipsumdolarsitamet"
    adapter.start_connection()
    assert adapter.conn is None

def test_db_execute():
    """Case: Execution error on db"""
    adapter = PlayerAdapter()
    statement = """SELECT * FROM lorem"""
    res = adapter.execute_query(statement)
    assert res == []
