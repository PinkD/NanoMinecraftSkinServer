def sha256(data: bytes) -> str:
    import hashlib
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()
