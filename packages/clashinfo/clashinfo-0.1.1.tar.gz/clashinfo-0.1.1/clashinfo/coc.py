"""
Package for COC (Clash of Clans) API."""

import requests


class ClashOfClansAPI:
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.clashofclans.com/v1/"
        self.headers = {}

    def set_api_key(self, api_key: str):
        """Set the API key and update headers."""
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }

    def get_clan_info(self, clan_tag: str):
        """Get information about a specific clan."""
        if not self.api_key:
            raise ValueError("API key must be set before making requests.")
        url = f"{self.base_url}clans/%23{clan_tag[1:]}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_player_info(self, player_tag: str):
        """
        Get information about a specific player.

        Args:
            player_tag (str): The player's tag.
            
        Returns:
            Player: The player object.
        """
        if not self.api_key:
            raise ValueError("API key must be set before making requests.")
        url = f"{self.base_url}players/%23{player_tag[1:]}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        player_data = response.json()
        return Player(**player_data)
    

# Create an instance of ClashOfClansAPI that can be accessed globally
api = ClashOfClansAPI()


class Player:
    def __init__(self, **kwargs):
        """
        Initialize a Player object with the provided attributes.

        Args:
            **kwargs: Arbitrary keyword arguments representing player attributes.
                    tag (str): The player's tag.
                    name (str): The player's name.
                    townHallLevel (int): The player's town hall level.
                    townHallWeaponLevel (int): The player's town hall weapon level.
                    expLevel (int): The player's experience level.
                    trophies (int): The player's current trophies.
                    bestTrophies (int): The player's best trophies.
                    warStars (int): The player's war stars.
                    attackWins (int): The player's attack wins.
                    defenseWins (int): The player's defense wins.
                    builderHallLevel (int): The player's builder hall level.
                    builderBaseTrophies (int): The player's builder base trophies.
                    bestBuilderBaseTrophies (int): The player's best builder base trophies.
                    role (str): The player's role in the clan.
                    warPreference (str): The player's war preference.
                    donations (int): The player's donations.
                    donationsReceived (int): The player's donations received.
                    clanCapitalContributions (int): The player's clan capital contributions.
                    clan (dict): The player's clan information.
                    league (dict): The player's league information.
                    builderBaseLeague (dict): The player's builder base league information.
                    achievements (list): The player's achievements.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<Player {self.name} ({self.tag})>"

    def clan_info(self, fields: list = None):
        """
        Get the player's clan information.

        Args:
            fields (list, optional): A list of field names to return. If None, return all fields.

        Returns:
            dict: The filtered clan information.
        """
        if not hasattr(self, "clan"):
            return None

        clan_info = self.clan
        if fields:
            filtered_info = {
                field: clan_info.get(field) for field in fields if field in clan_info
            }
            return filtered_info

        return clan_info

    def league_info(self, fields: list = None):
        """
        Get the player's league information.

        Args:
            fields (list, optional): A list of field names to return. If None, return all fields.

        Returns:
            dict: The filtered league information.
        """
        if not hasattr(self, "league"):
            return None

        league_info = self.league
        if fields:
            filtered_info = {
                field: league_info.get(field)
                for field in fields
                if field in league_info
            }
            return filtered_info

        return league_info

    def bb_league_info(self, fields: list = None):
        """
        Get the player's builder base league information.

        Args:
            fields (list, optional): A list of field names to return. If None, return all fields.

        Returns:
            dict: The filtered builder base league information.
        """
        if not hasattr(self, "builderBaseLeague"):
            return None

        builder_base_league_info = self.builderBaseLeague
        if fields:
            filtered_info = {
                field: builder_base_league_info.get(field)
                for field in fields
                if field in builder_base_league_info
            }
            return filtered_info

        return builder_base_league_info

    def achievements_info(self, fields: list = None, completed: bool = None):
        """
        Get the player's achievements information.

        Args:
            fields (list, optional): A list of field names to return. If None, return all fields.
            completed (bool, optional): Filter achievements by completion status (True for completed, False for incomplete).

        Returns:
            list: The player's achievements information.
        """

        if not hasattr(self, "achievements"):
            return None

        achievements = self.achievements

        if completed is not None:
            achievements = [
                achievement
                for achievement in achievements
                if (
                    achievement.get("value", 0)
                    >= achievement.get("target", float("inf"))
                )
                == completed
            ]

        if fields:
            filtered_achievements = [
                {
                    field: achievement.get(field)
                    for field in fields
                    if field in achievement
                }
                for achievement in achievements
            ]
            return filtered_achievements

        return achievements

    def capital_house_info(self):
        """
        Get the info about player's capital house.

        Args:
            None

        Returns:
            list: The player's capital house information.
        """
        if not hasattr(self, "playerHouse"):
            return None

        playerhouse = self.playerHouse.get("elements")
        return playerhouse

    def home_troop_info(self):
        """
        Get the info about player's home village troops.

        Args:
            None

        Returns:
            list: The player's home village troops information.
        """
        if not hasattr(self, "troops"):
            return None

        home_troops = [
            {k: v for k, v in troop.items() if k != "village"}
            for troop in self.troops
            if troop.get("village") == "home"
        ]
        return home_troops

    def bb_troop_info(self):
        """
        Get the info about player's builder base troops.

        Args:
            None

        Returns:
            list: The player's builder base troops information.
        """
        if not hasattr(self, "troops"):
            return None

        bb_troops = [
            {k: v for k, v in troop.items() if k != "village"}
            for troop in self.troops
            if troop.get("village") == "builderBase"
        ]
        return bb_troops

    def hero_info(self, equipment=True, village=None):
        """
        Get the info about player's heroes.

        Args:
            equipment (bool): If True, return equipment information. Default is True.
            village (str): The village type ('home' or 'builderBase'). Default is None.

        Returns:
            list: The player's heroes information.
        """
        if not hasattr(self, "heroes"):
            return None

        if village:
            heroes = [
                {k: v for k, v in hero.items() if k != "village"}
                for hero in self.heroes
                if hero.get("village") == village
            ]
        else:
            heroes = [{k: v for k, v in hero.items()} for hero in self.heroes]

        if not equipment:
            heroes = [
                {k: v for k, v in hero.items() if k != "equipment"} for hero in heroes
            ]
        else:
            heroes = [{k: v for k, v in hero.items()} for hero in heroes]
        return heroes

    def hero_equipment_info(self):
        """
        Get the info about player's heroes equipment.

        Args:
            None

        Returns:
            list: The player's heroes equipment information.
        """
        if not hasattr(self, "heroEquipment"):
            return None

        hero_equipment = [
            {k: v for k, v in equipment.items()} for equipment in self.heroEquipment
        ]
        return hero_equipment

    def spell_info(self):
        """
        Get the info about player's spells.

        Args:
            None

        Returns:
            list: The player's spells information.
        """
        if not hasattr(self, "spells"):
            return None

        spells = [{k: v for k, v in spell.items()} for spell in self.spells]
        return spells

    def to_dict(self):
        """Convert the Player object to a dictionary.

        Returns:
            dict: The Player object as a dictionary.
        """
        return self.__dict__

    def to_json(self):
        """Convert the Player object to a JSON string.

        Returns:
            str: The Player object as a JSON string.
        """
        import json

        return json.dumps(self.__dict__)

    def export(self, filename: str):
        """Export the Player object to a JSON file.

        Args:
            filename (str): The name of the file to export to.
        """
        import json

        with open(filename, "w") as f:
            json.dump(self.__dict__, f)
