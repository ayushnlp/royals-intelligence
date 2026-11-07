"""initialize uncapped player foundation schema

Revision ID: 001_uncapped_player_foundation
Revises: None
Create Date: 2026-11-07 05:40:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_uncapped_player_foundation'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Competitions
    op.create_table(
        'competitions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('competition_id', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('competition_type', sa.String(length=30), nullable=False),
        sa.Column('governing_body', sa.String(length=50), nullable=False),
        sa.Column('is_domestic', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('competition_id')
    )
    op.create_index('ix_competitions_competition_id', 'competitions', ['competition_id'])

    # 2. Seasons
    op.create_table(
        'seasons',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('season_id', sa.String(length=20), nullable=False),
        sa.Column('competition_id', sa.String(length=36), nullable=False),
        sa.Column('year_start', sa.Integer(), nullable=False),
        sa.Column('year_end', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['competition_id'], ['competitions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('competition_id', 'season_id', name='uq_season_competition')
    )
    op.create_index('ix_seasons_season_id', 'seasons', ['season_id'])

    # 3. Teams
    op.create_table(
        'teams',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('team_code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('short_name', sa.String(length=50), nullable=False),
        sa.Column('is_rr', sa.Boolean(), nullable=False),
        sa.Column('is_domestic', sa.Boolean(), nullable=False),
        sa.Column('state_association', sa.String(length=100), nullable=True),
        sa.Column('primary_color', sa.String(length=20), nullable=True),
        sa.Column('accent_color', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('team_code')
    )
    op.create_index('ix_teams_team_code', 'teams', ['team_code'])

    # 4. Venues
    op.create_table(
        'venues',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('venue_code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('city', sa.String(length=80), nullable=False),
        sa.Column('country', sa.String(length=80), nullable=False),
        sa.Column('is_rr_home', sa.Boolean(), nullable=False),
        sa.Column('altitude_m', sa.Float(), nullable=True),
        sa.Column('pitch_soil_type', sa.String(length=50), nullable=True),
        sa.Column('straight_boundary_m', sa.Float(), nullable=True),
        sa.Column('off_boundary_m', sa.Float(), nullable=True),
        sa.Column('leg_boundary_m', sa.Float(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('venue_code')
    )
    op.create_index('ix_venues_venue_code', 'venues', ['venue_code'])

    # 5. Players
    op.create_table(
        'players',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('canonical_id', sa.String(length=60), nullable=False),
        sa.Column('full_name', sa.String(length=120), nullable=False),
        sa.Column('known_as', sa.String(length=80), nullable=True),
        sa.Column('dob', sa.Date(), nullable=True),
        sa.Column('dob_source', sa.String(length=100), nullable=True),
        sa.Column('dob_verified', sa.Boolean(), nullable=False),
        sa.Column('nationality', sa.String(length=60), nullable=False),
        sa.Column('home_state_association', sa.String(length=100), nullable=True),
        sa.Column('batting_hand', sa.String(length=10), nullable=True),
        sa.Column('bowling_style', sa.String(length=50), nullable=True),
        sa.Column('primary_role', sa.String(length=40), nullable=True),
        sa.Column('is_capped', sa.Boolean(), nullable=False),
        sa.Column('last_international_match_date', sa.Date(), nullable=True),
        sa.Column('international_caps_detail', sa.Text(), nullable=True),
        sa.Column('ipl_debut_season', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('canonical_id')
    )
    op.create_index('ix_players_canonical_id', 'players', ['canonical_id'])
    op.create_index('ix_players_full_name', 'players', ['full_name'])
    op.create_index('ix_players_dob', 'players', ['dob'])
    op.create_index('ix_players_is_capped', 'players', ['is_capped'])

    # 6. Player Identities
    op.create_table(
        'player_identities',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('source_name', sa.String(length=50), nullable=False),
        sa.Column('external_player_id', sa.String(length=100), nullable=False),
        sa.Column('name_as_source', sa.String(length=120), nullable=False),
        sa.Column('alias_names', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('conflict_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('source_name', 'external_player_id', name='uq_source_external_player')
    )
    op.create_index('ix_player_identities_player_id', 'player_identities', ['player_id'])
    op.create_index('ix_player_identity_lookup', 'player_identities', ['source_name', 'name_as_source'])

    # 7. Player Roles
    op.create_table(
        'player_roles',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('role_category', sa.String(length=50), nullable=False),
        sa.Column('batting_phase_preference', sa.String(length=30), nullable=True),
        sa.Column('bowling_phase_preference', sa.String(length=30), nullable=True),
        sa.Column('tactical_niche', sa.String(length=100), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_player_roles_player_id', 'player_roles', ['player_id'])

    # 8. Matches
    op.create_table(
        'matches',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('external_match_id', sa.String(length=100), nullable=False),
        sa.Column('competition_id', sa.String(length=36), nullable=False),
        sa.Column('season_id', sa.String(length=36), nullable=False),
        sa.Column('venue_id', sa.String(length=36), nullable=False),
        sa.Column('team_home_id', sa.String(length=36), nullable=False),
        sa.Column('team_away_id', sa.String(length=36), nullable=False),
        sa.Column('match_date', sa.Date(), nullable=False),
        sa.Column('match_number', sa.Integer(), nullable=True),
        sa.Column('toss_winner_id', sa.String(length=36), nullable=True),
        sa.Column('toss_decision', sa.String(length=10), nullable=True),
        sa.Column('winner_team_id', sa.String(length=36), nullable=True),
        sa.Column('win_margin_runs', sa.Integer(), nullable=True),
        sa.Column('win_margin_wickets', sa.Integer(), nullable=True),
        sa.Column('is_tie', sa.Boolean(), nullable=False),
        sa.Column('is_super_over', sa.Boolean(), nullable=False),
        sa.Column('result_outcome', sa.String(length=100), nullable=False),
        sa.Column('player_of_match_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['competition_id'], ['competitions.id']),
        sa.ForeignKeyConstraint(['player_of_match_id'], ['players.id']),
        sa.ForeignKeyConstraint(['season_id'], ['seasons.id']),
        sa.ForeignKeyConstraint(['team_away_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['team_home_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['toss_winner_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id']),
        sa.ForeignKeyConstraint(['winner_team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('external_match_id')
    )
    op.create_index('ix_matches_competition_id', 'matches', ['competition_id'])
    op.create_index('ix_matches_match_date', 'matches', ['match_date'])
    op.create_index('ix_matches_season_id', 'matches', ['season_id'])
    op.create_index('ix_matches_venue_id', 'matches', ['venue_id'])

    # 9. Innings
    op.create_table(
        'innings',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('innings_number', sa.SmallInteger(), nullable=False),
        sa.Column('batting_team_id', sa.String(length=36), nullable=False),
        sa.Column('bowling_team_id', sa.String(length=36), nullable=False),
        sa.Column('total_runs', sa.Integer(), nullable=False),
        sa.Column('wickets', sa.SmallInteger(), nullable=False),
        sa.Column('overs_completed', sa.Float(), nullable=False),
        sa.Column('is_declared_or_all_out', sa.Boolean(), nullable=False),
        sa.Column('extras_total', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['batting_team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['bowling_team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('match_id', 'innings_number', name='uq_match_innings_number')
    )
    op.create_index('ix_innings_match_id', 'innings', ['match_id'])

    # 10. Player Participations
    op.create_table(
        'player_participations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('team_id', sa.String(length=36), nullable=False),
        sa.Column('role_in_match', sa.String(length=40), nullable=False),
        sa.Column('is_impact_in', sa.Boolean(), nullable=False),
        sa.Column('is_impact_out', sa.Boolean(), nullable=False),
        sa.Column('is_captain', sa.Boolean(), nullable=False),
        sa.Column('is_wicketkeeper', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('match_id', 'player_id', name='uq_match_player_participation')
    )

    # 11. Batting Scorecards
    op.create_table(
        'batting_scorecards',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('innings_number', sa.SmallInteger(), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('team_id', sa.String(length=36), nullable=False),
        sa.Column('batting_position', sa.SmallInteger(), nullable=False),
        sa.Column('runs', sa.SmallInteger(), nullable=False),
        sa.Column('balls_faced', sa.SmallInteger(), nullable=False),
        sa.Column('fours', sa.SmallInteger(), nullable=False),
        sa.Column('sixes', sa.SmallInteger(), nullable=False),
        sa.Column('strike_rate', sa.Float(), nullable=False),
        sa.Column('is_out', sa.Boolean(), nullable=False),
        sa.Column('dismissal_kind', sa.String(length=40), nullable=True),
        sa.Column('bowler_id', sa.String(length=36), nullable=True),
        sa.Column('fielder_id', sa.String(length=36), nullable=True),
        sa.Column('dot_balls', sa.SmallInteger(), nullable=True),
        sa.Column('powerplay_runs', sa.SmallInteger(), nullable=True),
        sa.Column('powerplay_balls', sa.SmallInteger(), nullable=True),
        sa.Column('middle_runs', sa.SmallInteger(), nullable=True),
        sa.Column('middle_balls', sa.SmallInteger(), nullable=True),
        sa.Column('death_runs', sa.SmallInteger(), nullable=True),
        sa.Column('death_balls', sa.SmallInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['bowler_id'], ['players.id']),
        sa.ForeignKeyConstraint(['fielder_id'], ['players.id']),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('match_id', 'innings_number', 'player_id', name='uq_batting_match_innings_player')
    )
    op.create_index('ix_batting_player_perf', 'batting_scorecards', ['player_id', 'runs', 'strike_rate'])

    # 12. Bowling Scorecards
    op.create_table(
        'bowling_scorecards',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('innings_number', sa.SmallInteger(), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('team_id', sa.String(length=36), nullable=False),
        sa.Column('overs', sa.Float(), nullable=False),
        sa.Column('legal_balls', sa.SmallInteger(), nullable=False),
        sa.Column('maidens', sa.SmallInteger(), nullable=False),
        sa.Column('runs_conceded', sa.SmallInteger(), nullable=False),
        sa.Column('wickets', sa.SmallInteger(), nullable=False),
        sa.Column('economy_rate', sa.Float(), nullable=False),
        sa.Column('dot_balls', sa.SmallInteger(), nullable=True),
        sa.Column('wides', sa.SmallInteger(), nullable=False),
        sa.Column('noballs', sa.SmallInteger(), nullable=False),
        sa.Column('fours_conceded', sa.SmallInteger(), nullable=True),
        sa.Column('sixes_conceded', sa.SmallInteger(), nullable=True),
        sa.Column('powerplay_overs', sa.Float(), nullable=True),
        sa.Column('powerplay_wickets', sa.SmallInteger(), nullable=True),
        sa.Column('powerplay_runs', sa.SmallInteger(), nullable=True),
        sa.Column('death_overs', sa.Float(), nullable=True),
        sa.Column('death_wickets', sa.SmallInteger(), nullable=True),
        sa.Column('death_runs', sa.SmallInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('match_id', 'innings_number', 'player_id', name='uq_bowling_match_innings_player')
    )
    op.create_index('ix_bowling_player_perf', 'bowling_scorecards', ['player_id', 'wickets', 'economy_rate'])

    # 13. Ball-by-Ball Deliveries
    op.create_table(
        'ball_by_ball_deliveries',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('innings_id', sa.String(length=36), nullable=False),
        sa.Column('over_number', sa.SmallInteger(), nullable=False),
        sa.Column('ball_in_over', sa.SmallInteger(), nullable=False),
        sa.Column('over_display', sa.Float(), nullable=False),
        sa.Column('phase', sa.String(length=20), nullable=False),
        sa.Column('batting_team_id', sa.String(length=36), nullable=False),
        sa.Column('bowling_team_id', sa.String(length=36), nullable=False),
        sa.Column('striker_id', sa.String(length=36), nullable=False),
        sa.Column('non_striker_id', sa.String(length=36), nullable=False),
        sa.Column('bowler_id', sa.String(length=36), nullable=False),
        sa.Column('batter_runs', sa.SmallInteger(), nullable=False),
        sa.Column('extra_runs', sa.SmallInteger(), nullable=False),
        sa.Column('extra_type', sa.String(length=20), nullable=True),
        sa.Column('total_runs', sa.SmallInteger(), nullable=False),
        sa.Column('is_legal', sa.Boolean(), nullable=False),
        sa.Column('is_boundary_four', sa.Boolean(), nullable=False),
        sa.Column('is_boundary_six', sa.Boolean(), nullable=False),
        sa.Column('is_dot_ball', sa.Boolean(), nullable=False),
        sa.Column('is_wicket', sa.Boolean(), nullable=False),
        sa.Column('dismissal_type', sa.String(length=30), nullable=True),
        sa.Column('player_dismissed_id', sa.String(length=36), nullable=True),
        sa.Column('fielder_id', sa.String(length=36), nullable=True),
        sa.Column('release_speed_kph', sa.Float(), nullable=True),
        sa.Column('delivery_classification', sa.String(length=30), nullable=True),
        sa.Column('shot_type', sa.String(length=40), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.CheckConstraint('total_runs = batter_runs + extra_runs', name='ck_runs_math_balance'),
        sa.ForeignKeyConstraint(['batting_team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['bowler_id'], ['players.id']),
        sa.ForeignKeyConstraint(['bowling_team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['fielder_id'], ['players.id']),
        sa.ForeignKeyConstraint(['innings_id'], ['innings.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['non_striker_id'], ['players.id']),
        sa.ForeignKeyConstraint(['player_dismissed_id'], ['players.id']),
        sa.ForeignKeyConstraint(['striker_id'], ['players.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_delivery_matchup', 'ball_by_ball_deliveries', ['bowler_id', 'striker_id'])
    op.create_index('ix_delivery_over_sequence', 'ball_by_ball_deliveries', ['match_id', 'innings_id', 'over_number', 'ball_in_over'])

    # 14. Fielding Contributions
    op.create_table(
        'fielding_contributions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('catches', sa.SmallInteger(), nullable=False),
        sa.Column('run_outs_direct', sa.SmallInteger(), nullable=False),
        sa.Column('run_outs_assisted', sa.SmallInteger(), nullable=False),
        sa.Column('stumpings', sa.SmallInteger(), nullable=False),
        sa.Column('dropped_catches', sa.SmallInteger(), nullable=True),
        sa.Column('runs_saved', sa.SmallInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('match_id', 'player_id', name='uq_fielding_match_player')
    )

    # 15. Partnerships
    op.create_table(
        'partnerships',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('innings_number', sa.SmallInteger(), nullable=False),
        sa.Column('wicket_number', sa.SmallInteger(), nullable=False),
        sa.Column('batter_1_id', sa.String(length=36), nullable=False),
        sa.Column('batter_2_id', sa.String(length=36), nullable=False),
        sa.Column('runs', sa.SmallInteger(), nullable=False),
        sa.Column('balls', sa.SmallInteger(), nullable=False),
        sa.Column('batter_1_runs', sa.SmallInteger(), nullable=False),
        sa.Column('batter_1_balls', sa.SmallInteger(), nullable=False),
        sa.Column('batter_2_runs', sa.SmallInteger(), nullable=False),
        sa.Column('batter_2_balls', sa.SmallInteger(), nullable=False),
        sa.Column('is_unbroken', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['batter_1_id'], ['players.id']),
        sa.ForeignKeyConstraint(['batter_2_id'], ['players.id']),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('match_id', 'innings_number', 'wicket_number', name='uq_partnership_wicket')
    )

    # 16. Player Match Performances
    op.create_table(
        'player_match_performances',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('team_id', sa.String(length=36), nullable=False),
        sa.Column('batting_runs', sa.SmallInteger(), nullable=False),
        sa.Column('batting_balls', sa.SmallInteger(), nullable=False),
        sa.Column('batting_strike_rate', sa.Float(), nullable=False),
        sa.Column('bowling_wickets', sa.SmallInteger(), nullable=False),
        sa.Column('bowling_runs_conceded', sa.SmallInteger(), nullable=False),
        sa.Column('bowling_overs', sa.Float(), nullable=False),
        sa.Column('bowling_economy', sa.Float(), nullable=False),
        sa.Column('catches', sa.SmallInteger(), nullable=False),
        sa.Column('stumpings', sa.SmallInteger(), nullable=False),
        sa.Column('is_player_of_match', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('match_id', 'player_id', name='uq_player_match_perf')
    )
    op.create_index('ix_player_allround_perf', 'player_match_performances', ['player_id', 'batting_runs', 'bowling_wickets'])

    # 17. Data Sources
    op.create_table(
        'data_sources',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('source_id', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('tier', sa.String(length=20), nullable=False),
        sa.Column('category', sa.String(length=40), nullable=False),
        sa.Column('official_url', sa.String(length=255), nullable=True),
        sa.Column('access_method', sa.String(length=40), nullable=False),
        sa.Column('license_type', sa.String(length=50), nullable=False),
        sa.Column('update_frequency', sa.String(length=40), nullable=False),
        sa.Column('rate_limit_rpm', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('health_status', sa.String(length=30), nullable=False),
        sa.Column('data_classification', sa.String(length=40), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('source_id')
    )
    op.create_index('ix_data_sources_source_id', 'data_sources', ['source_id'])

    # 18. Datasets
    op.create_table(
        'datasets',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('dataset_key', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('competition_id', sa.String(length=50), nullable=True),
        sa.Column('season', sa.String(length=20), nullable=True),
        sa.Column('source_id', sa.String(length=36), nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('data_classification', sa.String(length=40), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['source_id'], ['data_sources.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dataset_key')
    )
    op.create_index('ix_datasets_dataset_key', 'datasets', ['dataset_key'])

    # 19. Ingestion Runs
    op.create_table(
        'ingestion_runs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('run_id', sa.String(length=80), nullable=False),
        sa.Column('source_id', sa.String(length=36), nullable=False),
        sa.Column('competition_id', sa.String(length=50), nullable=True),
        sa.Column('season', sa.String(length=20), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('total_records', sa.Integer(), nullable=False),
        sa.Column('valid_records', sa.Integer(), nullable=False),
        sa.Column('rejected_records', sa.Integer(), nullable=False),
        sa.Column('idempotent_skips', sa.Integer(), nullable=False),
        sa.Column('validation_pass_rate', sa.Float(), nullable=False, server_default='100.0'),
        sa.Column('completeness_percentage', sa.Float(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['source_id'], ['data_sources.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('run_id')
    )
    op.create_index('ix_ingestion_runs_run_id', 'ingestion_runs', ['run_id'])

    # 20. Dataset Manifests
    op.create_table(
        'dataset_manifests',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('manifest_key', sa.String(length=100), nullable=False),
        sa.Column('dataset_id', sa.String(length=36), nullable=False),
        sa.Column('run_id', sa.String(length=80), nullable=False),
        sa.Column('raw_file_count', sa.Integer(), nullable=False),
        sa.Column('processed_file_count', sa.Integer(), nullable=False),
        sa.Column('checksum_sha256', sa.String(length=64), nullable=False),
        sa.Column('completeness_percentage', sa.Float(), nullable=False),
        sa.Column('validation_status', sa.String(length=30), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('manifest_key')
    )

    # 21. Validation Results
    op.create_table(
        'validation_results',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('run_id', sa.String(length=36), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=100), nullable=False),
        sa.Column('rule_name', sa.String(length=80), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('field_name', sa.String(length=50), nullable=True),
        sa.Column('raw_value', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['run_id'], ['ingestion_runs.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 22. Source References
    op.create_table(
        'source_references',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('entity_table', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=36), nullable=False),
        sa.Column('source_name', sa.String(length=50), nullable=False),
        sa.Column('source_file_or_url', sa.String(length=255), nullable=False),
        sa.Column('checksum_sha256', sa.String(length=64), nullable=True),
        sa.Column('ingested_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_source_ref_lookup', 'source_references', ['entity_table', 'entity_id'])

    # 23. Data Quality Records
    op.create_table(
        'data_quality_records',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=36), nullable=False),
        sa.Column('completeness_score', sa.Float(), nullable=False),
        sa.Column('has_conflicts', sa.Boolean(), nullable=False),
        sa.Column('conflict_details', sa.Text(), nullable=True),
        sa.Column('missing_fields', sa.Text(), nullable=True),
        sa.Column('is_quarantined', sa.Boolean(), nullable=False),
        sa.Column('verified_by', sa.String(length=60), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # 24. Uncapped Player Profiles
    op.create_table(
        'uncapped_player_profiles',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('player_id', sa.String(length=36), nullable=False),
        sa.Column('eligibility_status', sa.String(length=30), nullable=False),
        sa.Column('eligibility_verified_at', sa.DateTime(), nullable=True),
        sa.Column('verification_notes', sa.Text(), nullable=True),
        sa.Column('calculated_age_at_cutoff', sa.Float(), nullable=True),
        sa.Column('reference_date_used', sa.Date(), nullable=True),
        sa.Column('international_caps_detail', sa.Text(), nullable=True),
        sa.Column('last_international_appearance_date', sa.Date(), nullable=True),
        sa.Column('eligibility_rule_source', sa.String(length=150), nullable=True),
        sa.Column('rule_version', sa.String(length=50), nullable=True),
        sa.Column('rule_evidence', sa.Text(), nullable=True),
        sa.Column('state_association', sa.String(length=100), nullable=True),
        sa.Column('current_domestic_team', sa.String(length=100), nullable=True),
        sa.Column('primary_discipline', sa.String(length=60), nullable=False),
        sa.Column('scouting_tier', sa.String(length=30), nullable=False),
        sa.Column('is_rr_trialist', sa.Boolean(), nullable=False),
        sa.Column('has_video_evidence', sa.Boolean(), nullable=False),
        sa.Column('data_classification', sa.String(length=40), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('player_id')
    )
    op.create_index('ix_uncapped_player_profiles_eligibility_status', 'uncapped_player_profiles', ['eligibility_status'])
    op.create_index('ix_uncapped_player_profiles_player_id', 'uncapped_player_profiles', ['player_id'])

    # 25. Player Performance Snapshots
    op.create_table(
        'player_performance_snapshots',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('uncapped_profile_id', sa.String(length=36), nullable=False),
        sa.Column('competition_id', sa.String(length=50), nullable=False),
        sa.Column('season', sa.String(length=20), nullable=False),
        sa.Column('matches', sa.SmallInteger(), nullable=False),
        sa.Column('innings_batted', sa.SmallInteger(), nullable=False),
        sa.Column('runs', sa.Integer(), nullable=False),
        sa.Column('balls_faced', sa.Integer(), nullable=False),
        sa.Column('batting_strike_rate', sa.Float(), nullable=False),
        sa.Column('batting_average', sa.Float(), nullable=True),
        sa.Column('boundary_percentage', sa.Float(), nullable=False),
        sa.Column('dot_ball_percentage_batting', sa.Float(), nullable=False),
        sa.Column('powerplay_strike_rate', sa.Float(), nullable=True),
        sa.Column('death_strike_rate', sa.Float(), nullable=True),
        sa.Column('overs_bowled', sa.Float(), nullable=False),
        sa.Column('wickets', sa.SmallInteger(), nullable=False),
        sa.Column('bowling_economy', sa.Float(), nullable=False),
        sa.Column('bowling_strike_rate', sa.Float(), nullable=True),
        sa.Column('bowling_average', sa.Float(), nullable=True),
        sa.Column('death_economy', sa.Float(), nullable=True),
        sa.Column('dot_ball_percentage_bowling', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['uncapped_profile_id'], ['uncapped_player_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('uncapped_profile_id', 'competition_id', 'season', name='uq_snapshot_profile_comp_season')
    )

    # 26. Player Role Assessments
    op.create_table(
        'player_role_assessments',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('uncapped_profile_id', sa.String(length=36), nullable=False),
        sa.Column('archetype_tag', sa.String(length=60), nullable=False),
        sa.Column('powerplay_rating', sa.Float(), nullable=False),
        sa.Column('middle_overs_rating', sa.Float(), nullable=False),
        sa.Column('death_overs_rating', sa.Float(), nullable=False),
        sa.Column('pace_comfort_score', sa.Float(), nullable=False),
        sa.Column('spin_comfort_score', sa.Float(), nullable=False),
        sa.Column('role_readiness', sa.String(length=40), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['uncapped_profile_id'], ['uncapped_player_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 27. Scouting Evaluations
    op.create_table(
        'scouting_evaluations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('uncapped_profile_id', sa.String(length=36), nullable=False),
        sa.Column('scout_identifier', sa.String(length=60), nullable=False),
        sa.Column('evaluation_date', sa.Date(), nullable=False),
        sa.Column('competition_or_trial', sa.String(length=100), nullable=False),
        sa.Column('technical_skill_rating', sa.Float(), nullable=False),
        sa.Column('temperament_rating', sa.Float(), nullable=False),
        sa.Column('athleticism_rating', sa.Float(), nullable=False),
        sa.Column('tactical_iq_rating', sa.Float(), nullable=False),
        sa.Column('ceiling_potential_rating', sa.Float(), nullable=False),
        sa.Column('strengths_summary', sa.Text(), nullable=False),
        sa.Column('development_areas', sa.Text(), nullable=False),
        sa.Column('scout_recommendation', sa.String(length=40), nullable=False),
        sa.Column('proprietary_notes', sa.Text(), nullable=True),
        sa.Column('data_classification', sa.String(length=40), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['uncapped_profile_id'], ['uncapped_player_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 28. Scouting Evidence
    op.create_table(
        'scouting_evidence',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('evaluation_id', sa.String(length=36), nullable=False),
        sa.Column('evidence_type', sa.String(length=40), nullable=False),
        sa.Column('metric_name', sa.String(length=60), nullable=False),
        sa.Column('metric_value', sa.String(length=100), nullable=False),
        sa.Column('source_reference', sa.String(length=255), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['evaluation_id'], ['scouting_evaluations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 29. Player Comparisons
    op.create_table(
        'player_comparisons',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('subject_player_id', sa.String(length=36), nullable=False),
        sa.Column('benchmark_player_id', sa.String(length=36), nullable=False),
        sa.Column('comparison_context', sa.String(length=80), nullable=False),
        sa.Column('similarity_score', sa.Float(), nullable=False),
        sa.Column('comparison_summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['benchmark_player_id'], ['players.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_player_id'], ['players.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('subject_player_id', 'benchmark_player_id', 'comparison_context', name='uq_player_benchmark_context')
    )


def downgrade() -> None:
    # Drop in exact reverse topological order
    op.drop_table('player_comparisons')
    op.drop_table('scouting_evidence')
    op.drop_table('scouting_evaluations')
    op.drop_table('player_role_assessments')
    op.drop_table('player_performance_snapshots')
    op.drop_table('uncapped_player_profiles')
    op.drop_table('data_quality_records')
    op.drop_table('source_references')
    op.drop_table('validation_results')
    op.drop_table('dataset_manifests')
    op.drop_table('ingestion_runs')
    op.drop_table('datasets')
    op.drop_table('data_sources')
    op.drop_table('player_match_performances')
    op.drop_table('partnerships')
    op.drop_table('fielding_contributions')
    op.drop_table('ball_by_ball_deliveries')
    op.drop_table('bowling_scorecards')
    op.drop_table('batting_scorecards')
    op.drop_table('player_participations')
    op.drop_table('innings')
    op.drop_table('matches')
    op.drop_table('player_roles')
    op.drop_table('player_identities')
    op.drop_table('players')
    op.drop_table('venues')
    op.drop_table('teams')
    op.drop_table('seasons')
    op.drop_table('competitions')
