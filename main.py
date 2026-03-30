from wechat_agent_sdk import WechatAgent
import os

# 从环境变量读取配置，这样最安全，不用写死在代码里
api_key = os.getenv("sk-rQG7HCouVlc9Tt8gC16864C1B1A94b8a9811956880D96a57")
base_url = os.getenv("https://aihubmix.com/v1")

bot = WechatAgent(api_key=api_key, base_url=base_url)

@bot.on_message()
def handle_message(message):
    print(f"收到消息: {message.content}")
    # 这里写你的逻辑
    return "已收到！"

if __name__ == "__main__":
    bot.run()