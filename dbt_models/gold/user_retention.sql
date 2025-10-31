-- Estimate user retention by tracking how many days user returns
SELECT
    user_id,
    COUNT(DISTINCT DATE_TRUNC('day', event_ts)) AS active_days,
    MIN(DATE(event_ts)) AS first_seen,
    MAX(DATE(event_ts)) AS last_seen
FROM {{ ref('spotify_silver') }}
GROUP BY user_id
ORDER BY active_days DESC
