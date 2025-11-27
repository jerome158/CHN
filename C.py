
import re
import os
import sys

def convert_m3u_to_txt(input_file, output_file, max_channels=200):
    """
    将M3U格式转换为简单的"频道名,频道地址"文本格式
    可限制最大频道数量
    """
    print("=== M3U转TXT频道清单转换 ===")
    print(f"输入文件: {input_file}")
    print(f"最大频道数限制: {max_channels}")
    
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
        channel_count = 0
        
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
                    # 检查是否已达到最大频道数量限制
                    if channel_count >= max_channels:
                        print(f"⚠️ 已达到最大频道数量限制 {max_channels}，停止处理")
                        break
                    
                    # 构建"频道名,频道地址"格式
                    output_line = f"{current_name},{line}"
                    output_lines.append(output_line)
                    success_count += 1
                    channel_count += 1
                    print(f"✅ 成功转换 ({channel_count}/{max_channels}): {current_name}")
                    current_name = ""
                else:
                    error_count += 1
                    print(f"❌ 第{line_count}行: 找到URL但没有频道名称")
                    
        print(f"\n=== 转换统计 ===")
        print(f"成功转换频道: {success_count}")
        print(f"转换失败: {error_count}")
        print(f"实际输出频道: {len(output_lines)}")
        
        # 写入输出文件
        if output_lines:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))
            
            print(f"✅ 转换完成！输出文件: {output_file}")
            print(f"📁 文件包含 {len(output_lines)} 个频道")
            return True
        else:
            print("❌ 没有找到有效的频道数据")
            return False
            
    except Exception as e:
        print(f"❌ 转换过程中发生错误: {str(e)}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("使用方法: python m3u_converter.py <输入文件.m3u> <输出文件.txt> [最大频道数]")
        print("示例: python m3u_converter.py playlist.m3u channels.txt 200")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 获取最大频道数参数，默认为200
    max_channels = 200
    if len(sys.argv) > 3:
        try:
            max_channels = int(sys.argv[3])
        except ValueError:
            print("❌ 最大频道数必须是整数，使用默认值200")
    
    # 执行转换
    convert_m3u_to_txt(input_file, output_file, max_channels)

if __name__ == "__main__":
    main()
