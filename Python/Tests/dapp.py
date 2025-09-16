import hashlib
import json
import os
from pathlib import Path

import redis

rds = redis.Redis(host="localhost", port=6379, decode_responses=True)


def md5_hash(file_path, block_size=65536):
    hasher = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)
        code = hasher.hexdigest()
        print(code)
        return code
    except Exception as e:
        print(f"Could not hash {file_path}: {e}")
        return None


def delete_duplicates(folder):
    # Load and decode the existing Redis hash values (assumed JSON strings)
    hashes = rds.hgetall("fb:hashes")
    hashes = {f"{k}": json.loads(f"{v}") for k, v in hashes.items()}

    # Clean up paths that no longer exist
    hashes = {k: [p for p in set(v) if os.path.exists(p)] for k, v in hashes.items()}

    mesfiles = [file for files in hashes.values() for file in files]

    # Walk the folder and update hashes
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            if full_path in mesfiles:
                continue
            file_hash = md5_hash(full_path)
            if file_hash is None:
                continue
            hashes.setdefault(file_hash, []).append(full_path)

    # Save updated hashes to Redis (serialize lists as JSON strings)
    rds.hset("fb:hashes", mapping={k: json.dumps(v) for k, v in hashes.items()})

    return hashes


# Example usage
if __name__ == "__main__":
    to_path = "/home/mohamed/Documents/.Socials/Database"
    dup_path = "/home/mohamed/Documents/.Socials/Dups"
    folder_path = "/home/mohamed/Documents/.Socials/Facebook"
    for root, _, files in os.walk(folder_path):
        for file in files:
            Path(to_path, file).touch()
    hashes = delete_duplicates(folder_path)
    for hashe in hashes:
        val = hashes[hashe]
        for p in val[1:]:
            *_, fl = p.split("/")
            os.rename(p, f"{dup_path}/{fl}")
