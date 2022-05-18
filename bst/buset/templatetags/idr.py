from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
register = template.Library()
def currency(IDR):
    idr = round(float(IDR), 2)
    return "Rp. %s%s" % (intcomma(int(IDR)), ("%0.2f" % IDR)[-3:])
register.filter('currency', currency)    