#!/usr/bin/env python
"""Example script demonstrating Fantasy GOAT functionality."""

from datetime import date, datetime, timedelta
from fantasy_goat.models.player import Player
from fantasy_goat.models.stats import PlayerStats
from fantasy_goat.models.game import Game, Schedule
from fantasy_goat.models.format import PointsScoringSettings
from fantasy_goat.core.stat_tracker import StatTracker
from fantasy_goat.core.schedule_manager import ScheduleManager
from fantasy_goat.core.calculator import FantasyPointsCalculator
from fantasy_goat.analytics.analyzer import PlayerAnalyzer


def main():
    """Run example demonstration."""
    print("=" * 70)
    print("Fantasy GOAT - Example Demonstration")
    print("=" * 70)
    print()
    
    # Create stat tracker
    tracker = StatTracker()
    
    # Add players
    print("1. Adding Players...")
    lebron = Player(
        player_id="lbj23",
        name="LeBron James",
        team="LAL",
        position="SF",
        jersey_number=23
    )
    durant = Player(
        player_id="kd35",
        name="Kevin Durant",
        team="PHX",
        position="SF",
        jersey_number=35
    )
    
    tracker.add_player(lebron)
    tracker.add_player(durant)
    print(f"   ✓ Added {lebron.name}")
    print(f"   ✓ Added {durant.name}")
    print()
    
    # Add game stats for LeBron
    print("2. Adding Game Stats...")
    lebron_games = [
        PlayerStats(
            player_id="lbj23",
            game_date=date(2024, 10, 20),
            opponent="GSW",
            minutes_played=35.5,
            points=28,
            rebounds=8,
            assists=7,
            steals=2,
            blocks=1,
            turnovers=3,
            field_goals_made=10,
            field_goals_attempted=20,
            three_pointers_made=3,
            three_pointers_attempted=8
        ),
        PlayerStats(
            player_id="lbj23",
            game_date=date(2024, 10, 22),
            opponent="LAC",
            minutes_played=32.0,
            points=25,
            rebounds=6,
            assists=9,
            steals=1,
            blocks=0,
            turnovers=2,
            field_goals_made=9,
            field_goals_attempted=18,
            three_pointers_made=2,
            three_pointers_attempted=5
        ),
        PlayerStats(
            player_id="lbj23",
            game_date=date(2024, 10, 24),
            opponent="PHX",
            minutes_played=34.0,
            points=30,
            rebounds=10,
            assists=8,
            steals=2,
            blocks=1,
            turnovers=4,
            field_goals_made=11,
            field_goals_attempted=22,
            three_pointers_made=4,
            three_pointers_attempted=9
        )
    ]
    
    for game in lebron_games:
        tracker.add_game_stats(game)
    print(f"   ✓ Added {len(lebron_games)} games for LeBron")
    print()
    
    # Calculate season stats
    print("3. Season Statistics...")
    season_stats = tracker.calculate_season_stats("lbj23", "2024-25")
    if season_stats:
        print(f"   Games Played: {season_stats.games_played}")
        print(f"   Averages:")
        print(f"     Points:   {season_stats.avg_points:.1f}")
        print(f"     Rebounds: {season_stats.avg_rebounds:.1f}")
        print(f"     Assists:  {season_stats.avg_assists:.1f}")
        print(f"     Steals:   {season_stats.avg_steals:.1f}")
        print(f"   Shooting:")
        if season_stats.field_goal_percentage:
            print(f"     FG%: {season_stats.field_goal_percentage:.1%}")
        if season_stats.three_point_percentage:
            print(f"     3P%: {season_stats.three_point_percentage:.1%}")
    print()
    
    # Calculate fantasy points
    print("4. Fantasy Points (Default Scoring)...")
    settings = PointsScoringSettings()
    calculator = FantasyPointsCalculator(settings)
    
    total_fp = 0
    for game in lebron_games:
        fp = calculator.calculate_fantasy_points(game)
        total_fp += fp
        print(f"   {game.game_date} vs {game.opponent}: {fp:.1f} FPTS")
    
    avg_fp = total_fp / len(lebron_games)
    print(f"   Average: {avg_fp:.1f} FPTS")
    print()
    
    # Schedule management
    print("5. Schedule Management...")
    schedule_manager = ScheduleManager()
    
    base_date = datetime.now() + timedelta(days=1)
    upcoming_games = [
        Game(
            game_id="game_001",
            game_date=base_date,
            home_team="LAL",
            away_team="GSW"
        ),
        Game(
            game_id="game_002",
            game_date=base_date + timedelta(days=2),
            home_team="PHX",
            away_team="LAL"
        ),
        Game(
            game_id="game_003",
            game_date=base_date + timedelta(days=3),
            home_team="LAL",
            away_team="BOS"
        )
    ]
    
    for game in upcoming_games:
        schedule_manager.add_game("2024-25", game)
    
    lal_games = schedule_manager.get_games_for_team("LAL", "2024-25")
    print(f"   LAL has {len(lal_games)} upcoming games:")
    for game in lal_games:
        opponent = game.away_team if game.home_team == "LAL" else game.home_team
        location = "vs" if game.home_team == "LAL" else "@"
        print(f"     {game.game_date.strftime('%Y-%m-%d')} {location} {opponent}")
    print()
    
    # Analytics
    print("6. Player Analytics...")
    analyzer = PlayerAnalyzer(tracker)
    
    # Add more games for trend analysis
    more_games = [
        PlayerStats(
            player_id="lbj23",
            game_date=date(2024, 10, 15),
            opponent="DEN",
            points=20, rebounds=5, assists=6
        ),
        PlayerStats(
            player_id="lbj23",
            game_date=date(2024, 10, 17),
            opponent="MIA",
            points=22, rebounds=6, assists=5
        )
    ]
    for game in more_games:
        tracker.add_game_stats(game)
    
    trends = analyzer.get_trending_stats("lbj23", recent_games=3, comparison_games=5)
    if trends:
        print("   Performance Trends (last 3 vs previous games):")
        for stat, change in trends.items():
            direction = "↑" if change > 0 else "↓" if change < 0 else "→"
            print(f"     {stat:20s}: {change:+6.1f}% {direction}")
    print()
    
    # AI Analytics placeholder
    print("7. AI Analytics Status...")
    print("   🤖 Status: Coming Soon!")
    print("   Future features:")
    print("     • ML-based projections")
    print("     • Advanced pattern recognition")
    print("     • Injury impact analysis")
    print()
    
    print("=" * 70)
    print("Example demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
