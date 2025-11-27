
import re
import os
import sys

def convert_m3u_to_txt(input_file, output_file):
    """
    将M3U格式转换为简单的"频道名,频道地址"文本格式
    """
    print("=== M3U转TXT频道清单转换 ===")
    print(f"输入文件: {input_file}")
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 错误：文件 {input_file} 不存在")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"文件大小: {len(content)} 字节")
        
        lines = content.split('\n')
        print(f"总行数: {len(lines)}")
        
        output_lines = []
        current_name = ""
        line_count = 0
        success_count = 0
        error_count = 0
        
        for line in lines:
            line_count += 1
            line = line.strip()
            
            if not line:
                continue
                
            if line.startswith('#EXTINF:'):
                # 提取频道名称
                name_match = re.search(r',\s*(.*)$', line)
                if name_match:
                    current_name = name_match.group(1).strip()
                    print(f"第{line_count}行: 找到频道名称 '{current_name}'")
                    
            elif line.startswith('http'):
                if current_name:
                    # 构建"频道名,频道地址"格式
                    output_line = f"{current_name},{line}"
                    output_lines.append(output_line)
                    success_count += 1
                    print(f"✅ 成功转换: {current_name}")
                    current_name = ""
                else:
                    error_count += 1
                    print(f"❌ 第{line_count}行: 找到URL但没有频道名称")
                    
        print(f"\n=== 转换统计 ===")
        print(f"成功转换频道: {success_count}")
        print(f"转换失败: {error_count}")
        
        # 写入输出文件
        if output_lines:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))
            print(f"✅ 转换完成！输出文件: {output_file}")
            print(f"📋 输出格式: 频道名称,URL地址")
            return True
        else:
            print(f"❌ 转换失败：未找到有效频道数据")
            return False
        
    except Exception as e:
        print(f"❌ 转换过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) != 3:
        print("用法: python m3u_converter.py <输入文件.m3u> <输出文件.txt>")
        print("示例: python m3u_converter.py playlist.m3u channels.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    success = convert_m3u_to_txt(input_file, output_file)
    
    if success:
        print(f"\n🎉 转换成功！")
        print(f"📁 输入: {input_file}")
        print(f"📁 输出: {output_file}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

