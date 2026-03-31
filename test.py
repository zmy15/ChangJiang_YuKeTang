from click_ppt import click_ppt
from image import get_image_url
from driver import driver
from config import Config
from main import go_lesson

config = Config()
driver = driver(config).driver
driver.get("https://changjiang.yuketang.cn/web")
input("请扫码登录，完成后按enter继续...")
if go_lesson(driver, lesson=config.lesson):
    target_item = click_ppt(driver)
    get_image_url(target_item)
