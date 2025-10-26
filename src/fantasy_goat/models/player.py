"""Player model for fantasy basketball."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Player(BaseModel):
    """Represents a basketball player."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "player_id": "player_001",
                "name": "LeBron James",
                "team": "LAL",
                "position": "SF",
                "jersey_number": 23,
                "status": "active"
            }
        }
    )
    
    player_id: str = Field(..., description="Unique player identifier")
    name: str = Field(..., description="Player's full name")
    team: str = Field(..., description="NBA team abbreviation")
    position: str = Field(..., description="Player position (PG, SG, SF, PF, C)")
    
    # Optional fields
    jersey_number: Optional[int] = None
    status: str = Field(default="active", description="Player status (active, injured, out)")
