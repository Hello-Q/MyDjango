from django import template

register = template.Library()


@register.filter
def myreplace(valu):
    myreplac = '首页:我的首1页'
    newValue = myreplac.split(':')[1]
    return "1"
