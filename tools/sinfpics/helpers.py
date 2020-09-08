import config

def save_picture(img, name):
    path = config.upload_folder / f"{name}.png"
    i = 1
    while path.exists():
        path =  config.upload_folder / f"{name}_{i}.png"
        i += 1
    with path.open("wb") as f:
        f.write(img)
    return name