# SPDX-License-Identifier: MIT
import os
import sys
import hashlib
from pathlib import Path

def main():
    script_dir = Path(__file__).resolve().parent
    source_path = script_dir / "entry.png"
    
    if not source_path.is_file():
        print(f"Error: Source image missing at {source_path}", file=sys.stderr)
        sys.exit(1)

    source_bytes = source_path.read_bytes()

    # Validate image magic bytes
    # PNG signature: 89 50 4E 47 0D 0A 1A 0A
    # JPEG SOI: FF D8
    png_sig = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"
    jpeg_sig = b"\xff\xd8"

    is_png = source_bytes.startswith(png_sig)
    is_jpeg = source_bytes.startswith(jpeg_sig)

    if not (is_png or is_jpeg):
        print(f"Error: Invalid image magic bytes in {source_path}", file=sys.stderr)
        sys.exit(1)

    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest_dir = Path(output_dir_env)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / "entry.png"

    # Copy source bytes to destination
    dest_path.write_bytes(source_bytes)

    # Verify destination size and SHA-256
    dest_bytes = dest_path.read_bytes()

    if len(dest_bytes) != len(source_bytes):
        print(f"Error: Size mismatch: source size {len(source_bytes)} vs dest size {len(dest_bytes)}", file=sys.stderr)
        sys.exit(1)

    source_hash = hashlib.sha256(source_bytes).digest()
    dest_hash = hashlib.sha256(dest_bytes).digest()

    if source_hash != dest_hash:
        print(f"Error: SHA-256 mismatch: source {source_hash.hex()} vs dest {dest_hash.hex()}", file=sys.stderr)
        sys.exit(1)

    sha256_hex = hashlib.sha256(source_bytes).hexdigest()
    print(f"wrote {dest_path} ({len(source_bytes)} bytes, sha256 {sha256_hex[:16]}...)")

if __name__ == "__main__":
    main()
