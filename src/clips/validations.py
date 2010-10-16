'''
Created on Oct 15, 2010

@author: michalracek
'''

#Defines default null value provided by clients
NULL = "null"

class ValidationError(Exception):
    """
    Raised in case of error during value validation.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def validate_url(value,name,required=False):
    """
    Performs validation of passed value. In case of invalid values throws
    exception.
    """
    if (not value or value == NULL) and required:
        raise ValidationError("Attribute %s is not defined but it's required." % (name))
    validate_str(value,name)
    #Check if url starts with http or https string
    if not (value.startswith("http://") or not value.startswith("https://")):
        raise ValidationError("Attribute %s with value %s does not start with http:// or https://." % (name,value))
    
   
def validate_str(value,name):
    """
    Perform validation for string property length.
    """
    if not value:
        raise ValidationError("Attribute %s is not defined but it's required." % (name))
    try:
        str(value)
    except:
        raise ValidationError("Attribute %s cannot be converted to string." % (name))
    if len(value)>=500:
        raise ValidationError("Attribute %s is too long! It could have only 500 characters." % (name))
    
def is_set(value):
    """
    Returns True in case that value is set.
    Otherwise returns false.
    """
    return (value and value != NULL)

def is_one_set(*values):
    """
    Returns true in case that at lest one of the passed values is set.
    Otherwise returns false.
    """
    for value in values:
        if is_set(value):
            return True
    raise ValidationError("One of the required values is not set!" )

        