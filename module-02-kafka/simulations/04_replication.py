"""
Kafka Replication Simulation
=============================
This script simulates how Kafka handles replication and fault tolerance.

Key concepts demonstrated:
1. Leader-follower replication
2. In-Sync Replicas (ISR)
3. Producer acknowledgments (acks)
4. Leader election on failure
5. Replication factor

Run: python 04_replication.py
"""

import time
import random
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from threading import Thread
import queue


class AckMode(Enum):
    FIRE_AND_FORGET = 0  # acks=0
    LEADER_ONLY = 1      # acks=1
    ALL_REPLICAS = -1    # acks=all


@dataclass
class Message:
    """A message to be replicated"""
    offset: int
    key: Optional[str]
    value: str
    timestamp: float = field(default_factory=time.time)


class Replica:
    """
    Simulates a replica of a partition on a broker.
    Can be either a leader or a follower.
    """

    def __init__(self, broker_id: int, partition_id: int):
        self.broker_id = broker_id
        self.partition_id = partition_id
        self.messages: List[Message] = []
        self.is_leader = False
        self.is_alive = True
        self.high_watermark = 0  # Highest replicated offset
        self.log_end_offset = 0  # Latest offset in this replica

    def append(self, message: Message) -> bool:
        """Append a message to this replica's log"""
        if not self.is_alive:
            return False
        self.messages.append(message)
        self.log_end_offset = message.offset + 1
        return True

    def get_lag(self, leader_leo: int) -> int:
        """Get replication lag compared to leader"""
        return leader_leo - self.log_end_offset

    def __repr__(self):
        role = "LEADER" if self.is_leader else "follower"
        status = "UP" if self.is_alive else "DOWN"
        return f"Broker-{self.broker_id}({role}, {status}, LEO={self.log_end_offset})"


class Partition:
    """
    Simulates a Kafka partition with replication.

    Key components:
    - One leader handles all reads/writes
    - Followers replicate from leader
    - ISR tracks which replicas are caught up
    """

    def __init__(self, topic: str, partition_id: int, replication_factor: int, broker_ids: List[int]):
        self.topic = topic
        self.partition_id = partition_id
        self.replication_factor = replication_factor

        # Create replicas on different brokers
        self.replicas: Dict[int, Replica] = {}
        for i, broker_id in enumerate(broker_ids[:replication_factor]):
            replica = Replica(broker_id, partition_id)
            self.replicas[broker_id] = replica

        # First replica is initially the leader
        self.leader_broker = broker_ids[0]
        self.replicas[self.leader_broker].is_leader = True

        # In-Sync Replicas - replicas that are caught up with leader
        self.isr: Set[int] = set(broker_ids[:replication_factor])

        self.current_offset = 0
        self.high_watermark = 0  # Committed offset (replicated to all ISR)

    def get_leader(self) -> Optional[Replica]:
        """Get the current leader replica"""
        if self.leader_broker and self.leader_broker in self.replicas:
            leader = self.replicas[self.leader_broker]
            if leader.is_alive:
                return leader
        return None

    def produce(self, key: Optional[str], value: str, acks: AckMode) -> Dict:
        """
        Produce a message with specified acknowledgment mode.

        acks=0: Don't wait for any acknowledgment
        acks=1: Wait for leader to write
        acks=all: Wait for all ISR replicas to write
        """
        result = {
            "success": False,
            "offset": None,
            "message": None
        }

        leader = self.get_leader()
        if not leader:
            result["message"] = "No leader available!"
            return result

        # Create message
        message = Message(
            offset=self.current_offset,
            key=key,
            value=value
        )

        # acks=0: Fire and forget
        if acks == AckMode.FIRE_AND_FORGET:
            leader.append(message)
            self.current_offset += 1
            result["success"] = True
            result["offset"] = message.offset
            result["message"] = "Sent (no ack waited)"
            return result

        # acks=1: Leader acknowledgment
        if acks == AckMode.LEADER_ONLY:
            if leader.append(message):
                self.current_offset += 1
                result["success"] = True
                result["offset"] = message.offset
                result["message"] = "Leader acknowledged"
            else:
                result["message"] = "Leader failed to write"
            return result

        # acks=all: All ISR acknowledgment
        if acks == AckMode.ALL_REPLICAS:
            # Write to leader first
            if not leader.append(message):
                result["message"] = "Leader failed to write"
                return result

            # Replicate to followers in ISR
            replicated_to = {self.leader_broker}
            for broker_id in self.isr:
                if broker_id != self.leader_broker:
                    follower = self.replicas[broker_id]
                    if follower.is_alive and follower.append(message):
                        replicated_to.add(broker_id)

            # Check if replicated to all ISR
            if replicated_to == self.isr:
                self.current_offset += 1
                self.high_watermark = message.offset + 1
                result["success"] = True
                result["offset"] = message.offset
                result["message"] = f"Replicated to {len(replicated_to)} replicas"
            else:
                result["message"] = f"Only replicated to {len(replicated_to)}/{len(self.isr)} ISR"

            return result

    def fail_broker(self, broker_id: int):
        """Simulate a broker failure"""
        if broker_id in self.replicas:
            self.replicas[broker_id].is_alive = False

            # Remove from ISR
            self.isr.discard(broker_id)

            # If leader failed, elect new leader
            if broker_id == self.leader_broker:
                self._elect_new_leader()

    def recover_broker(self, broker_id: int):
        """Simulate a broker recovery"""
        if broker_id in self.replicas:
            replica = self.replicas[broker_id]
            replica.is_alive = True

            # Replica needs to catch up before rejoining ISR
            # In real Kafka, it fetches from leader until caught up
            print(f"  Broker-{broker_id} recovering, needs to catch up...")

    def _elect_new_leader(self):
        """Elect a new leader from ISR"""
        print(f"\n  🔄 LEADER ELECTION for {self.topic}-{self.partition_id}")

        # Choose first available replica from ISR
        new_leader = None
        for broker_id in self.isr:
            if self.replicas[broker_id].is_alive:
                new_leader = broker_id
                break

        if new_leader:
            # Demote old leader
            if self.leader_broker in self.replicas:
                self.replicas[self.leader_broker].is_leader = False

            # Promote new leader
            self.leader_broker = new_leader
            self.replicas[new_leader].is_leader = True
            print(f"  ✅ Broker-{new_leader} elected as new leader")
        else:
            self.leader_broker = None
            print(f"  ❌ No available replicas in ISR! Partition is OFFLINE")

    def status(self) -> str:
        """Get partition status"""
        lines = [f"\n  Partition {self.partition_id}:"]
        lines.append(f"    Leader: Broker-{self.leader_broker}")
        lines.append(f"    ISR: {sorted(self.isr)}")
        lines.append(f"    Replicas:")
        for broker_id, replica in sorted(self.replicas.items()):
            lines.append(f"      {replica}")
        return "\n".join(lines)


