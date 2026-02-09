"""
Kafka Producer Examples
========================
Various producer patterns and configurations using kafka-python.

Prerequisites:
    pip install kafka-python

Run Kafka first:
    cd real_kafka && docker-compose up -d

Run this script:
    python producer_example.py
"""

import json
import time
import random
from datetime import datetime
from typing import Optional, Dict, Any
from kafka import KafkaProducer
from kafka.errors import KafkaError


# =============================================================================
# BASIC PRODUCER
# =============================================================================

def create_basic_producer() -> KafkaProducer:
    """
    Create a basic Kafka producer with common settings.
    """
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],

        # Serialization
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),

        # Reliability settings
        acks='all',          # Wait for all replicas
        retries=3,           # Retry on failure
        retry_backoff_ms=100,

        # Performance settings
        batch_size=16384,        # 16KB batches
        linger_ms=10,            # Wait 10ms for batching
        buffer_memory=33554432,  # 32MB buffer

        # Compression
        compression_type='gzip',  # Options: 'gzip', 'snappy', 'lz4', 'zstd'
    )


def basic_producer_example():
    """Demonstrate basic producer usage"""

    print("=" * 60)
    print("BASIC PRODUCER EXAMPLE")
    print("=" * 60)
    print()

    producer = create_basic_producer()

    # Send a simple message
    message = {
        "event": "user_signup",
        "user_id": "user-123",
        "email": "john@example.com",
        "timestamp": datetime.now().isoformat()
    }

    # Synchronous send (blocking)
    print("Sending message synchronously...")
    future = producer.send(
        topic='user-events',
        key='user-123',
        value=message
    )

    try:
        # Block until message is sent (or timeout)
        record_metadata = future.get(timeout=10)
        print(f"✅ Message sent successfully!")
        print(f"   Topic: {record_metadata.topic}")
        print(f"   Partition: {record_metadata.partition}")
        print(f"   Offset: {record_metadata.offset}")
    except KafkaError as e:
        print(f"❌ Failed to send message: {e}")

    producer.close()


# =============================================================================
# ASYNC PRODUCER WITH CALLBACKS
# =============================================================================

def on_send_success(record_metadata):
    """Callback for successful sends"""
    print(f"✅ Sent to {record_metadata.topic}[{record_metadata.partition}] @ offset {record_metadata.offset}")


def on_send_error(excp):
    """Callback for failed sends"""
    print(f"❌ Error sending message: {excp}")


def async_producer_example():
    """Demonstrate asynchronous producer with callbacks"""

    print("\n" + "=" * 60)
    print("ASYNC PRODUCER WITH CALLBACKS")
    print("=" * 60)
    print()

    producer = create_basic_producer()

    # Send multiple messages asynchronously
    print("Sending 5 messages asynchronously...")

    for i in range(5):
        message = {
            "event": "page_view",
            "page": f"/product/{i}",
            "user_id": f"user-{random.randint(1, 100)}",
            "timestamp": datetime.now().isoformat()
        }

        producer.send(
            topic='page-views',
            key=str(i),
            value=message
        ).add_callback(on_send_success).add_errback(on_send_error)

    # Flush to ensure all messages are sent
    print("\nFlushing producer buffer...")
    producer.flush()

    print("\nAll messages sent!")
    producer.close()


# =============================================================================
# HIGH-THROUGHPUT PRODUCER
# =============================================================================

def high_throughput_producer_example():
    """
    Producer optimized for high throughput.
    Trades latency for throughput.
    """

    print("\n" + "=" * 60)
    print("HIGH-THROUGHPUT PRODUCER")
    print("=" * 60)
    print()

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),

        # High throughput settings
        acks=1,                   # Only wait for leader (faster)
        batch_size=65536,         # 64KB batches (larger batches)
        linger_ms=50,             # Wait 50ms for batching
        buffer_memory=67108864,   # 64MB buffer
        compression_type='lz4',   # Fast compression
        max_in_flight_requests_per_connection=5,
    )

    # Send 10,000 messages
    num_messages = 10000
    start_time = time.time()

    print(f"Sending {num_messages:,} messages...")

    for i in range(num_messages):
        producer.send(
            topic='high-volume-topic',
            key=f"key-{i % 100}",
            value={"id": i, "data": "x" * 100}  # ~100 bytes each
        )

    producer.flush()
    elapsed = time.time() - start_time

    print(f"\n✅ Sent {num_messages:,} messages in {elapsed:.2f} seconds")
    print(f"   Throughput: {num_messages/elapsed:,.0f} messages/second")

    producer.close()


# =============================================================================
# IDEMPOTENT PRODUCER (Exactly-Once Semantics)
# =============================================================================

