def mask_database_url_password(url: str) -> str:
    parts = url.split(":")
    assert len(parts) == 4
    parts = parts[2].split('@')
    assert len(parts) == 2
    password = parts[0]
    updated_url = url.replace(password, "***")
    assert url != updated_url
    return updated_url
