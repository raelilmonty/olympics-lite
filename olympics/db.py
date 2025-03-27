"""Database connection and ORM model management with SQLAlchemy."""

from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Connexion à la base de données
db_path = Path(__file__).parents[1] / 'database' / 'olympics.db'
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# =======================
# Définition des Modèles
# =======================

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Athlete(Base):
    __tablename__ = "athlete"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"))
    country = relationship("Country")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"))
    country = relationship("Country")


class Discipline(Base):
    __tablename__ = "discipline"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    discipline_id = Column(Integer, ForeignKey("discipline.id"))
    discipline = relationship("Discipline")


class Medal(Base):
    __tablename__ = "medal"

    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer, ForeignKey("athlete.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    type = Column(String, nullable=False)
    date = Column(Date)
    athlete = relationship("Athlete")
    team = relationship("Team")
    event = relationship("Event")


# =================================
# Fonctions Génériques et Requêtes
# =================================

def get_session():
    """Retourne une session SQLAlchemy."""
    return SessionLocal()


def get_all(model, id=None):
    """Récupère tous les éléments d'un modèle donné (Country, Athlete, etc.).

    Si `id` est spécifié, retourne uniquement l'objet correspondant.
    """
    session = get_session()
    try:
        if id:
            return session.query(model).filter_by(id=id).all()
        return session.query(model).all()
    finally:
        session.close()


def get_top_countries(top=10):
    """Retourne le classement des pays par nombre de médailles."""
    session = get_session()
    try:
        return (
            session.query(
                Country.name,
                func.sum(func.case((Medal.type == 'gold', 1), else_=0)).label("gold"),
                func.sum(func.case((Medal.type == 'silver', 1), else_=0)).label("silver"),
                func.sum(func.case((Medal.type == 'bronze', 1), else_=0)).label("bronze"),
            )
            .join(Athlete, Athlete.country_id == Country.id, isouter=True)
            .join(Team, Team.country_id == Country.id, isouter=True)
            .join(Medal, (Medal.athlete_id == Athlete.id) | (Medal.team_id == Team.id), isouter=True)
            .group_by(Country.id)
            .order_by(func.sum(func.case((Medal.type == 'gold', 1), else_=0)).desc(),
                      func.sum(func.case((Medal.type == 'silver', 1), else_=0)).desc(),
                      func.sum(func.case((Medal.type == 'bronze', 1), else_=0)).desc())
            .limit(top)
            .all()
        )
    finally:
        session.close()


def get_collective_medals(team_id=None):
    """Retourne les médailles remportées par des équipes."""
    session = get_session()
    try:
        query = (
            session.query(
                Country.name,
                Discipline.name.label("discipline"),
                Event.name.label("event"),
                Medal.type,
                Medal.date
            )
            .join(Team, Team.country_id == Country.id)
            .join(Medal, Medal.team_id == Team.id)
            .join(Event, Event.id == Medal.event_id)
            .join(Discipline, Discipline.id == Event.discipline_id)
        )

        if team_id:
            query = query.filter(Team.id == team_id)

        return query.all()
    finally:
        session.close()


def get_individual_medals(athlete_id=None):
    """Retourne les médailles remportées par des athlètes individuels."""
    session = get_session()
    try:
        query = (
            session.query(
                Athlete.name,
                Country.name.label("country"),
                Discipline.name.label("discipline"),
                Event.name.label("event"),
                Medal.type,
                Medal.date
            )
            .join(Country, Country.id == Athlete.country_id)
            .join(Medal, Medal.athlete_id == Athlete.id)
            .join(Event, Event.id == Medal.event_id)
            .join(Discipline, Discipline.id == Event.discipline_id)
        )

        if athlete_id:
            query = query.filter(Athlete.id == athlete_id)

        return query.all()
    finally:
        session.close()


def get_top_individual(top=10):
    """Retourne le classement des athlètes par nombre de médailles."""
    session = get_session()
    try:
        return (
            session.query(
                Athlete.name,
                Athlete.gender,
                Country.name.label("country"),
                func.count(Medal.id).label("medals")
            )
            .join(Country, Country.id == Athlete.country_id)
            .join(Medal, Medal.athlete_id == Athlete.id)
            .group_by(Athlete.name, Country.name)
            .order_by(func.count(Medal.id).desc())
            .limit(top)
            .all()
        )
    finally:
        session.close()
