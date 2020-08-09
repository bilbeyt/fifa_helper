"""This module is a script handling player creation"""
import os
import logging
from typing import List
import pandas as pd
from src.custom_types import PlayerCreateTuple
from src.db import PlayerAdapter


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class PlayerCreator:
    """This class loads the data and creates players"""
    def __init__(self, filename: str) -> None:
        """This function initialize PlayerCreator"""
        self.filename = filename
        self.adapter = PlayerAdapter()
        self.csv_data: pd.DataFrame = None

    def parse_csv(self) -> None:
        """This function reads and parses the csv and fill null
        values with ''"""
        csv_data = pd.read_csv(self.filename)
        csv_data["Value"] = csv_data["Value"]\
            .replace({"[Kk]": "*1e3", "[Mm]": "*1e6", "€": ""},
                     regex=True)\
            .map(pd.eval).astype(int)
        fields = [
            "ID", "Name", "Age", "Nationality", "Club",
            "Photo", "Overall", "Value", "Position"]
        csv_data = csv_data[fields]
        csv_data = csv_data.fillna("")
        self.csv_data = csv_data

    def create_object_tuples(self) -> List[PlayerCreateTuple]:
        """This function returns player tuples created from dataframe"""
        return list(self.csv_data.itertuples(index=False, name=None))

    def create_players(self, players: List[PlayerCreateTuple],
                       batch_size: int) -> None:
        """This function create players with given batch size"""
        self.adapter.create_table()
        batches = [
            players[i:i+batch_size] for i in range(0, len(players), batch_size)]
        for batch in batches:
            self.adapter.bulk_create(batch)

if __name__ == "__main__":
    logger.info("Create player operation started")
    creator = PlayerCreator(os.path.abspath("data/data.csv"))
    creator.parse_csv()
    logger.info("CSV file processed")
    player_tuples = creator.create_object_tuples()
    logger.info("Creating players")
    creator.create_players(player_tuples, 1000)
    logger.info("Create player operation finished")