def demo_replication_basics():
    """Demonstrate basic replication"""

    print("=" * 60)
    print("KAFKA REPLICATION BASICS")
    print("=" * 60)
    print()
    print("Replication Factor = 3 means each message is stored on 3 brokers")
    print()

    # Create a partition with replication factor 3
    partition = Partition(
        topic="orders",
        partition_id=0,
        replication_factor=3,
        broker_ids=[1, 2, 3]
    )

    print("Initial state:")
    print(partition.status())
    print()

    print("Writing messages with acks=all:")
    print("-" * 40)

    for i in range(3):
        result = partition.produce(
            key=f"key-{i}",
            value=f"order-{i}",
            acks=AckMode.ALL_REPLICAS
        )
        print(f"  Message {i}: {result['message']} (offset={result['offset']})")

    print()
    print("After writes:")
    print(partition.status())


def demo_ack_modes():
    """Demonstrate different acknowledgment modes"""

    print("\n" + "=" * 60)
    print("ACKNOWLEDGMENT MODES")
    print("=" * 60)
    print()

    print("""
    ┌─────────────────────────────────────────────────────────────┐
    │                    PRODUCER ACK MODES                        │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │  acks=0 (Fire and Forget)                                    │
    │  ─────────────────────────                                   │
    │  Producer ──msg──▶ [Leader]     [Follower]    [Follower]    │
    │     ✓                                                        │
    │  • Fastest, no waiting                                       │
    │  • Risk: Message may be lost if leader fails                 │
    │                                                              │
    │  acks=1 (Leader Only)                                        │
    │  ────────────────────                                        │
    │  Producer ──msg──▶ [Leader] ──▶ [Follower]    [Follower]    │
    │     ◀──ack──────────  ✓           (async)       (async)     │
    │  • Wait for leader write                                     │
    │  • Risk: Lost if leader fails before replication             │
    │                                                              │
    │  acks=all (All In-Sync Replicas)                            │
    │  ───────────────────────────────                             │
    │  Producer ──msg──▶ [Leader] ──▶ [Follower] ──▶ [Follower]   │
    │     ◀──────ack───────  ✓            ✓             ✓         │
    │  • Wait for all ISR to acknowledge                          │
    │  • Safest, but slowest                                       │
    │  • Combined with min.insync.replicas for durability         │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
    """)

    # Demonstrate timing differences
    partition = Partition(
        topic="test",
        partition_id=0,
        replication_factor=3,
        broker_ids=[1, 2, 3]
    )

    print("Simulated latency comparison:")
    print("-" * 40)

    modes = [
        (AckMode.FIRE_AND_FORGET, "acks=0"),
        (AckMode.LEADER_ONLY, "acks=1"),
        (AckMode.ALL_REPLICAS, "acks=all"),
    ]

    for mode, name in modes:
        start = time.time()
        for _ in range(100):
            partition.produce("key", "value", mode)
        elapsed = time.time() - start
        print(f"  {name:12}: {elapsed*1000:.2f}ms for 100 messages")


