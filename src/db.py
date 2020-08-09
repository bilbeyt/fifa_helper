"""This module is created for db operations"""
import logging
from typing import List, Any

import mysql.connector

import conf
from utils import create_player_list
from custom_types import Player, PlayerTuple, PlayerCreateTuple


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class DBAdapter:
    """This class is an adapter for database"""
    def __init__(self) -> None:
        """This function initialize the db adapter"""
        self.username = conf.DB_USER
        self.__password = conf.DB_PASS
        self.db_name = conf.DB
        self.host = conf.DB_HOST
        self.port = conf.DB_PORT
        self.conn: Any = None

    def start_connection(self) -> None:
        """This function starts the connection for db"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host, port=self.port, user=self.username,
                passwd=self.__password, db=self.db_name, autocommit=True)
        except mysql.connector.Error as err:
            logger.exception(err)

    def execute_query(self, statement: str,
                      fetch_type: str = "") -> List[PlayerTuple]:
        """This function executes the statement given and returns the result"""
        try:
            self.start_connection()
            if self.conn.is_connected():
                cursor = self.conn.cursor()
                cursor.execute(statement)
                if fetch_type == "list":
                    return cursor.fetchall()
        except mysql.connector.Error as error:
            logger.exception(error)
        finally:
            if self.conn.is_connected():
                cursor.close()
                self.conn.close()
        return []


class PlayerAdapter(DBAdapter):
    """This class is related with player db table"""

    def create_table(self) -> None:
        """This function creates the player table"""
        statement = """
        CREATE TABLE IF NOT EXISTS player(
            id INT PRIMARY KEY,
            name VARCHAR(255),
            age INT,
            nationality VARCHAR(255),
            club VARCHAR(255),
            photo TEXT,
            overall INT,
            value FLOAT,
            position VARCHAR(3),
            INDEX (name, nationality, club)
        );
        """
        self.execute_query(statement)

    def search_table(self, word: str) -> List[Player]:
        """This function search for word in fields name, nationality,
        club and returns players"""
        statement = f"""
        SELECT name, age, nationality, club, photo, overall, value
        FROM player 
        WHERE name LIKE '%{word}%' OR 
            nationality LIKE '%{word}%' OR 
            club LIKE '%{word}%'
        ORDER BY overall DESC
        """
        records = self.execute_query(statement, "list")
        fields = ["name", "age", "nationality",
                  "club", "photo", "overall", "value"]
        players = create_player_list(records, fields)
        return players

    def search_table_by_value_and_positions(self,
                                            given_positions: List[str],
                                            value: int) -> List[Player]:
        """This function search players with given position and value
        and returns players"""
        positions: str = ""
        if len(given_positions) > 1:
            positions = str(tuple(given_positions))
        else:
            positions = str(tuple(given_positions)).replace(",", "")
        statement = f"""
        SELECT name, age, nationality, club, photo, overall, value, position
        FROM player 
        WHERE value <= {value} AND
        position IN {positions}
        ORDER BY overall DESC
        """
        records = self.execute_query(statement, "list") or []
        fields = ["name", "age", "nationality", "club",
                  "photo", "overall", "value", "position"]
        players = create_player_list(records, fields)
        return players

    def bulk_create(self, tuples: List[PlayerCreateTuple]) -> None:
        """This function bulk create players with given people tuples"""
        values = ", ".join([str(tup) for tup in tuples])
        statement = "INSERT IGNORE INTO player (id, name, age, nationality, " +\
        f"club, photo, overall, value, position) VALUES {values}"
        self.execute_query(statement)
