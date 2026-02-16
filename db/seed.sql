INSERT INTO assets (id, name, asset_type, business_criticality, owner, tags)
VALUES
  ('00000000-0000-0000-0000-000000000001', 'Payment API', 'service', 'high', 'platform-team', '["pci", "internet-facing"]'::jsonb),
  ('00000000-0000-0000-0000-000000000002', 'Customer DB', 'database', 'critical', 'data-team', '["pii", "encrypted"]'::jsonb)
ON CONFLICT DO NOTHING;

INSERT INTO threat_scenarios (id, asset_id, framework, category, description, likelihood, impact, status)
VALUES
  ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'STRIDE', 'Tampering', 'Request payload tampering in payment flow', 0.70, 0.80, 'open'),
  ('10000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-000000000002', 'STRIDE', 'Information Disclosure', 'Potential data exfiltration from backup channel', 0.50, 0.90, 'in_progress')
ON CONFLICT DO NOTHING;
