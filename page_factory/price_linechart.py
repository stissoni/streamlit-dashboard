import plotly.graph_objects as go
import pandas as pd


class PriceLineChart:
    def __init__(self):
        pass

    def plot(self, data, currency, title):
        # Prepare data for plotting

        data = data[(data["currency"] == currency) & (data["year"] < 2026)]

        avg_price = data["price"].mean()

        price_by_year = data.groupby("year")["price"].mean().reset_index()

        # Create figure
        fig = go.Figure()

        # Add line plot
        fig.add_trace(
            go.Line(
                x=price_by_year["year"],
                y=price_by_year["price"],
                mode="lines",
                line=dict(color="#636EFA", width=2),
                name="Price Trend",
            )
        )

        # Add scatter plot
        fig.add_trace(
            go.Scatter(
                x=data["year"],
                y=data["price"],
                mode="markers",
                marker=dict(color="#EF553B"),
                name="Price",
            )
        )

        # Add average line
        fig.add_trace(
            go.Scatter(
                x=[data["year"].min(), data["year"].max()],
                y=[avg_price, avg_price],
                mode="lines",
                line=dict(color="green", width=3, dash="dash"),
                name=f"Avg: {avg_price:.2f}",
            )
        )

        # Improve layout
        fig.update_layout(
            title=title,
            xaxis_title="Year",
            yaxis_title="Price",
            template="plotly_dark",
            font=dict(size=14),
            legend=dict(x=0.02, y=0.98, bgcolor="rgba(0,0,0,0.1)"),
        )

        return fig
