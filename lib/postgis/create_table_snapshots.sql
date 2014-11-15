CREATE TABLE ittc_snapshots
(
  id serial,
  source_repo text,
  source_workspace text,
  source_datastore text,
  source_layer text,
  snapshot_timestamp timestamp,
  snapshot_workspace text,
  snapshot_layergroup text,
  snapshot_layer text,
  geom geometry
);
