from django import template
import calendar
register = template.Library()

@register.filter
def monthify(value):
	return calendar.month_name[value]

