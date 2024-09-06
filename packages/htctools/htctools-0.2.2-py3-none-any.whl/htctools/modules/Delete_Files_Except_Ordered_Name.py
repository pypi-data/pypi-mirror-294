import os
import shutil
from datetime import datetime

def backup_file(file_path, folder_path, backup_folder):
    """
    备份单个文件到指定的备份目录，并保留原始的文件夹结构。
    
    :param file_path: 要备份的文件路径。
    :param folder_path: 原始文件夹路径。
    :param backup_folder: 备份目录路径。
    """
    # 计算文件相对于原始文件夹的相对路径
    relative_path = os.path.relpath(file_path, folder_path)
    # 计算备份文件的目标路径
    backup_path = os.path.join(backup_folder, relative_path)

    # 创建备份文件的父目录（如果不存在）
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    
    # 复制文件到备份目录
    shutil.copy2(file_path, backup_path)
    print(f"Backed up: {file_path} to {backup_path}")

def delete_files_except(folder_path, keep_files, backup_folder):
    """
    删除指定文件夹及子文件夹中除了指定文件列表之外的所有文件，并备份被删除的文件。

    :param folder_path: 目标文件夹的路径。
    :param keep_files: 一个列表，包含要保留的文件名。
    :param backup_folder: 备份被删除文件的目录。
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file not in keep_files:
                file_path = os.path.join(root, file)
                try:
                    # 备份文件到备份目录
                    backup_file(file_path, folder_path, backup_folder)
                    # 删除文件
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

def run(terminal_directory):
    folder_path = terminal_directory
    # 创建备份目录，带有时间戳
    backup_folder = os.path.join(folder_path, "backup_" + datetime.now().strftime('%Y%m%d_%H%M%S'))

    keep_files_input = input("Please Enter the Reserved file names (separated by comma), or type 'Exit' to cancel deleting: ")

    # 检查用户输入是否为退出命令
    if keep_files_input.lower() == 'exit':
        input("Delete has been cancelled. Press any key to continue...")
    else:
        # 处理保留文件名列表
        keep_files = [file.strip() for file in keep_files_input.split(',') if file.strip()]

        # 检查用户输入是否为空
        if not keep_files:
            print("No files specified to keep. Exiting.")
            return

        # 执行删除操作，并备份被删除的文件
        delete_files_except(folder_path, keep_files, backup_folder)
        input("You can find original backup files in the backup directory. Press any key to continue...")