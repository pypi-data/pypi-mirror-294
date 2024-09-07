from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-bgp.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_bgp = resolve('router_bgp')
    l_0_distance_cli = resolve('distance_cli')
    l_0_rr_preserve_attributes_cli = resolve('rr_preserve_attributes_cli')
    l_0_paths_cli = resolve('paths_cli')
    l_0_bgp_vlans = resolve('bgp_vlans')
    l_0_hostflap_detection_cli = resolve('hostflap_detection_cli')
    l_0_evpn_neighbor_default_encap_cli = resolve('evpn_neighbor_default_encap_cli')
    l_0_evpn_mpls_resolution_ribs = resolve('evpn_mpls_resolution_ribs')
    l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = resolve('evpn_neighbor_default_nhs_received_evpn_routes_cli')
    l_0_layer2_cli = resolve('layer2_cli')
    l_0_path_selection_roles = resolve('path_selection_roles')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.hide_passwords']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.hide_passwords' found.")
    try:
        t_3 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_4 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_5 = environment.filters['join']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No filter named 'join' found.")
    try:
        t_6 = environment.filters['sort']
    except KeyError:
        @internalcode
        def t_6(*unused):
            raise TemplateRuntimeError("No filter named 'sort' found.")
    try:
        t_7 = environment.filters['string']
    except KeyError:
        @internalcode
        def t_7(*unused):
            raise TemplateRuntimeError("No filter named 'string' found.")
    try:
        t_8 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_8(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    try:
        t_9 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_9(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    try:
        t_10 = environment.tests['number']
    except KeyError:
        @internalcode
        def t_10(*unused):
            raise TemplateRuntimeError("No test named 'number' found.")
    pass
    if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as')):
        pass
        yield '!\nrouter bgp '
        yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as'))
        yield '\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as_notation')):
            pass
            yield '   bgp asn notation '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'as_notation'))
            yield '\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'router_id')):
            pass
            yield '   router-id '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'router_id'))
            yield '\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes')):
            pass
            l_0_distance_cli = str_join(('distance bgp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'external_routes'), ))
            context.vars['distance_cli'] = l_0_distance_cli
            context.exported_vars.add('distance_cli')
            if (t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes')) and t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'))):
                pass
                l_0_distance_cli = str_join(((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'internal_routes'), ' ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'distance'), 'local_routes'), ))
                context.vars['distance_cli'] = l_0_distance_cli
                context.exported_vars.add('distance_cli')
            yield '   '
            yield str((undefined(name='distance_cli') if l_0_distance_cli is missing else l_0_distance_cli))
            yield '\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'enabled'), True):
            pass
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time')):
                pass
                yield '   graceful-restart restart-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'restart_time'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time')):
                pass
                yield '   graceful-restart stalepath-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart'), 'stalepath_time'))
                yield '\n'
            yield '   graceful-restart\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), False):
            pass
            yield '   no graceful-restart-helper\n'
        elif t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'enabled'), True):
            pass
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time')):
                pass
                yield '   graceful-restart-helper restart-time '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'restart_time'))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'graceful_restart_helper'), 'long_lived'), True):
                pass
                yield '   graceful-restart-helper long-lived\n'
        if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'enabled'), True):
            pass
            l_0_rr_preserve_attributes_cli = 'bgp route-reflector preserve-attributes'
            context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
            context.exported_vars.add('rr_preserve_attributes_cli')
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'route_reflector_preserve_attributes'), 'always'), True):
                pass
                l_0_rr_preserve_attributes_cli = str_join(((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli), ' always', ))
                context.vars['rr_preserve_attributes_cli'] = l_0_rr_preserve_attributes_cli
                context.exported_vars.add('rr_preserve_attributes_cli')
            yield '   '
            yield str((undefined(name='rr_preserve_attributes_cli') if l_0_rr_preserve_attributes_cli is missing else l_0_rr_preserve_attributes_cli))
            yield '\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths')):
            pass
            l_0_paths_cli = str_join(('maximum-paths ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'paths'), ))
            context.vars['paths_cli'] = l_0_paths_cli
            context.exported_vars.add('paths_cli')
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp')):
                pass
                l_0_paths_cli = str_join(((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli), ' ecmp ', environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'maximum_paths'), 'ecmp'), ))
                context.vars['paths_cli'] = l_0_paths_cli
                context.exported_vars.add('paths_cli')
            yield '   '
            yield str((undefined(name='paths_cli') if l_0_paths_cli is missing else l_0_paths_cli))
            yield '\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_for_convergence'), True):
            pass
            yield '   update wait-for-convergence\n'
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'updates'), 'wait_install'), True):
            pass
            yield '   update wait-install\n'
        if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), True):
            pass
            yield '   bgp default ipv4-unicast\n'
        elif t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast'), False):
            pass
            yield '   no bgp default ipv4-unicast\n'
        if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), True):
            pass
            yield '   bgp default ipv4-unicast transport ipv6\n'
        elif t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'default'), 'ipv4_unicast_transport_ipv6'), False):
            pass
            yield '   no bgp default ipv4-unicast transport ipv6\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id')):
            pass
            yield '   bgp cluster-id '
            yield str(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_cluster_id'))
            yield '\n'
        for l_1_bgp_default in t_1(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp_defaults'), []):
            _loop_vars = {}
            pass
            yield '   '
            yield str(l_1_bgp_default)
            yield '\n'
        l_1_bgp_default = missing
        if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'bestpath'), 'd_path'), True):
            pass
            yield '   bgp bestpath d-path\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges')):
            pass
            def t_11(fiter):
                for l_1_listen_range in fiter:
                    if ((t_8(environment.getattr(l_1_listen_range, 'peer_group')) and t_8(environment.getattr(l_1_listen_range, 'prefix'))) and (t_8(environment.getattr(l_1_listen_range, 'peer_filter')) or t_8(environment.getattr(l_1_listen_range, 'remote_as')))):
                        yield l_1_listen_range
            for l_1_listen_range in t_11(t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'listen_ranges'), 'peer_group')):
                l_1_listen_range_cli = missing
                _loop_vars = {}
                pass
                l_1_listen_range_cli = str_join(('bgp listen range ', environment.getattr(l_1_listen_range, 'prefix'), ))
                _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                if t_8(environment.getattr(l_1_listen_range, 'peer_id_include_router_id'), True):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-id include router-id', ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-group ', environment.getattr(l_1_listen_range, 'peer_group'), ))
                _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                if t_8(environment.getattr(l_1_listen_range, 'peer_filter')):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' peer-filter ', environment.getattr(l_1_listen_range, 'peer_filter'), ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                elif t_8(environment.getattr(l_1_listen_range, 'remote_as')):
                    pass
                    l_1_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli), ' remote-as ', environment.getattr(l_1_listen_range, 'remote_as'), ))
                    _loop_vars['listen_range_cli'] = l_1_listen_range_cli
                yield '   '
                yield str((undefined(name='listen_range_cli') if l_1_listen_range_cli is missing else l_1_listen_range_cli))
                yield '\n'
            l_1_listen_range = l_1_listen_range_cli = missing
        for l_1_peer_group in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
            _loop_vars = {}
            pass
            if (t_8(environment.getattr(l_1_peer_group, 'bgp_listen_range_prefix')) and t_8(environment.getattr(l_1_peer_group, 'peer_filter'))):
                pass
                yield '   bgp listen range '
                yield str(environment.getattr(l_1_peer_group, 'bgp_listen_range_prefix'))
                yield ' peer-group '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' peer-filter '
                yield str(environment.getattr(l_1_peer_group, 'peer_filter'))
                yield '\n'
        l_1_peer_group = missing
        for l_1_peer_group in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'peer_groups'), 'name'):
            l_1_remove_private_as_cli = resolve('remove_private_as_cli')
            l_1_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
            l_1_allowas_in_cli = resolve('allowas_in_cli')
            l_1_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
            l_1_hide_passwords = resolve('hide_passwords')
            l_1_default_originate_cli = resolve('default_originate_cli')
            l_1_maximum_routes_cli = resolve('maximum_routes_cli')
            l_1_link_bandwidth_cli = resolve('link_bandwidth_cli')
            _loop_vars = {}
            pass
            if t_8(environment.getattr(l_1_peer_group, 'shutdown'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' shutdown\n'
            yield '   neighbor '
            yield str(environment.getattr(l_1_peer_group, 'name'))
            yield ' peer group\n'
            if t_8(environment.getattr(l_1_peer_group, 'remote_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_peer_group, 'remote_as'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'local_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' local-as '
                yield str(environment.getattr(l_1_peer_group, 'local_as'))
                yield ' no-prepend replace-as\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'as_path'), 'remote_as_replace_out'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' as-path remote-as replace out\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'as_path'), 'prepend_own_disabled'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' as-path prepend-own disabled\n'
            if t_8(environment.getattr(l_1_peer_group, 'next_hop_self'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' next-hop-self\n'
            if t_8(environment.getattr(l_1_peer_group, 'next_hop_unchanged'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' next-hop-unchanged\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled'), True):
                pass
                l_1_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' remove-private-as', ))
                _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'all'), True):
                    pass
                    l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' all', ))
                    _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'replace_as'), True):
                        pass
                        l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                yield '   '
                yield str((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remove-private-as\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled'), True):
                pass
                l_1_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' remove-private-as ingress', ))
                _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'replace_as'), True):
                    pass
                    l_1_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli), ' replace-as', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                yield '   '
                yield str((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'remove_private_as_ingress'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' remove-private-as ingress\n'
            if t_8(environment.getattr(l_1_peer_group, 'update_source')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' update-source '
                yield str(environment.getattr(l_1_peer_group, 'update_source'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'description')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' description '
                yield str(environment.getattr(l_1_peer_group, 'description'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'route_reflector_client'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-reflector-client\n'
            if t_8(environment.getattr(l_1_peer_group, 'bfd'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' bfd\n'
                if ((t_8(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'interval')) and t_8(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'min_rx'))) and t_8(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'multiplier'))):
                    pass
                    yield '   neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' bfd interval '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'interval'))
                    yield ' min-rx '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'min_rx'))
                    yield ' multiplier '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'bfd_timers'), 'multiplier'))
                    yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'enabled'), True):
                pass
                l_1_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' allowas-in', ))
                _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'times')):
                    pass
                    l_1_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_1_peer_group, 'allowas_in'), 'times'), ))
                    _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                yield '   '
                yield str((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled'), True):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'all'), True):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'rib_in_pre_policy_retain'), 'enabled'), False):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_1_peer_group, 'name'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'ebgp_multihop')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' ebgp-multihop '
                yield str(environment.getattr(l_1_peer_group, 'ebgp_multihop'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'ttl_maximum_hops')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' ttl maximum-hops '
                yield str(environment.getattr(l_1_peer_group, 'ttl_maximum_hops'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'password')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' password 7 '
                yield str(t_2(environment.getattr(l_1_peer_group, 'password'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'enabled'), True):
                pass
                l_1_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-originate', ))
                _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map')):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map'), ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'always'), True):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' always', ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                yield '   '
                yield str((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'passive'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' passive\n'
            if t_8(environment.getattr(l_1_peer_group, 'session_tracker')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' session tracker '
                yield str(environment.getattr(l_1_peer_group, 'session_tracker'))
                yield '\n'
            if (t_8(environment.getattr(environment.getattr(l_1_peer_group, 'shared_secret'), 'profile')) and t_8(environment.getattr(environment.getattr(l_1_peer_group, 'shared_secret'), 'hash_algorithm'))):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' password shared-secret profile '
                yield str(environment.getattr(environment.getattr(l_1_peer_group, 'shared_secret'), 'profile'))
                yield ' algorithm '
                yield str(environment.getattr(environment.getattr(l_1_peer_group, 'shared_secret'), 'hash_algorithm'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'send_community'), 'all'):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' send-community\n'
            elif t_8(environment.getattr(l_1_peer_group, 'send_community')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' send-community '
                yield str(environment.getattr(l_1_peer_group, 'send_community'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'maximum_routes')):
                pass
                l_1_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' maximum-routes ', environment.getattr(l_1_peer_group, 'maximum_routes'), ))
                _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_8(environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit')):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-limit ', environment.getattr(l_1_peer_group, 'maximum_routes_warning_limit'), ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_8(environment.getattr(l_1_peer_group, 'maximum_routes_warning_only'), True):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-only', ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                yield '   '
                yield str((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'missing_policy')):
                pass
                for l_2_direction in ['in', 'out']:
                    l_2_missing_policy_cli = resolve('missing_policy_cli')
                    l_2_dir = l_2_policy = missing
                    _loop_vars = {}
                    pass
                    l_2_dir = str_join(('direction_', l_2_direction, ))
                    _loop_vars['dir'] = l_2_dir
                    l_2_policy = environment.getitem(environment.getattr(l_1_peer_group, 'missing_policy'), (undefined(name='dir') if l_2_dir is missing else l_2_dir))
                    _loop_vars['policy'] = l_2_policy
                    if t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action')):
                        pass
                        l_2_missing_policy_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' missing-policy address-family all', ))
                        _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        if ((t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True) or t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True)) or t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True)):
                            pass
                            l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' include', ))
                            _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' community-list', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' prefix-list', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' sub-route-map', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' direction ', l_2_direction, ' action ', environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action'), ))
                        _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        yield '   '
                        yield str((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli))
                        yield '\n'
                l_2_direction = l_2_dir = l_2_policy = l_2_missing_policy_cli = missing
            if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'enabled'), True):
                pass
                l_1_link_bandwidth_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' link-bandwidth', ))
                _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default')):
                    pass
                    l_1_link_bandwidth_cli = str_join(((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli), ' default ', environment.getattr(environment.getattr(l_1_peer_group, 'link_bandwidth'), 'default'), ))
                    _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                yield '   '
                yield str((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'weight')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' weight '
                yield str(environment.getattr(l_1_peer_group, 'weight'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'timers')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' timers '
                yield str(environment.getattr(l_1_peer_group, 'timers'))
                yield '\n'
            if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-map '
                yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                yield ' in\n'
            if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_peer_group, 'name'))
                yield ' route-map '
                yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                yield ' out\n'
        l_1_peer_group = l_1_remove_private_as_cli = l_1_remove_private_as_ingress_cli = l_1_allowas_in_cli = l_1_neighbor_rib_in_pre_policy_retain_cli = l_1_hide_passwords = l_1_default_originate_cli = l_1_maximum_routes_cli = l_1_link_bandwidth_cli = missing
        for l_1_neighbor_interface in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbor_interfaces'), 'name'):
            _loop_vars = {}
            pass
            if (t_8(environment.getattr(l_1_neighbor_interface, 'peer_group')) and t_8(environment.getattr(l_1_neighbor_interface, 'remote_as'))):
                pass
                yield '   neighbor interface '
                yield str(environment.getattr(l_1_neighbor_interface, 'name'))
                yield ' peer-group '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_group'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_neighbor_interface, 'remote_as'))
                yield '\n'
            elif (t_8(environment.getattr(l_1_neighbor_interface, 'peer_group')) and t_8(environment.getattr(l_1_neighbor_interface, 'peer_filter'))):
                pass
                yield '   neighbor interface '
                yield str(environment.getattr(l_1_neighbor_interface, 'name'))
                yield ' peer-group '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_group'))
                yield ' peer-filter '
                yield str(environment.getattr(l_1_neighbor_interface, 'peer_filter'))
                yield '\n'
        l_1_neighbor_interface = missing
        for l_1_neighbor in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'neighbors'), 'ip_address'):
            l_1_remove_private_as_cli = resolve('remove_private_as_cli')
            l_1_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
            l_1_allowas_in_cli = resolve('allowas_in_cli')
            l_1_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
            l_1_hide_passwords = resolve('hide_passwords')
            l_1_default_originate_cli = resolve('default_originate_cli')
            l_1_maximum_routes_cli = resolve('maximum_routes_cli')
            l_1_link_bandwidth_cli = resolve('link_bandwidth_cli')
            _loop_vars = {}
            pass
            if t_8(environment.getattr(l_1_neighbor, 'peer_group')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' peer group '
                yield str(environment.getattr(l_1_neighbor, 'peer_group'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'remote_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remote-as '
                yield str(environment.getattr(l_1_neighbor, 'remote_as'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'next_hop_self'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' next-hop-self\n'
            if t_8(environment.getattr(l_1_neighbor, 'shutdown'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' shutdown\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'enabled'), True):
                pass
                l_1_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' remove-private-as', ))
                _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'all'), True):
                    pass
                    l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' all', ))
                    _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'replace_as'), True):
                        pass
                        l_1_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_cli'] = l_1_remove_private_as_cli
                yield '   '
                yield str((undefined(name='remove_private_as_cli') if l_1_remove_private_as_cli is missing else l_1_remove_private_as_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remove-private-as\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'enabled'), True):
                pass
                l_1_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' remove-private-as ingress', ))
                _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'replace_as'), True):
                    pass
                    l_1_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli), ' replace-as', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_1_remove_private_as_ingress_cli
                yield '   '
                yield str((undefined(name='remove_private_as_ingress_cli') if l_1_remove_private_as_ingress_cli is missing else l_1_remove_private_as_ingress_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'remove_private_as_ingress'), 'enabled'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' remove-private-as ingress\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'as_path'), 'remote_as_replace_out'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' as-path remote-as replace out\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'as_path'), 'prepend_own_disabled'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' as-path prepend-own disabled\n'
            if t_8(environment.getattr(l_1_neighbor, 'local_as')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' local-as '
                yield str(environment.getattr(l_1_neighbor, 'local_as'))
                yield ' no-prepend replace-as\n'
            if t_8(environment.getattr(l_1_neighbor, 'description')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' description '
                yield str(environment.getattr(l_1_neighbor, 'description'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'route_reflector_client'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-reflector-client\n'
            elif t_8(environment.getattr(l_1_neighbor, 'route_reflector_client'), False):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-reflector-client\n'
            if t_8(environment.getattr(l_1_neighbor, 'ebgp_multihop')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' ebgp-multihop '
                yield str(environment.getattr(l_1_neighbor, 'ebgp_multihop'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'ttl_maximum_hops')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' ttl maximum-hops '
                yield str(environment.getattr(l_1_neighbor, 'ttl_maximum_hops'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'update_source')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' update-source '
                yield str(environment.getattr(l_1_neighbor, 'update_source'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'bfd'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' bfd\n'
                if ((t_8(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'interval')) and t_8(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'min_rx'))) and t_8(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'multiplier'))):
                    pass
                    yield '   neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' bfd interval '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'interval'))
                    yield ' min-rx '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'min_rx'))
                    yield ' multiplier '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'bfd_timers'), 'multiplier'))
                    yield '\n'
            elif (t_8(environment.getattr(l_1_neighbor, 'bfd'), False) and t_8(environment.getattr(l_1_neighbor, 'peer_group'))):
                pass
                yield '   no neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' bfd\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'enabled'), True):
                pass
                l_1_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' allowas-in', ))
                _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times')):
                    pass
                    l_1_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_1_neighbor, 'allowas_in'), 'times'), ))
                    _loop_vars['allowas_in_cli'] = l_1_allowas_in_cli
                yield '   '
                yield str((undefined(name='allowas_in_cli') if l_1_allowas_in_cli is missing else l_1_allowas_in_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'all'), True):
                    pass
                    l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), False):
                pass
                l_1_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_1_neighbor_rib_in_pre_policy_retain_cli
                yield '   '
                yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_1_neighbor_rib_in_pre_policy_retain_cli is missing else l_1_neighbor_rib_in_pre_policy_retain_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'password')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' password 7 '
                yield str(t_2(environment.getattr(l_1_neighbor, 'password'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'passive'), True):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' passive\n'
            if t_8(environment.getattr(l_1_neighbor, 'weight')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' weight '
                yield str(environment.getattr(l_1_neighbor, 'weight'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'session_tracker')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' session tracker '
                yield str(environment.getattr(l_1_neighbor, 'session_tracker'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'timers')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' timers '
                yield str(environment.getattr(l_1_neighbor, 'timers'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-map '
                yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                yield ' in\n'
            if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' route-map '
                yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                yield ' out\n'
            if (t_8(environment.getattr(environment.getattr(l_1_neighbor, 'shared_secret'), 'profile')) and t_8(environment.getattr(environment.getattr(l_1_neighbor, 'shared_secret'), 'hash_algorithm'))):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' password shared-secret profile '
                yield str(environment.getattr(environment.getattr(l_1_neighbor, 'shared_secret'), 'profile'))
                yield ' algorithm '
                yield str(environment.getattr(environment.getattr(l_1_neighbor, 'shared_secret'), 'hash_algorithm'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'enabled'), True):
                pass
                l_1_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-originate', ))
                _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map')):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map'), ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'always'), True):
                    pass
                    l_1_default_originate_cli = str_join(((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli), ' always', ))
                    _loop_vars['default_originate_cli'] = l_1_default_originate_cli
                yield '   '
                yield str((undefined(name='default_originate_cli') if l_1_default_originate_cli is missing else l_1_default_originate_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'send_community'), 'all'):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' send-community\n'
            elif t_8(environment.getattr(l_1_neighbor, 'send_community')):
                pass
                yield '   neighbor '
                yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                yield ' send-community '
                yield str(environment.getattr(l_1_neighbor, 'send_community'))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'maximum_routes')):
                pass
                l_1_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' maximum-routes ', environment.getattr(l_1_neighbor, 'maximum_routes'), ))
                _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_8(environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit')):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-limit ', environment.getattr(l_1_neighbor, 'maximum_routes_warning_limit'), ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                if t_8(environment.getattr(l_1_neighbor, 'maximum_routes_warning_only'), True):
                    pass
                    l_1_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli), ' warning-only', ))
                    _loop_vars['maximum_routes_cli'] = l_1_maximum_routes_cli
                yield '   '
                yield str((undefined(name='maximum_routes_cli') if l_1_maximum_routes_cli is missing else l_1_maximum_routes_cli))
                yield '\n'
            if t_8(environment.getattr(l_1_neighbor, 'missing_policy')):
                pass
                for l_2_direction in ['in', 'out']:
                    l_2_missing_policy_cli = resolve('missing_policy_cli')
                    l_2_dir = l_2_policy = missing
                    _loop_vars = {}
                    pass
                    l_2_dir = str_join(('direction_', l_2_direction, ))
                    _loop_vars['dir'] = l_2_dir
                    l_2_policy = environment.getitem(environment.getattr(l_1_neighbor, 'missing_policy'), (undefined(name='dir') if l_2_dir is missing else l_2_dir))
                    _loop_vars['policy'] = l_2_policy
                    if t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action')):
                        pass
                        l_2_missing_policy_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' missing-policy address-family all', ))
                        _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        if ((t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True) or t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True)) or t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True)):
                            pass
                            l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' include', ))
                            _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_community_list'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' community-list', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_prefix_list'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' prefix-list', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                            if t_8(environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'include_sub_route_map'), True):
                                pass
                                l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' sub-route-map', ))
                                _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        l_2_missing_policy_cli = str_join(((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli), ' direction ', l_2_direction, ' action ', environment.getattr((undefined(name='policy') if l_2_policy is missing else l_2_policy), 'action'), ))
                        _loop_vars['missing_policy_cli'] = l_2_missing_policy_cli
                        yield '   '
                        yield str((undefined(name='missing_policy_cli') if l_2_missing_policy_cli is missing else l_2_missing_policy_cli))
                        yield '\n'
                l_2_direction = l_2_dir = l_2_policy = l_2_missing_policy_cli = missing
            if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'enabled'), True):
                pass
                l_1_link_bandwidth_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' link-bandwidth', ))
                _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'default')):
                    pass
                    l_1_link_bandwidth_cli = str_join(((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli), ' default ', environment.getattr(environment.getattr(l_1_neighbor, 'link_bandwidth'), 'default'), ))
                    _loop_vars['link_bandwidth_cli'] = l_1_link_bandwidth_cli
                yield '   '
                yield str((undefined(name='link_bandwidth_cli') if l_1_link_bandwidth_cli is missing else l_1_link_bandwidth_cli))
                yield '\n'
        l_1_neighbor = l_1_remove_private_as_cli = l_1_remove_private_as_ingress_cli = l_1_allowas_in_cli = l_1_neighbor_rib_in_pre_policy_retain_cli = l_1_hide_passwords = l_1_default_originate_cli = l_1_maximum_routes_cli = l_1_link_bandwidth_cli = missing
        if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'redistribute_internal'), True):
            pass
            yield '   bgp redistribute-internal\n'
        elif t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'bgp'), 'redistribute_internal'), False):
            pass
            yield '   no bgp redistribute-internal\n'
        for l_1_aggregate_address in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'aggregate_addresses'), 'prefix'):
            l_1_aggregate_address_cli = missing
            _loop_vars = {}
            pass
            l_1_aggregate_address_cli = str_join(('aggregate-address ', environment.getattr(l_1_aggregate_address, 'prefix'), ))
            _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'as_set'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' as-set', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'summary_only'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' summary-only', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'attribute_map')):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' attribute-map ', environment.getattr(l_1_aggregate_address, 'attribute_map'), ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'match_map')):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' match-map ', environment.getattr(l_1_aggregate_address, 'match_map'), ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            if t_8(environment.getattr(l_1_aggregate_address, 'advertise_only'), True):
                pass
                l_1_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli), ' advertise-only', ))
                _loop_vars['aggregate_address_cli'] = l_1_aggregate_address_cli
            yield '   '
            yield str((undefined(name='aggregate_address_cli') if l_1_aggregate_address_cli is missing else l_1_aggregate_address_cli))
            yield '\n'
        l_1_aggregate_address = l_1_aggregate_address_cli = missing
        for l_1_redistribute_route in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'redistribute_routes'), 'source_protocol'):
            l_1_redistribute_route_cli = resolve('redistribute_route_cli')
            _loop_vars = {}
            pass
            if t_8(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                pass
                l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                    pass
                    if t_8(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'bgp'):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' leaked', ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif t_8(environment.getattr(l_1_redistribute_route, 'include_leaked')):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                if t_8(environment.getattr(l_1_redistribute_route, 'route_map')):
                    pass
                    l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                elif (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                    pass
                    if t_8(environment.getattr(l_1_redistribute_route, 'rcf')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                yield '   '
                yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                yield '\n'
        l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans')):
            pass
            l_0_bgp_vlans = environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlans')
            context.vars['bgp_vlans'] = l_0_bgp_vlans
            context.exported_vars.add('bgp_vlans')
            for l_1_bgp_vlan in (undefined(name='bgp_vlans') if l_0_bgp_vlans is missing else l_0_bgp_vlans):
                _loop_vars = {}
                pass
                context.call(environment.getattr(l_1_bgp_vlan, 'update'), {'id': t_7(environment.getitem(l_1_bgp_vlan, 'id'))}, _loop_vars=_loop_vars)
            l_1_bgp_vlan = missing
            for l_1_vlan in t_6(environment, (undefined(name='bgp_vlans') if l_0_bgp_vlans is missing else l_0_bgp_vlans), attribute='id'):
                _loop_vars = {}
                pass
                yield '   !\n   vlan '
                yield str(environment.getattr(l_1_vlan, 'id'))
                yield '\n'
                if t_8(environment.getattr(l_1_vlan, 'rd')):
                    pass
                    yield '      rd '
                    yield str(environment.getattr(l_1_vlan, 'rd'))
                    yield '\n'
                if (t_8(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'domain')) and t_8(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'rd'))):
                    pass
                    yield '      rd evpn domain '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'domain'))
                    yield ' '
                    yield str(environment.getattr(environment.getattr(l_1_vlan, 'rd_evpn_domain'), 'rd'))
                    yield '\n'
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'both')):
                    _loop_vars = {}
                    pass
                    yield '      route-target both '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export')):
                    _loop_vars = {}
                    pass
                    yield '      route-target export '
                    yield str(l_2_route_target)
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'export_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target export evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan, 'route_targets'), 'import_export_evpn_domains')):
                    _loop_vars = {}
                    pass
                    yield '      route-target import export evpn domain '
                    yield str(environment.getattr(l_2_route_target, 'domain'))
                    yield ' '
                    yield str(environment.getattr(l_2_route_target, 'route_target'))
                    yield '\n'
                l_2_route_target = missing
                for l_2_redistribute_route in t_3(environment.getattr(l_1_vlan, 'redistribute_routes')):
                    _loop_vars = {}
                    pass
                    yield '      redistribute '
                    yield str(l_2_redistribute_route)
                    yield '\n'
                l_2_redistribute_route = missing
                for l_2_no_redistribute_route in t_3(environment.getattr(l_1_vlan, 'no_redistribute_routes')):
                    _loop_vars = {}
                    pass
                    yield '      no redistribute '
                    yield str(l_2_no_redistribute_route)
                    yield '\n'
                l_2_no_redistribute_route = missing
                if t_8(environment.getattr(l_1_vlan, 'eos_cli')):
                    pass
                    yield '      !\n      '
                    yield str(t_4(environment.getattr(l_1_vlan, 'eos_cli'), 6, False))
                    yield '\n'
            l_1_vlan = missing
        for l_1_vlan_aware_bundle in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vlan_aware_bundles'), 'name'):
            _loop_vars = {}
            pass
            yield '   !\n   vlan-aware-bundle '
            yield str(environment.getattr(l_1_vlan_aware_bundle, 'name'))
            yield '\n'
            if t_8(environment.getattr(l_1_vlan_aware_bundle, 'rd')):
                pass
                yield '      rd '
                yield str(environment.getattr(l_1_vlan_aware_bundle, 'rd'))
                yield '\n'
            if (t_8(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'domain')) and t_8(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'rd'))):
                pass
                yield '      rd evpn domain '
                yield str(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'domain'))
                yield ' '
                yield str(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'rd_evpn_domain'), 'rd'))
                yield '\n'
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'both')):
                _loop_vars = {}
                pass
                yield '      route-target both '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import')):
                _loop_vars = {}
                pass
                yield '      route-target import '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export')):
                _loop_vars = {}
                pass
                yield '      route-target export '
                yield str(l_2_route_target)
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target import evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'export_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target export evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_route_target in t_3(environment.getattr(environment.getattr(l_1_vlan_aware_bundle, 'route_targets'), 'import_export_evpn_domains')):
                _loop_vars = {}
                pass
                yield '      route-target import export evpn domain '
                yield str(environment.getattr(l_2_route_target, 'domain'))
                yield ' '
                yield str(environment.getattr(l_2_route_target, 'route_target'))
                yield '\n'
            l_2_route_target = missing
            for l_2_redistribute_route in t_3(environment.getattr(l_1_vlan_aware_bundle, 'redistribute_routes')):
                _loop_vars = {}
                pass
                yield '      redistribute '
                yield str(l_2_redistribute_route)
                yield '\n'
            l_2_redistribute_route = missing
            for l_2_no_redistribute_route in t_3(environment.getattr(l_1_vlan_aware_bundle, 'no_redistribute_routes')):
                _loop_vars = {}
                pass
                yield '      no redistribute '
                yield str(l_2_no_redistribute_route)
                yield '\n'
            l_2_no_redistribute_route = missing
            yield '      vlan '
            yield str(environment.getattr(l_1_vlan_aware_bundle, 'vlan'))
            yield '\n'
            if t_8(environment.getattr(l_1_vlan_aware_bundle, 'eos_cli')):
                pass
                yield '      !\n      '
                yield str(t_4(environment.getattr(l_1_vlan_aware_bundle, 'eos_cli'), 6, False))
                yield '\n'
        l_1_vlan_aware_bundle = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws')):
            pass
            for l_1_vpws_service in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vpws'), 'name'):
                _loop_vars = {}
                pass
                yield '   !\n'
                if t_8(environment.getattr(l_1_vpws_service, 'name')):
                    pass
                    yield '   vpws '
                    yield str(environment.getattr(l_1_vpws_service, 'name'))
                    yield '\n'
                    if t_8(environment.getattr(l_1_vpws_service, 'rd')):
                        pass
                        yield '      rd '
                        yield str(environment.getattr(l_1_vpws_service, 'rd'))
                        yield '\n'
                    if t_8(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export')):
                        pass
                        yield '      route-target import export evpn '
                        yield str(environment.getattr(environment.getattr(l_1_vpws_service, 'route_targets'), 'import_export'))
                        yield '\n'
                    if t_8(environment.getattr(l_1_vpws_service, 'mpls_control_word'), True):
                        pass
                        yield '      mpls control-word\n'
                    if t_8(environment.getattr(l_1_vpws_service, 'label_flow'), True):
                        pass
                        yield '      label flow\n'
                    if t_8(environment.getattr(l_1_vpws_service, 'mtu')):
                        pass
                        yield '      mtu '
                        yield str(environment.getattr(l_1_vpws_service, 'mtu'))
                        yield '\n'
                    for l_2_pw in t_3(environment.getattr(l_1_vpws_service, 'pseudowires'), 'name'):
                        _loop_vars = {}
                        pass
                        if ((t_8(environment.getattr(l_2_pw, 'name')) and t_8(environment.getattr(l_2_pw, 'id_local'))) and t_8(environment.getattr(l_2_pw, 'id_remote'))):
                            pass
                            yield '      !\n      pseudowire '
                            yield str(environment.getattr(l_2_pw, 'name'))
                            yield '\n         evpn vpws id local '
                            yield str(environment.getattr(l_2_pw, 'id_local'))
                            yield ' remote '
                            yield str(environment.getattr(l_2_pw, 'id_remote'))
                            yield '\n'
                    l_2_pw = missing
            l_1_vpws_service = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn')):
            pass
            yield '   !\n   address-family evpn\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'any'), True):
                pass
                yield '      bgp additional-paths send any\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'backup'), True):
                pass
                yield '      bgp additional-paths send backup\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'ecmp'), True):
                pass
                yield '      bgp additional-paths send ecmp\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'ecmp_limit')):
                pass
                yield '      bgp additional-paths send ecmp limit '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'ecmp_limit'))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'limit')):
                pass
                yield '      bgp additional-paths send limit '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'bgp_additional_paths'), 'send'), 'limit'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_unchanged'), True):
                pass
                yield '      bgp next-hop-unchanged\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'enabled'), False):
                pass
                yield '      no host-flap detection\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'enabled'), True):
                pass
                l_0_hostflap_detection_cli = ''
                context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                context.exported_vars.add('hostflap_detection_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' window ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'window'), ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'threshold')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' threshold ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'threshold'), ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout')):
                    pass
                    l_0_hostflap_detection_cli = str_join(((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli), ' expiry timeout ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'evpn_hostflap_detection'), 'expiry_timeout'), ' seconds', ))
                    context.vars['hostflap_detection_cli'] = l_0_hostflap_detection_cli
                    context.exported_vars.add('hostflap_detection_cli')
                if ((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli) != ''):
                    pass
                    yield '      host-flap detection'
                    yield str((undefined(name='hostflap_detection_cli') if l_0_hostflap_detection_cli is missing else l_0_hostflap_detection_cli))
                    yield '\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'domain_identifier'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'encapsulation'), 'mpls'):
                pass
                l_0_evpn_neighbor_default_encap_cli = 'neighbor default encapsulation mpls'
                context.vars['evpn_neighbor_default_encap_cli'] = l_0_evpn_neighbor_default_encap_cli
                context.exported_vars.add('evpn_neighbor_default_encap_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_source_interface')):
                    pass
                    l_0_evpn_neighbor_default_encap_cli = str_join(((undefined(name='evpn_neighbor_default_encap_cli') if l_0_evpn_neighbor_default_encap_cli is missing else l_0_evpn_neighbor_default_encap_cli), ' next-hop-self source-interface ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_source_interface'), ))
                    context.vars['evpn_neighbor_default_encap_cli'] = l_0_evpn_neighbor_default_encap_cli
                    context.exported_vars.add('evpn_neighbor_default_encap_cli')
                yield '      '
                yield str((undefined(name='evpn_neighbor_default_encap_cli') if l_0_evpn_neighbor_default_encap_cli is missing else l_0_evpn_neighbor_default_encap_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_mpls_resolution_ribs')):
                pass
                l_0_evpn_mpls_resolution_ribs = []
                context.vars['evpn_mpls_resolution_ribs'] = l_0_evpn_mpls_resolution_ribs
                context.exported_vars.add('evpn_mpls_resolution_ribs')
                for l_1_rib in environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop_mpls_resolution_ribs'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib-colored'):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), 'tunnel-rib-colored system-colored-tunnel-rib', _loop_vars=_loop_vars)
                    elif (t_8(environment.getattr(l_1_rib, 'rib_type'), 'tunnel-rib') and t_8(environment.getattr(l_1_rib, 'rib_name'))):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), str_join(('tunnel-rib ', environment.getattr(l_1_rib, 'rib_name'), )), _loop_vars=_loop_vars)
                    elif t_8(environment.getattr(l_1_rib, 'rib_type')):
                        pass
                        context.call(environment.getattr((undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), 'append'), environment.getattr(l_1_rib, 'rib_type'), _loop_vars=_loop_vars)
                l_1_rib = missing
                if (undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs):
                    pass
                    yield '      next-hop mpls resolution ribs '
                    yield str(t_5(context.eval_ctx, (undefined(name='evpn_mpls_resolution_ribs') if l_0_evpn_mpls_resolution_ribs is missing else l_0_evpn_mpls_resolution_ribs), ' '))
                    yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'peer_groups'), 'name'):
                l_1_peer_group_default_route_cli = resolve('peer_group_default_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'enabled'), True):
                    pass
                    l_1_peer_group_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-route', ))
                    _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    yield '      '
                    yield str((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'any'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'domain_remote'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' domain remote\n'
                if t_8(environment.getattr(l_1_peer_group, 'encapsulation')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' encapsulation '
                    yield str(environment.getattr(l_1_peer_group, 'encapsulation'))
                    yield '\n'
            l_1_peer_group = l_1_peer_group_default_route_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_route_cli = resolve('neighbor_default_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'enabled'), True):
                    pass
                    l_1_neighbor_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-route', ))
                    _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli))
                    yield '\n'
            l_1_neighbor = l_1_neighbor_default_route_cli = missing
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'next_hop'), 'resolution_disabled'), True):
                pass
                yield '      next-hop resolution disabled\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'enable'), True):
                pass
                l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = 'neighbor default next-hop-self received-evpn-routes route-type ip-prefix'
                context.vars['evpn_neighbor_default_nhs_received_evpn_routes_cli'] = l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli
                context.exported_vars.add('evpn_neighbor_default_nhs_received_evpn_routes_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'neighbor_default'), 'next_hop_self_received_evpn_routes'), 'inter_domain'), True):
                    pass
                    l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli = str_join(((undefined(name='evpn_neighbor_default_nhs_received_evpn_routes_cli') if l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli is missing else l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli), ' inter-domain', ))
                    context.vars['evpn_neighbor_default_nhs_received_evpn_routes_cli'] = l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli
                    context.exported_vars.add('evpn_neighbor_default_nhs_received_evpn_routes_cli')
                yield '      '
                yield str((undefined(name='evpn_neighbor_default_nhs_received_evpn_routes_cli') if l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli is missing else l_0_evpn_neighbor_default_nhs_received_evpn_routes_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_ethernet_segment_ip_mass_withdraw'), True):
                pass
                yield '      route import ethernet-segment ip mass-withdraw\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'export_ethernet_segment_ip_mass_withdraw'), True):
                pass
                yield '      route export ethernet-segment ip mass-withdraw\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'layer_2_fec_in_place_update'), 'enabled'), True):
                pass
                l_0_layer2_cli = 'layer-2 fec in-place update'
                context.vars['layer2_cli'] = l_0_layer2_cli
                context.exported_vars.add('layer2_cli')
                if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'layer_2_fec_in_place_update'), 'timeout')):
                    pass
                    l_0_layer2_cli = str_join(((undefined(name='layer2_cli') if l_0_layer2_cli is missing else l_0_layer2_cli), ' timeout ', environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'layer_2_fec_in_place_update'), 'timeout'), ' seconds', ))
                    context.vars['layer2_cli'] = l_0_layer2_cli
                    context.exported_vars.add('layer2_cli')
                yield '      '
                yield str((undefined(name='layer2_cli') if l_0_layer2_cli is missing else l_0_layer2_cli))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_evpn'), 'route'), 'import_overlay_index_gateway'), True):
                pass
                yield '      route import overlay-index gateway\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4')):
            pass
            yield '   !\n   address-family flow-spec ipv4\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv4'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6')):
            pass
            yield '   !\n   address-family flow-spec ipv6\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_flow_spec_ipv6'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_rtc')):
            pass
            yield '   !\n   address-family rt-membership\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_rtc'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_9(environment.getattr(l_1_peer_group, 'default_route_target')):
                    pass
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route_target'), 'only'), True):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' default-route-target only\n'
                    else:
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_1_peer_group, 'name'))
                        yield ' default-route-target\n'
                if t_9(environment.getattr(environment.getattr(l_1_peer_group, 'default_route_target'), 'encoding_origin_as_omit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' default-route-target encoding origin-as omit\n'
            l_1_peer_group = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4')):
            pass
            yield '   !\n   address-family ipv4\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'peer_groups'), 'name'):
                l_1_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                l_1_nexthop_v6_cli = resolve('nexthop_v6_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'default_originate')):
                    pass
                    l_1_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map')):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_originate'), 'always'), True):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'next_hop'), 'address_family_ipv6'), 'enabled'), True):
                    pass
                    l_1_nexthop_v6_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' next-hop address-family ipv6', ))
                    _loop_vars['nexthop_v6_cli'] = l_1_nexthop_v6_cli
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'next_hop'), 'address_family_ipv6'), 'originate'), True):
                        pass
                        l_1_nexthop_v6_cli = str_join(((undefined(name='nexthop_v6_cli') if l_1_nexthop_v6_cli is missing else l_1_nexthop_v6_cli), ' originate', ))
                        _loop_vars['nexthop_v6_cli'] = l_1_nexthop_v6_cli
                    yield '      '
                    yield str((undefined(name='nexthop_v6_cli') if l_1_nexthop_v6_cli is missing else l_1_nexthop_v6_cli))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'next_hop'), 'address_family_ipv6_originate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' next-hop address-family ipv6 originate\n'
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = l_1_neighbor_default_originate_cli = l_1_nexthop_v6_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'default_originate')):
                    pass
                    l_1_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map')):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_originate'), 'always'), True):
                        pass
                        l_1_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_1_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_1_neighbor_default_originate_cli is missing else l_1_neighbor_default_originate_cli))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = l_1_neighbor_default_originate_cli = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield '\n'
            l_1_network = missing
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'redistribute_internal'), True):
                pass
                yield '      bgp redistribute-internal\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'bgp'), 'redistribute_internal'), False):
                pass
                yield '      no bgp redistribute-internal\n'
            for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4'), 'redistribute_routes'), 'source_protocol'):
                l_1_redistribute_route_cli = resolve('redistribute_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                        pass
                        if t_8(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'bgp'):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif (t_8(environment.getattr(l_1_redistribute_route, 'include_leaked')) and (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'ospf', 'ospfv3'])):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_8(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                        pass
                        if t_8(environment.getattr(l_1_redistribute_route, 'rcf')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
            l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast')):
            pass
            yield '   !\n   address-family ipv4 multicast\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
            for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_multicast'), 'redistribute_routes'), 'source_protocol'):
                l_1_redistribute_route_cli = resolve('redistribute_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                        pass
                        if t_8(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (t_8(environment.getattr(l_1_redistribute_route, 'include_leaked')) and (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_8(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif ((environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis') and t_8(environment.getattr(l_1_redistribute_route, 'rcf'))):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
            l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te')):
            pass
            yield '   !\n   address-family ipv4 sr-te\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv4_sr_te'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6')):
            pass
            yield '   !\n   address-family ipv6\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_peer_group, 'prefix_list_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'prefix_list_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'prefix_list_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' prefix-list '
                    yield str(environment.getattr(l_1_neighbor, 'prefix_list_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
            l_1_neighbor = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_1_network, 'prefix'))
                    yield '\n'
            l_1_network = missing
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'redistribute_internal'), True):
                pass
                yield '      bgp redistribute-internal\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'bgp'), 'redistribute_internal'), False):
                pass
                yield '      no bgp redistribute-internal\n'
            for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6'), 'redistribute_routes'), 'source_protocol'):
                l_1_redistribute_route_cli = resolve('redistribute_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'ospfv3'):
                        pass
                        if t_8(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'bgp'):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif t_8(environment.getattr(l_1_redistribute_route, 'include_leaked')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_8(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                        pass
                        if t_8(environment.getattr(l_1_redistribute_route, 'rcf')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
            l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast')):
            pass
            yield '   !\n   address-family ipv6 multicast\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
            for l_1_network in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'networks'), 'prefix'):
                l_1_network_cli = missing
                _loop_vars = {}
                pass
                l_1_network_cli = str_join(('network ', environment.getattr(l_1_network, 'prefix'), ))
                _loop_vars['network_cli'] = l_1_network_cli
                if t_8(environment.getattr(l_1_network, 'route_map')):
                    pass
                    l_1_network_cli = str_join(((undefined(name='network_cli') if l_1_network_cli is missing else l_1_network_cli), ' route-map ', environment.getattr(l_1_network, 'route_map'), ))
                    _loop_vars['network_cli'] = l_1_network_cli
                yield '      '
                yield str((undefined(name='network_cli') if l_1_network_cli is missing else l_1_network_cli))
                yield '\n'
            l_1_network = l_1_network_cli = missing
            for l_1_redistribute_route in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_multicast'), 'redistribute_routes'), 'source_protocol'):
                l_1_redistribute_route_cli = resolve('redistribute_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_redistribute_route, 'source_protocol')):
                    pass
                    l_1_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_1_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (environment.getattr(l_1_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                        pass
                        if t_8(environment.getattr(l_1_redistribute_route, 'ospf_route_type')):
                            pass
                            l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' match ', environment.getattr(l_1_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if (t_8(environment.getattr(l_1_redistribute_route, 'include_leaked')) and (environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    if t_8(environment.getattr(l_1_redistribute_route, 'route_map')):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' route-map ', environment.getattr(l_1_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    elif ((environment.getattr(l_1_redistribute_route, 'source_protocol') == 'isis') and t_8(environment.getattr(l_1_redistribute_route, 'rcf'))):
                        pass
                        l_1_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli), ' rcf ', environment.getattr(l_1_redistribute_route, 'rcf'), ))
                        _loop_vars['redistribute_route_cli'] = l_1_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_1_redistribute_route_cli is missing else l_1_redistribute_route_cli))
                    yield '\n'
            l_1_redistribute_route = l_1_redistribute_route_cli = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te')):
            pass
            yield '   !\n   address-family ipv6 sr-te\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_ipv6_sr_te'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state')):
            pass
            yield '   !\n   address-family link-state\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                pass
                yield '      bgp missing-policy direction in action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                pass
                yield '      bgp missing-policy direction out action '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(l_1_peer_group, 'missing_policy'), 'direction_out_action'))
                    yield '\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(l_1_neighbor, 'missing_policy'), 'direction_out_action'))
                    yield '\n'
            l_1_neighbor = missing
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection')):
                pass
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'producer'), True):
                    pass
                    yield '      path-selection\n'
                if (t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'consumer'), True) or t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'propagator'), True)):
                    pass
                    l_0_path_selection_roles = 'path-selection role'
                    context.vars['path_selection_roles'] = l_0_path_selection_roles
                    context.exported_vars.add('path_selection_roles')
                    if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'consumer'), True):
                        pass
                        l_0_path_selection_roles = str_join(((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), ' consumer', ))
                        context.vars['path_selection_roles'] = l_0_path_selection_roles
                        context.exported_vars.add('path_selection_roles')
                    if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_link_state'), 'path_selection'), 'roles'), 'propagator'), True):
                        pass
                        l_0_path_selection_roles = str_join(((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles), ' propagator', ))
                        context.vars['path_selection_roles'] = l_0_path_selection_roles
                        context.exported_vars.add('path_selection_roles')
                    yield '      '
                    yield str((undefined(name='path_selection_roles') if l_0_path_selection_roles is missing else l_0_path_selection_roles))
                    yield '\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection')):
            pass
            yield '   !\n   address-family path-selection\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'receive'), True):
                pass
                yield '      bgp additional-paths receive\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'any'), True):
                pass
                yield '      bgp additional-paths send any\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'backup'), True):
                pass
                yield '      bgp additional-paths send backup\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'ecmp'), True):
                pass
                yield '      bgp additional-paths send ecmp\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit')):
                pass
                yield '      bgp additional-paths send ecmp limit '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit'))
                yield '\n'
            elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'limit')):
                pass
                yield '      bgp additional-paths send limit '
                yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'bgp'), 'additional_paths'), 'send'), 'limit'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'peer_groups'), 'name'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_peer_group, 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
            l_1_peer_group = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_path_selection'), 'neighbors'), 'ip_address'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'receive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_1_neighbor, 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
            l_1_neighbor = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4')):
            pass
            yield '   !\n   address-family vpn-ipv4\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'domain_identifier'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'peer_groups'), 'name'):
                l_1_peer_group_default_route_cli = resolve('peer_group_default_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'enabled'), True):
                    pass
                    l_1_peer_group_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-route', ))
                    _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    yield '      '
                    yield str((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli))
                    yield '\n'
            l_1_peer_group = l_1_peer_group_default_route_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_route_cli = resolve('neighbor_default_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'enabled'), True):
                    pass
                    l_1_neighbor_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-route', ))
                    _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli))
                    yield '\n'
            l_1_neighbor = l_1_neighbor_default_route_cli = missing
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface')):
                pass
                yield '      neighbor default encapsulation mpls next-hop-self source-interface '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv4'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6')):
            pass
            yield '   !\n   address-family vpn-ipv6\n'
            if t_8(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'domain_identifier')):
                pass
                yield '      domain identifier '
                yield str(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'domain_identifier'))
                yield '\n'
            for l_1_peer_group in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'peer_groups'), 'name'):
                l_1_peer_group_default_route_cli = resolve('peer_group_default_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_peer_group, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_peer_group, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_peer_group, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_peer_group, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_peer_group, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_peer_group, 'name'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_peer_group, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'enabled'), True):
                    pass
                    l_1_peer_group_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_peer_group, 'name'), ' default-route', ))
                    _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    if t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'rcf'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    elif t_8(environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map')):
                        pass
                        l_1_peer_group_default_route_cli = str_join(((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_peer_group, 'default_route'), 'route_map'), ))
                        _loop_vars['peer_group_default_route_cli'] = l_1_peer_group_default_route_cli
                    yield '      '
                    yield str((undefined(name='peer_group_default_route_cli') if l_1_peer_group_default_route_cli is missing else l_1_peer_group_default_route_cli))
                    yield '\n'
            l_1_peer_group = l_1_peer_group_default_route_cli = missing
            for l_1_neighbor in t_3(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbors'), 'ip_address'):
                l_1_neighbor_default_route_cli = resolve('neighbor_default_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_1_neighbor, 'activate'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                elif t_8(environment.getattr(l_1_neighbor, 'activate'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' activate\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_1_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_1_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf in '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_in'))
                    yield '\n'
                if t_8(environment.getattr(l_1_neighbor, 'rcf_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_1_neighbor, 'ip_address'))
                    yield ' rcf out '
                    yield str(environment.getattr(l_1_neighbor, 'rcf_out'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'enabled'), True):
                    pass
                    l_1_neighbor_default_route_cli = str_join(('neighbor ', environment.getattr(l_1_neighbor, 'ip_address'), ' default-route', ))
                    _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    if t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' rcf ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'rcf'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    elif t_8(environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map')):
                        pass
                        l_1_neighbor_default_route_cli = str_join(((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli), ' route-map ', environment.getattr(environment.getattr(l_1_neighbor, 'default_route'), 'route_map'), ))
                        _loop_vars['neighbor_default_route_cli'] = l_1_neighbor_default_route_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_route_cli') if l_1_neighbor_default_route_cli is missing else l_1_neighbor_default_route_cli))
                    yield '\n'
            l_1_neighbor = l_1_neighbor_default_route_cli = missing
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface')):
                pass
                yield '      neighbor default encapsulation mpls next-hop-self source-interface '
                yield str(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'neighbor_default_encapsulation_mpls_next_hop_self'), 'source_interface'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'address_family_vpn_ipv6'), 'route'), 'import_match_failure_action'), 'discard'):
                pass
                yield '      route import match-failure action discard\n'
        for l_1_vrf in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'vrfs'), 'name'):
            l_1_tmp_vrf_neighbor_prefix_list_in = l_1_tmp_vrf_neighbor_prefix_list_out = missing
            _loop_vars = {}
            pass
            yield '   !\n   vrf '
            yield str(environment.getattr(l_1_vrf, 'name'))
            yield '\n'
            if t_8(environment.getattr(l_1_vrf, 'rd')):
                pass
                yield '      rd '
                yield str(environment.getattr(l_1_vrf, 'rd'))
                yield '\n'
            if t_8(environment.getattr(l_1_vrf, 'evpn_multicast'), True):
                pass
                yield '      evpn multicast\n'
                if t_8(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'algorithm')):
                    pass
                    if (environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'algorithm') == 'preference'):
                        pass
                        if t_8(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'preference_value')):
                            pass
                            yield '         gateway dr election algorithm preference '
                            yield str(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'preference_value'))
                            yield '\n'
                    else:
                        pass
                        yield '         gateway dr election algorithm '
                        yield str(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_gateway_dr_election'), 'algorithm'))
                        yield '\n'
                if (t_8(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4')) and t_8(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4'), 'transit'), True)):
                    pass
                    yield '         address-family ipv4\n'
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'evpn_multicast_address_family'), 'ipv4'), 'transit'), True):
                        pass
                        yield '            transit\n'
            if t_8(environment.getattr(l_1_vrf, 'default_route_exports')):
                pass
                for l_2_default_route_export in environment.getattr(l_1_vrf, 'default_route_exports'):
                    l_2_vrf_default_route_export_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_vrf_default_route_export_cli = str_join(('default-route export ', environment.getattr(l_2_default_route_export, 'address_family'), ))
                    _loop_vars['vrf_default_route_export_cli'] = l_2_vrf_default_route_export_cli
                    if t_8(environment.getattr(l_2_default_route_export, 'always'), True):
                        pass
                        l_2_vrf_default_route_export_cli = str_join(((undefined(name='vrf_default_route_export_cli') if l_2_vrf_default_route_export_cli is missing else l_2_vrf_default_route_export_cli), ' always', ))
                        _loop_vars['vrf_default_route_export_cli'] = l_2_vrf_default_route_export_cli
                    if t_8(environment.getattr(l_2_default_route_export, 'rcf')):
                        pass
                        l_2_vrf_default_route_export_cli = str_join(((undefined(name='vrf_default_route_export_cli') if l_2_vrf_default_route_export_cli is missing else l_2_vrf_default_route_export_cli), ' rcf ', environment.getattr(l_2_default_route_export, 'rcf'), ))
                        _loop_vars['vrf_default_route_export_cli'] = l_2_vrf_default_route_export_cli
                    elif t_8(environment.getattr(l_2_default_route_export, 'route_map')):
                        pass
                        l_2_vrf_default_route_export_cli = str_join(((undefined(name='vrf_default_route_export_cli') if l_2_vrf_default_route_export_cli is missing else l_2_vrf_default_route_export_cli), ' route-map ', environment.getattr(l_2_default_route_export, 'route_map'), ))
                        _loop_vars['vrf_default_route_export_cli'] = l_2_vrf_default_route_export_cli
                    yield '      '
                    yield str((undefined(name='vrf_default_route_export_cli') if l_2_vrf_default_route_export_cli is missing else l_2_vrf_default_route_export_cli))
                    yield '\n'
                l_2_default_route_export = l_2_vrf_default_route_export_cli = missing
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'import')):
                pass
                for l_2_address_family in environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'import'):
                    _loop_vars = {}
                    pass
                    for l_3_route_target in environment.getattr(l_2_address_family, 'route_targets'):
                        _loop_vars = {}
                        pass
                        yield '      route-target import '
                        yield str(environment.getattr(l_2_address_family, 'address_family'))
                        yield ' '
                        yield str(l_3_route_target)
                        yield '\n'
                    l_3_route_target = missing
                    if (environment.getattr(l_2_address_family, 'address_family') in ['evpn', 'vpn-ipv4', 'vpn-ipv6']):
                        pass
                        if t_8(environment.getattr(l_2_address_family, 'rcf')):
                            pass
                            if (t_8(environment.getattr(l_2_address_family, 'vpn_route_filter_rcf')) and (environment.getattr(l_2_address_family, 'address_family') in ['vpn-ipv4', 'vpn-ipv6'])):
                                pass
                                yield '      route-target import '
                                yield str(environment.getattr(l_2_address_family, 'address_family'))
                                yield ' rcf '
                                yield str(environment.getattr(l_2_address_family, 'rcf'))
                                yield ' vpn-route filter-rcf '
                                yield str(environment.getattr(l_2_address_family, 'vpn_route_filter_rcf'))
                                yield '\n'
                            else:
                                pass
                                yield '      route-target import '
                                yield str(environment.getattr(l_2_address_family, 'address_family'))
                                yield ' rcf '
                                yield str(environment.getattr(l_2_address_family, 'rcf'))
                                yield '\n'
                        if t_8(environment.getattr(l_2_address_family, 'route_map')):
                            pass
                            yield '      route-target import '
                            yield str(environment.getattr(l_2_address_family, 'address_family'))
                            yield ' route-map '
                            yield str(environment.getattr(l_2_address_family, 'route_map'))
                            yield '\n'
                l_2_address_family = missing
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'export')):
                pass
                for l_2_address_family in environment.getattr(environment.getattr(l_1_vrf, 'route_targets'), 'export'):
                    _loop_vars = {}
                    pass
                    for l_3_route_target in environment.getattr(l_2_address_family, 'route_targets'):
                        _loop_vars = {}
                        pass
                        yield '      route-target export '
                        yield str(environment.getattr(l_2_address_family, 'address_family'))
                        yield ' '
                        yield str(l_3_route_target)
                        yield '\n'
                    l_3_route_target = missing
                    if (environment.getattr(l_2_address_family, 'address_family') in ['evpn', 'vpn-ipv4', 'vpn-ipv6']):
                        pass
                        if t_8(environment.getattr(l_2_address_family, 'rcf')):
                            pass
                            if (t_8(environment.getattr(l_2_address_family, 'vpn_route_filter_rcf')) and (environment.getattr(l_2_address_family, 'address_family') in ['vpn-ipv4', 'vpn-ipv6'])):
                                pass
                                yield '      route-target export '
                                yield str(environment.getattr(l_2_address_family, 'address_family'))
                                yield ' rcf '
                                yield str(environment.getattr(l_2_address_family, 'rcf'))
                                yield ' vpn-route filter-rcf '
                                yield str(environment.getattr(l_2_address_family, 'vpn_route_filter_rcf'))
                                yield '\n'
                            else:
                                pass
                                yield '      route-target export '
                                yield str(environment.getattr(l_2_address_family, 'address_family'))
                                yield ' rcf '
                                yield str(environment.getattr(l_2_address_family, 'rcf'))
                                yield '\n'
                        if t_8(environment.getattr(l_2_address_family, 'route_map')):
                            pass
                            yield '      route-target export '
                            yield str(environment.getattr(l_2_address_family, 'address_family'))
                            yield ' route-map '
                            yield str(environment.getattr(l_2_address_family, 'route_map'))
                            yield '\n'
                l_2_address_family = missing
            if t_8(environment.getattr(l_1_vrf, 'router_id')):
                pass
                yield '      router-id '
                yield str(environment.getattr(l_1_vrf, 'router_id'))
                yield '\n'
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'updates'), 'wait_for_convergence'), True):
                pass
                yield '      update wait-for-convergence\n'
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'updates'), 'wait_install'), True):
                pass
                yield '      update wait-install\n'
            if t_8(environment.getattr(l_1_vrf, 'timers')):
                pass
                yield '      timers bgp '
                yield str(environment.getattr(l_1_vrf, 'timers'))
                yield '\n'
            if t_8(environment.getattr(l_1_vrf, 'listen_ranges')):
                pass
                def t_12(fiter):
                    for l_2_listen_range in fiter:
                        if ((t_8(environment.getattr(l_2_listen_range, 'peer_group')) and t_8(environment.getattr(l_2_listen_range, 'prefix'))) and (t_8(environment.getattr(l_2_listen_range, 'peer_filter')) or t_8(environment.getattr(l_2_listen_range, 'remote_as')))):
                            yield l_2_listen_range
                for l_2_listen_range in t_12(t_3(environment.getattr(l_1_vrf, 'listen_ranges'), 'peer_group')):
                    l_2_listen_range_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_listen_range_cli = str_join(('bgp listen range ', environment.getattr(l_2_listen_range, 'prefix'), ))
                    _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    if t_8(environment.getattr(l_2_listen_range, 'peer_id_include_router_id'), True):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-id include router-id', ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-group ', environment.getattr(l_2_listen_range, 'peer_group'), ))
                    _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    if t_8(environment.getattr(l_2_listen_range, 'peer_filter')):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' peer-filter ', environment.getattr(l_2_listen_range, 'peer_filter'), ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    elif t_8(environment.getattr(l_2_listen_range, 'remote_as')):
                        pass
                        l_2_listen_range_cli = str_join(((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli), ' remote-as ', environment.getattr(l_2_listen_range, 'remote_as'), ))
                        _loop_vars['listen_range_cli'] = l_2_listen_range_cli
                    yield '      '
                    yield str((undefined(name='listen_range_cli') if l_2_listen_range_cli is missing else l_2_listen_range_cli))
                    yield '\n'
                l_2_listen_range = l_2_listen_range_cli = missing
            for l_2_neighbor_interface in t_3(environment.getattr(l_1_vrf, 'neighbor_interfaces'), 'name'):
                _loop_vars = {}
                pass
                if (t_8(environment.getattr(l_2_neighbor_interface, 'peer_group')) and t_8(environment.getattr(l_2_neighbor_interface, 'remote_as'))):
                    pass
                    yield '      neighbor interface '
                    yield str(environment.getattr(l_2_neighbor_interface, 'name'))
                    yield ' peer-group '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_group'))
                    yield ' remote-as '
                    yield str(environment.getattr(l_2_neighbor_interface, 'remote_as'))
                    yield '\n'
                elif (t_8(environment.getattr(l_2_neighbor_interface, 'peer_group')) and t_8(environment.getattr(l_2_neighbor_interface, 'peer_filter'))):
                    pass
                    yield '      neighbor interface '
                    yield str(environment.getattr(l_2_neighbor_interface, 'name'))
                    yield ' peer-group '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_group'))
                    yield ' peer-filter '
                    yield str(environment.getattr(l_2_neighbor_interface, 'peer_filter'))
                    yield '\n'
            l_2_neighbor_interface = missing
            l_1_tmp_vrf_neighbor_prefix_list_in = {}
            _loop_vars['tmp_vrf_neighbor_prefix_list_in'] = l_1_tmp_vrf_neighbor_prefix_list_in
            l_1_tmp_vrf_neighbor_prefix_list_out = {}
            _loop_vars['tmp_vrf_neighbor_prefix_list_out'] = l_1_tmp_vrf_neighbor_prefix_list_out
            for l_2_neighbor in t_3(environment.getattr(l_1_vrf, 'neighbors'), 'ip_address'):
                l_2_remove_private_as_cli = resolve('remove_private_as_cli')
                l_2_remove_private_as_ingress_cli = resolve('remove_private_as_ingress_cli')
                l_2_hide_passwords = resolve('hide_passwords')
                l_2_neighbor_ebgp_multihop_cli = resolve('neighbor_ebgp_multihop_cli')
                l_2_allowas_in_cli = resolve('allowas_in_cli')
                l_2_neighbor_rib_in_pre_policy_retain_cli = resolve('neighbor_rib_in_pre_policy_retain_cli')
                l_2_maximum_routes_cli = resolve('maximum_routes_cli')
                l_2_neighbor_default_originate_cli = resolve('neighbor_default_originate_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_2_neighbor, 'remote_as')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remote-as '
                    yield str(environment.getattr(l_2_neighbor, 'remote_as'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'peer_group')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' peer group '
                    yield str(environment.getattr(l_2_neighbor, 'peer_group'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'enabled'), True):
                    pass
                    l_2_remove_private_as_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' remove-private-as', ))
                    _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'all'), True):
                        pass
                        l_2_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli), ' all', ))
                        _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                        if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'replace_as'), True):
                            pass
                            l_2_remove_private_as_cli = str_join(((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli), ' replace-as', ))
                            _loop_vars['remove_private_as_cli'] = l_2_remove_private_as_cli
                    yield '      '
                    yield str((undefined(name='remove_private_as_cli') if l_2_remove_private_as_cli is missing else l_2_remove_private_as_cli))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as'), 'enabled'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remove-private-as\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'enabled'), True):
                    pass
                    l_2_remove_private_as_ingress_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' remove-private-as ingress', ))
                    _loop_vars['remove_private_as_ingress_cli'] = l_2_remove_private_as_ingress_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'replace_as'), True):
                        pass
                        l_2_remove_private_as_ingress_cli = str_join(((undefined(name='remove_private_as_ingress_cli') if l_2_remove_private_as_ingress_cli is missing else l_2_remove_private_as_ingress_cli), ' replace-as', ))
                        _loop_vars['remove_private_as_ingress_cli'] = l_2_remove_private_as_ingress_cli
                    yield '      '
                    yield str((undefined(name='remove_private_as_ingress_cli') if l_2_remove_private_as_ingress_cli is missing else l_2_remove_private_as_ingress_cli))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(l_2_neighbor, 'remove_private_as_ingress'), 'enabled'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' remove-private-as ingress\n'
                if t_8(environment.getattr(l_2_neighbor, 'password')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' password 7 '
                    yield str(t_2(environment.getattr(l_2_neighbor, 'password'), (undefined(name='hide_passwords') if l_2_hide_passwords is missing else l_2_hide_passwords)))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'passive'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' passive\n'
                if t_8(environment.getattr(l_2_neighbor, 'weight')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' weight '
                    yield str(environment.getattr(l_2_neighbor, 'weight'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'as_path'), 'remote_as_replace_out'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' as-path remote-as replace out\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'as_path'), 'prepend_own_disabled'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' as-path prepend-own disabled\n'
                if t_8(environment.getattr(l_2_neighbor, 'local_as')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' local-as '
                    yield str(environment.getattr(l_2_neighbor, 'local_as'))
                    yield ' no-prepend replace-as\n'
                if t_8(environment.getattr(l_2_neighbor, 'description')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' description '
                    yield str(environment.getattr(l_2_neighbor, 'description'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'ebgp_multihop')):
                    pass
                    l_2_neighbor_ebgp_multihop_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' ebgp-multihop', ))
                    _loop_vars['neighbor_ebgp_multihop_cli'] = l_2_neighbor_ebgp_multihop_cli
                    if t_10(environment.getattr(l_2_neighbor, 'ebgp_multihop')):
                        pass
                        l_2_neighbor_ebgp_multihop_cli = str_join(((undefined(name='neighbor_ebgp_multihop_cli') if l_2_neighbor_ebgp_multihop_cli is missing else l_2_neighbor_ebgp_multihop_cli), ' ', environment.getattr(l_2_neighbor, 'ebgp_multihop'), ))
                        _loop_vars['neighbor_ebgp_multihop_cli'] = l_2_neighbor_ebgp_multihop_cli
                    yield '      '
                    yield str((undefined(name='neighbor_ebgp_multihop_cli') if l_2_neighbor_ebgp_multihop_cli is missing else l_2_neighbor_ebgp_multihop_cli))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'next_hop_self'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' next-hop-self\n'
                if t_8(environment.getattr(l_2_neighbor, 'bfd'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' bfd\n'
                    if ((t_8(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'interval')) and t_8(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'min_rx'))) and t_8(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'multiplier'))):
                        pass
                        yield '      neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' bfd interval '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'interval'))
                        yield ' min-rx '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'min_rx'))
                        yield ' multiplier '
                        yield str(environment.getattr(environment.getattr(l_2_neighbor, 'bfd_timers'), 'multiplier'))
                        yield '\n'
                elif (t_8(environment.getattr(l_2_neighbor, 'bfd'), False) and t_8(environment.getattr(l_2_neighbor, 'peer_group'))):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' bfd\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'enabled'), True):
                    pass
                    l_2_allowas_in_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' allowas-in', ))
                    _loop_vars['allowas_in_cli'] = l_2_allowas_in_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times')):
                        pass
                        l_2_allowas_in_cli = str_join(((undefined(name='allowas_in_cli') if l_2_allowas_in_cli is missing else l_2_allowas_in_cli), ' ', environment.getattr(environment.getattr(l_2_neighbor, 'allowas_in'), 'times'), ))
                        _loop_vars['allowas_in_cli'] = l_2_allowas_in_cli
                    yield '      '
                    yield str((undefined(name='allowas_in_cli') if l_2_allowas_in_cli is missing else l_2_allowas_in_cli))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), True):
                    pass
                    l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'all'), True):
                        pass
                        l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli), ' all', ))
                        _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    yield '      '
                    yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(l_2_neighbor, 'rib_in_pre_policy_retain'), 'enabled'), False):
                    pass
                    l_2_neighbor_rib_in_pre_policy_retain_cli = str_join(('no neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' rib-in pre-policy retain', ))
                    _loop_vars['neighbor_rib_in_pre_policy_retain_cli'] = l_2_neighbor_rib_in_pre_policy_retain_cli
                    yield '      '
                    yield str((undefined(name='neighbor_rib_in_pre_policy_retain_cli') if l_2_neighbor_rib_in_pre_policy_retain_cli is missing else l_2_neighbor_rib_in_pre_policy_retain_cli))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'timers')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' timers '
                    yield str(environment.getattr(l_2_neighbor, 'timers'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'shutdown'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' shutdown\n'
                if t_8(environment.getattr(l_2_neighbor, 'send_community'), 'all'):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' send-community\n'
                elif t_8(environment.getattr(l_2_neighbor, 'send_community')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' send-community '
                    yield str(environment.getattr(l_2_neighbor, 'send_community'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'route_reflector_client'), True):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-reflector-client\n'
                elif t_8(environment.getattr(l_2_neighbor, 'route_reflector_client'), False):
                    pass
                    yield '      no neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-reflector-client\n'
                if t_8(environment.getattr(l_2_neighbor, 'maximum_routes')):
                    pass
                    l_2_maximum_routes_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' maximum-routes ', environment.getattr(l_2_neighbor, 'maximum_routes'), ))
                    _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    if t_8(environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit')):
                        pass
                        l_2_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli), ' warning-limit ', environment.getattr(l_2_neighbor, 'maximum_routes_warning_limit'), ))
                        _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    if t_8(environment.getattr(l_2_neighbor, 'maximum_routes_warning_only'), True):
                        pass
                        l_2_maximum_routes_cli = str_join(((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli), ' warning-only', ))
                        _loop_vars['maximum_routes_cli'] = l_2_maximum_routes_cli
                    yield '      '
                    yield str((undefined(name='maximum_routes_cli') if l_2_maximum_routes_cli is missing else l_2_maximum_routes_cli))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'default_originate')):
                    pass
                    l_2_neighbor_default_originate_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' default-originate', ))
                    _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'route_map')):
                        pass
                        l_2_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli), ' route-map ', environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'route_map'), ))
                        _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    if t_8(environment.getattr(environment.getattr(l_2_neighbor, 'default_originate'), 'always'), True):
                        pass
                        l_2_neighbor_default_originate_cli = str_join(((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli), ' always', ))
                        _loop_vars['neighbor_default_originate_cli'] = l_2_neighbor_default_originate_cli
                    yield '      '
                    yield str((undefined(name='neighbor_default_originate_cli') if l_2_neighbor_default_originate_cli is missing else l_2_neighbor_default_originate_cli))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'update_source')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' update-source '
                    yield str(environment.getattr(l_2_neighbor, 'update_source'))
                    yield '\n'
                if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                    yield ' out\n'
                if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                    pass
                    yield '      neighbor '
                    yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                    yield ' in\n'
                if t_8(environment.getattr(l_2_neighbor, 'prefix_list_in')):
                    pass
                    context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), 'update'), {environment.getattr(l_2_neighbor, 'ip_address'): environment.getattr(l_2_neighbor, 'prefix_list_in')}, _loop_vars=_loop_vars)
                if t_8(environment.getattr(l_2_neighbor, 'prefix_list_out')):
                    pass
                    context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), 'update'), {environment.getattr(l_2_neighbor, 'ip_address'): environment.getattr(l_2_neighbor, 'prefix_list_out')}, _loop_vars=_loop_vars)
            l_2_neighbor = l_2_remove_private_as_cli = l_2_remove_private_as_ingress_cli = l_2_hide_passwords = l_2_neighbor_ebgp_multihop_cli = l_2_allowas_in_cli = l_2_neighbor_rib_in_pre_policy_retain_cli = l_2_maximum_routes_cli = l_2_neighbor_default_originate_cli = missing
            for l_2_network in t_3(environment.getattr(l_1_vrf, 'networks'), 'prefix'):
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_2_network, 'route_map')):
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_2_network, 'prefix'))
                    yield ' route-map '
                    yield str(environment.getattr(l_2_network, 'route_map'))
                    yield '\n'
                else:
                    pass
                    yield '      network '
                    yield str(environment.getattr(l_2_network, 'prefix'))
                    yield '\n'
            l_2_network = missing
            if t_8(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'redistribute_internal'), True):
                pass
                yield '      bgp redistribute-internal\n'
            elif t_8(environment.getattr(environment.getattr(l_1_vrf, 'bgp'), 'redistribute_internal'), False):
                pass
                yield '      no bgp redistribute-internal\n'
            for l_2_aggregate_address in t_3(environment.getattr(l_1_vrf, 'aggregate_addresses'), 'prefix'):
                l_2_aggregate_address_cli = missing
                _loop_vars = {}
                pass
                l_2_aggregate_address_cli = str_join(('aggregate-address ', environment.getattr(l_2_aggregate_address, 'prefix'), ))
                _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'as_set'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' as-set', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'summary_only'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' summary-only', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'attribute_map')):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' attribute-map ', environment.getattr(l_2_aggregate_address, 'attribute_map'), ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'match_map')):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' match-map ', environment.getattr(l_2_aggregate_address, 'match_map'), ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                if t_8(environment.getattr(l_2_aggregate_address, 'advertise_only'), True):
                    pass
                    l_2_aggregate_address_cli = str_join(((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli), ' advertise-only', ))
                    _loop_vars['aggregate_address_cli'] = l_2_aggregate_address_cli
                yield '      '
                yield str((undefined(name='aggregate_address_cli') if l_2_aggregate_address_cli is missing else l_2_aggregate_address_cli))
                yield '\n'
            l_2_aggregate_address = l_2_aggregate_address_cli = missing
            for l_2_redistribute_route in t_3(environment.getattr(l_1_vrf, 'redistribute_routes'), 'source_protocol'):
                l_2_redistribute_route_cli = resolve('redistribute_route_cli')
                _loop_vars = {}
                pass
                if t_8(environment.getattr(l_2_redistribute_route, 'source_protocol')):
                    pass
                    l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                    _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    if (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                        pass
                        if t_8(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'bgp'):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    elif t_8(environment.getattr(l_2_redistribute_route, 'include_leaked')):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    if t_8(environment.getattr(l_2_redistribute_route, 'route_map')):
                        pass
                        l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    elif (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                        pass
                        if t_8(environment.getattr(l_2_redistribute_route, 'rcf')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                    yield '      '
                    yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                    yield '\n'
            l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4')):
                pass
                yield '      !\n      address-family flow-spec ipv4\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv4'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                l_2_neighbor = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6')):
                pass
                yield '      !\n      address-family flow-spec ipv6\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_flow_spec_ipv6'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                l_2_neighbor = missing
            if ((t_8(environment.getattr(l_1_vrf, 'address_family_ipv4')) or (undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in)) or (undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out)):
                pass
                yield '      !\n      address-family ipv4\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'install'), True):
                    pass
                    yield '         bgp additional-paths install\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                    pass
                    yield '         bgp additional-paths install ecmp-primary\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '         bgp additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '         bgp additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '         bgp additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '         bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '         bgp additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'neighbors'), 'ip_address'):
                    l_2_ipv6_originate_cli = resolve('ipv6_originate_cli')
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                    if t_8(environment.getattr(l_2_neighbor, 'rcf_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' rcf in '
                        yield str(environment.getattr(l_2_neighbor, 'rcf_in'))
                        yield '\n'
                    if t_8(environment.getattr(l_2_neighbor, 'rcf_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' rcf out '
                        yield str(environment.getattr(l_2_neighbor, 'rcf_out'))
                        yield '\n'
                    if t_8(environment.getattr(l_2_neighbor, 'prefix_list_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_in'))
                        yield ' in\n'
                        if t_8(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), environment.getattr(l_2_neighbor, 'ip_address'))):
                            pass
                            context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), 'pop'), environment.getattr(l_2_neighbor, 'ip_address'), _loop_vars=_loop_vars)
                    elif t_8(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), environment.getattr(l_2_neighbor, 'ip_address'))):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), 'pop'), environment.getattr(l_2_neighbor, 'ip_address'), _loop_vars=_loop_vars))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'prefix_list_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_out'))
                        yield ' out\n'
                        if t_8(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), environment.getattr(l_2_neighbor, 'ip_address'))):
                            pass
                            context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), 'pop'), environment.getattr(l_2_neighbor, 'ip_address'), _loop_vars=_loop_vars)
                    elif t_8(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), environment.getattr(l_2_neighbor, 'ip_address'))):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(context.call(environment.getattr((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), 'pop'), environment.getattr(l_2_neighbor, 'ip_address'), _loop_vars=_loop_vars))
                        yield ' out\n'
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled')):
                        pass
                        if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled'), True):
                            pass
                            l_2_ipv6_originate_cli = str_join(('neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' next-hop address-family ipv6', ))
                            _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                            if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'originate'), True):
                                pass
                                l_2_ipv6_originate_cli = str_join(((undefined(name='ipv6_originate_cli') if l_2_ipv6_originate_cli is missing else l_2_ipv6_originate_cli), ' originate', ))
                                _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                        elif t_8(environment.getattr(environment.getattr(environment.getattr(l_2_neighbor, 'next_hop'), 'address_family_ipv6'), 'enabled'), False):
                            pass
                            l_2_ipv6_originate_cli = str_join(('no neighbor ', environment.getattr(l_2_neighbor, 'ip_address'), ' next-hop address-family ipv6', ))
                            _loop_vars['ipv6_originate_cli'] = l_2_ipv6_originate_cli
                        yield '         '
                        yield str((undefined(name='ipv6_originate_cli') if l_2_ipv6_originate_cli is missing else l_2_ipv6_originate_cli))
                        yield '\n'
                l_2_neighbor = l_2_ipv6_originate_cli = missing
                for l_2_tmp_neighbor_ip in t_3((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in)):
                    _loop_vars = {}
                    pass
                    yield '         neighbor '
                    yield str(l_2_tmp_neighbor_ip)
                    yield ' prefix-list '
                    yield str(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_in') if l_1_tmp_vrf_neighbor_prefix_list_in is missing else l_1_tmp_vrf_neighbor_prefix_list_in), l_2_tmp_neighbor_ip))
                    yield ' in\n'
                l_2_tmp_neighbor_ip = missing
                for l_2_tmp_neighbor_ip in t_3((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out)):
                    _loop_vars = {}
                    pass
                    yield '         neighbor '
                    yield str(l_2_tmp_neighbor_ip)
                    yield ' prefix-list '
                    yield str(environment.getitem((undefined(name='tmp_vrf_neighbor_prefix_list_out') if l_1_tmp_vrf_neighbor_prefix_list_out is missing else l_1_tmp_vrf_neighbor_prefix_list_out), l_2_tmp_neighbor_ip))
                    yield ' out\n'
                l_2_tmp_neighbor_ip = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_8(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'redistribute_internal'), True):
                    pass
                    yield '         bgp redistribute-internal\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'bgp'), 'redistribute_internal'), False):
                    pass
                    yield '         no bgp redistribute-internal\n'
                for l_2_redistribute_route in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4'), 'redistribute_routes'), 'source_protocol'):
                    l_2_redistribute_route_cli = resolve('redistribute_route_cli')
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_redistribute_route, 'source_protocol')):
                        pass
                        l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                            pass
                            if t_8(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'bgp'):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif t_8(environment.getattr(l_2_redistribute_route, 'include_leaked')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_8(environment.getattr(l_2_redistribute_route, 'route_map')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                            pass
                            if t_8(environment.getattr(l_2_redistribute_route, 'rcf')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        yield '         '
                        yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                        yield '\n'
                l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast')):
                pass
                yield '      !\n      address-family ipv4 multicast\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_8(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
                for l_2_redistribute_route in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv4_multicast'), 'redistribute_routes'), 'source_protocol'):
                    l_2_redistribute_route_cli = resolve('redistribute_route_cli')
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_redistribute_route, 'source_protocol')):
                        pass
                        l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                            pass
                            if t_8(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (t_8(environment.getattr(l_2_redistribute_route, 'include_leaked')) and (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'isis')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_8(environment.getattr(l_2_redistribute_route, 'route_map')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'isis'):
                            pass
                            if t_8(environment.getattr(l_2_redistribute_route, 'rcf')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        yield '         '
                        yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                        yield '\n'
                l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_ipv6')):
                pass
                yield '      !\n      address-family ipv6\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'install'), True):
                    pass
                    yield '         bgp additional-paths install\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'install_ecmp_primary'), True):
                    pass
                    yield '         bgp additional-paths install ecmp-primary\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'any'), True):
                    pass
                    yield '         bgp additional-paths send any\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'backup'), True):
                    pass
                    yield '         bgp additional-paths send backup\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'ecmp'), True):
                    pass
                    yield '         bgp additional-paths send ecmp\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit')):
                    pass
                    yield '         bgp additional-paths send ecmp limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'ecmp_limit'))
                    yield '\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'limit')):
                    pass
                    yield '         bgp additional-paths send limit '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'additional_paths'), 'send'), 'limit'))
                    yield '\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                    if t_8(environment.getattr(l_2_neighbor, 'rcf_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' rcf in '
                        yield str(environment.getattr(l_2_neighbor, 'rcf_in'))
                        yield '\n'
                    if t_8(environment.getattr(l_2_neighbor, 'rcf_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' rcf out '
                        yield str(environment.getattr(l_2_neighbor, 'rcf_out'))
                        yield '\n'
                    if t_8(environment.getattr(l_2_neighbor, 'prefix_list_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'prefix_list_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' prefix-list '
                        yield str(environment.getattr(l_2_neighbor, 'prefix_list_out'))
                        yield ' out\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_8(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
                if t_8(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'redistribute_internal'), True):
                    pass
                    yield '         bgp redistribute-internal\n'
                elif t_8(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'bgp'), 'redistribute_internal'), False):
                    pass
                    yield '         no bgp redistribute-internal\n'
                for l_2_redistribute_route in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6'), 'redistribute_routes'), 'source_protocol'):
                    l_2_redistribute_route_cli = resolve('redistribute_route_cli')
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_redistribute_route, 'source_protocol')):
                        pass
                        l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'ospfv3'):
                            pass
                            if t_8(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'bgp'):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif t_8(environment.getattr(l_2_redistribute_route, 'include_leaked')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_8(environment.getattr(l_2_redistribute_route, 'route_map')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['connected', 'static', 'isis', 'user', 'dynamic']):
                            pass
                            if t_8(environment.getattr(l_2_redistribute_route, 'rcf')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        yield '      '
                        yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                        yield '\n'
                l_2_redistribute_route = l_2_redistribute_route_cli = missing
            if t_8(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast')):
                pass
                yield '      !\n      address-family ipv6 multicast\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action')):
                    pass
                    yield '         bgp missing-policy direction in action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_in_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action')):
                    pass
                    yield '         bgp missing-policy direction out action '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'missing_policy'), 'direction_out_action'))
                    yield '\n'
                if t_8(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'bgp'), 'additional_paths'), 'receive'), True):
                    pass
                    yield '         bgp additional-paths receive\n'
                for l_2_neighbor in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_2_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_2_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_2_neighbor, 'route_map_out'))
                        yield ' out\n'
                l_2_neighbor = missing
                for l_2_network in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'networks'), 'prefix'):
                    l_2_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_network_cli = str_join(('network ', environment.getattr(l_2_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_2_network_cli
                    if t_8(environment.getattr(l_2_network, 'route_map')):
                        pass
                        l_2_network_cli = str_join(((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli), ' route-map ', environment.getattr(l_2_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_2_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_2_network_cli is missing else l_2_network_cli))
                    yield '\n'
                l_2_network = l_2_network_cli = missing
                for l_2_redistribute_route in t_3(environment.getattr(environment.getattr(l_1_vrf, 'address_family_ipv6_multicast'), 'redistribute_routes'), 'source_protocol'):
                    l_2_redistribute_route_cli = resolve('redistribute_route_cli')
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_2_redistribute_route, 'source_protocol')):
                        pass
                        l_2_redistribute_route_cli = str_join(('redistribute ', environment.getattr(l_2_redistribute_route, 'source_protocol'), ))
                        _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (environment.getattr(l_2_redistribute_route, 'source_protocol') in ['ospf', 'ospfv3']):
                            pass
                            if t_8(environment.getattr(l_2_redistribute_route, 'ospf_route_type')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' match ', environment.getattr(l_2_redistribute_route, 'ospf_route_type'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if (t_8(environment.getattr(l_2_redistribute_route, 'include_leaked')) and (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'isis')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' include leaked', ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        if t_8(environment.getattr(l_2_redistribute_route, 'route_map')):
                            pass
                            l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' route-map ', environment.getattr(l_2_redistribute_route, 'route_map'), ))
                            _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        elif (environment.getattr(l_2_redistribute_route, 'source_protocol') == 'isis'):
                            pass
                            if t_8(environment.getattr(l_2_redistribute_route, 'rcf')):
                                pass
                                l_2_redistribute_route_cli = str_join(((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli), ' rcf ', environment.getattr(l_2_redistribute_route, 'rcf'), ))
                                _loop_vars['redistribute_route_cli'] = l_2_redistribute_route_cli
                        yield '         '
                        yield str((undefined(name='redistribute_route_cli') if l_2_redistribute_route_cli is missing else l_2_redistribute_route_cli))
                        yield '\n'
                l_2_redistribute_route = l_2_redistribute_route_cli = missing
            for l_2_address_family in t_3(environment.getattr(l_1_vrf, 'address_families'), 'address_family'):
                _loop_vars = {}
                pass
                yield '      !\n      address-family '
                yield str(environment.getattr(l_2_address_family, 'address_family'))
                yield '\n'
                if t_8(environment.getattr(l_2_address_family, 'bgp')):
                    pass
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'missing_policy'), 'direction_in_action')):
                        pass
                        yield '         bgp missing-policy direction in action '
                        yield str(environment.getattr(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'missing_policy'), 'direction_in_action'))
                        yield '\n'
                    if t_8(environment.getattr(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'missing_policy'), 'direction_out_action')):
                        pass
                        yield '         bgp missing-policy direction out action '
                        yield str(environment.getattr(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'missing_policy'), 'direction_out_action'))
                        yield '\n'
                    for l_3_additional_path in t_3(environment.getattr(environment.getattr(l_2_address_family, 'bgp'), 'additional_paths')):
                        _loop_vars = {}
                        pass
                        yield '         bgp additional-paths '
                        yield str(l_3_additional_path)
                        yield '\n'
                    l_3_additional_path = missing
                for l_3_peer_group in t_3(environment.getattr(l_2_address_family, 'peer_groups'), 'name'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_3_peer_group, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_peer_group, 'name'))
                        yield ' activate\n'
                    elif t_8(environment.getattr(l_3_peer_group, 'activate'), False):
                        pass
                        yield '         no neighbor '
                        yield str(environment.getattr(l_3_peer_group, 'name'))
                        yield ' activate\n'
                    if t_8(environment.getattr(environment.getattr(l_3_peer_group, 'next_hop'), 'address_family_ipv6_originate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_peer_group, 'name'))
                        yield ' next-hop address-family ipv6 originate\n'
                l_3_peer_group = missing
                for l_3_neighbor in t_3(environment.getattr(l_2_address_family, 'neighbors'), 'ip_address'):
                    _loop_vars = {}
                    pass
                    if t_8(environment.getattr(l_3_neighbor, 'activate'), True):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_neighbor, 'ip_address'))
                        yield ' activate\n'
                    if t_8(environment.getattr(l_3_neighbor, 'route_map_in')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_3_neighbor, 'route_map_in'))
                        yield ' in\n'
                    if t_8(environment.getattr(l_3_neighbor, 'route_map_out')):
                        pass
                        yield '         neighbor '
                        yield str(environment.getattr(l_3_neighbor, 'ip_address'))
                        yield ' route-map '
                        yield str(environment.getattr(l_3_neighbor, 'route_map_out'))
                        yield ' out\n'
                l_3_neighbor = missing
                for l_3_network in t_3(environment.getattr(l_2_address_family, 'networks'), 'prefix'):
                    l_3_network_cli = missing
                    _loop_vars = {}
                    pass
                    l_3_network_cli = str_join(('network ', environment.getattr(l_3_network, 'prefix'), ))
                    _loop_vars['network_cli'] = l_3_network_cli
                    if t_8(environment.getattr(l_3_network, 'route_map')):
                        pass
                        l_3_network_cli = str_join(((undefined(name='network_cli') if l_3_network_cli is missing else l_3_network_cli), ' route-map ', environment.getattr(l_3_network, 'route_map'), ))
                        _loop_vars['network_cli'] = l_3_network_cli
                    yield '         '
                    yield str((undefined(name='network_cli') if l_3_network_cli is missing else l_3_network_cli))
                    yield '\n'
                l_3_network = l_3_network_cli = missing
            l_2_address_family = missing
            if t_8(environment.getattr(l_1_vrf, 'eos_cli')):
                pass
                yield '      !\n      '
                yield str(t_4(environment.getattr(l_1_vrf, 'eos_cli'), 6, False))
                yield '\n'
        l_1_vrf = l_1_tmp_vrf_neighbor_prefix_list_in = l_1_tmp_vrf_neighbor_prefix_list_out = missing
        for l_1_session_tracker in t_3(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'session_trackers'), 'name'):
            _loop_vars = {}
            pass
            yield '   session tracker '
            yield str(environment.getattr(l_1_session_tracker, 'name'))
            yield '\n'
            if t_8(environment.getattr(l_1_session_tracker, 'recovery_delay')):
                pass
                yield '      recovery delay '
                yield str(environment.getattr(l_1_session_tracker, 'recovery_delay'))
                yield ' seconds\n'
        l_1_session_tracker = missing
        if t_8(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'eos_cli')):
            pass
            yield '   !\n   '
            yield str(t_4(environment.getattr((undefined(name='router_bgp') if l_0_router_bgp is missing else l_0_router_bgp), 'eos_cli'), 3, False))
            yield '\n'

