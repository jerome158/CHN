# 部署指南

## 快速部署到GitHub

### 1. 准备仓库

```bash
# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: GitHub镜像加速地址列表"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/yourusername/gitfast.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 2. 配置GitHub仓库设置

#### 2.1 启用GitHub Actions

1. 进入仓库页面
2. 点击 `Settings` 标签
3. 左侧菜单：`Actions` -> `General`
4. 找到 `Actions permissions` 部分
5. 选择 `Allow all actions and reusable workflows`
6. 点击 `Save`

#### 2.2 配置GitHub Pages

1. 进入仓库页面
2. 点击 `Settings` 标签
3. 左侧菜单选择 `Pages`
4. 在 `Build and deployment` -> `Source` 中选择 `GitHub Actions`
5. 点击 `Save`

### 3. 手动触发首次运行

1. 进入仓库的 `Actions` 标签
2. 选择 `Update GitHub Mirrors` 工作流
3. 点击右侧的 `Run workflow` 按钮
4. 选择 `main` 分支
5. 点击 `Run workflow`

### 4. 访问GitHub Pages

等待工作流完成后（约2-3分钟），访问：

```
https://yourusername.github.io/gitfast/
```

## 本地测试

### 环境准备

```bash
# 安装Python依赖
cd gitfast
pip install -r requirements.txt
```

### 运行脚本

```bash
# 完整检测（包含搜索）
python scripts/fetch_mirrors.py

# 仅生成页面
python scripts/generate_pages.py
```

### 查看结果

```bash
# 查看镜像数据
type mirrors.json

# 查看生成的HTML
start docs\index.html
```

## 工作流说明

### 自动触发

- **每日更新**: 每天北京时间 00:00 (UTC 16:00)
- **每周搜索**: 每周日北京时间 00:00 进行完整网络搜索
- **推送触发**: 推送到 `main` 分支时自动运行

### 手动触发

任何时候都可以在GitHub Actions页面手动触发工作流。

## 故障排查

### Actions无法运行

1. 检查Actions权限设置
2. 确认workflow文件路径正确：`.github/workflows/update-mirrors.yml`
3. 查看Actions日志了解详细错误信息

### Pages无法访问

1. 检查Pages配置中的Source是否为 `GitHub Actions`
2. 确认Actions工作流成功完成
3. 查看Pages部署日志

### 搜索功能不工作

1. 检查环境变量 `ENABLE_REALTIME_SEARCH` 是否为 `true`
2. 查看脚本输出的搜索结果
3. 确认网络连接正常

## 自定义配置

### 修改更新频率

编辑 `.github/workflows/update-mirrors.yml` 中的cron表达式：

```yaml
schedule:
  - cron: '0 16 * * *'  # 每天UTC 16:00运行
```

### 添加新的镜像源

编辑 `gitfast/scripts/fetch_mirrors.py` 中的 `MIRROR_SOURCES` 数组。

### 禁用实时搜索

在工作流中设置环境变量：

```yaml
env:
  ENABLE_REALTIME_SEARCH: 'false'
```

## 维护建议

1. **定期检查**: 每周查看一次GitHub Pages，确认镜像状态正常
2. **更新依赖**: 定期更新Python依赖包
3. **监控日志**: 定期查看Actions日志，及时发现潜在问题
4. **备份配置**: 定期备份配置文件和镜像数据

## 联系支持

如有问题，请：
- 提交Issue到仓库
- 查看现有Issue和讨论
- 查阅项目README文档
