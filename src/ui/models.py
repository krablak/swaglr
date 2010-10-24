'''
Created on Oct 12, 2010

@author: michalracek
'''
from datetime import date

def to_day_clips(clips):
    """
    Creates page model from list of clips.
    """
    #Clips model divided to day based dict
    days_model = {}
    #Go over each clip and add it into days model according to humanized date.
    for clip in clips:
        #Create humanized date string
        str_date = __to_humanized_date(clip.date)
        #Check if model has record for this date.
        if not days_model.has_key(str_date):
            days_model[str_date] = []
        #Append clip into model by date
        days_model[str_date].append(clip)
    #Covert to list- due to Django templates 0.96 which is not able to iterate over dict :(
    days_model_list = []
    for day in days_model.keys():
        days_model_list.insert(0,{'day':day , 'clips': days_model[day]})    
    return days_model_list

def __to_page_clip(clip):
    return None


UNKNOWN_DATE_TEXT = "in the year one";
def __to_humanized_date(robotic_date):
    """
    Converts date time into human readable string.
    """
    if date:
        try:
            delta = date(robotic_date.year, robotic_date.month, robotic_date.day) - date.today()
            days = delta.days
            if days == 0:
                return "today"
            if days == -1:
                return "yesterday"
            else:
                return robotic_date.strftime("%d.%m")
        except AttributeError:
            pass
        except ValueError:
            pass
    return UNKNOWN_DATE_TEXT
