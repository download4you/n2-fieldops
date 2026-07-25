# n2-fieldops 1.0.1

Maintenance release for the initial n2-fieldops 1.0.0 product line.

## Fixes

- Release archives are byte-for-byte reproducible across Windows and Linux
  checkouts: text is LF-normalized, entry ordering is POSIX-stable, and ZIP creator
  metadata is explicit.
- Source archives include only Git-tracked files, preventing ignored local settings
  or editor artifacts from entering a release.
- Added cross-checkout hash and archive-metadata tests.
- Updated CC Switch instructions for the current Repository URL + Branch interface.

## Compatibility

The canonical repository remains one root-level tree with exactly 17 `SKILL.md`
directories. Install from CC Switch with:

```text
Repository URL: https://github.com/download4you/n2-fieldops
Branch: main
```

The native Claude plugin and marketplace bundles are generated from the same
canonical tree.

## Release assets

- `n2-fieldops-1.0.1-source.zip`
- `n2-fieldops-1.0.1-claude-plugin.zip`
- `n2-fieldops-1.0.1-claude-marketplace.zip`
- `SHA256SUMS`
