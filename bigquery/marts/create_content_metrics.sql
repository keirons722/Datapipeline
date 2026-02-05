CREATE SCHEMA IF NOT EXISTS `marts`;

CREATE OR REPLACE TABLE `marts.daily_content_metrics` AS
WITH events AS (
  SELECT
    DATE(event_ts) AS event_date,
    user_id,
    content_id,
    content_type,
    event_type,
    duration_seconds,
    progress_percent,
    price_usd
  FROM `staging.book_media_events`
)
SELECT
  event_date,
  content_id,
  content_type,
  COUNT(DISTINCT user_id) AS daily_active_users,
  COUNTIF(event_type IN ('audio_played', 'video_played')) AS plays,
  SUM(CASE WHEN event_type = 'chapter_completed' THEN 1 ELSE 0 END) AS chapters_completed,
  AVG(progress_percent) AS avg_progress_percent,
  SUM(CASE WHEN event_type = 'purchase' THEN price_usd ELSE 0 END) AS revenue_usd,
  SUM(duration_seconds) AS total_play_seconds
FROM events
GROUP BY event_date, content_id, content_type;
