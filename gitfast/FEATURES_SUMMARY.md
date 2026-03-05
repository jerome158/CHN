# 功能更新总结

## 新增：最快镜像推荐

### 功能说明

自动将测速最快的前两个镜像地址保存到 `gitfast/gitfast.txt` 文件，每行一个镜像前缀。

### 使用方法

```bash
# 查看最快的镜像
cat gitfast/gitfast.txt

# 使用第一个（最快的）镜像
git clone $(head -1 gitfast/gitfast.txt)user/repo.git
```

### 输出格式

`gitfast.txt` 文件内容示例：

```
https://mirror.ghproxy.com/
https://ghproxy.com/
```

### 特点

- 只包含可用的镜像
- 按响应时间排序
- 每行一个前缀
- 自动更新（每次检测后）
- 不会提交到 Git（在 `.gitignore` 中）

---

## 新增：动态管理功能

### 核心规则

1. **自动淘汰失效镜像**
   - 预置镜像连续3次工作流运行不可用时自动剔除
   - 保留历史记录用于跟踪和评估

2. **自动添加优质镜像**
   - 新发现的高质量镜像可自动加入预置列表
   - 按响应时间和可用性排序选择

3. **数量限制**
   - 预置列表最多保持7个镜像
   - 优先保留最稳定、最快的镜像

### 新增文件

#### `gitfast/scripts/mirror_manager.py`
镜像动态管理模块，提供以下功能：
- 镜像历史记录跟踪
- 连续失败次数统计
- 可用率计算
- 自动淘汰和晋升机制

#### `gitfast/static_mirrors.json`
存储当前的预置镜像列表（动态更新）

#### `gitfast/mirror_history.json`
存储所有镜像的详细历史记录（本地，不提交到Git）

### 更新的文件

#### `gitfast/scripts/fetch_mirrors.py`
- 集成动态管理功能
- 支持从 `static_mirrors.json` 加载预置镜像
- 添加环境变量 `ENABLE_DYNAMIC_MANAGEMENT` 控制开关
- 更新输出信息，显示动态管理状态

#### `.github/workflows/update-mirrors.yml`
- 添加 `ENABLE_DYNAMIC_MANAGEMENT: 'true'` 环境变量
- 默认启用动态管理

#### `gitfast/.gitignore`
- 添加 `mirror_history.json` 到忽略列表

#### 文档文件
- `gitfast/README.md` - 更新功能说明
- `DYNAMIC_MANAGEMENT.md` - 详细的功能文档

### 使用方法

#### 启用动态管理

```yaml
# 工作流配置
env:
  ENABLE_REALTIME_SEARCH: 'true'
  ENABLE_DYNAMIC_MANAGEMENT: 'true'
```

#### 本地运行

```bash
# 启用动态管理
ENABLE_DYNAMIC_MANAGEMENT=true python gitfast/scripts/fetch_mirrors.py

# 禁用动态管理
ENABLE_DYNAMIC_MANAGEMENT=false python gitfast/scripts/fetch_mirrors.py
```

#### 查看管理摘要

```bash
python gitfast/scripts/mirror_manager.py
```

### 工作流程

```
1. 加载预置镜像（static_mirrors.json 或默认）
   ↓
2. 加载发现的镜像
   ↓
3. 检测所有镜像的可用性
   ↓
4. 更新历史记录
   ↓
5. 动态管理（如果启用）
   - 移除连续3次失败的预置镜像
   - 选择优质的新镜像加入预置
   - 限制总数≤7个
   ↓
6. 保存更新后的配置
   ↓
7. 生成页面并部署
```

### 镜像状态标识

- ⭐ 预置镜像（通过动态管理或手动配置）
- 🔍 发现镜像（通过实时搜索发现）

### 数据文件说明

#### `static_mirrors.json`
- 存储当前预置镜像列表
- 提交到Git，可手动编辑
- 动态管理会自动更新此文件

#### `mirror_history.json`
- 存储所有镜像的详细历史
- 本地文件，不提交到Git
- 包含：可用率、连续失败次数、最后检查时间等

### 配置参数

在 `gitfast/scripts/mirror_manager.py` 中可调整：

```python
MAX_STATIC_MIRRORS = 7  # 预置镜像最大数量
MAX_FAILURES = 3         # 连续失败阈值
```

### 优势

1. **自动化**: 无需手动维护预置列表
2. **智能**: 基于实际使用数据决策
3. **可靠**: 淘汰失效镜像，添加优质镜像
4. **灵活**: 可随时禁用或手动干预
5. **透明**: 提供完整的历史记录和统计信息

### 注意事项

1. `mirror_history.json` 本地文件，丢失后需要重新积累数据
2. 动态管理建议与实时搜索配合使用
3. 可以通过环境变量随时禁用功能
4. 支持手动编辑 `static_mirrors.json`

### 文档

- `DYNAMIC_MANAGEMENT.md` - 完整的功能文档
- `gitfast/README.md` - 项目使用说明
- `DEPLOY.md` - 部署指南

## 完整功能列表

### 核心功能
- ✅ 实时搜索 GitHub 镜像源
- ✅ 自动检测镜像可用性
- ✅ 动态管理预置镜像列表
- ✅ 生成美观的展示页面
- ✅ GitHub Actions 定时更新
- ✅ 一键复制镜像地址

### 管理功能
- ✅ 自动淘汰失效镜像（连续3次失败）
- ✅ 自动添加优质镜像（最多7个）
- ✅ 历史记录跟踪
- ✅ 可用率统计
- ✅ 响应时间监控

### 配置选项
- ✅ 环境变量控制功能开关
- ✅ 灵活的配置文件
- ✅ 手动干预支持
- ✅ 跨平台兼容

## 快速开始

```bash
# 1. 克隆或 fork 仓库
git clone https://github.com/yourusername/gitfast.git

# 2. 安装依赖
cd gitfast
pip install -r requirements.txt

# 3. 运行检测
ENABLE_DYNAMIC_MANAGEMENT=true python scripts/fetch_mirrors.py

# 4. 生成页面
python scripts/generate_pages.py

# 5. 查看结果
start docs\index.html
```

## 部署到GitHub

参考 `DEPLOY.md` 文档完成以下步骤：

1. Fork 仓库
2. 启用 GitHub Actions
3. 配置 GitHub Pages
4. 手动触发首次运行
5. 访问生成的页面

## 联系与支持

如有问题或建议，请：
- 提交 Issue
- 查阅文档
- 检查 Actions 日志
