"""venue pitch and weather intelligence schema

Revision ID: 002_venue_pitch_weather
Revises: 001_uncapped_player_foundation
Create Date: 2026-11-07 13:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_venue_pitch_weather'
down_revision: Union[str, None] = '001_uncapped_player_foundation'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add provenance columns to venues
    with op.batch_alter_table('venues', schema=None) as batch_op:
        batch_op.add_column(sa.Column('boundary_dimensions_source', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('coordinates_source', sa.String(length=100), nullable=True))

    # 2. Match Weather Observations table
    op.create_table(
        'match_weather_observations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=False),
        sa.Column('venue_id', sa.String(length=36), nullable=False),
        sa.Column('observation_time', sa.DateTime(), nullable=False),
        sa.Column('phase_in_match', sa.String(length=30), nullable=False),
        sa.Column('temperature_c', sa.Float(), nullable=False),
        sa.Column('relative_humidity_pct', sa.Float(), nullable=False),
        sa.Column('dew_point_c', sa.Float(), nullable=False),
        sa.Column('precipitation_mm', sa.Float(), nullable=False),
        sa.Column('wind_speed_kph', sa.Float(), nullable=False),
        sa.Column('wind_direction_deg', sa.Float(), nullable=False),
        sa.Column('cloud_cover_pct', sa.Float(), nullable=False),
        sa.Column('weather_condition', sa.String(length=50), nullable=False),
        sa.Column('is_forecast', sa.Boolean(), nullable=False),
        sa.Column('source_name', sa.String(length=50), nullable=False),
        sa.Column('retrieval_timestamp', sa.DateTime(), nullable=False),
        sa.Column('reliability', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_match_weather_match_id', 'match_weather_observations', ['match_id'])
    op.create_index('ix_match_weather_venue_id', 'match_weather_observations', ['venue_id'])

    # 3. Venue Pitch Reports table
    op.create_table(
        'venue_pitch_reports',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('venue_id', sa.String(length=36), nullable=False),
        sa.Column('match_id', sa.String(length=36), nullable=True),
        sa.Column('report_date', sa.Date(), nullable=False),
        sa.Column('pitch_soil_type', sa.String(length=50), nullable=False),
        sa.Column('grass_coverage', sa.String(length=40), nullable=True),
        sa.Column('expected_pace_bounce', sa.String(length=50), nullable=True),
        sa.Column('expected_turn', sa.String(length=50), nullable=True),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('reporter_reference', sa.String(length=100), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id']),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_venue_pitch_reports_venue_id', 'venue_pitch_reports', ['venue_id'])
    op.create_index('ix_venue_pitch_reports_match_id', 'venue_pitch_reports', ['match_id'])
    op.create_index('ix_venue_pitch_reports_report_date', 'venue_pitch_reports', ['report_date'])


def downgrade() -> None:
    op.drop_index('ix_venue_pitch_reports_report_date', table_name='venue_pitch_reports')
    op.drop_index('ix_venue_pitch_reports_match_id', table_name='venue_pitch_reports')
    op.drop_index('ix_venue_pitch_reports_venue_id', table_name='venue_pitch_reports')
    op.drop_table('venue_pitch_reports')

    op.drop_index('ix_match_weather_venue_id', table_name='match_weather_observations')
    op.drop_index('ix_match_weather_match_id', table_name='match_weather_observations')
    op.drop_table('match_weather_observations')

    with op.batch_alter_table('venues', schema=None) as batch_op:
        batch_op.drop_column('coordinates_source')
        batch_op.drop_column('boundary_dimensions_source')

