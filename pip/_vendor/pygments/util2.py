
    Note that this method automatically searches the whole string (eg:
    the regular expression is wrapped in ``'^$'``)
    """
    index = text.find('\n')
    if index >= 0:
        first_line = text[:index].lower()
    else:
        first_line = text.lower()
    if first_line.startswith('#!'):
        try:
            found = [x for x in split_path_re.split(first_line[2:].strip())
                     if x and not x.startswith('-')][-1]
        except IndexError:
            return False
        regex = re.compile(rf'^{regex}(\.(exe|cmd|bat|bin))?$', re.IGNORECASE)
        if regex.search(found) is not None:
            return True
    return False


def doctype_matches(text, regex):
    """Check if the doctype matches a regular expression (if present).

    Note that this method only checks the first part of a DOCTYPE.
    eg: 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
    """
    m = doctype_lookup_re.search(text)
    if m is None:
        return False
    doctype = m.group(1)
    return re.compile(regex, re.I).match(doctype.strip()) is not None


def html_doctype_matches(text):
    """Check if the file looks like it has a html doctype."""
    return doctype_matches(text, r'html')


_looks_like_xml_cache = {}


def looks_like_xml(text):
    """Check if a doctype exists or if we have some tags."""
    if xml_decl_re.match(text):
        return True
    key = hash(text)
    try:
        return _looks_like_xml_cache[key]
    except KeyError:
        m = doctype_lookup_re.search(text)
        if m is not None:
            return True
        rv = tag_re.search(text[:1000]) is not None
        _looks_like_xml_cache[key] = rv
        return rv


def surrogatepair(c):
    """Given a unicode character code with length greater than 16 bits,
    return the two 16 bit surrogate pair.
    """
    # From example D28 of:
    # http://www.unicode.org/book/ch03.pdf
    return (0xd7c0 + (c >> 10), (0xdc00 + (c & 0x3ff)))


def format_lines(var_name, seq, raw=False, indent_level=0):
    """Formats a sequence of strings for output."""
    lines = []
    base_indent = ' ' * indent_level * 4
    inner_indent = ' ' * (indent_level + 1) * 4
    lines.append(base_indent + var_name + ' = (')
    if raw:
        # These should be preformatted reprs of, say, tuples.
        for i in seq:
            lines.append(inner_indent + i + ',')
    else:
        for i in seq:
            # Force use of single quotes
            r = repr(i + '"')
            lines.append(inner_indent + r[:-2] + r[-1] + ',')
    lines.append(base_indent + ')')
    return '\n'.join(lines)


def duplicates_removed(it, already_seen=()):
    """
    Returns a list with duplicates removed from the iterable `it`.

    Order is preserved.
    """
    lst = []
    seen = set()
    for i in it:
        if i in seen or i in already_seen:
            continue
        lst.append(i)
        seen.add(i)
    return lst


class Future:
    """Generic class to defer some work.

    Handled specially in RegexLexerMeta, to support regex string construction at
    first use.
    """
    def get(self):
        raise NotImplementedError


def guess_decode(text):
    """Decode *text* with guessed encoding.

    First try UTF-8; this should fail for non-UTF-8 encodings.
    Then try the preferred locale encoding.
    Fall back to latin-1, which always works.
    """
    try:
        text = text.decode('utf-8')
        return text, 'utf-8'
    except UnicodeDecodeError:
        try:
            import locale
            prefencoding = locale.getpreferredencoding()
            text = text.decode()
            return text, prefencoding
        except (UnicodeDecodeError, LookupError):
            text = text.decode('latin1')
            return text, 'latin1'


def guess_decode_from_terminal(text, term):
    """Decode *text* coming from terminal *term*.

    First try the terminal encoding, if given.
    Then try UTF-8.  Then try the preferred locale encoding.
    Fall back to latin-1, which always works.
    """
    if getattr(term, 'encoding', None):
        try:
            text = text.decode(term.encoding)
        except UnicodeDecodeError:
            pass
        else:
            return text, term.encoding
    return guess_decode(text)


def terminal_encoding(term):
    """Return our best guess of encoding for the given *term*."""
    if getattr(term, 'encoding', None):
        return term.encoding
    import locale
    return locale.getpreferredencoding()


class UnclosingTextIOWrapper(TextIOWrapper):
    # Don't close underlying buffer on destruction.
    def close(self):
        self.flush()
