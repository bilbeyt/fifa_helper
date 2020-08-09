"""Tests for player create functionalities"""
import os
import pandas as pd
from player_creator import PlayerCreator


def test_player_creator():
    """Player Creator Test Case"""
    filename = os.path.abspath("data/data.csv")
    creator = PlayerCreator(filename)
    creator.parse_csv()
    assert isinstance(creator.csv_data, pd.DataFrame)
    tuples = creator.create_object_tuples()
    assert isinstance(tuples, list)
    creator.create_players(tuples[:100], 10)
