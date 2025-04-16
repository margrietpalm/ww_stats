from typing import Dict, List, Optional
from dataclasses import dataclass, field
from functools import cached_property, lru_cache
from enum import Enum


class Team(Enum):
    WOLF = "wolven"
    CIV = "burgers"
    OTHER = "alliantie onbekend"
    NAR = "verteller"

    def __str__(self):
        return self.value  # Return the custom name when converting to a string


@dataclass
class Role:
    name: str
    team: Team
    description: str


@dataclass
class PlayerRole:
    player: str
    role: Role


@dataclass
class Game:
    number: int
    theme: str
    player_roles: Dict[str, Role]
    winning_team: Team


@dataclass
class Player:
    name: str
    games: List[Game] = field(default_factory=list)

    @cached_property
    def nof_games(self) -> int:
        return len(self.games)

    @lru_cache(maxsize=None)
    def get_game(self, number: int) -> Optional[Game]:
        """Retrieve a specific game by number."""
        return next((game for game in self.games if game.number == number), None)

    def get_team(self, game_number: int) -> Optional[Role]:
        """Get the team for a specific game."""
        game = self.get_game(game_number)
        return game.player_roles.get(self.name) if game else None