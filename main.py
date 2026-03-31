import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from answer_question import get_question
from click_ppt import click_ppt
from ocr import managed_process
from config import Config
from driver import driver


def main(driver, config):
    start_time = time.time()
    total_duration = config.duration * 60  # 分钟转换为秒
    cycle_count = 0
    target_item = None
    print(f"程序开始执行，将持续{config.duration}分钟")

    while time.time() - start_time < total_duration:
        cycle_start = time.time()
        cycle_count += 1
        print(f"开始第 {cycle_count} 次循环")

        if target_item != click_ppt(driver):
            target_item = click_ppt(driver)
            get_question(driver, config, target_item)
        else:
            print("PPT未翻页跳过答题...")

        # 计算剩余等待时间
        elapsed = int(time.time() - cycle_start)
        wait_time = max(0, 30 - elapsed)  # 30秒检查一次

        print(f"第 {cycle_count} 次循环完成，耗时 {elapsed} 秒，等待 {wait_time} 秒")

        # 等待到下一个周期
        if wait_time > 0:
            time.sleep(wait_time)


def go_lesson(driver, lesson="就业指导") -> bool:
    try:
        # employment_course = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH, "//h1[contains(text(), " + lesson + ")]/ancestor::div[contains(@class, 'lesson-cardS')]"))
        # )
        # # 点击课程
        # employment_course.click()

        onlesson_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(driver.find_element(By.CLASS_NAME, "onlesson")))
        # 点击onlesson元素
        click_and_switch_to_new_window(driver, onlesson_element, timeout=10, close_old=False)

        # 等待课程页面加载
        time.sleep(5)

        print("成功点击")
        return True
    except Exception as e:
        print(f"发生错误: {e}")
        return False


def click_and_switch_to_new_window(driver, clickable, timeout=10, close_old=False):
    old_handles = driver.window_handles[:]  # 记录点击前的窗口
    clickable.click()
    # 等待新窗口出现
    WebDriverWait(driver, timeout).until(EC.new_window_is_opened(old_handles))
    # 找到新窗口句柄
    new_handle = next(h for h in driver.window_handles if h not in old_handles)
    # 切换到新窗口
    driver.switch_to.window(new_handle)
    # 等待新页面加载完成（也可以改成等待某个特定元素出现）
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    # 可选：关闭旧窗口们，只保留新窗口
    if close_old:
        for h in old_handles:
            try:
                driver.switch_to.window(h)
                driver.close()
            except Exception:
                pass
        driver.switch_to.window(new_handle)
    return new_handle


if __name__ == "__main__":
    config = Config()
    with managed_process(config.ocr_path) as process:
        driver = driver(config).driver
        driver.get("https://changjiang.yuketang.cn/web")
        input("请扫码登录，完成后按enter继续...")
        if go_lesson(driver, lesson=config.lesson):
            main(driver, config)
        driver.quit()
