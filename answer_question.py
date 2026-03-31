import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from ocr import ocr
from deepseek import deepseek
from image import get_image_url, download_image


def get_question(driver, config, target_item) -> bool:
    """识别题目类型并调用相应的答题函数"""
    element1 = None
    element2 = None

    try:
        # 先检查更具体的元素（带 can 类的按钮）
        element2 = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".slide__shape.submit-btn.can"))
        )
        print("找到填空题/主观题作答按钮")
        empty_question(driver, element2, config, target_item)
        return True
    except TimeoutException:
        print("未找到 .slide__shape.submit-btn.can 元素")

    try:
        # 检查选择题按钮
        element1 = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".slide__shape.submit-btn"))
        )
        print("找到选择题作答区域")
        choose_question(driver, config, target_item)
        return True
    except TimeoutException:
        print("未找到 .slide__shape.submit-btn 元素")

    print("未找到任何可作答的题目")
    return False


def choose_question(driver, config, target_item) -> bool:
    """处理选择题"""
    try:
        img_url = get_image_url(target_item)
        image = download_image(img_url)
        question = ocr(image)
        print(f"识别到题目：\n{question}...")  # 只打印前50字符

        if "多选" in question:
            answer = deepseek(
                question + "\n这是多选题请回答多个选项（A,B,C,D）格式：答案为：",
                config
            )
        elif "单选" in question:
            answer = deepseek(
                question + "\n这是单选题请回答单个选项（A,B,C,D）,格式：答案为：",
                config
            )
        else:
            answer = deepseek(
                question + "\n这是选择题请回答选项（A,B,C,D）(如有多个答案请以,分割),格式：答案为：",
                config
            )
        print(f"AI 回答：{answer}")

        answer_list = answer.split('答案为：')[-1].strip().split(',')
        answer_list = [a.strip() for a in answer_list]  # 去除空格
        print(f"解析后的答案列表：{answer_list}")

        # 查找选项元素
        option_elements = driver.find_elements(By.CSS_SELECTOR, "p.options-label.MultipleChoice")
        if not option_elements:
            option_elements = driver.find_elements(By.XPATH, "//p[contains(@class, 'options-label')]")

        if not option_elements:
            print("❌ 未找到任何选项元素")
            return False

        # 构建选项字典
        options = {}
        for element in option_elements:
            option_value = element.get_attribute('data-option')
            if option_value:
                options[option_value] = element
                print(f"找到选项：{option_value}")

        # 点击答案
        for answer in answer_list:
            if answer in options:
                options[answer].click()
                print(f"✓ 已选择选项：{answer}")
            else:
                print(f"❌ 未找到选项：{answer}")

        # 提交答案
        final_submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".submit-btn"))
        )
        final_submit_btn.click()
        print("✓ 已提交选择题答案")
        return True

    except Exception as e:
        print(f"❌ 处理选择题时出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def empty_question(driver, element, config, target_item):
    """处理填空题/主观题"""
    try:
        # 点击作答按钮
        element.click()
        print("✓ 已点击作答按钮")
        time.sleep(2)

        # 获取题目
        img_url = get_image_url(target_item)
        image = download_image(img_url)
        question = ocr(image)
        print(f"识别到题目：\n{question}...")

        # 判断题目类型
        question_type = question.split("题")[0] if "题" in question else ""
        if "填空" in question_type:
            prompt = question + "\n这是填空题请回答文本(如有多个答案请以,分割),格式：答案为："
        elif "主观" in question_type:
            prompt = question + "\n这是主观题请回答文本,格式：答案为："
        else:
            prompt = question + "\n请回答(如有多个答案请以,分割),格式：答案为："

        answer = deepseek(prompt, config)
        print(f"AI 回答：{answer}")

        answer_list = answer.split('答案为：')[-1].strip().split(',')
        answer_list = [a.strip() for a in answer_list]  # 去除空格
        print(f"解析后的答案列表：{answer_list}")

        # 等待填空区域显示
        blanks_wrap = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "blanks__wrap"))
        )

        # 查找所有输入框
        blank_inputs = blanks_wrap.find_elements(By.CSS_SELECTOR, ".blank__input")
        print(f"找到 {len(blank_inputs)} 个填空题输入框")

        # 填写答案
        for i, input_box in enumerate(blank_inputs):
            if i >= len(answer_list):
                print(f"⚠ 警告：答案数量不足，第 {i + 1} 题无答案")
                break

            try:
                # 滚动到输入框
                driver.execute_script("arguments[0].scrollIntoView(true);", input_box)
                time.sleep(0.3)

                # 清空并输入答案
                input_box.clear()
                input_box.send_keys(answer_list[i])
                print(f"✓ 第 {i + 1} 题已输入答案: {answer_list[i]}")
                time.sleep(0.3)

            except Exception as e:
                print(f"❌ 第 {i + 1} 题输入失败: {e}")
                return False

        # 提交答案
        final_submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".blanks__wrap .submit-btn"))
        )
        final_submit_btn.click()
        print("✓ 已提交填空题/主观题答案")
        return True

    except Exception as e:
        print(f"❌ 处理填空题/主观题时出错: {e}")
        import traceback
        traceback.print_exc()
        return False
