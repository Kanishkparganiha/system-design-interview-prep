"""
Kafka Consumer Groups Simulation
=================================
This script simulates how Kafka consumer groups work.

Key concepts demonstrated:
1. Consumer group partition assignment
2. Rebalancing when consumers join/leave
3. Offset management
4. Multiple consumer groups on same topic

Run: python 03_consumer_groups.py
"""

import time
import random
from typing import Optional, List, Dict, Set
from dataclasses import dataclass, field
from enum import Enum


class AssignmentStrategy(Enum):
    RANGE = "range"
    ROUND_ROBIN = "round_robin"
    STICKY = "sticky"


@dataclass
class Partition:
    """Represents a topic partition"""
    topic: str
    partition_id: int
    messages: List[Dict] = field(default_factory=list)

    def __hash__(self):
        return hash((self.topic, self.partition_id))


@dataclass
class Consumer:
    """Represents a consumer in a consumer group"""
    consumer_id: str
    group_id: str
    assigned_partitions: Set[Partition] = field(default_factory=set)
    current_offsets: Dict[Partition, int] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.consumer_id)


class ConsumerGroup:
    """
    Simulates a Kafka consumer group.

    Key behaviors:
    - Partitions are distributed among consumers
    - Each partition goes to exactly ONE consumer
    - When consumers join/leave, rebalancing occurs
    """

    def __init__(self, group_id: str, strategy: AssignmentStrategy = AssignmentStrategy.ROUND_ROBIN):
        self.group_id = group_id
        self.strategy = strategy
        self.consumers: Dict[str, Consumer] = {}
        self.subscribed_topics: Dict[str, List[Partition]] = {}
        self.committed_offsets: Dict[str, Dict[Partition, int]] = {}  # consumer_id -> {partition: offset}

    def subscribe(self, topic: str, partitions: List[Partition]):
        """Subscribe the group to a topic"""
        self.subscribed_topics[topic] = partitions
        print(f"📬 Group '{self.group_id}' subscribed to topic '{topic}' ({len(partitions)} partitions)")

    def add_consumer(self, consumer_id: str) -> Consumer:
        """Add a consumer to the group and trigger rebalancing"""
        consumer = Consumer(consumer_id=consumer_id, group_id=self.group_id)
        self.consumers[consumer_id] = consumer
        print(f"\n➕ Consumer '{consumer_id}' joining group '{self.group_id}'")
        self._rebalance()
        return consumer

    def remove_consumer(self, consumer_id: str):
        """Remove a consumer and trigger rebalancing"""
        if consumer_id in self.consumers:
            # Save committed offsets
            consumer = self.consumers[consumer_id]
            self.committed_offsets[consumer_id] = consumer.current_offsets.copy()

            del self.consumers[consumer_id]
            print(f"\n➖ Consumer '{consumer_id}' leaving group '{self.group_id}'")
            self._rebalance()

    def _rebalance(self):
        """
        Reassign partitions to consumers.
        This simulates the GroupCoordinator's rebalancing logic.
        """
        print(f"\n🔄 REBALANCING GROUP '{self.group_id}'")
        print("-" * 40)

        if not self.consumers:
            print("  No consumers in group")
            return

        # Get all partitions
        all_partitions = []
        for partitions in self.subscribed_topics.values():
            all_partitions.extend(partitions)

        # Clear current assignments
        for consumer in self.consumers.values():
            consumer.assigned_partitions.clear()

        # Assign partitions based on strategy
        if self.strategy == AssignmentStrategy.ROUND_ROBIN:
            self._assign_round_robin(all_partitions)
        elif self.strategy == AssignmentStrategy.RANGE:
            self._assign_range(all_partitions)

        # Print assignments
        self._print_assignments()

    def _assign_round_robin(self, partitions: List[Partition]):
        """Round-robin assignment: distribute partitions evenly"""
        consumers = list(self.consumers.values())
        for i, partition in enumerate(partitions):
            consumer = consumers[i % len(consumers)]
            consumer.assigned_partitions.add(partition)
            # Initialize offset if not committed
            if partition not in consumer.current_offsets:
                consumer.current_offsets[partition] = 0

    def _assign_range(self, partitions: List[Partition]):
        """Range assignment: assign contiguous ranges of partitions"""
        consumers = sorted(self.consumers.values(), key=lambda c: c.consumer_id)
        num_consumers = len(consumers)
        num_partitions = len(partitions)

        partitions_per_consumer = num_partitions // num_consumers
        extra = num_partitions % num_consumers

        partition_index = 0
        for i, consumer in enumerate(consumers):
            # Some consumers get one extra partition
            count = partitions_per_consumer + (1 if i < extra else 0)
            for _ in range(count):
                if partition_index < len(partitions):
                    partition = partitions[partition_index]
                    consumer.assigned_partitions.add(partition)
                    if partition not in consumer.current_offsets:
                        consumer.current_offsets[partition] = 0
                    partition_index += 1

    def _print_assignments(self):
        """Print current partition assignments"""
        for consumer_id, consumer in self.consumers.items():
            partitions = sorted([p.partition_id for p in consumer.assigned_partitions])
            print(f"  {consumer_id}: Partitions {partitions}")

    def get_assignment(self, consumer_id: str) -> Set[Partition]:
        """Get partitions assigned to a consumer"""
        if consumer_id in self.consumers:
            return self.consumers[consumer_id].assigned_partitions
        return set()


