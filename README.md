# p2p-copy

Secure P2P-style file transfer via intermediate storage for NAT-restricted Linux systems.

## Installation

```bash
pip install .
```

## Usage

### Send a file

```bash
p2p-copy send <file_path> [--password <pass>] [--provider <name>]
```

Supported providers: `litterbox` (default, 1GB, 1h), `file.io` (2GB), `pixeldrain` (5GB+).

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
