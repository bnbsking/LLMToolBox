from typing import List, Union

from google import genai
from google.genai.types import GenerateContentConfig
from tenacity import retry, stop_after_attempt, wait_fixed

from .base_api import BaseAPI


class GoogleGeminiChatAPI(BaseAPI):
    """
    This class wraps Google Gemini API calls which has:
    1 async, 2 retry, 3 token count with price, 4 pydantic response, 5 multi-modal input
    """
    def __init__(
            self,
            api_key: str,
            model_name: str,
            price_csv_path: str = "/app/ragentools/api_calls/prices.csv"
        ):
        super().__init__(api_key, model_name, price_csv_path)
        self.client = genai.Client(api_key=api_key)

    def run(
            self,
            prompt: Union[str, List],
            response_format: dict,
            temperature: float = 0.7,
            retry_times: int = 3,
            retry_sec: int = 5
        ) -> Union[str, dict]:
        @retry(stop=stop_after_attempt(retry_times), wait=wait_fixed(retry_sec))
        def _call_api():
            if response_format:
                cfg = GenerateContentConfig(
                        temperature=temperature,
                        response_mime_type="application/json",
                        response_schema={
                            "type": "object",
                            "properties": response_format,
                        }
                    )
            else:
                cfg = GenerateContentConfig(temperature=temperature)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=cfg
            )
            self.update_acc_tokens(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count
            )
            return response.parsed if response_format else response.text
        return _call_api()

    async def arun(
            self,
            prompt: Union[str, List],
            response_format: dict,
            temperature: float = 0.7,
            retry_times: int = 3,
            retry_sec: int = 5
        ) -> Union[str, dict]:
        @retry(stop=stop_after_attempt(retry_times), wait=wait_fixed(retry_sec))
        async def _call_api():
            if response_format:
                cfg = GenerateContentConfig(
                        temperature=temperature,
                        response_mime_type="application/json",
                        response_schema={
                            "type": "object",
                            "properties": response_format,
                        }
                    )
            else:
                cfg = GenerateContentConfig(temperature=temperature)
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=cfg
            )
            self.update_acc_tokens(
                input_tokens=response.usage_metadata.prompt_token_count,
                output_tokens=response.usage_metadata.candidates_token_count
            )
            return response.parsed if response_format else response.text
        return await _call_api()
        