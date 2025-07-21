# Port Scanner

This is a simple Python-based port scanner tool. It allows you to scan a target IP address for open ports and optionally retrieve service banners from those ports.

## Features

- Scan a target IP for open ports
- Specify ports as a list (e.g., `22,80,443`) or a range (e.g., `1-1000`)
- Optionally retrieve banners from open ports
- Customizable banner request data
- Verbose output mode

## Usage

Run the scanner from the command line:

```powershell
python scanner.py -t <target_ip> -p <ports> [-g] [-b <banner>] [-v]
```

### Arguments

- `-t`, `--target` : Target IP address (required)
- `-p`, `--ports` : Ports to scan (e.g. `22,80,443` or `1-1000`) (required)
- `-g`, `--get-banner` : Get banner for open ports (optional)
- `-b`, `--banner` : Data to send in banner request (default: `hello\r\n`) (optional)
- `-v`, `--verbose` : Verbose mode (optional)

### Example

```powershell
python scanner.py -t 127.0.0.1 -p 22,80,443 -g -b "Hello\r\n" -v
```

## Requirements

- Python 3.x

## Status

## Notes

- This project uses threads for concurrency, not asyncio or async/await.
- The project is not finished yet and may be missing features or have bugs.

## License

This project is provided as-is for educational purposes.
