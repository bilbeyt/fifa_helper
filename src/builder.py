"""This module has team builder related class"""
from typing import Tuple, List
from src.db import PlayerAdapter
from src.custom_types import BuilderData, Player


class TeamBuilder:
    """This class is building the team with given budget"""
    def __init__(self, budget: int) -> None:
        """This function initialize the TeamBuilder object"""
        self.budget = budget
        self.adapter = PlayerAdapter()
        self.positions = {
            1: ["GK"],
            2: ["LB", "RB", "LWB", "RWB"],
            3: ["CB", "LCB", "RCB", "CDM", "LDM",
                "RDM", "CM", "LCM", "RCM", "LM", "RM"],
            5: ["CAM", "LAM", "RAM", "LWF", "RWF", "CF", "LCF", "RCF"]
        }

    @staticmethod
    def calculate_budget_and_overall(players: List[Player]) -> Tuple[int, int]:
        """This function returns the budget and total overall for players"""
        spent_budget = sum([p["value"] for p in players])
        team_overall = sum([p["overall"] for p in players])
        return spent_budget, team_overall

    def build(self) -> BuilderData:
        """This function returns the team and build statistics"""
        team: List[Player] = []
        total_spent = 0
        available_budget = self.budget
        team_overall: int = 0
        for count, positions in self.positions.items():
            average_budget = available_budget // (11 - len(team))
            players = self.adapter.search_table_by_value_and_positions(
                positions, average_budget)
            chosen_players: List[Player] = players[:count]
            spent_budget, player_overall = \
                self.calculate_budget_and_overall(chosen_players)
            team_overall += player_overall
            available_budget -= spent_budget
            total_spent += spent_budget
            team += chosen_players
        data: BuilderData = {
            "team": team,
            "overall": team_overall // 11,
            "spent": total_spent,
            "remaining": available_budget
        }
        return data
