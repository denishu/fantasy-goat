"""Game and schedule models for fantasy basketball."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class Game(BaseModel):
    """Represents a basketball game."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "game_id": "game_20251026_LAL_GSW",
                "game_date": "2025-10-26T19:30:00",
                "home_team": "GSW",
                "away_team": "LAL",
                "home_score": 110,
                "away_score": 105,
                "status": "final"
            }
        }
    )
    
    game_id: str = Field(..., description="Unique game identifier")
    game_date: datetime = Field(..., description="Date and time of the game")
    home_team: str = Field(..., description="Home team abbreviation")
    away_team: str = Field(..., description="Away team abbreviation")
    
    # Optional game result fields
    home_score: Optional[int] = Field(default=None, ge=0)
    away_score: Optional[int] = Field(default=None, ge=0)
    status: str = Field(default="scheduled", description="Game status (scheduled, in_progress, final)")


class Schedule(BaseModel):
    """Represents a schedule of games."""
    
    schedule_id: str = Field(..., description="Unique schedule identifier")
    season: str = Field(..., description="Season identifier (e.g., '2024-25')")
    games: List[Game] = Field(default_factory=list, description="List of games in the schedule")
    
    def get_games_by_date(self, target_date: datetime) -> List[Game]:
        """Get all games on a specific date."""
        return [
            game for game in self.games 
            if game.game_date.date() == target_date.date()
        ]
    
    def get_games_by_team(self, team: str) -> List[Game]:
        """Get all games for a specific team."""
        return [
            game for game in self.games 
            if game.home_team == team or game.away_team == team
        ]
    
    def get_upcoming_games(self, from_date: Optional[datetime] = None) -> List[Game]:
        """Get upcoming games from a specific date (default: now)."""
        if from_date is None:
            from_date = datetime.now()
        return [
            game for game in self.games 
            if game.game_date >= from_date and game.status == "scheduled"
        ]
