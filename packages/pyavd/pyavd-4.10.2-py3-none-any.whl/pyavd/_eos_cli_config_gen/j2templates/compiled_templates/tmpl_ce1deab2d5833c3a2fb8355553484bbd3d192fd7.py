from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/vlan-interfaces.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_vlan_interfaces = resolve('vlan_interfaces')
    try:
        t_1 = environment.filters['arista.avd.hide_passwords']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.hide_passwords' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_4 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    for l_1_vlan_interface in t_2((undefined(name='vlan_interfaces') if l_0_vlan_interfaces is missing else l_0_vlan_interfaces), 'name'):
        l_1_ipv6_attached_host_route_export_cli = resolve('ipv6_attached_host_route_export_cli')
        l_1_host_proxy_cli = resolve('host_proxy_cli')
        l_1_interface_ip_nat = resolve('interface_ip_nat')
        l_1_hide_passwords = resolve('hide_passwords')
        l_1_ip_attached_host_route_export_cli = resolve('ip_attached_host_route_export_cli')
        _loop_vars = {}
        pass
        yield '!\ninterface '
        yield str(environment.getattr(l_1_vlan_interface, 'name'))
        yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'description')):
            pass
            yield '   description '
            yield str(environment.getattr(l_1_vlan_interface, 'description'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'shutdown'), True):
            pass
            yield '   shutdown\n'
        elif t_4(environment.getattr(l_1_vlan_interface, 'shutdown'), False):
            pass
            yield '   no shutdown\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'mtu')):
            pass
            yield '   mtu '
            yield str(environment.getattr(l_1_vlan_interface, 'mtu'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'no_autostate'), True):
            pass
            yield '   no autostate\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'vrf')):
            pass
            yield '   vrf '
            yield str(environment.getattr(l_1_vlan_interface, 'vrf'))
            yield '\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'logging'), 'event'), 'link_status'), True):
            pass
            yield '   logging event link-status\n'
        elif t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'logging'), 'event'), 'link_status'), False):
            pass
            yield '   no logging event link-status\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'arp_aging_timeout')):
            pass
            yield '   arp aging timeout '
            yield str(environment.getattr(l_1_vlan_interface, 'arp_aging_timeout'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'arp_gratuitous_accept'), True):
            pass
            yield '   arp gratuitous accept\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'arp_monitor_mac_address'), True):
            pass
            yield '   arp monitor mac-address\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'arp_cache_dynamic_capacity')):
            pass
            yield '   arp cache dynamic capacity '
            yield str(environment.getattr(l_1_vlan_interface, 'arp_cache_dynamic_capacity'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_nd_cache')):
            pass
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_nd_cache'), 'expire')):
                pass
                yield '   ipv6 nd cache expire '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_nd_cache'), 'expire'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_nd_cache'), 'dynamic_capacity')):
                pass
                yield '   ipv6 nd cache dynamic capacity '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_nd_cache'), 'dynamic_capacity'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_nd_cache'), 'refresh_always'), True):
                pass
                yield '   ipv6 nd cache refresh always\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_proxy_arp'), True):
            pass
            yield '   ip proxy-arp\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_directed_broadcast'), True):
            pass
            yield '   ip directed-broadcast\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_address')):
            pass
            yield '   ip address '
            yield str(environment.getattr(l_1_vlan_interface, 'ip_address'))
            yield '\n'
            if t_4(environment.getattr(l_1_vlan_interface, 'ip_address_secondaries')):
                pass
                for l_2_ip_address_secondary in environment.getattr(l_1_vlan_interface, 'ip_address_secondaries'):
                    _loop_vars = {}
                    pass
                    yield '   ip address '
                    yield str(l_2_ip_address_secondary)
                    yield ' secondary\n'
                l_2_ip_address_secondary = missing
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_verify_unicast_source_reachable_via')):
            pass
            yield '   ip verify unicast source reachable-via '
            yield str(environment.getattr(l_1_vlan_interface, 'ip_verify_unicast_source_reachable_via'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_dhcp_relay_all_subnets'), True):
            pass
            yield '   ip dhcp relay all-subnets\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_dhcp_relay_all_subnets'), True):
            pass
            yield '   ipv6 dhcp relay all-subnets\n'
        for l_2_ip_helper in t_2(environment.getattr(l_1_vlan_interface, 'ip_helpers'), 'ip_helper'):
            l_2_ip_helper_cli = missing
            _loop_vars = {}
            pass
            l_2_ip_helper_cli = str_join(('ip helper-address ', environment.getattr(l_2_ip_helper, 'ip_helper'), ))
            _loop_vars['ip_helper_cli'] = l_2_ip_helper_cli
            if t_4(environment.getattr(l_2_ip_helper, 'vrf')):
                pass
                l_2_ip_helper_cli = str_join(((undefined(name='ip_helper_cli') if l_2_ip_helper_cli is missing else l_2_ip_helper_cli), ' vrf ', environment.getattr(l_2_ip_helper, 'vrf'), ))
                _loop_vars['ip_helper_cli'] = l_2_ip_helper_cli
            if t_4(environment.getattr(l_2_ip_helper, 'source_interface')):
                pass
                l_2_ip_helper_cli = str_join(((undefined(name='ip_helper_cli') if l_2_ip_helper_cli is missing else l_2_ip_helper_cli), ' source-interface ', environment.getattr(l_2_ip_helper, 'source_interface'), ))
                _loop_vars['ip_helper_cli'] = l_2_ip_helper_cli
            yield '   '
            yield str((undefined(name='ip_helper_cli') if l_2_ip_helper_cli is missing else l_2_ip_helper_cli))
            yield '\n'
        l_2_ip_helper = l_2_ip_helper_cli = missing
        for l_2_destination in t_2(environment.getattr(l_1_vlan_interface, 'ipv6_dhcp_relay_destinations'), 'address'):
            l_2_destination_cli = missing
            _loop_vars = {}
            pass
            l_2_destination_cli = str_join(('ipv6 dhcp relay destination ', environment.getattr(l_2_destination, 'address'), ))
            _loop_vars['destination_cli'] = l_2_destination_cli
            if t_4(environment.getattr(l_2_destination, 'vrf')):
                pass
                l_2_destination_cli = str_join(((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli), ' vrf ', environment.getattr(l_2_destination, 'vrf'), ))
                _loop_vars['destination_cli'] = l_2_destination_cli
            if t_4(environment.getattr(l_2_destination, 'local_interface')):
                pass
                l_2_destination_cli = str_join(((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli), ' local-interface ', environment.getattr(l_2_destination, 'local_interface'), ))
                _loop_vars['destination_cli'] = l_2_destination_cli
            elif t_4(environment.getattr(l_2_destination, 'source_address')):
                pass
                l_2_destination_cli = str_join(((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli), ' source-address ', environment.getattr(l_2_destination, 'source_address'), ))
                _loop_vars['destination_cli'] = l_2_destination_cli
            if t_4(environment.getattr(l_2_destination, 'link_address')):
                pass
                l_2_destination_cli = str_join(((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli), ' link-address ', environment.getattr(l_2_destination, 'link_address'), ))
                _loop_vars['destination_cli'] = l_2_destination_cli
            yield '   '
            yield str((undefined(name='destination_cli') if l_2_destination_cli is missing else l_2_destination_cli))
            yield '\n'
        l_2_destination = l_2_destination_cli = missing
        if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_attached_host_route_export'), 'enabled'), True):
            pass
            l_1_ipv6_attached_host_route_export_cli = 'ipv6 attached-host route export'
            _loop_vars['ipv6_attached_host_route_export_cli'] = l_1_ipv6_attached_host_route_export_cli
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_attached_host_route_export'), 'distance')):
                pass
                l_1_ipv6_attached_host_route_export_cli = str_join(((undefined(name='ipv6_attached_host_route_export_cli') if l_1_ipv6_attached_host_route_export_cli is missing else l_1_ipv6_attached_host_route_export_cli), ' ', environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_attached_host_route_export'), 'distance'), ))
                _loop_vars['ipv6_attached_host_route_export_cli'] = l_1_ipv6_attached_host_route_export_cli
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_attached_host_route_export'), 'prefix_length')):
                pass
                l_1_ipv6_attached_host_route_export_cli = str_join(((undefined(name='ipv6_attached_host_route_export_cli') if l_1_ipv6_attached_host_route_export_cli is missing else l_1_ipv6_attached_host_route_export_cli), ' prefix-length ', environment.getattr(environment.getattr(l_1_vlan_interface, 'ipv6_attached_host_route_export'), 'prefix_length'), ))
                _loop_vars['ipv6_attached_host_route_export_cli'] = l_1_ipv6_attached_host_route_export_cli
            yield '   '
            yield str((undefined(name='ipv6_attached_host_route_export_cli') if l_1_ipv6_attached_host_route_export_cli is missing else l_1_ipv6_attached_host_route_export_cli))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_igmp'), True):
            pass
            yield '   ip igmp\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_igmp_version')):
            pass
            yield '   ip igmp version '
            yield str(environment.getattr(l_1_vlan_interface, 'ip_igmp_version'))
            yield '\n'
        if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'enabled'), True):
            pass
            l_1_host_proxy_cli = 'ip igmp host-proxy'
            _loop_vars['host_proxy_cli'] = l_1_host_proxy_cli
            yield '   '
            yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
            yield '\n'
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'groups')):
                pass
                for l_2_proxy_group in environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'groups'):
                    _loop_vars = {}
                    pass
                    if (t_4(environment.getattr(l_2_proxy_group, 'exclude')) or t_4(environment.getattr(l_2_proxy_group, 'include'))):
                        pass
                        if t_4(environment.getattr(l_2_proxy_group, 'include')):
                            pass
                            for l_3_include_source in environment.getattr(l_2_proxy_group, 'include'):
                                _loop_vars = {}
                                pass
                                yield '   '
                                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                                yield ' '
                                yield str(environment.getattr(l_2_proxy_group, 'group'))
                                yield ' include '
                                yield str(environment.getattr(l_3_include_source, 'source'))
                                yield '\n'
                            l_3_include_source = missing
                        if t_4(environment.getattr(l_2_proxy_group, 'exclude')):
                            pass
                            for l_3_exclude_source in environment.getattr(l_2_proxy_group, 'exclude'):
                                _loop_vars = {}
                                pass
                                yield '   '
                                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                                yield ' '
                                yield str(environment.getattr(l_2_proxy_group, 'group'))
                                yield ' exclude '
                                yield str(environment.getattr(l_3_exclude_source, 'source'))
                                yield '\n'
                            l_3_exclude_source = missing
                    elif t_4(environment.getattr(l_2_proxy_group, 'group')):
                        pass
                        yield '   '
                        yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                        yield ' '
                        yield str(environment.getattr(l_2_proxy_group, 'group'))
                        yield '\n'
                l_2_proxy_group = missing
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'access_lists')):
                pass
                for l_2_access_list in environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'access_lists'):
                    _loop_vars = {}
                    pass
                    yield '   '
                    yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                    yield ' access-list '
                    yield str(environment.getattr(l_2_access_list, 'name'))
                    yield '\n'
                l_2_access_list = missing
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'report_interval')):
                pass
                yield '   '
                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                yield ' report-interval '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'report_interval'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'version')):
                pass
                yield '   '
                yield str((undefined(name='host_proxy_cli') if l_1_host_proxy_cli is missing else l_1_host_proxy_cli))
                yield ' version '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_igmp_host_proxy'), 'version'))
                yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_enable'), True):
            pass
            yield '   ipv6 enable\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_address')):
            pass
            yield '   ipv6 address '
            yield str(environment.getattr(l_1_vlan_interface, 'ipv6_address'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_address_link_local')):
            pass
            yield '   ipv6 address '
            yield str(environment.getattr(l_1_vlan_interface, 'ipv6_address_link_local'))
            yield ' link-local\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_address_virtual')):
            pass
            yield '   ipv6 address virtual '
            yield str(environment.getattr(l_1_vlan_interface, 'ipv6_address_virtual'))
            yield '\n'
        for l_2_ipv6_address_virtual in t_2(environment.getattr(l_1_vlan_interface, 'ipv6_address_virtuals')):
            _loop_vars = {}
            pass
            yield '   ipv6 address virtual '
            yield str(l_2_ipv6_address_virtual)
            yield '\n'
        l_2_ipv6_address_virtual = missing
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_nd_ra_disabled'), True):
            pass
            yield '   ipv6 nd ra disabled\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_nd_managed_config_flag'), True):
            pass
            yield '   ipv6 nd managed-config-flag\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_nd_other_config_flag'), True):
            pass
            yield '   ipv6 nd other-config-flag\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_nd_prefixes')):
            pass
            for l_2_prefix in environment.getattr(l_1_vlan_interface, 'ipv6_nd_prefixes'):
                l_2_ipv6_nd_prefix_cli = missing
                _loop_vars = {}
                pass
                l_2_ipv6_nd_prefix_cli = str_join(('ipv6 nd prefix ', environment.getattr(l_2_prefix, 'ipv6_prefix'), ))
                _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
                if t_4(environment.getattr(l_2_prefix, 'valid_lifetime')):
                    pass
                    l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' ', environment.getattr(l_2_prefix, 'valid_lifetime'), ))
                    _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
                    if t_4(environment.getattr(l_2_prefix, 'preferred_lifetime')):
                        pass
                        l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' ', environment.getattr(l_2_prefix, 'preferred_lifetime'), ))
                        _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
                if t_4(environment.getattr(l_2_prefix, 'no_autoconfig_flag'), True):
                    pass
                    l_2_ipv6_nd_prefix_cli = str_join(((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli), ' no-autoconfig', ))
                    _loop_vars['ipv6_nd_prefix_cli'] = l_2_ipv6_nd_prefix_cli
                yield '   '
                yield str((undefined(name='ipv6_nd_prefix_cli') if l_2_ipv6_nd_prefix_cli is missing else l_2_ipv6_nd_prefix_cli))
                yield '\n'
            l_2_prefix = l_2_ipv6_nd_prefix_cli = missing
        if t_4(environment.getattr(l_1_vlan_interface, 'multicast')):
            pass
            if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv4'), 'boundaries')):
                pass
                for l_2_boundary in environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv4'), 'boundaries'):
                    l_2_boundary_cli = missing
                    _loop_vars = {}
                    pass
                    l_2_boundary_cli = str_join(('multicast ipv4 boundary ', environment.getattr(l_2_boundary, 'boundary'), ))
                    _loop_vars['boundary_cli'] = l_2_boundary_cli
                    if t_4(environment.getattr(l_2_boundary, 'out'), True):
                        pass
                        l_2_boundary_cli = str_join(((undefined(name='boundary_cli') if l_2_boundary_cli is missing else l_2_boundary_cli), ' out', ))
                        _loop_vars['boundary_cli'] = l_2_boundary_cli
                    yield '   '
                    yield str((undefined(name='boundary_cli') if l_2_boundary_cli is missing else l_2_boundary_cli))
                    yield '\n'
                l_2_boundary = l_2_boundary_cli = missing
            if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv6'), 'boundaries')):
                pass
                for l_2_boundary in environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv6'), 'boundaries'):
                    _loop_vars = {}
                    pass
                    yield '   multicast ipv6 boundary '
                    yield str(environment.getattr(l_2_boundary, 'boundary'))
                    yield ' out\n'
                l_2_boundary = missing
            if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv4'), 'source_route_export'), 'enabled'), True):
                pass
                if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv4'), 'source_route_export'), 'administrative_distance')):
                    pass
                    yield '   multicast ipv4 source route export '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv4'), 'source_route_export'), 'administrative_distance'))
                    yield '\n'
                else:
                    pass
                    yield '   multicast ipv4 source route export\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv6'), 'source_route_export'), 'enabled'), True):
                pass
                if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv6'), 'source_route_export'), 'administrative_distance')):
                    pass
                    yield '   multicast ipv6 source route export '
                    yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv6'), 'source_route_export'), 'administrative_distance'))
                    yield '\n'
                else:
                    pass
                    yield '   multicast ipv6 source route export\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv4'), 'static'), True):
                pass
                yield '   multicast ipv4 static\n'
            if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'multicast'), 'ipv6'), 'static'), True):
                pass
                yield '   multicast ipv6 static\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_nat')):
            pass
            l_1_interface_ip_nat = environment.getattr(l_1_vlan_interface, 'ip_nat')
            _loop_vars['interface_ip_nat'] = l_1_interface_ip_nat
            template = environment.get_template('eos/interface-ip-nat.j2', 'eos/vlan-interfaces.j2')
            for event in template.root_render_func(template.new_context(context.get_all(), True, {'host_proxy_cli': l_1_host_proxy_cli, 'interface_ip_nat': l_1_interface_ip_nat, 'ip_attached_host_route_export_cli': l_1_ip_attached_host_route_export_cli, 'ipv6_attached_host_route_export_cli': l_1_ipv6_attached_host_route_export_cli, 'vlan_interface': l_1_vlan_interface})):
                yield event
        if t_4(environment.getattr(l_1_vlan_interface, 'access_group_in')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr(l_1_vlan_interface, 'access_group_in'))
            yield ' in\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'access_group_out')):
            pass
            yield '   ip access-group '
            yield str(environment.getattr(l_1_vlan_interface, 'access_group_out'))
            yield ' out\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_access_group_in')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr(l_1_vlan_interface, 'ipv6_access_group_in'))
            yield ' in\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_access_group_out')):
            pass
            yield '   ipv6 access-group '
            yield str(environment.getattr(l_1_vlan_interface, 'ipv6_access_group_out'))
            yield ' out\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ospf_network_point_to_point'), True):
            pass
            yield '   ip ospf network point-to-point\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ospf_area')):
            pass
            yield '   ip ospf area '
            yield str(environment.getattr(l_1_vlan_interface, 'ospf_area'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ospf_cost')):
            pass
            yield '   ip ospf cost '
            yield str(environment.getattr(l_1_vlan_interface, 'ospf_cost'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ospf_authentication')):
            pass
            if (environment.getattr(l_1_vlan_interface, 'ospf_authentication') == 'simple'):
                pass
                yield '   ip ospf authentication\n'
            elif (environment.getattr(l_1_vlan_interface, 'ospf_authentication') == 'message-digest'):
                pass
                yield '   ip ospf authentication message-digest\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ospf_authentication_key')):
            pass
            yield '   ip ospf authentication-key 7 '
            yield str(t_1(environment.getattr(l_1_vlan_interface, 'ospf_authentication_key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
            yield '\n'
        for l_2_ospf_message_digest_key in t_2(environment.getattr(l_1_vlan_interface, 'ospf_message_digest_keys'), 'id'):
            _loop_vars = {}
            pass
            if (t_4(environment.getattr(l_2_ospf_message_digest_key, 'hash_algorithm')) and t_4(environment.getattr(l_2_ospf_message_digest_key, 'key'))):
                pass
                yield '   ip ospf message-digest-key '
                yield str(environment.getattr(l_2_ospf_message_digest_key, 'id'))
                yield ' '
                yield str(environment.getattr(l_2_ospf_message_digest_key, 'hash_algorithm'))
                yield ' 7 '
                yield str(t_1(environment.getattr(l_2_ospf_message_digest_key, 'key'), (undefined(name='hide_passwords') if l_1_hide_passwords is missing else l_1_hide_passwords)))
                yield '\n'
        l_2_ospf_message_digest_key = missing
        if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'sparse_mode'), True):
            pass
            yield '   pim ipv4 sparse-mode\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'bidirectional'), True):
            pass
            yield '   pim ipv4 bidirectional\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'border_router'), True):
            pass
            yield '   pim ipv4 border-router\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'hello'), 'interval')):
            pass
            yield '   pim ipv4 hello interval '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'hello'), 'interval'))
            yield '\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'hello'), 'count')):
            pass
            yield '   pim ipv4 hello count '
            yield str(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'hello'), 'count'))
            yield '\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'dr_priority')):
            pass
            yield '   pim ipv4 dr-priority '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'dr_priority'))
            yield '\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'bfd'), True):
            pass
            yield '   pim ipv4 bfd\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'local_interface')):
            pass
            yield '   pim ipv4 local-interface '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'pim'), 'ipv4'), 'local_interface'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_virtual_router_address')):
            pass
            yield '   ipv6 virtual-router address '
            yield str(environment.getattr(l_1_vlan_interface, 'ipv6_virtual_router_address'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ipv6_virtual_router_addresses')):
            pass
            for l_2_ipv6_virtual_router_address in environment.getattr(l_1_vlan_interface, 'ipv6_virtual_router_addresses'):
                _loop_vars = {}
                pass
                yield '   ipv6 virtual-router address '
                yield str(l_2_ipv6_virtual_router_address)
                yield '\n'
            l_2_ipv6_virtual_router_address = missing
        if t_4(environment.getattr(l_1_vlan_interface, 'isis_enable')):
            pass
            yield '   isis enable '
            yield str(environment.getattr(l_1_vlan_interface, 'isis_enable'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'isis_bfd'), True):
            pass
            yield '   isis bfd\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'isis_passive'), True):
            pass
            yield '   isis passive\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'isis_metric')):
            pass
            yield '   isis metric '
            yield str(environment.getattr(l_1_vlan_interface, 'isis_metric'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'isis_network_point_to_point'), True):
            pass
            yield '   isis network point-to-point\n'
        if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'virtual_router')):
            pass
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'priority')):
                pass
                yield '   vrrp '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'virtual_router'))
                yield ' priority-level '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'priority'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'advertisement_interval')):
                pass
                yield '   vrrp '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'virtual_router'))
                yield ' advertisement interval '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'advertisement_interval'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'preempt_delay_minimum')):
                pass
                yield '   vrrp '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'virtual_router'))
                yield ' preempt delay minimum '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'preempt_delay_minimum'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'ipv4')):
                pass
                yield '   vrrp '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'virtual_router'))
                yield ' ipv4 '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'ipv4'))
                yield '\n'
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'ipv6')):
                pass
                yield '   vrrp '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'virtual_router'))
                yield ' ipv6 '
                yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'vrrp'), 'ipv6'))
                yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'vrrp_ids')):
            pass
            def t_5(fiter):
                for l_2_vrid in fiter:
                    if t_4(environment.getattr(l_2_vrid, 'id')):
                        yield l_2_vrid
            for l_2_vrid in t_5(t_2(environment.getattr(l_1_vlan_interface, 'vrrp_ids'), 'id')):
                l_2_delay_cli = resolve('delay_cli')
                _loop_vars = {}
                pass
                if t_4(environment.getattr(l_2_vrid, 'priority_level')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' priority-level '
                    yield str(environment.getattr(l_2_vrid, 'priority_level'))
                    yield '\n'
                if t_4(environment.getattr(environment.getattr(l_2_vrid, 'advertisement'), 'interval')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' advertisement interval '
                    yield str(environment.getattr(environment.getattr(l_2_vrid, 'advertisement'), 'interval'))
                    yield '\n'
                if (t_4(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'enabled'), True) and (t_4(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'minimum')) or t_4(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'reload')))):
                    pass
                    l_2_delay_cli = str_join(('vrrp ', environment.getattr(l_2_vrid, 'id'), ' preempt delay', ))
                    _loop_vars['delay_cli'] = l_2_delay_cli
                    if t_4(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'minimum')):
                        pass
                        l_2_delay_cli = str_join(((undefined(name='delay_cli') if l_2_delay_cli is missing else l_2_delay_cli), ' minimum ', environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'minimum'), ))
                        _loop_vars['delay_cli'] = l_2_delay_cli
                    if t_4(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'reload')):
                        pass
                        l_2_delay_cli = str_join(((undefined(name='delay_cli') if l_2_delay_cli is missing else l_2_delay_cli), ' reload ', environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'delay'), 'reload'), ))
                        _loop_vars['delay_cli'] = l_2_delay_cli
                    yield '   '
                    yield str((undefined(name='delay_cli') if l_2_delay_cli is missing else l_2_delay_cli))
                    yield '\n'
                elif t_4(environment.getattr(environment.getattr(l_2_vrid, 'preempt'), 'enabled'), False):
                    pass
                    yield '   no vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' preempt\n'
                if t_4(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'timers'), 'delay'), 'reload')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' timers delay reload '
                    yield str(environment.getattr(environment.getattr(environment.getattr(l_2_vrid, 'timers'), 'delay'), 'reload'))
                    yield '\n'
                if t_4(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'address')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' ipv4 '
                    yield str(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'address'))
                    yield '\n'
                if t_4(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'version')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' ipv4 version '
                    yield str(environment.getattr(environment.getattr(l_2_vrid, 'ipv4'), 'version'))
                    yield '\n'
                if t_4(environment.getattr(environment.getattr(l_2_vrid, 'ipv6'), 'address')):
                    pass
                    yield '   vrrp '
                    yield str(environment.getattr(l_2_vrid, 'id'))
                    yield ' ipv6 '
                    yield str(environment.getattr(environment.getattr(l_2_vrid, 'ipv6'), 'address'))
                    yield '\n'
                for l_3_tracked_obj in t_2(environment.getattr(l_2_vrid, 'tracked_object'), 'name'):
                    l_3_tracked_obj_cli = resolve('tracked_obj_cli')
                    _loop_vars = {}
                    pass
                    if t_4(environment.getattr(l_3_tracked_obj, 'name')):
                        pass
                        l_3_tracked_obj_cli = str_join(('vrrp ', environment.getattr(l_2_vrid, 'id'), ' tracked-object ', environment.getattr(l_3_tracked_obj, 'name'), ))
                        _loop_vars['tracked_obj_cli'] = l_3_tracked_obj_cli
                        if t_4(environment.getattr(l_3_tracked_obj, 'decrement')):
                            pass
                            l_3_tracked_obj_cli = str_join(((undefined(name='tracked_obj_cli') if l_3_tracked_obj_cli is missing else l_3_tracked_obj_cli), ' decrement ', environment.getattr(l_3_tracked_obj, 'decrement'), ))
                            _loop_vars['tracked_obj_cli'] = l_3_tracked_obj_cli
                        elif t_4(environment.getattr(l_3_tracked_obj, 'shutdown'), True):
                            pass
                            l_3_tracked_obj_cli = str_join(((undefined(name='tracked_obj_cli') if l_3_tracked_obj_cli is missing else l_3_tracked_obj_cli), ' shutdown', ))
                            _loop_vars['tracked_obj_cli'] = l_3_tracked_obj_cli
                        yield '   '
                        yield str((undefined(name='tracked_obj_cli') if l_3_tracked_obj_cli is missing else l_3_tracked_obj_cli))
                        yield '\n'
                l_3_tracked_obj = l_3_tracked_obj_cli = missing
            l_2_vrid = l_2_delay_cli = missing
        if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_attached_host_route_export'), 'enabled'), True):
            pass
            l_1_ip_attached_host_route_export_cli = 'ip attached-host route export'
            _loop_vars['ip_attached_host_route_export_cli'] = l_1_ip_attached_host_route_export_cli
            if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_attached_host_route_export'), 'distance')):
                pass
                l_1_ip_attached_host_route_export_cli = str_join(((undefined(name='ip_attached_host_route_export_cli') if l_1_ip_attached_host_route_export_cli is missing else l_1_ip_attached_host_route_export_cli), ' ', environment.getattr(environment.getattr(l_1_vlan_interface, 'ip_attached_host_route_export'), 'distance'), ))
                _loop_vars['ip_attached_host_route_export_cli'] = l_1_ip_attached_host_route_export_cli
            yield '   '
            yield str((undefined(name='ip_attached_host_route_export_cli') if l_1_ip_attached_host_route_export_cli is missing else l_1_ip_attached_host_route_export_cli))
            yield '\n'
        if ((t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'bfd'), 'interval')) and t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'bfd'), 'min_rx'))) and t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'bfd'), 'multiplier'))):
            pass
            yield '   bfd interval '
            yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'bfd'), 'interval'))
            yield ' min-rx '
            yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'bfd'), 'min_rx'))
            yield ' multiplier '
            yield str(environment.getattr(environment.getattr(l_1_vlan_interface, 'bfd'), 'multiplier'))
            yield '\n'
        if t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'bfd'), 'echo'), True):
            pass
            yield '   bfd echo\n'
        elif t_4(environment.getattr(environment.getattr(l_1_vlan_interface, 'bfd'), 'echo'), False):
            pass
            yield '   no bfd echo\n'
        if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'service_policy'), 'pbr'), 'input')):
            pass
            yield '   service-policy type pbr input '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_vlan_interface, 'service_policy'), 'pbr'), 'input'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'pvlan_mapping')):
            pass
            yield '   pvlan mapping '
            yield str(environment.getattr(l_1_vlan_interface, 'pvlan_mapping'))
            yield '\n'
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_virtual_router_addresses')):
            pass
            for l_2_ip_virtual_router_address in environment.getattr(l_1_vlan_interface, 'ip_virtual_router_addresses'):
                _loop_vars = {}
                pass
                yield '   ip virtual-router address '
                yield str(l_2_ip_virtual_router_address)
                yield '\n'
            l_2_ip_virtual_router_address = missing
        if t_4(environment.getattr(l_1_vlan_interface, 'ip_address_virtual')):
            pass
            yield '   ip address virtual '
            yield str(environment.getattr(l_1_vlan_interface, 'ip_address_virtual'))
            yield '\n'
            if t_4(environment.getattr(l_1_vlan_interface, 'ip_address_virtual_secondaries')):
                pass
                for l_2_ip_address_virtual_secondary in environment.getattr(l_1_vlan_interface, 'ip_address_virtual_secondaries'):
                    _loop_vars = {}
                    pass
                    yield '   ip address virtual '
                    yield str(l_2_ip_address_virtual_secondary)
                    yield ' secondary\n'
                l_2_ip_address_virtual_secondary = missing
        if t_4(environment.getattr(l_1_vlan_interface, 'eos_cli')):
            pass
            yield '   '
            yield str(t_3(environment.getattr(l_1_vlan_interface, 'eos_cli'), 3, False))
            yield '\n'
    l_1_vlan_interface = l_1_ipv6_attached_host_route_export_cli = l_1_host_proxy_cli = l_1_interface_ip_nat = l_1_hide_passwords = l_1_ip_attached_host_route_export_cli = missing

