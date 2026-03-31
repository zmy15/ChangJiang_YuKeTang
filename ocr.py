import contextlib
import os
import subprocess
from io import BytesIO
import requests
import json
import base64
from PIL import Image


def pil_image_to_base64(pil_image, format='JPEG') -> str:
    """
    将PIL Image对象转换为Base64编码

    Args:
        pil_image (Image): PIL Image对象
        format (str): 输出格式，如 'JPEG', 'PNG', 'GIF'等

    Returns:
        str: Base64编码的图片字符串
    """
    try:
        # 创建字节缓冲区
        buffer = BytesIO()

        # 将图片保存到缓冲区
        if format.upper() == 'JPEG':
            # JPEG格式需要处理RGB模式
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
        elif format.upper() == 'PNG':
            # PNG支持透明通道
            if pil_image.mode not in ['RGB', 'RGBA']:
                pil_image = pil_image.convert('RGBA')

        pil_image.save(buffer, format=format)

        # 获取字节数据并进行Base64编码
        image_data = buffer.getvalue()
        base64_encoded = base64.b64encode(image_data).decode('utf-8')

        return base64_encoded

    except Exception as e:
        print(f"编码过程中发生错误：{e}")
        return ""


def ocr(image) -> str:
    url = "http://127.0.0.1:1224/api/ocr"
    data = {
        "base64": pil_image_to_base64(image),
        "options": {
            "ocr.cls": True,
            "data.format": "text",
        }
    }
    headers = {"Content-Type": "application/json"}
    data_str = json.dumps(data)
    response = requests.post(url, data=data_str, headers=headers)
    response.raise_for_status()
    res_dict = json.loads(response.text)
    return res_dict["data"]


@contextlib.contextmanager
def managed_process(executable_path):
    """管理进程的上下文管理器"""
    process = None
    try:
        if os.path.exists(executable_path):
            print(f"启动程序: {executable_path}")
            process = subprocess.Popen([executable_path])
            print(f"程序已启动，PID: {process.pid}")
            yield process
        else:
            raise FileNotFoundError(f"文件不存在: {executable_path}")
    finally:
        if process and process.poll() is None:
            print("结束进程...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print("进程已结束")
            except subprocess.TimeoutExpired:
                print("进程未响应，强制结束...")
                process.kill()
                process.wait()
                print("进程已被强制结束")
