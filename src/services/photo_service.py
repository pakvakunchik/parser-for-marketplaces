async def get_photo(raw_data):
    base_photo = raw_data['photoUrl']
    photo = raw_data.get('photo_link')
    if isinstance(photo, list):
        photo = photo[0]
    elif raw_data.get('base_photo_url'):
        photo = f"{raw_data['img']}0.jpg"
    else:
        photo = None