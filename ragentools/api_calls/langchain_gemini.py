from langchain_core.runnables import Runnable

from .google_gemini import GoogleGeminiChatAPI


class LangChainGeminiChatAPI(GoogleGeminiChatAPI, Runnable):
    """
    Base on benifits of GoogleGeminiChatAPI,
    also allow scalabilty with LangChain.
    """
    def invoke(self, input: dict, config = None) -> dict:
        return self.run(
            prompt=input["prompt"],
            response_format=input["response_format"],
            temperature=input.get("temperature", 0.7),
            retry_times=input.get("retry_times", 3),
            retry_sec=input.get("retry_sec", 5)
        )

    async def ainvoke(self, input: dict, config= None) -> dict:
        return await self.arun(
            prompt=input["prompt"],
            response_format=input["response_format"],
            temperature=input.get("temperature", 0.7),
            retry_times=input.get("retry_times", 3),
            retry_sec=input.get("retry_sec", 5),
        )
