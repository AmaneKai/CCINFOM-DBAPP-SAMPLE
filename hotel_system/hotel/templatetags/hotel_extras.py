from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def peso(amount):
    return f'₱{floatformat(amount, 0)}'


@register.filter
def php(amount):
    # xhtml2pdf's built-in Helvetica font has no glyph for the peso sign,
    # so PDF output spells out the currency code instead of using "peso".
    return f'PHP {floatformat(amount, 0)}'
