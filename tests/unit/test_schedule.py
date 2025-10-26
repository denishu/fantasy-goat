"""Unit tests for Schedule and ScheduleManager."""

import pytest
from datetime import datetime, timedelta
from fantasy_goat.models.game import Game, Schedule
from fantasy_goat.core.schedule_manager import ScheduleManager


@pytest.fixture
def schedule_manager():
    """Create a ScheduleManager instance."""
    return ScheduleManager()


@pytest.fixture
def sample_games():
    """Create sample games."""
    base_date = datetime(2024, 10, 26, 19, 0)
    return [
        Game(
            game_id="game_001",
            game_date=base_date,
            home_team="LAL",
            away_team="GSW",
            status="scheduled"
        ),
        Game(
            game_id="game_002",
            game_date=base_date + timedelta(days=1),
            home_team="GSW",
            away_team="PHX",
            status="scheduled"
        ),
        Game(
            game_id="game_003",
            game_date=base_date + timedelta(days=2),
            home_team="LAL",
            away_team="PHX",
            status="scheduled"
        ),
    ]


def test_add_schedule(schedule_manager, sample_games):
    """Test adding a complete schedule."""
    schedule = Schedule(
        schedule_id="schedule_2024",
        season="2024-25",
        games=sample_games
    )
    
    schedule_manager.add_schedule(schedule)
    assert "2024-25" in schedule_manager.schedules
    assert len(schedule_manager.games_by_id) == 3


def test_add_single_game(schedule_manager):
    """Test adding a single game."""
    game = Game(
        game_id="game_001",
        game_date=datetime(2024, 10, 26, 19, 0),
        home_team="LAL",
        away_team="GSW"
    )
    
    schedule_manager.add_game("2024-25", game)
    assert "2024-25" in schedule_manager.schedules
    assert "game_001" in schedule_manager.games_by_id


def test_get_games_for_team(schedule_manager, sample_games):
    """Test retrieving games for a specific team."""
    schedule = Schedule(
        schedule_id="schedule_2024",
        season="2024-25",
        games=sample_games
    )
    schedule_manager.add_schedule(schedule)
    
    lal_games = schedule_manager.get_games_for_team("LAL")
    assert len(lal_games) == 2
    
    gsw_games = schedule_manager.get_games_for_team("GSW")
    assert len(gsw_games) == 2


def test_get_games_for_date(schedule_manager, sample_games):
    """Test retrieving games for a specific date."""
    schedule = Schedule(
        schedule_id="schedule_2024",
        season="2024-25",
        games=sample_games
    )
    schedule_manager.add_schedule(schedule)
    
    target_date = datetime(2024, 10, 26)
    games = schedule_manager.get_games_for_date(target_date)
    assert len(games) == 1
    assert games[0].game_id == "game_001"


def test_get_game_count_by_team(schedule_manager, sample_games):
    """Test getting game count by team."""
    schedule = Schedule(
        schedule_id="schedule_2024",
        season="2024-25",
        games=sample_games
    )
    schedule_manager.add_schedule(schedule)
    
    start = datetime(2024, 10, 26)
    end = datetime(2024, 10, 28, 23, 59, 59)  # Include all of Oct 28
    
    counts = schedule_manager.get_game_count_by_team(start, end)
    assert counts["LAL"] == 2
    assert counts["GSW"] == 2
    assert counts["PHX"] == 2


def test_schedule_get_games_by_date():
    """Test Schedule.get_games_by_date method."""
    base_date = datetime(2024, 10, 26, 19, 0)
    games = [
        Game(game_id="g1", game_date=base_date, home_team="A", away_team="B"),
        Game(game_id="g2", game_date=base_date + timedelta(days=1), home_team="C", away_team="D"),
    ]
    
    schedule = Schedule(
        schedule_id="test",
        season="2024-25",
        games=games
    )
    
    day1_games = schedule.get_games_by_date(base_date)
    assert len(day1_games) == 1
    assert day1_games[0].game_id == "g1"


def test_schedule_get_games_by_team():
    """Test Schedule.get_games_by_team method."""
    base_date = datetime(2024, 10, 26, 19, 0)
    games = [
        Game(game_id="g1", game_date=base_date, home_team="LAL", away_team="GSW"),
        Game(game_id="g2", game_date=base_date + timedelta(days=1), home_team="GSW", away_team="PHX"),
    ]
    
    schedule = Schedule(
        schedule_id="test",
        season="2024-25",
        games=games
    )
    
    gsw_games = schedule.get_games_by_team("GSW")
    assert len(gsw_games) == 2
