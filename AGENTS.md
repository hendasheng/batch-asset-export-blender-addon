# AGENTS.md

This repository contains the Blender add-on `Batch Asset Export`.

## Documentation Rules

1. `README_CN.md` is the source of truth for user-facing documentation.
2. If `README_CN.md` is updated, `README.md` must be updated in the same change.
3. The English README must stay fully aligned with the Chinese README in:
   - structure
   - installation steps
   - feature list
   - notes
   - repository structure
4. Do not leave the English README partially updated after a Chinese documentation change.

## Preferred Workflow

1. Edit `README_CN.md` first.
2. Immediately mirror the same meaning and structure into `README.md`.
3. Review both files side by side before committing.

## Add-on Scope

The add-on supports:

- Collection Instance
- Mesh
- Curve
- Realized Geometry Nodes results

Main export targets:

- OBJ
- GLB

## Release / Download Guidance

When updating installation guidance:

- direct users to the GitHub Releases page
- tell users to download the plugin package zip
- do not tell users to download GitHub's automatically generated source code zip
