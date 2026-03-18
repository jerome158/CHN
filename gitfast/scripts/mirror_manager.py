#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
镜像源动态管理模块
- 跟踪预置镜像的可用性历史
- 连续3次不可用则剔除
- 新发现的可用镜像可以加入预置列表
- 预置列表最多7个
"""

import json
import os
from datetime import datetime

# 获取项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 历史记录文件
HISTORY_FILE = os.path.join(PROJECT_ROOT, "mirror_history.json")

# 预置镜像历史文件
STATIC_MIRRORS_FILE = os.path.join(PROJECT_ROOT, "static_mirrors.json")

# 配置
MAX_STATIC_MIRRORS = 7
MAX_FAILURES = 3  # 连续失败次数


def load_history():
    """
    加载镜像历史记录
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载历史记录失败: {e}")
    return {}


def save_history(history):
    """
    保存镜像历史记录
    """
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def load_static_mirrors():
    """
    加载预置镜像列表
    """
    if os.path.exists(STATIC_MIRRORS_FILE):
        try:
            with open(STATIC_MIRRORS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载预置镜像失败: {e}")
    return None


def save_static_mirrors(mirrors):
    """
    保存预置镜像列表
    """
    with open(STATIC_MIRRORS_FILE, 'w', encoding='utf-8') as f:
        json.dump(mirrors, f, ensure_ascii=False, indent=2)


def get_mirror_prefix(mirror):
    """
    获取镜像的前缀（用于标识）
    """
    return mirror.get("prefix", mirror.get("url", ""))


def update_mirror_status(mirror, available):
    """
    更新镜像状态到历史记录
    """
    history = load_history()
    prefix = get_mirror_prefix(mirror)
    
    if prefix not in history:
        history[prefix] = {
            "name": mirror.get("name", "Unknown"),
            "prefix": prefix,
            "url": mirror.get("url", prefix),
            "first_seen": datetime.now().isoformat(),
            "status_history": []
        }
    
    # 添加当前状态
    history[prefix]["status_history"].append({
        "available": available,
        "timestamp": datetime.now().isoformat(),
        "last_checked": datetime.now().isoformat()
    })
    
    # 只保留最近20次记录
    if len(history[prefix]["status_history"]) > 20:
        history[prefix]["status_history"] = history[prefix]["status_history"][-20:]
    
    # 更新连续失败次数
    if available:
        history[prefix]["consecutive_failures"] = 0
        history[prefix]["last_available"] = datetime.now().isoformat()
    else:
        history[prefix]["consecutive_failures"] = history[prefix].get("consecutive_failures", 0) + 1
    
    history[prefix]["last_checked"] = datetime.now().isoformat()
    
    save_history(history)
    return history[prefix]


def should_remove_from_static(mirror):
    """
    判断是否应该从预置列表中移除
    连续3次不可用
    """
    prefix = get_mirror_prefix(mirror)
    history = load_history()
    
    if prefix not in history:
        return False
    
    mirror_history = history[prefix]
    consecutive_failures = mirror_history.get("consecutive_failures", 0)
    
    return consecutive_failures >= MAX_FAILURES


def filter_static_mirrors(static_mirrors):
    """
    过滤掉连续多次不可用的预置镜像
    返回：应保留的镜像列表，被移除的镜像列表
    """
    kept_mirrors = []
    removed_mirrors = []
    
    for mirror in static_mirrors:
        if should_remove_from_static(mirror):
            removed_mirrors.append(mirror)
            print(f"  ⚠ 预置镜像已失效: {mirror['name']}")
            print(f"    原因: 连续{MAX_FAILURES}次不可用，已自动移除")
        else:
            kept_mirrors.append(mirror)
    
    return kept_mirrors, removed_mirrors


def select_new_mirrors_for_static(discovered_mirrors, current_static_count, removed_count):
    """
    从新发现的镜像中选择可用的加入预置列表
    
    Args:
        discovered_mirrors: 新发现的镜像列表
        current_static_count: 当前预置镜像数量
        removed_count: 被移除的数量
    
    Returns:
        可以加入预置列表的镜像列表
    """
    # 计算可以添加的数量
    available_slots = MAX_STATIC_MIRRORS - current_static_count + removed_count
    
    if available_slots <= 0:
        return []
    
    # 筛选可用的镜像
    available_mirrors = [m for m in discovered_mirrors if m.get("available", False)]
    
    # 按响应时间排序
    available_mirrors.sort(key=lambda x: x.get("response_time", float('inf')))
    
    # 选择前N个
    selected = available_mirrors[:available_slots]
    
    return selected


def promote_to_static(new_mirrors):
    """
    将新发现的镜像提升为预置镜像
    """
    history = load_history()
    
    promoted_mirrors = []
    for mirror in new_mirrors:
        prefix = get_mirror_prefix(mirror)
        
        # 创建静态格式的镜像配置
        static_mirror = {
            "name": mirror.get("name", f"镜像 - {prefix}"),
            "url": mirror.get("url", prefix),
            "type": "static",
            "prefix": prefix,
            "description": mirror.get("description", "通过发现和验证加入的预置镜像"),
            "promoted_date": datetime.now().isoformat(),
            "source": "promoted"
        }
        
        # 更新历史记录
        if prefix in history:
            history[prefix]["promoted"] = True
            history[prefix]["promoted_date"] = datetime.now().isoformat()
        
        promoted_mirrors.append(static_mirror)
        print(f"  ✓ 新镜像加入预置: {static_mirror['name']}")
    
    save_history(history)
    return promoted_mirrors


def get_mirrors_with_stats():
    """
    获取所有镜像及其统计信息
    """
    history = load_history()
    mirrors_with_stats = []
    
    for prefix, data in history.items():
        # 计算可用率
        status_history = data.get("status_history", [])
        if status_history:
            available_count = sum(1 for s in status_history if s.get("available", False))
            availability_rate = round(available_count / len(status_history) * 100, 1)
        else:
            availability_rate = 0
        
        mirrors_with_stats.append({
            "prefix": prefix,
            "name": data.get("name", "Unknown"),
            "consecutive_failures": data.get("consecutive_failures", 0),
            "availability_rate": availability_rate,
            "last_checked": data.get("last_checked", "Never"),
            "last_available": data.get("last_available", "Never"),
            "promoted": data.get("promoted", False)
        })
    
    return mirrors_with_stats


def update_mirrors_after_check(all_mirrors, detected_mirrors):
    """
    在检测完所有镜像后，更新预置镜像列表
    
    Args:
        all_mirrors: 所有检测过的镜像
        detected_mirrors: 新发现的镜像
    
    Returns:
        更新后的预置镜像列表
    """
    # 1. 加载当前的预置镜像
    current_static = load_static_mirrors()
    if current_static is None:
        # 如果没有预置文件，使用默认的
        from fetch_mirrors import DEFAULT_MIRROR_SOURCES
        current_static = DEFAULT_MIRROR_SOURCES.copy()
    
    # 2. 更新所有镜像的历史状态
    for mirror in all_mirrors:
        update_mirror_status(mirror, mirror.get("available", False))
    
    # 3. 过滤掉连续不可用的预置镜像
    print("\n检查预置镜像状态...")
    kept_mirrors, removed_mirrors = filter_static_mirrors(current_static)
    
    # 4. 选择新发现的可用镜像加入预置
    if removed_mirrors and detected_mirrors:
        print("\n选择新镜像加入预置...")
        available_discovered = [m for m in detected_mirrors if m.get("available", False)]
        new_mirrors = select_new_mirrors_for_static(
            available_discovered,
            len(kept_mirrors),
            len(removed_mirrors)
        )
        
        if new_mirrors:
            promoted_mirrors = promote_to_static(new_mirrors)
            kept_mirrors.extend(promoted_mirrors)
            print(f"\n已将 {len(promoted_mirrors)} 个新镜像加入预置列表")
    
    # 5. 限制预置镜像数量不超过7个
    # 按优先级排序:优先保留新加入的镜像,然后按响应时间排序
    history = load_history()

    def sort_priority(mirror):
        """
        计算镜像的排序优先级
        返回元组: (是否新镜像, 响应时间)
        新镜像优先级最高,响应时间越短优先级越高
        """
        prefix = get_mirror_prefix(mirror)

        # 检查是否是新加入的镜像
        is_promoted = False
        if prefix in history:
            mirror_data = history[prefix]
            # 如果有 promoted_date 且在最近7天内加入,认为是新镜像
            promoted_date = mirror_data.get("promoted_date")
            if promoted_date:
                try:
                    promoted_time = datetime.fromisoformat(promoted_date)
                    days_since_promoted = (datetime.now() - promoted_time).days
                    is_promoted = days_since_promoted < 7
                except:
                    pass

        # 获取响应时间 (越小越好)
        response_time = mirror.get("response_time", float('inf'))

        # 返回排序元组: (不是新镜像(0/1), 响应时间)
        # False(0) < True(1), 所以新镜像(is_promoted=True)会排在前面
        return (not is_promoted, response_time)

    # 按优先级排序
    kept_mirrors.sort(key=sort_priority)

    # 保留前7个
    final_mirrors = kept_mirrors[:MAX_STATIC_MIRRORS]

    # 如果被截断了,打印信息
    if len(kept_mirrors) > MAX_STATIC_MIRRORS:
        removed_extra = kept_mirrors[MAX_STATIC_MIRRORS:]
        print(f"\n  ℹ 超过预置数量限制,移除 {len(removed_extra)} 个优先级较低的镜像:")
        for mirror in removed_extra:
            print(f"    - {mirror['name']}")

    kept_mirrors = final_mirrors
    
    # 6. 保存更新后的预置镜像
    save_static_mirrors(kept_mirrors)
    
    print(f"\n预置镜像更新完成:")
    print(f"  - 当前预置镜像数: {len(kept_mirrors)}")
    print(f"  - 被移除的镜像: {len(removed_mirrors)}")
    
    return kept_mirrors


def get_summary():
    """
    获取镜像管理摘要
    """
    history = load_history()
    static_mirrors = load_static_mirrors()
    
    summary = {
        "total_tracked": len(history),
        "static_count": len(static_mirrors) if static_mirrors else 0,
        "mirrors_with_stats": get_mirrors_with_stats()
    }
    
    return summary


if __name__ == "__main__":
    print("=" * 60)
    print("镜像管理摘要")
    print("=" * 60)
    
    summary = get_summary()
    print(f"\n总计跟踪的镜像: {summary['total_tracked']}")
    print(f"预置镜像数量: {summary['static_count']}")
    
    if summary['mirrors_with_stats']:
        print("\n镜像统计:")
        print("-" * 60)
        for mirror_stat in summary['mirrors_with_stats']:
            status = "✓" if mirror_stat['consecutive_failures'] == 0 else "✗"
            promoted = " [预置]" if mirror_stat['promoted'] else ""
            print(f"{status} {mirror_stat['name']}{promoted}")
            print(f"  可用率: {mirror_stat['availability_rate']}%")
            print(f"  连续失败: {mirror_stat['consecutive_failures']}次")
            print(f"  最后检查: {mirror_stat['last_checked']}")
            print()
