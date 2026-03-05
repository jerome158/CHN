# GitHub Pages 设置指南

## 问题解决

### 问题1: GitHub Pages 返回404

**原因**: HTML 文件没有正确生成或提交到仓库

**解决方法**:

#### 步骤1: 确认文件存在

检查以下文件是否存在：

```bash
# 在 gitfast 目录下
ls -l gitfast/docs/index.html  # HTML页面
ls -l gitfast/mirrors.json     # 镜像数据
ls -l gitfast/gitfast.txt      # 最快的镜像
```

#### 步骤2: 提交所有文件到仓库

```bash
cd gitfast

# 添加所有生成的文件
git add mirrors.json gitfast.txt docs/

# 提交
git commit -m "feat: 添加GitHub Pages和镜像数据文件"

# 推送到远程
git push origin main
```

#### 步骤3: 配置 GitHub Pages

1. 进入仓库页面
2. 点击 `Settings` 标签
3. 左侧菜单选择 `Pages`
4. 在 `Build and deployment` 中：
   - **Source**: 选择 `Deploy from a branch`
   - **Branch**: 选择 `main` 分支
   - **Folder**: 选择 `/(root)` 或 `/docs`（根据你的设置）

5. 点击 `Save`

#### 步骤4: 使用 GitHub Actions 部署（推荐）

如果使用 GitHub Actions 部署：

1. 确保 `.github/workflows/update-mirrors.yml` 存在
2. 工作流会自动生成 `gitfast/docs/index.html`
3. 自动部署到 GitHub Pages

配置 `.github/workflows/update-mirrors.yml`:

```yaml
name: Update GitHub Mirrors

on:
  schedule:
    - cron: '0 16 * * *'  # 每天UTC 16:00运行
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  update-mirrors:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4 lxml

      - name: Run mirror fetcher
        run: |
          python gitfast/scripts/fetch_mirrors.py
        env:
          ENABLE_REALTIME_SEARCH: 'true'
          ENABLE_DYNAMIC_MANAGEMENT: 'true'

      - name: Generate GitHub Pages
        run: |
          python gitfast/scripts/generate_pages.py

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./gitfast/docs
```

### 问题2: 输出文件没有提交到仓库

**原因**:
1. 文件在 `.gitignore` 中被忽略了
2. 文件没有使用 `git add` 添加
3. GitHub Actions 生成的文件没有提交

**解决方法**:

#### 方法1: 手动提交（推荐用于初始化）

```bash
cd gitfast

# 生成文件
python scripts/fetch_mirrors.py
python scripts/generate_pages.py

# 添加文件（确保 .gitignore 没有忽略这些文件）
git add mirrors.json gitfast.txt docs/
git status  # 确认文件被添加

# 提交
git commit -m "feat: 添加初始镜像数据和页面"
git push origin main
```

#### 方法2: 使用 GitHub Actions 自动提交

在 `.github/workflows/update-mirrors.yml` 中添加自动提交步骤：

```yaml
- name: Commit and push changes
  run: |
    git config user.name "GitHub Actions"
    git config user.email "actions@github.com"
    git add gitfast/mirrors.json gitfast/gitfast.txt gitfast/docs/
    git diff --staged --quiet || git commit -m "chore: 更新镜像数据 [skip ci]"
    git push origin main
```

#### 方法3: 创建静态文件提交一次

```bash
# 创建初始文件
cd gitfast

# 确保这些文件已生成
ls -l mirrors.json gitfast.txt docs/index.html

# 提交到仓库
git add mirrors.json gitfast.txt docs/
git commit -m "feat: 添加静态文件"
git push origin main
```

## 目录结构说明

正确的目录结构应该是：

```
your-repo/
├── .github/
│   └── workflows/
│       └── update-mirrors.yml
├── gitfast/
│   ├── docs/
│   │   └── index.html          # GitHub Pages 页面
│   ├── scripts/
│   │   ├── fetch_mirrors.py
│   │   ├── generate_pages.py
│   │   └── ...
│   ├── mirrors.json            # 镜像数据
│   ├── gitfast.txt             # 最快的镜像
│   └── README.md
└── README.md
```

## GitHub Pages 访问地址

根据你的仓库配置，访问地址可能是：

1. **使用 `/(root)` 目录**:
   ```
   https://yourusername.github.io/your-repo/
   ```

2. **使用 `/docs` 目录**:
   ```
   https://yourusername.github.io/your-repo/docs/
   ```

3. **使用 `/gitfast/docs` 目录**（如果这样配置）:
   ```
   https://yourusername.github.io/your-repo/gitfast/docs/
   ```

## 验证步骤

### 1. 检查文件是否在仓库中

```bash
# 在仓库根目录
git ls-files | grep -E "(mirrors.json|gitfast.txt|docs/index.html)"
```

### 2. 检查 GitHub Pages 设置

1. 进入仓库 `Settings` -> `Pages`
2. 确认 `Source` 和 `Branch` 配置正确
3. 查看 `Deployments` 标签，确认部署状态

### 3. 查看部署日志

1. 进入仓库 `Actions` 标签
2. 查看最近的 workflow 运行
3. 检查 "Deploy to GitHub Pages" 步骤的日志

## 常见问题

### Q1: 文件生成了但页面还是404

**A**:
1. 确认文件已提交并推送到仓库
2. 检查 GitHub Pages 的 Source 设置
3. 等待几分钟让 GitHub Pages 重新部署
4. 清除浏览器缓存

### Q2: Actions 生成的文件没有提交

**A**:
1. 检查 `.gitignore` 是否忽略了这些文件
2. 确认 Actions 有 `contents: write` 权限
3. 添加自动提交步骤到 workflow

### Q3: 页面显示了但数据是旧的

**A**:
1. 检查 Actions 是否正常运行
2. 查看最近的 workflow 日志
3. 手动触发 workflow 更新

### Q4: 找不到 docs 目录

**A**:
1. 运行 `python scripts/generate_pages.py` 生成页面
2. 或者手动创建 `docs` 目录并添加 `index.html`

## 快速修复命令

```bash
# 一键修复
cd gitfast

# 1. 生成所有文件
python scripts/fetch_mirrors.py
python scripts/generate_pages.py

# 2. 检查文件
ls -l mirrors.json gitfast.txt docs/index.html

# 3. 提交到仓库
git add mirrors.json gitfast.txt docs/
git commit -m "feat: 更新GitHub Pages和镜像数据"
git push origin main

# 4. 等待 GitHub Pages 部署完成（约1-2分钟）
# 访问: https://yourusername.github.io/your-repo/
```

## 联系支持

如果问题仍然存在，请：

1. 查看 Actions 日志了解详细错误
2. 提交 Issue 到仓库
3. 检查 GitHub Pages 的 Deployments 日志
