from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos-intended-config.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_eos_cli_config_gen_configuration = resolve('eos_cli_config_gen_configuration')
    l_0_hide_passwords = missing
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    pass
    l_0_hide_passwords = t_1(environment.getattr((undefined(name='eos_cli_config_gen_configuration') if l_0_eos_cli_config_gen_configuration is missing else l_0_eos_cli_config_gen_configuration), 'hide_passwords'), False)
    context.vars['hide_passwords'] = l_0_hide_passwords
    context.exported_vars.add('hide_passwords')
    template = environment.get_template('eos/rancid-content-type.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/config-comment.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/boot.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/agents.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/terminal.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/prompt.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/aliases.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/hardware-counters.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/service-routing-configuration-bgp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/daemon-terminattr.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/daemons.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dhcp-relay.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-dhcp-relay.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-dhcp-relay.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-dhcp-snooping.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dhcp-servers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/switchport-default.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vlan-internal-order.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-igmp-snooping.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/event-monitor.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/flow-tracking.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/flow-trackings.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/load-interval.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/interface-defaults.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/interface-profiles.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/transceiver-qsfp-default-mode.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/errdisable.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/service-routing-protocols-model.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/queue-monitor-length.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/monitor-layer1.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/lldp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/l2-protocol-forwarding.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/lacp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/logging.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mcs-client.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/match-list-input.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/as-path.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mac-security.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-nat-part1.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/platform-trident.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/hostname.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-domain-lookup.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-name-servers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dns-domain.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/domain-list.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/trackers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/switchport-port-security.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-adaptive-virtual-topology.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-internet-exit.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-l2-vpn.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-path-selection.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ntp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/poe.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ptp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/radius-servers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/radius-server.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/sflow.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/redundancy.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/qos-profiles.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-service-insertion.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/snmp-server.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/hardware.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/spanning-tree.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/sync-e.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/platform.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/service-unsupported-transceiver.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/tacacs-servers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/aaa.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/enable-password.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/aaa-root.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/local-users.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/roles.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/address-locking.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/system-l1.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/tap-aggregation.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/clock.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vlans.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vrfs.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/link-tracking-groups.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/cvx.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/monitor-telemetry-influx.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-security.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/port-channel-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dps-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ethernet-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/loopback-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/tunnel-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vlan-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vxlan-interface.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/tcam-profile.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/application-traffic-recognition.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/monitor-connectivity.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mac-address-table-aging-time.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-virtual-router-mac-address.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/virtual-source-nat-vrfs.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/event-handlers.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/bgp-groups.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/interface-groups.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-standard-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/standard-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mac-access-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-routing.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-icmp-redirect.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-hardware.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-routing-vrfs.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-unicast-routing.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-unicast-routing-vrfs.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-icmp-redirect.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-hardware.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/monitor-sessions.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/qos.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/priority-flow-control.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/community-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-community-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-extcommunity-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-extcommunity-lists-regexp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dynamic-prefix-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/prefix-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-prefix-lists.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/system.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mac-address-table-notification.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/maintenance.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mlag-configuration.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-neighbors.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/static-routes.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ipv6-static-routes.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-nat-part2.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/class-maps.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/policy-maps-copp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/policy-maps-pbr.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/monitor-telemetry-postcard-policy.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/policy-maps-qos.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/arp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/route-maps.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-bfd.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/peer-filters.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-bgp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-igmp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-multicast.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-general.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-segment-security.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-traffic-engineering.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-ospf.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-pim-sparse-mode.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-isis.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/router-msdp.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/mpls.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/patch-panel.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/queue-monitor-streaming.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-tacacs-source-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-radius-source-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/vmtracer-sessions.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/traffic-policies.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/banners.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/ip-client-source-interfaces.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-accounts.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-api-http.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-console.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-cvx.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-defaults.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-api-gnmi.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-api-models.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-security.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/stun.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/dot1x.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-ssh.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/management-tech-support.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/platform-apply.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/eos-cli.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event
    template = environment.get_template('eos/end.j2', 'eos-intended-config.j2')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'hide_passwords': l_0_hide_passwords})):
        yield event

blocks = {}
debug_info = '8=19&9=22&10=25&12=28&14=31&16=34&18=37&20=40&22=43&24=46&26=49&28=52&30=55&32=58&34=61&36=64&38=67&40=70&42=73&44=76&46=79&48=82&49=85&51=88&53=91&55=94&57=97&59=100&61=103&63=106&65=109&67=112&69=115&71=118&73=121&75=124&77=127&79=130&81=133&83=136&85=139&87=142&89=145&91=148&93=151&95=154&97=157&99=160&101=163&103=166&105=169&107=172&109=175&111=178&113=181&115=184&117=187&119=190&121=193&123=196&125=199&127=202&129=205&131=208&133=211&135=214&137=217&139=220&141=223&143=226&145=229&147=232&149=235&151=238&153=241&155=244&157=247&159=250&161=253&163=256&165=259&167=262&169=265&171=268&173=271&175=274&177=277&179=280&181=283&183=286&185=289&187=292&189=295&191=298&193=301&195=304&197=307&199=310&201=313&203=316&205=319&207=322&209=325&211=328&213=331&215=334&217=337&219=340&221=343&223=346&225=349&227=352&229=355&231=358&233=361&235=364&237=367&239=370&241=373&243=376&245=379&247=382&249=385&251=388&253=391&255=394&257=397&259=400&261=403&263=406&265=409&267=412&269=415&271=418&273=421&275=424&277=427&279=430&281=433&283=436&285=439&287=442&289=445&291=448&293=451&295=454&297=457&299=460&301=463&303=466&305=469&307=472&309=475&311=478&313=481&315=484&317=487&319=490&321=493&323=496&325=499&327=502&329=505&331=508&333=511&335=514&337=517&339=520&341=523&343=526&345=529&347=532&349=535&351=538&353=541'