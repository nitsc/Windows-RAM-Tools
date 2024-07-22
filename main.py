#导入必要的模块
import io
import psutil
import sys
import mmap
import os

#简介
print("Windows RAM 写入与进程PID展示工具")
print("作者：Dean of NITSC， 出现问题不负责")

#主循环
def main():
    def main_in_main():
        while True:
            ans = input("请选择操作：\n\t1. 获取当前进程的 PID\n\t2. 加载文件到内存中\n\t3. 退出\n")
            if ans == "1":
                list_running_processes()
            elif ans == "2":
                load()
            elif ans == "3":
                sys.exit()
            else:
                print("无效的选项，请重新输入。")
                continue

    # 获取当前进程的 PID
    def list_running_processes():
        for process in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                pid = process.info['pid']
                name = process.info['name']
                exe = process.info['exe']
                print(f"PID: {pid}, Name: {name}, Executable Path: {exe}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    # 读取二进制文件到内存中
    def read_binary_file(file_path):
        with open(file_path, 'rb') as f:
            binary_data = f.read()
        return io.BytesIO(binary_data)

    # 写回到文件
    def write_binary_file(file_path, binary_io):
        with open(file_path, 'wb') as f:
            f.write(binary_io.getbuffer())

    # 读取内存映射文件
    def read_from_memory_mapped_file(file_path, start, length):
        with open(file_path, 'rb') as f:
            # 创建内存映射对象
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            try:
                # 读取内存映射文件内容
                mm.seek(start)
                data = mm.read(length)
            finally:
                mm.close()
        return data

    # 写入内存映射文件
    def write_to_memory_mapped_file(file_path, data, start):
        with open(file_path, 'r+b') as f:
            # 创建内存映射对象
            mm = mmap.mmap(f.fileno(), 0)
            try:
                mm.seek(start)  # 回到指定位置
                mm.write(data)
            finally:
                mm.close()
    
    # 加载函数
    def load():
        file_path = input("请输入文件路径：")
                
        # 读取二进制文件到内存中
        binary_io = read_binary_file(file_path)

        # 假设我们对内容进行某种修改（这里只是示例）
        # 在实际应用中，你会进行具体的操作，如编辑视频元数据
        binary_io.seek(100)
        binary_io.write(b'NEW DATA')

        # 写回到文件
        write_binary_file(file_path, binary_io)
                
        # 验证写入是否成功
        modified_data = read_from_memory_mapped_file(file_path, 100, len(b'NEW DATA'))
        print(f'Modified data: {modified_data}')
        print("成功 successfully")
        
    if  '1' == '1':
        main_in_main()  

if '1' == '1':
    main()
