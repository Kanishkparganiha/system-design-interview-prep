"""
Order Processing Demo Runner
=============================
Runs all components of the order processing system in one terminal.

This is a convenient way to see the entire system working together.

Run: python run_demo.py
"""

import subprocess
import sys
import time
import os
import signal
from threading import Thread


# Track all processes for cleanup
processes = []


def cleanup(signum=None, frame=None):
    """Clean up all spawned processes"""
    print("\n\n🛑 Stopping all services...")
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except:
            proc.kill()
    print("✅ All services stopped")
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


def run_service(name: str, script: str, delay: float = 0):
    """Run a service script"""
    if delay:
        time.sleep(delay)

    print(f"\n🚀 Starting {name}...")

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script)

    proc = subprocess.Popen(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )
    processes.append(proc)

    # Stream output
    for line in proc.stdout:
        print(f"[{name}] {line}", end="")


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║         ORDER PROCESSING SYSTEM DEMO                          ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  This demo runs all components of the order processing        ║
    ║  system to show how Kafka enables event-driven architecture.  ║
    ║                                                               ║
    ║  Components:                                                  ║
    ║  1. Order Producer - Generates orders                         ║
    ║  2. Order Consumer - Processes orders                         ║
    ║  3. Inventory Consumer - Manages stock                        ║
    ║  4. Analytics Consumer - Real-time metrics                    ║
    ║                                                               ║
    ║  Prerequisites:                                               ║
    ║  - Kafka running: docker-compose up -d                        ║
    ║  - kafka-python installed: pip install kafka-python           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    print("\n📋 Choose demo mode:")
    print("  1. Run all services (best viewed in separate terminals)")
    print("  2. Run producer only (generates orders)")
    print("  3. Run order processor only")
    print("  4. Run inventory service only")
    print("  5. Run analytics dashboard only")
    print("  q. Quit")

    choice = input("\nSelect option (1-5 or q): ").strip().lower()

    if choice == 'q':
        return

    if choice == '1':
        print("""
        ⚠️  For the best experience, run each service in a separate terminal:

        Terminal 1: python analytics_consumer.py   (Start first for the dashboard)
        Terminal 2: python order_consumer.py
        Terminal 3: python inventory_consumer.py
        Terminal 4: python order_producer.py --orders 20 --delay 2

        This allows you to see all outputs clearly.

        Alternatively, press Enter to run the producer only and observe
        how messages are processed by consumers you start separately.
        """)
        input("Press Enter to continue with producer only...")
        choice = '2'

    script_map = {
        '2': ('Order Producer', 'order_producer.py'),
        '3': ('Order Processor', 'order_consumer.py'),
        '4': ('Inventory Service', 'inventory_consumer.py'),
        '5': ('Analytics Dashboard', 'analytics_consumer.py'),
    }

    if choice in script_map:
        name, script = script_map[choice]
        run_service(name, script)
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
