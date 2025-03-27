"""Web API."""

from fastapi import FastAPI
from . import db

app = FastAPI()


# ===================
# Simple API entries
# ===================

@app.get("/countries/")
def countries(id: int | None = None):
    """List of all countries."""
    return db.get_all(db.Country, id)


@app.get("/athletes/")
def athletes(id: int | None = None):
    """List of athletes."""
    return db.get_all(db.Athlete, id)


@app.get("/disciplines/")
def disciplines(id: int | None = None):
    """List of disciplines."""
    return db.get_all(db.Discipline, id)


@app.get("/teams/")
def teams(id: int | None = None):
    """List of teams."""
    return db.get_all(db.Team, id)


@app.get("/events/")
def events(id: int | None = None):
    """List of events."""
    return db.get_all(db.Event, id)


@app.get("/medals/")
def medals(id: int | None = None):
    """List of medals."""
    return db.get_all(db.Medal, id)


# ========================
# Complex API entry points
# ========================

@app.get("/top-countries/")
def top_countries(top: int = 10):
    """Medal count ranking of countries."""
    return db.get_top_countries(top)


@app.get("/collective-medals/")
def collective_medals(team_id: int | None = None):
    """List of medals for team events."""
    return db.get_collective_medals(team_id)


@app.get("/individual-medals/")
def individual_medals(athlete_id: int | None = None):
    """List of medals for individual events."""
    return db.get_individual_medals(athlete_id)


@app.get("/top-individual/")
def top_individual(top: int = 10):
    """Medal count ranking of athletes for individual events."""
    return db.get_top_individual(top)
