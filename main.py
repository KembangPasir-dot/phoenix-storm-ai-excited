# SPDX-License-Identifier: MIT
import os
import sys
import hashlib
import pathlib

def main():
    script_dir = pathlib.Path(__file__).resolve().parent
    source_path = script_dir / "entry.png"
    
    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir_env:
        output_dir = pathlib.Path(output_dir_env)
    else:
        output_dir = pathlib.Path("/output")
        
    dest_path = output_dir / "entry.png"
    
    if not source_path.is_file():
        print(f"Error: source missing: {source_path} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    source_bytes = source_path.read_bytes()
    
    # Validate image magic bytes
    # JPEG SOI: FF D8
    # PNG signature: 89 50 4E 47 0D 0A 1A 0A
    jpeg_magic = b'\xff\xd8'
    png_magic = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'
    
    if not (source_bytes.startswith(jpeg_magic) or source_bytes.startswith(png_magic)):
        print(f"Error: source is not a valid JPEG or PNG image (invalid magic bytes).", file=sys.stderr)
        sys.exit(1)
        
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy file and verify
    dest_path.write_bytes(source_bytes)
    
    if not dest_path.is_file():
        print(f"Error: destination file was not created: {dest_path}", file=sys.stderr)
        sys.exit(1)
        
    dest_bytes = dest_path.read_bytes()
    
    if len(dest_bytes) != len(source_bytes):
        print(f"Error: size mismatch: source size {len(source_bytes)} != dest size {len(dest_bytes)}", file=sys.stderr)
        sys.exit(1)
        
    source_hash = hashlib.sha256(source_bytes).digest()
    dest_hash = hashlib.sha256(dest_bytes).digest()
    
    if source_hash != dest_hash:
        print(f"Error: SHA-256 hash mismatch between source and destination.", file=sys.stderr)
        sys.exit(1)
        
    print(f"wrote {dest_path} ({len(dest_bytes)} bytes, sha256 {source_hash.hex()[:16]}...)")

if __name__ == "__main__":
    main()
