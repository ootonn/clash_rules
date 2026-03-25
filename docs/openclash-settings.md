# OpenClash Settings Baseline

## Scope

This repository assumes a split of responsibilities:

- `clash_config.ini` only defines policy groups and remote rule sources.
- OpenClash owns runtime DNS behavior, DNS hijack, fake-IP storage, and geodata refresh.
- The router runs Mihomo Meta core in `fake-ip` + `rule` mode.

If this runtime baseline is not kept, the rule design in this repo will not behave as intended.

## Router baseline

### Core and mode

Apply this baseline in OpenClash:

- Core: `Meta / Mihomo`
- Proxy mode: `rule`
- Operation mode: `fake-ip`
- Enable custom DNS: `1`
- Enable redirect DNS: `1`
- Redirect DNS: `1`
- Enable respect rules: `1`
- Store fake IP: `1`
- Disable UDP QUIC: `1`
- IPv6: `0` unless WAN and LAN IPv6 are already validated end to end

### Geodata

Enable all geodata auto update switches:

- `geosite_auto_update=1`
- `geoip_auto_update=1`
- `geo_auto_update=1`

This repo now uses `GEOSITE/GEOIP` as the main backbone for AI, Google, Steam, communication, social, and CN routing. Disabling geodata refresh will eventually age out rule accuracy.

## DNS design

### Goal

The intended path is:

`client -> dnsmasq -> OpenClash :7874 -> encrypted upstream DNS`

The important part is not only “clients use the router”, but also “OpenClash itself avoids plain UDP upstream DNS whenever possible”.

### Required constraints

- LAN DHCP must hand out the router itself as DNS, not public resolvers.
- `dnsmasq` must use `127.0.0.1#7874`.
- `dnsmasq noresolv` should be enabled.
- WAN `peerdns` should be disabled.
- OpenClash active `nameserver`, `fallback`, and `proxy-server-nameserver` should only contain encrypted upstream resolvers.

### Recommended resolver layout

#### default-nameserver

Use a minimal bootstrap set for resolving encrypted DNS hostnames:

- `119.29.29.29`
- `223.5.5.5`

Keep this set small. It is bootstrap only, not the main working resolver pool.

#### nameserver

Use domestic encrypted DNS for primary direct resolution:

- `https://doh.pub/dns-query`
- `https://dns.alidns.com/dns-query`

Remove active plain UDP entries from the `nameserver` group.

#### proxy-server-nameserver

Use encrypted overseas resolvers here:

- `https://1.1.1.1/dns-query`
- `https://dns.google/dns-query`

This group is for proxy node hostname resolution. Keeping it on encrypted overseas resolvers reduces the chance of domestic-path DNS pollution on foreign node domains.

#### fallback

Use encrypted overseas resolvers only:

- `https://1.1.1.1/dns-query`
- `https://dns.google/dns-query`

Disable redundant plain `tls://1.1.1.1` or extra mixed entries if they are still present from old configs.

## OpenClash UI mapping

If you want to apply this from the LuCI UI instead of editing UCI directly, use this checklist:

### Overwrite Settings

- Enable custom DNS
- Enable redirect DNS
- Enable respect rules
- Enable fake-IP persistence
- Keep proxy mode at `rule`
- Keep enhanced mode at `fake-ip`

### DNS Settings

- `Default DNS`: `119.29.29.29`, `223.5.5.5`
- `NameServer`: `https://doh.pub/dns-query`, `https://dns.alidns.com/dns-query`
- `Proxy Server NameServer`: `https://doh.pub/dns-query`, `https://dns.alidns.com/dns-query`, `https://1.1.1.1/dns-query`
- `Fallback`: `https://1.1.1.1/dns-query`, `https://dns.google/dns-query`

### DHCP / DNSMasq

- Ensure LAN DHCP still gives out `192.168.6.1`
- Do not set public DNS in DHCP option 6
- Ensure `dnsmasq` forwards to `127.0.0.1#7874`

## Subscription expectation

The `xxx` subscription entry should continue to reference the user-owned subconverter URL, and that URL should already contain:

- the subscription source URL
- this repository `main` branch `clash_config.ini`

After each push to `main`, refresh the OpenClash subscription or reload the current config so the router rebuilds `/etc/openclash/xxx.yaml` from the new template.

## Verification checklist

After changing the router, verify these items:

- `uci show openclash.config` still shows `core_type='Meta'`, `proxy_mode='rule'`, `operation_mode='fake-ip'`
- `uci show dhcp.@dnsmasq[0]` shows `noresolv='1'`
- `uci show network.wan` shows `peerdns='0'`
- `/etc/openclash/xxx.yaml` runtime `dns:` block only keeps plain UDP under `default-nameserver` bootstrap if needed, and does not keep active plain UDP entries in `nameserver`, `proxy-server-nameserver`, or `fallback`
- `nslookup github.com 127.0.0.1#7874`
- `nslookup openai.com 127.0.0.1#7874`

## Local patch philosophy

- Keep `direct_own.list` tiny and explicit.
- Keep `ai_patch.list` tiny and only for upstream AI gaps.
- Keep `🌍 国外` broad enough to remain the main non-CN catch-all, instead of pushing ordinary foreign traffic into `🐟 漏网之鱼`.
- Do not reintroduce broad local CN IP tables.
