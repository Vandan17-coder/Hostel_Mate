from datetime import datetime, date

def format_date_filter(val, fmt=None):
    """Format datetime or date using Django-like or strftime format strings."""
    if not val:
        return ""
    if not isinstance(val, (datetime, date)):
        return str(val)

    if not fmt or fmt == "M d, Y":
        return val.strftime("%b %d, %Y")
    elif fmt == "M d, Y • h:i A":
        if isinstance(val, datetime):
            return val.strftime("%b %d, %Y • %I:%M %p")
        return val.strftime("%b %d, %Y")
    elif fmt == "M d, H:i":
        if isinstance(val, datetime):
            return val.strftime("%b %d, %H:%M")
        return val.strftime("%b %d")
    elif fmt == "M d":
        return val.strftime("%b %d")
    elif fmt == "M Y":
        return val.strftime("%b %Y")
    elif "%" in fmt:
        return val.strftime(fmt)
    else:
        # Fallback basic mapping
        py_fmt = fmt.replace("M", "%b").replace("d", "%d").replace("Y", "%Y").replace("h", "%I").replace("i", "%M").replace("A", "%p").replace("H", "%H")
        try:
            return val.strftime(py_fmt)
        except Exception:
            return val.strftime("%b %d, %Y")

def truncatewords_filter(text, num):
    """Truncate a string after a certain number of words."""
    if not text:
        return ""
    words = str(text).split()
    if len(words) <= int(num):
        return str(text)
    return " ".join(words[:int(num)]) + "..."

def slice_filter(val, s):
    """Slice string or sequence using Python slice notation e.g. ':1'."""
    if not val:
        return ""
    if isinstance(s, str) and ":" in s:
        parts = s.split(":")
        start = int(parts[0]) if parts[0] else None
        end = int(parts[1]) if len(parts) > 1 and parts[1] else None
        return val[start:end]
    return val

def make_list_filter(val):
    """Convert string/iterable to list."""
    if val is None:
        return []
    return list(val)

def register_filters(app):
    app.jinja_env.filters['date'] = format_date_filter
    app.jinja_env.filters['truncatewords'] = truncatewords_filter
    app.jinja_env.filters['slice'] = slice_filter
    app.jinja_env.filters['make_list'] = make_list_filter
