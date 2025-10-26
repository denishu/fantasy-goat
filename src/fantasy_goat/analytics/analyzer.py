"""Analytics module for fantasy basketball insights."""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, date, timedelta
from statistics import mean, stdev

from fantasy_goat.models.stats import PlayerStats, SeasonStats
from fantasy_goat.models.player import Player
from fantasy_goat.core.stat_tracker import StatTracker
from fantasy_goat.core.calculator import FantasyPointsCalculator, CategoryComparator


class PlayerAnalyzer:
    """Provides analytical insights for player performance."""
    
    def __init__(self, stat_tracker: StatTracker):
        """Initialize with a stat tracker."""
        self.stat_tracker = stat_tracker
    
    def get_trending_stats(
        self, 
        player_id: str, 
        recent_games: int = 10,
        comparison_games: int = 20
    ) -> Dict[str, float]:
        """
        Analyze if a player's recent performance is trending up or down.
        
        Args:
            player_id: Player identifier
            recent_games: Number of recent games to analyze
            comparison_games: Number of games to compare against (should be > recent_games)
            
        Returns:
            Dictionary with percentage changes in key stats
        """
        all_games = self.stat_tracker.get_last_n_games(player_id, comparison_games)
        
        if len(all_games) < recent_games:
            return {}
        
        recent = all_games[:recent_games]
        older = all_games[recent_games:comparison_games]
        
        if not older:
            return {}
        
        # Calculate averages
        recent_avg_pts = mean(g.points for g in recent)
        older_avg_pts = mean(g.points for g in older)
        
        recent_avg_reb = mean(g.rebounds for g in recent)
        older_avg_reb = mean(g.rebounds for g in older)
        
        recent_avg_ast = mean(g.assists for g in recent)
        older_avg_ast = mean(g.assists for g in older)
        
        # Calculate percentage changes
        trends = {}
        if older_avg_pts > 0:
            trends['points_change'] = ((recent_avg_pts - older_avg_pts) / older_avg_pts) * 100
        if older_avg_reb > 0:
            trends['rebounds_change'] = ((recent_avg_reb - older_avg_reb) / older_avg_reb) * 100
        if older_avg_ast > 0:
            trends['assists_change'] = ((recent_avg_ast - older_avg_ast) / older_avg_ast) * 100
        
        return trends
    
    def get_consistency_score(self, player_id: str, num_games: int = 20) -> Dict[str, float]:
        """
        Calculate consistency scores for a player (lower standard deviation = more consistent).
        
        Args:
            player_id: Player identifier
            num_games: Number of recent games to analyze
            
        Returns:
            Dictionary with consistency metrics (coefficient of variation)
        """
        games = self.stat_tracker.get_last_n_games(player_id, num_games)
        
        if len(games) < 3:
            return {}
        
        points = [g.points for g in games]
        rebounds = [g.rebounds for g in games]
        assists = [g.assists for g in games]
        
        consistency = {}
        
        # Coefficient of variation (CV) = (std dev / mean) * 100
        # Lower CV means more consistent
        if mean(points) > 0:
            consistency['points_cv'] = (stdev(points) / mean(points)) * 100
        if mean(rebounds) > 0:
            consistency['rebounds_cv'] = (stdev(rebounds) / mean(rebounds)) * 100
        if mean(assists) > 0:
            consistency['assists_cv'] = (stdev(assists) / mean(assists)) * 100
        
        return consistency
    
    def project_next_game(
        self, 
        player_id: str, 
        opponent: str,
        num_games: int = 10
    ) -> Dict[str, float]:
        """
        Project stats for the next game based on recent performance.
        
        This is a simple projection based on recent averages.
        Future enhancements could include opponent adjustments and AI-based projections.
        
        Args:
            player_id: Player identifier
            opponent: Opposing team
            num_games: Number of recent games to base projection on
            
        Returns:
            Dictionary with projected stats
        """
        games = self.stat_tracker.get_last_n_games(player_id, num_games)
        
        if not games:
            return {}
        
        # Simple average-based projection
        projection = {
            'projected_points': mean(g.points for g in games),
            'projected_rebounds': mean(g.rebounds for g in games),
            'projected_assists': mean(g.assists for g in games),
            'projected_steals': mean(g.steals for g in games),
            'projected_blocks': mean(g.blocks for g in games),
        }
        
        # Add confidence interval (standard deviation)
        projection['points_std'] = stdev([g.points for g in games]) if len(games) > 1 else 0
        
        return projection
    
    def compare_players(
        self, 
        player1_id: str, 
        player2_id: str,
        num_games: int = 20
    ) -> Dict[str, any]:
        """
        Compare two players' recent performance.
        
        Args:
            player1_id: First player identifier
            player2_id: Second player identifier
            num_games: Number of recent games to compare
            
        Returns:
            Dictionary with comparison metrics
        """
        p1_games = self.stat_tracker.get_last_n_games(player1_id, num_games)
        p2_games = self.stat_tracker.get_last_n_games(player2_id, num_games)
        
        if not p1_games or not p2_games:
            return {}
        
        comparison = {
            'player1': {
                'avg_points': mean(g.points for g in p1_games),
                'avg_rebounds': mean(g.rebounds for g in p1_games),
                'avg_assists': mean(g.assists for g in p1_games),
            },
            'player2': {
                'avg_points': mean(g.points for g in p2_games),
                'avg_rebounds': mean(g.rebounds for g in p2_games),
                'avg_assists': mean(g.assists for g in p2_games),
            }
        }
        
        # Calculate differences
        comparison['difference'] = {
            'points': comparison['player1']['avg_points'] - comparison['player2']['avg_points'],
            'rebounds': comparison['player1']['avg_rebounds'] - comparison['player2']['avg_rebounds'],
            'assists': comparison['player1']['avg_assists'] - comparison['player2']['avg_assists'],
        }
        
        return comparison


