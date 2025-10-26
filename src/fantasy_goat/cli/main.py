"""Command-line interface for Fantasy GOAT."""

import click
import json
from datetime import datetime, date
from typing import Optional

from fantasy_goat.models.player import Player
from fantasy_goat.models.stats import PlayerStats
from fantasy_goat.models.game import Game, Schedule
from fantasy_goat.models.format import FantasyFormat, PointsScoringSettings, CategoryScoringSettings
from fantasy_goat.core.stat_tracker import StatTracker
from fantasy_goat.core.schedule_manager import ScheduleManager
from fantasy_goat.core.calculator import FantasyPointsCalculator, CategoryComparator
from fantasy_goat.analytics.analyzer import PlayerAnalyzer, AIAnalyticsPreparation


# Global instances (in a real app, these would be persisted)
stat_tracker = StatTracker()
schedule_manager = ScheduleManager()


@click.group()
@click.version_option(version='0.1.0')
def main():
    """Fantasy GOAT - Fantasy Basketball Stat Tracker and Analysis Tool."""
    pass


@main.group()
def player():
    """Manage players."""
    pass


@player.command('add')
@click.option('--player-id', required=True, help='Unique player identifier')
@click.option('--name', required=True, help='Player name')
@click.option('--team', required=True, help='NBA team abbreviation')
@click.option('--position', required=True, help='Player position')
@click.option('--jersey', type=int, help='Jersey number')
def add_player(player_id: str, name: str, team: str, position: str, jersey: Optional[int]):
    """Add a new player to the tracker."""
    try:
        player_obj = Player(
            player_id=player_id,
            name=name,
            team=team,
            position=position,
            jersey_number=jersey
        )
        stat_tracker.add_player(player_obj)
        click.echo(f"✓ Added player: {name} ({team})")
    except Exception as e:
        click.echo(f"✗ Error adding player: {e}", err=True)


@player.command('list')
def list_players():
    """List all players."""
    if not stat_tracker.players:
        click.echo("No players found.")
        return
    
    click.echo("\nPlayers:")
    click.echo("-" * 60)
    for player_id, player in stat_tracker.players.items():
        click.echo(f"{player.name:30s} {player.team:5s} {player.position:3s}")


@main.group()
def stats():
    """Manage player statistics."""
    pass


@stats.command('add')
@click.option('--player-id', required=True, help='Player identifier')
@click.option('--date', required=True, help='Game date (YYYY-MM-DD)')
@click.option('--opponent', required=True, help='Opponent team abbreviation')
@click.option('--points', type=int, default=0)
@click.option('--rebounds', type=int, default=0)
@click.option('--assists', type=int, default=0)
@click.option('--steals', type=int, default=0)
@click.option('--blocks', type=int, default=0)
@click.option('--turnovers', type=int, default=0)
@click.option('--minutes', type=float, default=0.0)
@click.option('--fgm', type=int, default=0, help='Field goals made')
@click.option('--fga', type=int, default=0, help='Field goals attempted')
@click.option('--threes', type=int, default=0, help='Three-pointers made')
@click.option('--three-attempts', type=int, default=0, help='Three-pointers attempted')
def add_stats(player_id: str, date: str, opponent: str, **kwargs):
    """Add game statistics for a player."""
    try:
        game_date = datetime.strptime(date, '%Y-%m-%d').date()
        game_stats = PlayerStats(
            player_id=player_id,
            game_date=game_date,
            opponent=opponent,
            minutes_played=kwargs['minutes'],
            points=kwargs['points'],
            rebounds=kwargs['rebounds'],
            assists=kwargs['assists'],
            steals=kwargs['steals'],
            blocks=kwargs['blocks'],
            turnovers=kwargs['turnovers'],
            field_goals_made=kwargs['fgm'],
            field_goals_attempted=kwargs['fga'],
            three_pointers_made=kwargs['threes'],
            three_pointers_attempted=kwargs['three_attempts']
        )
        stat_tracker.add_game_stats(game_stats)
        click.echo(f"✓ Added stats for {player_id} vs {opponent} on {date}")
    except Exception as e:
        click.echo(f"✗ Error adding stats: {e}", err=True)


