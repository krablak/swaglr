'''
Created on Oct 15, 2010

@author: michalracek
'''

import cgi

#Defines default null value provided by clients
NULL = "null"
#Maximal allowed length of input values.
MAX_LEN = 500;

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
        raise ValidationError("Attribute '%s' is not defined but it's required." % (name))
    validate_str(value,name)
    #Check if url starts with http or https string
    if not (value.startswith("http://") or not value.startswith("https://")):
        raise ValidationError("Attribute '%s' with value '%s' does not start with http:// or https://." % (name,value))
    
   
def validate_str(value,name):
    """
    Perform validation for string property length.
    """
    if not value or value == NULL:
        raise ValidationError("Attribute '%s' is not defined but it's required." % (name))
    try:
        unicode(value)
    except:
        raise ValidationError("Attribute '%s' cannot be converted to unicode." % (name))
    if len(value)>=MAX_LEN:
        raise ValidationError("Attribute '%s' is too long! It could have only 500 characters." % (name))
    
def validate_null(value,name):
    """
    Checks if the value is not set.
    """
    if value and value != NULL:
        raise ValidationError("Attribute '%s' is defined but should be not set." % (name))
    
    
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

def is_one_of_them(value,allowed):
    """
    Checks if value equals to one of the values.
    """
    if not value in allowed:
        raise ValidationError("Value '%s' is not in allowed values '%s'."  % (value,allowed))

def validate_int(value,name):
    """
    Perform validation for required integer property.
    """
    if not value:
        raise ValidationError("Attribute '%s' is not defined but it's required." % (name))
    try:
        str(value)
    except:
        raise ValidationError("Attribute '%s' cannot be converted to int." % (name))


def to_param(value,not_null=False,escape=True):
    """
    Helper function for update of the input values into clips API allowed style.
    """       
    if not value:
        if not_null:
            value = NULL
        else:
            value = ""
    else:
        if escape:
            value = cgi.escape(value)
        value = unicode(value)
        if len(value)>MAX_LEN:
            value = value[:499]
        value = value.replace('\n',' ').replace('\t',' ')
    return value


def to_int_param(value):
    """
    Helper function for update of the input values into clips API allowed style.
    """       
    if not value:
        value = 0
    else:
        try:
            value = int(value)
        except:
            value = 0
    return value 