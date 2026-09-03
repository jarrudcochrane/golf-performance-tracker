# ⛳ Golf Performance Tracker

<div align="center">

### **Turn your scorecards into a story.**

A Python-powered golf analytics project that transforms personal round data into meaningful statistics, visualisations, trends, and an interactive dashboard.

🏌️‍♂️ 📊 📈

</div>


## 📌 Overview

Golf Performance Tracker is built around one thing: **tracking and understanding my own golf performance**.

Instead of relying on public datasets or scraped leaderboards, the project uses a personal round log stored in `data/rounds.csv`. Each recorded round feeds directly into statistical analysis, visualisations, trend tracking, and a live interactive dashboard.

The goal is simple:

> **Log a round → Analyse the data → Understand what's improving and what's hurting the scorecard.**

Whether it's a quick post-round analysis or a deeper dive into long-term performance, Golf Performance Tracker makes it easier to answer one important question:

> **"Am I actually getting better, or does it just feel that way?"**


# 🎯 Two Ways to Analyse Your Game

The project includes two different ways to explore the data.

| | 📊 `golf_analysis.py` | 🌐 `dashboard.py` |
|---|---|---|
| **Experience** | Fast, focused analysis | Full interactive dashboard |
| **Best for** | Quick post-round check | Deep dives and exploration |
| **Output** | Terminal summary + 5 charts | Interactive Streamlit web app |
| **Visualisation** | Matplotlib & Seaborn | Plotly |
| **Data Management** | Reads existing round data | Filter, explore and log new rounds |

### ⚡ Quick Analysis

Run the analytics script to generate a summary of your performance and automatically create visualisations.

### 🌐 Interactive Dashboard

Launch the Streamlit dashboard to explore performance trends, filter rounds, interact with charts, download data, and log new rounds without manually editing the CSV file.



# 🧠 What It Analyses

This project goes beyond simply calculating an average score.

It derives and analyses key golf performance metrics, including:

- 📊 **Score-to-par** - Understand how each round compares to the course par.
- 🎯 **Fairway percentage** - Track driving accuracy over time.
- 🟢 **Greens in Regulation (GIR)** - Measure approach consistency.
- ⛳ **Putts per hole** - Identify putting performance.
- 📉 **3-round rolling average** - Smooth out individual bad rounds and highlight longer-term performance.
- 📈 **Linear trend analysis** - Identify scoring direction and estimate future performance.
- 🏅 **Simplified handicap estimate** - Calculated using recent best rounds.
- 🎲 **Consistency analysis** - Uses standard deviation to measure how stable scoring performance is.
- 🔍 **Correlation analysis** - Identifies which performance metrics are most strongly associated with lower or higher scores.

The more rounds added to the dataset, the clearer the picture becomes.


# 📊 Visualisations

Running the analysis script automatically generates **five charts** inside the `charts/` directory.

### 1️⃣ Score Over Time

Tracks scores across all recorded rounds and compares them against:

- Course par
- 3-round rolling average
- Linear trend line

This makes it easier to see whether performance is genuinely improving over time.

### 2️⃣ Fairways, GIR & Putts

Tracks three of the most important performance indicators round-by-round:

- Fairway accuracy
- Greens in Regulation
- Total putts

### 3️⃣ Score vs Par by Course

Compares performance across different courses to identify:

🏆 Your strongest course  
😅 Your toughest course  
📈 Where your scoring is improving

### 4️⃣ Correlation Heatmap

Displays relationships between your score and underlying performance metrics.

This helps answer questions such as:

> **Does better putting actually lead to lower scores?**  
> **How strongly does GIR affect performance?**  
> **Are fairways or putting more important for your game?**

### 5️⃣ Putts vs Score

A scatter plot with a regression line showing the relationship between putting performance and total score.

Sometimes the numbers confirm what you already suspected:

> **Fairways and greens are the game. Putting is the tax.** 🏌️➡️⛳


# 🌐 Interactive Dashboard

The Streamlit dashboard provides everything from the analysis script, with additional interactive features.

### Dashboard Features

- 🗓️ **Filter rounds by date**
- ⛳ **Filter performance by course**
- ⚡ **Live KPI cards**
- 📊 **Interactive Plotly charts**
- 🔍 **Hover, zoom and explore data**
- 📋 **Sortable round history**
- 📥 **Download filtered data as CSV**
- ✍️ **Log a New Round directly from the dashboard**

No manual CSV editing is required when using the built-in round logging form.

Each newly logged round automatically becomes part of the dataset and feeds into future analysis.


# 📸 Dashboard Screenshots