class AIAnalyticsPreparation:
    """
    Placeholder for future AI analytics integration.
    
    This class prepares data structures and provides hooks for future
    AI-based analytics like machine learning projections, player
    clustering, and advanced pattern recognition.
    """
    
    def __init__(self, stat_tracker: StatTracker):
        """Initialize with stat tracker."""
        self.stat_tracker = stat_tracker
    
    def prepare_training_data(
        self, 
        player_ids: List[str],
        season: str
    ) -> Dict[str, List[PlayerStats]]:
        """
        Prepare historical data for AI model training.
        
        This method aggregates player statistics in a format suitable
        for machine learning models.
        
        Args:
            player_ids: List of player identifiers
            season: Season to prepare data for
            
        Returns:
            Dictionary mapping player IDs to their game statistics
        """
        training_data = {}
        
        for player_id in player_ids:
            games = self.stat_tracker.game_stats.get(player_id, [])
            training_data[player_id] = games
        
        return training_data
    
    def get_feature_vector(self, stats: PlayerStats) -> List[float]:
        """
        Convert PlayerStats to a feature vector for ML models.
        
        Args:
            stats: PlayerStats object
            
        Returns:
            List of numeric features
        """
        return [
            stats.minutes_played,
            float(stats.points),
            float(stats.rebounds),
            float(stats.assists),
            float(stats.steals),
            float(stats.blocks),
            float(stats.turnovers),
            float(stats.field_goals_made),
            float(stats.field_goals_attempted),
            float(stats.three_pointers_made),
            float(stats.three_pointers_attempted),
            float(stats.free_throws_made),
            float(stats.free_throws_attempted),
        ]
    
    def placeholder_ai_projection(self, player_id: str) -> Dict[str, str]:
        """
        Placeholder for future AI-based projections.
        
        Args:
            player_id: Player identifier
            
        Returns:
            Message indicating AI analytics coming soon
        """
        return {
            "status": "not_implemented",
            "message": "AI analytics coming soon! This feature will provide ML-based projections and insights."
        }
