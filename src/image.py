'''
Created on Oct 10, 2010

@author: michalracek
'''
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import images
from dbo import Image
import logging

TINY_IMAGE_HEIGHT = 280;
TINY_IMAGE_WIDTH = 280;

def thumbnail(url=None):
    logging.debug("Thumbnail start")
    image_do = Image()
    image_do.url = url
    image = __downloadImage(url)
    if image:
        __to_thumbnail(image,image_do)
    else:
        logging.debug("Image was not downloaded.")
    image_do.put()
    logging.debug("Thumbnail end")
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
    __log_image(img_tiny)
    resized = False
    #Check if the image is large and should be resized
    if img_tiny.width > TINY_IMAGE_WIDTH:
        img_tiny.resize(width=TINY_IMAGE_WIDTH)
        resized = True
        logging.debug("Image was is large and will be resized.")
    else:
        logging.debug("Image was is not large and will be not resized.")
    if resized:
        tiny = img_tiny.execute_transforms(output_encoding=images.JPEG)
        image_do.tiny = db.Blob(tiny)
    else:        
        image_do.tiny = db.Blob(image)
    
def __is_large(image):
    """
    Checks if image should be resized. One of the sizes is bigger than thumbnail dimensions.
    """
    return image.height > TINY_IMAGE_HEIGHT or image.width > TINY_IMAGE_WIDTH
    
def __is_vertical(image):
    """
    Helper method checks if the image should by resized by height.
    """
    return image.height > image.width

def __is_horizontal(image):
    """
    Helper method checks if the image should by resized by width.
    """
    return image.width > image.height

def __log_image(image):
    """
    Helper method for logging all details about processe image.
    """
    logging.debug("Image size %s x %s " % (image.height,image.width))

