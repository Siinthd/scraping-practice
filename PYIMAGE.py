from pytoimage import PyImage
from pathlib import Path


def pycode_to_img(filename):
    path = Path(filename)
    if not path.is_file():
        return 'No file'

    code = PyImage(filename,background=(255,255,255))

    palette = {'line':(255,0,255), 'normal':(0,0,0)}

    code.set_color_palette(palette=palette)
    code.generate_image()
    img_name = f"{filename.split('.')[0]}.png"
    code.save_image(img_name)

    return f"{img_name} saved."


if __name__ == "__main__":
    print(pycode_to_img('PYIMAGE.py'))
