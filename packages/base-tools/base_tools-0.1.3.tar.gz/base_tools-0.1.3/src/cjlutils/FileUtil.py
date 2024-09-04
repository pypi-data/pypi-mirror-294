import os
import numpy as np
import random
import shutil
import zipfile


def create_dir(dir_path: str, create_parent: bool = True) -> bool:
    """
    创建目录
    :param dir_path: 目录路径
    :param create_parent: 是否创建父目录
    """
    if dir_path is None or dir_path == '':
        return False
    if create_parent:
        os.makedirs(dir_path, exist_ok=True)
        return True
    else:
        parent_dir = get_parent_dir(dir_path, 1)
        if not is_dir(parent_dir):
            return False
        os.mkdir(dir_path)
        return True


def create_file(file_path: str, content: str = None, create_parent: bool = True, replace: bool = False) -> bool:
    """
    创建文件
    :param file_path: 文件路径
    :param content: 文件内容
    :param create_parent: 是否创建父目录
    :param replace: 如果路径上已经存在文件，是否替换
    """
    if file_path is None or file_path == '':
        return False
    parent_dir = os.path.dirname(file_path)

    if create_parent:
        create_dir_result = create_dir(parent_dir, True)
        if not create_dir_result:
            return False
    if not is_dir(parent_dir):
        return False
    if is_file(file_path):
        # 如果文件已经存在
        if replace:
            # 如果需要替换，则删除原文件
            os.remove(file_path)
        else:
            # 如果不需要替换，则返回失败
            return False
    with open(file_path, 'w') as f:
        if content is not None:
            f.write(content)
    return True


def create_audio_file(signal: list | np.ndarray, save_path: str, sample_rate: int = 44100) -> bool:
    if is_file(save_path):
        return False
    if not is_dir(get_parent_dir(save_path)):
        return False

    from scipy.io import wavfile
    # 将信号转换为16位整数
    audio = np.array(signal).astype(np.int16)

    # 保存为WAV文件
    wavfile.write(save_path, sample_rate, audio)
    return True


def create_random_audio_file(save_path: str, duration: int, sample_rate: int = 44100) -> bool:
    if is_file(save_path):
        return False
    if not is_dir(get_parent_dir(save_path)):
        return False

    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # 生成随机信号(高斯波)
    signal = np.random.uniform(-1, 1, int(sample_rate * duration))

    # 添加一些随机频率的正弦波,使声音更有趣
    for _ in range(5):
        frequency = np.random.uniform(20, 2000)
        signal += 0.2 * np.sin(2 * np.pi * frequency * t)

    # 确保信号在-1到1之间
    signal = np.clip(signal, -1, 1)

    # 放大信号
    signal *= 2**15-1

    create_audio_file(signal, save_path, sample_rate)
    return True


def create_random_rgb_image_file(save_path: str, width: int, height: int) -> bool:
    if is_file(save_path):
        return False
    if not is_dir(get_parent_dir(save_path)):
        return False

    from PIL import Image

    image: Image = Image.new('RGB', (width, height))

    # 获取像素访问对象
    pixels = image.load()

    # 为每个像素随机生成颜色
    for x in range(width):
        for y in range(height):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            pixels[x, y] = (r, g, b)

    # 保存图片
    image.save(save_path)
    return True


def create_random_rgb_video_file(save_path: str, width: int, height: int, duration: int, fps: int):
    if is_file(save_path):
        return False
    if not is_dir(get_parent_dir(save_path)):
        return False

    import cv2

    # 创建VideoWriter对象
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    # 生成随机帧并写入视频
    for _ in range(fps * duration):
        # 创建随机颜色的帧
        frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        out.write(frame)

    # 释放资源
    out.release()

    print("随机视频已生成并保存为 'random_video.mp4'")


def exists(path: str) -> bool:
    """
    判断路径是否存在
    :param path: 路径
    :return: 是否存在
    """
    if path is None or path == '':
        return False
    return os.path.exists(path)


