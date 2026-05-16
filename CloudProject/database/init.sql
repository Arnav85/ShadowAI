-- Cloud Janitor — PostgreSQL initialisation script
-- This runs automatically when the Docker container first starts.

CREATE TABLE IF NOT EXISTS migration_jobs (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    target_db   VARCHAR(100) NOT NULL,
    sql_script  TEXT         NOT NULL,
    dry_run     BOOLEAN      DEFAULT FALSE,
    status      VARCHAR(50)  DEFAULT 'pending',
    output      TEXT,
    error       TEXT,
    executed_by VARCHAR(100) DEFAULT 'api',
    created_at  TIMESTAMPTZ  DEFAULT NOW(),
    updated_at  TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id          SERIAL PRIMARY KEY,
    event_type  VARCHAR(100) NOT NULL,
    actor       VARCHAR(100) DEFAULT 'api',
    details     JSONB,
    created_at  TIMESTAMPTZ  DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_migration_jobs_status  ON migration_jobs(status);
CREATE INDEX IF NOT EXISTS idx_migration_jobs_target  ON migration_jobs(target_db);
