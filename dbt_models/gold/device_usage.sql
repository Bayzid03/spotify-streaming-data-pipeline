-- Estimate device usage by tracking plays, skips, and playlist adds
SELECT
    device_type,
    COUNT(*) AS total_events,
    COUNT(DISTINCT user_id) AS unique_users,
    ROUND(COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (), 2) AS device_event_pct
FROM {{ ref('spotify_silver') }}
GROUP BY device_type
ORDER BY total_events DESC
