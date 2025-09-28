import serial
import serial.tools.list_ports
import threading
import csv
from datetime import datetime
import pandas as pd
import os
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox


class SerialMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("串口监控工具 - 带时间戳记录（整合版）")
        self.root.geometry("850x650")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # 窗口关闭事件

        # 串口参数
        self.ser = None
        self.running = False
        self.port_var = tk.StringVar()
        self.baud_var = tk.IntVar(value=115200)  # 默认波特率设为115200（常用）

        # 文件存储参数
        self.default_output_folder = os.path.join(os.getcwd(), "Data")  # 默认数据文件夹（项目根目录/Data）
        self.output_folder = self.default_output_folder  # 实际存储路径
        self.filename_prefix = "SerialData"  # 默认文件名前缀
        self.max_lines = 1000  # 单个CSV文件最大行数
        self.current_lines = 0  # 当前文件已写行数
        self.file_counter = 1  # 文件分块计数器
        self.csv_file = None  # 当前打开的CSV文件对象
        self.csv_writer = None  # CSV写入器

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        """创建所有界面组件"""
        # 1. 串口设置区域
        frame_serial = ttk.LabelFrame(self.root, text="串口配置", padding=10)
        frame_serial.pack(fill=tk.X, padx=10, pady=5)

        # 端口选择
        ttk.Label(frame_serial, text="端口:").grid(row=0, column=0, sticky=tk.W)
        self.port_combobox = ttk.Combobox(frame_serial, textvariable=self.port_var, width=15)
        self.port_combobox['values'] = [port.device for port in serial.tools.list_ports.comports()]
        if self.port_combobox['values']:
            self.port_var.set(self.port_combobox['values'][0])  # 默认选中第一个端口
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5)

        # 波特率选择
        ttk.Label(frame_serial, text="波特率:").grid(row=0, column=2, sticky=tk.W)
        self.baud_combobox = ttk.Combobox(frame_serial, textvariable=self.baud_var, width=10,
                                         values=[9600, 19200, 38400, 57600, 115200, 230400])
        self.baud_combobox.set(115200)  # 默认波特率115200
        self.baud_combobox.grid(row=0, column=3, padx=5, pady=5)

        # 连接/断开按钮
        self.connect_btn = ttk.Button(frame_serial, text="打开串口", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=4, padx=10, pady=5)

        # 2. 文件设置区域（含自定义存储路径）
        frame_file = ttk.LabelFrame(self.root, text="文件配置", padding=10)
        frame_file.pack(fill=tk.X, padx=10, pady=5)

        # 存储路径设置
        ttk.Label(frame_file, text="存储路径:").grid(row=0, column=0, sticky=tk.W)
        self.path_entry = ttk.Entry(frame_file, width=40)
        self.path_entry.insert(0, self.default_output_folder)  # 默认显示项目根目录/Data
        self.path_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=tk.EW)
        self.browse_btn = ttk.Button(frame_file, text="浏览...", command=self.browse_folder)
        self.browse_btn.grid(row=0, column=4, padx=5, pady=5)

        # 自动创建子文件夹复选框
        self.subfolder_var = tk.BooleanVar(value=True)  # 默认勾选
        ttk.Checkbutton(frame_file, text="自动创建数据子文件夹（Data）", variable=self.subfolder_var).grid(
            row=1, column=0, columnspan=5, padx=5, pady=5, sticky=tk.W)

        # 文件名前缀和最大行数
        ttk.Label(frame_file, text="文件名前缀:").grid(row=2, column=0, sticky=tk.W)
        self.prefix_entry = ttk.Entry(frame_file, width=20)
        self.prefix_entry.insert(0, self.filename_prefix)
        self.prefix_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_file, text="单文件最大行数:").grid(row=2, column=2, sticky=tk.W)
        self.max_lines_entry = ttk.Spinbox(frame_file, from_=100, to=100000, width=10)
        self.max_lines_entry.insert(0, str(self.max_lines))
        self.max_lines_entry.grid(row=2, column=3, padx=5, pady=5)

        # 导出Excel按钮
        self.export_btn = ttk.Button(frame_file, text="导出Excel", command=self.export_to_excel)
        self.export_btn.grid(row=2, column=4, padx=5, pady=5)

        # 3. 数据收发区域
        frame_io = ttk.LabelFrame(self.root, text="数据收发", padding=10)
        frame_io.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 发送数据部分
        ttk.Label(frame_io, text="发送数据:").grid(row=0, column=0, sticky=tk.W)
        self.send_entry = ttk.Entry(frame_io, width=50)
        self.send_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW, columnspan=2)
        self.send_btn = ttk.Button(frame_io, text="发送", command=self.send_data)
        self.send_btn.grid(row=0, column=3, padx=5, pady=5)

        # 接收数据部分（带滚动条）
        ttk.Label(frame_io, text="接收数据:").grid(row=1, column=0, sticky=tk.W)
        self.receive_text = scrolledtext.ScrolledText(frame_io, height=15, wrap=tk.WORD)
        self.receive_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=tk.NSEW)
        self.receive_text.tag_config('timestamp', foreground='#0078D7')  # 时间戳蓝色
        self.receive_text.tag_config('data', foreground='#000000')  # 数据黑色

        # 4. 状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # 调整网格布局（让接收区域占满剩余空间）
        frame_io.grid_rowconfigure(2, weight=1)
        frame_io.grid_columnconfigure(1, weight=1)

    def toggle_connection(self):
        """切换串口连接状态（打开/关闭）"""
        if not self.running:
            self.connect_serial()
        else:
            self.disconnect_serial()

    def connect_serial(self):
        """连接串口"""
        # 获取用户输入的参数
        port = self.port_var.get()
        baud = self.baud_var.get()
        self.filename_prefix = self.prefix_entry.get().strip()
        self.max_lines = int(self.max_lines_entry.get())
        self.output_folder = self.path_entry.get().strip()

        # 验证参数有效性
        if not port:
            messagebox.showwarning("参数错误", "请选择串口端口！")
            return
        if not self.filename_prefix:
            messagebox.showwarning("参数错误", "文件名前缀不能为空！")
            return
        if not self.output_folder:
            messagebox.showwarning("参数错误", "存储路径不能为空！")
            return

        try:
            # 打开串口
            self.ser = serial.Serial(port, baud, timeout=0.1)
            self.running = True

            # 更新界面状态
            self.connect_btn.config(text="关闭串口")
            self.status_var.set(f"已连接：{port} @ {baud} 波特率")

            # 确保存储路径存在（自动创建文件夹）
            os.makedirs(self.output_folder, exist_ok=True)

            # 创建第一个CSV文件
            self.create_new_file()

            # 启动接收线程（后台运行，不阻塞界面）
            self.receive_thread = threading.Thread(target=self.receive_data, daemon=True)
            self.receive_thread.start()

        except Exception as e:
            messagebox.showerror("连接失败", f"无法打开串口：\n{str(e)}")
            self.running = False

    def disconnect_serial(self):
        """断开串口连接"""
        if self.running:
            self.running = False
            # 关闭串口
            if self.ser and self.ser.is_open:
                self.ser.close()
            # 关闭CSV文件
            if self.csv_file:
                self.csv_file.close()
            # 更新界面状态
            self.connect_btn.config(text="打开串口")
            self.status_var.set("已断开连接")

    def create_new_file(self):
        """创建新的CSV数据文件（带时间戳和分块）"""
        # 关闭当前打开的CSV文件（如果有）
        if self.csv_file:
            self.csv_file.close()

        # 生成文件名（格式：前缀_日期_时间_partN.csv）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.filename_prefix}_{timestamp}_part{self.file_counter}.csv"
        filepath = os.path.join(self.output_folder, filename)

        try:
            # 打开CSV文件（w模式：覆盖旧文件，newline=''避免空行）
            self.csv_file = open(filepath, 'w', newline='', encoding='utf-8')
            self.csv_writer = csv.writer(self.csv_file)
            # 写入表头（时间戳、数据）
            self.csv_writer.writerow(["Timestamp", "ReceivedData"])
            # 重置计数器
            self.current_lines = 0
            self.file_counter += 1
            # 更新状态栏
            self.status_var.set(f"当前文件：{filename}（存储路径：{self.output_folder}）")

        except Exception as e:
            messagebox.showerror("文件错误", f"无法创建CSV文件：\n{str(e)}")

    def receive_data(self):
        """接收串口数据（后台线程）"""
        while self.running and self.ser.is_open:
            try:
                # 读取串口数据（按行读取，去除换行符）
                data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                if data:
                    # 获取当前时间戳（毫秒级）
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    # 写入CSV文件
                    self.csv_writer.writerow([timestamp, data])
                    self.current_lines += 1
                    # 更新接收区域显示（线程安全：用root.after()避免界面冻结）
                    self.root.after(0, self.update_receive_display, timestamp, data)
                    # 检查是否需要分块（超过最大行数则创建新文件）
                    if self.current_lines >= self.max_lines:
                        self.root.after(0, self.create_new_file)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("接收错误", f"数据接收失败：\n{str(e)}"))
                self.disconnect_serial()
                break

    def update_receive_display(self, timestamp, data):
        """更新接收区域的显示（线程安全）"""
        # 插入时间戳（蓝色）
        self.receive_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        # 插入数据（黑色）
        self.receive_text.insert(tk.END, f"{data}\n", 'data')
        # 自动滚动到最底部（显示最新数据）
        self.receive_text.see(tk.END)

    def send_data(self):
        """发送数据到串口"""
        if not self.running or not self.ser.is_open:
            messagebox.showwarning("发送失败", "请先连接串口！")
            return

        # 获取发送内容（去除前后空格）
        data = self.send_entry.get().strip()
        if not data:
            messagebox.showwarning("发送失败", "发送内容不能为空！")
            return

        try:
            # 发送数据（添加换行符，方便设备接收）
            self.ser.write(f"{data}\n".encode('utf-8'))
            # 清空发送输入框
            self.send_entry.delete(0, tk.END)
            # 更新状态栏
            self.status_var.set(f"已发送：{data}")
        except Exception as e:
            messagebox.showerror("发送失败", f"无法发送数据：\n{str(e)}")

    def browse_folder(self):
        """浏览选择存储路径"""
        # 让用户选择父文件夹
        parent_folder = filedialog.askdirectory(title="选择存储父文件夹")
        if not parent_folder:
            return  # 用户取消选择，不做处理

        # 根据复选框状态决定是否创建Data子文件夹
        if self.subfolder_var.get():
            self.output_folder = os.path.join(parent_folder, "Data")
        else:
            self.output_folder = parent_folder

        # 更新输入框显示当前存储路径
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.output_folder)

        # 确保路径存在（自动创建）
        try:
            os.makedirs(self.output_folder, exist_ok=True)
            self.status_var.set(f"存储路径设置成功：{self.output_folder}")
        except Exception as e:
            messagebox.showerror("路径错误", f"无法创建存储路径：\n{str(e)}")

    def export_to_excel(self):
        """将CSV数据导出为Excel文件"""
        if not self.output_folder:
            messagebox.showwarning("导出失败", "存储路径不能为空！")
            return

        # 获取所有CSV文件（按文件名排序，确保分块顺序正确）
        csv_files = [
            os.path.join(self.output_folder, f)
            for f in os.listdir(self.output_folder)
            if f.startswith(self.filename_prefix) and f.endswith('.csv')
        ]
        csv_files.sort()  # 按文件名排序（确保part1、part2顺序正确）

        if not csv_files:
            messagebox.showwarning("导出失败", "没有可导出的CSV数据文件！")
            return

        try:
            # 合并所有CSV文件到一个DataFrame
            df_list = []
            for file in csv_files:
                df = pd.read_csv(file)
                df_list.append(df)
            combined_df = pd.concat(df_list, ignore_index=True)

            # 生成Excel文件名（前缀+日期时间）
            excel_filename = f"{self.filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            excel_path = os.path.join(self.output_folder, excel_filename)

            # 导出为Excel（不保留索引）
            combined_df.to_excel(excel_path, index=False, engine='openpyxl')

            # 提示导出成功
            messagebox.showinfo("导出成功", f"Excel文件已保存到：\n{excel_path}")
            self.status_var.set(f"导出成功：{excel_filename}")

        except Exception as e:
            messagebox.showerror("导出失败", f"无法导出Excel：\n{str(e)}")

    def on_closing(self):
        """窗口关闭事件处理（确保资源释放）"""
        self.disconnect_serial()
        self.root.destroy()


if __name__ == "__main__":
    # 创建Tkinter主窗口
    root = tk.Tk()
    # 实例化串口监控工具
    app = SerialMonitor(root)
    # 运行主循环（显示界面）
    root.mainloop()