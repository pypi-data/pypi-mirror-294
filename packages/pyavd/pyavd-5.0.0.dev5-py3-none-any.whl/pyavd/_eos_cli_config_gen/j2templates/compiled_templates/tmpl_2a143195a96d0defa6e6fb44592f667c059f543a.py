from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/monitor-connectivity.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_monitor_connectivity = resolve('monitor_connectivity')
    l_0_local_interfaces_cli = resolve('local_interfaces_cli')
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
    if t_3((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity)):
        pass
        yield '!\nmonitor connectivity\n'
        if t_3(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'interval')):
            pass
            yield '   interval '
            yield str(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'interval'))
            yield '\n'
        if t_3(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'shutdown'), False):
            pass
            yield '   no shutdown\n'
        elif t_3(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'shutdown'), True):
            pass
            yield '   shutdown\n'
        for l_1_interface_set in t_2(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'interface_sets'), 'name'):
            _loop_vars = {}
            pass
            if (t_3(environment.getattr(l_1_interface_set, 'name')) and t_3(environment.getattr(l_1_interface_set, 'interfaces'))):
                pass
                yield '   interface set '
                yield str(environment.getattr(l_1_interface_set, 'name'))
                yield ' '
                yield str(environment.getattr(l_1_interface_set, 'interfaces'))
                yield '\n'
        l_1_interface_set = missing
        if t_3(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'local_interfaces')):
            pass
            l_0_local_interfaces_cli = str_join(('local-interfaces ', environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'local_interfaces'), ))
            context.vars['local_interfaces_cli'] = l_0_local_interfaces_cli
            context.exported_vars.add('local_interfaces_cli')
            if t_1(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'address_only'), True):
                pass
                l_0_local_interfaces_cli = str_join(((undefined(name='local_interfaces_cli') if l_0_local_interfaces_cli is missing else l_0_local_interfaces_cli), ' address-only', ))
                context.vars['local_interfaces_cli'] = l_0_local_interfaces_cli
                context.exported_vars.add('local_interfaces_cli')
            yield '   '
            yield str((undefined(name='local_interfaces_cli') if l_0_local_interfaces_cli is missing else l_0_local_interfaces_cli))
            yield ' default\n'
        for l_1_host in t_2(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'hosts'), 'name'):
            l_1_local_interfaces_cli = l_0_local_interfaces_cli
            _loop_vars = {}
            pass
            if t_3(environment.getattr(l_1_host, 'name')):
                pass
                yield '   !\n   host '
                yield str(environment.getattr(l_1_host, 'name'))
                yield '\n'
                if t_3(environment.getattr(l_1_host, 'description')):
                    pass
                    yield '      description\n      '
                    yield str(environment.getattr(l_1_host, 'description'))
                    yield '\n'
                if t_3(environment.getattr(l_1_host, 'local_interfaces')):
                    pass
                    l_1_local_interfaces_cli = str_join(('local-interfaces ', environment.getattr(l_1_host, 'local_interfaces'), ))
                    _loop_vars['local_interfaces_cli'] = l_1_local_interfaces_cli
                    if t_1(environment.getattr(l_1_host, 'address_only'), True):
                        pass
                        l_1_local_interfaces_cli = str_join(((undefined(name='local_interfaces_cli') if l_1_local_interfaces_cli is missing else l_1_local_interfaces_cli), ' address-only', ))
                        _loop_vars['local_interfaces_cli'] = l_1_local_interfaces_cli
                    yield '      '
                    yield str((undefined(name='local_interfaces_cli') if l_1_local_interfaces_cli is missing else l_1_local_interfaces_cli))
                    yield '\n'
                if t_3(environment.getattr(l_1_host, 'ip')):
                    pass
                    yield '      ip '
                    yield str(environment.getattr(l_1_host, 'ip'))
                    yield '\n'
                if t_3(environment.getattr(l_1_host, 'url')):
                    pass
                    yield '      url '
                    yield str(environment.getattr(l_1_host, 'url'))
                    yield '\n'
        l_1_host = l_1_local_interfaces_cli = missing
        for l_1_vrf in t_2(environment.getattr((undefined(name='monitor_connectivity') if l_0_monitor_connectivity is missing else l_0_monitor_connectivity), 'vrfs'), 'name'):
            l_1_local_interfaces_cli = l_0_local_interfaces_cli
            _loop_vars = {}
            pass
            if t_3(environment.getattr(l_1_vrf, 'name')):
                pass
                yield '   vrf '
                yield str(environment.getattr(l_1_vrf, 'name'))
                yield '\n'
                for l_2_interface_set in t_2(environment.getattr(l_1_vrf, 'interface_sets'), 'name'):
                    _loop_vars = {}
                    pass
                    if (t_3(environment.getattr(l_2_interface_set, 'name')) and t_3(environment.getattr(l_2_interface_set, 'interfaces'))):
                        pass
                        yield '      interface set '
                        yield str(environment.getattr(l_2_interface_set, 'name'))
                        yield ' '
                        yield str(environment.getattr(l_2_interface_set, 'interfaces'))
                        yield '\n'
                l_2_interface_set = missing
                if t_3(environment.getattr(l_1_vrf, 'local_interfaces')):
                    pass
                    l_1_local_interfaces_cli = str_join(('local-interfaces ', environment.getattr(l_1_vrf, 'local_interfaces'), ))
                    _loop_vars['local_interfaces_cli'] = l_1_local_interfaces_cli
                    if t_1(environment.getattr(l_1_vrf, 'address_only'), True):
                        pass
                        l_1_local_interfaces_cli = str_join(((undefined(name='local_interfaces_cli') if l_1_local_interfaces_cli is missing else l_1_local_interfaces_cli), ' address-only', ))
                        _loop_vars['local_interfaces_cli'] = l_1_local_interfaces_cli
                    yield '      '
                    yield str((undefined(name='local_interfaces_cli') if l_1_local_interfaces_cli is missing else l_1_local_interfaces_cli))
                    yield ' default\n'
                if t_3(environment.getattr(l_1_vrf, 'description')):
                    pass
                    yield '      description\n      '
                    yield str(environment.getattr(l_1_vrf, 'description'))
                    yield '\n'
                for l_2_host in t_2(environment.getattr(l_1_vrf, 'hosts'), 'name'):
                    l_2_local_interfaces_cli = l_1_local_interfaces_cli
                    _loop_vars = {}
                    pass
                    if t_3(environment.getattr(l_2_host, 'name')):
                        pass
                        yield '      !\n      host '
                        yield str(environment.getattr(l_2_host, 'name'))
                        yield '\n'
                        if t_3(environment.getattr(l_2_host, 'description')):
                            pass
                            yield '         description\n         '
                            yield str(environment.getattr(l_2_host, 'description'))
                            yield '\n'
                        if t_3(environment.getattr(l_2_host, 'local_interfaces')):
                            pass
                            l_2_local_interfaces_cli = str_join(('local-interfaces ', environment.getattr(l_2_host, 'local_interfaces'), ))
                            _loop_vars['local_interfaces_cli'] = l_2_local_interfaces_cli
                            if t_1(environment.getattr(l_2_host, 'address_only'), True):
                                pass
                                l_2_local_interfaces_cli = str_join(((undefined(name='local_interfaces_cli') if l_2_local_interfaces_cli is missing else l_2_local_interfaces_cli), ' address-only', ))
                                _loop_vars['local_interfaces_cli'] = l_2_local_interfaces_cli
                            yield '         '
                            yield str((undefined(name='local_interfaces_cli') if l_2_local_interfaces_cli is missing else l_2_local_interfaces_cli))
                            yield '\n'
                        if t_3(environment.getattr(l_2_host, 'ip')):
                            pass
                            yield '         ip '
                            yield str(environment.getattr(l_2_host, 'ip'))
                            yield '\n'
                        if t_3(environment.getattr(l_2_host, 'url')):
                            pass
                            yield '         url '
                            yield str(environment.getattr(l_2_host, 'url'))
                            yield '\n'
                l_2_host = l_2_local_interfaces_cli = missing
        l_1_vrf = l_1_local_interfaces_cli = missing

blocks = {}
debug_info = '7=31&10=34&11=37&13=39&15=42&18=45&19=48&20=51&23=56&24=58&25=61&26=63&28=67&30=69&31=73&33=76&34=78&36=81&38=83&39=85&40=87&41=89&43=92&45=94&46=97&48=99&49=102&53=105&54=109&55=112&56=114&57=117&58=120&61=125&62=127&63=129&64=131&66=134&68=136&70=139&72=141&73=145&75=148&76=150&78=153&80=155&81=157&82=159&83=161&85=164&87=166&88=169&90=171&91=174'