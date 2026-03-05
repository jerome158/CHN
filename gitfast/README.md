# GitHub镜像加速地址列表

自动收集和检测GitHub镜像加速地址的GitHub Actions工作流项目。

## ✨ 功能特性

- 🔍 **智能搜索**: 实时从网络搜索最新的GitHub镜像地址
- ✅ **自动检测**: 自动检测多个GitHub镜像地址的可用性
- 🤖 **动态管理**: 自动淘汰失效镜像，自动添加新镜像到预置列表
- ⚡ **最快推荐**: 自动保存测速最快的前两个镜像到 `gitfast.txt`
- 📊 **状态监控**: 显示每个镜像的响应时间和可用状态
- 🌐 **GitHub Pages**: 提供美观的网页界面展示
- 📋 **一键复制**: 方便用户快速复制镜像地址
- 🔐 **安全过滤**: 自动过滤不安全和无效的镜像源

## 🚀 快速开始

### 1. Fork此仓库

点击右上角的Fork按钮，将此仓库复制到你的GitHub账号下。

### 2. 启用GitHub Actions

1. 进入你fork的仓库
2. 点击 `Settings` 标签
3. 在左侧菜单中选择 `Actions` -> `General`
4. 在 `Actions permissions` 部分，选择 `Allow all actions and reusable workflows`
5. 点击 `Save`

### 3. 启用GitHub Pages

1. 进入仓库的 `Settings` 页面
2. 在左侧菜单中选择 `Pages`
3. 在 `Build and deployment` -> `Source` 中选择 `GitHub Actions`
4. 点击 `Save`

### 4. 手动触发工作流（可选）

如果你不想等待定时任务，可以手动触发工作流：

1. 进入仓库的 `Actions` 标签
2. 选择 `Update GitHub Mirrors` 工作流
3. 点击右侧的 `Run workflow` 按钮
4. 选择分支并点击 `Run workflow`

## 📁 项目结构

```
.
├── .github/
│   └── workflows/
│       └── update-mirrors.yml    # GitHub Actions工作流配置
├── gitfast/                      # 项目主目录
│   ├── scripts/                  # 脚本目录
│   │   ├── fetch_mirrors.py      # 镜像地址检测和搜索脚本
│   │   ├── search_mirrors.py      # 实时网络搜索脚本
│   │   └── generate_pages.py      # HTML页面生成脚本
│   ├── docs/                     # GitHub Pages生成的HTML文件
│   ├── config.json               # 配置文件
│   ├── mirrors.json              # 镜像数据（自动生成）
│   └── README.md                 # 项目说明文档
└── README.md                     # 项目根README
```

## 🔧 工作原理

1. **实时搜索** (`search_mirrors.py`):
   - 从GitHub API搜索相关仓库
   - 从技术博客和社区论坛获取镜像信息
   - 使用正则表达式提取潜在镜像地址
   - 自动过滤不安全和无效的URL

2. **镜像检测** (`fetch_mirrors.py`):
   - 整合预置和搜索发现的镜像源
   - 对每个镜像进行可用性检测
   - 记录响应时间和状态码
   - 按可用性和响应时间排序

3. **动态管理** (`mirror_manager.py`):
   - 跟踪每个镜像的可用性历史
   - 连续3次不可用则从预置列表移除
   - 将新发现的高质量镜像加入预置
   - 保持预置列表最多7个

4. **页面生成** (`generate_pages.py`):
   - 读取检测到的镜像数据
   - 生成美观的HTML页面
   - 包含复制功能和使用说明

5. **定时更新** (`.github/workflows/update-mirrors.yml`):
   - 每天北京时间 00:00 (UTC 16:00) 自动运行
   - 每周日进行完整的网络搜索
   - 支持手动触发
   - 自动部署到GitHub Pages

## 📊 支持的镜像源

项目当前监控以下镜像源：

- `https://mirror.ghproxy.com/` - ghproxy镜像
- `https://ghproxy.com/` - ghproxy.com镜像
- `https://gitclone.com/github.com/` - GitClone镜像
- `https://gh.api.99988866.xyz/` - moeyy镜像
- `https://ghproxy.net/` - GitProxy镜像
- `https://hub.fastgit.xyz/` - FastGit镜像

以及通过实时搜索发现的新镜像源。

