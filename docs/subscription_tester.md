# subscription_tester.py

## Purpose

`subscription_tester.py` is only a local verification helper. It is not part of the router runtime.

Use it to check whether your subconverter endpoint can still generate a valid Clash YAML after this repository template changes.

## Current behavior

- A subscription URL is now required as the first positional argument.
- The default template is this repository `main` branch `clash_config.ini`.
- The default output file is `./tmp/output.yaml`, not the repository root.
- The script no longer contains a real subscription token by default.

## Example

```powershell
python .\subscription_tester.py "https://example.com/sub/xxxx"
```

If you need to point at a self-hosted subconverter and write to a custom file:

```powershell
python .\subscription_tester.py `
  "https://example.com/sub/xxxx" `
  --base "http://127.0.0.1:25500" `
  --config "https://raw.githubusercontent.com/ootonn/clash_rules/refs/heads/main/clash_config.ini" `
  --output ".\\tmp\\check.yaml"
```

## Expected result

- Exit code `0`: subconverter returned valid YAML and the file was written successfully.
- Exit code `1`: request failed or the returned content was not valid YAML.

## Notes

- If the generated YAML fails, check the reachable rule URLs in `clash_config.ini` first.
- `tmp/` is intentionally ignored and should not be committed.
