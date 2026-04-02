#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版游戏GUI - 完全避免ttk主题问题
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
from game_data import Player, SCENES, ITEMS
from game_effects import GameEffects

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("神秘森林 - 文字冒险游戏")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')
        
        # 初始化游戏数据
        self.player = Player()
        self.current_scene = None
        
        # 初始化音效和视觉效果
        self.effects = GameEffects(self.root)
        
        # 创建UI组件
        self.create_widgets()
        
        # 加载初始场景
        self.load_scene("start")
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """创建UI组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 顶部信息栏
        self.create_info_bar(main_frame)
        
        # 中间内容区域
        content_frame = tk.Frame(main_frame, bg='#2b2b2b')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧游戏区域
        self.create_game_area(content_frame)
        
        # 右侧背包区域
        self.create_inventory_area(content_frame)
        
        # 底部控制按钮
        self.create_control_bar(main_frame)
        
    def create_info_bar(self, parent):
        """创建顶部信息栏"""
        info_frame = tk.Frame(parent, bg='#1a1a1a', height=60)
        info_frame.pack(fill=tk.X)
        info_frame.pack_propagate(False)
        
        # 游戏标题
        title_label = tk.Label(info_frame, text="神秘森林冒险", bg='#1a1a1a', fg='#ffffff',
                              font=('微软雅黑', 16, 'bold'))
        title_label.pack(side=tk.LEFT, pady=15)
        
        # 生命值显示
        self.health_label = tk.Label(info_frame, text=f"生命值: {self.player.health}/{self.player.max_health}", 
                                    bg='#1a1a1a', fg='#ff6b6b', font=('微软雅黑', 12))
        self.health_label.pack(side=tk.RIGHT, pady=15)
        
        # 当前场景
        self.scene_label = tk.Label(info_frame, text="当前位置: 未知", bg='#1a1a1a', fg='#4CAF50',
                                   font=('微软雅黑', 12))
        self.scene_label.pack(side=tk.RIGHT, pady=15)
        
    def create_game_area(self, parent):
        """创建游戏主区域"""
        game_frame = tk.Frame(parent, bg='#2b2b2b')
        game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 场景标题
        self.scene_title = tk.Label(game_frame, text="", bg='#2b2b2b', fg='#4CAF50', 
                                   font=('微软雅黑', 16, 'bold'))
        self.scene_title.pack(pady=10)
        
        # 场景描述文本框
        self.description_text = scrolledtext.ScrolledText(
            game_frame, 
            wrap=tk.WORD, 
            width=50, 
            height=15,
            bg='#3b3b3b', 
            fg='#ffffff',
            font=('微软雅黑', 12),
            relief=tk.FLAT
        )
        self.description_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.description_text.config(state=tk.DISABLED)
        
        # 选择按钮框架
        self.choices_frame = tk.Frame(game_frame, bg='#2b2b2b')
        self.choices_frame.pack(fill=tk.X)
        
        # 选择按钮列表
        self.choice_buttons = []
        
    def create_inventory_area(self, parent):
        """创建背包区域"""
        inventory_frame = tk.Frame(parent, bg='#1a1a1a', width=300)
        inventory_frame.pack(side=tk.RIGHT, fill=tk.Y)
        inventory_frame.pack_propagate(False)
        
        # 背包标题
        inventory_title = tk.Label(inventory_frame, text="背包", bg='#1a1a1a', fg='#FFD700',
                                  font=('微软雅黑', 14, 'bold'))
        inventory_title.pack(pady=10)
        
        # 物品列表框架
        self.inventory_listbox = tk.Listbox(
            inventory_frame,
            bg='#3b3b3b',
            fg='#ffffff',
            font=('微软雅黑', 10),
            selectmode=tk.SINGLE,
            height=15,
            relief=tk.FLAT
        )
        self.inventory_listbox.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 物品描述
        self.item_description = tk.Text(
            inventory_frame,
            height=4,
            bg='#2b2b2b',
            fg='#cccccc',
            font=('微软雅黑', 9),
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.item_description.pack(fill=tk.X, pady=10)
        self.item_description.config(state=tk.DISABLED)
        
        # 使用物品按钮
        self.use_item_btn = tk.Button(
            inventory_frame,
            text="使用物品",
            bg='#4CAF50',
            fg='white',
            font=('微软雅黑', 10),
            relief=tk.FLAT,
            command=self.use_item,
            state=tk.DISABLED
        )
        self.use_item_btn.pack(pady=10)
        
        # 绑定物品选择事件
        self.inventory_listbox.bind('<<ListboxSelect>>', self.on_item_select)
        
    def create_control_bar(self, parent):
        """创建底部控制栏"""
        control_frame = tk.Frame(parent, bg='#1a1a1a', height=50)
        control_frame.pack(fill=tk.X, pady=10)
        control_frame.pack_propagate(False)
        
        # 重新开始按钮
        restart_btn = tk.Button(
            control_frame,
            text="重新开始",
            bg='#ff6b6b',
            fg='white',
            font=('微软雅黑', 11),
            relief=tk.FLAT,
            command=self.restart_game
        )
        restart_btn.pack(side=tk.LEFT, pady=10)
        
        # 保存游戏按钮
        save_btn = tk.Button(
            control_frame,
            text="保存游戏",
            bg='#4169E1',
            fg='white',
            font=('微软雅黑', 11),
            relief=tk.FLAT,
            command=self.save_game
        )
        save_btn.pack(side=tk.LEFT, pady=10)
        
        # 加载游戏按钮
        load_btn = tk.Button(
            control_frame,
            text="加载游戏",
            bg='#FF8C00',
            fg='white',
            font=('微软雅黑', 11),
            relief=tk.FLAT,
            command=self.load_game
        )
        load_btn.pack(side=tk.LEFT, pady=10)
        
        # 退出按钮
        quit_btn = tk.Button(
            control_frame,
            text="退出游戏",
            bg='#666666',
            fg='white',
            font=('微软雅黑', 11),
            relief=tk.FLAT,
            command=self.on_closing
        )
        quit_btn.pack(side=tk.RIGHT, pady=10)
        
    def load_scene(self, scene_id):
        """加载场景"""
        if scene_id not in SCENES:
            messagebox.showerror("错误", f"场景 {scene_id} 不存在！")
            return
            
        self.current_scene = SCENES[scene_id]
        self.player.current_scene = scene_id
        
        # 更新场景标题
        self.scene_title.config(text=f"当前位置: {self.current_scene.title}")
        self.scene_label.config(text=f"当前位置: {self.current_scene.title}")
        
        # 更新场景描述
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, self.current_scene.description)
        self.description_text.config(state=tk.DISABLED)
        
        # 清除旧的选择按钮
        for btn in self.choice_buttons:
            btn.destroy()
        self.choice_buttons.clear()
        
        # 创建新的选择按钮
        for i, (choice_text, next_scene) in enumerate(self.current_scene.choices):
            # 创建按钮
            btn = tk.Button(
                self.choices_frame,
                text=f"{i+1}. {choice_text}",
                bg='#4CAF50',
                fg='white',
                font=('微软雅黑', 11),
                relief=tk.FLAT,
                wraplength=400,
                justify=tk.LEFT
            )
            btn.pack(fill=tk.X, pady=3)
            self.choice_buttons.append(btn)
            
            # 设置命令，避免lambda作用域问题
            btn.config(command=lambda ns=next_scene, b=btn: self.on_choice_click(ns, b))
        
        # 获得物品
        for item_name in self.current_scene.items:
            if item_name in ITEMS and item_name not in self.player.inventory:
                self.player.inventory.append(item_name)
                self.effects.play_item_sound()
                self.show_message(f"获得物品: {item_name}")
        
        # 更新背包显示
        self.update_inventory()
        
        # 检查是否是结局场景
        if scene_id in ["ending_good", "ending_bad"]:
            self.show_ending(scene_id)
            
    def on_choice_click(self, next_scene_id, button):
        """选择按钮点击事件"""
        # 播放点击音效
        self.effects.play_click_sound()
        
        # 延迟加载下一个场景
        self.root.after(300, lambda: self.make_choice(next_scene_id))
        
    def make_choice(self, next_scene_id):
        """做出选择"""
        # 特殊场景处理
        if self.player.current_scene == "help_wolf" and next_scene_id == "follow_wolf":
            self.load_scene("cave_deep")
        elif self.player.current_scene == "swim_to_island" and next_scene_id == "take_treasure":
            self.load_scene("ending_good")
        elif next_scene_id not in SCENES:
            # 默认处理未定义的场景
            self.load_scene("ending_bad")
        else:
            self.load_scene(next_scene_id)
            
    def update_inventory(self):
        """更新背包显示"""
        self.inventory_listbox.delete(0, tk.END)
        for item_name in self.player.inventory:
            if item_name in ITEMS:
                item = ITEMS[item_name]
                display_text = f"{item_name}"
                if item.usable:
                    display_text += " [可用]"
                self.inventory_listbox.insert(tk.END, display_text)
                
    def on_item_select(self, event):
        """物品选择事件"""
        selection = self.inventory_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.player.inventory):
                item_name = self.player.inventory[index]
                if item_name in ITEMS:
                    item = ITEMS[item_name]
                    self.item_description.config(state=tk.NORMAL)
                    self.item_description.delete(1.0, tk.END)
                    self.item_description.insert(tk.END, item.description)
                    self.item_description.config(state=tk.DISABLED)
                    
                    # 启用/禁用使用按钮
                    if item.usable:
                        self.use_item_btn.config(state=tk.NORMAL)
                    else:
                        self.use_item_btn.config(state=tk.DISABLED)
                        
    def use_item(self):
        """使用物品"""
        selection = self.inventory_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        if index >= len(self.player.inventory):
            return
            
        item_name = self.player.inventory[index]
        if item_name not in ITEMS:
            return
            
        item = ITEMS[item_name]
        if not item.usable:
            messagebox.showinfo("提示", "这个物品不能使用。")
            return
            
        # 执行物品效果
        if item_name == "急救包":
            heal_amount = 30
            self.player.health = min(self.player.max_health, self.player.health + heal_amount)
            self.player.inventory.remove(item_name)
            self.show_message(f"使用了急救包，恢复了 {heal_amount} 点生命值！")
            self.update_health_display()
            self.update_inventory()
            
        elif item_name == "手电筒":
            self.show_message("手电筒照亮了周围的环境，你可以看得更清楚了。")
            
        elif item_name == "罐头食品":
            self.player.health = min(self.player.max_health, self.player.health + 10)
            self.player.inventory.remove(item_name)
            self.show_message("吃了罐头食品，恢复了 10 点生命值！")
            self.update_health_display()
            self.update_inventory()
            
        elif item_name == "露营刀":
            self.show_message("这把露营刀很锋利，可能在关键时刻有用。")
            
        elif item_name == "树枝":
            self.show_message("这是一根结实的树枝，可以作为简单的武器。")
            
        elif item_name == "生锈的钥匙":
            self.show_message("这把钥匙看起来很古老，也许能打开某个重要的门。")
            
    def update_health_display(self):
        """更新生命值显示"""
        self.health_label.config(text=f"生命值: {self.player.health}/{self.player.max_health}")
        
    def show_message(self, message):
        """显示临时消息"""
        messagebox.showinfo("提示", message)
        
    def show_ending(self, ending_type):
        """显示结局"""
        if ending_type == "ending_good":
            messagebox.showinfo("完美结局", "恭喜你完成了冒险！你找到了传说中的宝藏，成为了森林的传奇。")
        else:
            messagebox.showinfo("悲剧结局", "很遗憾，这次冒险失败了。也许下次会有更好的结果...")
            
    def restart_game(self):
        """重新开始游戏"""
        if messagebox.askyesno("确认", "确定要重新开始游戏吗？当前进度将会丢失。"):
            self.player = Player()
            self.load_scene("start")
            self.update_health_display()
            self.update_inventory()
            
    def save_game(self):
        """保存游戏"""
        # 简单的保存功能
        save_data = {
            'health': self.player.health,
            'inventory': self.player.inventory,
            'current_scene': self.player.current_scene,
            'game_flags': self.player.game_flags
        }
        try:
            import json
            with open('savegame.json', 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("成功", "游戏已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
            
    def load_game(self):
        """加载游戏"""
        try:
            import json
            with open('savegame.json', 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            self.player.health = save_data['health']
            self.player.inventory = save_data['inventory']
            self.player.current_scene = save_data['current_scene']
            self.player.game_flags = save_data.get('game_flags', {})
            
            self.load_scene(self.player.current_scene)
            self.update_health_display()
            self.update_inventory()
            messagebox.showinfo("成功", "游戏已加载！")
        except FileNotFoundError:
            messagebox.showerror("错误", "没有找到存档文件！")
        except Exception as e:
            messagebox.showerror("错误", f"加载失败: {str(e)}")
            
    def on_closing(self):
        """窗口关闭事件"""
        if messagebox.askyesno("退出", "确定要退出游戏吗？"):
            self.root.destroy()
            
    def run(self):
        """运行游戏"""
        self.root.mainloop()
