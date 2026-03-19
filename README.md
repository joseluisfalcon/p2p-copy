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

Supported providers: `file.io` (default, 2GB), `transfer.sh` (10GB).

### Receive a file

```bash
p2p-copy receive <url> --password <pass> [--output <path>]
```

## Security

- All files are encrypted locally with **AES-256-GCM** before upload.
- The intermediate storage server never sees the plaintext data.
- Key derivation uses **PBKDF2** with a unique salt.
