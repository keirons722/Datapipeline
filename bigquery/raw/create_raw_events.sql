CREATE SCHEMA IF NOT EXISTS `raw`;

CREATE TABLE IF NOT EXISTS `raw.book_media_events` (
  event_id STRING NOT NULL,
  event_type STRING NOT NULL,
  event_ts TIMESTAMP NOT NULL,
  user_id STRING NOT NULL,
  session_id STRING NOT NULL,
  content_id STRING,
  content_type STRING,
  chapter_id STRING,
  device_type STRING,
  app_version STRING,
  country STRING,
  duration_seconds FLOAT64,
  progress_percent FLOAT64,
  price_usd FLOAT64,
  currency STRING,
  metadata JSON
)
PARTITION BY DATE(event_ts)
CLUSTER BY event_type, user_id;
