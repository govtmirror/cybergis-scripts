INSERT INTO ittc_snapshot_layers
(
  source_repo,
  source_workspace,
  source_datastore,
  source_layer,
  snapshot_timestamp,
  snapshot_layer,
  geom
)
VALUES
(
  {{source-repo}},
  {{source-workspace}},
  {{source-datstore}},
  {{source-layer}},
  {{snapshot-timestamp}},
  {{snapshot-layer}},
  ST_MakeEnvelope({{xmin}}, {{ymin}}, {{xmax}}, {{ymax}}, {{srid}})
);
