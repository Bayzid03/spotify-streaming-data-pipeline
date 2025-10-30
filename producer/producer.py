import os
import json
import time
import uuid
import random
from faker import Faker
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv

# --------------------------------------------
# Load environment variables
# --------------------------------------------
load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS") # Kafka bootstrap servers
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "spotify-events") # Kafka topic
USER_COUNT = int(os.getenv("USER_COUNT", 20)) # Number of users
EVENT_INTERVAL_SECONDS = int(os.getenv("EVENT_INTERVAL_SECONDS", 1)) # Event interval in seconds

fake = Faker()

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda v: json.dumps(v).encode("utf-8") # convert value to JSON string
)

# --------------------------------------------
# Stable Song/Artist Definitions
# --------------------------------------------
song_artist_pairs = [
    {"artist": "The Weeknd", "song": "Blinding Lights"},
    {"artist": "Dua Lipa", "song": "Levitating"},
    {"artist": "Drake", "song": "God's Plan"},
    {"artist": "Taylor Swift", "song": "Love Story"},
    {"artist": "Ed Sheeran", "song": "Shape of You"},
    {"artist": "Kanye West", "song": "Stronger"}
]

for pair in song_artist_pairs:
    name_for_uuid = f"{pair['artist']}::{pair['song']}"
    pair["song_id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS, name_for_uuid))

devices = ["mobile", "desktop", "web"]
countries = ["US", "UK", "CA", "AU", "IN", "DE"]
event_types = ["play", "pause", "skip", "add_to_playlist"]

# Generate random users
user_ids = [str(uuid.uuid4()) for _ in range(USER_COUNT)]

def generate_event():
    pair = random.choice(song_artist_pairs)
    user_id = random.choice(user_ids)
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "song_id": pair["song_id"],
        "artist_name": pair["artist"],
        "song_name": pair["song"],
        "event_type": random.choice(event_types),
        "device_type": random.choice(devices),
        "country": random.choice(countries),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

if __name__ == "__main__":
    print("🎧 Starting Spotify data simulator...")
    print(f"Using {len(song_artist_pairs)} songs and {len(user_ids)} users.")
    for p in song_artist_pairs:
        print(f"{p['song']} — {p['artist']} -> song_id={p['song_id']}")

    while True:
        event = generate_event()
        producer.send(KAFKA_TOPIC, event) # Send event to Kafka
        print(f"Produced event: {event['event_type']} - {event['song_name']} by {event['artist_name']} (user {event['user_id']})")
        time.sleep(EVENT_INTERVAL_SECONDS) # Wait for next event
