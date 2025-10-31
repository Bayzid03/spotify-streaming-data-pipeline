import json
import os
from kafka import KafkaConsumer
from datetime import datetime
import boto3
from dotenv import load_dotenv

# ---------- Load environment variables ----------
load_dotenv()

# ---------- Configuration ----------
MINIO_BUCKET = os.getenv("MINIO_BUCKET")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10)) 

# ---------- Connect to MinIO ----------
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

# Ensure bucket exists (idempotent)
try:
    s3.head_bucket(Bucket=MINIO_BUCKET)
    print(f"Bucket {MINIO_BUCKET} already exists.")
except Exception:
    s3.create_bucket(Bucket=MINIO_BUCKET)
    print(f"Created bucket {MINIO_BUCKET}.")

# ---------- Kafka Consumer Setup ----------
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=KAFKA_GROUP_ID,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print(f"🎧 Listening for events on Kafka topic '{KAFKA_TOPIC}'...")

batch = []

# ---------- Consume and Process Events ----------
for message in consumer:
    event = message.value
    batch.append(event)

    if len(batch) >= BATCH_SIZE: # Upload batch to MinIO
        now = datetime.utcnow()
        date_path = now.strftime("date=%Y-%m-%d/hour=%H")
        file_name = f"spotify_events_{now.strftime('%Y-%m-%dT%H-%M-%S')}.json"
        file_path = f"bronze/{date_path}/{file_name}"

        json_data = "\n".join([json.dumps(e) for e in batch]) # Convert batch to JSON string

        s3.put_object( # Upload batch to MinIO
            Bucket=MINIO_BUCKET,
            Key=file_path,
            Body=json_data.encode("utf-8")
        )

        print(f"✅ Uploaded {len(batch)} events to MinIO: {file_path}") # Print success message
        batch = []