blocks = {}
debug_info = '7=36&9=45&10=47&11=50&13=52&15=55&18=58&19=61&21=63&24=66&25=69&27=71&29=74&32=77&33=80&35=82&38=85&41=88&42=91&44=93&45=95&46=98&48=100&49=103&51=105&55=108&58=111&61=114&62=117&63=119&64=121&65=125&69=128&70=131&72=133&75=136&78=139&79=143&80=145&81=147&83=149&84=151&86=154&88=157&89=161&90=163&91=165&93=167&94=169&95=171&96=173&98=175&99=177&101=180&103=183&104=185&105=187&106=189&108=191&109=193&111=196&113=198&116=201&117=204&119=206&120=208&121=211&122=213&123=215&124=218&125=220&126=222&127=226&130=233&131=235&132=239&135=246&136=249&140=254&141=256&142=260&145=265&146=268&148=272&149=275&152=279&155=282&156=285&158=287&159=290&161=292&162=295&164=297&165=301&167=304&170=307&173=310&176=313&177=315&178=319&179=321&180=323&181=325&182=327&185=329&186=331&188=334&191=337&192=339&193=341&194=345&195=347&196=349&198=352&201=355&202=357&203=361&206=364&207=366&208=369&213=374&214=376&215=379&220=384&223=387&227=390&228=392&229=394&231=397&232=400&234=402&235=405&237=407&238=410&240=412&241=415&243=417&246=420&247=423&249=425&250=428&252=430&253=432&255=435&259=438&260=441&262=443&263=446&265=449&268=456&271=459&274=462&277=465&278=468&280=470&281=473&283=475&284=478&286=480&289=483&290=486&294=488&295=491&298=493&299=495&300=499&303=502&304=505&306=507&309=510&312=513&313=516&315=518&319=521&320=523&321=526&323=530&324=533&326=537&327=540&329=544&330=547&332=551&333=554&337=558&338=560&339=568&340=571&342=575&343=578&345=582&348=584&349=586&350=588&352=590&353=592&355=595&356=597&357=600&359=602&360=605&362=609&363=612&365=616&366=619&368=623&369=626&371=630&372=634&373=636&374=638&375=640&376=642&377=644&379=647&384=651&385=653&386=655&387=657&389=660&391=662&394=665&396=671&398=674&401=677&402=680&404=682&405=685&407=687&408=689&409=693&412=696&413=699&414=701&415=703&416=707&420=710&421=713'