@stats.command('show')
@click.option('--player-id', required=True, help='Player identifier')
@click.option('--games', type=int, default=10, help='Number of recent games to show')
def show_stats(player_id: str, games: int):
    """Show recent statistics for a player."""
    recent_games = stat_tracker.get_last_n_games(player_id, games)
    
    if not recent_games:
        click.echo(f"No statistics found for player {player_id}")
        return
    
    player = stat_tracker.players.get(player_id)
    player_name = player.name if player else player_id
    
    click.echo(f"\nRecent games for {player_name}:")
    click.echo("-" * 80)
    click.echo(f"{'Date':12s} {'Opp':5s} {'MIN':5s} {'PTS':4s} {'REB':4s} {'AST':4s} {'STL':4s} {'BLK':4s}")
    click.echo("-" * 80)
    
    for game in recent_games:
        click.echo(
            f"{str(game.game_date):12s} "
            f"{game.opponent:5s} "
            f"{game.minutes_played:5.1f} "
            f"{game.points:4d} "
            f"{game.rebounds:4d} "
            f"{game.assists:4d} "
            f"{game.steals:4d} "
            f"{game.blocks:4d}"
        )


@stats.command('season')
@click.option('--player-id', required=True, help='Player identifier')
@click.option('--season', default='2024-25', help='Season identifier')
def season_stats(player_id: str, season: str):
    """Show season statistics for a player."""
    season_data = stat_tracker.calculate_season_stats(player_id, season)
    
    if not season_data:
        click.echo(f"No season statistics found for player {player_id}")
        return
    
    player = stat_tracker.players.get(player_id)
    player_name = player.name if player else player_id
    
    click.echo(f"\n{season} Season Stats for {player_name}:")
    click.echo("-" * 60)
    click.echo(f"Games Played: {season_data.games_played}")
    click.echo(f"\nAverages:")
    click.echo(f"  Points:   {season_data.avg_points:.1f}")
    click.echo(f"  Rebounds: {season_data.avg_rebounds:.1f}")
    click.echo(f"  Assists:  {season_data.avg_assists:.1f}")
    click.echo(f"  Steals:   {season_data.avg_steals:.1f}")
    click.echo(f"  Blocks:   {season_data.avg_blocks:.1f}")
    click.echo(f"  Minutes:  {season_data.avg_minutes:.1f}")
    
    if season_data.field_goal_percentage:
        click.echo(f"\nShooting:")
        click.echo(f"  FG%:  {season_data.field_goal_percentage:.1%}")
        if season_data.three_point_percentage:
            click.echo(f"  3P%:  {season_data.three_point_percentage:.1%}")
        if season_data.free_throw_percentage:
            click.echo(f"  FT%:  {season_data.free_throw_percentage:.1%}")


@main.group()
def schedule():
    """Manage game schedules."""
    pass


@schedule.command('add')
@click.option('--game-id', required=True, help='Unique game identifier')
@click.option('--date', required=True, help='Game date and time (YYYY-MM-DD HH:MM)')
@click.option('--home', required=True, help='Home team abbreviation')
@click.option('--away', required=True, help='Away team abbreviation')
@click.option('--season', default='2024-25', help='Season identifier')
def add_game(game_id: str, date: str, home: str, away: str, season: str):
    """Add a game to the schedule."""
    try:
        game_date = datetime.strptime(date, '%Y-%m-%d %H:%M')
        game = Game(
            game_id=game_id,
            game_date=game_date,
            home_team=home,
            away_team=away
        )
        schedule_manager.add_game(season, game)
        click.echo(f"✓ Added game: {away} @ {home} on {date}")
    except Exception as e:
        click.echo(f"✗ Error adding game: {e}", err=True)


@schedule.command('upcoming')
@click.option('--days', type=int, default=7, help='Number of days to look ahead')
@click.option('--team', help='Filter by team abbreviation')
def upcoming_games(days: int, team: Optional[str]):
    """Show upcoming games."""
    games = schedule_manager.get_upcoming_games(days_ahead=days, team=team)
    
    if not games:
        click.echo("No upcoming games found.")
        return
    
    title = f"Upcoming games" + (f" for {team}" if team else "") + f" (next {days} days)"
    click.echo(f"\n{title}:")
    click.echo("-" * 60)
    
    for game in games:
        date_str = game.game_date.strftime('%Y-%m-%d %H:%M')
        click.echo(f"{date_str} - {game.away_team} @ {game.home_team}")


@main.group()
def analyze():
    """Analyze player performance."""
    pass


