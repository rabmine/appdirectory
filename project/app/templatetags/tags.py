from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='truncate')
@stringfilter
def trunc(value, size):
    trunc_size = int(size)
    return value[:trunc_size - 3:] + "..."

@register.filter(name='format_sentence')
@stringfilter
def format_sentence(value):
    value = value.lower()
    sentences = value.split(".")
    sentences = [sentence and (sentence[0].upper() + sentence[1:]) for sentence in sentences]
    return ".".join(sentences)

register.filter('truncate', trunc)
register.filter('format_sentence', format_sentence)