"""Unit tests for StatTracker."""

import pytest
from datetime import date
from fantasy_goat.models.player import Player
from fantasy_goat.models.stats import PlayerStats
from fantasy_goat.core.stat_tracker import StatTracker


@pytest.fixture
def stat_tracker():
    """Create a StatTracker instance."""
    return StatTracker()


@pytest.fixture
def sample_player():
    """Create a sample player."""
    return Player(
        player_id="test_001",
        name="Test Player",
        team="LAL",
        position="PG"
    )


@pytest.fixture
def sample_stats():
    """Create sample player stats."""
    return [
        PlayerStats(
            player_id="test_001",
            game_date=date(2024, 10, 20),
            opponent="GSW",
            points=25, rebounds=8, assists=7
        ),
        PlayerStats(
            player_id="test_001",
            game_date=date(2024, 10, 22),
            opponent="LAC",
            points=30, rebounds=6, assists=9
        ),
        PlayerStats(
            player_id="test_001",
            game_date=date(2024, 10, 24),
            opponent="PHX",
            points=28, rebounds=7, assists=8
        ),
    ]


def test_add_player(stat_tracker, sample_player):
    """Test adding a player to the tracker."""
    stat_tracker.add_player(sample_player)
    assert "test_001" in stat_tracker.players
    assert stat_tracker.players["test_001"].name == "Test Player"


def test_add_game_stats(stat_tracker, sample_stats):
    """Test adding game stats."""
    for stats in sample_stats:
        stat_tracker.add_game_stats(stats)
    
    assert len(stat_tracker.game_stats["test_001"]) == 3


def test_get_player_game_stats(stat_tracker, sample_stats):
    """Test retrieving player game stats."""
    for stats in sample_stats:
        stat_tracker.add_game_stats(stats)
    
    all_stats = stat_tracker.get_player_game_stats("test_001")
    assert len(all_stats) == 3
    
    # Test date filtering
    filtered = stat_tracker.get_player_game_stats(
        "test_001",
        start_date=date(2024, 10, 22)
    )
    assert len(filtered) == 2


def test_calculate_season_stats(stat_tracker, sample_stats):
    """Test calculating season statistics."""
    for stats in sample_stats:
        stat_tracker.add_game_stats(stats)
    
    season = stat_tracker.calculate_season_stats("test_001", "2024-25")
    
    assert season is not None
    assert season.games_played == 3
    assert season.avg_points == pytest.approx(27.67, rel=0.01)
    assert season.avg_rebounds == pytest.approx(7.0, rel=0.01)
    assert season.avg_assists == 8.0


def test_get_last_n_games(stat_tracker, sample_stats):
    """Test getting last N games."""
    for stats in sample_stats:
        stat_tracker.add_game_stats(stats)
    
    last_two = stat_tracker.get_last_n_games("test_001", 2)
    assert len(last_two) == 2
    # Should be sorted by date descending
    assert last_two[0].game_date > last_two[1].game_date


def test_empty_stats(stat_tracker):
    """Test behavior with no stats."""
    result = stat_tracker.calculate_season_stats("nonexistent", "2024-25")
    assert result is None
    
    games = stat_tracker.get_last_n_games("nonexistent", 10)
    assert len(games) == 0
