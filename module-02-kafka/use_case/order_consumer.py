"""
Order Processing Consumer
==========================
Consumes orders from the 'orders' topic, validates them,
and publishes status updates.

This simulates the core order processing service.

Run: python order_consumer.py
"""

import json
import time
import random
import signal
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError


# Graceful shutdown
running = True


def signal_handler(signum, frame):
    global running
    print("\n\n⚠️  Shutting down gracefully...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


def create_consumer() -> KafkaConsumer:
    """Create consumer for orders topic"""
    return KafkaConsumer(
        'orders',
        bootstrap_servers=['localhost:9092'],
        group_id='order-processing-service',
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=False,  # Manual commit for safety
        max_poll_records=10,
    )


def create_producer() -> KafkaProducer:
    """Create producer for status updates"""
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
        acks='all',
    )


def validate_order(order: dict) -> tuple[bool, str]:
    """
    Validate an order.
    Returns (is_valid, reason)
    """
    # Check required fields
    required_fields = ['order_id', 'customer', 'items', 'total']
    for field in required_fields:
        if field not in order:
            return False, f"Missing required field: {field}"

    # Check items
    if not order['items'] or len(order['items']) == 0:
        return False, "Order must have at least one item"

    # Check total
    if order['total'] <= 0:
        return False, "Order total must be positive"

    # Simulate random validation failures (10% chance)
    if random.random() < 0.1:
        reasons = [
            "Payment verification failed",
            "Customer account on hold",
            "Suspicious activity detected"
        ]
        return False, random.choice(reasons)

    return True, "Order validated successfully"


def process_order(order: dict) -> dict:
    """
    Process a validated order.
    Simulates order processing steps.
    """
    steps = [
        "Checking inventory",
        "Reserving items",
        "Processing payment",
        "Generating shipping label",
        "Finalizing order"
    ]

    for step in steps:
        # Simulate processing time
        time.sleep(random.uniform(0.1, 0.3))

    return {
        "order_id": order['order_id'],
        "status": "confirmed",
        "confirmation_number": f"CONF-{order['order_id'][-8:]}",
        "estimated_delivery": "3-5 business days",
        "processed_at": datetime.now().isoformat()
    }


def publish_status_update(producer: KafkaProducer, order_id: str,
                          status: str, details: dict):
    """Publish order status update to order-status topic"""
    status_event = {
        "order_id": order_id,
        "status": status,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }

    producer.send(
        topic='order-status',
        key=order_id,
        value=status_event
    )


def publish_notification(producer: KafkaProducer, order: dict, status: str, message: str):
    """Publish notification event"""
    notification = {
        "type": f"order_{status}",
        "order_id": order['order_id'],
        "customer_email": order['customer']['email'],
        "customer_name": order['customer']['name'],
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

    producer.send(
        topic='notifications',
        key=order['customer']['id'],
        value=notification
    )


def run_consumer():
    """Run the order processing consumer"""

    print("=" * 60)
    print("ORDER PROCESSING SERVICE")
    print("=" * 60)
    print()
    print("Consumer Group: order-processing-service")
    print("Subscribed to: orders")
    print("Publishing to: order-status, notifications")
    print()
    print("Press Ctrl+C to stop")
    print("-" * 60)

    consumer = create_consumer()
    producer = create_producer()

    global running
    processed = 0
    validated = 0
    rejected = 0

    try:
        while running:
            messages = consumer.poll(timeout_ms=1000)

            for topic_partition, records in messages.items():
                for record in records:
                    order = record.value
                    order_id = order['order_id']

                    print(f"\n📥 Received: {order_id}")
                    print(f"   Customer: {order['customer']['name']}")
                    print(f"   Total: ${order['total']:.2f}")

                    # Update status to "processing"
                    publish_status_update(
                        producer, order_id, "processing",
                        {"message": "Order received and being processed"}
                    )

                    # Validate order
                    is_valid, reason = validate_order(order)

                    if is_valid:
                        validated += 1

                        # Process the order
                        result = process_order(order)

                        # Update status to "confirmed"
                        publish_status_update(
                            producer, order_id, "confirmed",
                            result
                        )

                        # Send notification
                        publish_notification(
                            producer, order, "confirmed",
                            f"Your order {order_id} has been confirmed! "
                            f"Confirmation: {result['confirmation_number']}"
                        )

                        print(f"   ✅ Confirmed: {result['confirmation_number']}")

                    else:
                        rejected += 1

                        # Update status to "rejected"
                        publish_status_update(
                            producer, order_id, "rejected",
                            {"reason": reason}
                        )

                        # Send rejection notification
                        publish_notification(
                            producer, order, "rejected",
                            f"Your order {order_id} could not be processed: {reason}"
                        )

                        print(f"   ❌ Rejected: {reason}")

                    processed += 1

                    # Commit after processing
                    consumer.commit()

            producer.flush()

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        consumer.close()
        producer.close()

        print("\n" + "=" * 60)
        print("CONSUMER SUMMARY")
        print("=" * 60)
        print(f"\nTotal processed: {processed}")
        print(f"Validated: {validated}")
        print(f"Rejected: {rejected}")
        print(f"Success rate: {validated/processed*100:.1f}%" if processed > 0 else "N/A")


if __name__ == "__main__":
    run_consumer()
