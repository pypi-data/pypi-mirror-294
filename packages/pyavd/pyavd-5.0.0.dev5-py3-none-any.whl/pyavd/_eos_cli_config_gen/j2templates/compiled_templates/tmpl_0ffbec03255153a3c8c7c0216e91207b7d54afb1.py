from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-internet-exit.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_internet_exit = resolve('router_internet_exit')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_3((undefined(name='router_internet_exit') if l_0_router_internet_exit is missing else l_0_router_internet_exit)):
        pass
        yield '!\nrouter internet-exit\n'
        for l_1_exit_group in t_2(environment.getattr((undefined(name='router_internet_exit') if l_0_router_internet_exit is missing else l_0_router_internet_exit), 'exit_groups'), 'name'):
            _loop_vars = {}
            pass
            yield '    !\n    exit-group '
            yield str(environment.getattr(l_1_exit_group, 'name'))
            yield '\n'
            for l_2_local_connection in t_2(environment.getattr(l_1_exit_group, 'local_connections'), 'name'):
                _loop_vars = {}
                pass
                yield '        local connection '
                yield str(environment.getattr(l_2_local_connection, 'name'))
                yield '\n'
            l_2_local_connection = missing
            if t_3(environment.getattr(l_1_exit_group, 'fib_default'), True):
                pass
                yield '        fib-default\n'
        l_1_exit_group = missing
        for l_1_policy in t_2(environment.getattr((undefined(name='router_internet_exit') if l_0_router_internet_exit is missing else l_0_router_internet_exit), 'policies'), 'name'):
            _loop_vars = {}
            pass
            yield '    !\n    policy '
            yield str(environment.getattr(l_1_policy, 'name'))
            yield '\n'
            for l_2_exit_group in t_1(environment.getattr(l_1_policy, 'exit_groups'), []):
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_2_exit_group, 'name')):
                    pass
                    yield '        exit-group '
                    yield str(environment.getattr(l_2_exit_group, 'name'))
                    yield '\n'
            l_2_exit_group = missing
        l_1_policy = missing

blocks = {}
debug_info = '7=30&10=33&12=37&13=39&14=43&16=46&20=50&22=54&24=56&25=59&26=62'