"""
Analytics Consumer
===================
Real-time analytics on order stream.

This demonstrates stream processing patterns:
- Aggregations (counts, sums)
- Windowed analytics
- Real-time dashboards

Run: python analytics_consumer.py
"""

import json
import signal
import time
from datetime import datetime, timedelta
from collections import defaultdict
from kafka import KafkaConsumer


# Graceful shutdown
running = True


def signal_handler(signum, frame):
    global running
    print("\n\n⚠️  Shutting down gracefully...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


class RealTimeAnalytics:
    """
    Real-time analytics engine for order data.
    Maintains running statistics as orders flow through.
    """

    def __init__(self):
        # Overall metrics
        self.total_orders = 0
        self.total_revenue = 0.0
        self.total_items = 0

        # Time-based metrics (last 5 minutes)
        self.window_size = 300  # seconds
        self.recent_orders = []  # (timestamp, order) tuples

        # Category metrics
        self.revenue_by_category = defaultdict(float)
        self.items_by_category = defaultdict(int)

        # Customer metrics
        self.revenue_by_tier = defaultdict(float)
        self.orders_by_tier = defaultdict(int)

        # Product metrics
        self.top_products = defaultdict(int)

        # Geographic metrics
        self.orders_by_city = defaultdict(int)

        # Payment metrics
        self.orders_by_payment = defaultdict(int)

        # Shipping metrics
        self.orders_by_shipping = defaultdict(int)

        # Time tracking
        self.start_time = datetime.now()

    def process_order(self, order: dict):
        """Process a single order and update all metrics"""

        now = datetime.now()

        # Basic metrics
        self.total_orders += 1
        self.total_revenue += order['total']

        # Track for windowed metrics
        self.recent_orders.append((now, order))

        # Clean old orders from window
        cutoff = now - timedelta(seconds=self.window_size)
        self.recent_orders = [(t, o) for t, o in self.recent_orders if t > cutoff]

        # Process items
        for item in order['items']:
            self.total_items += item['quantity']
            self.items_by_category[item['category']] += item['quantity']
            self.revenue_by_category[item['category']] += item['total']
            self.top_products[item['product_name']] += item['quantity']

        # Customer metrics
        tier = order['customer']['tier']
        self.revenue_by_tier[tier] += order['total']
        self.orders_by_tier[tier] += 1

        # Geographic metrics
        city = order['shipping']['address']['city']
        self.orders_by_city[city] += 1

        # Payment metrics
        self.orders_by_payment[order['payment_method']] += 1

        # Shipping metrics
        self.orders_by_shipping[order['shipping']['method']] += 1

    def get_windowed_metrics(self) -> dict:
        """Get metrics for the current time window"""
        if not self.recent_orders:
            return {"orders": 0, "revenue": 0, "avg_order": 0}

        window_orders = len(self.recent_orders)
        window_revenue = sum(o['total'] for _, o in self.recent_orders)

        return {
            "orders": window_orders,
            "revenue": window_revenue,
            "avg_order": window_revenue / window_orders if window_orders > 0 else 0,
            "orders_per_minute": window_orders / (self.window_size / 60)
        }

    def get_top_products(self, n: int = 5) -> list:
        """Get top N products by quantity sold"""
        sorted_products = sorted(
            self.top_products.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_products[:n]

    def display_dashboard(self):
        """Display real-time analytics dashboard"""

        runtime = datetime.now() - self.start_time
        window = self.get_windowed_metrics()

        # Clear screen (works in most terminals)
        print("\033[2J\033[H", end="")

        print("╔" + "═" * 78 + "╗")
        print("║" + " 📊 REAL-TIME ORDER ANALYTICS DASHBOARD ".center(78) + "║")
        print("╠" + "═" * 78 + "╣")

        # Runtime info
        print(f"║  Runtime: {str(runtime).split('.')[0]:20} "
              f"Last updated: {datetime.now().strftime('%H:%M:%S'):>20}          ║")
        print("╠" + "═" * 78 + "╣")

        # Overall metrics
        print("║" + " OVERALL METRICS ".center(78, "─") + "║")
        print(f"║  Total Orders: {self.total_orders:>10}     "
              f"Total Revenue: ${self.total_revenue:>12,.2f}     "
              f"Total Items: {self.total_items:>8}  ║")
        avg_order = self.total_revenue / self.total_orders if self.total_orders > 0 else 0
        print(f"║  Average Order Value: ${avg_order:>10,.2f}                                          ║")
        print("╠" + "═" * 78 + "╣")

        # Windowed metrics
        print("║" + f" LAST {self.window_size//60} MINUTES ".center(78, "─") + "║")
        print(f"║  Orders: {window['orders']:>5}     "
              f"Revenue: ${window['revenue']:>10,.2f}     "
              f"Rate: {window.get('orders_per_minute', 0):.1f} orders/min          ║")
        print("╠" + "═" * 78 + "╣")

        # Revenue by category
        print("║" + " REVENUE BY CATEGORY ".center(78, "─") + "║")
        for category, revenue in sorted(self.revenue_by_category.items(), key=lambda x: -x[1]):
            pct = revenue / self.total_revenue * 100 if self.total_revenue > 0 else 0
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"║  {category:<15} ${revenue:>10,.2f} {bar} {pct:>5.1f}%            ║")
        print("╠" + "═" * 78 + "╣")

        # Customer tiers
        print("║" + " ORDERS BY CUSTOMER TIER ".center(78, "─") + "║")
        for tier, count in sorted(self.orders_by_tier.items(), key=lambda x: -x[1]):
            revenue = self.revenue_by_tier[tier]
            avg = revenue / count if count > 0 else 0
            print(f"║  {tier:<12} Orders: {count:>5}  "
                  f"Revenue: ${revenue:>10,.2f}  Avg: ${avg:>8,.2f}           ║")
        print("╠" + "═" * 78 + "╣")

        # Top products
        print("║" + " TOP 5 PRODUCTS ".center(78, "─") + "║")
        for product, qty in self.get_top_products(5):
            print(f"║  {product:<30} Qty: {qty:>5}                                  ║")
        print("╠" + "═" * 78 + "╣")

        # Geographic distribution
        print("║" + " ORDERS BY CITY ".center(78, "─") + "║")
        cities = sorted(self.orders_by_city.items(), key=lambda x: -x[1])[:4]
        city_str = "  ".join([f"{city}: {count}" for city, count in cities])
        print(f"║  {city_str:<74}  ║")
        print("╠" + "═" * 78 + "╣")

        # Payment & Shipping
        print("║" + " PAYMENT METHODS ".center(39, "─") + "│" + " SHIPPING METHODS ".center(38, "─") + "║")
        payments = sorted(self.orders_by_payment.items(), key=lambda x: -x[1])
        shipping = sorted(self.orders_by_shipping.items(), key=lambda x: -x[1])

        max_rows = max(len(payments), len(shipping))
        for i in range(max_rows):
            pay_str = f"{payments[i][0]}: {payments[i][1]}" if i < len(payments) else ""
            ship_str = f"{shipping[i][0]}: {shipping[i][1]}" if i < len(shipping) else ""
            print(f"║  {pay_str:<36} │ {ship_str:<36}  ║")

        print("╚" + "═" * 78 + "╝")
        print("\nPress Ctrl+C to stop")


def create_consumer() -> KafkaConsumer:
    """Create consumer for orders topic"""
    return KafkaConsumer(
        'orders',
        bootstrap_servers=['localhost:9092'],
        group_id='analytics-service',  # Different group!
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )


def run_consumer():
    """Run the analytics consumer"""

    print("=" * 60)
    print("ANALYTICS SERVICE")
    print("=" * 60)
    print()
    print("Consumer Group: analytics-service")
    print("Subscribed to: orders")
    print()
    print("Starting dashboard in 3 seconds...")
    time.sleep(3)

    consumer = create_consumer()
    analytics = RealTimeAnalytics()

    global running
    last_display = time.time()
    display_interval = 1.0  # Update display every second

    try:
        while running:
            messages = consumer.poll(timeout_ms=500)

            for topic_partition, records in messages.items():
                for record in records:
                    order = record.value
                    analytics.process_order(order)

            # Update display periodically
            now = time.time()
            if now - last_display >= display_interval:
                analytics.display_dashboard()
                last_display = now

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        consumer.close()

        print("\n" + "=" * 60)
        print("FINAL ANALYTICS SUMMARY")
        print("=" * 60)
        print(f"\nTotal Orders Analyzed: {analytics.total_orders}")
        print(f"Total Revenue: ${analytics.total_revenue:,.2f}")
        print(f"Average Order Value: ${analytics.total_revenue/analytics.total_orders if analytics.total_orders > 0 else 0:,.2f}")


if __name__ == "__main__":
    run_consumer()
