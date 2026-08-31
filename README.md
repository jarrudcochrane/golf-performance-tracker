# Golf Performance Tracker

A Python project that analyses my own golf rounds and turns them into
performance charts, deeper statistical breakdowns, and an interactive
dashboard. This isn't built on a public or scraped dataset — it's my
personal round log (`data/rounds.csv`), and the project is designed so I
can keep appending new rounds after every game and immediately see how I'm
trending over a season.

It ships two ways to explore the data:

1. **`golf_analysis.py`** — a console script that prints a detailed stat
   summary and saves five charts as PNGs (great for a quick check or for
   embedding static images, like below).
2. **`dashboard.py`** — a Streamlit web app with filters, interactive
   charts, and a form to log new rounds without touching the CSV directly.

## What it does

- Loads round-by-round data (score, fairways, greens in regulation, putts, penalties)
- Calculates derived stats: score-to-par, fairway %, GIR %, and putts per hole
- Computes a **3-round rolling scoring average** to smooth out noise
- Fits a **linear trend line** to scoring average and projects the next round
- Estimates a **simplified handicap index** from the best recent rounds
- Reports **score consistency** (standard deviation)
- Runs a **correlation analysis** to show which stats (fairways, GIR, putts,
  penalties) actually move the scoreboard, and by how much
- Generates five charts to `charts/`:
  - Score over time, with rolling average and linear trend overlaid on a par line
  - Fairway %, GIR %, and putts per round over time
  - Average score-vs-par by course, ranked best to worst
  - A correlation heatmap of score vs. underlying stats
  - A putts-vs-score scatter plot with a regression line
- The dashboard adds: date/course filtering, live KPI cards, interactive
  Plotly versions of the charts above, a sortable/downloadable round table,
  and a form to log new rounds that appends straight to `data/rounds.csv`

## Sample output (`golf_analysis.py`)

```
==================================================
GOLF PERFORMANCE SUMMARY
==================================================
Rounds logged:              18
Average score:               83.8  (std dev 4.2)
Average vs. par:             +12.1
Best round:                  77 (Pinehurst Meadows, 2025-08-31)
Worst round:                 91 (Riverside Golf Club, 2025-01-05)
Average fairways hit:        59.5%
Average greens in reg.:      38.3%
Average putts per round:     32.0
Average penalties per round: 1.6
Trend (1st half vs 2nd):     improving by 7.0 strokes on average (87.3 -> 80.3)
Linear trend slope:          -0.76 strokes/round (projected next round: 76.2)
Estimated handicap index:    +7.9 (simplified estimate)

What's correlated with a lower score (most to least helpful):
  fairway_pct  r = -0.99  (more fairway_pct -> lower score)
  gir_pct      r = -0.98  (more gir_pct -> lower score)
  penalties    r = +0.95  (more penalties -> higher score)
  putts        r = +0.98  (more putts -> higher score)
==================================================

Charts saved to charts/
```

## Screenshots

<img width="1917" height="962" alt="dashboard_overview png" src="https://github.com/user-attachments/assets/220c3415-d28d-46b6-b589-5ab5d914479c" />

<img width="1916" height="965" alt="dashboard_add_round png" src="https://github.com/user-attachments/assets/fc3bb174-e1d4-46de-8363-99a2526bf2f9" />

<img width="1917" height="917" alt="dashboard_correlation png" src="https://github.com/user-attachments/assets/9c62eda0-aad0-4986-9291-c3282848a68e" />

<img width="1917" height="957" alt="dashboard_round_log png" src="https://github.com/user-attachments/assets/0a4eeeef-f86f-449a-b4b3-f4c8364a50c8" />

<img width="1912" height="971" alt="dashboard_stats_courses png" src="https://github.com/user-attachments/assets/bedb2448-dff0-4f79-9aaa-eb6b541c83a3" />




## Tech stack

- Python 3
- pandas — data loading and aggregation
- numpy — linear trend regression
- matplotlib / seaborn — static charts and heatmap
- streamlit — interactive dashboard
- plotly — interactive charts inside the dashboard

## Running it

**Console script (static charts + summary):**

```bash
pip install -r requirements.txt
python golf_analysis.py
```

**Interactive dashboard:**

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

This opens a browser tab where you can filter by course/date, explore
interactive charts, view the round log as a sortable table, download the
filtered data as CSV, and log new rounds through a form — no need to edit
the CSV by hand.

## Logging your own rounds

Add rows to `data/rounds.csv` (or use the dashboard's "Log a New Round"
form) using this format:

| Column                 | Description                                      |
|-------------------------|--------------------------------------------------|
| `date`                  | Round date, `YYYY-MM-DD`                          |
| `course`                | Course name                                       |
| `par`                   | Course par (typically 71 or 72)                   |
| `score`                 | Total strokes for the round                       |
| `fairways_hit`          | Number of fairways hit                            |
| `fairways_total`        | Fairway opportunities (usually 14)                |
| `greens_in_regulation`  | Number of greens hit in regulation                |
| `putts`                 | Total putts for the round                         |
| `penalties`             | Penalty strokes taken                             |

## Possible next steps

- Track performance club-by-club (driver accuracy, approach distances, etc.)
- Correlate scores with weather conditions on the day
- Swap the simplified handicap formula for the full USGA calculation
- Deploy the dashboard (e.g. Streamlit Community Cloud) for access from any device
