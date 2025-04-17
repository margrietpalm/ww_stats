import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[2]  # Navigate two levels up to the project root
sys.path.insert(0, str(project_root))

from wiki_parser.parser import parse_spellenoverzicht, parse_spelersoverzicht, parse_rollen, WWData
from wiki_parser.models import Role, Team


def test_parse_spellenoverzicht():
    """Test the parse_spellenoverzicht function with the actual URL."""
    result = parse_spellenoverzicht()

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # Check that at least one game is parsed
    assert len(result) > 0

    # Check the structure of the parsed data
    for game, details in result.items():
        assert isinstance(game, str)  # Game key should be a string
        assert isinstance(details, list)  # Details should be a list
        assert len(details) >= 2  # At least theme and winning team


def test_parse_spelersoverzicht():
    """Test the parse_spelersoverzicht function with the actual URL."""
    result = parse_spelersoverzicht()

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # Check that at least one game is parsed
    assert len(result) > 0

    # Check the structure of the parsed data
    for game, players in result.items():
        assert isinstance(game, str)  # Game key should be a string
        assert isinstance(players, dict)  # Players should be a dictionary
        for player, role in players.items():
            assert isinstance(player, str)  # Player name should be a string
            assert isinstance(role, str)  # Role should be a string


def test_parse_rollen():
    """Test the parse_rollen function with the actual URL."""
    result = parse_rollen()

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # Check that at least one role is parsed
    assert len(result) > 0

    # Check the structure of the parsed data
    for role_name, role in result.items():
        assert isinstance(role_name, str)  # Role name should be a string
        assert isinstance(role, Role)  # Role should be an instance of Role
        assert role.team in [Team.WOLF, Team.CIV, Team.OTHER, Team.NAR]  # Valid team


def test_WWData():
    data = WWData()
    assert isinstance(data.role_map, dict)
    assert isinstance(data.games_overview, dict)
    assert isinstance(data.games_roles, dict)
    assert isinstance(data.game_map, dict)
    assert isinstance(data.player_map, dict)
    assert len(data.role_map) > 0
    assert len(data.games_overview) > 0
    assert len(data.games_roles) > 0
    assert len(data.game_map) > 0
    assert len(data.player_map) > 0
    