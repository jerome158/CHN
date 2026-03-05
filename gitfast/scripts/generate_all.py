#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键生成所有输出文件
- 生成 HTML 页面
- 生成 gitfast.txt
- 提交所有生成文件到 Git
"""

import os
import sys
import subprocess

# 获取项目根目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def run_command(cmd, cwd=None):
    """运行命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        return False
    print(result.stdout)
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("生成所有输出文件")
    print("=" * 60)

    # 1. 生成镜像数据
    print("\n1. 检测镜像...")
    if not run_command(f"{sys.executable} scripts/fetch_mirrors.py", cwd=PROJECT_ROOT):
        print("镜像检测失败")
        return False

    # 2. 生成 HTML 页面
    print("\n2. 生成 HTML 页面...")
    if not run_command(f"{sys.executable} scripts/generate_pages.py", cwd=PROJECT_ROOT):
        print("页面生成失败")
        return False

    # 3. 检查生成的文件
    print("\n3. 检查生成的文件...")
    files_to_check = [
        os.path.join(PROJECT_ROOT, "mirrors.json"),
        os.path.join(PROJECT_ROOT, "gitfast.txt"),
        os.path.join(PROJECT_ROOT, "docs", "index.html"),
    ]

    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✓ {os.path.relpath(file, PROJECT_ROOT)} ({size} bytes)")
        else:
            print(f"  ✗ {os.path.relpath(file, PROJECT_ROOT)} 不存在")

    # 4. 提交到 Git
    print("\n4. 提交到 Git...")
    print("提示: 你需要手动运行以下命令提交文件：")
    print()
    print("cd gitfast")
    print("git add mirrors.json gitfast.txt docs/")
    print("git commit -m 'Update: 更新镜像数据和页面'")
    print("git push origin main")

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

    print("\n📝 提醒：")
    print("1. mirrors.json - 镜像数据")
    print("2. gitfast.txt - 最快的两个镜像地址")
    print("3. docs/index.html - GitHub Pages 页面")
    print("\n这些文件已生成，请提交到 Git 仓库。")

if __name__ == "__main__":
    main()
