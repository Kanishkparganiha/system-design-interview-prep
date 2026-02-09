"""
Kafka Consumer Examples
========================
Various consumer patterns and configurations using kafka-python.

Prerequisites:
    pip install kafka-python

Run Kafka first:
    cd real_kafka && docker-compose up -d

Run the producer first to create some messages:
    python producer_example.py

Then run this script:
    python consumer_example.py
"""

import json
import time
import signal
import sys
from typing import Optional, List, Dict
from datetime import datetime
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError


# Global flag for graceful shutdown
running = True


def signal_handler(signum, frame):
    """Handle Ctrl+C for graceful shutdown"""
    global running
    print("\n\n⚠️  Shutting down gracefully...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


# =============================================================================
# BASIC CONSUMER
# =============================================================================

def create_basic_consumer(group_id: str, topics: List[str]) -> KafkaConsumer:
    """
    Create a basic Kafka consumer with common settings.
    """
    return KafkaConsumer(
        *topics,
        bootstrap_servers=['localhost:9092'],
        group_id=group_id,

        # Deserialization
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),

        # Offset management
        auto_offset_reset='earliest',  # Start from beginning if no offset
        enable_auto_commit=True,       # Auto-commit offsets
        auto_commit_interval_ms=5000,  # Commit every 5 seconds

        # Consumer settings
        max_poll_records=500,          # Max records per poll
        max_poll_interval_ms=300000,   # Max time between polls
        session_timeout_ms=10000,      # Session timeout

        # Fetch settings
        fetch_min_bytes=1,             # Minimum data to fetch
        fetch_max_wait_ms=500,         # Max wait time for fetch
    )


def basic_consumer_example():
    """Demonstrate basic consumer usage"""

    print("=" * 60)
    print("BASIC CONSUMER EXAMPLE")
    print("=" * 60)
    print()
    print("Press Ctrl+C to stop")
    print("-" * 40)

    consumer = create_basic_consumer(
        group_id='basic-consumer-group',
        topics=['user-events', 'page-views']
    )

    global running
    message_count = 0

    try:
        while running:
            # Poll for messages (timeout in ms)
            messages = consumer.poll(timeout_ms=1000)

            for topic_partition, records in messages.items():
                for record in records:
                    message_count += 1
                    print(f"\n📨 Message #{message_count}")
                    print(f"   Topic: {record.topic}")
                    print(f"   Partition: {record.partition}")
                    print(f"   Offset: {record.offset}")
                    print(f"   Key: {record.key}")
                    print(f"   Value: {record.value}")
                    print(f"   Timestamp: {datetime.fromtimestamp(record.timestamp/1000)}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        consumer.close()
        print(f"\n✅ Consumed {message_count} messages")


# =============================================================================
# MANUAL COMMIT CONSUMER
# =============================================================================

def manual_commit_consumer_example():
    """
    Consumer with manual offset commits.
    Provides more control over exactly-once processing.
    """

    print("\n" + "=" * 60)
    print("MANUAL COMMIT CONSUMER")
    print("=" * 60)
    print()

    print("""
    Why Manual Commit?
    ──────────────────
    • Auto-commit may commit before processing completes
    • If consumer crashes after commit but before processing → lost message
    • Manual commit ensures we only commit AFTER successful processing
    """)

    consumer = KafkaConsumer(
        'user-events',
        bootstrap_servers=['localhost:9092'],
        group_id='manual-commit-group',
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=False,  # Disable auto-commit!
    )

    global running
    message_count = 0

    print("\nPress Ctrl+C to stop")
    print("-" * 40)

    try:
        while running and message_count < 10:  # Process 10 messages for demo
            messages = consumer.poll(timeout_ms=1000)

            for topic_partition, records in messages.items():
                for record in records:
                    # Process the message
                    message_count += 1
                    print(f"\n📨 Processing message at offset {record.offset}")
                    print(f"   Value: {record.value}")

                    # Simulate processing
                    process_message(record)

                    # Commit offset AFTER successful processing
                    consumer.commit()
                    print(f"   ✅ Offset {record.offset} committed")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        consumer.close()
        print(f"\n✅ Processed and committed {message_count} messages")


def process_message(record):
    """Simulate message processing"""
    time.sleep(0.1)  # Simulate work


# =============================================================================
# BATCH COMMIT CONSUMER
# =============================================================================

def batch_commit_consumer_example():
    """
    Consumer that commits offsets in batches for better performance.
    """

    print("\n" + "=" * 60)
    print("BATCH COMMIT CONSUMER")
    print("=" * 60)
    print()

    consumer = KafkaConsumer(
        'high-volume-topic',
        bootstrap_servers=['localhost:9092'],
        group_id='batch-commit-group',
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        max_poll_records=100,  # Get more records per poll
    )

    BATCH_SIZE = 50
    global running
    batch = []
    total_processed = 0

    print(f"Processing in batches of {BATCH_SIZE}")
    print("Press Ctrl+C to stop")
    print("-" * 40)

    try:
        while running and total_processed < 200:
            messages = consumer.poll(timeout_ms=1000)

            for topic_partition, records in messages.items():
                for record in records:
                    batch.append(record)

                    if len(batch) >= BATCH_SIZE:
                        # Process batch
                        process_batch(batch)

                        # Commit after batch
                        consumer.commit()
                        total_processed += len(batch)
                        print(f"✅ Committed batch of {len(batch)} (total: {total_processed})")
                        batch = []

        # Process remaining messages
        if batch:
            process_batch(batch)
            consumer.commit()
            total_processed += len(batch)
            print(f"✅ Committed final batch of {len(batch)} (total: {total_processed})")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        consumer.close()
        print(f"\n✅ Processed {total_processed} messages in batches")


def process_batch(batch):
    """Process a batch of messages"""
    # In real scenario: bulk insert to database, etc.
    time.sleep(0.1)


# =============================================================================
# SEEK AND REPLAY CONSUMER
# =============================================================================

def seek_and_replay_example():
    """
    Demonstrate seeking to specific offsets for replay.
    """

    print("\n" + "=" * 60)
    print("SEEK AND REPLAY CONSUMER")
    print("=" * 60)
    print()

    print("""
    Use Cases for Seeking:
    ──────────────────────
    • Replay messages after bug fix
    • Skip problematic messages
    • Start from specific point in time
    • Reset consumer to beginning
    """)

    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        group_id='seek-demo-group',
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=False,
    )

    # Manually assign partitions
    topic = 'user-events'
    partitions = consumer.partitions_for_topic(topic)

    if not partitions:
        print(f"Topic '{topic}' not found or has no partitions")
        consumer.close()
        return

    # Assign all partitions
    topic_partitions = [TopicPartition(topic, p) for p in partitions]
    consumer.assign(topic_partitions)

    print(f"\nAssigned partitions: {partitions}")

    # Seek to beginning
    print("\n📍 Seeking to BEGINNING...")
    consumer.seek_to_beginning()

    # Read first 3 messages
    count = 0
    for message in consumer:
        print(f"   Offset {message.offset}: {message.value}")
        count += 1
        if count >= 3:
            break

    # Seek to end
    print("\n📍 Seeking to END...")
    consumer.seek_to_end()

    # Get current positions
    for tp in topic_partitions:
        position = consumer.position(tp)
        print(f"   Partition {tp.partition} position: {position}")

    # Seek to specific offset
    print("\n📍 Seeking to offset 0 on partition 0...")
    consumer.seek(TopicPartition(topic, 0), 0)

    # Read next message
    message = next(consumer)
    print(f"   Message at offset 0: {message.value}")

    consumer.close()


