# Batch Asset Export for Blender

Blender add-on for batch exporting selected objects to OBJ and GLB.

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

1. In Blender, open `Edit > Preferences > Add-ons`
2. Click `Install...`
3. Choose the add-on zip package, or install from this repo after zipping the `Batch_Asset_Export` folder
4. Enable `Batch Asset Export`

## Notes

- Set output paths before exporting.
- If Geometry Nodes export is empty, realize instances first.
