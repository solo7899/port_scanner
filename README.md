# Port Scanner

A simple Python port scanner that scans for open ports on a target host.  
**This project is currently unfinished and under development.**

## Features

- Scan single ports, comma-separated lists, or port ranges (e.g. `22,80,443` or `1-1000`)
- Multi-threaded scanning for faster results
- Optional banner grabbing for open ports
- Verbose output option

## Usage

```sh
python scanner.py -t <target_ip> -p <ports> [options]
```

### Arguments

- `-t`, `--target` (required): Target IP address (e.g. `127.0.0.1`)
- `-p`, `--ports` (required): Ports to scan (e.g. `22,80,443` or `1-1000`)
- `-g`, `--get-banner`: Try to grab banners from open ports
- `-b`, `--banner`: Data to send for banner grabbing (default: `hello\r\n`)
- `-v`, `--verbose`: Enable verbose output

### Example

```sh
python scanner.py -t 127.0.0.1 -p 22,80,443 -g -v
```

## How it works

- Uses Python threads for concurrent port scanning.
- Uses blocking sockets (not asyncio).
- Results are collected in a thread-safe queue and printed after scanning.

## Notes

- **This project is not finished yet.**
- Only supports TCP port scanning.
- No async/await or asyncio is used; all concurrency is via threads.
- Error handling and input validation are basic and may be improved in future versions.