class Topic:
    """Simulates a Kafka topic"""

    def __init__(self, name: str, num_partitions: int):
        self.name = name
        self.partitions = [
            Partition(topic=name, partition_id=i)
            for i in range(num_partitions)
        ]

    def produce(self, partition_id: int, message: Dict):
        """Add a message to a partition"""
        self.partitions[partition_id].messages.append(message)


def demo_basic_consumer_group():
    """Demonstrate basic consumer group functionality"""

    print("=" * 60)
    print("BASIC CONSUMER GROUP")
    print("=" * 60)

    # Create a topic with 6 partitions
    topic = Topic("orders", num_partitions=6)

    # Add some messages
    for i in range(18):
        partition = i % 6
        topic.produce(partition, {"order_id": f"order-{i}", "amount": random.randint(10, 100)})

    # Create a consumer group
    group = ConsumerGroup("order-processors", AssignmentStrategy.ROUND_ROBIN)
    group.subscribe("orders", topic.partitions)

    # Add consumers one by one and observe rebalancing
    print("\n📊 Adding consumers and observing rebalancing:")

    group.add_consumer("consumer-1")
    time.sleep(0.5)

    group.add_consumer("consumer-2")
    time.sleep(0.5)

    group.add_consumer("consumer-3")

    print("\n" + "=" * 60)
    print("OBSERVATION: 6 partitions distributed evenly to 3 consumers")
    print("Each consumer handles 2 partitions")
    print("=" * 60)


def demo_consumer_failure():
    """Demonstrate rebalancing when a consumer fails"""

    print("\n" + "=" * 60)
    print("CONSUMER FAILURE & REBALANCING")
    print("=" * 60)

    topic = Topic("events", num_partitions=4)

    group = ConsumerGroup("event-processors", AssignmentStrategy.ROUND_ROBIN)
    group.subscribe("events", topic.partitions)

    # Add 4 consumers (1 partition each)
    for i in range(1, 5):
        group.add_consumer(f"consumer-{i}")

    print("\n💥 Simulating consumer-2 CRASH...")
    time.sleep(0.5)

    group.remove_consumer("consumer-2")

    print("\n" + "=" * 60)
    print("OBSERVATION: Partitions from failed consumer redistributed")
    print("Remaining 3 consumers now handle 4 partitions")
    print("=" * 60)


