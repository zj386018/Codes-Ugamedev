"""
游戏音效和视觉效果模块
提供音效播放、动画效果等功能
"""

import tkinter as tk
import threading
import time
import random
import winsound
import sys
import os

class GameEffects:
    """游戏效果管理器"""
    
    def __init__(self, root_window):
        self.root = root_window
        self.sound_enabled = True
        self.animation_enabled = True
        
        # 检查系统是否支持音效
        self.check_sound_support()
        
    def check_sound_support(self):
        """检查音效支持"""
        try:
            # 尝试播放一个测试声音
            winsound.Beep(1000, 1)
            self.sound_enabled = True
        except:
            self.sound_enabled = False
            print("警告: 系统不支持音效播放")
            
    def play_typing_sound(self):
        """播放打字音效"""
        if not self.sound_enabled:
            return
            
        def play_sound():
            try:
                # 模拟打字声音
                frequency = random.randint(800, 1200)
                duration = 50
                winsound.Beep(frequency, duration)
            except:
                pass
                
        threading.Thread(target=play_sound, daemon=True).start()
        
    def play_click_sound(self):
        """播放点击音效"""
        if not self.sound_enabled:
            return
            
        def play_sound():
            try:
                winsound.Beep(600, 100)
            except:
                pass
                
        threading.Thread(target=play_sound, daemon=True).start()
        
    def play_success_sound(self):
        """播放成功音效"""
        if not self.sound_enabled:
            return
            
        def play_sound():
            try:
                # 播放上升音调
                for freq in [523, 659, 784]:  # C, E, G
                    winsound.Beep(freq, 150)
                    time.sleep(0.1)
            except:
                pass
                
        threading.Thread(target=play_sound, daemon=True).start()
        
    def play_error_sound(self):
        """播放错误音效"""
        if not self.sound_enabled:
            return
            
        def play_sound():
            try:
                # 播放下降音调
                for freq in [400, 300, 200]:
                    winsound.Beep(freq, 200)
                    time.sleep(0.1)
            except:
                pass
                
        threading.Thread(target=play_sound, daemon=True).start()
        
    def play_item_sound(self):
        """播放获得物品音效"""
        if not self.sound_enabled:
            return
            
        def play_sound():
            try:
                # 播放闪烁音效
                for _ in range(3):
                    winsound.Beep(1000, 50)
                    time.sleep(0.05)
            except:
                pass
                
        threading.Thread(target=play_sound, daemon=True).start()
        
    def typewriter_effect(self, text_widget, text, delay=30):
        """打字机效果显示文本"""
        # 简化版本，直接显示文本避免线程问题
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)
        
        # 播放一次音效表示文本显示完成
        self.play_typing_sound()
        
    def fade_in_effect(self, widget, duration=1000):
        """淡入效果"""
        if not self.animation_enabled:
            return
            
        def fade():
            steps = 20
            for i in range(steps + 1):
                alpha = i / steps
                # 这里简化处理，实际Tkinter的透明度支持有限
                widget.update()
                time.sleep(duration / (steps * 1000.0))
                
        threading.Thread(target=fade, daemon=True).start()
        
    def shake_effect(self, widget, intensity=5, duration=200):
        """震动效果"""
        if not self.animation_enabled:
            return
            
        def shake():
            original_x = widget.winfo_x()
            original_y = widget.winfo_y()
            
            steps = int(duration / 20)
            for i in range(steps):
                if i % 2 == 0:
                    offset_x = random.randint(-intensity, intensity)
                    offset_y = random.randint(-intensity, intensity)
                    # 注意：这里只是示例，实际移动窗口需要不同的方法
                time.sleep(0.02)
                
        threading.Thread(target=shake, daemon=True).start()
        
    def highlight_effect(self, widget, color='#FFD700', duration=500):
        """高亮效果"""
        if not self.animation_enabled:
            return
            
        original_bg = widget.cget('bg') if hasattr(widget, 'cget') else widget['bg']
        
        def highlight():
            try:
                # 设置高亮颜色
                if hasattr(widget, 'config'):
                    widget.config(bg=color)
                elif hasattr(widget, '__setitem__'):
                    widget['bg'] = color
                    
                time.sleep(duration / 1000.0)
                
                # 恢复原色
                if hasattr(widget, 'config'):
                    widget.config(bg=original_bg)
                elif hasattr(widget, '__setitem__'):
                    widget['bg'] = original_bg
            except:
                pass
                
        threading.Thread(target=highlight, daemon=True).start()
        
    def pulse_effect(self, widget, duration=1000):
        """脉冲效果"""
        if not self.animation_enabled:
            return
            
        def pulse():
            try:
                original_font = widget.cget('font') if hasattr(widget, 'cget') else widget['font']
                steps = 10
                
                for i in range(steps * 2):
                    if i < steps:
                        # 放大
                        scale = 1 + (i / steps) * 0.2
                    else:
                        # 缩小
                        scale = 1.2 - ((i - steps) / steps) * 0.2
                    
                    # 这里简化处理，实际字体缩放需要更复杂的实现
                    time.sleep(duration / (steps * 2 * 1000.0))
                    
            except:
                pass
                
        threading.Thread(target=pulse, daemon=True).start()
        
    def create_particle_effect(self, parent, x, y, count=10, color='#FFD700'):
        """创建粒子效果"""
        if not self.animation_enabled:
            return
            
        particles = []
        
        for i in range(count):
            particle = tk.Label(
                parent,
                text='✨',
                bg='transparent',
                fg=color,
                font=('Arial', random.randint(8, 16))
            )
            
            # 随机位置
            px = x + random.randint(-20, 20)
            py = y + random.randint(-20, 20)
            particle.place(x=px, y=py)
            particles.append(particle)
            
        def animate_particles():
            for _ in range(20):  # 动画帧数
                for particle in particles:
                    try:
                        current_x = particle.winfo_x()
                        current_y = particle.winfo_y()
                        
                        # 向上飘动
                        new_y = current_y - random.randint(1, 3)
                        new_x = current_x + random.randint(-2, 2)
                        
                        particle.place(x=new_x, y=new_y)
                        
                        # 逐渐消失
                        if _ > 15:
                            particle.config(fg='#FFFFFF' if _ % 2 == 0 else color)
                            
                    except:
                        pass
                        
                time.sleep(0.05)
                
            # 清理粒子
            for particle in particles:
                try:
                    particle.destroy()
                except:
                    pass
                    
        threading.Thread(target=animate_particles, daemon=True).start()
        
    def scene_transition_effect(self, callback):
        """场景转换效果"""
        if not self.animation_enabled:
            callback()
            return
            
        def transition():
            # 创建黑色遮罩
            overlay = tk.Toplevel(self.root)
            overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}")
            overlay.configure(bg='black')
            overlay.overrideredirect(True)
            
            # 居中显示
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            overlay.geometry(f"+{x}+{y}")
            
            # 淡入黑色
            for i in range(10):
                overlay.attributes('-alpha', i / 10)
                overlay.update()
                time.sleep(0.03)
                
            # 执行回调（加载新场景）
            callback()
            
            # 淡出黑色
            for i in range(10, -1, -1):
                overlay.attributes('-alpha', i / 10)
                overlay.update()
                time.sleep(0.03)
                
            overlay.destroy()
            
        threading.Thread(target=transition, daemon=True).start()
        
    def toggle_sound(self):
        """切换音效开关"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled
        
    def toggle_animation(self):
        """切换动画开关"""
        self.animation_enabled = not self.animation_enabled
        return self.animation_enabled