def demo_leader_failure():
    """Demonstrate leader failure and election"""

    print("\n" + "=" * 60)
    print("LEADER FAILURE & ELECTION")
    print("=" * 60)

    partition = Partition(
        topic="critical-data",
        partition_id=0,
        replication_factor=3,
        broker_ids=[1, 2, 3]
    )

    print("\nInitial state:")
    print(partition.status())

    # Produce some messages
    print("\nProducing 3 messages...")
    for i in range(3):
        partition.produce(f"key-{i}", f"value-{i}", AckMode.ALL_REPLICAS)

    print("\n💥 BROKER-1 (Leader) CRASHES!")
    partition.fail_broker(1)

    print("\nAfter failure:")
    print(partition.status())

    # Try to produce after failure
    print("\nProducing message after leader failure...")
    result = partition.produce("new-key", "new-value", AckMode.ALL_REPLICAS)
    print(f"  Result: {result['message']}")

    print("\nAfter new write:")
    print(partition.status())


def demo_isr_shrink():
    """Demonstrate ISR shrinking when follower falls behind"""

    print("\n" + "=" * 60)
    print("IN-SYNC REPLICAS (ISR) BEHAVIOR")
    print("=" * 60)

    print("""
    ISR = Set of replicas that are "in-sync" with the leader

    A replica is removed from ISR when:
    1. It fails/becomes unavailable
    2. It falls behind (lag > replica.lag.time.max.ms)

    Why ISR matters:
    ─────────────────
    • acks=all only waits for ISR replicas
    • Leader election only considers ISR members
    • min.insync.replicas ensures durability
    """)

    partition = Partition(
        topic="orders",
        partition_id=0,
        replication_factor=3,
        broker_ids=[1, 2, 3]
    )

    print("\nScenario: Broker-3 becomes slow/unresponsive")
    print("-" * 40)
    print(f"\nInitial ISR: {sorted(partition.isr)}")

    # Simulate Broker-3 falling out of ISR
    print("\n⚠️  Broker-3 falls behind (removed from ISR)")
    partition.isr.discard(3)
    print(f"Current ISR: {sorted(partition.isr)}")

    # Produce with acks=all
    print("\nProducing with acks=all...")
    result = partition.produce("key", "value", AckMode.ALL_REPLICAS)
    print(f"  Result: {result['message']}")
    print("  Note: Only waited for Broker-1 and Broker-2!")

    # What if ISR shrinks to just leader?
    print("\n⚠️  Broker-2 also falls behind")
    partition.isr.discard(2)
    print(f"Current ISR: {sorted(partition.isr)}")

    print("""
    With ISR = {1} and min.insync.replicas=2:
    • Producer with acks=all would FAIL
    • This prevents data loss at the cost of availability

    Trade-off: Availability vs Durability
    """)


def demo_unclean_leader_election():
    """Demonstrate unclean leader election scenario"""

    print("\n" + "=" * 60)
    print("UNCLEAN LEADER ELECTION")
    print("=" * 60)

    print("""
    What if ALL ISR replicas fail?

    Scenario:
    ─────────
    • Replication factor: 3
    • ISR: {1, 2} (Broker-3 was behind)
    • Broker-1 (leader) and Broker-2 fail simultaneously!

    Option 1: Wait for ISR replica to recover (default)
    ──────────────────────────────────────────────────
    • Partition stays OFFLINE
    • No data loss
    • Availability sacrificed

    Option 2: unclean.leader.election.enable=true
    ──────────────────────────────────────────────
    • Broker-3 (out-of-sync) becomes leader
    • Partition comes back ONLINE
    • ⚠️ DATA LOSS: messages only on Broker-1/2 are lost!


    Visualization:
    ─────────────────────────────────────────────────────
    Before failure:

    Broker-1 (Leader, ISR): [msg1, msg2, msg3, msg4, msg5]
    Broker-2 (ISR):         [msg1, msg2, msg3, msg4, msg5]
    Broker-3 (not in ISR):  [msg1, msg2, msg3]  ← behind!

    After Broker-1 & 2 fail, Broker-3 becomes leader:

    Broker-3 (New Leader):  [msg1, msg2, msg3]

    msg4 and msg5 are LOST forever!
    ─────────────────────────────────────────────────────

    Best Practice:
    • Keep unclean.leader.election.enable=false (default)
    • Use min.insync.replicas >= 2
    • Monitor ISR closely
    """)


def main():
    demo_replication_basics()
    demo_ack_modes()
    demo_leader_failure()
    demo_isr_shrink()
    demo_unclean_leader_election()

    print("\n" + "=" * 60)
    print("KEY TAKEAWAYS")
    print("=" * 60)
    print("""
    1. Replication Factor determines copies of each partition
    2. Leader handles ALL reads and writes
    3. Followers replicate from leader
    4. ISR = replicas that are caught up
    5. acks setting controls durability vs performance
    6. Leader election happens from ISR members
    7. min.insync.replicas prevents writes when ISR too small

    Recommended Production Settings:
    ─────────────────────────────────
    replication.factor=3
    min.insync.replicas=2
    acks=all
    unclean.leader.election.enable=false
    """)


if __name__ == "__main__":
    main()
