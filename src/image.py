'''
Created on Oct 10, 2010

@author: michalracek
'''
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import images
from dbo import Image

TINY_IMAGE_HEIGHT = 296;
TINY_IMAGE_WIDTH = 296;

SMALL_IMAGE_HEIGHT = TINY_IMAGE_HEIGHT * 2;
SMALL_IMAGE_WIDTH = TINY_IMAGE_HEIGHT * 2;

def thumbnail(url=None):
    image_do = Image()
    image_do.url = url
    image = __downloadImage(url)
    if image:
        __to_thumbnail(image,image_do)
    image_do.put()
    return image_do

def __downloadImage(url=None):
    try:
        result = urlfetch.fetch(url=url)
        if result.status_code == 200:
            return result.content
        else:
            return None
    except:
        return None 


def __to_thumbnail(image,image_do):
    img_tiny = images.Image(image)
    img_tiny.resize(width=TINY_IMAGE_WIDTH,height=TINY_IMAGE_HEIGHT)
    tiny = img_tiny.execute_transforms(output_encoding=images.JPEG)
    image_do.tiny = db.Blob(tiny)
    
    img_small = images.Image(image)
    img_small.resize(width=SMALL_IMAGE_WIDTH,height=SMALL_IMAGE_HEIGHT)
    small = img_small.execute_transforms(output_encoding=images.JPEG)
    image_do.small =  db.Blob(small)


