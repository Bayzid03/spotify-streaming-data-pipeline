-- Estimate country-wise engagement by tracking plays, skips, and playlist adds
SELECT
    country,
    DATE_TRUNC('day', event_ts) AS day,
    COUNT(CASE WHEN event_type = 'play' THEN 1 END) AS plays,
    COUNT(CASE WHEN event_type = 'skip' THEN 1 END) AS skips,
    COUNT(CASE WHEN event_type = 'add_to_playlist' THEN 1 END) AS playlist_adds
FROM {{ ref('spotify_silver') }}
GROUP BY country, DATE_TRUNC('day', event_ts)
ORDER BY day, plays DESC
