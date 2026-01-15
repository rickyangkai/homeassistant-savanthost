# SavantHost for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Maintainer](https://img.shields.io/badge/maintainer-%40rickyangkai-blue.svg)](https://github.com/rickyangkai)

一个用于将 **Savant 主机场景** 无缝接入 **Home Assistant** 的自定义组件。
无需复杂的 YAML 配置，支持自动发现、自动同步与一键控制。

---

## ✨ 核心功能

- **🚀 自动发现**：利用 Zeroconf (mDNS) 技术，自动扫描局域网内的 Savant 主机 IP 和端口。
- **🔄 自动同步**：插件启动后自动获取主机上的所有场景，并创建为 Home Assistant `scene` 实体。
- **🔐 安全授权**：内置企业级激活验证机制，确保系统授权使用。
- **⏱️ 实时保活**：每 5 分钟自动同步一次场景列表，确保场景增删改实时生效。
- **🔌 无需配置**：无需手动填写 IP 地址，全自动引导流程。

## 📋 前置要求

1. **Savant 主机**：必须开启 OpenAPI 功能（通常默认开启）。
2. **网络环境**：Home Assistant 必须与 Savant 主机处于同一局域网，且路由器未拦截 mDNS (Multicast) 广播。
3. **授权码**：首次使用需要输入激活码（与 Homebridge 版通用）。

## 📦 安装指南

### 方式一：使用 HACS 安装 (推荐)

这是管理更新最简单的方法。

1. 打开 Home Assistant 的 **HACS** 页面。
2. 点击右上角菜单 > **Custom repositories** (自定义仓库)。
3. 在 URL 栏输入本仓库地址：`https://github.com/rickyangkai/homeassistant-savanthost`。
4. 类别选择 **Integration**。
5. 点击 **ADD** 添加仓库。
6. 在 HACS 集成列表中搜索 **SavantHost** 并点击 **Download**。
7. 下载完成后，**重启 Home Assistant**。

### 方式二：手动安装

1. 下载本仓库的最新 Release 压缩包。
2. 解压后，将 `custom_components/savanthost` 文件夹复制到您 Home Assistant 配置目录下的 `custom_components/` 文件夹中。
3. 目录结构应如下所示：
   ```text
   /config/custom_components/savanthost/__init__.py
   /config/custom_components/savanthost/manifest.json
   ...
   ```
4. **重启 Home Assistant**。

## ⚙️ 配置与使用

### 1. 添加集成
1. 前往 **配置 (Settings)** > **设备与服务 (Devices & Services)**。
2. 点击右下角的 **+ 添加集成 (+ ADD INTEGRATION)**。
3. 搜索 **SavantHost** 并点击。

### 2. 激活与连接
1. **输入激活码**：在弹出的对话框中，系统会显示您的**设备地址码**。请联系开发者获取对应的**授权码**并填入。
2. **自动搜索**：验证通过后，插件会自动扫描局域网。
   - **单台主机**：如果只发现一台 Savant 主机，将自动连接并完成配置。
   - **多台主机**：如果发现多台，将弹出下拉列表供您选择。
   - **未发现主机**：如果超时未找到（可能是网络隔离导致），系统将允许您手动输入 IP 地址和端口。

### 3. 使用场景
配置完成后，您的 Savant 场景将自动出现在 Home Assistant 的 **场景 (Scenes)** 列表中。
- 实体 ID 格式通常为：`scene.savant_scene_[scene_id]`。
- 您可以直接在 Dashboard 中调用，或在自动化脚本中使用 `scene.turn_on` 服务来触发。

## ❓ 常见问题 (FAQ)

**Q: 提示“无效的授权码”怎么办？**
A: 请确保您提供的“设备地址码”是准确的（区分大小写，通常为全大写），并且填入的授权码与该设备一一对应。

**Q: 找不到 Savant 主机？**
A: 请检查 HA 与 Savant 主机是否在同一网段（VLAN）。如果跨网段，mDNS 可能无法通过，您可以在扫描失败后手动输入 IP 地址。

**Q: 场景更新了但 HA 里没有变？**
A: 插件每 5 分钟自动同步一次。如果您刚修改了 Savant 场景，可以手动重载集成或稍等片刻。

## 📄 版权与许可

Copyright © 2024-2026 Rick Yang. All rights reserved.
本插件仅供测试与交流使用，禁止用于商业用途。

测试提交