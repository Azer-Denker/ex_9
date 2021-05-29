from django import template

register = template.Library()


@register.filter
def liked_by(obj, user):
    return obj.is_in_favorite(user)