# =============================================================================
# MULTI-THREADED CONSUMER (one consumer per partition)
# =============================================================================

def partition_assignment_example():
    """
    Show how to manually assign partitions for more control.
    """

    print("\n" + "=" * 60)
    print("MANUAL PARTITION ASSIGNMENT")
    print("=" * 60)
    print()

    print("""
    Subscribe vs Assign:
    ────────────────────
    subscribe(): Automatic partition assignment with rebalancing
    assign():    Manual partition assignment, no rebalancing

    Use assign() when:
    • You need deterministic partition assignment
    • You want to process specific partitions
    • You're implementing your own partition management
    """)

    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        group_id=None,  # No group = no coordination
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
    )

    # Only consume from partition 0
    topic = 'user-events'
    partition = TopicPartition(topic, 0)
    consumer.assign([partition])

    print(f"\nManually assigned to {topic} partition 0")
    print("Reading first 5 messages...")
    print("-" * 40)

    count = 0
    for message in consumer:
        print(f"   P{message.partition} offset {message.offset}: {message.key}")
        count += 1
        if count >= 5:
            break

    consumer.close()


# =============================================================================
# CONSUMER LAG MONITORING
# =============================================================================

def consumer_lag_example():
    """
    Demonstrate how to monitor consumer lag.
    """

    print("\n" + "=" * 60)
    print("CONSUMER LAG MONITORING")
    print("=" * 60)
    print()

    print("""
    Consumer Lag = Latest Offset - Current Consumer Offset

    High lag indicates:
    • Consumer can't keep up with producers
    • Consumer was down and needs to catch up
    • Processing is too slow

    Monitoring lag is CRITICAL for production systems!
    """)

    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        group_id='lag-monitor-group',
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    )

    topic = 'high-volume-topic'
    consumer.subscribe([topic])

    # Force assignment
    consumer.poll(timeout_ms=1000)

    # Get assigned partitions
    assignment = consumer.assignment()

    if not assignment:
        print(f"No partitions assigned for topic '{topic}'")
        consumer.close()
        return

    print(f"\nAssigned partitions: {[tp.partition for tp in assignment]}")
    print("\nCalculating lag...")
    print("-" * 40)

    # Get end offsets (latest)
    end_offsets = consumer.end_offsets(assignment)

    # Get committed offsets
    total_lag = 0
    for tp in assignment:
        committed = consumer.committed(tp) or 0
        latest = end_offsets[tp]
        lag = latest - committed

        print(f"   Partition {tp.partition}:")
        print(f"      Committed offset: {committed}")
        print(f"      Latest offset:    {latest}")
        print(f"      Lag:              {lag}")

        total_lag += lag

    print(f"\n📊 Total lag across all partitions: {total_lag}")

    consumer.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run consumer examples"""

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           KAFKA CONSUMER EXAMPLES                         ║
    ╠═══════════════════════════════════════════════════════════╣
    ║  Make sure Kafka is running and has messages:             ║
    ║  1. cd real_kafka && docker-compose up -d                 ║
    ║  2. python producer_example.py                            ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    examples = [
        ("1", "Basic Consumer", basic_consumer_example),
        ("2", "Manual Commit Consumer", manual_commit_consumer_example),
        ("3", "Batch Commit Consumer", batch_commit_consumer_example),
        ("4", "Seek and Replay", seek_and_replay_example),
        ("5", "Manual Partition Assignment", partition_assignment_example),
        ("6", "Consumer Lag Monitoring", consumer_lag_example),
    ]

    print("\nAvailable examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    print("  a. Run all examples")
    print("  q. Quit")

    choice = input("\nSelect an example (1-6, a, or q): ").strip().lower()

    if choice == 'q':
        return

    if choice == 'a':
        for _, name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"Error in {name}: {e}")
    else:
        for num, name, func in examples:
            if choice == num:
                try:
                    func()
                except Exception as e:
                    print(f"Error: {e}")
                break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
