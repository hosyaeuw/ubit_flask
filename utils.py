import os
import re
from app import app

from transliterate import translit
from werkzeug.utils import secure_filename
from PIL import Image


def get_img_link(link):
    return os.path.join(app.config['UPLOAD_FOLDER'], link)


def crop_img(im):
    width, height = im.size
    need_width, need_height = (400, 250)
    top = (height - need_height) / 2
    left = (width - need_height) / 2
    return im.crop((left, top, left + need_width, height - need_height))


def image_preparation(img):
    img_filename = translit_filename(img.filename)
    # size = 592, 864
    im = Image.open(img.stream)
    # im.thumbnail(size, Image.ANTIALIAS)
    # im.convert('RGB')
    # im = crop_img(im)
    img_filename = f'{img_filename}.webp'
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
    im.save(img_path, 'webp')
    return img_filename


def translit_filename(filename):
    refactor_filename = ''.join(filename.split('.')[:-1])
    filename = translit(refactor_filename, 'ru', reversed=True)
    template = r'[^\w+]'
    filename = re.sub(template, '', filename)
    filename = secure_filename(filename)
    return filename
