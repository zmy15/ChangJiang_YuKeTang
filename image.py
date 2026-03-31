import requests
from PIL import Image
import io

from PIL.ImageFile import ImageFile
from selenium.webdriver.common.by import By


def get_image_url(target_item) -> str | None:
    """获取图片URL"""
    try:
        # 根据您提供的HTML，图片在class为"cover"的img元素中
        img_element = target_item.find_element(By.CSS_SELECTOR, "img.cover")
        img_url = img_element.get_attribute("src")
        print(f"获取到图片URL: {img_url}")
        return img_url
    except Exception as e:
        print("未找到图片元素")
        return None


def download_image(img_url) -> ImageFile | None:
    """下载图片"""
    try:
        response = requests.get(img_url)
        response.raise_for_status()

        # 将图片转换为PIL Image对象
        image = Image.open(io.BytesIO(response.content))
        print(f"图片下载成功，尺寸: {image.size}")
        return image
    except Exception as e:
        print(f"下载图片失败: {e}")
        return None
