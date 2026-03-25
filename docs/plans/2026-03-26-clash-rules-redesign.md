# Clash Rules Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refactor `clash_rules` to keep the current traffic-group layout while replacing risky rule sources with maintained `GEOSITE/GEOIP` sources, removing generated artifacts, and documenting the resulting OpenClash-compatible design.

**Architecture:** Keep `clash_config.ini` as the single subscription-converter entrypoint, but simplify its sources so the backbone is `GEOSITE/GEOIP` plus a minimal local direct patch file. Remove generated outputs and dangerous custom CN IP tables. Sanitize the helper script so the repo no longer stores live subscription data.

**Tech Stack:** Subconverter INI templates, Mihomo/OpenClash `GEOSITE/GEOIP`, PowerShell validation, Python utility script.

---

### Task 1: Save the approved design and prepare the repo

**Files:**
- Create: `docs/plans/2026-03-26-clash-rules-redesign-design.md`
- Create: `docs/plans/2026-03-26-clash-rules-redesign.md`
- Modify: `.gitignore`

**Step 1: Add the approved design document**

Write the design summary, rule-source decisions, and validation approach into `docs/plans/2026-03-26-clash-rules-redesign-design.md`.

**Step 2: Add the implementation plan**

Write this implementation plan into `docs/plans/2026-03-26-clash-rules-redesign.md`.

**Step 3: Ignore generated outputs**

Update `.gitignore` so generated files such as `output.yaml` and temporary output directories stay out of version control.

**Step 4: Verify repo structure**

Run: `git -C C:\Users\ootonn\Documents\Repos\clash_rules status --short`
Expected: only intended doc/config changes appear.

### Task 2: Replace risky and duplicated active rule sources

**Files:**
- Modify: `clash_config.ini`
- Create: `ai_patch.list`

**Step 1: Rewrite the AI section to upstream geosite entries**

Use:

- `[]GEOSITE,openai`
- `[]GEOSITE,anthropic`
- `[]GEOSITE,google-gemini`
- `[]GEOSITE,meta`
- `[]GEOSITE,xai`
- `[]GEOSITE,perplexity`
- `[]GEOSITE,bing`
- `[]GEOSITE,category-ai-!cn`

**Step 2: Remove dead and low-trust sources**

Delete the dead `liandu2024` YouTube rule and the low-trust `WC-Dream` direct/proxy sources.

**Step 3: Collapse duplicated category lists into maintained geosite/ge oip rules**

Replace duplicated `blackmatrix7` streaming/global/china sources with maintained `GEOSITE/GEOIP` entries while keeping the current policy group layout intact.

Add a tiny `ai_patch.list` only if a required AI domain is still missing upstream.

Keep `🌍 国外` broad enough to remain the main non-CN catch-all. A retained `Global.list` fallback is acceptable here if removing it would push ordinary foreign traffic into `🐟 漏网之鱼`.

**Step 4: Verify risky sources are gone**

Run:

```powershell
Select-String -Path 'C:\Users\ootonn\Documents\Repos\clash_rules\clash_config.ini' -Pattern 'AI.list|AI2.list|cniplist|C_cniplist|liandu2024|WC-Dream|China.list|ChinaIp.list|ChinaDomain.list|ChinaCompanyIp.list'
```

Expected: no matches for removed active sources.

### Task 3: Clean local patch files and remove obsolete files

**Files:**
- Modify: `direct_own.list`
- Delete: `AI.list`
- Delete: `AI2.list`
- Delete: `cniplist.list`
- Delete: `C_cniplist.list`
- Delete: `output.yaml`

**Step 1: Narrow the direct patch list**

Remove the broad `ootonn.com` direct suffix while keeping the user’s explicit remaining direct entries.

**Step 2: Remove obsolete AI lists**

Delete `AI.list` and `AI2.list` after their coverage is moved to upstream geosite entries.

**Step 3: Remove dangerous CN IP tables**

Delete `cniplist.list` and `C_cniplist.list`.

**Step 4: Remove generated output**

Delete `output.yaml`.

**Step 5: Verify git tracks only source files**

Run: `git -C C:\Users\ootonn\Documents\Repos\clash_rules ls-files`
Expected: removed runtime/generated files are gone.

### Task 4: Sanitize the helper script

**Files:**
- Modify: `subscription_tester.py`

**Step 1: Remove the embedded subscription token**

Change the default subscription URL so the script no longer ships a live token.

**Step 2: Move the default output out of the repo root artifact path**

Write generated output into a temporary directory such as `./tmp/output.yaml`.

**Step 3: Verify the helper no longer exposes secrets**

Run:

```powershell
Select-String -Path 'C:\Users\ootonn\Documents\Repos\clash_rules\subscription_tester.py' -Pattern 'token='
```

Expected: no live token value remains.

### Task 5: Validate the final rule source set

**Files:**
- Modify: `clash_config.ini`

**Step 1: Check every remote URL**

Run a validation script that extracts all `http/https` URLs from `clash_config.ini` and confirms they return success.

**Step 2: Check final git status**

Run: `git -C C:\Users\ootonn\Documents\Repos\clash_rules status --short`
Expected: only intended tracked changes remain.

**Step 3: Review the final diff**

Run: `git -C C:\Users\ootonn\Documents\Repos\clash_rules diff -- .`
Expected: the diff shows the streamlined rule set, removed artifacts, and sanitized helper defaults.
