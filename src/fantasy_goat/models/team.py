"""Team model for fantasy basketball."""

from typing import List, Optional
from pydantic import BaseModel, Field


class Team(BaseModel):
    """Represents a fantasy basketball team."""
    
    team_id: str = Field(..., description="Unique team identifier")
    name: str = Field(..., description="Team name")
    owner: str = Field(..., description="Team owner's name")
    league_id: str = Field(..., description="League identifier this team belongs to")
    
    # Roster
    player_ids: List[str] = Field(default_factory=list, description="List of player IDs on the roster")
    
    # Optional team stats
    wins: int = Field(default=0, ge=0)
    losses: int = Field(default=0, ge=0)
    ties: int = Field(default=0, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "team_id": "team_001",
                "name": "The Dream Team",
                "owner": "John Doe",
                "league_id": "league_2024",
                "player_ids": ["player_001", "player_002", "player_003"],
                "wins": 5,
                "losses": 3,
                "ties": 0
            }
        }


class League(BaseModel):
    """Represents a fantasy basketball league."""
    
    league_id: str = Field(..., description="Unique league identifier")
    name: str = Field(..., description="League name")
    season: str = Field(..., description="Season identifier (e.g., '2024-25')")
    format: str = Field(..., description="League format (category, points, roto)")
    
    # League settings
    num_teams: int = Field(..., ge=2, description="Number of teams in the league")
    roster_size: int = Field(..., ge=1, description="Number of players per roster")
    
    # Scoring categories for category-based leagues
    scoring_categories: Optional[List[str]] = Field(
        default=None, 
        description="List of categories (e.g., ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG%', 'FT%', '3PM'])"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "league_id": "league_2024",
                "name": "Friends Basketball League",
                "season": "2024-25",
                "format": "category",
                "num_teams": 10,
                "roster_size": 13,
                "scoring_categories": ["PTS", "REB", "AST", "STL", "BLK", "FG%", "FT%", "3PM", "TO"]
            }
        }
