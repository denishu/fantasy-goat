"""Unit tests for Player model."""

import pytest
from fantasy_goat.models.player import Player


def test_player_creation():
    """Test creating a player with required fields."""
    player = Player(
        player_id="test_001",
        name="Test Player",
        team="LAL",
        position="PG"
    )
    
    assert player.player_id == "test_001"
    assert player.name == "Test Player"
    assert player.team == "LAL"
    assert player.position == "PG"
    assert player.status == "active"


def test_player_with_jersey():
    """Test creating a player with jersey number."""
    player = Player(
        player_id="test_002",
        name="Another Player",
        team="GSW",
        position="SF",
        jersey_number=30
    )
    
    assert player.jersey_number == 30


def test_player_with_status():
    """Test creating a player with custom status."""
    player = Player(
        player_id="test_003",
        name="Injured Player",
        team="BKN",
        position="C",
        status="injured"
    )
    
    assert player.status == "injured"
