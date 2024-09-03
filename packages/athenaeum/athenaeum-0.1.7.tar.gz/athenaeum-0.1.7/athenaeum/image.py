def base64_to_base64(image_base64: str) -> str:
    if ',' in image_base64:
        image_type, image_base64 = image_base64.split(',')  # data:image/png;base64,...
    return image_base64
