CREATE TABLE {{table}}
(
  id serial,
  source_layers text,
  snapshot_timestamp timestamp,
  snapshot_layergroup text,
  geom geometry
);
