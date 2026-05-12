-- init.sql
-- Runs once when the PostgreSQL container is first created.
-- Flask-Migrate will handle the actual table creation via Alembic migrations.

-- Ensure the database exists (Postgres already creates it via POSTGRES_DB env var,
-- but this guard is harmless).
SELECT 'Database initialised at ' || NOW()::text AS info;
