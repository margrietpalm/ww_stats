import pandas as pd

def process_player_counts(data, selected_player_name, excluded_teams, group_less_than=None):
    """Process the data based on user inputs and return a DataFrame."""
    selected_player = data.player_map[selected_player_name]

    # Count roles for the selected player
    role_counts = {}
    for game in selected_player.games:
        role = game.player_roles.get(selected_player_name)
        if role and role.team.name not in excluded_teams:
            role_counts[role.name] = role_counts.get(role.name, 0) + 1

    # Convert role counts to a DataFrame
    role_counts_df = pd.DataFrame(
        {"rol": list(role_counts.keys()), "aantal": list(role_counts.values())}
    )
    

    if group_less_than > 1:
        # Combine rows where 'aantal' is less than 'group_less_than'
        grouped_rows = role_counts_df[role_counts_df['aantal'] < group_less_than]
        if not grouped_rows.empty:
            overige_row = pd.DataFrame([{
            "rol": "overige",
            "aantal": grouped_rows["aantal"].sum()
            }])
            role_counts_df = pd.concat([role_counts_df[role_counts_df['aantal'] >= group_less_than], overige_row], ignore_index=True)

    # Add percentage column
    if not role_counts_df.empty:
        total_roles = role_counts_df["aantal"].sum()
        role_counts_df["percentage"] = (role_counts_df["aantal"] / total_roles) * 100

    return role_counts_df