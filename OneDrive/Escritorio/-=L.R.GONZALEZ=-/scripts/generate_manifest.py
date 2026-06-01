
import hashlib
import json
import os
import sys

def generate_manifest(directory):
    manifest = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
                relative_path = os.path.relpath(filepath, directory)
                manifest[relative_path] = file_hash
    
    with open(os.path.join(directory, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=4)
    print(f"Manifest generated in {directory}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_manifest.py <directory>")
    else:
        generate_manifest(sys.argv[1])

