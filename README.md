# ChangJiang_YuKeTang

用于在长江雨课堂网页端中辅助完成课程页面轮询、题目识别与自动作答的 Python 脚本集合。

## 功能概览

- 使用 Selenium 打开课程页面并进入在学课程（`onlesson`）
- 每 30 秒检查一次 PPT 时间轴是否翻页
- 识别题目图片并调用本地 OCR 服务提取文字
- 调用 DeepSeek 接口生成选择题/填空题/主观题答案
- 自动填写选项或输入框并提交

## 环境要求

- Python 3.10+
- Microsoft Edge 浏览器
- 与浏览器版本匹配的 `msedgedriver`
- Umi-OCR（本项目通过本地 HTTP 接口 `http://127.0.0.1:1224/api/ocr` 调用）

相关下载地址：

- Umi-OCR：`https://github.com/hiroi-sora/Umi-OCR`
- Edge WebDriver：`https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads`

## 如何查看 Edge 浏览器版本

可使用以下任一方式：

1. 打开 Edge，访问：`edge://settings/help`
2. 或点击「设置」→「关于 Microsoft Edge」

记录主版本号（例如 `134.x.x.x` 中的 `134`），下载与之匹配主版本的 Edge WebDriver。

## 安装依赖

项目已提供 `requirements.txt`，推荐使用以下命令安装：

```bash
pip install -r requirements.txt
```

## 配置说明

编辑根目录下 `config.json`：

```json
{
  "lesson": "Java软件开发（混合式）",
  "deepseek_api": "",
  "ocr_path": "D:\\Umi-OCR\\Umi-OCR_Paddle_v2.1.5\\Umi-OCR.exe",
  "edge_driver_path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe",
  "duration": 95
}
```

字段说明：

- `lesson`：课程名（当前代码实际通过 `.onlesson` 元素进入课程，此字段暂未直接用于定位课程卡片）
- `deepseek_api`：DeepSeek API Key
- `ocr_path`：Umi-OCR 可执行文件路径
- `edge_driver_path`：EdgeDriver 路径
- `duration`：运行时长（分钟）

## 使用方法

1. 启动命令：

   ```bash
   python main.py
   ```

2. 程序会自动打开雨课堂网页并提示扫码登录：
   - 登录完成后，回到终端按 `Enter`
3. 程序进入课程后开始循环检查与自动答题
4. 到达 `duration` 指定时长后结束并退出浏览器

## 文件说明

- `main.py`：程序入口、课程进入逻辑、循环调度
- `answer_question.py`：题型识别与自动作答逻辑
- `click_ppt.py`：定位并点击最新 PPT 时间轴项
- `image.py`：题图链接提取与下载
- `ocr.py`：OCR 请求与本地 OCR 进程管理
- `deepseek.py`：DeepSeek API 调用
- `driver.py`：Edge WebDriver 初始化
- `config.py` / `config.json`：配置读取与配置文件

## 注意事项

- 本项目依赖页面结构（CSS 选择器），雨课堂页面改版后可能失效。
- `config.json` 中路径示例为 Windows 路径，请按本机环境调整。
- 请妥善保管 API Key，不要提交到公开仓库。
