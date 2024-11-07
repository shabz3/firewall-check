                raise NotImplementedError('op not implemented: %s' % op)
            elhs = expr['lhs']
            erhs = expr['rhs']
            if _is_literal(expr['lhs']) and _is_literal(expr['rhs']):
                raise SyntaxError('invalid comparison: %s %s %s' % (elhs, op, erhs))

            lhs = self.evaluate(elhs, context)
            rhs = self.evaluate(erhs, context)
            if ((_is_version_marker(elhs) or _is_version_marker(erhs)) and
                    op in ('<', '<=', '>', '>=', '===', '==', '!=', '~=')):
                lhs = LV(lhs)
                rhs = LV(rhs)
            elif _is_version_marker(elhs) and op in ('in', 'not in'):
                lhs = LV(lhs)
                rhs = _get_versions(rhs)
            result = self.operations[op](lhs, rhs)
        return result


_DIGITS = re.compile(r'\d+\.\d+')


def default_context():

    def format_full_version(info):
        version = '%s.%s.%s' % (info.major, info.minor, info.micro)
        kind = info.releaselevel
        if kind != 'final':
            version += kind[0] + str(info.serial)
        return version

    if hasattr(sys, 'implementation'):
        implementation_version = format_full_version(sys.implementation.version)
        implementation_name = sys.implementation.name
    else:
        implementation_version = '0'
        implementation_name = ''

    ppv = platform.python_version()
    m = _DIGITS.match(ppv)
    pv = m.group(0)
    result = {
        'implementation_name': implementation_name,
        'implementation_version': implementation_version,
        'os_name': os.name,
        'platform_machine': platform.machine(),
        'platform_python_implementation': platform.python_implementation(),
        'platform_release': platform.release(),
        'platform_system': platform.system(),
        'platform_version': platform.version(),
        'platform_in_venv': str(in_venv()),
        'python_full_version': ppv,
        'python_version': pv,
        'sys_platform': sys.platform,
    }
    return result


DEFAULT_CONTEXT = default_context()
del default_context

evaluator = Evaluator()


def interpret(marker, execution_context=None):
    """
    Interpret a marker and return a result depending on environment.

    :param marker: The marker to interpret.
    :type marker: str
    :param execution_context: The context used for name lookup.
    :type execution_context: mapping
    """
    try:
        expr, rest = parse_marker(marker)
    except Exception as e:
        raise SyntaxError('Unable to interpret marker syntax: %s: %s' % (marker, e))
    if rest and rest[0] != '#':
        raise SyntaxError('unexpected trailing data in marker: %s: %s' % (marker, rest))
    context = dict(DEFAULT_CONTEXT)
    if execution_context:
        context.update(execution_context)
    return evaluator.evaluate(expr, context)