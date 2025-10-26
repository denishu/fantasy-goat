"""Stat tracker for managing and querying player statistics."""

from typing import List, Optional, Dict
from datetime import date, datetime
from collections import defaultdict

from fantasy_goat.models.stats import PlayerStats, SeasonStats
from fantasy_goat.models.player import Player


class StatTracker:
    """Tracks and manages player statistics."""
    
    def __init__(self):
        """Initialize the stat tracker."""
        self.game_stats: Dict[str, List[PlayerStats]] = defaultdict(list)  # player_id -> list of game stats
        self.players: Dict[str, Player] = {}  # player_id -> Player
    
    def add_player(self, player: Player) -> None:
        """Add a player to the tracker."""
        self.players[player.player_id] = player
    
    def add_game_stats(self, stats: PlayerStats) -> None:
        """Add game statistics for a player."""
        self.game_stats[stats.player_id].append(stats)
    
    def get_player_game_stats(
        self, 
        player_id: str, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[PlayerStats]:
        """
        Get game statistics for a player within a date range.
        
        Args:
            player_id: Player identifier
            start_date: Start date (inclusive), None for no lower bound
            end_date: End date (inclusive), None for no upper bound
            
        Returns:
            List of PlayerStats matching the criteria
        """
        stats = self.game_stats.get(player_id, [])
        
        if start_date is not None:
            stats = [s for s in stats if s.game_date >= start_date]
        if end_date is not None:
            stats = [s for s in stats if s.game_date <= end_date]
        
        return sorted(stats, key=lambda x: x.game_date)
    
    def calculate_season_stats(
        self, 
        player_id: str, 
        season: str,
        games: Optional[List[PlayerStats]] = None
    ) -> Optional[SeasonStats]:
        """
        Calculate aggregated season statistics for a player.
        
        Args:
            player_id: Player identifier
            season: Season identifier
            games: Optional list of games to use; if None, uses all games for the player
            
        Returns:
            SeasonStats object with aggregated statistics
        """
        if games is None:
            games = self.game_stats.get(player_id, [])
        
        if not games:
            return None
        
        games_played = len(games)
        
        # Calculate totals
        total_points = sum(g.points for g in games)
        total_rebounds = sum(g.rebounds for g in games)
        total_assists = sum(g.assists for g in games)
        total_steals = sum(g.steals for g in games)
        total_blocks = sum(g.blocks for g in games)
        total_turnovers = sum(g.turnovers for g in games)
        total_minutes = sum(g.minutes_played for g in games)
        
        # Calculate shooting stats
        total_fgm = sum(g.field_goals_made for g in games)
        total_fga = sum(g.field_goals_attempted for g in games)
        total_3pm = sum(g.three_pointers_made for g in games)
        total_3pa = sum(g.three_pointers_attempted for g in games)
        total_ftm = sum(g.free_throws_made for g in games)
        total_fta = sum(g.free_throws_attempted for g in games)
        
        # Calculate percentages
        fg_pct = total_fgm / total_fga if total_fga > 0 else None
        three_pct = total_3pm / total_3pa if total_3pa > 0 else None
        ft_pct = total_ftm / total_fta if total_fta > 0 else None
        
        return SeasonStats(
            player_id=player_id,
            season=season,
            games_played=games_played,
            avg_points=total_points / games_played,
            avg_rebounds=total_rebounds / games_played,
            avg_assists=total_assists / games_played,
            avg_steals=total_steals / games_played,
            avg_blocks=total_blocks / games_played,
            avg_turnovers=total_turnovers / games_played,
            avg_minutes=total_minutes / games_played,
            field_goal_percentage=fg_pct,
            three_point_percentage=three_pct,
            free_throw_percentage=ft_pct,
            total_points=total_points,
            total_rebounds=total_rebounds,
            total_assists=total_assists,
            total_steals=total_steals,
            total_blocks=total_blocks,
        )
    
    def get_last_n_games(self, player_id: str, n: int = 10) -> List[PlayerStats]:
        """Get the last N games for a player."""
        stats = self.game_stats.get(player_id, [])
        sorted_stats = sorted(stats, key=lambda x: x.game_date, reverse=True)
        return sorted_stats[:n]
