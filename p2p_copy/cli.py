import argparse
import os
import sys
import getpass
import requests
from .encryptor import encrypt_file, decrypt_file
from .providers import get_provider

def print_progress(current, total):
    """Simple text-based progress bar."""
    bar_length = 40
    progress = current / total
    arrow = "=" * int(round(progress * bar_length) - 1) + ">"
    spaces = " " * (bar_length - len(arrow))
    sys.stdout.write(f"\rProgress: [{arrow}{spaces}] {int(progress * 100)}% ({current}/{total} bytes)")
    sys.stdout.flush()
    if current >= total:
        print()

def handle_send(args):
    """Handle the 'send' command."""
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

    password = args.password
    if not password:
        password = getpass.getpass("Enter encryption password: ")

    encrypted_file = args.file + ".enc"
    print(f"Encrypting '{args.file}'...")
    try:
        encrypt_file(args.file, encrypted_file, password)
        print(f"Uploading to {args.provider}...")
        
        if args.relay_url:
            from .providers import CustomRelayProvider
            provider = CustomRelayProvider(args.relay_url)
        else:
            provider = get_provider(args.provider)
            
        url = provider.upload(encrypted_file, progress_callback=print_progress)
        print(f"\nUpload complete!")
        print(f"Share this URL with the recipient: {url}")
    except Exception as e:
        print(f"Error during send: {e}")
        sys.exit(1)
    finally:
        if os.path.exists(encrypted_file):
            os.remove(encrypted_file)

def handle_receive(args):
    """Handle the 'receive' command."""
    password = args.password
    if not password:
        password = getpass.getpass("Enter decryption password: ")

    temp_enc_file = "download.enc"
    print(f"Downloading from {args.url}...")
    try:
        response = requests.get(args.url, stream=True)
        if response.status_code != 200:
            print(f"Error: Download failed (HTTP {response.status_code})")
            sys.exit(1)

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        with open(temp_enc_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        print_progress(downloaded, total_size)

        output_path = args.output or "received_file"
        print(f"\nDecrypting to '{output_path}'...")
        decrypt_file(temp_enc_file, output_path, password)
        print("\nSuccess! File received and decrypted.")
    except Exception as e:
        print(f"Error during receive: {e}")
        sys.exit(1)
    finally:
        if os.path.exists(temp_enc_file):
            os.remove(temp_enc_file)

def main():
    parser = argparse.ArgumentParser(description="p2p-copy: Secure P2P-style file transfer via intermediate storage.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Send command
    send_parser = subparsers.add_parser("send", help="Encrypt and upload a file")
    send_parser.add_argument("file", help="Path to the file to send")
    send_parser.add_argument("--provider", default="litterbox", choices=["file.io", "pixeldrain", "litterbox"], help="Storage provider")
    send_parser.add_argument("--relay-url", help="Custom relay URL (overrides --provider)")
    send_parser.add_argument("--password", help="Encryption password (optional, will prompt if not provided)")

    # Receive command
    receive_parser = subparsers.add_parser("receive", help="Download and decrypt a file")
    receive_parser.add_argument("url", help="URL of the encrypted file")
    receive_parser.add_argument("--output", help="Path to save the decrypted file")
    receive_parser.add_argument("--password", help="Decryption password (optional, will prompt if not provided)")

    args = parser.parse_args()

    if args.command == "send":
        handle_send(args)
    elif args.command == "receive":
        handle_receive(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