@analyze.command('trends')
@click.option('--player-id', required=True, help='Player identifier')
def analyze_trends(player_id: str):
    """Analyze player performance trends."""
    analyzer = PlayerAnalyzer(stat_tracker)
    trends = analyzer.get_trending_stats(player_id)
    
    if not trends:
        click.echo(f"Insufficient data to analyze trends for {player_id}")
        return
    
    player = stat_tracker.players.get(player_id)
    player_name = player.name if player else player_id
    
    click.echo(f"\nPerformance Trends for {player_name}:")
    click.echo("-" * 60)
    
    for stat, change in trends.items():
        trend_icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        click.echo(f"{stat:20s}: {change:+.1f}% {trend_icon}")


@analyze.command('consistency')
@click.option('--player-id', required=True, help='Player identifier')
def analyze_consistency(player_id: str):
    """Analyze player consistency."""
    analyzer = PlayerAnalyzer(stat_tracker)
    consistency = analyzer.get_consistency_score(player_id)
    
    if not consistency:
        click.echo(f"Insufficient data to analyze consistency for {player_id}")
        return
    
    player = stat_tracker.players.get(player_id)
    player_name = player.name if player else player_id
    
    click.echo(f"\nConsistency Analysis for {player_name}:")
    click.echo("-" * 60)
    click.echo("(Lower coefficient of variation = more consistent)")
    click.echo()
    
    for stat, cv in consistency.items():
        rating = "Very Consistent" if cv < 20 else "Consistent" if cv < 40 else "Inconsistent"
        click.echo(f"{stat:20s}: {cv:5.1f}% - {rating}")


@analyze.command('compare')
@click.option('--player1', required=True, help='First player ID')
@click.option('--player2', required=True, help='Second player ID')
def compare_players(player1: str, player2: str):
    """Compare two players."""
    analyzer = PlayerAnalyzer(stat_tracker)
    comparison = analyzer.compare_players(player1, player2)
    
    if not comparison:
        click.echo("Insufficient data to compare players")
        return
    
    p1 = stat_tracker.players.get(player1)
    p2 = stat_tracker.players.get(player2)
    p1_name = p1.name if p1 else player1
    p2_name = p2.name if p2 else player2
    
    click.echo(f"\nPlayer Comparison: {p1_name} vs {p2_name}")
    click.echo("=" * 60)
    
    stats = ['avg_points', 'avg_rebounds', 'avg_assists']
    for stat in stats:
        val1 = comparison['player1'].get(stat, 0)
        val2 = comparison['player2'].get(stat, 0)
        click.echo(f"\n{stat.replace('avg_', '').title()}:")
        click.echo(f"  {p1_name:30s}: {val1:.1f}")
        click.echo(f"  {p2_name:30s}: {val2:.1f}")


@main.group()
def fantasy():
    """Fantasy scoring calculations."""
    pass


@fantasy.command('points')
@click.option('--player-id', required=True, help='Player identifier')
@click.option('--games', type=int, default=10, help='Number of recent games')
def fantasy_points(player_id: str, games: int):
    """Calculate fantasy points for recent games."""
    # Use default ESPN scoring
    settings = PointsScoringSettings()
    calculator = FantasyPointsCalculator(settings)
    
    recent_games = stat_tracker.get_last_n_games(player_id, games)
    
    if not recent_games:
        click.echo(f"No games found for player {player_id}")
        return
    
    player = stat_tracker.players.get(player_id)
    player_name = player.name if player else player_id
    
    click.echo(f"\nFantasy Points for {player_name} (last {len(recent_games)} games):")
    click.echo("-" * 60)
    
    total_points = 0.0
    for game in recent_games:
        fp = calculator.calculate_fantasy_points(game)
        total_points += fp
        click.echo(f"{str(game.game_date):12s} vs {game.opponent:5s}: {fp:.1f} FPTS")
    
    avg_points = total_points / len(recent_games)
    click.echo("-" * 60)
    click.echo(f"Average: {avg_points:.1f} FPTS")


@main.command('ai-status')
def ai_status():
    """Check AI analytics status."""
    click.echo("\n🤖 AI Analytics Status")
    click.echo("=" * 60)
    click.echo("Status: Coming Soon!")
    click.echo()
    click.echo("Future AI features will include:")
    click.echo("  • Machine learning-based player projections")
    click.echo("  • Advanced pattern recognition")
    click.echo("  • Injury impact analysis")
    click.echo("  • Matchup-based predictions")
    click.echo("  • Player clustering and similarity analysis")
    click.echo()


if __name__ == '__main__':
    main()
