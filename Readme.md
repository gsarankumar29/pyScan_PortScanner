# Pyscan

Pyscan is a simple command-line TCP port scanner written in Python. Its primary purpose is to check for open TCP ports on a target host. The project is designed as a learning tool to teach network security fundamentals and how sockets work by providing a hands-on example of how services communicate over a network.

---

## Features

* **TCP Connect Scanning** — Uses the standard TCP connect (3-way handshake) to detect listening services.
* **Multi-threading** — Uses Python's `threading` and `queue` to scan multiple ports concurrently for faster results.
* **Hostname resolution** — Accepts both IP addresses (e.g. `192.168.1.1`) and hostnames (e.g. `scanme.nmap.org`).
* **Custom port range** — Lets users specify start and end ports using `-p1` and `-p2`.

---

## How Pyscan Works (Technical overview)

Pyscan performs a TCP Connect Scan using the operating system’s socket implementation:

1. **Socket creation**

   * Creates a standard `socket.socket()` with `AF_INET` (IPv4) and `SOCK_STREAM` (TCP).

2. **Handshake attempt**

   * Uses `connect_ex()` to attempt a TCP connection (initiates the TCP three-way handshake with SYN).

3. **Result interpretation**

   * If `connect_ex()` returns `0`, the handshake succeeded (SYN/ACK received) and the port is **OPEN**.
   * If it fails, the port is treated as **CLOSED** or **FILTERED** (e.g., blocked by a firewall). TCP Connect scans cannot reliably distinguish between CLOSED and FILTERED; they are both considered non-open here.

---

## Requirements

* Python 3.x (standard library only — no external packages required)

---

## Installation

No installation is necessary. The scanner is a single Python file.

1. Save the script as `port_scanner.py`.
2. Make sure you have Python 3 installed.

---

## Usage

Open a terminal and run:

```bash
python3 port_scanner.py <target> [-p1 <start_port>] [-p2 <end_port>]
```

* `<target>` — target IP address or hostname (required)
* `-p1` — starting port (optional)
* `-p2` — ending port (optional)

### Examples

Scan common ports (default behavior if your script uses defaults):

```bash
python3 port_scanner.py IP
```

Scan a custom range:

```bash
python3 port_scanner.py scanme.nmap.org -p1 1 -p2 1024
```

---

## Example Output (illustrative)

```
Target: scanme.nmap.org (IP)
Scanning ports 1 - 1024
[+] Port 22: OPEN
[+] Port 80: OPEN
[-] Port 23: CLOSED
Scan complete. Open ports: 22, 80
```

---

## Notes & Limitations

* This tool performs **TCP Connect** scans (full connect). It is straightforward, reliable, and portable, but it can be noisier than stealthier scan types.
* The scanner cannot reliably differentiate between **closed** and **filtered** ports when a connection attempt fails.
* Use this tool responsibly and only on systems you own or have explicit permission to test. Unauthorized port scanning may be illegal or violate acceptable use policies.

