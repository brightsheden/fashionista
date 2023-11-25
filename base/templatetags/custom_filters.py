from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='format_details')
@stringfilter
def format_details(value):
    details = value.split('<br>')
    formatted_details = ' '.join(details)  # replace ' ' with '\n' for newline
    return formatted_details
