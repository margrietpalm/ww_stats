import streamlit as st
import pandas as pd
import altair as alt
from utils.chart_utils import create_timeline_chart

def render_role_timeline_tab(data):
    """Render the 'Tijdlijn per rol' tab."""
    role_names = sorted({role.name for game in data.game_map.values() for role in game.player_roles.values()})
    with st.popover("Selecteer rollen"):
        search_query = st.text_input("Zoek rollen", "")
        filtered_roles = [role for role in role_names if search_query.lower() in role.lower()]
        selected_roles = st.pills("Rollen", filtered_roles, selection_mode="multi")

    if selected_roles:
        # Prepare timeline data
        timeline_data = []
        for game_id, game in data.game_map.items():
            for role in selected_roles:
                if any(r.name == role for r in game.player_roles.values()):
                    timeline_data.append({"Game": game.number, "Role": role})

        # Convert to DataFrame
        timeline_df = pd.DataFrame(timeline_data)

        # Display the timeline chart
        if not timeline_df.empty:
            chart = create_timeline_chart(timeline_df)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No data available for the selected roles.")