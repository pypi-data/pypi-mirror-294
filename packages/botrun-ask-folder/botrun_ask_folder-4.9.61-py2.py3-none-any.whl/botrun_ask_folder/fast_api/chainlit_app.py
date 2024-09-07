import chainlit as cl
from chainlit.input_widget import Select
from litellm import completion
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx
from typing import Optional, Dict
import httpx

load_dotenv()

# 設置全局變量
MAX_HISTORY_FOR_LLM = 10  # 設置發送給 LLM 的最大歷史記錄數量

# 模型配置
MODEL_CONFIGS = {
    "openai/gpt-4o-mini": {
        "model": "openai/gpt-4o-mini",
        "provider": "OpenAI",
        "max_tokens": 4096,  # 調整為 gpt-4o-mini 的最大 token 數
    },
    "gemini/gemini-1.5-pro": {
        "model": "gemini/gemini-1.5-pro",
        "provider": "Gemini",
        "max_tokens": 4096,
    },
    "anthropic/claude-3-sonnet-20240229": {
        "model": "anthropic/claude-3-sonnet-20240229",
        "provider": "Anthropic",
        "max_tokens": 4096,
    },
}


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    return default_user


@cl.on_chat_start
async def start():
    user = cl.user_session.get("user")
    if not user:
        await cl.Message(content="認證失敗。請先登錄").send()
        return

    cl.user_session.set("chat_history", [])
    cl.user_session.set("current_model", "openai/gpt-4o-mini")  # 默認使用 gpt-4o-mini
    cl.user_session.set("file_contents", {})

    # 創建模型選擇器
    settings = await cl.ChatSettings(
        [
            Select(
                id="model_selector",
                label="選擇模型",
                values=list(MODEL_CONFIGS.keys()),
                initial_index=list(MODEL_CONFIGS.keys()).index("openai/gpt-4o-mini"),
            )
        ]
    ).send()
    print(f"[chainlit_app.py] user: {user}")
    user_name = ""
    try:
        user_name = user.metadata.get("name", "")
    except:
        user_name = "您好"
    await cl.Message(
        content=(
            f"歡迎！請上傳文件或直接開始對話。"
            if user_name == ""
            else f"歡迎，{user_name}！請上傳文件或直接開始對話。"
        )
    ).send()


@cl.on_settings_update
async def setup_agent(settings):
    cl.user_session.set("current_model", settings["model_selector"])


@cl.on_message
async def main(message: cl.Message):
    file_contents = cl.user_session.get("file_contents", {})

    # 檢查是否有文件上傳
    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File):
                await handle_file_upload(element)

        if not message.content:
            return

    chat_history = cl.user_session.get("chat_history")
    current_model = cl.user_session.get("current_model")
    model_config = MODEL_CONFIGS[current_model]

    # 構建消息列表，只取最近的 MAX_HISTORY_FOR_LLM 條記錄用於發送給 LLM
    messages_for_llm = []
    for entry in chat_history[-MAX_HISTORY_FOR_LLM:]:
        messages_for_llm.append({"content": entry["user"], "role": "user"})
        messages_for_llm.append({"content": entry["assistant"], "role": "assistant"})

    if file_contents:
        combined_content = "\n\n".join(
            [f"文件 '{name}':\n{content}" for name, content in file_contents.items()]
        )
        messages_for_llm.append(
            {
                "content": f"以下是上傳的文件內容：\n\n{combined_content}\n\n請根據這些信息回答用戶的問題。",
                "role": "system",
            }
        )

    messages_for_llm.append({"content": message.content, "role": "user"})

    try:
        # 使用 litellm 進行對話，啟用流式回應
        response = completion(
            model=model_config["model"],
            messages=messages_for_llm,
            api_key=os.getenv(f"{current_model.upper()}_API_KEY"),
            stream=True,
            max_tokens=model_config["max_tokens"],  # 使用模型特定的 max_tokens
        )

        # 初始化流式回應
        msg = cl.Message(content="")
        await msg.send()

        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                await msg.stream_token(content)

        # 完成流式回應
        await msg.update()

        # 更新聊天歷史，保留所有記錄
        chat_history.append({"user": message.content, "assistant": full_response})
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        error_message = (
            f"🙇‍♂️ 發生了一些問題，請稍後再試或聯繫支援團隊。錯誤詳情：{str(e)}"
        )
        await cl.Message(content=error_message).send()


async def handle_file_upload(file: cl.File):
    content = ""
    if file.mime == "application/pdf":
        content = extract_text_from_pdf(file.path)
    elif (
        file.mime
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        content = extract_text_from_docx(file.path)
    elif file.mime == "text/plain":
        with open(file.path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        await cl.Message(content=f"不支持的文件類型: {file.mime}").send()
        return

    file_contents = cl.user_session.get("file_contents", {})
    file_contents[file.name] = content
    cl.user_session.set("file_contents", file_contents)
    await cl.Message(content=f"文件 '{file.name}' 已成功上傳和處理。").send()


def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
