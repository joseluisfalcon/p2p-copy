# p2p-copy

![p2p-copy Demo](/home/falcon/.gemini/antigravity/brain/82fd2e01-6be3-48df-a656-fa635e3756d5/p2p_copy_terminal_demo_1773906137342.png)

Secure P2P-style file transfer via intermediate storage for NAT-restricted Linux systems.

## Features

- **Local Encryption**: AES-256-GCM (authenticated encryption).
- **Multiple Providers**: `Litterbox` (default), `File.io`, `PixelDrain`, and Custom Relays.
- **Visual Progress**: Real-time progress bar for uploads/downloads.
- **Improved UX**: Visual ANSI colors, ASCII banners, and automatic command generation for recipients.

## Installation

### Linux
```bash
./install.sh
```

### Windows
```cmd
install.bat
```

## Usage

### Send a file

```bash
p2p-copy send <file_path> [--password <pass>] [--provider <name>]
```

Supported providers:
- `litterbox` (default): 1GB limit. Files expire automatically after **1 hour** (no manual delete).
- `file.io`: 2GB limit. Files are **automatically deleted** after the first download.
- `pixeldrain`: 5GB+ limit. Files expire after 30 days of inactivity.

### Custom Relay

If you have your own server that can open ports, you can use it as a relay:
```bash
p2p-copy send <file> --relay-url https://your-relay-server.com/upload
```
The relay should accept a POST request with the file and return the download URL as plain text.

### Receive a file

```bash
p2p-copy receive <url> --password <pass> [--output <path>]
```

## Security

- All files are encrypted locally with **AES-256-GCM** before upload.
- The intermediate storage server never sees the plaintext data.
- Key derivation uses **PBKDF2** with a unique salt.
