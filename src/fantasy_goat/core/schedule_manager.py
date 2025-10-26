"""Schedule manager for tracking games and matchups."""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from fantasy_goat.models.game import Game, Schedule


class ScheduleManager:
    """Manages game schedules and provides schedule queries."""
    
    def __init__(self):
        """Initialize the schedule manager."""
        self.schedules: Dict[str, Schedule] = {}  # season -> Schedule
        self.games_by_id: Dict[str, Game] = {}  # game_id -> Game
    
    def add_schedule(self, schedule: Schedule) -> None:
        """Add a schedule to the manager."""
        self.schedules[schedule.season] = schedule
        for game in schedule.games:
            self.games_by_id[game.game_id] = game
    
    def add_game(self, season: str, game: Game) -> None:
        """Add a single game to a schedule."""
        if season not in self.schedules:
            self.schedules[season] = Schedule(
                schedule_id=f"schedule_{season}",
                season=season,
                games=[]
            )
        self.schedules[season].games.append(game)
        self.games_by_id[game.game_id] = game
    
    def get_games_for_date(self, target_date: datetime, season: Optional[str] = None) -> List[Game]:
        """
        Get all games on a specific date.
        
        Args:
            target_date: Date to query
            season: Optional season filter
            
        Returns:
            List of games on that date
        """
        games = []
        schedules = [self.schedules[season]] if season and season in self.schedules else self.schedules.values()
        
        for schedule in schedules:
            games.extend(schedule.get_games_by_date(target_date))
        
        return sorted(games, key=lambda x: x.game_date)
    
    def get_games_for_team(self, team: str, season: Optional[str] = None) -> List[Game]:
        """
        Get all games for a specific team.
        
        Args:
            team: Team abbreviation
            season: Optional season filter
            
        Returns:
            List of games for that team
        """
        games = []
        schedules = [self.schedules[season]] if season and season in self.schedules else self.schedules.values()
        
        for schedule in schedules:
            games.extend(schedule.get_games_by_team(team))
        
        return sorted(games, key=lambda x: x.game_date)
    
    def get_upcoming_games(
        self, 
        days_ahead: int = 7, 
        team: Optional[str] = None,
        season: Optional[str] = None
    ) -> List[Game]:
        """
        Get upcoming games within a specified number of days.
        
        Args:
            days_ahead: Number of days to look ahead
            team: Optional team filter
            season: Optional season filter
            
        Returns:
            List of upcoming games
        """
        now = datetime.now()
        end_date = now + timedelta(days=days_ahead)
        
        games = []
        schedules = [self.schedules[season]] if season and season in self.schedules else self.schedules.values()
        
        for schedule in schedules:
            for game in schedule.get_upcoming_games(now):
                if game.game_date <= end_date:
                    if team is None or game.home_team == team or game.away_team == team:
                        games.append(game)
        
        return sorted(games, key=lambda x: x.game_date)
    
    def get_game_count_by_team(
        self, 
        start_date: datetime, 
        end_date: datetime,
        season: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Get the number of games each team plays in a date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            season: Optional season filter
            
        Returns:
            Dictionary mapping team abbreviations to game counts
        """
        game_counts = defaultdict(int)
        schedules = [self.schedules[season]] if season and season in self.schedules else self.schedules.values()
        
        for schedule in schedules:
            for game in schedule.games:
                if start_date <= game.game_date <= end_date:
                    game_counts[game.home_team] += 1
                    game_counts[game.away_team] += 1
        
        return dict(game_counts)
    
    def get_back_to_back_games(self, team: str, season: Optional[str] = None) -> List[tuple[Game, Game]]:
        """
        Find back-to-back games for a team (games on consecutive days).
        
        Args:
            team: Team abbreviation
            season: Optional season filter
            
        Returns:
            List of tuples containing consecutive game pairs
        """
        team_games = self.get_games_for_team(team, season)
        team_games = sorted(team_games, key=lambda x: x.game_date)
        
        back_to_backs = []
        for i in range(len(team_games) - 1):
            game1 = team_games[i]
            game2 = team_games[i + 1]
            
            # Check if games are on consecutive days
            days_between = (game2.game_date.date() - game1.game_date.date()).days
            if days_between == 1:
                back_to_backs.append((game1, game2))
        
        return back_to_backs
