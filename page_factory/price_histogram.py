from plotly import express as px


class PriceHistogram:
    def __init__(self):
        pass

    def plot(self, data, col, title, nbins=50):
        fig = px.histogram(
            data,
            x=col,
            nbins=nbins,  # Increase bin count
            color_discrete_sequence=["#636EFA"],  # Use a stylish color
        )

        median_price = data[col].median()

        print("This are the columns: ", data.columns)

        # Add vertical line for the median
        fig.add_vline(
            x=median_price,
            line_dash="dash",  # Dashed line for better visibility
            line_color="green",  # Green color to make it stand out
            line_width=4,  # Increase line width
        )

        # Add annotation to label the median value
        fig.add_annotation(
            x=median_price,
            y=0.075,  # Place it at the bottom of the chart
            xref="x",
            yref="paper",
            text=f"Mediana: {int(median_price)}",  # Add descriptive text
            showarrow=False,  # Display an arrow pointing to the green line
            font=dict(color="white", size=12),  # Style of the text
            bgcolor="green",  # Background color for better readability
            borderpad=4,  # Padding between text and background
        )

        mean = data[col].mean()

        # Add vertical line for the average
        fig.add_vline(
            x=mean,
            line_dash="dash",  # Dashed line for better visibility
            line_color="red",  # Red color to make it stand out
            line_width=4,  # Increase line width
        )

        fig.add_annotation(
            x=mean,
            y=0.2,  # Place it at the bottom of the chart
            xref="x",
            yref="paper",
            text=f"Media: {int(mean)}",  # Add descriptive text
            showarrow=False,  # Display an arrow pointing to the red line
            font=dict(color="white", size=12),  # Style of the text
            bgcolor="red",  # Background color for better readability
            borderpad=4,  # Padding between text and background
        )

        # Update layout for better aesthetics
        fig.update_layout(
            title=title,
            xaxis_title=col.capitalize(),
            yaxis_title="Count",
            template="plotly_dark",  # Stylish dark mode
            bargap=0.03,  # Reduce gap between bars
            font=dict(size=14),  # Increase font size
            showlegend=False,  # Hide legend
        )

        return fig
