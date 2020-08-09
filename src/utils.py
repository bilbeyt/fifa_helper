"""This module includes helper functions for application"""
def field_storage_parser(obj):
    """This function handles the post data"""
    params = {}
    for key in obj.keys():
        params[key] = obj[key].value
    return params

def create_player_list(records, fields):
    """This function change tuples to list of dicts using fields"""
    players = []
    for record in records:
        player = {}
        for idx, field in enumerate(fields):
            player[field] = record[idx]
        players.append(player)
    return players
