# Generated Release Packages

This directory is the stable repo-local landing path for generated release-package snapshots.

When release-package publishing has been run, the latest generated entrypoints will be maintained here:

- `latest.md`
- `latest.json`
- `PUBLICATION_MANIFEST.json`
- `PUBLICATION_INDEX.md`
- `<version>/README.md`
- `<version>/MANIFEST.json`

Generate or refresh this path with:

```bash
python governance_tools/release_package_snapshot.py --version v1.0.0-alpha --publish-docs-release --format human
```

Read the generated release root with:

```bash
python governance_tools/release_package_publication_reader.py --project-root . --docs-release-root --format human
```
