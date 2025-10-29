from google import genai
import pandas as pd

from .base_api import BaseAPI
from google.genai.types import GenerateContentConfig
from tenacity import retry, stop_after_attempt, wait_fixed


class GoogleGeminiChatAPI(BaseAPI):
    def __init__(
            self,
            api_key: str,
            model_name: str,
            price_csv_path: str = "/app/llmtoolbox/api_calls/price_gemini.csv"
        ):
        super().__init__(api_key, model_name, price_csv_path)
        self.client = genai.Client(api_key=api_key)

    def run(self, prompt: str, response_format: dict, retry_times: int = 1, retry_sec: int = 10) -> dict:
        @retry(stop=stop_after_attempt(retry_times), wait=wait_fixed(retry_sec))
        def _call_api():
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "object",
                        "properties": response_format,
                    }
                )
            )
            self.update_acc_tokens(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count
            )
            return response.parsed
        return _call_api()

    async def arun(self, prompt: str, response_format: dict, retry_times: int = 1, retry_sec: int = 10) -> dict:
        @retry(stop=stop_after_attempt(retry_times), wait=wait_fixed(retry_sec))
        async def _call_api():
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "object",
                        "properties": response_format,
                    }
                )
            )
            self.update_acc_tokens(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count
            )
            return response.parsed
        return await _call_api()
    