blocks = {}
debug_info = '7=82&9=85&10=87&11=90&13=92&14=95&16=97&17=99&18=102&19=104&21=108&23=110&24=112&25=115&27=117&28=120&32=123&34=126&35=128&36=131&37=133&41=136&42=138&43=141&44=143&46=147&48=149&49=151&50=154&51=156&53=160&55=162&58=165&61=168&63=171&66=174&68=177&71=180&72=183&74=185&75=189&77=192&80=195&82=197&81=201&83=205&84=207&85=209&87=211&88=213&89=215&90=217&91=219&93=222&96=225&97=228&98=231&101=238&102=249&103=252&105=255&106=257&107=260&109=264&110=267&112=271&113=274&115=276&116=279&118=281&119=284&121=286&122=289&124=291&125=293&126=295&127=297&128=299&129=301&132=304&133=306&134=309&136=311&137=313&138=315&139=317&141=320&142=322&143=325&145=327&146=330&148=334&149=337&151=341&152=344&154=346&155=349&156=351&159=354&162=362&163=364&164=366&165=368&167=371&169=373&170=375&171=377&172=379&174=382&175=384&176=386&177=389&179=391&180=394&182=398&183=401&185=405&186=408&188=412&189=414&190=416&191=418&193=420&194=422&196=425&198=427&199=430&201=432&202=435&204=439&205=442&207=448&208=451&209=453&210=456&212=460&213=462&214=464&215=466&217=468&218=470&220=473&222=475&223=477&224=482&225=484&226=486&227=488&228=490&229=492&230=494&231=496&233=498&234=500&236=502&237=504&240=506&241=509&245=512&246=514&247=516&248=518&250=521&252=523&253=526&255=530&256=533&258=537&259=540&261=544&262=547&265=552&266=555&267=558&268=564&269=567&272=574&273=585&274=588&276=592&277=595&279=599&280=602&282=604&283=607&285=609&286=611&287=613&288=615&289=617&290=619&293=622&294=624&295=627&297=629&298=631&299=633&300=635&302=638&303=640&304=643&306=645&307=648&309=650&310=653&312=655&313=658&315=662&316=665&318=669&319=672&320=674&321=677&323=679&324=682&326=686&327=689&329=693&330=696&332=700&333=703&334=705&337=708&339=716&340=719&342=721&343=723&344=725&345=727&347=730&349=732&350=734&351=736&352=738&354=741&355=743&356=745&357=748&359=750&360=753&362=757&363=760&365=762&366=765&368=769&369=772&371=776&372=779&374=783&375=786&377=790&378=793&380=797&381=800&383=806&384=808&385=810&386=812&388=814&389=816&391=819&393=821&394=824&395=826&396=829&398=833&399=835&400=837&401=839&403=841&404=843&406=846&408=848&409=850&410=855&411=857&412=859&413=861&414=863&415=865&416=867&417=869&419=871&420=873&422=875&423=877&426=879&427=882&431=885&432=887&433=889&434=891&436=894&439=897&441=900&444=903&445=907&446=909&447=911&449=913&450=915&452=917&453=919&455=921&456=923&458=925&459=927&461=930&463=933&464=937&465=939&466=941&467=943&468=945&471=947&472=949&473=951&474=953&476=955&477=957&478=959&479=961&480=963&483=966&487=969&489=971&490=974&491=977&493=979&495=983&496=985&497=988&499=990&500=993&502=997&503=1001&505=1004&506=1008&508=1011&509=1015&511=1018&512=1022&514=1027&515=1031&517=1036&518=1040&520=1045&521=1049&523=1052&524=1056&526=1059&528=1062&533=1065&535=1069&536=1071&537=1074&539=1076&540=1079&542=1083&543=1087&545=1090&546=1094&548=1097&549=1101&551=1104&552=1108&554=1113&555=1117&557=1122&558=1126&560=1131&561=1135&563=1138&564=1142&566=1146&567=1148&569=1151&573=1154&574=1156&576=1160&577=1163&578=1165&579=1168&581=1170&582=1173&584=1175&587=1178&590=1181&591=1184&593=1186&594=1189&596=1192&597=1194&605=1200&608=1203&611=1206&613=1209&615=1212&617=1215&618=1218&619=1220&620=1223&622=1225&625=1228&627=1231&628=1233&629=1236&630=1238&632=1241&633=1243&635=1246&636=1248&638=1251&639=1254&642=1256&643=1259&645=1261&646=1263&647=1266&648=1268&650=1272&652=1274&653=1276&654=1279&655=1282&656=1284&657=1285&658=1287&659=1288&660=1290&663=1292&664=1295&667=1297&668=1301&669=1304&671=1308&672=1311&674=1315&675=1318&677=1322&678=1325&680=1329&681=1331&682=1333&683=1335&684=1337&685=1339&687=1342&689=1344&690=1347&691=1349&692=1352&694=1354&695=1357&697=1359&698=1362&699=1364&700=1367&701=1369&702=1372&703=1374&704=1377&705=1379&706=1382&707=1386&708=1389&710=1393&711=1396&713=1398&714=1401&717=1406&718=1410&719=1413&720=1415&721=1418&723=1420&724=1423&726=1427&727=1430&729=1434&730=1436&731=1438&732=1440&733=1442&734=1444&736=1447&739=1450&742=1453&743=1455&744=1458&745=1460&747=1464&749=1466&752=1469&755=1472&758=1475&759=1477&760=1480&761=1482&763=1486&765=1488&770=1491&773=1494&774=1497&776=1499&777=1502&779=1504&780=1507&781=1510&782=1512&783=1515&786=1518&787=1521&788=1524&793=1527&796=1530&797=1533&799=1535&800=1538&802=1540&803=1543&804=1546&805=1548&806=1551&809=1554&810=1557&811=1560&816=1563&819=1566&820=1569&821=1572&822=1574&823=1577&825=1579&826=1581&827=1584&829=1589&832=1591&833=1594&838=1597&841=1600&842=1605&843=1608&845=1612&846=1615&848=1619&849=1622&851=1626&852=1629&854=1633&855=1636&857=1640&858=1643&860=1647&861=1649&862=1651&863=1653&865=1655&866=1657&868=1660&870=1662&871=1664&872=1666&873=1668&875=1671&876=1673&877=1676&879=1678&880=1681&881=1683&882=1686&885=1689&886=1693&887=1696&889=1700&890=1703&892=1707&893=1710&895=1714&896=1717&898=1721&899=1724&901=1728&902=1731&904=1735&905=1737&906=1739&907=1741&909=1743&910=1745&912=1748&914=1750&915=1753&916=1755&917=1758&920=1761&921=1764&922=1767&924=1774&927=1777&929=1780&932=1783&933=1787&934=1789&935=1791&936=1793&937=1795&940=1797&941=1799&942=1801&943=1803&945=1805&946=1807&947=1809&948=1811&949=1813&952=1816&957=1819&960=1822&961=1825&962=1828&964=1832&965=1835&967=1839&968=1842&969=1844&970=1847&973=1850&974=1853&975=1856&977=1860&978=1863&980=1867&981=1870&982=1872&983=1875&986=1878&987=1882&988=1884&989=1886&990=1888&991=1890&994=1892&995=1894&997=1896&998=1898&999=1900&1000=1902&1002=1905&1007=1908&1010=1911&1011=1914&1012=1917&1013=1919&1014=1922&1016=1924&1017=1927&1019=1931&1020=1934&1023=1939&1024=1942&1025=1945&1026=1947&1027=1950&1029=1952&1030=1955&1032=1959&1033=1962&1038=1967&1041=1970&1042=1973&1043=1976&1045=1980&1046=1983&1048=1987&1049=1990&1051=1994&1052=1997&1054=2001&1055=2004&1057=2008&1058=2011&1060=2015&1061=2018&1062=2020&1063=2023&1066=2026&1067=2029&1068=2032&1070=2036&1071=2039&1073=2043&1074=2046&1076=2050&1077=2053&1079=2057&1080=2060&1082=2064&1083=2067&1085=2071&1086=2074&1087=2076&1088=2079&1091=2082&1092=2085&1093=2088&1095=2095&1098=2098&1100=2101&1103=2104&1104=2108&1105=2110&1106=2112&1107=2114&1108=2116&1111=2118&1112=2120&1113=2122&1114=2124&1116=2126&1117=2128&1118=2130&1119=2132&1120=2134&1123=2137&1128=2140&1131=2143&1132=2146&1134=2148&1135=2151&1137=2153&1140=2156&1141=2159&1142=2162&1143=2164&1144=2167&1147=2170&1148=2173&1149=2176&1151=2178&1152=2181&1154=2185&1155=2188&1158=2193&1159=2197&1160=2199&1161=2201&1163=2204&1165=2207&1166=2211&1167=2213&1168=2215&1169=2217&1170=2219&1173=2221&1174=2223&1176=2225&1177=2227&1178=2229&1179=2231&1181=2234&1186=2237&1189=2240&1190=2243&1191=2246&1192=2248&1193=2251&1195=2253&1196=2256&1198=2260&1199=2263&1202=2268&1203=2271&1204=2274&1205=2276&1206=2279&1208=2281&1209=2284&1211=2288&1212=2291&1217=2296&1220=2299&1221=2302&1223=2304&1224=2307&1226=2309&1227=2312&1228=2315&1229=2317&1230=2320&1232=2322&1233=2325&1235=2329&1236=2332&1239=2337&1240=2340&1241=2343&1243=2345&1244=2348&1246=2352&1247=2355&1250=2360&1251=2362&1254=2365&1255=2367&1256=2370&1257=2372&1259=2375&1260=2377&1262=2381&1267=2383&1270=2386&1273=2389&1275=2392&1277=2395&1279=2398&1280=2401&1281=2403&1282=2406&1284=2408&1285=2411&1286=2414&1287=2416&1288=2419&1290=2421&1291=2424&1293=2426&1294=2429&1295=2431&1296=2434&1297=2436&1298=2439&1299=2441&1300=2444&1301=2448&1302=2451&1305=2456&1306=2459&1307=2462&1308=2464&1309=2467&1311=2469&1312=2472&1314=2474&1315=2477&1316=2479&1317=2482&1318=2484&1319=2487&1320=2489&1321=2492&1322=2496&1323=2499&1328=2504&1331=2507&1332=2510&1334=2512&1335=2516&1336=2519&1337=2521&1338=2524&1340=2526&1341=2529&1343=2533&1344=2536&1346=2540&1347=2543&1349=2547&1350=2550&1352=2554&1353=2556&1354=2558&1355=2560&1356=2562&1357=2564&1359=2567&1362=2570&1363=2574&1364=2577&1365=2579&1366=2582&1368=2584&1369=2587&1371=2591&1372=2594&1374=2598&1375=2601&1377=2605&1378=2608&1380=2612&1381=2614&1382=2616&1383=2618&1384=2620&1385=2622&1387=2625&1390=2628&1391=2631&1393=2633&1398=2636&1401=2639&1402=2642&1404=2644&1405=2648&1406=2651&1407=2653&1408=2656&1410=2658&1411=2661&1413=2665&1414=2668&1416=2672&1417=2675&1419=2679&1420=2682&1422=2686&1423=2688&1424=2690&1425=2692&1426=2694&1427=2696&1429=2699&1432=2702&1433=2706&1434=2709&1435=2711&1436=2714&1438=2716&1439=2719&1441=2723&1442=2726&1444=2730&1445=2733&1447=2737&1448=2740&1450=2744&1451=2746&1452=2748&1453=2750&1454=2752&1455=2754&1457=2757&1460=2760&1461=2763&1463=2765&1468=2768&1470=2773&1471=2775&1472=2778&1474=2780&1476=2783&1477=2785&1478=2787&1479=2790&1482=2795&1485=2797&1488=2800&1493=2803&1494=2805&1495=2809&1496=2811&1497=2813&1499=2815&1500=2817&1501=2819&1502=2821&1504=2824&1507=2827&1508=2829&1509=2832&1510=2836&1512=2841&1513=2843&1514=2845&1515=2848&1517=2857&1520=2861&1521=2864&1526=2869&1527=2871&1528=2874&1529=2878&1531=2883&1532=2885&1533=2887&1534=2890&1536=2899&1539=2903&1540=2906&1545=2911&1546=2914&1548=2916&1551=2919&1554=2922&1555=2925&1557=2927&1559=2929&1558=2933&1560=2937&1561=2939&1562=2941&1564=2943&1565=2945&1566=2947&1567=2949&1568=2951&1570=2954&1573=2957&1574=2960&1575=2963&1576=2969&1577=2972&1584=2979&1585=2981&1586=2983&1587=2994&1588=2997&1590=3001&1591=3004&1593=3008&1594=3010&1595=3012&1596=3014&1597=3016&1598=3018&1601=3021&1602=3023&1603=3026&1605=3028&1606=3030&1607=3032&1608=3034&1610=3037&1611=3039&1612=3042&1614=3044&1615=3047&1617=3051&1618=3054&1620=3056&1621=3059&1623=3063&1624=3066&1626=3068&1627=3071&1629=3073&1630=3076&1632=3080&1633=3083&1635=3087&1636=3089&1637=3091&1638=3093&1640=3096&1642=3098&1643=3101&1645=3103&1646=3106&1647=3108&1650=3111&1652=3119&1653=3122&1655=3124&1656=3126&1657=3128&1658=3130&1660=3133&1662=3135&1663=3137&1664=3139&1665=3141&1667=3144&1668=3146&1669=3148&1670=3151&1672=3153&1673=3156&1675=3160&1676=3163&1678=3165&1679=3168&1680=3170&1681=3173&1683=3177&1684=3180&1685=3182&1686=3185&1688=3187&1689=3189&1690=3191&1691=3193&1693=3195&1694=3197&1696=3200&1698=3202&1699=3204&1700=3206&1701=3208&1703=3210&1704=3212&1706=3215&1708=3217&1709=3220&1711=3224&1712=3227&1714=3231&1715=3234&1721=3238&1722=3240&1724=3241&1725=3243&1728=3245&1729=3248&1730=3251&1732=3258&1735=3261&1737=3264&1740=3267&1741=3271&1742=3273&1743=3275&1745=3277&1746=3279&1748=3281&1749=3283&1751=3285&1752=3287&1754=3289&1755=3291&1757=3294&1759=3297&1760=3301&1761=3303&1762=3305&1763=3307&1764=3309&1767=3311&1768=3313&1769=3315&1770=3317&1772=3319&1773=3321&1774=3323&1775=3325&1776=3327&1779=3330&1782=3333&1785=3336&1786=3339&1788=3341&1789=3344&1791=3346&1792=3349&1793=3352&1797=3355&1800=3358&1801=3361&1803=3363&1804=3366&1806=3368&1807=3371&1808=3374&1813=3377&1816=3380&1817=3383&1819=3385&1820=3388&1822=3390&1824=3393&1827=3396&1830=3399&1832=3402&1834=3405&1836=3408&1837=3411&1838=3413&1839=3416&1841=3418&1842=3422&1843=3425&1845=3427&1846=3430&1848=3434&1849=3437&1851=3441&1852=3444&1854=3448&1855=3451&1858=3455&1859=3458&1860=3462&1861=3464&1863=3465&1864=3468&1866=3472&1867=3475&1868=3479&1869=3481&1871=3482&1872=3485&1874=3489&1875=3491&1876=3493&1877=3495&1878=3497&1880=3499&1881=3501&1883=3504&1887=3507&1888=3511&1890=3516&1891=3520&1893=3525&1894=3529&1895=3531&1896=3533&1898=3536&1900=3539&1902=3542&1905=3545&1906=3549&1907=3551&1908=3553&1909=3555&1910=3557&1913=3559&1914=3561&1915=3563&1916=3565&1918=3567&1919=3569&1920=3571&1921=3573&1922=3575&1925=3578&1929=3581&1932=3584&1933=3587&1935=3589&1936=3592&1938=3594&1941=3597&1942=3600&1943=3603&1945=3605&1946=3608&1948=3612&1949=3615&1952=3620&1953=3624&1954=3626&1955=3628&1957=3631&1959=3634&1960=3638&1961=3640&1962=3642&1963=3644&1964=3646&1967=3648&1968=3650&1970=3652&1971=3654&1972=3656&1973=3658&1974=3660&1977=3663&1981=3666&1984=3669&1985=3672&1987=3674&1988=3677&1990=3679&1992=3682&1995=3685&1998=3688&2000=3691&2002=3694&2004=3697&2005=3700&2006=3702&2007=3705&2009=3707&2010=3710&2011=3713&2013=3715&2014=3718&2016=3722&2017=3725&2019=3729&2020=3732&2022=3736&2023=3739&2025=3743&2026=3746&2028=3750&2029=3753&2032=3758&2033=3762&2034=3764&2035=3766&2037=3769&2039=3772&2041=3775&2044=3778&2045=3782&2046=3784&2047=3786&2048=3788&2049=3790&2052=3792&2053=3794&2054=3796&2055=3798&2057=3800&2058=3802&2059=3804&2060=3806&2061=3808&2064=3811&2068=3814&2071=3817&2072=3820&2074=3822&2075=3825&2077=3827&2080=3830&2081=3833&2082=3836&2084=3838&2085=3841&2087=3845&2088=3848&2091=3853&2092=3857&2093=3859&2094=3861&2096=3864&2098=3867&2099=3871&2100=3873&2101=3875&2102=3877&2103=3879&2106=3881&2107=3883&2109=3885&2110=3887&2111=3889&2112=3891&2113=3893&2116=3896&2120=3899&2122=3903&2123=3905&2124=3907&2125=3910&2127=3912&2128=3915&2130=3917&2131=3921&2134=3924&2135=3927&2136=3930&2137=3932&2138=3935&2140=3937&2141=3940&2144=3943&2145=3946&2146=3949&2148=3951&2149=3954&2151=3958&2152=3961&2155=3966&2156=3970&2157=3972&2158=3974&2160=3977&2163=3981&2165=3984&2169=3987&2170=3991&2171=3993&2172=3996&2175=3999&2177=4002'