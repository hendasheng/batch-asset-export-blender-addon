# Batch Asset Export for Blender

用于 Blender 的批量导出插件，可将当前选中的对象批量导出为 `OBJ` 和 `GLB`。

- [English Doc.md](README.md)
- [下载安装包](https://github.com/hendasheng/batch-asset-export-blender-addon/releases)

## 功能

- 支持对象类型：
  - `Collection Instance`
  - `Mesh`
  - `Curve`
  - 已经能评估为实际几何的 `Geometry Nodes` 结果
- 每个选中对象导出一组文件
  - 一个 `OBJ`
  - 一个 `GLB`
- 支持递归处理集合实例中的嵌套集合
- 支持“位置归零”开关
- 界面支持中英文，会跟随 Blender 语言切换

## 安装

推荐方式：

1. 打开插件下载页面：
   - https://github.com/hendasheng/batch-asset-export-blender-addon/releases
2. 下载最新版本下面附带的插件 zip 安装包
3. 打开 Blender
4. 进入 `Edit > Preferences > Add-ons`
5. 点击 `Install...`
6. 选择刚下载的插件 zip 文件
7. 启用 `Batch Asset Export`

备用方式：

1. 打开 Blender
2. 进入 `Edit > Preferences > Add-ons`
3. 点击 `Install...`
4. 选择插件 zip 包，或将仓库中的 `Batch_Asset_Export` 文件夹打包后安装
5. 启用 `Batch Asset Export`

## 面板位置

- `View3D > Sidebar > Batch Export`

## 使用方法

1. 先勾选需要导出的格式
   - `Export OBJ`
   - `Export GLB`
2. 为已勾选的格式设置输出目录
   - 可以直接点击右侧文件夹按钮选择
   - 也可以填写 Blender 相对路径，例如 `//../output/...`
3. 按需设置
   - `Reset To Origin`
4. 在 `Object Mode` 下选中需要导出的对象
5. 点击 `Export Selected`

## 注意事项

- 请下载版本页面里附带的插件安装包，不要下载 GitHub 自动生成的源码压缩包
- 导出前必须先设置输出路径，否则插件会阻止导出
- 如果 `Geometry Nodes` 导出为空，先检查是否已经“实现实例（Realize Instances）”
- 每次换项目都建议重新确认输出目录

## 仓库结构

- `Batch_Asset_Export/__init__.py`
  - 插件主文件
- `Batch_Asset_Export/README.md`
  - 插件目录内简要说明
- `README.md`
  - 英文说明
- `README_CN.md`
  - 中文说明
