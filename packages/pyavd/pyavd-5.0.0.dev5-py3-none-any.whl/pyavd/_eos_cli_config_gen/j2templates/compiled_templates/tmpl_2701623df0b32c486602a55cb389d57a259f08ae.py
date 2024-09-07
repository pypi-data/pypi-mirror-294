from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/management-api-gnmi.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_management_api_gnmi = resolve('management_api_gnmi')
    try:
        t_1 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_2((undefined(name='management_api_gnmi') if l_0_management_api_gnmi is missing else l_0_management_api_gnmi)):
        pass
        yield '!\nmanagement api gnmi\n'
        if t_2(environment.getattr((undefined(name='management_api_gnmi') if l_0_management_api_gnmi is missing else l_0_management_api_gnmi), 'transport')):
            pass
            if t_2(environment.getattr(environment.getattr((undefined(name='management_api_gnmi') if l_0_management_api_gnmi is missing else l_0_management_api_gnmi), 'transport'), 'grpc')):
                pass
                for l_1_transport in environment.getattr(environment.getattr((undefined(name='management_api_gnmi') if l_0_management_api_gnmi is missing else l_0_management_api_gnmi), 'transport'), 'grpc'):
                    _loop_vars = {}
                    pass
                    if t_2(environment.getattr(l_1_transport, 'name')):
                        pass
                        yield '   transport grpc '
                        yield str(environment.getattr(l_1_transport, 'name'))
                        yield '\n'
                        if t_2(environment.getattr(l_1_transport, 'ssl_profile')):
                            pass
                            yield '      ssl profile '
                            yield str(environment.getattr(l_1_transport, 'ssl_profile'))
                            yield '\n'
                        if t_2(environment.getattr(l_1_transport, 'port')):
                            pass
                            yield '      port '
                            yield str(environment.getattr(l_1_transport, 'port'))
                            yield '\n'
                        if t_2(environment.getattr(l_1_transport, 'vrf')):
                            pass
                            yield '      vrf '
                            yield str(environment.getattr(l_1_transport, 'vrf'))
                            yield '\n'
                        if t_2(environment.getattr(l_1_transport, 'ip_access_group')):
                            pass
                            yield '      ip access-group '
                            yield str(environment.getattr(l_1_transport, 'ip_access_group'))
                            yield '\n'
                        if t_2(environment.getattr(l_1_transport, 'notification_timestamp')):
                            pass
                            yield '      notification timestamp '
                            yield str(environment.getattr(l_1_transport, 'notification_timestamp'))
                            yield '\n'
                l_1_transport = missing
            if t_2(environment.getattr(environment.getattr((undefined(name='management_api_gnmi') if l_0_management_api_gnmi is missing else l_0_management_api_gnmi), 'transport'), 'grpc_tunnels')):
                pass
                for l_1_transport in environment.getattr(environment.getattr((undefined(name='management_api_gnmi') if l_0_management_api_gnmi is missing else l_0_management_api_gnmi), 'transport'), 'grpc_tunnels'):
                    _loop_vars = {}
                    pass
                    yield '   transport grpc-tunnel '
                    yield str(environment.getattr(l_1_transport, 'name'))
                    yield '\n'
                    if t_2(environment.getattr(l_1_transport, 'shutdown'), True):
                        pass
                        yield '      shutdown\n'
                    elif t_2(environment.getattr(l_1_transport, 'shutdown'), False):
                        pass
                        yield '      no shutdown\n'
                    if t_2(environment.getattr(l_1_transport, 'vrf')):
                        pass
                        yield '      vrf '
                        yield str(environment.getattr(l_1_transport, 'vrf'))
                        yield '\n'
                    if t_2(environment.getattr(l_1_transport, 'tunnel_ssl_profile')):
                        pass
                        yield '      tunnel ssl profile '
                        yield str(environment.getattr(l_1_transport, 'tunnel_ssl_profile'))
                        yield '\n'
                    if t_2(environment.getattr(l_1_transport, 'gnmi_ssl_profile')):
                        pass
                        yield '      gnmi ssl profile '
                        yield str(environment.getattr(l_1_transport, 'gnmi_ssl_profile'))
                        yield '\n'
                    if t_2(environment.getattr(l_1_transport, 'destination')):
                        pass
                        yield '      destination '
                        yield str(environment.getattr(environment.getattr(l_1_transport, 'destination'), 'address'))
                        yield ' port '
                        yield str(environment.getattr(environment.getattr(l_1_transport, 'destination'), 'port'))
                        yield '\n'
                    if t_2(environment.getattr(l_1_transport, 'local_interface')):
                        pass
                        yield '      local interface '
                        yield str(environment.getattr(environment.getattr(l_1_transport, 'local_interface'), 'name'))
                        yield ' port '
                        yield str(environment.getattr(environment.getattr(l_1_transport, 'local_interface'), 'port'))
                        yield '\n'
                    if t_2(environment.getattr(environment.getattr(l_1_transport, 'target'), 'use_serial_number'), True):
                        pass
                        if t_2(environment.getattr(environment.getattr(l_1_transport, 'target'), 'target_ids')):
                            pass
                            yield '      target serial-number '
                            yield str(t_1(context.eval_ctx, environment.getattr(environment.getattr(l_1_transport, 'target'), 'target_ids'), ' '))
                            yield '\n'
                        else:
                            pass
                            yield '      target serial-number\n'
                    elif t_2(environment.getattr(environment.getattr(l_1_transport, 'target'), 'target_ids')):
                        pass
                        yield '      target '
                        yield str(t_1(context.eval_ctx, environment.getattr(environment.getattr(l_1_transport, 'target'), 'target_ids'), ' '))
                        yield '\n'
                l_1_transport = missing
        if t_2(environment.getattr((undefined(name='management_api_gnmi') if l_0_management_api_gnmi is missing else l_0_management_api_gnmi), 'provider')):
            pass
            yield '   provider '
            yield str(environment.getattr((undefined(name='management_api_gnmi') if l_0_management_api_gnmi is missing else l_0_management_api_gnmi), 'provider'))
            yield '\n'

blocks = {}
debug_info = '7=24&10=27&11=29&12=31&13=34&14=37&15=39&16=42&18=44&19=47&21=49&22=52&24=54&25=57&27=59&28=62&33=65&34=67&35=71&36=73&38=76&41=79&42=82&44=84&45=87&47=89&48=92&50=94&51=97&53=101&54=104&56=108&57=110&58=113&62=118&63=121&68=124&69=127'