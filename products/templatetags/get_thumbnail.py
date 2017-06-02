from django import template

from ..models import Product, THUMB_CHOICES

register = template.Library()



@register.filter
def get_thumbnail(obj, arg):

	arg = arg.lower()
	if not isinstance(obj, Product):
		raise TyprError("This is not valid product model.")
	choices = dict(THUMB_CHOICES)
	if not choices.get(arg):
		raise TyprError("This is not a valid type for this model")
	try:
		return obj.thumbnail_set.filter(type=arg).first().media.url
	except:
		return None