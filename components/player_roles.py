import streamlit as st
import pandas as pd
import altair as alt
from utils.chart_utils import create_bar_chart
from utils.data_processing import process_player_counts
from wiki_parser.models import Team  # Import the Team enum


def setup_ui(data):
    """Set up the UI elements and return user inputs."""
    with st.popover("Instellingen"):
        # Slider to select the starting game number
        min_game_number = min(game.number for game in data.game_map.values())
        max_game_number = max(game.number for game in data.game_map.values())
        start_game_number = st.slider(
            "Verberg spelers die niet meegedaan hebben na WW:",
            min_value=min_game_number,
            max_value=max_game_number,
            value=min_game_number,
        )

        # Filter players based on the selected game number
        player_names = sorted(
            [
                player.name
                for player in data.player_map.values()
                if any(game.number > start_game_number for game in player.games)
            ]
        )

        selected_player_name = st.multiselect("Speler", player_names, default=None)
        y_axis_type = st.segmented_control("y-as", ["aantal", "percentage"], default="aantal")
        teams = [team.name for team in Team]
        team_map = {Team.CIV: "burger", Team.WOLF: "wolf", Team.OTHER: "anders", Team.NAR: "verteller"}
        excluded_teams = st.pills(
            "Verberg rollen voor team",
            teams,
            selection_mode="multi",
            format_func=lambda team: team_map[Team[team]],
        )

    return selected_player_name, y_axis_type, excluded_teams


def render_player_roles_tab(data):
    with st.popover("Instellingen"):
        # Slider to select the starting game number
        min_game_number = min(game.number for game in data.game_map.values())
        max_game_number = max(game.number for game in data.game_map.values())
        start_game_number = st.slider(
            "Verberg spelers die niet meegedaan hebben na WW:",
            min_value=min_game_number,
            max_value=max_game_number,
            value=min_game_number,
        )

        # Filter players based on the selected game number
        player_names = sorted(
            [
                player.name
                for player in data.player_map.values()
                if any(game.number > start_game_number for game in player.games)
            ]
        )

        selected_player_name = st.multiselect("Speler", player_names, default=None)
        y_axis_type = st.segmented_control("y-as", ["aantal", "percentage"], default="aantal")
        teams = [team.name for team in Team]
        team_map = {Team.CIV: "burger", Team.WOLF: "wolf", Team.OTHER: "anders", Team.NAR: "verteller"}
        excluded_teams = st.pills(
            "Verberg rollen voor team",
            teams,
            selection_mode="multi",
            format_func=lambda team: team_map[Team[team]],
        )
        group_less_than = st.slider(
            "Combineer rollen die minder voorkomen dan:",
            min_value=1,
            max_value=10,
            value=1,
        )

    if selected_player_name:
        # Step 2: Process the data
        role_counts_df = pd.DataFrame()
        for player in selected_player_name:
            role_counts_player = process_player_counts(data, player, excluded_teams, group_less_than)
            role_counts_player['speler'] = player
            role_counts_df = pd.concat([role_counts_df, role_counts_player], ignore_index=True)


        # Step 3: Create and display the chart
        if not role_counts_df.empty:
            chart_title = f"Rolverdeling voor {', '.join(selected_player_name)}"
            chart = create_bar_chart(role_counts_df, chart_title, y_axis_type)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No role data available for this player.")