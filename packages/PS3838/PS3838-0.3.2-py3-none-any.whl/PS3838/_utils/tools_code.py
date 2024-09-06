import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from PS3838._PS3838Bet import Bet
from PS3838._PS3838Retrieve import Retrieve
from PS3838._telegram.telegram_bot import CustomLogger
from PS3838._utils.constants import ID_SOCCER

######################################
#        Retrieving Functions        #
######################################

def get_all_matches(
        api_retrieve: Retrieve, 
        until_date: Optional[datetime] = None, 
        leagues_filter: Optional[List[int]] = None,
        logger: CustomLogger = None, 
    ) -> List[Dict[str, Any]]:
    """
    This function retrieves all the matches for the provided leagues and until the date specified. It also retrieves the odds for each match by parallelizing the process.

    Parameters:
        api_retrieve : Retrieve : API object to retrieve the odds
        until_date : Optional[datetime] : Date until which the matches are retrieved
        leagues_filter : Optional[List[int]] : Leagues to retrieve the matches from
        logger : CustomLogger : Logger to log the results

    Returns:
        match_odds : List[Dict[str, Any]] : List of matches with their corresponding odds
    """

    # Retrieve fixtures in the provided leagues or all of them if not provided
    all_fixtures = api_retrieve.get_fixtures_v3(sport_id=ID_SOCCER, league_ids=leagues_filter) if leagues_filter else api_retrieve.get_fixtures_v3(sport_id=ID_SOCCER)

    # Function to process each match (that we will parallelize)
    def process_match(league_id, match):
        try:
            # Check if match is open and (if specified) before the until_date
            if match["status"] == "O" and (not until_date or datetime.fromisoformat(match["starts"].replace('Z','')) <= until_date):
                match_info = {
                    "id": match["id"],
                    "starts": match["starts"],
                    "home": match["home"],
                    "away": match["away"],
                    "league": league_id,
                    "line_id": None
                }

                # Retrieve odds in the same step
                team1_odds, line_id = get_team_odds(api_retrieve, match_info, "Team1")
                team2_odds, _ = get_team_odds(api_retrieve, match_info, "Team2")
                draw_odds, _ = get_team_odds(api_retrieve, match_info, "Draw")

                return {**match_info, "line_id": line_id, "odds": {"home": team1_odds, "away": team2_odds, "draw": draw_odds}}
            
        except Exception as e:
            if logger:
                logger.error(f"Error processing match {match['id']}: {e}")

        return None

    # List to store the matches with odds
    match_odds = []  

    # Use a ThreadPoolExecutor to parallelize match processing
    with ThreadPoolExecutor(max_workers=10) as executor: 
        future_to_match = {
            executor.submit(process_match, league["id"], match): match
            for league in all_fixtures["league"]
            for match in league["events"]
        }

        # Collect results as they complete
        for future in as_completed(future_to_match):
            result = future.result()
            if result:
                match_odds.append(result)

    if logger:
        logger.info(f"Retrieved odds for {len(match_odds)} match(es)" if len(match_odds) > 0 else "No matches found")

    return match_odds
             

def get_team_odds(
    api_retrieve: Retrieve, 
    match: Dict[str, Any], 
    team: str
) -> Dict[str, Any]:
    """
    This function retrieves the odds for a specific team in a match.

    Parameters:
        api_retrieve : Retrieve : API object to retrieve the odds
        match : Dict[str, Any] : Match to retrieve the odds for
        team : str : Team to retrieve the odds for

    Returns:
        odds : Dict[str, Any] : Odds for the team
        line_id : int : Line ID of the bet
    """
    odds_response = api_retrieve.get_straight_line_v2(
        league_id=match["league"],
        handicap=0,
        odds_format="Decimal",
        sport_id=ID_SOCCER,
        event_id=match["id"],
        period_number=match.get("period_number", 0),
        bet_type="MONEYLINE",
        team=team
    )

    return odds_response.get("price", 0), odds_response.get("lineId", 0)



######################################
#          Betting Functions         #
######################################

