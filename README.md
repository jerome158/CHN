# 

访问 https://jerome158.github.io/CHN/

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



