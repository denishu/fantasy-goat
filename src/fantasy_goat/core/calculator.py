"""Fantasy points calculator for different formats."""

from typing import Dict, List
from fantasy_goat.models.stats import PlayerStats
from fantasy_goat.models.format import PointsScoringSettings, CategoryScoringSettings


class FantasyPointsCalculator:
    """Calculates fantasy points for different scoring systems."""
    
    def __init__(self, settings: PointsScoringSettings):
        """Initialize calculator with scoring settings."""
        self.settings = settings
    
    def calculate_fantasy_points(self, stats: PlayerStats) -> float:
        """
        Calculate fantasy points for a game based on scoring settings.
        
        Args:
            stats: PlayerStats object containing game statistics
            
        Returns:
            Total fantasy points earned
        """
        points = 0.0
        
        # Basic stats
        points += stats.points * self.settings.points_per_point
        points += stats.rebounds * self.settings.points_per_rebound
        points += stats.assists * self.settings.points_per_assist
        points += stats.steals * self.settings.points_per_steal
        points += stats.blocks * self.settings.points_per_block
        points += stats.turnovers * self.settings.points_per_turnover
        
        # Three-pointers bonus
        points += stats.three_pointers_made * self.settings.points_per_three
        
        # Shooting stats (if applicable)
        points += stats.field_goals_made * self.settings.points_per_fgm
        points += stats.field_goals_attempted * self.settings.points_per_fga
        points += stats.free_throws_made * self.settings.points_per_ftm
        points += stats.free_throws_attempted * self.settings.points_per_fta
        
        # Check for double-double
        if self.settings.points_per_double_double > 0:
            if self._is_double_double(stats):
                points += self.settings.points_per_double_double
        
        # Check for triple-double
        if self.settings.points_per_triple_double > 0:
            if self._is_triple_double(stats):
                points += self.settings.points_per_triple_double
        
        return points
    
    def _is_double_double(self, stats: PlayerStats) -> bool:
        """Check if stats represent a double-double."""
        stat_categories = [
            stats.points,
            stats.rebounds,
            stats.assists,
            stats.steals,
            stats.blocks
        ]
        return sum(1 for stat in stat_categories if stat >= 10) >= 2
    
    def _is_triple_double(self, stats: PlayerStats) -> bool:
        """Check if stats represent a triple-double."""
        stat_categories = [
            stats.points,
            stats.rebounds,
            stats.assists,
            stats.steals,
            stats.blocks
        ]
        return sum(1 for stat in stat_categories if stat >= 10) >= 3
    
    def calculate_total_points(self, games: List[PlayerStats]) -> float:
        """Calculate total fantasy points across multiple games."""
        return sum(self.calculate_fantasy_points(game) for game in games)
    
    def calculate_average_points(self, games: List[PlayerStats]) -> float:
        """Calculate average fantasy points per game."""
        if not games:
            return 0.0
        return self.calculate_total_points(games) / len(games)


class CategoryComparator:
    """Compares stats across multiple categories for category-based leagues."""
    
    def __init__(self, settings: CategoryScoringSettings):
        """Initialize with category settings."""
        self.settings = settings
    
    def get_category_value(self, stats: PlayerStats, category: str) -> float:
        """
        Get the value for a specific category from stats.
        
        Args:
            stats: PlayerStats object
            category: Category name (e.g., 'PTS', 'REB', 'AST')
            
        Returns:
            The value for that category
        """
        category_map = {
            'PTS': stats.points,
            'REB': stats.rebounds,
            'AST': stats.assists,
            'STL': stats.steals,
            'BLK': stats.blocks,
            'TO': stats.turnovers,
            '3PM': stats.three_pointers_made,
            'FGM': stats.field_goals_made,
            'FGA': stats.field_goals_attempted,
            'FTM': stats.free_throws_made,
            'FTA': stats.free_throws_attempted,
        }
        
        # Calculate percentages if requested
        if category == 'FG%':
            return stats.field_goals_made / stats.field_goals_attempted if stats.field_goals_attempted > 0 else 0.0
        elif category == '3P%':
            return stats.three_pointers_made / stats.three_pointers_attempted if stats.three_pointers_attempted > 0 else 0.0
        elif category == 'FT%':
            return stats.free_throws_made / stats.free_throws_attempted if stats.free_throws_attempted > 0 else 0.0
        
        return float(category_map.get(category, 0))
    
    def aggregate_categories(self, games: List[PlayerStats]) -> Dict[str, float]:
        """
        Aggregate statistics across multiple games for each category.
        
        Args:
            games: List of PlayerStats objects
            
        Returns:
            Dictionary mapping category names to aggregated values
        """
        if not games:
            return {cat: 0.0 for cat in self.settings.categories}
        
        result = {}
        for category in self.settings.categories:
            if category in ['FG%', '3P%', 'FT%']:
                # For percentages, calculate overall percentage
                if category == 'FG%':
                    total_made = sum(g.field_goals_made for g in games)
                    total_attempted = sum(g.field_goals_attempted for g in games)
                    result[category] = total_made / total_attempted if total_attempted > 0 else 0.0
                elif category == '3P%':
                    total_made = sum(g.three_pointers_made for g in games)
                    total_attempted = sum(g.three_pointers_attempted for g in games)
                    result[category] = total_made / total_attempted if total_attempted > 0 else 0.0
                elif category == 'FT%':
                    total_made = sum(g.free_throws_made for g in games)
                    total_attempted = sum(g.free_throws_attempted for g in games)
                    result[category] = total_made / total_attempted if total_attempted > 0 else 0.0
            else:
                # For counting stats, sum them up
                result[category] = sum(self.get_category_value(g, category) for g in games)
        
        return result
    
    def compare_categories(
        self, 
        team1_games: List[PlayerStats], 
        team2_games: List[PlayerStats]
    ) -> Dict[str, int]:
        """
        Compare two teams' performance across all categories.
        
        Args:
            team1_games: All games for team 1
            team2_games: All games for team 2
            
        Returns:
            Dict with 'team1_wins', 'team2_wins', 'ties' counts
        """
        team1_totals = self.aggregate_categories(team1_games)
        team2_totals = self.aggregate_categories(team2_games)
        
        wins = {'team1_wins': 0, 'team2_wins': 0, 'ties': 0}
        
        for category in self.settings.categories:
            val1 = team1_totals[category]
            val2 = team2_totals[category]
            
            # Handle negative categories (like turnovers)
            if category == 'TO' and self.settings.count_turnovers_negative:
                # Lower is better for turnovers
                if val1 < val2:
                    wins['team1_wins'] += 1
                elif val2 < val1:
                    wins['team2_wins'] += 1
                else:
                    wins['ties'] += 1
            else:
                # Higher is better for other categories
                if val1 > val2:
                    wins['team1_wins'] += 1
                elif val2 > val1:
                    wins['team2_wins'] += 1
                else:
                    wins['ties'] += 1
        
        return wins
