# SPDX-License-Identifier: MIT
import os
import pathlib

def main():
    script_dir = pathlib.Path(__file__).resolve().parent
    src_path = script_dir / "entry.png"
    
    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    output_dir = pathlib.Path(output_dir_env) if output_dir_env else pathlib.Path("/output")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    dst_path = output_dir / "entry.png"
    
    src_data = src_path.read_bytes()
    src_size = len(src_data)
    
    dst_path.write_bytes(src_data)
    
    dst_size = dst_path.stat().st_size
    if dst_size != src_size:
        raise RuntimeError(f"Copy size mismatch: expected {src_size}, got {dst_size}")

if __name__ == "__main__":
    main()
