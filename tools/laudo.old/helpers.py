import config


def is_image(file):
    return file.suffix in config.image_extensions
