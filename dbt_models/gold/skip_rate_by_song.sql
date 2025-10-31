-- Estimate skip rate by song by tracking plays and skips
SELECT
    song_id,
    song_name,
    artist_name,
    COUNT(CASE WHEN event_type = 'play' THEN 1 END) AS total_plays,
    COUNT(CASE WHEN event_type = 'skip' THEN 1 END) AS total_skips,
    ROUND(
        COUNT(CASE WHEN event_type = 'skip' THEN 1 END) * 1.0 /
        NULLIF(COUNT(CASE WHEN event_type = 'play' THEN 1 END), 0),
        2
    ) AS skip_rate
FROM {{ ref('spotify_silver') }}
GROUP BY song_id, song_name, artist_name
ORDER BY skip_rate DESC
