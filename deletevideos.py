import os
import shutil

def delete_videos_from_folder(folder_path):
    # 定义一个包含视频文件扩展名的列表
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.mpg', '.3gp', '.webm']
    
    # 遍历指定文件夹
    for filename in os.listdir(folder_path):
        
       
        # 检查文件扩展名是否在视频扩展名列表中
        if any(filename.lower().endswith(ext) for ext in video_extensions):
            print(f"Will delete: {filename}")
            # 构建完整的文件路径
            file_path = os.path.join(folder_path, filename)
            
            # 删除文件
            try:
                shutil.rmtree(file_path)  # 如果是文件夹
            except NotADirectoryError:
                os.remove(file_path)  # 如果是文件

if __name__ == "__main__":
    folder_path = r'./'
    delete_videos_from_folder(folder_path)
