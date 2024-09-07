from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/monitor-sessions.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_monitor_sessions = resolve('monitor_sessions')
    l_0_monitor_session_default_encapsulation_gre = resolve('monitor_session_default_encapsulation_gre')
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
        t_4 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if (t_4((undefined(name='monitor_sessions') if l_0_monitor_sessions is missing else l_0_monitor_sessions)) or t_4((undefined(name='monitor_session_default_encapsulation_gre') if l_0_monitor_session_default_encapsulation_gre is missing else l_0_monitor_session_default_encapsulation_gre))):
        pass
        yield '\n### Monitor Sessions\n\n#### Monitor Sessions Summary\n'
        def t_5(fiter):
            for l_1_monitor_session in fiter:
                if t_4(environment.getattr(l_1_monitor_session, 'name')):
                    yield l_1_monitor_session
        for l_1_monitor_session in t_5(t_2((undefined(name='monitor_sessions') if l_0_monitor_sessions is missing else l_0_monitor_sessions), 'name')):
            _loop_vars = {}
            pass
            if (t_4(environment.getattr(l_1_monitor_session, 'sources')) and t_4(environment.getattr(l_1_monitor_session, 'destinations'))):
                pass
                yield '\n##### '
                yield str(environment.getattr(l_1_monitor_session, 'name'))
                yield '\n\n####### '
                yield str(environment.getattr(l_1_monitor_session, 'name'))
                yield ' Sources\n\n| Sources | Direction | Access Group Type | Access Group Name | Access Group Priority |\n| ------- | --------- | ----------------- | ----------------- | --------------------- |\n'
                def t_6(fiter):
                    for l_2_source in fiter:
                        if t_4(environment.getattr(l_2_source, 'name')):
                            yield l_2_source
                for l_2_source in t_6(t_2(environment.getattr(l_1_monitor_session, 'sources'), 'name')):
                    _loop_vars = {}
                    pass
                    yield '| '
                    yield str(environment.getattr(l_2_source, 'name'))
                    yield ' | '
                    yield str(t_1(environment.getattr(l_2_source, 'direction'), 'both'))
                    yield ' | '
                    yield str(t_1(environment.getattr(environment.getattr(l_2_source, 'access_group'), 'type'), '-'))
                    yield ' | '
                    yield str(t_1(environment.getattr(environment.getattr(l_2_source, 'access_group'), 'name'), '-'))
                    yield ' | '
                    yield str(t_1(environment.getattr(environment.getattr(l_2_source, 'access_group'), 'priority'), '-'))
                    yield ' |\n'
                l_2_source = missing
                yield '\n####### '
                yield str(environment.getattr(l_1_monitor_session, 'name'))
                yield ' Destinations and Session Settings\n\n| Settings | Values |\n| -------- | ------ |\n| Destinations | '
                yield str(t_3(context.eval_ctx, environment.getattr(l_1_monitor_session, 'destinations'), ', '))
                yield ' |\n'
                if t_4(environment.getattr(l_1_monitor_session, 'encapsulation_gre_metadata_tx'), True):
                    pass
                    yield '| Encapsulation Gre Metadata Tx | '
                    yield str(environment.getattr(l_1_monitor_session, 'encapsulation_gre_metadata_tx'))
                    yield ' |\n'
                if t_4(environment.getattr(l_1_monitor_session, 'header_remove_size')):
                    pass
                    yield '| Header Remove Size | '
                    yield str(environment.getattr(l_1_monitor_session, 'header_remove_size'))
                    yield ' |\n'
                if (t_4(environment.getattr(environment.getattr(l_1_monitor_session, 'access_group'), 'type')) and t_4(environment.getattr(environment.getattr(l_1_monitor_session, 'access_group'), 'name'))):
                    pass
                    yield '| Access Group Type | '
                    yield str(environment.getattr(environment.getattr(l_1_monitor_session, 'access_group'), 'type'))
                    yield ' |\n| Access Group Name | '
                    yield str(environment.getattr(environment.getattr(l_1_monitor_session, 'access_group'), 'name'))
                    yield ' |\n'
                if t_4(environment.getattr(l_1_monitor_session, 'rate_limit_per_ingress_chip')):
                    pass
                    yield '| Rate Limit per Ingress Chip | '
                    yield str(environment.getattr(l_1_monitor_session, 'rate_limit_per_ingress_chip'))
                    yield ' |\n'
                if t_4(environment.getattr(l_1_monitor_session, 'rate_limit_per_ingress_chip')):
                    pass
                    yield '| Rate Limit per Egress Chip | '
                    yield str(environment.getattr(l_1_monitor_session, 'rate_limit_per_egress_chip'))
                    yield ' |\n'
                if t_4(environment.getattr(l_1_monitor_session, 'sample')):
                    pass
                    yield '| Sample | '
                    yield str(environment.getattr(l_1_monitor_session, 'sample'))
                    yield ' |\n'
                if t_4(environment.getattr(environment.getattr(l_1_monitor_session, 'truncate'), 'enabled'), True):
                    pass
                    yield '| Truncate Enabled | '
                    yield str(environment.getattr(environment.getattr(l_1_monitor_session, 'truncate'), 'enabled'))
                    yield ' |\n'
                    if t_4(environment.getattr(environment.getattr(l_1_monitor_session, 'truncate'), 'size')):
                        pass
                        yield '| Truncate Size | '
                        yield str(environment.getattr(environment.getattr(l_1_monitor_session, 'truncate'), 'size'))
                        yield ' |\n'
        l_1_monitor_session = missing
        if t_4(environment.getattr((undefined(name='monitor_session_default_encapsulation_gre') if l_0_monitor_session_default_encapsulation_gre is missing else l_0_monitor_session_default_encapsulation_gre), 'payload')):
            pass
            yield '\n##### Monitor Session Default Settings\n\n| Settings | Values |\n| -------- | ------ |\n| Encapsulation GRE Payload | '
            yield str(environment.getattr((undefined(name='monitor_session_default_encapsulation_gre') if l_0_monitor_session_default_encapsulation_gre is missing else l_0_monitor_session_default_encapsulation_gre), 'payload'))
            yield ' |\n'
        yield '\n#### Monitor Sessions Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/monitor-sessions.j2', 'documentation/monitor-sessions.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        template = environment.get_template('eos/monitor-session-default-encapsulation-gre.j2', 'documentation/monitor-sessions.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '7=37&12=40&13=47&15=50&17=52&21=54&22=62&25=74&29=76&30=78&31=81&33=83&34=86&36=88&37=91&38=93&40=95&41=98&43=100&44=103&46=105&47=108&49=110&50=113&51=115&52=118&57=121&63=124&69=127&70=130'