def place_bets(
    list_matches : List[Tuple[Dict[str, Any], Dict[str, Any]]], 
    bet : Bet, 
    logger : CustomLogger = None,
) -> List[Dict[str, Any]]:
    """
    This function places the bets for the matches found with the odds provided. It verifies if the odds are not too low and if the bet is not already placed. Then in function of the parameter result, it places the bet on the home team, the away team or the draw.
    
    Parameters:
        list_matches : List[Tuple[Dict[str, Any], Dict[str, Any]]] : List of matches with their corresponding odds
            Example: [{'id': 1595460299, 'starts': '2024-08-23T18:45:00Z', 'home': 'Paris Saint-Germain', 'away': 'Montpellier HSC', 'league': 2036, 'line_id': 2650184231, 'odds': {'home': 1.309, 'draw': 6.14, 'away': 8.47}, 'result': 1, 'amount': 5}}, ...]
        bet : Bet : API object to place the bets
        logger : CustomLogger : Logger to log the results

    Returns:
        matches_successfull : List[Dict[str, Any]] : List of matches with their corresponding status
    """

    # List to store the matches with their status
    matches_successfull = []
    for match in list_matches:
        try : 
            # Check if the bet is already placed
            if is_already_bet(bet, match):
                if logger:
                    logger.warning(f"Bet already placed for match {match['id']} : {match['home']} - {match['away']}, skipping bet")
                matches_successfull.append({**match, "status": "ALREADY_BET"})
                continue
            # Place the bet depending on the "result" parameter
            if match["result"] == 1:
                bet.place_bet(stake=match["amount"], line_id=match["line_id"], sport_id=ID_SOCCER, event_id=match["id"], period_number=0, team="TEAM1")
            elif match["result"] == 2:
                bet.place_bet(stake=match["amount"], line_id=match["line_id"], sport_id=ID_SOCCER, event_id=match["id"], period_number=0, team="TEAM2")
            elif match["result"] == 0:
                bet.place_bet(stake=match["amount"], line_id=match["line_id"], sport_id=ID_SOCCER, event_id=match["id"], period_number=0, team="Draw")

            # Wait for 2 seconds to avoid rate limiting, and check if the bet is now well placed
            time.sleep(2)
            if is_already_bet(bet, match):
                if logger:
                    logger.info(f"Bet placed successfully for match : {match['home']} - {match['away']}")
                matches_successfull.append({**match, "status": "SUCCESS"})
                continue
            else:
                matches_successfull.append({**match, "status": "WTF"})

        except Exception as e:
            if logger:
                logger.error(f"Error placing bet for match {match['id']} : {match['home']} - {match['away']}: {e}")
            matches_successfull.append({**match, "status": "ERROR"})

    return matches_successfull

    
def change_date(date : str, days : int, hours : int) -> str:
    """
    This function changes the date by adding days and hours to it. It is useful to search for bets that were placed from 25 days in the past to 1 day in the future (as it is done in the function is_already_bet).
    """
    date = datetime.fromisoformat(date.replace('Z',''))
    date = date + timedelta(days=days, hours=hours)
    return date.isoformat() + 'Z'


def is_already_bet(api_bet : Bet, match : Dict[str, Any]) -> bool:
    """
    This function verifies if the bet is already placed for the match provided. It retrieves the bets placed in the past and checks if the bet is here. Also depending on the status of the bet, it returns True or False.
    """
    # Retrieve the bets placed in the past 25 days
    bets = api_bet.get_bets_v3(betlist='ALL', from_date=change_date(date=match["starts"], days=-25, hours=0), to_date=change_date(date=match["starts"], days=1, hours=0))

    # Check if the bet is already placed
    if "straightBets" in bets.keys():
        straights = bets["straightBets"]
        for bet in straights:
            if (bet["eventId"] == match["id"]) and (bet['betStatus'] == 'LOSE' or bet['betStatus'] == 'ACCEPTED' or bet['betStatus'] == 'CANCELLED' or bet['betStatus'] == 'WON' or bet['betStatus'] == 'REFUNDED' or bet['betStatus'] == 'PENDING_ACCEPTANCE'):
                return True
    
    return False

