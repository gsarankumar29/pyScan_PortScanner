# Pyscan - A Simple TCP Port Scanner
# This script is a basic cybersecurity tool used for reconnaissance.
# It checks a target host (IP or hostname) for open TCP ports within a specified range.

import socket
import argparse
from datetime import datetime
import threading
from queue import Queue

# Configuration
# Increase this value for slower network conditions, but it will slow down the scan.
SCAN_TIMEOUT = 1.0  
# Max threads to run concurrently
MAX_THREADS = 100 

def port_scan(target_ip, port):
    """
    Attempts to connect to the given port on the target IP.
    Uses the basic TCP Connect Scan method (a full 3-way handshake attempt).
    """
    # Create a new socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(SCAN_TIMEOUT)

    try:
        # Attempt to establish a connection
        result = s.connect_ex((target_ip, port))
        
        # connect_ex returns 0 if the connection is successful (port is open)
        if result == 0:
            try:
                # Attempt to retrieve the service name associated with the port
                service = socket.getservbyport(port, 'tcp')
            except OSError:
                service = "Unknown"
            
            print(f"| {port:<5} | OPEN   | {service}")

    except socket.error as e:
        # Handle network or host-related errors
        # Note: In a professional tool, closed ports would be distinguished from filtered ports.
        pass
    except Exception as e:
        # Catch all other potential errors
        print(f"Error scanning port {port}: {e}")
    finally:
        s.close()

def worker(q, target_ip):
    """
    Worker function for threading. Takes ports from the queue and scans them.
    """
    while not q.empty():
        port = q.get()
        port_scan(target_ip, port)
        q.task_done()

def main():
    """
    Main function to parse arguments and initiate the scan.
    """
    parser = argparse.ArgumentParser(description="Pyscan: A simple TCP Port Scanner.")
    parser.add_argument("target", help="The target IP address or hostname (e.g., 127.0.0.1 or example.com)")
    parser.add_argument("-p1", "--start_port", type=int, default=1, help="Starting port number (default: 1)")
    parser.add_argument("-p2", "--end_port", type=int, default=1024, help="Ending port number (default: 1024)")

    args = parser.parse_args()

    # Input validation
    if args.start_port < 1 or args.end_port > 65535 or args.start_port > args.end_port:
        print("Error: Port range must be between 1 and 65535, and start_port must be less than or equal to end_port.")
        return

    # Resolve hostname to IP address
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"Error: Hostname '{args.target}' could not be resolved.")
        return

    print("=" * 50)
    print(f"Pyscan: Simple TCP Port Scanner")
    print(f"Target: {target_ip} (Host: {args.target})")
    print(f"Scanning ports {args.start_port} to {args.end_port}...")
    print(f"Scan started at: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 50)
    print(f"| Port  | Status | Service")
    print("-" * 50)

    # Initialize the queue and add ports to be scanned
    port_queue = Queue()
    for port in range(args.start_port, args.end_port + 1):
        port_queue.put(port)

    # Determine the number of threads to use
    num_threads = min(port_queue.qsize(), MAX_THREADS)

    # Create and start worker threads
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(port_queue, target_ip))
        thread.daemon = True # Allows the main program to exit even if threads are running
        thread.start()

    # Wait for all tasks in the queue to be completed
    port_queue.join()

    print("-" * 50)
    print(f"Scan finished at: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)

if __name__ == "__main__":
    main()
