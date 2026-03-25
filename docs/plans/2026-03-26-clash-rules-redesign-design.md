# Clash Rules Redesign Design

## Goal

Refactor `clash_rules` into an OpenClash-friendly source repository that keeps the existing traffic-group layout while removing risky custom rule sources, reducing duplication, and relying on maintained `GEOSITE/GEOIP` data for the main rule backbone.

## Current Problems

- `clash_config.ini` mixes maintained upstream sources with low-trust custom lists and dead URLs.
- `cniplist.list` and `C_cniplist.list` contain broad CN IP rules that can misroute international traffic to `DIRECT`.
- `AI.list` and `AI2.list` duplicate upstream AI coverage and include broad infrastructure domains.
- `direct_own.list` contains an over-broad `ootonn.com` direct rule.
- `output.yaml` is a generated artifact with live runtime data and should not live in the repo.
- `subscription_tester.py` contains a hardcoded subscription token and writes to `output.yaml` by default.

## Design Decisions

### 1. Keep the existing policy-group layout

The current user-facing groups stay in place:

- `🎯 直连`
- `👽 AI`
- `📘 GitHub`
- `🍎 苹果服务`
- `Ⓜ️ 微软服务`
- `📢 谷歌FCM`
- `🇬 谷歌服务`
- `🚀 测速工具`
- `💬 即时通讯`
- `🌐 社交媒体`
- `📀 流媒体`
- `🎮 Steam`
- `🌍 国外`
- `➡️ 国内`
- `🐟 漏网之鱼`

Only the rule sources behind these groups are changed.

### 2. Use `GEOSITE/GEOIP` as the primary rule backbone

The repo already depends on `GEOSITE`. The redesign standardizes on that instead of maintaining large overlapping text lists.

Main sources:

- `GEOSITE` for service/domain-oriented matching
- `GEOIP` only where IP matching is still useful and explicit
- small local patch files only when upstream coverage is missing

### 3. AI routing becomes explicit and upstream-driven

`👽 AI` will use explicit upstream entries instead of large local AI lists:

- `openai`
- `anthropic`
- `google-gemini`
- `meta`
- `xai`
- `perplexity`
- `bing`
- `category-ai-!cn`

If an AI domain is still missing upstream, it is added through a minimal local patch list instead of reviving the old broad `AI.list` files.

This preserves readability while still benefiting from maintained upstream datasets.

### 4. Remove risky and low-value sources

The following sources are removed from active use:

- `liandu2024/.../YouTube.list`
- `WC-Dream/ACL4SSR/WD/Clash/proxy.list`
- `WC-Dream/ACL4SSR/WD/Clash/direct.list`
- `blackmatrix7` list sources that duplicate maintained `GEOSITE` categories
- local `cniplist.list`
- local `C_cniplist.list`

`🌍 国外` stays intentionally broad. It can keep a maintained global fallback list in addition to `ProxyGFWlist.list` so ordinary foreign traffic does not collapse into `🐟 漏网之鱼`.

### 5. Treat the repo as source, not runtime output

- `output.yaml` is removed from the repo.
- `.gitignore` is updated to ignore generated outputs.
- `subscription_tester.py` is changed so it no longer embeds a real subscription URL and no longer writes `output.yaml` in the repo root by default.

## File-Level Outcome

### Keep and modify

- `clash_config.ini`
- `direct_own.list`
- `ai_patch.list`
- `.gitignore`
- `subscription_tester.py`

### Remove

- `AI.list`
- `AI2.list`
- `cniplist.list`
- `C_cniplist.list`
- `output.yaml`

### Add

- `docs/plans/2026-03-26-clash-rules-redesign-design.md`
- `docs/plans/2026-03-26-clash-rules-redesign.md`

## OpenClash Compatibility

This design assumes:

- OpenClash handles runtime DNS settings and policy runtime behavior.
- The repo provides only subscription-converter rule layout plus a few local patch rules.
- `GEOSITE/GEOIP` updates are handled by current Mihomo/OpenClash tooling.

This matches the current direction used by `Aethersailor/Custom_OpenClash_Rules`: keep the rule source concise and let OpenClash own runtime settings.

## Validation Strategy

- Verify every remote rule URL in `clash_config.ini` responds successfully.
- Verify removed risky sources no longer appear in `clash_config.ini`.
- Verify deleted generated artifacts are ignored by git.
- Verify `subscription_tester.py` no longer contains a real subscription token by default.
