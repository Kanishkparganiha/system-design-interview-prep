"""
Kafka Commit Log Simulation
============================
This script simulates Kafka's append-only commit log structure.

Key concepts demonstrated:
1. Append-only writes (O(1) complexity)
2. Immutable messages
3. Offset-based reading
4. Segment files
5. Log retention/compaction

Run: python 01_commit_log.py
"""

import os
import json
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Message:
    """Represents a single message in the log"""
    offset: int
    timestamp: float
    key: Optional[str]
    value: Any

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        return cls(**data)


class Segment:
    """
    A segment is a portion of the commit log.

    In real Kafka:
    - Segments are stored as .log files
    - Each segment has a .index file for fast lookups
    - Segments are named by their base offset
    """

    def __init__(self, base_offset: int, max_size: int = 5):
        self.base_offset = base_offset
        self.max_size = max_size  # Max messages per segment
        self.messages: List[Message] = []
        self.is_active = True

    def append(self, message: Message) -> bool:
        """Append a message to this segment"""
        if len(self.messages) >= self.max_size:
            self.is_active = False
            return False
        self.messages.append(message)
        return True

    def read(self, offset: int) -> Optional[Message]:
        """Read a message by offset"""
        for msg in self.messages:
            if msg.offset == offset:
                return msg
        return None

    def __len__(self) -> int:
        return len(self.messages)

    def __repr__(self) -> str:
        return f"Segment(base={self.base_offset}, messages={len(self)})"


class CommitLog:
    """
    Simulates Kafka's commit log for a single partition.

    Features:
    - Append-only writes
    - Segment-based storage
    - Offset tracking
    - Sequential reads
    """

    def __init__(self, name: str, segment_size: int = 5):
        self.name = name
        self.segment_size = segment_size
        self.segments: List[Segment] = []
        self.current_offset = 0

        # Create initial segment
        self._create_new_segment()

    def _create_new_segment(self):
        """Create a new active segment"""
        segment = Segment(self.current_offset, self.segment_size)
        self.segments.append(segment)
        print(f"📁 Created new segment starting at offset {self.current_offset}")

    def _get_active_segment(self) -> Segment:
        """Get the current active segment, creating new one if needed"""
        if not self.segments[-1].is_active:
            self._create_new_segment()
        return self.segments[-1]

    def append(self, key: Optional[str], value: Any) -> int:
        """
        Append a message to the log.
        Returns the offset of the written message.

        This is O(1) - always appending to the end!
        """
        message = Message(
            offset=self.current_offset,
            timestamp=time.time(),
            key=key,
            value=value
        )

        segment = self._get_active_segment()
        if not segment.append(message):
            # Segment is full, create new one
            segment = self._get_active_segment()
            segment.append(message)

        written_offset = self.current_offset
        self.current_offset += 1

        return written_offset

    def read(self, offset: int) -> Optional[Message]:
        """
        Read a message by offset.

        In real Kafka:
        1. Find the right segment (binary search on base offsets)
        2. Use .index file to find approximate position
        3. Sequential scan to exact offset
        """
        # Find the right segment
        for segment in self.segments:
            if segment.base_offset <= offset < segment.base_offset + len(segment):
                return segment.read(offset)
        return None

    def read_from(self, start_offset: int, count: int = 10) -> List[Message]:
        """Read multiple messages starting from an offset"""
        messages = []
        for offset in range(start_offset, min(start_offset + count, self.current_offset)):
            msg = self.read(offset)
            if msg:
                messages.append(msg)
        return messages

    def get_latest_offset(self) -> int:
        """Get the offset of the next message to be written"""
        return self.current_offset

    def get_earliest_offset(self) -> int:
        """Get the earliest available offset"""
        if self.segments:
            return self.segments[0].base_offset
        return 0

    def stats(self) -> Dict:
        """Get log statistics"""
        return {
            "name": self.name,
            "total_messages": self.current_offset,
            "num_segments": len(self.segments),
            "earliest_offset": self.get_earliest_offset(),
            "latest_offset": self.get_latest_offset(),
            "segments": [repr(s) for s in self.segments]
        }


def demo_commit_log():
    """Demonstrate the commit log functionality"""

    print("=" * 60)
    print("KAFKA COMMIT LOG SIMULATION")
    print("=" * 60)
    print()

    # Create a commit log (simulating one partition)
    log = CommitLog("orders-partition-0", segment_size=5)

    # Simulate producer sending messages
    print("📝 PRODUCING MESSAGES")
    print("-" * 40)

    orders = [
        ("user-1", {"order_id": "A001", "item": "Laptop", "price": 999}),
        ("user-2", {"order_id": "A002", "item": "Mouse", "price": 29}),
        ("user-1", {"order_id": "A003", "item": "Keyboard", "price": 79}),
        ("user-3", {"order_id": "A004", "item": "Monitor", "price": 299}),
        ("user-2", {"order_id": "A005", "item": "Headphones", "price": 149}),
        # These will create a new segment
        ("user-4", {"order_id": "A006", "item": "Webcam", "price": 89}),
        ("user-1", {"order_id": "A007", "item": "USB Hub", "price": 35}),
        ("user-5", {"order_id": "A008", "item": "SSD", "price": 120}),
    ]

    for key, value in orders:
        offset = log.append(key, value)
        print(f"  Written: offset={offset}, key={key}, order_id={value['order_id']}")
        time.sleep(0.1)  # Small delay for different timestamps

    print()

    # Show log statistics
    print("📊 LOG STATISTICS")
    print("-" * 40)
    stats = log.stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print()

    # Read individual messages
    print("📖 READING INDIVIDUAL MESSAGES")
    print("-" * 40)
    for offset in [0, 3, 5, 7]:
        msg = log.read(offset)
        if msg:
            print(f"  Offset {offset}: key={msg.key}, value={msg.value}")
    print()

    # Simulate consumer reading from an offset
    print("🚚 CONSUMER READING (starting from offset 3)")
    print("-" * 40)
    messages = log.read_from(start_offset=3, count=4)
    for msg in messages:
        print(f"  Consumed: offset={msg.offset}, key={msg.key}")
        print(f"            value={msg.value}")
    print()

    # Demonstrate immutability
    print("🔒 DEMONSTRATING IMMUTABILITY")
    print("-" * 40)
    print("  In Kafka, messages are NEVER modified after writing.")
    print("  This enables:")
    print("    • Multiple consumers reading same data")
    print("    • Replay from any point in history")
    print("    • Safe replication to followers")
    print()

    # Show segment structure
    print("📁 SEGMENT FILE STRUCTURE (conceptual)")
    print("-" * 40)
    print("""
    In real Kafka, the log directory looks like:

    orders-partition-0/
    ├── 00000000000000000000.log     <- Segment 1 (offsets 0-4)
    ├── 00000000000000000000.index   <- Sparse index
    ├── 00000000000000000000.timeindex
    ├── 00000000000000000005.log     <- Segment 2 (offsets 5+)
    ├── 00000000000000000005.index
    └── 00000000000000000005.timeindex
    """)


if __name__ == "__main__":
    demo_commit_log()
