'''
Created on Dec 15, 2010

@author: michalracek
'''

#List of functions called on when clip is created 
on_clip_created_functions = []

#List of functions called on when clip is deleted 
on_clip_deleted_functions = []


def register_on_clip_created(function):
    on_clip_created_functions.append(function) 

def register_on_clip_deleted(function):
    on_clip_deleted_functions.append(function)
    
def clip_created(clip):
    for func in on_clip_created_functions:
        func(clip)

def clip_deleted(clip):
    for func in on_clip_deleted_functions:
        func(clip)