def get_file_list(dir_path: str, suffix: str = None, recursive: bool = False) -> list[str]:
    """
    获取指定目录下的所有文件路径
    :param dir_path: 目录路径
    :param suffix: 文件后缀名
    :param recursive: 是否递归查找
    :return: 文件路径组成的列表
    """
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if suffix is not None and not file.endswith(suffix):
                continue
            file_list.append(os.path.join(root, file))
        if not recursive:
            break
    return file_list


def get_file_name(path: str) -> str:
    """
    获取文件名
    :param path: 文件路径
    :return: 文件名
    """
    if path is None or path == '':
        return ''
    return os.path.basename(path)


def get_file_size(path: str) -> int:
    """
    获取文件大小
    :param path: 文件路径
    :return: 文件大小
    """
    if path is None or path == '':
        return -1
    if not is_file(path):
        return -1
    return os.path.getsize(path)


def get_file_data(path: str) -> None | bytes:
    """
    获取文件数据
    :param path: 文件路径
    :return: 文件数据
    """
    if not is_file(path):
        return None
    with open(path, 'rb') as f:
        data = f.read()
        if data is not None and data.__class__ is str:
            data = str(data).encode()
        return data


def get_parent_dir(path: str, level: int = 1) -> str:
    """
    获取指定路径的父目录
    :param path: 路径
    :param level: 父目录层级
    :return: 父目录路径
    """
    for _ in range(level):
        path = os.path.dirname(path)
    return path


def is_dir(path: str) -> bool:
    """
    判断路径是否为目录
    :param path: 路径
    :return: 是否为目录
    """
    if path is None or path == '':
        return False
    return os.path.isdir(path)


def is_file(path: str) -> bool:
    """
    判断路径是否为文件
    :param path: 路径
    :return: 是否为文件
    """
    if path is None or path == '':
        return False
    return os.path.isfile(path)


def md5_file(file_path: str) -> str:
    """
    获取文件的MD5值
    :param file_path: 文件路径
    :return: MD5值
    """
    import hashlib
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def read_all(file_path: str) -> str:
    """
    读取文件内容
    :param file_path: 文件路径
    :return:
    """
    with open(file_path, 'r') as f:
        return f.read()


def remove_dir(dir_path: str):
    """
    删除目录
    :param dir_path: 目录路径
    """
    shutil.rmtree(dir_path)


def remove_file(file_path: str):
    """
    删除文件
    :param file_path: 文件路径
    """
    os.remove(file_path)


def unzip_file(zip_path: str, out_dir: str):
    """
    解压指定文件
    :param zip_path: 压缩文件路径
    :param out_dir: 输出的目录路径
    """
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(out_dir)


def zip_files(paths: list[str], out_path: str, compression: int = zipfile.ZIP_STORED):
    """
    压缩指定文件
    :param paths: 文件路径组成的列表
    :param out_path: 输出的压缩文件的路径
    :param compression: 压缩方式
                ZIP_STORED = 0 # 不进行实际的压缩。它只是将文件原样打包到 ZIP 归档中，适用于已经经过其他压缩算法压缩的文件，或者对于不需要进一步压缩的文件。
                ZIP_DEFLATED = 8 # 使用 DEFLATE 算法进行压缩，通常可以提供较好的压缩比。
                ZIP_BZIP2 = 12 # 使用 BZIP2 算法进行压缩。BZIP2 通常比 DEFLATED 提供更好的压缩效果，但压缩和解压缩的速度可能会稍慢一些。
                ZIP_LZMA = 14 # 使用 LZMA 算法进行压缩。LZMA 通常能够提供更高的压缩比，但可能需要更多的计算资源来压缩和解压缩。
    :return:
    """
    zip_file = zipfile.ZipFile(out_path, "w", compression, allowZip64=True)

    for path in paths:
        pre_len = len(os.path.dirname(path))
        arc_name = path[pre_len:].strip(os.path.sep)
        zip_file.write(path, arc_name)
    zip_file.close()
