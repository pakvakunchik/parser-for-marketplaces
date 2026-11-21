from typing import Optional


async def get_photo(raw_data: dict) -> Optional[str]:
    if not isinstance(raw_data, dict):
        return None

    if raw_data.get("photoUrl"):
        return raw_data["photoUrl"]

    photo_link = raw_data.get("photo_link")
    if isinstance(photo_link, list) and photo_link:
        return photo_link[0]
    if isinstance(photo_link, str) and photo_link:
        return photo_link

    photos = raw_data.get("photos")
    if isinstance(photos, list) and photos:
        first = photos[0]
        if isinstance(first, dict):
            return first.get("url") or first.get("src")
        if isinstance(first, str):
            return first

    if raw_data.get("img"):
        return f"{raw_data['img']}0.jpg"

    return None
