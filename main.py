import asyncio
import os

from wechat_agent_sdk import Agent, ChatRequest, ChatResponse, WeChatBot


class OpenAIAgent(Agent):
    """使用 OpenAI 兼容 API（如 aihubmix），通过环境变量配置。"""

    def __init__(self) -> None:
        self._conversations: dict[str, list[dict]] = {}

    async def on_start(self) -> None:
        from openai import AsyncOpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("请设置环境变量 OPENAI_API_KEY")

        base_url = os.environ.get("OPENAI_BASE_URL")  # 例如 https://aihubmix.com/v1
        kwargs: dict = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url

        self._client = AsyncOpenAI(**kwargs)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        history = self._conversations.setdefault(request.conversation_id, [])
        history.append({"role": "user", "content": request.text})

        model = os.environ.get("OPENAI_MODEL", "gpt-4o")
        resp = await self._client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "你是一个友好的AI助手。"}]
            + history[-20:],
        )
        reply = resp.choices[0].message.content or ""
        history.append({"role": "assistant", "content": reply})
        return ChatResponse(text=reply)


async def main() -> None:
    bot = WeChatBot(agent=OpenAIAgent())
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