## 💡 使用方法

### 使用最快的镜像（推荐）

项目会自动生成 `gitfast.txt` 文件，包含测速最快的前两个镜像地址：

```bash
# 查看最快的镜像
cat gitfast/gitfast.txt

# 使用第一个（最快的）镜像
git clone $(head -1 gitfast/gitfast.txt)user/repo.git
```

### Git Clone

```bash
# 原始地址
git clone https://github.com/user/repo.git

# 使用镜像地址（以mirror.ghproxy.com为例）
git clone https://mirror.ghproxy.com/user/repo.git

# 使用最快的镜像
git clone $(head -1 gitfast/gitfast.txt)user/repo.git
```

### Git Push

```bash
# 添加远程地址（使用镜像）
git remote add origin https://mirror.ghproxy.com/user/repo.git

# 推送代码
git push origin main
```

### 配置 Git 使用镜像

将以下内容添加到 `~/.gitconfig`（Windows: `C:\Users\你的用户名\.gitconfig`）：

```ini
[url "https://mirror.ghproxy.com/"]
    insteadOf = https://github.com/
```

或者使用最快的镜像：

```bash
# 从 gitfast.txt 读取第一个镜像并配置
FASTEST=$(head -1 gitfast/gitfast.txt)
git config --global url."$FASTEST".insteadOf https://github.com/
```

## ⚙️ 自定义配置

### 修改镜像源列表

编辑 `gitfast/scripts/fetch_mirrors.py` 文件中的 `MIRROR_SOURCES` 数组：

```python
MIRROR_SOURCES = [
    {
        "name": "镜像名称",
        "url": "镜像主页",
        "type": "static",
        "prefix": "镜像前缀"
    },
    # 添加更多镜像源...
]
```

### 修改更新频率

编辑 `.github/workflows/update-mirrors.yml` 文件中的 `cron` 表达式：

```yaml
schedule:
  - cron: '0 16 * * *'  # 每天UTC 16:00（北京时间00:00）运行
```

### 控制实时搜索功能

通过环境变量控制是否启用实时搜索：

```yaml
# 在工作流中
env:
  ENABLE_REALTIME_SEARCH: 'true'  # 或 'false'
```

### 控制动态管理功能

动态管理功能会自动：
- 移除连续3次不可用的预置镜像
- 将可用的新镜像加入预置列表
- 保持预置列表最多7个

通过环境变量控制是否启用：

```yaml
# 在工作流中
env:
  ENABLE_DYNAMIC_MANAGEMENT: 'true'  # 或 'false'
```

本地运行时：

```bash
# 启用动态管理
ENABLE_DYNAMIC_MANAGEMENT=true python scripts/fetch_mirrors.py

# 禁用动态管理
ENABLE_DYNAMIC_MANAGEMENT=false python scripts/fetch_mirrors.py
```

### 查看镜像管理摘要

```bash
python gitfast/scripts/mirror_manager.py
```

这将显示所有跟踪镜像的统计信息，包括：
- 可用率
- 连续失败次数
- 最后检查时间
- 是否为预置镜像

或在 `gitfast/config.json` 中配置：

```json
{
  "search": {
    "enabled": true,
    "sources": ["github_api", "tech_blogs"],
    "max_results": 50
  }
}
```

## 🛠️ 本地开发

### 环境要求

- Python 3.11+
- 依赖包：`requests`, `beautifulsoup4`, `lxml`

### 安装依赖

```bash
cd gitfast
pip install -r requirements.txt
```

### 运行脚本

```bash
# 检测镜像（启用搜索）
ENABLE_REALTIME_SEARCH=true python scripts/fetch_mirrors.py

# 检测镜像（禁用搜索）
ENABLE_REALTIME_SEARCH=false python scripts/fetch_mirrors.py

# 单独运行搜索
python scripts/search_mirrors.py

# 生成HTML页面
python scripts/generate_pages.py
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

### 添加新的镜像源

1. Fork仓库
2. 编辑 `gitfast/scripts/fetch_mirrors.py` 添加新镜像源
3. 提交Pull Request

## 📝 许可证

MIT License

## 🔗 相关链接

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [GitHub Pages文档](https://docs.github.com/en/pages)
- [项目页面](https://yourusername.github.io/gitfast/)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
