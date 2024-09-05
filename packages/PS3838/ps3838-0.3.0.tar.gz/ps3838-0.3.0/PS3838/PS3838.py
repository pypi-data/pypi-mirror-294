from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from PS3838._PS3838Bet import Bet
from PS3838._PS3838Retrieve import Retrieve
from PS3838._telegram.telegram_bot import CustomLogger
from PS3838._utils.tools_check import check_config, check_list_matches
from PS3838._utils.tools_code import get_all_matches, place_bets

############################
#     Retrieving Class     #
############################

class PS3838RetrieveOdds():
    def __init__(
        self,
        config : Dict[str, str] = None,
        logger_active: Optional[bool] = True,
        logger_name: Optional[str] = "PS3838.log",
        *args,
        **kwargs
    ):
        self.config = config
        self.logger_active = logger_active
        self.logger_name = logger_name
        self.logger = None
        self.retrieve = None

        self._initiate()
        '''
        This class is used to retrieve the odds from the PS3838 API. It uses the Retrieve class to connect to the API and retrieve the odds for each match. It also uses a CustomLogger to log the information.
        
        Parameters:
            config (Dict[str, str]): The config to connect to the PS3838 API.
                Example: {"username": "my_username", "password": "my_password"}
            logger_active (bool): A boolean to activate the logger. Default is True.
            logger_name (str): The name of the log file. Default is "PS3838.log".
        '''

    def _initiate(self):
        # Create the logger. 
        if self.logger_active:
            custom_logger = CustomLogger(name="PS3838", log_file=self.logger_name, func="retrieving", config=self.config)
            self.logger = custom_logger.get_logger()

        # Check if the parameters are provided and valid (Raise a ConfigError if not)
        check_config(self.config)

        # Create the Retrieve object
        self.retrieve = Retrieve(config=self.config)

    ###############################
    #         Retrieving          #
    ###############################

    def retrieving(
        self,
        until_date : Optional[datetime] = None, 
        leagues : Optional[List[int]] = None
    ) -> List[List[Dict[str, Any]]]:
        """
        This function retrieves the odds for all the matches until a given date and for a given list of leagues. It uses the Retrieve class to connect to the PS3838 API and retrieve the odds for each match.

        Parameters:
            until_date (datetime): The date until which we want to retrieve the matches. Default is None, it retrieves everything in the specified leagues.
            leagues (List[int]): A list of leagues for which we want to retrieve the matches. Default is None, it retrieves every league until the date specified.

        Returns:
            List[List[Dict[str, Any]]]: A list of matches with their corresponding odds.
                Example: [{'id': 1595460299, 'starts': '2024-08-23T18:45:00Z', 'home': 'Paris Saint-Germain', 'away': 'Montpellier HSC', 'league': 2036, 'line_id': 2650184231, 'odds': {'home': 1.309, 'draw': 6.14, 'away': 8.47}}, ...]
        """

        try :
            matches = get_all_matches(self.retrieve, until_date, leagues, self.logger)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error while retrieving matches: {e}")

        return matches
    





############################
#      Betting Class       #
############################ 

class PS3838AutomatedBet():
    def __init__(
        self,
        config : Dict[str, str] = None,
        list_matches : List[Dict[str, Any]] = None,
        logger_active: Optional[bool] = True,
        to_bet: Optional[bool] = False,
        *args,
        **kwargs
    ):
        """
        This class is used to place bets on the PS3838 API. It uses the Bet classes to connect to the API and place the bets. It also uses a CustomLogger to log the information.
        
        Parameters:
            config (Dict[str, str]): The config to connect to the PS3838 API. 
                Example: {"username": "my_username", "password": "my_password"}
            list_matches (List[Dict[str, Any]]): A list of matches to bet on.
                Example: 
                    [{'id': 1596465583, 'starts': '2024-09-04T17:45:00Z', 'home': 'Resende FC', 'away': 'Artsul', 'league': 216059, 'line_id': 2673459336, 'odds': {'Team1': 2.05, 'Team2': 3.1, 'Draw': 3.25}, 'result': 1, 'amount': 5},
                    {'id': 1596465586, 'starts': '2024-09-04T17:45:00Z', 'home': 'Fluminense', 'away': 'AF Perolas Negras', 'league': 216059, 'line_id': 2673462355, 'odds': {'Team1': 1.159, 'Team2': 11.83, 'Draw': 5.83}, 'result': 0, 'amount': 5}, ...].
            logger_active (bool): A boolean to activate the logger. Default is True.
            to_bet (bool): A boolean to know if we really want to bets. Default is False, useful for testing the code.
        """

        self.config = config
        self.list_matches = list_matches
        self.logger_active = logger_active
        self.to_bet = to_bet
        self.bet = None
        self.logger = None

        self._initiate()

    def _initiate(self):
        # Create the logger. 
        if self.logger_active:
            custom_logger = CustomLogger(name="PS3838", log_file="PS3838.log", func="betting", config=self.config)
            self.logger = custom_logger.get_logger()

        # Check if the parameters are provided and valid (Raise a ConfigError if not), and check if the list of matches is valid (Raise a ParameterError if not)
        check_config(self.config)
        check_list_matches(self.list_matches)

        # Create the Bet and Retrieve objects
        self.bet = Bet(config=self.config)


    #############################
    #         Betting           #
    #############################

    def betting(self) -> List[Dict[str, Any]] :
        """
        This function places bets on the PS3838 API for a given list of matches, if the bets are not already placed and if the maintenance is not in progress.
 
        Returns:
            List[List[Dict[str, Any]]] | None: A list of matches with their corresponding odds if the bets were placed, None otherwise.
                Example: [{'id': 1595460299, 'starts': '2024-08-23T18:45:00Z', 'home': 'Paris Saint-Germain', 'away': 'Montpellier HSC', 'league': 2036, 'line_id': 2650184231, 'odds': {'home': 1.309, 'draw': 6.14, 'away': 8.47}}, ...]
        """
        matches_successful = None
        
        # Check if there is maintenance
        maintenance = self.bet.check_maintenance()

        if maintenance["status"] == 'ALL_BETTING_ENABLED':
            try:

                if self.to_bet:
                    # Place the bets
                    matches_successful = place_bets(self.list_matches, self.bet, logger=self.logger)
                else:
                    if self.logger:
                        self.logger.info("Bets not placed, to_bet is set to False")

            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error placing bets: {e}")
        else:
            if self.logger:
                self.logger.info("Maintenance in progress, no bets placed. Try another time")

        return matches_successful 