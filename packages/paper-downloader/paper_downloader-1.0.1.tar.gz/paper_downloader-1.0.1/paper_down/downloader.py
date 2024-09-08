# Example usage
import requests
from pypdf import PdfWriter
import os
from tqdm import tqdm  # 进度条库
from paper_down.config.config_loader import config


def download_and_merge_pdfs(url1, url2=None):
    temp_filename = config.temp_filename
    temp_first_name  = config.temp_filename_1
    temp_second_name = config.temp_filename_2
    # Helper function to download a single PDF with progress bar
    def download_pdf(url, filename):
        response = requests.get(url, stream=True)
        if response.headers['Content-Type'] != 'application/pdf':
            raise ValueError(f"URL {url} does not point to a PDF file.")
        
        # 获取文件大小以便计算进度
        total_size = int(response.headers.get('Content-Length', 0))
        true_filename = url.split('/')[-1]
        
        # 下载并显示进度条
        with open(filename, 'wb') as f, tqdm(
            desc=f"Downloading {true_filename}",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(1024):  # 每次下载1024字节
                f.write(chunk)
                bar.update(len(chunk))
        
        return filename
    
    # 下载第一个PDF
    file1 = download_pdf(url1, temp_filename if not url2 else temp_first_name)
    
    if url2:
        # 下载第二个PDF
        file2 = download_pdf(url2, temp_second_name)
        
        # 合并PDF
        merger = PdfWriter()
        # import pdb; pdb.set_trace()
        merger.append(file1)
        merger.append(file2)
        with open(temp_filename, 'wb') as f_out:
            merger.write(f_out)
        merger.close()
        
        # 删除临时下载的PDF文件
        os.remove(file1)
        os.remove(file2)
        
        return temp_filename
    else:
        return file1
