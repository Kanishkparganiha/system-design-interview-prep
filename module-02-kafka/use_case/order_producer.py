"""
Order Producer
===============
Simulates an e-commerce API that publishes orders to Kafka.

This represents the entry point where orders are created and
published to the 'orders' topic for downstream processing.

Run: python order_producer.py
"""

import json
import time
import random
import uuid
from datetime import datetime
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


# Sample data for generating orders
PRODUCTS = [
    {"id": "LAPTOP-001", "name": "MacBook Pro", "price": 1999.00, "category": "Electronics"},
    {"id": "PHONE-001", "name": "iPhone 15", "price": 999.00, "category": "Electronics"},
    {"id": "HEADPHONES-001", "name": "AirPods Pro", "price": 249.00, "category": "Electronics"},
    {"id": "BOOK-001", "name": "Clean Code", "price": 45.00, "category": "Books"},
    {"id": "BOOK-002", "name": "System Design Interview", "price": 35.00, "category": "Books"},
    {"id": "SHIRT-001", "name": "Cotton T-Shirt", "price": 29.00, "category": "Clothing"},
    {"id": "SHOES-001", "name": "Running Shoes", "price": 120.00, "category": "Clothing"},
]

CUSTOMERS = [
    {"id": "CUST-001", "name": "Alice Johnson", "email": "alice@example.com", "tier": "premium"},
    {"id": "CUST-002", "name": "Bob Smith", "email": "bob@example.com", "tier": "standard"},
    {"id": "CUST-003", "name": "Carol Williams", "email": "carol@example.com", "tier": "premium"},
    {"id": "CUST-004", "name": "David Brown", "email": "david@example.com", "tier": "standard"},
    {"id": "CUST-005", "name": "Eve Davis", "email": "eve@example.com", "tier": "new"},
]

PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "apple_pay"]
SHIPPING_METHODS = ["standard", "express", "next_day"]


def create_topics():
    """Create required Kafka topics"""
    admin_client = KafkaAdminClient(
        bootstrap_servers=['localhost:9092'],
        client_id='order-admin'
    )

    topics = [
        NewTopic(name='orders', num_partitions=3, replication_factor=1),
        NewTopic(name='order-status', num_partitions=3, replication_factor=1),
        NewTopic(name='inventory-updates', num_partitions=3, replication_factor=1),
        NewTopic(name='notifications', num_partitions=3, replication_factor=1),
    ]

    for topic in topics:
        try:
            admin_client.create_topics([topic])
            print(f"✅ Created topic: {topic.name}")
        except TopicAlreadyExistsError:
            print(f"ℹ️  Topic already exists: {topic.name}")

    admin_client.close()


def create_producer() -> KafkaProducer:
    """Create a Kafka producer for orders"""
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
        acks='all',
        retries=3,
        compression_type='gzip',
    )


def generate_order() -> dict:
    """Generate a random order"""

    customer = random.choice(CUSTOMERS)
    num_items = random.randint(1, 4)
    items = random.sample(PRODUCTS, num_items)

    order_items = []
    subtotal = 0

    for product in items:
        quantity = random.randint(1, 3)
        item_total = product["price"] * quantity
        order_items.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "category": product["category"],
            "quantity": quantity,
            "unit_price": product["price"],
            "total": item_total
        })
        subtotal += item_total

    # Apply discount for premium customers
    discount = 0.1 if customer["tier"] == "premium" else 0
    discount_amount = subtotal * discount

    # Shipping costs
    shipping_method = random.choice(SHIPPING_METHODS)
    shipping_costs = {"standard": 5.99, "express": 12.99, "next_day": 24.99}
    shipping_cost = shipping_costs[shipping_method]

    # Calculate total
    total = subtotal - discount_amount + shipping_cost

    order = {
        "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
        "customer": customer,
        "items": order_items,
        "subtotal": round(subtotal, 2),
        "discount": round(discount_amount, 2),
        "shipping": {
            "method": shipping_method,
            "cost": shipping_cost,
            "address": {
                "street": f"{random.randint(100, 999)} Main St",
                "city": random.choice(["New York", "Los Angeles", "Chicago", "Houston"]),
                "state": random.choice(["NY", "CA", "IL", "TX"]),
                "zip": f"{random.randint(10000, 99999)}"
            }
        },
        "total": round(total, 2),
        "payment_method": random.choice(PAYMENT_METHODS),
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "metadata": {
            "source": random.choice(["web", "mobile_app", "api"]),
            "user_agent": "Mozilla/5.0",
            "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        }
    }

    return order


def run_producer(num_orders: int = 10, delay: float = 1.0):
    """Run the order producer"""

    print("=" * 60)
    print("ORDER PRODUCER")
    print("=" * 60)
    print()

    # Create topics if they don't exist
    print("Setting up topics...")
    try:
        create_topics()
    except Exception as e:
        print(f"Topic setup error (may be OK): {e}")

    print()

    # Create producer
    producer = create_producer()

    print(f"Producing {num_orders} orders with {delay}s delay between each...")
    print("-" * 60)

    total_revenue = 0
    orders_by_category = {}

    for i in range(num_orders):
        # Generate order
        order = generate_order()

        # Use customer ID as key for ordering guarantee
        # All orders from same customer go to same partition
        key = order["customer"]["id"]

        # Send to Kafka
        future = producer.send(
            topic='orders',
            key=key,
            value=order
        )

        try:
            metadata = future.get(timeout=10)
            print(f"\n📦 Order #{i+1}: {order['order_id']}")
            print(f"   Customer: {order['customer']['name']} ({order['customer']['tier']})")
            print(f"   Items: {len(order['items'])} items")
            print(f"   Total: ${order['total']:.2f}")
            print(f"   → Partition {metadata.partition}, Offset {metadata.offset}")

            # Track stats
            total_revenue += order['total']
            for item in order['items']:
                cat = item['category']
                orders_by_category[cat] = orders_by_category.get(cat, 0) + item['quantity']

        except Exception as e:
            print(f"❌ Failed to send order: {e}")

        if i < num_orders - 1:
            time.sleep(delay)

    producer.flush()
    producer.close()

    # Summary
    print("\n" + "=" * 60)
    print("PRODUCER SUMMARY")
    print("=" * 60)
    print(f"\nTotal orders sent: {num_orders}")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"\nItems by category:")
    for cat, count in sorted(orders_by_category.items()):
        print(f"  {cat}: {count} items")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Order Producer')
    parser.add_argument('--orders', '-n', type=int, default=10, help='Number of orders to produce')
    parser.add_argument('--delay', '-d', type=float, default=1.0, help='Delay between orders (seconds)')
    parser.add_argument('--continuous', '-c', action='store_true', help='Run continuously')

    args = parser.parse_args()

    if args.continuous:
        print("Running in continuous mode. Press Ctrl+C to stop.")
        try:
            while True:
                run_producer(num_orders=1, delay=0)
                time.sleep(args.delay)
        except KeyboardInterrupt:
            print("\n\nStopped by user")
    else:
        run_producer(num_orders=args.orders, delay=args.delay)


if __name__ == "__main__":
    main()
