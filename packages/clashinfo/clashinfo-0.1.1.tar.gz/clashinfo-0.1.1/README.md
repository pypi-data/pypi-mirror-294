# ClashInfo

ClashInfo is a Python wrapper for the Clash of Clans and Clash Royale APIs, allowing you to easily interact with the games' data.

## Installation

```bash
pip install clashinfo
```

## Modules

- **coc**: Contains the `ClashOfClansAPI` class and `Player` class to interact with the Clash of Clans API.
- **cr**: Placeholder for Clash Royale API interactions (not implemented yet).

## Usage for COC

### Setting Up

To use the Clash of Clans API, you need to set your API key:

```python
from clashinfo import coc

coc.set_api_key("your_api_key_here")
```

### Getting Player Information

You can retrieve information about a specific player using their player tag:

```python
player = coc.get_player_info("#player_tag_here")
print(player)
```

### Getting Clan Information

To get information about a specific clan, use the clan tag:

```python
clan = coc.get_clan_info("#clan_tag_here")
print(clan)
```

### Player Methods

The `Player` class provides several methods to get detailed information:

- `achievements_info(fields: list, completed: bool)`: Get player's achievements.
- `clan_info(fields: list)`: Get player's clan information.
- `league_info(fields: list)`: Get player's league information.
- `bb_league_info(fields: list)`: Get player's builder base league information.
- `capital_house_info()`: Get info about player's capital house.
- `home_troop_info()`: Get info about player's home village troops.
- `bb_troop_info()`: Get info about player's builder base troops.
- `hero_info(equipment: bool, village: String)`: Get info about player's heroes.
- `hero_equipment_info()`: Get info about player's heroes equipment.
- `spell_info()`: Get info about player's spells.
- `to_dict()`: Convert the Player object to a dictionary.
- `to_json()`: Convert the Player object to a JSON string.
- `export(filename)`: Export the Player object to a JSON file.

Example:

```python
player = coc.get_player_info("#player_tag")
print(player.achievements_info(completed=True))
```
