"""Unit tests for Stats models."""

import pytest
from datetime import date
from fantasy_goat.models.stats import PlayerStats, SeasonStats


def test_player_stats_creation():
    """Test creating basic player stats."""
    stats = PlayerStats(
        player_id="test_001",
        game_date=date(2024, 10, 26),
        opponent="GSW",
        points=25,
        rebounds=8,
        assists=6
    )
    
    assert stats.player_id == "test_001"
    assert stats.points == 25
    assert stats.rebounds == 8
    assert stats.assists == 6
    assert stats.steals == 0  # default value


def test_player_stats_full():
    """Test creating complete player stats."""
    stats = PlayerStats(
        player_id="test_002",
        game_date=date(2024, 10, 26),
        opponent="LAL",
        minutes_played=35.5,
        points=30,
        rebounds=10,
        assists=8,
        steals=2,
        blocks=1,
        turnovers=3,
        field_goals_made=11,
        field_goals_attempted=20,
        three_pointers_made=3,
        three_pointers_attempted=7
    )
    
    assert stats.minutes_played == 35.5
    assert stats.field_goals_made == 11
    assert stats.field_goals_attempted == 20


def test_season_stats_creation():
    """Test creating season stats."""
    season = SeasonStats(
        player_id="test_001",
        season="2024-25",
        games_played=20,
        avg_points=25.5,
        avg_rebounds=7.2,
        avg_assists=6.8
    )
    
    assert season.player_id == "test_001"
    assert season.season == "2024-25"
    assert season.games_played == 20
    assert season.avg_points == 25.5


def test_season_stats_with_percentages():
    """Test season stats with shooting percentages."""
    season = SeasonStats(
        player_id="test_002",
        season="2024-25",
        games_played=15,
        avg_points=20.0,
        field_goal_percentage=0.485,
        three_point_percentage=0.375,
        free_throw_percentage=0.850
    )
    
    assert season.field_goal_percentage == 0.485
    assert season.three_point_percentage == 0.375
    assert season.free_throw_percentage == 0.850
