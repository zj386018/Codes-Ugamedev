#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神秘森林文字冒险游戏 - 简化版启动脚本
完全避免ttk主题问题，使用纯tkinter实现
"""

import sys
import os

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    return True

def check_dependencies():
    """检查依赖库"""
    required_modules = ['tkinter']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"错误: 缺少必要的依赖库: {', '.join(missing_modules)}")
        return False
    
    return True

def main():
    """主函数"""
    print("神秘森林文字冒险游戏 - 简化版")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        input("按回车键退出...")
        return
    
    # 检查依赖库
    if not check_dependencies():
        input("按回车键退出...")
        return
    
    try:
        # 导入简化版游戏GUI
        from game_gui_simple import GameGUI
        
        print("正在启动游戏...")
        print("游戏窗口将在新窗口中打开")
        print("如果游戏窗口没有出现，请检查是否有错误提示")
        print("=" * 50)
        
        # 创建并运行游戏
        game = GameGUI()
        game.run()
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保所有游戏文件都在同一目录下")
        input("按回车键退出...")
    except Exception as e:
        print(f"游戏运行错误: {e}")
        print("请检查系统是否支持tkinter")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
