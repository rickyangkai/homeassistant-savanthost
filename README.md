# SavantHost for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

一个用于将 Savant 主机场景无缝接入 Home Assistant 的自定义组件。

## ✨ 功能特点

- **自动发现**：通过 Zeroconf (mDNS) 自动扫描局域网内的 Savant 主机。
- **自动同步**：自动获取主机上的场景并创建为 Home Assistant 场景实体。
- **授权验证**：内置激活码验证机制，保障系统安全。
- **实时更新**：每 5 分钟自动同步一次场景列表。

## 📦 安装方法

### 方式一：HACS (推荐)

1. 打开 HACS > Integrations > 右上角菜单 > **Custom repositories**。
2. 添加本仓库 URL，类别选择 **Integration**。
3. 搜索 **SavantHost** 并点击下载。
4. 重启 Home Assistant。

### 方式二：手动安装

1. 下载本仓库代码。
2. 将 `custom_components/savanthost` 文件夹复制到你的 HA 配置目录下的 `custom_components/` 中。
3. 重启 Home Assistant。

## ⚙️ 配置

1. 前往 **设置** > **设备与服务** > **添加集成**。
2. 搜索 **SavantHost**。
3. 输入您的 **激活码**。
4. 系统将自动寻找主机，如果发现多台主机，请从列表中选择。
5. 完成！

## ⚠️ 注意事项

- 本插件需要有效的授权码才能工作。
- 请确保 Home Assistant 与 Savant 主机在同一局域网内，且 mDNS (Multicast) 未被路由器拦截。

## 📄 版权

Copyright © 2024 Rick Yang. All rights reserved.
