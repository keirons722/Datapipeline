# Book Media Website Data Pipeline (BigQuery)

This repo provides a starter data pipeline for a website that supports reading books and consuming audio/video content. The goal is to land event data into BigQuery, then transform it into analytics-friendly tables for product, content, and revenue insights.

## Architecture overview

```
Client apps (web/mobile)
  -> Event collector (HTTP API)
  -> Pub/Sub (or Kafka)
  -> Cloud Storage (raw JSON landing)
  -> BigQuery raw tables
  -> BigQuery staging tables
  -> BigQuery marts (analytics-ready)
```

## Event model

The pipeline models the key actions for a reading/media product:

- `session_start` / `session_end`
- `book_opened` (opening an ebook)
- `page_turned` (page scroll/turn metrics)
- `audio_played` / `audio_paused`
- `video_played` / `video_paused`
- `chapter_completed`
- `purchase` (subscription or book purchase)

A JSON schema for the raw events is defined in `schemas/book_media_events.json`.

## BigQuery datasets and tables

- **raw**: append-only event storage.
- **staging**: cleaned/typed data (deduped, expanded fields).
- **marts**: business-level aggregates (daily active users, content completion rate, revenue).

SQL templates are located in `bigquery/`:

- `bigquery/raw/create_raw_events.sql`
- `bigquery/staging/create_stg_events.sql`
- `bigquery/marts/create_content_metrics.sql`

## Recommended ingestion flow

1. **Client instrumentation**: Send JSON events to your event collector endpoint.
2. **Streaming ingestion**: Publish events to Pub/Sub or Kafka.
3. **Raw landing**: Write batches to Cloud Storage as newline-delimited JSON.
4. **BigQuery load**: Use `bq load` or a Dataflow job to load into `raw.book_media_events`.
5. **Transform**: Run the staging and marts SQL on a schedule (Cloud Composer, dbt, or BigQuery scheduled queries).

## Near real-time options

To get close to real time, swap the batch load step with a streaming path that writes to BigQuery within seconds:

- **Collector -> Pub/Sub -> Dataflow -> BigQuery**: Dataflow streaming pipeline parses events, enforces schema, and writes to `raw.book_media_events` using the BigQuery Storage Write API.
- **Collector -> Pub/Sub -> BigQuery subscription**: For low transformation needs, use a direct BigQuery subscription from Pub/Sub to land JSON into the raw table (best for simpler schemas).
- **Collector -> Kafka -> Dataflow/Connect**: Use Kafka Connect (BigQuery sink) or Dataflow for streaming writes.

This keeps your `staging` and `marts` queries on schedules, while the raw data arrives continuously.

## Plugging in a real website

Yes, you can connect your real website domain. Typical steps:

1. **Instrument the site** with a lightweight tracking SDK that posts events to your collector API (e.g., `https://events.yourdomain.com/collect`).
2. **Validate payloads** at the collector (authentication, rate limits, schema checks).
3. **Stream events** into Pub/Sub or Kafka.
4. **Land in BigQuery** via Dataflow or a BigQuery subscription.

For local development, you can run the collector behind your domain using a reverse proxy (e.g., Cloud Load Balancer) and ensure CORS is configured for your website origin.

## Example usage

Generate sample events for testing and load them into BigQuery.

```
python scripts/generate_sample_events.py --output examples/sample_events.json
bq load --source_format=NEWLINE_DELIMITED_JSON \
  your_project:raw.book_media_events \
  examples/sample_events.json \
  schemas/book_media_events.json
```

## Next steps

- Add a transformation runner (dbt, Airflow/Composer) and wire it to the SQL templates.
- Enhance the schema with content metadata (author, genre, narration length).
- Integrate subscription billing events from your payments provider.
