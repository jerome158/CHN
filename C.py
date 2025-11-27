import re
import os
import sys

def debug_m3u_conversion(input_file, output_file):
    """
    调试版本的M3U转换函数，带有详细的日志输出
    """
    print("=== M3U文件转换调试开始 ===")
    print(f"输入文件: {input_file}")
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 错误：文件 {input_file} 不存在")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"文件大小: {len(content)} 字节")
        print(f"文件内容预览:")
        print("-" * 50)
        print(content[:500] + "..." if len(content) > 500 else content)
        print("-" * 50)
        
        lines = content.split('\n')
        print(f"总行数: {len(lines)}")
        
        output = []
        name = ''
        line_count = 0
        extinf_count = 0
        url_count = 0
        
        for line in lines:
            line_count += 1
            line = line.strip()
            
            if not line:
                continue
                
            if line.startswith('#EXTINF:'):
                extinf_count += 1
                print(f"第{line_count}行: 找到#EXTINF标签")
                
                # 尝试多种可能的格式匹配
                matches = [
                    re.search(r'#EXTINF:-?\d+,(.*)', line),
                    re.search(r'#EXTINF:(\d+),(.*)', line),
                    re.search(r'#EXTINF:(.*)', line)
                ]
                
                matched = False
                for i, match in enumerate(matches):
                    if match:
                        if i == 0:
                            name = match.group(1)
                        elif i == 1:
                            name = match.group(2)
                        else:
                            name = match.group(1)
                        
                        name = re.sub(r'[^\w\s\u4e00-\u9fa5\-_]', '', name)
                        name = name.replace('|', '-').strip()
                        print(f"  提取频道名称: {name}")
                        matched = True
                        break
                
                if not matched:
                    print(f"  警告：无法解析#EXTINF行: {line}")
                    
            elif line.startswith('http'):
                url_count += 1
                if name:
                    output.append(f"{name} | {line}")
                    print(f"第{line_count}行: ✅ 成功匹配频道 '{name}'")
                else:
                    print(f"第{line_count}行: ❌ 找到URL但没有频道名称: {line}")
                    
        print(f"\n=== 转换统计 ===")
        print(f"#EXTINF行数: {extinf_count}")
        print(f"URL行数: {url_count}")
        print(f"有效频道: {len(output)}")
        
        # 写入输出文件
        if output:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output))
            print(f"✅ 转换成功！输出文件: {output_file}")
        else:
            print(f"❌ 转换失败：未找到有效频道")
            print("可能的原因:")
            print("1. 文件格式不是标准M3U")
            print("2. 编码问题")
            print("3. 格式差异")
        
        return len(output) > 0
        
    except Exception as e:
        print(f"❌ 转换过程中发生错误: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("用法: python debug_converter.py <输入文件> <输出文件>")
        print("示例: python debug_converter.py mig2.txt channels.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    success = debug_m3u_conversion(input_file, output_file)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
