# Batch Asset Export for Blender

![img](https://hendasheng-web.oss-cn-beijing.aliyuncs.com/Media/Image/Cover/Blender%20Batch%20Asset%20Export_en.png?x-oss-process=image/format,webp/quality,q_80)

Blender add-on for batch exporting selected objects to OBJ and GLB.

[中文文档](README_CN.md)

## Features

![img](https://hendasheng-web.oss-cn-beijing.aliyuncs.com/Weekly/vol.162/2026-05-03%2015-58-46_demo.gif)

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
1. [Download Blender Add-on](https://github.com/hendasheng/batch-asset-export-blender-addon/releases)
2. Open Blender
3. Go to `Edit > Preferences > Add-ons`
4. Click `Install...`
5. Choose the downloaded plugin zip package
6. Enable `Batch Asset Export`

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
- If `Geometry Nodes` export is empty, make sure `Realize Instances` has been applied first.
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
