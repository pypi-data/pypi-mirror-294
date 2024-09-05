from datetime import datetime
from typing import Any, Dict, List

from PS3838._utils.errors import ConfigError, ParameterError


def check_config(config : Dict[str, str] = None) -> None:
    if not config:
        raise ConfigError("Config is missing")
    if not isinstance(config, dict):
        raise ConfigError("Config must be a dictionary")
    if not all(key in config for key in ["username", "password"]):
        raise ConfigError("Config must contain 'username' and 'password' keys")
    if not all(isinstance(config[key], str) for key in ["username", "password"]):
        raise ConfigError("Config 'username' and 'password' must be strings")



def check_list_matches(list_matches : List[Dict[str, Any]] = None) -> None:
    # check if the list of matches is provided
    if not list_matches:
        raise ParameterError("The list of matches is missing")
    
    # check if the list of matches is a list
    if not isinstance(list_matches, list):
        raise ParameterError("The list of matches must be a list")
    
    # check each match in the list of matches
    for match in list_matches:
        check_match(match)


def check_match(match : Dict[str, Any]) -> None:
    if not isinstance(match, dict):
        raise ParameterError("Each match must be a dictionary")
    if "id" not in match.keys():
        raise ParameterError(f"Parameter \"id\" is missing for at least one match")
    if "starts" not in match.keys():
        raise ParameterError(f"Parameter \"starts\" is missing for at least one match")
    if "league" not in match.keys():
        raise ParameterError(f"Parameter \"league\" is missing for at least one match")
    if "home" not in match.keys():
        raise ParameterError(f"Parameter \"team1\" is missing for at least one match")
    if "away" not in match.keys():
        raise ParameterError(f"Parameter \"team2\" is missing for at least one match")
    if "line_id" not in match.keys():
        raise ParameterError(f"Parameter \"line_id\" is missing for at least one match")
    if "odds" not in match.keys():
        raise ParameterError(f"Parameter \"odds\" is missing for at least one match")
    if "result" not in match.keys():
        raise ParameterError(f"Parameter \"result\" is missing for at least one match")
    if "amount" not in match.keys():
        raise ParameterError(f"Parameter \"amount\" is missing for at least one match")
    if type(match["id"]) != int:
        raise ParameterError(f"\"id\" for match  {match['home']} - {match['away']}  must be an integer")
    if type(match["starts"]) != str:
        raise ParameterError(f"\"starts\" for match  {match['home']} - {match['away']}  must be a datetime object")
    if type(match["league"]) != int:
        raise ParameterError(f"\"league\" for match  {match['home']} - {match['away']}  must be an integer")
    if type(match["home"]) != str:
        raise ParameterError(f"\"home\" for match  {match['home']} - {match['away']}  must be a string")
    if type(match["away"]) != str:
        raise ParameterError(f"\"away\" for match  {match['home']} - {match['away']}  must be a string")
    if type(match["line_id"]) != int:
        raise ParameterError(f"\"line_id\" for match  {match['home']} - {match['away']}  must be an integer")
    if type(match["odds"]) != dict or (type(match["odds"]) == dict and not all(key in match["odds"] for key in ["home", "away", "draw"])):
        raise ParameterError(f"\"odds\" for match  {match['home']} - {match['away']}  must be a dictionary with keys \"home\", \"away\" and \"draw\"")
    if type(match["result"]) != int or (type(match["result"]) == int and match["result"] not in [0, 1, 2]):
        raise ParameterError(f"Result for match  {match['home']} - {match['away']}  must be an integer in [0, 1, 2]")
    if (type(match["amount"]) != float and type(match["amount"]) != int) or (((type(match["amount"]) == int) or (type(match["amount"]) == float)) and match["amount"] < 5):
        raise ParameterError(f"Amount for match  {match['home']} - {match['away']}  must be an integer or a float greater than 5")
        
