from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time


def click_ppt(driver: webdriver) -> WebElement | None:
    try:
        # 使用正确的 CSS 选择器
        slide_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section.timeline__item.J_slide"))
        )

        if not slide_items:
            print("未找到任何幻灯片项目")
            return None

        # 找到最大 data-index
        max_index = -1
        max_index_element = None

        for item in slide_items:
            data_index = item.get_attribute("data-index")
            if data_index and data_index.isdigit():
                index_num = int(data_index)
                print(f"找到元素 data-index={index_num}")
                if index_num > max_index:
                    max_index = index_num
                    max_index_element = item

        if max_index_element:
            print(f"准备点击 data-index={max_index} 的元素")

            # 滚动到元素
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                max_index_element
            )
            time.sleep(0.5)

            # 点击元素
            try:
                max_index_element.click()
                print(f"✓ 成功点击 data-index={max_index}")
            except:
                driver.execute_script("arguments[0].click();", max_index_element)
                print(f"✓ 使用 JS 点击 data-index={max_index}")

            return max_index_element
        else:
            print("未找到有效的 data-index")
            return None

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None