def demo_multiple_consumer_groups():
    """Demonstrate multiple consumer groups on same topic"""

    print("\n" + "=" * 60)
    print("MULTIPLE CONSUMER GROUPS")
    print("=" * 60)
    print()
    print("Different groups can independently consume the same topic!")
    print()

    # Create a topic
    topic = Topic("user-activity", num_partitions=3)

    # Group 1: Analytics service
    analytics_group = ConsumerGroup("analytics-service", AssignmentStrategy.ROUND_ROBIN)
    analytics_group.subscribe("user-activity", topic.partitions)

    # Group 2: Notification service
    notification_group = ConsumerGroup("notification-service", AssignmentStrategy.ROUND_ROBIN)
    notification_group.subscribe("user-activity", topic.partitions)

    print("Adding consumers to Analytics group:")
    analytics_group.add_consumer("analytics-1")
    analytics_group.add_consumer("analytics-2")

    print("\nAdding consumers to Notification group:")
    notification_group.add_consumer("notifier-1")

    print("\n" + "=" * 60)
    print("OBSERVATION:")
    print("  • Both groups read ALL messages from the topic")
    print("  • Groups are completely independent")
    print("  • Each group tracks its own offsets")
    print("=" * 60)


def demo_consumer_scaling():
    """Demonstrate what happens when consumers > partitions"""

    print("\n" + "=" * 60)
    print("CONSUMER SCALING LIMITS")
    print("=" * 60)
    print()
    print("What happens when you have MORE consumers than partitions?")
    print()

    topic = Topic("small-topic", num_partitions=2)

    group = ConsumerGroup("greedy-consumers", AssignmentStrategy.ROUND_ROBIN)
    group.subscribe("small-topic", topic.partitions)

    group.add_consumer("consumer-1")
    group.add_consumer("consumer-2")
    group.add_consumer("consumer-3")
    group.add_consumer("consumer-4")

    print("\n" + "=" * 60)
    print("OBSERVATION:")
    print("  • Only 2 consumers are active (matching partition count)")
    print("  • Extra consumers are IDLE")
    print("  • Max parallelism = Number of partitions!")
    print("  • This is why partition count is a critical design decision")
    print("=" * 60)


def demo_offset_tracking():
    """Demonstrate offset tracking within consumer groups"""

    print("\n" + "=" * 60)
    print("OFFSET TRACKING")
    print("=" * 60)

    print("""
    Each consumer group tracks its position (offset) independently:

    Topic: user-events (3 partitions)

                        Partition 0     Partition 1     Partition 2
    Messages:          [0,1,2,3,4,5]   [0,1,2,3,4,5]   [0,1,2,3,4,5]
                            ↑               ↑               ↑
    analytics-group:       offset=4        offset=3        offset=5
    notification-group:    offset=2        offset=5        offset=1


    Key behaviors:
    ─────────────────────────────────────────────────────────────

    1. COMMITTED OFFSET
       • Position saved to __consumer_offsets topic
       • Survives consumer restarts
       • "Last successfully processed message"

    2. AUTO COMMIT
       • enable.auto.commit=true (default)
       • Commits periodically in background
       • Risk: may commit before processing complete

    3. MANUAL COMMIT
       • enable.auto.commit=false
       • Call consumer.commit() after processing
       • Safer but requires explicit handling

    4. OFFSET RESET
       • auto.offset.reset=earliest (start from beginning)
       • auto.offset.reset=latest (start from newest)
       • Used when no committed offset exists
    """)


def main():
    demo_basic_consumer_group()
    demo_consumer_failure()
    demo_multiple_consumer_groups()
    demo_consumer_scaling()
    demo_offset_tracking()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
    1. Each partition → exactly ONE consumer in a group
    2. Consumers > partitions = idle consumers
    3. Consumer failure → automatic rebalancing
    4. Multiple groups = independent consumption
    5. Offset tracking enables exactly-once processing
    6. max(parallelism) = number of partitions
    """)


if __name__ == "__main__":
    main()
