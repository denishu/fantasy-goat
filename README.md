# Fantasy GOAT 🏀

Fantasy Basketball Stat Tracker and Analysis Tool supporting multiple formats, game schedules, and AI analytics.

## Features

- **Player Management**: Track NBA players and their information
- **Stat Tracking**: Record and analyze game-by-game statistics
- **Multiple Fantasy Formats**: 
  - Points-based scoring
  - Category-based leagues (H2H)
  - Rotisserie leagues
- **Game Schedule Management**: Track upcoming games and team schedules
- **Advanced Analytics**:
  - Performance trends analysis
  - Consistency scoring
  - Player comparisons
  - Projections (coming soon with AI)
- **AI Analytics** (Planned): Machine learning-based projections and insights

## Installation

```bash
# Clone the repository
git clone https://github.com/denishu/fantasy-goat.git
cd fantasy-goat

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

### Add a Player
```bash
fantasy-goat player add --player-id lbj23 --name "LeBron James" --team LAL --position SF --jersey 23
```

### Add Game Stats
```bash
fantasy-goat stats add --player-id lbj23 --date 2024-10-26 --opponent GSW \
  --points 28 --rebounds 8 --assists 7 --steals 2 --blocks 1 --turnovers 3 \
  --minutes 35.5 --fgm 10 --fga 20 --threes 3 --three-attempts 8
```

### View Player Stats
```bash
# Recent games
fantasy-goat stats show --player-id lbj23 --games 10

# Season averages
fantasy-goat stats season --player-id lbj23 --season 2024-25
```

### Manage Schedule
```bash
# Add a game
fantasy-goat schedule add --game-id game_001 --date "2024-10-27 19:30" \
  --home GSW --away LAL --season 2024-25

# View upcoming games
fantasy-goat schedule upcoming --days 7
fantasy-goat schedule upcoming --days 7 --team LAL
```

### Analyze Performance
```bash
# View performance trends
fantasy-goat analyze trends --player-id lbj23

# Check consistency
fantasy-goat analyze consistency --player-id lbj23

# Compare players
fantasy-goat analyze compare --player1 lbj23 --player2 kd35
```

### Calculate Fantasy Points
```bash
fantasy-goat fantasy points --player-id lbj23 --games 10
```

### Check AI Analytics Status
```bash
fantasy-goat ai-status
```

## Project Structure

```
fantasy-goat/
├── src/fantasy_goat/
│   ├── models/          # Data models (Player, Stats, Game, Team, Format)
│   ├── core/            # Core functionality (StatTracker, Calculator, ScheduleManager)
│   ├── analytics/       # Analytics and projections
│   └── cli/             # Command-line interface
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
└── README.md           # This file
```

## Supported Fantasy Formats

### Points-Based Scoring
Customizable scoring settings for points leagues. Default scoring:
- Points: 1.0
- Rebounds: 1.2
- Assists: 1.5
- Steals: 3.0
- Blocks: 3.0
- Turnovers: -1.0
- 3-Pointers: +0.5 bonus

### Category-Based Leagues
Track performance across multiple statistical categories:
- Standard 9-cat: PTS, REB, AST, STL, BLK, FG%, FT%, 3PM, TO
- Customizable category selection

### Rotisserie Leagues
Season-long rankings across all categories.

## Roadmap

- [x] Core data models
- [x] Stat tracking functionality
- [x] Multiple fantasy format support
- [x] Game schedule management
- [x] Basic analytics (trends, consistency, comparisons)
- [x] CLI interface
- [ ] Data persistence (database integration)
- [ ] Import from external sources (ESPN, Yahoo, NBA Stats API)
- [ ] Web interface
- [ ] AI-powered projections
- [ ] Machine learning models for player performance
- [ ] Injury impact analysis
- [ ] Advanced matchup analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details