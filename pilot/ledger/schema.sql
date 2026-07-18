PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE missions (
  id TEXT PRIMARY KEY,
  version TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  content_hash TEXT NOT NULL
);

CREATE TABLE attempts (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  mission_id TEXT NOT NULL REFERENCES missions(id),
  mission_version TEXT NOT NULL,
  attempt_number INTEGER NOT NULL CHECK (attempt_number > 0),
  status TEXT NOT NULL CHECK (status IN ('STARTED','SUBMITTED','ASSESSED','REMEDIATION','MASTERED','ABANDONED')),
  started_at TEXT NOT NULL,
  submitted_at TEXT,
  completed_at TEXT,
  UNIQUE (user_id, mission_id, attempt_number)
);

CREATE TABLE evidence_metadata (
  id TEXT PRIMARY KEY,
  attempt_id TEXT NOT NULL REFERENCES attempts(id),
  classification TEXT NOT NULL CHECK (classification IN ('PUBLIC','INTERNAL','PRIVATE','SENSITIVE','PROHIBITED')),
  status TEXT NOT NULL CHECK (status IN ('DECLARED','STORED','VALIDATED','REJECTED','BLOCKED','DELETED')),
  private_storage_ref TEXT,
  content_hash TEXT,
  redacted INTEGER NOT NULL DEFAULT 0 CHECK (redacted IN (0,1)),
  retention_until TEXT,
  created_at TEXT NOT NULL,
  deleted_at TEXT,
  CHECK (classification <> 'PROHIBITED' OR (private_storage_ref IS NULL AND content_hash IS NULL))
);

CREATE TABLE assessments (
  id TEXT PRIMARY KEY,
  attempt_id TEXT NOT NULL UNIQUE REFERENCES attempts(id),
  rubric_id TEXT NOT NULL,
  rubric_version TEXT NOT NULL,
  total_score REAL NOT NULL CHECK (total_score BETWEEN 0 AND 100),
  result TEXT NOT NULL CHECK (result IN ('NOT_COMPLETED','COMPLETED_WITH_REMEDIATION','MASTERED','MASTERED_EXCELLENCE')),
  eliminatories_passed INTEGER NOT NULL CHECK (eliminatories_passed IN (0,1)),
  assessed_at TEXT NOT NULL,
  assessor TEXT NOT NULL
);

CREATE TABLE assessment_criteria (
  assessment_id TEXT NOT NULL REFERENCES assessments(id),
  criterion_id TEXT NOT NULL,
  score REAL NOT NULL CHECK (score BETWEEN 0 AND 100),
  weight REAL NOT NULL CHECK (weight > 0 AND weight <= 1),
  PRIMARY KEY (assessment_id, criterion_id)
);

CREATE TABLE xp_transactions (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  attempt_id TEXT REFERENCES attempts(id),
  transaction_type TEXT NOT NULL CHECK (transaction_type IN ('MISSION','DEBUG','REMEDIATION','RETENTION','BADGE','ADJUSTMENT')),
  amount INTEGER NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE retention_reviews (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  mission_id TEXT REFERENCES missions(id),
  module_id TEXT,
  interval_code TEXT NOT NULL CHECK (interval_code IN ('24H','7D','30D','90D')),
  due_at TEXT NOT NULL,
  completed_at TEXT,
  score REAL CHECK (score BETWEEN 0 AND 100),
  result TEXT CHECK (result IN ('PENDING','PASS','REMEDIATION','MISSED')),
  CHECK (mission_id IS NOT NULL OR module_id IS NOT NULL)
);

CREATE TABLE prompt_runs (
  id TEXT PRIMARY KEY,
  prompt_id TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  variation_id TEXT NOT NULL,
  input_hash TEXT NOT NULL,
  result TEXT NOT NULL CHECK (result IN ('PASS','FAIL')),
  executed_at TEXT NOT NULL,
  UNIQUE (prompt_id, prompt_version, variation_id)
);

CREATE TABLE skill_candidates (
  id TEXT PRIMARY KEY,
  version TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('EXPERIMENTAL','PILOT','VALIDATED','STABLE','DEPRECATED','ARCHIVED')),
  source_prompt_id TEXT,
  limitations TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE audit_events (
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  actor_id TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  transition_id TEXT,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE INDEX idx_attempts_user_mission ON attempts(user_id, mission_id);
CREATE INDEX idx_evidence_attempt ON evidence_metadata(attempt_id);
CREATE INDEX idx_retention_due ON retention_reviews(due_at, result);
CREATE INDEX idx_audit_entity ON audit_events(entity_type, entity_id, created_at);
