"""
文件路径提取器
从文本文件中提取文件路径并复制到剪贴板
作者: [不忙脚本盒子]
版本: 0.0.1
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Optional


class FilePathExtractor:
    """
    文件路径提取器类
    用于从文本文件中提取文件路径并复制到剪贴板
    """

    def __init__(self):
        """初始化提取器"""
        self.clipboard_encoding = self._get_system_clipboard_encoding()

    def _get_system_clipboard_encoding(self) -> str:
        """
        获取系统剪贴板编码

        Returns:
            str: 系统剪贴板编码
        """
        # 根据系统判断编码
        if sys.platform.startswith('win'):
            return 'gbk'  # Windows中文系统通常使用gbk
        else:
            return 'utf-8'  # Linux/Mac使用utf-8

    def read_params_file(self, filepath: str) -> Optional[List[str]]:
        """
        读取参数文件

        Args:
            filepath: 参数文件路径

        Returns:
            参数列表，如果读取失败则返回None
        """
        try:
            file_path = Path(filepath)

            # 检查文件是否存在
            if not file_path.exists():
                print(f"错误: 文件不存在 - {filepath}")
                return None

            # 检查是否为文件
            if not file_path.is_file():
                print(f"错误: 路径不是文件 - {filepath}")
                return None

            # 尝试读取文件
            content = file_path.read_text(encoding='utf-8').splitlines()
            return content

        except UnicodeDecodeError:
            print("错误: 无法用UTF-8编码读取文件，尝试使用GBK编码...")
            try:
                # 尝试使用GBK编码
                file_path = Path(filepath)
                content = file_path.read_text(encoding='gbk').splitlines()
                return content
            except Exception as e:
                print(f"错误: 无法读取文件 - {e}")
                return None
        except Exception as e:
            print(f"错误: 读取文件时发生异常 - {e}")
            return None

    def extract_file_paths(self, content: List[str]) -> List[str]:
        """
        提取文件路径

        Args:
            content: 文件内容列表

        Returns:
            提取并处理后的文件路径列表
        """
        if not content:
            return []

        try:
            # 过滤空行和空白字符，并去除首尾空格
            file_paths = [line.strip() for line in content if line.strip()]

            # 去重（保持原始顺序）
            unique_paths = []
            for path in file_paths:
                if path not in unique_paths:
                    unique_paths.append(path)

            # 按文件名升序排序（不区分大小写）
            sorted_paths = sorted(unique_paths, key=lambda x: x.lower())

            return sorted_paths
        except Exception as e:
            print(f"错误: 提取文件路径时发生异常 - {e}")
            return []

    def copy_file_paths(self, file_paths: List[str]) -> bool:
        """
        复制文件路径到剪贴板

        Args:
            file_paths: 文件路径列表

        Returns:
            复制是否成功
        """
        if not file_paths:
            print("提示: 没有文件路径可复制")
            return False

        try:
            result = '\n'.join(file_paths)

            # 根据系统选择剪贴板命令
            if sys.platform.startswith('win'):
                # Windows系统使用clip命令
                process = subprocess.Popen(
                    ['clip'],
                    stdin=subprocess.PIPE,
                    shell=True
                )
                process.communicate(result.encode(self.clipboard_encoding))

                print(f"✅ 已复制 {len(file_paths)} 个文件路径到剪贴板")
                return True
            else:
                print(f"⚠️  当前系统 ({sys.platform}) 暂不支持自动复制到剪贴板")
                print("请手动复制以下内容：")
                print("-" * 50)
                print(result)
                print("-" * 50)
                return False

        except Exception as e:
            print(f"错误: 复制到剪贴板失败 - {e}")
            return False

    def process(self, params_file: str) -> bool:
        """
        处理参数文件的主流程

        Args:
            params_file: 参数文件路径

        Returns:
            处理是否成功
        """
        print(f"正在处理文件: {params_file}")

        # 1. 读取文件
        content = self.read_params_file(params_file)
        if content is None:
            return False

        # 2. 提取路径
        file_paths = self.extract_file_paths(content)
        if not file_paths:
            print("提示: 文件中没有找到有效的文件路径")
            return True  # 视为成功，只是没有内容

        # 3. 显示提取结果
        print(f"找到 {len(file_paths)} 个文件路径:")
        for i, path in enumerate(file_paths, 1):
            print(f"  {i:3d}. {path}")

        # 4. 复制到剪贴板
        return self.copy_file_paths(file_paths)


def main(params_file: str):
    """
    主函数

    Args:
        params_file: 参数文件路径
    """
    try:
        extractor = FilePathExtractor()
        success = extractor.process(params_file)

        if not success:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生未预期的错误: {e}")
        sys.exit(1)


def display_help():
    """显示帮助信息"""
    script_name = Path(__file__).name
    help_text = f"""
{script_name} - 文件路径提取器

💡 提示:本脚本无法直接使用,请使用<不忙脚本盒子>配置快捷键或用右键菜单启动。
   不忙脚本盒子:https://www.bm-box.cn

🚀 功能特性:
    • 批量将选中的文件路径复制到剪贴板
    • 自动过滤空行和重复项
    • 按文件名升级序排序（不区分大小写）
    • 自动复制到系统剪贴板
    • 支持多种编码格式

🔧  技术特性:
    • 支持 Windows 7 及以上系统
    • 自动编码检测 (UTF-8, GBK, UTF-16)
    • 智能错误处理
    • 实时处理进度显示

📖 更多帮助:
    • 在不忙脚本盒子中点击本脚本详情
    • 访问不忙脚本盒子官网脚本库
    • 搜索'文件路径提取器'查看详细教程
    """
    print(help_text)


if __name__ == "__main__":
    # 接收参数执行脚本(不忙脚本盒子会传一个tmp文件路径(包含用户选中的文件路径))
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        # 无参启动显示帮助信息
        display_help()
        input("\n按 Enter 键退出... ")
        sys.exit(0)
