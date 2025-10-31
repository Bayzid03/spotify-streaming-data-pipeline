-- Estimate daily active users by tracking unique users per day
SELECT
    DATE_TRUNC('day', event_ts) AS day,
    COUNT(DISTINCT user_id) AS daily_active_users
FROM {{ ref('spotify_silver') }}
GROUP BY day
ORDER BY day
