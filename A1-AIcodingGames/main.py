#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神秘森林 - 文字冒险游戏
主程序入口文件

作者: AI Assistant
版本: 1.0.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 6):
        messagebox.showerror("版本错误", "需要Python 3.6或更高版本才能运行此游戏！")
        return False
    return True

def check_dependencies():
    """检查依赖库"""
    try:
        import tkinter
        return True
    except ImportError:
        messagebox.showerror("依赖错误", "缺少tkinter库！请确保Python安装时包含了tkinter。")
        return False

def show_splash_screen():
    """显示启动画面"""
    splash = tk.Tk()
    splash.title("")
    splash.geometry("400x200")
    splash.configure(bg='#1a1a1a')
    
    # 居中显示
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (400 // 2)
    y = (splash.winfo_screenheight() // 2) - (200 // 2)
    splash.geometry(f"400x200+{x}+{y}")
    
    # 移除窗口边框
    splash.overrideredirect(True)
    
    # 启动画面内容
    title_label = tk.Label(
        splash,
        text="🌲 神秘森林 🌲",
        bg='#1a1a1a',
        fg='#4CAF50',
        font=('微软雅黑', 20, 'bold')
    )
    title_label.pack(pady=(40, 10))
    
    subtitle_label = tk.Label(
        splash,
        text="文字冒险游戏",
        bg='#1a1a1a',
        fg='#ffffff',
        font=('微软雅黑', 12)
    )
    subtitle_label.pack(pady=5)
    
    loading_label = tk.Label(
        splash,
        text="正在加载...",
        bg='#1a1a1a',
        fg='#cccccc',
        font=('微软雅黑', 10)
    )
    loading_label.pack(pady=(20, 0))
    
    # 显示启动画面
    splash.update()
    
    return splash

def main():
    """主函数"""
    # 检查Python版本
    if not check_python_version():
        return
    
    # 检查依赖库
    if not check_dependencies():
        return
    
    # 显示启动画面
    splash = show_splash_screen()
    
    try:
        # 导入游戏模块
        from game_gui import GameGUI
        
        # 延迟一下让启动画面显示
        splash.after(2000, splash.destroy)
        
        # 创建并运行游戏
        game = GameGUI()
        game.run()
        
    except ImportError as e:
        splash.destroy()
        messagebox.showerror("导入错误", f"无法导入游戏模块: {str(e)}")
    except Exception as e:
        splash.destroy()
        messagebox.showerror("运行错误", f"游戏运行时发生错误: {str(e)}")
    finally:
        try:
            splash.destroy()
        except:
            pass

if __name__ == "__main__":
    main()
