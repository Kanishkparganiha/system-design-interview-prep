"""
Inventory Consumer
===================
Consumes orders and manages inventory levels.

This demonstrates a separate consumer group processing
the same order events for a different purpose.

Run: python inventory_consumer.py
"""

import json
import signal
from datetime import datetime
from collections import defaultdict
from kafka import KafkaConsumer, KafkaProducer


# Graceful shutdown
running = True


def signal_handler(signum, frame):
    global running
    print("\n\n⚠️  Shutting down gracefully...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


class InventoryManager:
    """
    Simulates an inventory management system.
    In production, this would be backed by a database.
    """

    def __init__(self):
        # Initialize with some stock
        self.inventory = {
            "LAPTOP-001": {"name": "MacBook Pro", "stock": 50, "reserved": 0},
            "PHONE-001": {"name": "iPhone 15", "stock": 100, "reserved": 0},
            "HEADPHONES-001": {"name": "AirPods Pro", "stock": 200, "reserved": 0},
            "BOOK-001": {"name": "Clean Code", "stock": 500, "reserved": 0},
            "BOOK-002": {"name": "System Design Interview", "stock": 300, "reserved": 0},
            "SHIRT-001": {"name": "Cotton T-Shirt", "stock": 1000, "reserved": 0},
            "SHOES-001": {"name": "Running Shoes", "stock": 150, "reserved": 0},
        }
        self.low_stock_threshold = 10

    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Check if requested quantity is available"""
        if product_id not in self.inventory:
            return False
        item = self.inventory[product_id]
        available = item['stock'] - item['reserved']
        return available >= quantity

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """Reserve stock for an order"""
        if not self.check_availability(product_id, quantity):
            return False
        self.inventory[product_id]['reserved'] += quantity
        return True

    def commit_reservation(self, product_id: str, quantity: int):
        """Convert reservation to actual stock reduction (order confirmed)"""
        if product_id in self.inventory:
            self.inventory[product_id]['stock'] -= quantity
            self.inventory[product_id]['reserved'] -= quantity

    def release_reservation(self, product_id: str, quantity: int):
        """Release reserved stock (order cancelled)"""
        if product_id in self.inventory:
            self.inventory[product_id]['reserved'] -= quantity

    def get_available(self, product_id: str) -> int:
        """Get available (unreserved) stock"""
        if product_id not in self.inventory:
            return 0
        item = self.inventory[product_id]
        return item['stock'] - item['reserved']

    def check_low_stock(self) -> list:
        """Return list of products with low stock"""
        low_stock = []
        for product_id, item in self.inventory.items():
            available = item['stock'] - item['reserved']
            if available <= self.low_stock_threshold:
                low_stock.append({
                    "product_id": product_id,
                    "name": item['name'],
                    "available": available,
                    "total_stock": item['stock'],
                    "reserved": item['reserved']
                })
        return low_stock

    def display_status(self):
        """Display current inventory status"""
        print("\n┌" + "─" * 58 + "┐")
        print("│" + " INVENTORY STATUS".center(58) + "│")
        print("├" + "─" * 58 + "┤")
        print("│" + f"{'Product':<25} {'Stock':>8} {'Reserved':>10} {'Available':>10}" + " │")
        print("├" + "─" * 58 + "┤")

        for product_id, item in self.inventory.items():
            available = item['stock'] - item['reserved']
            status = "⚠️" if available <= self.low_stock_threshold else "  "
            print(f"│ {item['name']:<23} {item['stock']:>8} {item['reserved']:>10} {available:>8} {status}│")

        print("└" + "─" * 58 + "┘")


def create_consumer() -> KafkaConsumer:
    """Create consumer for orders topic"""
    return KafkaConsumer(
        'orders',
        bootstrap_servers=['localhost:9092'],
        group_id='inventory-service',  # Different group than order-processing!
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=False,
    )


def create_producer() -> KafkaProducer:
    """Create producer for inventory updates"""
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
        acks='all',
    )


def publish_inventory_event(producer: KafkaProducer, event_type: str, data: dict):
    """Publish inventory event"""
    event = {
        "event_type": event_type,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
    producer.send(
        topic='inventory-updates',
        key=data.get('product_id', 'system'),
        value=event
    )


def run_consumer():
    """Run the inventory consumer"""

    print("=" * 60)
    print("INVENTORY SERVICE")
    print("=" * 60)
    print()
    print("Consumer Group: inventory-service")
    print("Subscribed to: orders")
    print("Publishing to: inventory-updates")
    print()
    print("Press Ctrl+C to stop")
    print("-" * 60)

    consumer = create_consumer()
    producer = create_producer()
    inventory = InventoryManager()

    # Show initial inventory
    inventory.display_status()

    global running
    processed = 0
    reserved_items = 0
    out_of_stock = 0

    try:
        while running:
            messages = consumer.poll(timeout_ms=1000)

            for topic_partition, records in messages.items():
                for record in records:
                    order = record.value
                    order_id = order['order_id']

                    print(f"\n📦 Processing inventory for: {order_id}")

                    all_available = True
                    items_to_reserve = []

                    # Check availability for all items
                    for item in order['items']:
                        product_id = item['product_id']
                        quantity = item['quantity']

                        available = inventory.get_available(product_id)
                        if inventory.check_availability(product_id, quantity):
                            items_to_reserve.append((product_id, quantity))
                            print(f"   ✓ {item['product_name']}: {quantity} available ({available} in stock)")
                        else:
                            all_available = False
                            print(f"   ✗ {item['product_name']}: need {quantity}, only {available} available")
                            out_of_stock += 1

                            # Publish out of stock event
                            publish_inventory_event(producer, "out_of_stock", {
                                "product_id": product_id,
                                "product_name": item['product_name'],
                                "requested": quantity,
                                "available": available,
                                "order_id": order_id
                            })

                    # Reserve items if all available
                    if all_available:
                        for product_id, quantity in items_to_reserve:
                            inventory.reserve_stock(product_id, quantity)
                            reserved_items += 1

                            # In real system, would also commit after order confirmation
                            # For demo, we immediately commit
                            inventory.commit_reservation(product_id, quantity)

                        print(f"   ✅ Reserved {len(items_to_reserve)} items")

                        # Publish reservation event
                        publish_inventory_event(producer, "stock_reserved", {
                            "order_id": order_id,
                            "items": [{"product_id": p, "quantity": q} for p, q in items_to_reserve]
                        })
                    else:
                        print(f"   ❌ Cannot fulfill order - insufficient stock")

                    # Check for low stock alerts
                    low_stock = inventory.check_low_stock()
                    for item in low_stock:
                        print(f"   ⚠️  LOW STOCK ALERT: {item['name']} ({item['available']} remaining)")
                        publish_inventory_event(producer, "low_stock_alert", item)

                    processed += 1
                    consumer.commit()

            producer.flush()

            # Periodically show inventory status
            if processed > 0 and processed % 5 == 0:
                inventory.display_status()

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        consumer.close()
        producer.close()

        print("\n" + "=" * 60)
        print("INVENTORY SERVICE SUMMARY")
        print("=" * 60)
        print(f"\nOrders processed: {processed}")
        print(f"Items reserved: {reserved_items}")
        print(f"Out of stock events: {out_of_stock}")

        inventory.display_status()


if __name__ == "__main__":
    run_consumer()
