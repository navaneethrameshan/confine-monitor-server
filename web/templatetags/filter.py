from django.template import Variable, VariableDoesNotExist
from django.template import Library
register = Library()

@register.filter
def hash(h, key):
        if h is None:
            return None

        elif key in h:
            return h[key]
        else:
            return None