Vahan Investor Dashboard (Streamlit)

Vahan Investor Dashboard is a simple, investor-focused web app built with Streamlit that turns Vahan vehicle registration data into clear, actionable insights.
It shows monthly registration trends, Year-over-Year (YoY) growth, and Quarter-over-Quarter (QoQ) growth for different categories and manufacturers — all in an interactive format.

1> Features

Filter by date range, vehicle category, and manufacturer.

Visualize monthly trends with YoY% and QoQ% growth rates.

Get instant investor insights like top-growing manufacturers and category mix changes.

Modular design with separate data processing, metrics, and UI components.

Works with both real Vahan CSV exports and the included sample dataset.

2> How to Run

Set up a Python environment, install the required dependencies from requirements.txt, and start the Streamlit app.
The dashboard will open in your browser, ready to use.

3> Using Real Vahan Data

Go to the Vahan dashboard and open the view you need (e.g., Vehicle Class Wise, Manufacturer-wise).

Apply your preferred date range filters.

Export the table as a CSV/Excel file.

Ensure your file contains:

date in YYYY-MM-DD format (first day of the month for monthly data)

category (e.g., 2W, 3W, 4W)

manufacturer (OEM name)

registrations (integer)

Upload the file in the app sidebar to view and analyze your data.

4> How It Works

Aggregates data monthly.

Calculates YoY% by comparing each month to the same month last year.

Calculates QoQ% based on quarterly totals.

Generates quick insights by comparing the latest three months to the same period the previous year.

5> Project Structure

app.py – Main Streamlit app.

data/ – Contains the sample dataset.

src/data_utils.py – Data loading and cleaning functions.

src/metrics.py – Growth calculations and metrics logic.

src/ui_components.py – UI building blocks for the dashboard.

6> Future Plans

EV vs ICE vehicle split.

State/RTO-level breakdowns and heatmaps.

Exportable charts (PDF/PNG).

Basic forecasting for the next few quarters.

Automated data fetching from Vahan using Selenium/Playwright.

7> License

MIT
