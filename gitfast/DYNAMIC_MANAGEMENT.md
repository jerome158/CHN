# 动态管理功能说明

## 功能概述

动态管理功能自动维护预置镜像列表，确保始终使用最新、最可靠的GitHub镜像源。

## 核心规则

### 1. 自动淘汰失效镜像

- **触发条件**: 预置镜像连续3次工作流运行不可用
- **执行动作**: 从预置列表中移除该镜像
- **数据保留**: 仍保留在历史记录中，可被重新评估

### 2. 自动添加优质镜像

- **触发条件**: 新发现的高质量镜像
- **选择标准**:
  - 当前可用
  - 响应速度快
  - 预置列表未满（最多7个）
- **执行动作**: 将新镜像加入预置列表

### 3. 数量限制

- **最大数量**: 预置列表最多7个镜像
- **选择策略**: 优先保留响应最快、最稳定的镜像

## 工作流程

```
1. 工作流触发
   ↓
2. 检测所有镜像（预置 + 发现）
   ↓
3. 更新历史记录
   - 记录可用/不可用状态
   - 计算连续失败次数
   - 统计可用率
   ↓
4. 动态管理
   - 识别连续失败≥3次的预置镜像 → 移除
   - 选择优质的新镜像 → 加入预置
   - 限制总数≤7个
   ↓
5. 保存更新
   - 更新 static_mirrors.json
   - 保留历史记录 mirror_history.json
   ↓
6. 生成页面并部署
```

## 文件说明

### `static_mirrors.json`

存储当前的预置镜像列表。

```json
[
  {
    "name": "镜像名称",
    "url": "https://example.com",
    "type": "static",
    "prefix": "https://example.com/",
    "description": "描述信息",
    "promoted_date": "2024-01-01T00:00:00",
    "source": "promoted"
  }
]
```

### `mirror_history.json`

存储所有镜像的历史记录（用于跟踪和统计）。

```json
{
  "https://example.com/": {
    "name": "镜像名称",
    "prefix": "https://example.com/",
    "url": "https://example.com",
    "first_seen": "2024-01-01T00:00:00",
    "last_checked": "2024-01-15T12:00:00",
    "last_available": "2024-01-15T12:00:00",
    "consecutive_failures": 0,
    "promoted": true,
    "promoted_date": "2024-01-01T00:00:00",
    "status_history": [
      {
        "available": true,
        "timestamp": "2024-01-15T12:00:00"
      }
    ]
  }
}
```

## 配置选项

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `ENABLE_REALTIME_SEARCH` | `true` | 是否启用实时搜索 |
| `ENABLE_DYNAMIC_MANAGEMENT` | `true` | 是否启用动态管理 |

### 脚本配置

在 `gitfast/scripts/mirror_manager.py` 中可以调整：

```python
MAX_STATIC_MIRRORS = 7  # 预置镜像最大数量
MAX_FAILURES = 3         # 连续失败阈值
```

## 使用示例

### 启用动态管理

```bash
# 工作流配置
env:
  ENABLE_DYNAMIC_MANAGEMENT: 'true'

# 本地运行
ENABLE_DYNAMIC_MANAGEMENT=true python scripts/fetch_mirrors.py
```

### 禁用动态管理

```bash
# 工作流配置
env:
  ENABLE_DYNAMIC_MANAGEMENT: 'false'

# 本地运行
ENABLE_DYNAMIC_MANAGEMENT=false python scripts/fetch_mirrors.py
```

### 查看管理摘要

```bash
python gitfast/scripts/mirror_manager.py
```

输出示例：

```
============================================================
镜像管理摘要
============================================================

总计跟踪的镜像: 15
预置镜像数量: 7

镜像统计:
------------------------------------------------------------
✓ GitHub镜像加速 - ghproxy [预置]
  可用率: 95.2%
  连续失败: 0次
  最后检查: 2024-01-15T12:00:00

✓ GitHub镜像加速 - ghproxy.com [预置]
  可用率: 88.9%
  连续失败: 0次
  最后检查: 2024-01-15T12:00:00

✗ 旧镜像 - old.example.com
  可用率: 20.0%
  连续失败: 3次
  最后检查: 2024-01-15T12:00:00
```

## 镜像生命周期

```
1. 发现阶段
   - 通过搜索发现新镜像
   - 记录到 discovered_mirrors.json
   - 首次检测可用性

2. 评估阶段
   - 连续检测可用性
   - 收集响应时间数据
   - 计算稳定性指标

3. 晋升阶段
   - 优质镜像晋升为预置
   - 写入 static_mirrors.json
   - 标记为预置镜像

4. 维护阶段
   - 持续监控可用性
   - 记录历史数据
   - 自动淘汰失效镜像

5. 淘汰阶段
   - 连续3次失败
   - 从预置列表移除
   - 保留历史记录
```

## 手动干预

### 手动添加预置镜像

编辑 `gitfast/static_mirrors.json`：

```json
[
  {
    "name": "我的镜像",
    "url": "https://my-mirror.com",
    "type": "static",
    "prefix": "https://my-mirror.com/",
    "description": "手动添加的镜像"
  }
]
```

### 手动移除预置镜像

编辑 `gitfast/static_mirrors.json`，删除对应条目。

### 重置历史记录

删除 `gitfast/mirror_history.json`，下次运行时会重新创建。

### 恢复默认配置

删除 `gitfast/static_mirrors.json`，会使用默认的预置镜像列表。

## 故障排查

### 镜像被误删除

如果可靠的镜像被误删除，可以：

1. 检查 `mirror_history.json` 确认失败次数
2. 手动添加回 `static_mirrors.json`
3. 下次运行会恢复跟踪

### 新镜像未被添加

检查：
- 新镜像是否可用
- 预置列表是否已满（7个）
- 新镜像是否响应时间过长

### 历史记录丢失

`mirror_history.json` 未提交到Git（在 `.gitignore` 中），重新运行会从头开始记录。

如需保留历史，可以：

1. 手动备份 `mirror_history.json`
2. 提交到私有分支
3. 工作流中恢复历史

## 最佳实践

1. **定期检查**: 每周查看一次管理摘要
2. **关注可用率**: 可用率低于80%的镜像需注意
3. **备份配置**: 定期备份 `static_mirrors.json`
4. **手动干预**: 特殊情况下可以手动调整预置列表
5. **监控日志**: 关注Actions日志中的管理信息

## 相关文件

- `gitfast/scripts/mirror_manager.py` - 管理逻辑
- `gitfast/scripts/fetch_mirrors.py` - 集成管理
- `gitfast/static_mirrors.json` - 预置镜像列表
- `gitfast/mirror_history.json` - 历史记录
- `.github/workflows/update-mirrors.yml` - 工作流配置
