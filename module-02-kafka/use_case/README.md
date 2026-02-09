# Use Case: Real-Time Order Processing System

A complete example demonstrating Kafka in an e-commerce order processing pipeline.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           E-COMMERCE ORDER SYSTEM                            │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │   Web/App    │
                              │   Frontend   │
                              └──────┬───────┘
                                     │
                                     ▼
                           ┌──────────────────┐
                           │   Order API      │
                           │   (Producer)     │
                           └────────┬─────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │   orders    │ │   orders    │ │   orders    │
            │     P0      │ │     P1      │ │     P2      │
            └─────────────┘ └─────────────┘ └─────────────┘
                    │               │               │
        ┌───────────┴───────────────┴───────────────┴───────────┐
        │                                                        │
        ▼                          ▼                            ▼
┌───────────────┐        ┌────────────────┐           ┌─────────────────┐
│ Order Service │        │ Inventory Svc  │           │ Analytics Svc   │
│ (Consumer     │        │ (Consumer      │           │ (Consumer       │
│  Group A)     │        │  Group B)      │           │  Group C)       │
│               │        │                │           │                 │
│ • Validate    │        │ • Reserve      │           │ • Real-time     │
│ • Process     │        │   stock        │           │   metrics       │
│ • Update DB   │        │ • Update       │           │ • Dashboard     │
│               │        │   inventory    │           │   updates       │
└───────┬───────┘        └────────┬───────┘           └─────────────────┘
        │                         │
        ▼                         ▼
┌───────────────┐        ┌────────────────┐
│ Notification  │        │ order-status   │
│    Topic      │        │    Topic       │
└───────────────┘        └────────────────┘
```

## Files

| File | Description |
|------|-------------|
| `order_producer.py` | Simulates order creation API |
| `order_consumer.py` | Processes orders and updates status |
| `inventory_consumer.py` | Manages inventory based on orders |
| `analytics_consumer.py` | Real-time order analytics |
| `run_demo.py` | Runs the complete demo |

## Quick Start

```bash
# 1. Start Kafka
cd ../real_kafka
docker-compose up -d

# 2. Install dependencies
pip install kafka-python

# 3. Run the demo (in separate terminals or use run_demo.py)
python order_producer.py      # Produces orders
python order_consumer.py      # Processes orders
python inventory_consumer.py  # Updates inventory
python analytics_consumer.py  # Shows real-time analytics
```

## Learning Objectives

1. **Multiple Consumer Groups** - Same topic, different processing
2. **Event-Driven Architecture** - Services react to events
3. **Eventual Consistency** - Async processing with guarantees
4. **Real-Time Analytics** - Stream processing basics
