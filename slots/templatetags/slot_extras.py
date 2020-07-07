from django import template

register = template.Library()

@register.filter(name='has_user')
def has_user(shop, user):
    """Evaluates whether user owns a slot in given shop."""
    return bool(shop.slot_set.filter(user=user))


@register.filter(name='var_property')
def var_property(obj, value):
    return None if value not in obj else obj[value]