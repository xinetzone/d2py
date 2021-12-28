'''解压后中文路径乱码的解决方案
'''

from pathlib import Path
from zipfile import ZipFile


def decode_path(path):
    '''将乱码的路径编码为 UTF8

    :path: Path 的实例
    '''
    try:
        path_name = path.decode('utf-8')
    except:
        path_name = path.encode('437').decode('gbk')
        path_name = path_name.encode('utf-8').decode('utf-8')
    return path_name


def extract(zip_name, out_dir):
    '''将 zip_name 文件解压到 out_dir 目录
    '''
    out_dir = Path(out_dir)
    with ZipFile(zip_name, allowZip64=True) as Z:
        # 排除目录文件
        file_iter = (file for file in Z.filelist if not file.is_dir())
        for file in file_iter:
            # 编码文件名称为 utf 格式
            file.filename = decode_path(file.filename)
            Z.extract(file, out_dir/file.filename)


def extract_all(zip_root, out_dir):
    '''解压 zip_root 目录下的全部 zip 文件到 out_dir 目录'''
    for zip_dir in Path(zip_root).rglob('*.zip'):
        # 解压单个数据集
        extract(zip_dir, out_dir)
    print("全部解压完成！")
