"""Stats model for fantasy basketball supporting multiple formats."""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PlayerStats(BaseModel):
    """Represents a player's statistics for a single game."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "player_id": "player_001",
                "game_date": "2025-10-26",
                "opponent": "GSW",
                "minutes_played": 35.5,
                "points": 28,
                "rebounds": 8,
                "assists": 7,
                "steals": 2,
                "blocks": 1,
                "turnovers": 3,
                "field_goals_made": 10,
                "field_goals_attempted": 20,
                "three_pointers_made": 3,
                "three_pointers_attempted": 8,
                "free_throws_made": 5,
                "free_throws_attempted": 6
            }
        }
    )
    
    player_id: str = Field(..., description="Player identifier")
    game_date: date = Field(..., description="Date of the game")
    opponent: str = Field(..., description="Opposing team abbreviation")
    
    # Basic stats
    minutes_played: float = Field(default=0.0, ge=0)
    points: int = Field(default=0, ge=0)
    rebounds: int = Field(default=0, ge=0)
    assists: int = Field(default=0, ge=0)
    steals: int = Field(default=0, ge=0)
    blocks: int = Field(default=0, ge=0)
    turnovers: int = Field(default=0, ge=0)
    
    # Shooting stats
    field_goals_made: int = Field(default=0, ge=0)
    field_goals_attempted: int = Field(default=0, ge=0)
    three_pointers_made: int = Field(default=0, ge=0)
    three_pointers_attempted: int = Field(default=0, ge=0)
    free_throws_made: int = Field(default=0, ge=0)
    free_throws_attempted: int = Field(default=0, ge=0)
    
    # Advanced stats
    offensive_rebounds: int = Field(default=0, ge=0)
    defensive_rebounds: int = Field(default=0, ge=0)
    personal_fouls: int = Field(default=0, ge=0)
    plus_minus: Optional[int] = None


class SeasonStats(BaseModel):
    """Represents aggregated season statistics for a player."""
    
    player_id: str
    season: str = Field(..., description="Season identifier (e.g., '2024-25')")
    games_played: int = Field(default=0, ge=0)
    
    # Averaged stats
    avg_points: float = Field(default=0.0, ge=0)
    avg_rebounds: float = Field(default=0.0, ge=0)
    avg_assists: float = Field(default=0.0, ge=0)
    avg_steals: float = Field(default=0.0, ge=0)
    avg_blocks: float = Field(default=0.0, ge=0)
    avg_turnovers: float = Field(default=0.0, ge=0)
    avg_minutes: float = Field(default=0.0, ge=0)
    
    # Shooting percentages
    field_goal_percentage: Optional[float] = Field(default=None, ge=0, le=1)
    three_point_percentage: Optional[float] = Field(default=None, ge=0, le=1)
    free_throw_percentage: Optional[float] = Field(default=None, ge=0, le=1)
    
    # Totals
    total_points: int = Field(default=0, ge=0)
    total_rebounds: int = Field(default=0, ge=0)
    total_assists: int = Field(default=0, ge=0)
    total_steals: int = Field(default=0, ge=0)
    total_blocks: int = Field(default=0, ge=0)
