import altair as alt

def create_bar_chart(data, title, y_axis_type):
    """Create a grouped bar chart for role counts with side-by-side bars."""
    y_axis = "aantal" if y_axis_type == "aantal" else "percentage"
    y_axis_title = "Aantal Spellen" if y_axis_type == "aantal" else "Percentage"

    # Get all unique values in the 'rol' column to ensure all are shown on the x-axis
    unique_roles = data["rol"].unique().tolist()

    return (
        alt.Chart(data, title=title)
        .mark_bar()
        .encode(
            x=alt.X(
                "rol:N",
                title="Rol",
                axis=alt.Axis(
                    labelAngle=-45,  # Rotate labels for better readability
                    labelOverlap=False,  # Ensure all labels are always visible
                ),
                scale=alt.Scale(domain=unique_roles),  # Ensure all roles are shown
            ),
            y=alt.Y(y_axis, title=y_axis_title),  # Counts or percentages on the y-axis
            color=alt.Color("speler:N", title="Speler"),  # Color by player
            xOffset=alt.XOffset("speler:N"),  # Offset bars by 'speler' for side-by-side grouping
            tooltip=["speler", "rol", "aantal", "percentage"],  # Add tooltips for more details
        )
        .configure_title(anchor="middle", fontSize=16)  # Center the title
        .configure_axis(labelFontSize=12, titleFontSize=14)  # Adjust axis font sizes
        .configure_legend(titleFontSize=14, labelFontSize=12)  # Adjust legend font sizes
    )


def create_timeline_chart(data):
    """Create a timeline chart for roles."""
    return (
        alt.Chart(data)
        .mark_point(size=100)
        .encode(
            x=alt.X("Game:O", title="Game Number"),
            y=alt.Y("Role:N", title="Role"),
            tooltip=["Game", "Role"],
        )
        .properties(title="Timeline of Selected Roles")
    )