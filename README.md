# Batch Asset Export for Blender

Blender add-on for batch exporting selected objects to OBJ and GLB.

- [中文文档.md](README_CN.md)
- [Download Plugin Package](https://github.com/hendasheng/batch-asset-export-blender-addon/releases)

## Features

- Supports:
  - Collection Instance
  - Mesh
  - Curve
  - Realized Geometry Nodes results
- One selected object exports one OBJ and/or one GLB
- Recursive support for nested collections inside collection instances
- Optional reset-to-origin transform behavior
- Chinese / English UI following Blender language

## Installation

Recommended:

1. Open the download page:
   - https://github.com/hendasheng/batch-asset-export-blender-addon/releases
2. Download the plugin zip package attached to the latest version
3. In Blender, open `Edit > Preferences > Add-ons`
4. Click `Install...`
5. Choose the downloaded plugin zip package
6. Enable `Batch Asset Export`

Alternative:

1. In Blender, open `Edit > Preferences > Add-ons`
2. Click `Install...`
3. Choose the add-on zip package, or install from this repo after zipping the `Batch_Asset_Export` folder
4. Enable `Batch Asset Export`

## Notes

- Download the plugin package zip from the version download page, not GitHub's automatically generated source code zip.
- Set output paths before exporting.
- If Geometry Nodes export is empty, realize instances first.
