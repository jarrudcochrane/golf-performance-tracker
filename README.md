# ⛳ Golf Performance Tracker

**Turn your scorecards into a story.**

This is a Python-powered analytics toolkit built around one thing: *my own golf rounds*. No public datasets, no scraped leaderboards — just `data/rounds.csv`, my personal round log, fed straight into charts, stats, and a live dashboard so I can watch my game evolve after every 18 holes. 🏌️‍♂️📈

Log a round → run a script → see exactly what's working (and what's wrecking your scorecard).

---

## 🎯 Two Ways to Play

| | **`golf_analysis.py`** | **`dashboard.py`** |
|---|---|---|
| **Vibe** | Fast, no-frills console report | Full interactive web app |
| **Best for** | A quick post-round gut check | Deep dives, filtering, logging new rounds |
| **Output** | Terminal summary + 5 PNG charts in `charts/` | Live Streamlit dashboard in your browser |
| **Powered by** | pandas, numpy, matplotlib, seaborn | + streamlit, plotly |

---

## 🧠 What It Actually Calculates

This isn't just "average score." It digs in:

- 📊 **Derived stats** — score-to-par, fairway %, GIR %, putts per hole
- 📉 **3-round rolling scoring average** — smooths out the one bad hole-in-the-water round
- 📈 **Linear trend line** — fits your scoring trajectory and *projects your next round*
- 🏅 **Simplified handicap index** — estimated from your best recent rounds
- 🎯 **Consistency score** — standard deviation, because everyone has an off day
- 🔍 **Correlation analysis** — which stats *actually* move your score, and by how much (spoiler: it's probably putts)

## 🖼️ Five Charts, Every Run

Dropped straight into `charts/`:

1. **Score over time** — with rolling average + trend line, plotted against par
2. **Fairways / GIR / Putts** — three key stats tracked round-by-round
3. **Score-vs-par by course** — ranked from your best track to your personal graveyard
4. **Correlation heatmap** — score vs. every underlying stat, at a glance
5. **Putts vs. score scatter** — with a regression line showing the damage bad putting does

## 💻 Dashboard Extras

Everything above, plus:

- 🗓️ Date & course filtering
- ⚡ Live KPI cards
- 🖱️ Interactive Plotly charts (hover, zoom, the works)
- 📋 Sortable, downloadable round table (CSV export)
- ✍️ **"Log a New Round" form** — appends straight to `data/rounds.csv`, no manual editing needed

18 rounds in, and the trend line doesn't lie: fairways and greens are the game, putting is the tax. 🏌️➡️⛳

## 📸 Dashboard Screenshots

<img width="1917" height="962" alt="dashboard_overview" src="https://github.com/user-attachments/assets/220c3415-d28d-46b6-b589-5ab5d914479c" />
<img width="1916" height="965" alt="dashboard_add_round" src="https://github.com/user-attachments/assets/fc3bb174-e1d4-46de-8363-99a2526bf2f9" />
<img width="1917" height="917" alt="dashboard_correlation" src="https://github.com/user-attachments/assets/9c62eda0-aad0-4986-9291-c3282848a68e" />
<img width="1917" height="957" alt="dashboard_round_log" src="https://github.com/user-attachments/assets/0a4eeeef-f86f-449a-b4b3-f4c8364a50c8" />
<img width="1912" height="971" alt="dashboard_stats_courses" src="https://github.com/user-attachments/assets/bedb2448-dff0-4f79-9aaa-eb6b541c83a3" />

---

## 🛠️ Tech Stack

| Tool | Job |
|---|---|
| 🐍 Python 3 | The engine |
| 🐼 pandas | Data loading & aggregation |
| 🔢 numpy | Linear trend regression |
| 📊 matplotlib / seaborn | Static charts + heatmap |
| 🌐 streamlit | Interactive dashboard |
| ✨ plotly | Interactive in-dashboard charts |

---

## 🚀 Running It

**Console script** (static charts + summary):

```bash
pip install -r requirements.txt
python golf_analysis.py
```

**Interactive dashboard:**

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

Opens a browser tab where you can filter by course/date, poke around interactive charts, browse the round log as a sortable table, download filtered data as CSV, and log new rounds through a form — zero manual CSV editing required.

---

## ✍️ Logging Your Own Rounds

Add a row to `data/rounds.csv` (or use the dashboard's **"Log a New Round"** form) in this format:

| Column | Description |
|---|---|
| `date` | Round date, `YYYY-MM-DD` |
| `course` | Course name |
| `par` | Course par (typically 71 or 72) |
| `score` | Total strokes for the round |
| `fairways_hit` | Number of fairways hit |
| `fairways_total` | Fairway opportunities (usually 14) |
| `greens_in_regulation` | Number of greens hit in regulation |
| `putts` | Total putts for the round |
| `penalties` | Penalty strokes taken |

Every new round automatically feeds the rolling average, the trend projection, and the correlation analysis — so the more you log, the smarter the picture gets. 🔁

---

## 🔭 Possible Next Steps

- 🏌️ Track performance club-by-club (driver accuracy, approach distances, etc.)
- ☁️ Correlate scores with weather conditions on the day
- 🧮 Swap the simplified handicap formula for the full USGA calculation
- ☁️ Deploy the dashboard (e.g. Streamlit Community Cloud) for access from any device

---

*Built to answer one question after every round: "Am I actually getting better, or does it just feel that way?"* 🏆

---

## 📋 Sample Output
