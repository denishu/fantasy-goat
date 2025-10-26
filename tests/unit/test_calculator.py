"""Unit tests for FantasyPointsCalculator."""

import pytest
from datetime import date
from fantasy_goat.models.stats import PlayerStats
from fantasy_goat.models.format import PointsScoringSettings
from fantasy_goat.core.calculator import FantasyPointsCalculator


@pytest.fixture
def default_settings():
    """Create default scoring settings."""
    return PointsScoringSettings()


@pytest.fixture
def calculator(default_settings):
    """Create a calculator with default settings."""
    return FantasyPointsCalculator(default_settings)


@pytest.fixture
def sample_stats():
    """Create sample player stats."""
    return PlayerStats(
        player_id="test_001",
        game_date=date(2024, 10, 26),
        opponent="GSW",
        points=25,
        rebounds=8,
        assists=6,
        steals=2,
        blocks=1,
        turnovers=3,
        three_pointers_made=3
    )


def test_calculate_fantasy_points(calculator, sample_stats):
    """Test basic fantasy points calculation."""
    points = calculator.calculate_fantasy_points(sample_stats)
    
    # Manual calculation:
    # Points: 25 * 1.0 = 25.0
    # Rebounds: 8 * 1.2 = 9.6
    # Assists: 6 * 1.5 = 9.0
    # Steals: 2 * 3.0 = 6.0
    # Blocks: 1 * 3.0 = 3.0
    # Turnovers: 3 * -1.0 = -3.0
    # Three-pointers: 3 * 0.5 = 1.5
    # Total: 51.1
    
    assert points == pytest.approx(51.1, rel=0.01)


def test_double_double_bonus():
    """Test double-double bonus calculation."""
    settings = PointsScoringSettings(points_per_double_double=2.0)
    calculator = FantasyPointsCalculator(settings)
    
    # Stats with double-double (points and rebounds)
    stats = PlayerStats(
        player_id="test_001",
        game_date=date(2024, 10, 26),
        opponent="GSW",
        points=20,
        rebounds=10,
        assists=5
    )
    
    points = calculator.calculate_fantasy_points(stats)
    # Should include the 2.0 bonus
    assert points > 20 + 12 + 7.5  # base points without bonus


def test_triple_double_bonus():
    """Test triple-double bonus calculation."""
    settings = PointsScoringSettings(points_per_triple_double=5.0)
    calculator = FantasyPointsCalculator(settings)
    
    # Stats with triple-double
    stats = PlayerStats(
        player_id="test_001",
        game_date=date(2024, 10, 26),
        opponent="GSW",
        points=20,
        rebounds=10,
        assists=10
    )
    
    points = calculator.calculate_fantasy_points(stats)
    # Should include the 5.0 bonus
    assert points > 20 + 12 + 15  # base points without bonus


def test_calculate_average_points(calculator):
    """Test calculating average fantasy points."""
    games = [
        PlayerStats(
            player_id="test_001",
            game_date=date(2024, 10, 20),
            opponent="GSW",
            points=25, rebounds=8, assists=6
        ),
        PlayerStats(
            player_id="test_001",
            game_date=date(2024, 10, 22),
            opponent="LAC",
            points=30, rebounds=10, assists=8
        ),
    ]
    
    avg = calculator.calculate_average_points(games)
    assert avg > 0
    
    # Empty list should return 0
    assert calculator.calculate_average_points([]) == 0.0


def test_custom_scoring():
    """Test calculator with custom scoring settings."""
    settings = PointsScoringSettings(
        points_per_point=0.5,
        points_per_rebound=1.0,
        points_per_assist=2.0
    )
    calculator = FantasyPointsCalculator(settings)
    
    stats = PlayerStats(
        player_id="test_001",
        game_date=date(2024, 10, 26),
        opponent="GSW",
        points=20,
        rebounds=10,
        assists=5
    )
    
    fp = calculator.calculate_fantasy_points(stats)
    # 20*0.5 + 10*1.0 + 5*2.0 = 10 + 10 + 10 = 30
    assert fp == pytest.approx(30.0, rel=0.01)
