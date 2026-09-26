# Habit Tracker

A full-stack web app for tracking daily habits, built with Flask.
Users can create habits, check them off day by day, see their current
streak, and view a 7-day analytics chart of overall activity.

## Stack

- **Flask** — web framework
- **Flask-SQLAlchemy** — ORM (object-relational mapping)
- **SQLite** — local database (created automatically on first run)
- **Tailwind CSS**, **Chart.js**, **Axios** — front end (loaded via CDN, no build step)

## Features

- Create and delete habits, each with a custom name and color
- Daily check-in toggle for the current day, plus a 7-day weekly grid per habit
- Automatic streak calculation (consecutive days checked in)
- `/analytics` page with a bar chart of total check-ins over the last 7 days

## Getting started

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install flask flask-sqlalchemy

# 3. Run the app
python app.py
```

The app runs at `http://127.0.0.1:5000`. The SQLite database
(`instance/habits.db`) is created automatically the first time you run it.

> This project doesn't have a `requirements.txt` yet — after installing
> the packages above, it's worth generating one with `pip freeze > requirements.txt`
> so anyone else (including future you, on another machine) can install
> the exact same dependencies.

## Routes

| Method | Route                    | Description                                  |
|--------|--------------------------|-----------------------------------------------|
| GET    | `/`                      | Dashboard — today's habits, weekly grid, chart |
| GET    | `/habits`                | List habits, with a form to add new ones      |
| POST   | `/habits/create`         | Create a new habit                            |
| POST   | `/habits/<id>/delete`    | Delete a habit                                |
| POST   | `/toggle`                | Toggle a check-in for a given habit and date  |
| GET    | `/analytics`             | Analytics page (chart + habit list)           |
| GET    | `/analytics.json`        | JSON data powering the analytics chart        |

## Project structure

```
app.py                    # routes, models (Habit, Checkin), and app logic
templates/
├── base.html               # shared layout, navigation, flash messages
├── index.html                # dashboard (today's view + weekly grid)
├── habits.html                # create/delete habits
└── analytics.html              # 7-day check-in chart
instance/
└── habits.db                    # SQLite database (auto-generated, not versioned)
```

## Ideas for future improvements

- [ ] Multi-user support with login (currently single-user)
- [ ] Edit an existing habit (name/color) instead of only create/delete
- [ ] Calendar heatmap view (GitHub-style) for longer-term history
- [ ] Deploy a live demo (e.g. Render or Fly.io)
