import logging
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import Dict, List
from .models import Role, Team, Game, Player


# Constants for URLs
BASE_URL = "https://metnerdsomtafel.nl/wiki/index.php"
SPELLENOVERZICHT_URL = f"{BASE_URL}/Spellenoverzicht"
SPELERSOVERZICHT_URL = f"{BASE_URL}/Spelersoverzicht_(Per_Spel)"
ROLLENOVERZICHT_URL = f"{BASE_URL}/Rollenoverzicht"


def parse_spellenoverzicht() -> Dict[str, List[str]]:
    logging.info("Fetching spellenoverzicht...")
    response = requests.get(SPELLENOVERZICHT_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")[1:]
    games = {}
    for row in rows:
        items = [td.text for td in row.find_all("td")]
        games[items[0]] = items[1:]
    return games


def parse_spelersoverzicht() -> Dict[str, Dict[str, str]]:
    logging.info("Fetching spelersoverzicht...")
    response = requests.get(SPELERSOVERZICHT_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    games = defaultdict(lambda: defaultdict(str))

    for table in soup.find_all("table"):
        headers = [th.text.strip() for th in table.find_all("th")[2:]]
        game_map = {i: header for i, header in enumerate(headers)}
        for row in table.find_all("tr")[1:]:
            cells = [td.text.strip() for td in row.find_all("td")]
            player_name = cells[1]
            for i, role in enumerate(cells[2:]):
                if role != "-":
                    games[game_map[i]][player_name] = role.lower()
    return games


def parse_rollen() -> Dict[str, Role]:
    logging.info("Fetching rollenoverzicht...")
    response = requests.get(ROLLENOVERZICHT_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    roles = {}
    current_team = None
    team_map = {
        "Wolvenrollen": Team.WOLF,
        "Burgerrollen": Team.CIV,
        "Alliantie onbekend bij start": Team.OTHER,
        "Overig": Team.NAR,
    }

    for element in soup.find_all(["h1", "dl"]):
        if element.name == "h1":
            headline = element.find("span", class_="mw-headline")
            if headline:
                current_team = team_map.get(headline.get_text().strip(), Team.OTHER)
        elif element.name == "dl" and current_team:
            titles = element.find_all("dt")
            descriptions = element.find_all("dd")
            for i in range(len(titles)):
                if i < len(descriptions):
                    role_name = titles[i].get_text().strip()
                    roles[role_name.lower()] = Role(
                        name=role_name,
                        team=current_team,
                        description=descriptions[i].get_text().strip(),
                    )
    return roles


class WWData:
    def __init__(self):
        logging.info("Initializing WWData...")
        self.role_map = parse_rollen()
        self.games_overview = parse_spellenoverzicht()
        self.games_roles = parse_spelersoverzicht()

        self.game_map = self._initialize_game_map()
        self.player_map = self._initialize_player_map()

    def _initialize_game_map(self) -> Dict[str, Game]:
        team_map = {"wolven": Team.WOLF, "burgers": Team.CIV}
        game_map = {}
        for key, game_info in self.games_overview.items():
            player_roles = {}
            for name, role in self.games_roles[key].items():
                # Normalize roles: Merge "ass. verteller" into "verteller"
                if role == "ass. verteller":
                    role = "verteller"

                if role not in self.role_map:
                    self.role_map[role] = Role(
                        name=role,
                        team=Team.OTHER,
                        description="Role not found in role_map.",
                    )
                player_roles[name] = self.role_map.get(role, None)

            game_map[key] = Game(
                number=int(key.strip("WW")),
                theme=game_info[0],
                winning_team=team_map.get(game_info[1], Team.OTHER),
                player_roles=player_roles,
            )
        return game_map

    def _initialize_player_map(self) -> Dict[str, Player]:
        player_map = {}
        for key, roles in self.games_roles.items():
            if key not in self.game_map:
                continue
            for name in roles:
                if name not in player_map:
                    player_map[name] = Player(name)
                player_map[name].games.append(self.game_map[key])
        return player_map