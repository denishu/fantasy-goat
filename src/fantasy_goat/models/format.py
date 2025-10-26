"""Fantasy format models for different scoring systems."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class FantasyFormat(str, Enum):
    """Supported fantasy basketball formats."""
    CATEGORY = "category"  # Head-to-head category
    POINTS = "points"      # Points-based scoring
    ROTO = "roto"          # Rotisserie (season-long rankings)


class PointsScoringSettings(BaseModel):
    """Scoring settings for points-based fantasy leagues."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "points_per_point": 1.0,
                "points_per_rebound": 1.2,
                "points_per_assist": 1.5,
                "points_per_steal": 3.0,
                "points_per_block": 3.0,
                "points_per_turnover": -1.0,
                "points_per_three": 0.5
            }
        }
    )
    
    points_per_point: float = Field(default=1.0, description="Points awarded per point scored")
    points_per_rebound: float = Field(default=1.2, description="Points awarded per rebound")
    points_per_assist: float = Field(default=1.5, description="Points awarded per assist")
    points_per_steal: float = Field(default=3.0, description="Points awarded per steal")
    points_per_block: float = Field(default=3.0, description="Points awarded per block")
    points_per_turnover: float = Field(default=-1.0, description="Points awarded (deducted) per turnover")
    points_per_three: float = Field(default=0.5, description="Bonus points for 3-pointers (in addition to point scored)")
    points_per_fgm: float = Field(default=0.0, description="Points awarded per field goal made")
    points_per_fga: float = Field(default=0.0, description="Points deducted per field goal attempted")
    points_per_ftm: float = Field(default=0.0, description="Points awarded per free throw made")
    points_per_fta: float = Field(default=0.0, description="Points deducted per free throw attempted")
    points_per_double_double: float = Field(default=0.0, description="Bonus points for double-double")
    points_per_triple_double: float = Field(default=0.0, description="Bonus points for triple-double")


class CategoryScoringSettings(BaseModel):
    """Settings for category-based fantasy leagues."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "categories": ["PTS", "REB", "AST", "STL", "BLK", "FG%", "FT%", "3PM"],
                "count_turnovers_negative": True
            }
        }
    )
    
    categories: List[str] = Field(
        default=["PTS", "REB", "AST", "STL", "BLK", "FG%", "FT%", "3PM", "TO"],
        description="List of statistical categories used for scoring"
    )
    
    # Some leagues count certain stats differently
    count_turnovers_negative: bool = Field(
        default=True,
        description="Whether fewer turnovers is better (True) or more is better (False)"
    )


class FantasyFormatSettings(BaseModel):
    """Complete settings for a fantasy league format."""
    
    format_type: FantasyFormat = Field(..., description="The fantasy format type")
    points_settings: Optional[PointsScoringSettings] = Field(
        default=None,
        description="Points scoring settings (required for points format)"
    )
    category_settings: Optional[CategoryScoringSettings] = Field(
        default=None,
        description="Category settings (required for category format)"
    )
    
    def validate_settings(self) -> bool:
        """Validate that appropriate settings exist for the format type."""
        if self.format_type == FantasyFormat.POINTS and not self.points_settings:
            return False
        if self.format_type in [FantasyFormat.CATEGORY, FantasyFormat.ROTO] and not self.category_settings:
            return False
        return True
