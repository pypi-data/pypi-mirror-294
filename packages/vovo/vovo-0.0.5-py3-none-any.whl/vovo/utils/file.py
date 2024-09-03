import os

import requests
from tqdm import tqdm


def download_file_with_temporary_save(url, save_path):
    """下载文件并保存"""

    temp_save_path = save_path + ".part"  # 使用临时文件路径

    try:
        # 发送HTTP请求获取文件
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果请求不成功，会抛出异常

        # 获取文件总大小
        total_size = int(response.headers.get('content-length', 0))

        # 打开文件以二进制写入
        with open(temp_save_path, 'wb') as file:
            # 使用 tqdm 显示进度条
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=temp_save_path, initial=0, ascii=True) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # 过滤掉保持活动的空块
                        file.write(chunk)
                        pbar.update(len(chunk))

        # 下载完成后重命名临时文件为最终文件
        os.rename(temp_save_path, save_path)
    except Exception:
        if os.path.exists(temp_save_path):
            os.remove(temp_save_path)  # 删除临时文件
        raise
