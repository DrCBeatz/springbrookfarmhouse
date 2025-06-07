# core/templatetags/nav.py
import re
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_active(context, pattern):
    """
    Return 'active text-white' if the current view_name matches *pattern*,
    otherwise 'text-light'.

    *pattern* can be:
      • a full view name   →  "store:producer_list"
      • a regex/prefix     →  r"store:producer_.*"
    """
    view_name = context["request"].resolver_match.view_name
    if re.fullmatch(pattern, view_name):
        return "active text-white"
    return "text-light"