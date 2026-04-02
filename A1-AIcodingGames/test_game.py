#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试游戏启动脚本
简化版本用于验证基本功能
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_basic_gui():
    """测试基本GUI功能"""
    root = tk.Tk()
    root.title("游戏测试")
    root.geometry("400x300")
    
    # 测试标签
    label = tk.Label(root, text="游戏测试成功！", font=("微软雅黑", 16))
    label.pack(pady=50)
    
    # 测试按钮
    def on_click():
        messagebox.showinfo("测试", "按钮点击正常！")
    
    button = tk.Button(root, text="测试按钮", command=on_click)
    button.pack(pady=20)
    
    # 退出按钮
    def on_quit():
        if messagebox.askyesno("退出", "确定要退出测试吗？"):
            root.destroy()
    
    quit_button = tk.Button(root, text="退出", command=on_quit)
    quit_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("开始测试游戏GUI...")
    test_basic_gui()
    print("测试完成")
