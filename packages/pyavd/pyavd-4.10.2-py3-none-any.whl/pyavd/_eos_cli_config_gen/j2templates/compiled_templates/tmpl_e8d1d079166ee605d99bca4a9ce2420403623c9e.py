from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/event-handlers.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_event_handlers = resolve('event_handlers')
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
        t_3 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_4 = environment.filters['replace']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'replace' found.")
    try:
        t_5 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_5((undefined(name='event_handlers') if l_0_event_handlers is missing else l_0_event_handlers)):
        pass
        yield '\n### Event Handler\n\n#### Event Handler Summary\n\n| Handler | Actions | Trigger | Trigger Config |\n| ------- | ------- | ------- | -------------- |\n'
        for l_1_handler in t_2((undefined(name='event_handlers') if l_0_event_handlers is missing else l_0_event_handlers), 'name'):
            l_1_actions = resolve('actions')
            l_1_action = resolve('action')
            l_1_bash_command = resolve('bash_command')
            l_1_metric = resolve('metric')
            l_1_trigger_cli = resolve('trigger_cli')
            l_1_on_maintenance_cli = resolve('on_maintenance_cli')
            l_1_trigger_config = resolve('trigger_config')
            _loop_vars = {}
            pass
            if t_5(environment.getattr(l_1_handler, 'action_type')):
                pass
                l_1_actions = environment.getattr(l_1_handler, 'action_type')
                _loop_vars['actions'] = l_1_actions
                if t_5(environment.getattr(l_1_handler, 'action')):
                    pass
                    l_1_action = t_4(context.eval_ctx, environment.getattr(l_1_handler, 'action'), '|', '\\|')
                    _loop_vars['action'] = l_1_action
                    l_1_actions = str_join(((undefined(name='actions') if l_1_actions is missing else l_1_actions), ' <code>', (undefined(name='action') if l_1_action is missing else l_1_action), '</code>', ))
                    _loop_vars['actions'] = l_1_actions
            if t_5(environment.getattr(l_1_handler, 'actions')):
                pass
                l_1_actions = []
                _loop_vars['actions'] = l_1_actions
                if t_5(environment.getattr(environment.getattr(l_1_handler, 'actions'), 'bash_command')):
                    pass
                    l_1_bash_command = t_4(context.eval_ctx, t_4(context.eval_ctx, environment.getattr(environment.getattr(l_1_handler, 'actions'), 'bash_command'), '\n', '\\n'), '|', '\\|')
                    _loop_vars['bash_command'] = l_1_bash_command
                    l_1_bash_command = str_join(('<code>', (undefined(name='bash_command') if l_1_bash_command is missing else l_1_bash_command), '</code>', ))
                    _loop_vars['bash_command'] = l_1_bash_command
                    l_1_bash_command = str_join(('bash ', (undefined(name='bash_command') if l_1_bash_command is missing else l_1_bash_command), ))
                    _loop_vars['bash_command'] = l_1_bash_command
                    context.call(environment.getattr((undefined(name='actions') if l_1_actions is missing else l_1_actions), 'append'), (undefined(name='bash_command') if l_1_bash_command is missing else l_1_bash_command), _loop_vars=_loop_vars)
                elif t_5(environment.getattr(environment.getattr(l_1_handler, 'actions'), 'log')):
                    pass
                    context.call(environment.getattr((undefined(name='actions') if l_1_actions is missing else l_1_actions), 'append'), 'log', _loop_vars=_loop_vars)
                if t_5(environment.getattr(environment.getattr(l_1_handler, 'actions'), 'increment_device_health_metric')):
                    pass
                    l_1_metric = str_join(('increment device health metric ', environment.getattr(environment.getattr(l_1_handler, 'actions'), 'increment_device_health_metric'), ))
                    _loop_vars['metric'] = l_1_metric
                    context.call(environment.getattr((undefined(name='actions') if l_1_actions is missing else l_1_actions), 'append'), (undefined(name='metric') if l_1_metric is missing else l_1_metric), _loop_vars=_loop_vars)
                l_1_actions = t_3(context.eval_ctx, (undefined(name='actions') if l_1_actions is missing else l_1_actions), '<br>')
                _loop_vars['actions'] = l_1_actions
            if ((t_5(environment.getattr(l_1_handler, 'trigger'), 'on-maintenance') and t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'operation'))) and t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'action'))):
                pass
                l_1_trigger_cli = str_join(('trigger ', environment.getattr(l_1_handler, 'trigger'), ' ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'operation'), ))
                _loop_vars['trigger_cli'] = l_1_trigger_cli
                if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'bgp_peer')):
                    pass
                    l_1_on_maintenance_cli = str_join(('bgp ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'bgp_peer'), ))
                    _loop_vars['on_maintenance_cli'] = l_1_on_maintenance_cli
                    if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'vrf')):
                        pass
                        l_1_on_maintenance_cli = str_join(((undefined(name='on_maintenance_cli') if l_1_on_maintenance_cli is missing else l_1_on_maintenance_cli), ' vrf ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'vrf'), ))
                        _loop_vars['on_maintenance_cli'] = l_1_on_maintenance_cli
                elif t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'interface')):
                    pass
                    l_1_on_maintenance_cli = str_join(('interface ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'interface'), ))
                    _loop_vars['on_maintenance_cli'] = l_1_on_maintenance_cli
                elif t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'unit')):
                    pass
                    l_1_on_maintenance_cli = str_join(('unit ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'unit'), ))
                    _loop_vars['on_maintenance_cli'] = l_1_on_maintenance_cli
                if t_5((undefined(name='on_maintenance_cli') if l_1_on_maintenance_cli is missing else l_1_on_maintenance_cli)):
                    pass
                    if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'action')):
                        pass
                        if ((environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'action') in ['after', 'before']) and t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'stage'))):
                            pass
                            l_1_trigger_config = str_join(((undefined(name='trigger_cli') if l_1_trigger_cli is missing else l_1_trigger_cli), ' ', (undefined(name='on_maintenance_cli') if l_1_on_maintenance_cli is missing else l_1_on_maintenance_cli), ' ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'action'), ' stage ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'stage'), ))
                            _loop_vars['trigger_config'] = l_1_trigger_config
                        elif (environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'action') in ['all', 'begin', 'end']):
                            pass
                            l_1_trigger_config = str_join(((undefined(name='trigger_cli') if l_1_trigger_cli is missing else l_1_trigger_cli), ' ', (undefined(name='on_maintenance_cli') if l_1_on_maintenance_cli is missing else l_1_on_maintenance_cli), ' ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_maintenance'), 'action'), ))
                            _loop_vars['trigger_config'] = l_1_trigger_config
            elif (t_5(environment.getattr(l_1_handler, 'trigger'), 'on-counters') and t_5(environment.getattr(l_1_handler, 'trigger_on_counters'))):
                pass
                l_1_trigger_config = []
                _loop_vars['trigger_config'] = l_1_trigger_config
                if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_counters'), 'poll_interval')):
                    pass
                    context.call(environment.getattr((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), 'append'), str_join(('poll interval ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_counters'), 'poll_interval'), )), _loop_vars=_loop_vars)
                if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_counters'), 'condition')):
                    pass
                    context.call(environment.getattr((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), 'append'), str_join(('condition ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_counters'), 'condition'), )), _loop_vars=_loop_vars)
                if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_counters'), 'granularity_per_source'), True):
                    pass
                    context.call(environment.getattr((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), 'append'), 'granularity per-source', _loop_vars=_loop_vars)
                l_1_trigger_config = t_3(context.eval_ctx, (undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), '<br>')
                _loop_vars['trigger_config'] = l_1_trigger_config
            elif (t_5(environment.getattr(l_1_handler, 'trigger'), 'on-logging') and t_5(environment.getattr(l_1_handler, 'trigger_on_logging'))):
                pass
                l_1_trigger_config = []
                _loop_vars['trigger_config'] = l_1_trigger_config
                if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_logging'), 'poll_interval')):
                    pass
                    context.call(environment.getattr((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), 'append'), str_join(('poll interval ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_logging'), 'poll_interval'), )), _loop_vars=_loop_vars)
                if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_logging'), 'regex')):
                    pass
                    context.call(environment.getattr((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), 'append'), str_join(('regex ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_logging'), 'regex'), )), _loop_vars=_loop_vars)
                l_1_trigger_config = t_3(context.eval_ctx, (undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), '<br>')
                _loop_vars['trigger_config'] = l_1_trigger_config
            elif t_5(environment.getattr(l_1_handler, 'trigger'), 'on-intf'):
                pass
                if (t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_intf'), 'interface')) and ((t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_intf'), 'ip'), True) or t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_intf'), 'ipv6'), True)) or t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_intf'), 'operstatus'), True))):
                    pass
                    l_1_trigger_config = str_join(('trigger on-intf ', environment.getattr(environment.getattr(l_1_handler, 'trigger_on_intf'), 'interface'), ))
                    _loop_vars['trigger_config'] = l_1_trigger_config
                    if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_intf'), 'operstatus'), True):
                        pass
                        l_1_trigger_config = str_join(((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), ' operstatus', ))
                        _loop_vars['trigger_config'] = l_1_trigger_config
                    if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_intf'), 'ip'), True):
                        pass
                        l_1_trigger_config = str_join(((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), ' ip', ))
                        _loop_vars['trigger_config'] = l_1_trigger_config
                    if t_5(environment.getattr(environment.getattr(l_1_handler, 'trigger_on_intf'), 'ipv6'), True):
                        pass
                        l_1_trigger_config = str_join(((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), ' ip6', ))
                        _loop_vars['trigger_config'] = l_1_trigger_config
            yield '| '
            yield str(environment.getattr(l_1_handler, 'name'))
            yield ' | '
            yield str(t_1((undefined(name='actions') if l_1_actions is missing else l_1_actions), '-'))
            yield ' | '
            yield str(t_1(environment.getattr(l_1_handler, 'trigger'), '-'))
            yield ' | '
            yield str(t_1((undefined(name='trigger_config') if l_1_trigger_config is missing else l_1_trigger_config), '-'))
            yield ' |\n'
        l_1_handler = l_1_actions = l_1_action = l_1_bash_command = l_1_metric = l_1_trigger_cli = l_1_on_maintenance_cli = l_1_trigger_config = missing
        yield '\n#### Event Handler Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/event-handlers.j2', 'documentation/event-handlers.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '7=42&15=45&16=55&17=57&18=59&19=61&20=63&23=65&24=67&25=69&26=71&27=73&28=75&29=77&30=78&31=80&33=81&34=83&35=85&37=86&39=88&42=90&43=92&44=94&45=96&46=98&48=100&49=102&50=104&51=106&53=108&54=110&55=112&56=114&57=116&58=118&62=120&63=122&64=124&65=126&67=127&68=129&70=130&71=132&73=133&74=135&75=137&76=139&77=141&79=142&80=144&82=145&83=147&84=149&88=151&89=153&90=155&92=157&93=159&95=161&96=163&100=166&106=176'