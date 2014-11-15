INSERT INTO {{table}}
(
  source_name,
  source_layers,
  snapshot_timestamp,
  snapshot_layergroup,
  geom
)
VALUES
(
  {{source-name}},
  {{source-layers}},
  {{snapshot-timestamp}},
  {{snapshot-layergroup}},
  ST_MakeEnvelope({{xmin}}, {{ymin}}, {{xmax}}, {{ymax}}, {{srid}})
);
