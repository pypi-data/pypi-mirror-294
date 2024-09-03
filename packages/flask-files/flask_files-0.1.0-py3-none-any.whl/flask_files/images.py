from PIL import Image
from werkzeug.datastructures import FileStorage
from io import BytesIO
import os


IMAGE_EXTS = tuple('jpg jpe jpeg png gif svg bmp webp'.split())
IMAGE_EXT_FORMAT_MAP = {"jpg": "jpeg"}


def resize_img(file, w=None, h=None, resample=None):
    img = open_img(file)

    keep_ratio = False
    try:
        w, h = get_size(w, h)
    except:
        size = get_size(w, h, img.size)
        keep_ratio = True

    if keep_ratio:
        img.thumbnail(size, resample)
    else:
        img = img.resize(size, resample)

    return _save_image(img, file, f"-{w}x{h}")


def create_thumbnail(file, w=None, h=None, resample=None):
    img = open_img(file)

    fixed_size = False
    try:
        size = get_size(w, h)
        fixed_size = True
    except:
        size = get_size(w, h, img.size)

    if fixed_size and size[0] < img.size[0] and size[1] < img.size[1]:
        r = max(float(size[0]) / float(img.size[0]), float(size[1]) / float(img.size[1]))
        isize = (int(img.size[0] * r), int(img.size[1] * r))
        img = img.resize(isize, resample)
        x = max((isize[0] - size[0]) / 2, 0)
        y = max((isize[1] - size[1]) / 2, 0)
        img = img.crop((x, y, size[0], size[1]))
    else:
        img.thumbnail(size, resample)

    return _save_image(img, file, f"-thumb-{w}x{h}")


def crop_img(file, x, y, w, h):
    img = open_img(file)
    img = img.crop((x, y, w, h))
    return _save_image(img, file, "-cropped")


def rotate_img(file, angle, resample=0, expand=0):
    img = open_img(file)
    img = img.rotate(float(angle), resample, expand)
    return _save_image(img, file, "-rotated")


def transpose_img(file, method):
    if isinstance(method, str):
        method = {"flip_left_right": Image.FLIP_LEFT_RIGHT,
                    "flip_top_bottom": Image.FLIP_TOP_BOTTOM,
                    "rotate90": Image.ROTATE_90,
                    "rotate180": Image.ROTATE_180,
                    "rotate270": Image.ROTATE_270}[method.lower()]
    img = open_img(file)
    img = img.transpose(method)
    return _save_image(img, file, "-transposed")


def watermark_img(file, watermark, x=None, y=None):
    img = open_img(file)
    wtmk = Image.open(watermark)
    iw, ih = img.size
    ww, wh = wtmk.size
    img.paste(wtmk, (x or (iw - ww), y or (ih - wh)))
    wtmk.close()
    return _save_image(img, file, "-watermark")


def open_img(file):
    fp = BytesIO()
    file.save(fp)
    return Image.open(fp)


def _save_image(img, file, suffix=None):
    filename = file.filename
    path, ext = os.path.splitext(filename)
    if suffix:
        filename = path + suffix + ext
    file = FileStorage(filename=filename, content_type=file.mimetype)
    img.save(file.stream, IMAGE_EXT_FORMAT_MAP.get(ext[1:].lower(), ext[1:]))
    file.stream.seek(0)
    return file


def get_size(w, h, ratio=None):
    if ((w is None or h is None) and not ratio) or (w is None and h is None):
        raise Exception("Missing size options for image manipulation")
    if w is None:
        r = float(h) / float(ratio[1])
        w = int(ratio[0] * r)
    elif h is None:
        r = float(w) / float(ratio[0])
        h = int(ratio[1] * r)
    return w, h