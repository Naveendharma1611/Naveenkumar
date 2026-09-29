import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdown(text):
    """Renders admin-authored Markdown (tables, fenced code) to HTML."""
    return mark_safe(md.markdown(text or "", extensions=["fenced_code", "tables", "sane_lists"]))


@register.filter
def split(value, sep=","):
    """'a, b,c' -> ['a', 'b', 'c']; sep 'lines' splits on newlines."""
    parts = (value or "").splitlines() if sep == "lines" else (value or "").split(sep)
    return [p.strip() for p in parts if p.strip()]


@register.simple_tag(takes_context=True)
def query(context, **kwargs):
    """Current query string with some params replaced, for filters and pagination links."""
    params = context["request"].GET.copy()
    for key, val in kwargs.items():
        if val in (None, ""):
            params.pop(key, None)
        else:
            params[key] = val
    if "page" not in kwargs:
        params.pop("page", None)
    return "?" + params.urlencode() if params else "?"