### 🏌️ Dashboard Overview

<img width="1917" height="962" alt="Dashboard Overview" src="https://github.com/user-attachments/assets/220c3415-d28d-46b6-b589-5ab5d914479c" />


### ➕ Log a New Round

<img width="1916" height="965" alt="Add New Round" src="https://github.com/user-attachments/assets/fc3bb174-e1d4-46de-8363-99a2526bf2f9" />


### 🔍 Correlation Analysis

<img width="1917" height="917" alt="Correlation Analysis" src="https://github.com/user-attachments/assets/9c62eda0-aad0-4986-9291-c3282848a68e" />


### 📋 Round Log

<img width="1917" height="957" alt="Round Log" src="https://github.com/user-attachments/assets/0a4eeeef-f86f-449a-b4b3-f4c8364a50c8" />


### ⛳ Course Statistics

<img width="1912" height="971" alt="Course Statistics" src="https://github.com/user-attachments/assets/bedb2448-dff0-4f79-9aaa-eb6b541c83a3" />


# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 **Python 3** | Core programming language |
| 🐼 **pandas** | Data loading, cleaning and aggregation |
| 🔢 **NumPy** | Numerical calculations and trend regression |
| 📊 **Matplotlib** | Static data visualisation |
| 🎨 **Seaborn** | Statistical visualisation and correlation heatmaps |
| 🌐 **Streamlit** | Interactive web dashboard |
| ✨ **Plotly** | Interactive charts and visualisations |


# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```


# 📊 Run the Analysis Script

For a quick statistical summary and automatically generated charts:

```bash
python golf_analysis.py
```

This will:

- Load your round data
- Calculate derived statistics
- Display a performance summary in the terminal
- Generate five charts
- Save the charts inside the `charts/` directory


# 🌐 Run the Interactive Dashboard

Launch the Streamlit application with:

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser, where you can:

- Explore interactive charts
- Filter data by course or date
- View performance statistics
- Browse your round history
- Download filtered data
- Log new rounds


# ✍️ Logging Your Own Rounds

Round data is stored in:

```text
data/rounds.csv
```

You can either manually add a row to the CSV file or use the dashboard's **Log a New Round** form.

The dataset uses the following structure:

| Column | Description |
|---|---|
| `date` | Round date in `YYYY-MM-DD` format |
| `course` | Name of the golf course |
| `par` | Course par, typically 71 or 72 |
| `score` | Total strokes for the round |
| `fairways_hit` | Number of fairways successfully hit |
| `fairways_total` | Total fairway opportunities |
| `greens_in_regulation` | Number of greens reached in regulation |
| `putts` | Total putts for the round |
| `penalties` | Total penalty strokes |

### Example

```csv
date,course,par,score,fairways_hit,fairways_total,greens_in_regulation,putts,penalties
2026-08-30,Example Golf Club,72,89,9,14,7,34,2
```

Every new round automatically contributes to:

- 📉 Rolling scoring averages
- 📈 Performance trend analysis
- 🏅 Handicap estimation
- 🎯 Consistency tracking
- 🔍 Correlation analysis

**The more rounds you log, the more meaningful the analysis becomes.**


# 📂 Project Structure

```text
Golf-Performance-Tracker/
│
├── data/
│   └── rounds.csv
│
├── charts/
│   └── Generated visualisations
│
├── golf_analysis.py
├── dashboard.py
├── requirements.txt
└── README.md
```


# 🔭 Future Improvements

There are several opportunities to expand the project further:

- 🏌️ **Club-by-club performance tracking**
  - Driver accuracy
  - Approach distances
  - Club selection analysis

- ☁️ **Weather integration**
  - Temperature
  - Wind
  - Rain
  - Weather impact on scoring

- 🧮 **Advanced handicap calculation**
  - Replace the simplified formula with a more comprehensive handicap calculation.

- 🌍 **Cloud deployment**
  - Deploy the Streamlit dashboard for access from any device.

- 📱 **Mobile-friendly experience**
  - Optimise the dashboard for quick post-round logging.


# 🎯 The Goal

Golf Performance Tracker was built to turn personal golf data into something useful.

Not just:

> *"What did I score?"*

But:

> **Why did I score that way?**

> **What part of my game is improving?**

> **Where am I losing strokes?**

> **And most importantly... am I actually getting better?** 🏆


<div align="center">

## ⛳ **Log. Analyse. Improve. Repeat.**

*Because every round tells a story — the data just helps you read it.*

🏌️‍♂️ 📊 📈

<br>

### **Developed by Jarrud Cochrane**

</div>
