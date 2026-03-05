# 文档索引

欢迎访问 GitHub 镜像加速地址列表项目文档。

## 📚 主要文档

### [README.md](README.md)
项目介绍和快速开始指南，包含：
- 功能特性介绍
- 快速部署步骤
- 使用方法
- 配置说明

### [DEPLOY.md](DEPLOY.md)
详细的部署指南，包含：
- GitHub 仓库设置
- Actions 配置
- Pages 设置
- 本地测试
- 故障排查

### [DYNAMIC_MANAGEMENT.md](DYNAMIC_MANAGEMENT.md)
动态管理功能详细说明，包含：
- 核心规则介绍
- 工作流程
- 配置选项
- 使用示例
- 镜像生命周期
- 故障排查

### [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
使用示例和场景，包含：
- 快速使用方法
- 全局配置镜像
- 验证镜像速度
- 批量操作示例
- 常见场景处理
- 高级技巧

### [FEATURES_SUMMARY.md](FEATURES_SUMMARY.md)
功能更新总结，包含：
- 最快镜像推荐功能
- 新增功能列表
- 文件变更说明
- 配置参数
- 快速开始
- 完整功能列表

## 📁 项目文件说明

### 核心脚本

- **`scripts/fetch_mirrors.py`** - 镜像检测主脚本
- **`scripts/search_mirrors.py`** - 实时搜索脚本
- **`scripts/mirror_manager.py`** - 动态管理脚本
- **`scripts/generate_pages.py`** - HTML 页面生成脚本

### 配置文件

- **`config.json`** - 项目配置文件
- **`static_mirrors.json`** - 预置镜像列表（动态更新）
- **`mirrors.json`** - 镜像检测数据（自动生成）

### 数据文件

- **`mirror_history.json`** - 镜像历史记录（本地，不提交到 Git）
- **`discovered_mirrors.json`** - 搜索发现的镜像（临时）

### 工作流

- **`.github/workflows/update-mirrors.yml`** - GitHub Actions 工作流配置

## 🚀 快速导航

### 想要...

1. **快速开始使用**
   - 阅读 [README.md](README.md)

2. **部署到 GitHub**
   - 阅读 [DEPLOY.md](DEPLOY.md)

3. **了解动态管理**
   - 阅读 [DYNAMIC_MANAGEMENT.md](DYNAMIC_MANAGEMENT.md)

4. **查看功能更新**
   - 阅读 [FEATURES_SUMMARY.md](FEATURES_SUMMARY.md)

5. **本地开发测试**
   - 阅读 [README.md#本地开发](README.md#本地开发)

6. **自定义配置**
   - 阅读 [README.md#自定义配置](README.md#自定义配置)

## 📖 文档阅读顺序

### 新手入门
1. [README.md](README.md) - 了解项目
2. [DEPLOY.md](DEPLOY.md) - 部署项目
3. [README.md](README.md) - 使用项目

### 高级使用
1. [DYNAMIC_MANAGEMENT.md](DYNAMIC_MANAGEMENT.md) - 理解动态管理
2. [README.md](README.md#自定义配置) - 自定义配置
3. [FEATURES_SUMMARY.md](FEATURES_SUMMARY.md) - 了解完整功能

### 开发者
1. [README.md#本地开发](README.md#本地开发) - 设置开发环境
2. [DEPLOY.md#本地测试](DEPLOY.md#本地测试) - 测试脚本
3. [DYNAMIC_MANAGEMENT.md#手动干预](DYNAMIC_MANAGEMENT.md#手动干预) - 手动管理

## 🔍 常见问题

### 项目文档

- **这是什么项目？**
  → 阅读 [README.md](README.md)

- **如何部署？**
  → 阅读 [DEPLOY.md](DEPLOY.md)

- **动态管理是什么？**
  → 阅读 [DYNAMIC_MANAGEMENT.md](DYNAMIC_MANAGEMENT.md)

- **有哪些功能？**
  → 阅读 [FEATURES_SUMMARY.md](FEATURES_SUMMARY.md)

### 功能使用

- **如何启用/禁用功能？**
  → 阅读 [README.md#控制实时搜索功能](README.md#控制实时搜索功能)
  → 阅读 [README.md#控制动态管理功能](README.md#控制动态管理功能)

- **如何自定义镜像？**
  → 阅读 [README.md#修改镜像源列表](README.md#修改镜像源列表)
  → 阅读 [DYNAMIC_MANAGEMENT.md#手动干预](DYNAMIC_MANAGEMENT.md#手动干预)

- **如何修改更新频率？**
  → 阅读 [README.md#修改更新频率](README.md#修改更新频率)

### 故障排查

- **Actions 无法运行？**
  → 阅读 [DEPLOY.md#故障排查](DEPLOY.md#故障排查)

- **Pages 无法访问？**
  → 阅读 [DEPLOY.md#故障排查](DEPLOY.md#故障排查)

- **搜索功能不工作？**
  → 阅读 [DEPLOY.md#故障排查](DEPLOY.md#故障排查)

- **镜像被误删除？**
  → 阅读 [DYNAMIC_MANAGEMENT.md#故障排查](DYNAMIC_MANAGEMENT.md#故障排查)

## 📞 获取帮助

### 文档内
- 查看各文档的"故障排查"章节
- 检查文档中的"常见问题"部分

### 项目相关
- 提交 Issue 到 GitHub 仓库
- 查看 Actions 日志
- 检查仓库的 Issues 页面

### 联系方式
- 在 GitHub 提交 Issue
- 查看 README 中的联系方式

## 🎯 文档维护

文档随项目更新，建议：
- 定期查看最新文档
- 关注功能更新说明
- 参考故障排查指南

---

💡 **提示**: 建议从 [README.md](README.md) 开始阅读，然后根据需要深入其他文档。
