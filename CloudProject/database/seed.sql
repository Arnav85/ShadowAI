-- Seed data for local development
INSERT INTO migration_jobs (name, target_db, sql_script, dry_run, status, executed_by)
VALUES
    ('initial_schema', 'dev', 'CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY);', true,  'success', 'seed'),
    ('add_users_table', 'dev', 'CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255));', false, 'success', 'seed')
ON CONFLICT DO NOTHING;

INSERT INTO audit_logs (event_type, actor, details)
VALUES
    ('migration_run', 'seed', '{"job_id": 1, "name": "initial_schema", "dry_run": true}'),
    ('migration_run', 'seed', '{"job_id": 2, "name": "add_users_table", "dry_run": false}')
ON CONFLICT DO NOTHING;