def idempotent_producer_example():
    """
    Idempotent producer ensures exactly-once delivery.
    Prevents duplicates even with retries.
    """

    print("\n" + "=" * 60)
    print("IDEMPOTENT PRODUCER (Exactly-Once)")
    print("=" * 60)
    print()

    print("""
    Idempotent Producer Guarantees:
    ───────────────────────────────
    • No duplicate messages on retry
    • Messages are delivered exactly once
    • Order is preserved even with retries

    How it works:
    ─────────────
    1. Producer gets a unique ID (PID) from broker
    2. Each message gets a sequence number
    3. Broker deduplicates using (PID, sequence)
    """)

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),

        # Enable idempotence
        enable_idempotence=True,  # This is the key setting!

        # These are automatically set with idempotence:
        # acks='all'
        # retries=MAX_INT
        # max_in_flight_requests_per_connection=5
    )

    # Send messages - even if we retry, no duplicates!
    for i in range(5):
        message = {"transaction_id": f"txn-{i}", "amount": 100 + i}
        producer.send(
            topic='transactions',
            key=f"txn-{i}",
            value=message
        ).add_callback(on_send_success)

    producer.flush()
    producer.close()

    print("\nMessages sent with exactly-once guarantee!")


# =============================================================================
# TRANSACTIONAL PRODUCER
# =============================================================================

def transactional_producer_example():
    """
    Transactional producer for atomic writes across multiple topics/partitions.
    """

    print("\n" + "=" * 60)
    print("TRANSACTIONAL PRODUCER")
    print("=" * 60)
    print()

    print("""
    Transactional Producer Use Case:
    ────────────────────────────────
    Write to multiple topics atomically.
    Either ALL messages are committed, or NONE.

    Example: Order processing
    - Write to 'orders' topic
    - Write to 'inventory' topic
    - Write to 'notifications' topic
    All or nothing!
    """)

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),

        # Transactional settings
        transactional_id='order-processor-1',  # Unique ID for this producer
        enable_idempotence=True,  # Required for transactions
    )

    # Initialize transactions (required before any transactional operations)
    producer.init_transactions()

    try:
        # Start a transaction
        producer.begin_transaction()

        order = {"order_id": "ORD-123", "items": ["laptop", "mouse"]}

        # Send to multiple topics atomically
        producer.send('orders', key='ORD-123', value=order)
        producer.send('inventory-updates', key='ORD-123', value={"action": "reserve", "order": order})
        producer.send('notifications', key='ORD-123', value={"type": "order_created", "order_id": "ORD-123"})

        # Commit the transaction
        producer.commit_transaction()
        print("✅ Transaction committed successfully!")

    except Exception as e:
        # Abort on any error
        producer.abort_transaction()
        print(f"❌ Transaction aborted: {e}")

    finally:
        producer.close()


# =============================================================================
# PARTITIONER EXAMPLES
# =============================================================================

def custom_partitioner_example():
    """
    Demonstrate custom partitioning logic.
    """

    print("\n" + "=" * 60)
    print("CUSTOM PARTITIONER")
    print("=" * 60)
    print()

    def priority_partitioner(key, all_partitions, available_partitions):
        """
        Custom partitioner that routes messages based on priority.
        - Keys starting with 'HIGH:' go to partition 0
        - Keys starting with 'LOW:' go to last partition
        - Others use default hash partitioning
        """
        if key is None:
            return random.choice(available_partitions)

        key_str = key.decode('utf-8') if isinstance(key, bytes) else key

        if key_str.startswith('HIGH:'):
            return available_partitions[0]
        elif key_str.startswith('LOW:'):
            return available_partitions[-1]
        else:
            # Default hash partitioning
            return hash(key_str) % len(available_partitions)

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        partitioner=priority_partitioner
    )

    messages = [
        ('HIGH:alert-1', {'type': 'critical', 'message': 'Server down!'}),
        ('NORMAL:event-1', {'type': 'info', 'message': 'User logged in'}),
        ('LOW:log-1', {'type': 'debug', 'message': 'Cache hit'}),
        ('HIGH:alert-2', {'type': 'critical', 'message': 'Database error!'}),
    ]

    print("Sending messages with custom partitioner:")
    print("-" * 40)

    for key, value in messages:
        future = producer.send('priority-queue', key=key, value=value)
        metadata = future.get(timeout=10)
        print(f"  {key:20} → Partition {metadata.partition}")

    producer.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run all producer examples"""

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           KAFKA PRODUCER EXAMPLES                         ║
    ╠═══════════════════════════════════════════════════════════╣
    ║  Make sure Kafka is running:                              ║
    ║  cd real_kafka && docker-compose up -d                    ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    try:
        basic_producer_example()
        async_producer_example()
        high_throughput_producer_example()
        idempotent_producer_example()

        # Note: Transactional producer requires proper topic setup
        # Uncomment to test:
        # transactional_producer_example()

        custom_partitioner_example()

        print("\n" + "=" * 60)
        print("ALL EXAMPLES COMPLETED!")
        print("=" * 60)
        print("\nCheck the messages in Kafka UI: http://localhost:8080")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Kafka is running:")
        print("  cd real_kafka && docker-compose up -d")


if __name__ == "__main__":
    main()
