CREATE SCHEMA IF NOT EXISTS `staging`;

CREATE OR REPLACE TABLE `staging.book_media_events` AS
SELECT
  event_id,
  event_type,
  event_ts,
  user_id,
  session_id,
  content_id,
  content_type,
  chapter_id,
  device_type,
  app_version,
  country,
  duration_seconds,
  progress_percent,
  price_usd,
  currency,
  SAFE_CAST(JSON_VALUE(metadata, '$.playback_speed') AS FLOAT64) AS playback_speed,
  JSON_VALUE(metadata, '$.referrer') AS referrer,
  JSON_VALUE(metadata, '$.device_os') AS device_os
FROM `raw.book_media_events`
WHERE event_id IS NOT NULL;
