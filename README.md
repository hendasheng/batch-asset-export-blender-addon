# Batch Asset Export for Blender

Blender add-on for batch exporting selected objects to OBJ and GLB.

- [中文文档](README_CN.md)

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

1. [Download Blender Add-on](https://github.com/hendasheng/batch-asset-export-blender-addon/releases)
3. In Blender, open `Edit > Preferences > Add-ons`
4. Click `Install...`
5. Choose the downloaded plugin zip package
6. Enable `Batch Asset Export`

Alternative:

1. In Blender, open `Edit > Preferences > Add-ons`
2. Click `Install...`
3. Choose the add-on zip package, or install from this repo after zipping the `Batch_Asset_Export` folder
4. Enable `Batch Asset Export`

## Panel Location

- `View3D > Sidebar > Batch Export`

## Usage

1. Enable the formats you want to export
   - `Export OBJ`
   - `Export GLB`
2. Set output directories for the enabled formats
   - You can click the folder button on the right
   - Or enter a Blender relative path such as `//../output/...`
3. Set options as needed
   - `Reset To Origin`
4. Select the objects you want to export in `Object Mode`
5. Click `Export Selected`

## Notes

- Download the plugin package from the version download page, not GitHub's automatically generated source code zip.
- Set output paths before exporting.
- If Geometry Nodes export is empty, realize instances first.
- Recheck output paths when switching projects.

## Repository Structure

- `Batch_Asset_Export/__init__.py`
  - Main add-on file
- `Batch_Asset_Export/README.md`
  - Short add-on note inside the plugin folder
- `README.md`
  - English documentation
- `README_CN.md`
  - Chinese documentation
