CREATE TABLE IF NOT EXISTS assets (
  id UUID PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  asset_type VARCHAR(60) NOT NULL,
  business_criticality VARCHAR(20) NOT NULL,
  owner VARCHAR(120),
  tags JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS threat_scenarios (
  id UUID PRIMARY KEY,
  asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  framework VARCHAR(20) NOT NULL DEFAULT 'STRIDE',
  category VARCHAR(40) NOT NULL,
  description TEXT NOT NULL,
  likelihood NUMERIC(4,2) NOT NULL CHECK (likelihood >= 0 AND likelihood <= 1),
  impact NUMERIC(4,2) NOT NULL CHECK (impact >= 0 AND impact <= 1),
  risk_score NUMERIC(5,2) GENERATED ALWAYS AS (ROUND((likelihood * impact * 10)::numeric, 2)) STORED,
  status VARCHAR(20) NOT NULL DEFAULT 'open',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mitigations (
  id UUID PRIMARY KEY,
  scenario_id UUID NOT NULL REFERENCES threat_scenarios(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  action_plan TEXT NOT NULL,
  owner VARCHAR(120),
  due_date DATE,
  status VARCHAR(20) NOT NULL DEFAULT 'planned',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ml_runs (
  id UUID PRIMARY KEY,
  model_name VARCHAR(120) NOT NULL,
  model_version VARCHAR(40) NOT NULL,
  dataset_ref VARCHAR(255),
  precision_score NUMERIC(5,4),
  recall_score NUMERIC(5,4),
  f1_score NUMERIC(5,4),
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ml_predictions (
  id UUID PRIMARY KEY,
  scenario_id UUID NOT NULL REFERENCES threat_scenarios(id) ON DELETE CASCADE,
  run_id UUID NOT NULL REFERENCES ml_runs(id) ON DELETE CASCADE,
  predicted_label VARCHAR(40) NOT NULL,
  confidence NUMERIC(5,4) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_threat_scenarios_asset_id ON threat_scenarios(asset_id);
CREATE INDEX IF NOT EXISTS idx_threat_scenarios_status ON threat_scenarios(status);
CREATE INDEX IF NOT EXISTS idx_mitigations_scenario_id ON mitigations(scenario_id);
