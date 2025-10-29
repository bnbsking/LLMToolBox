from pydantic import BaseModel
from typing import List
import yaml

from llmtoolbox.api_calls.google_gemini import GoogleGeminiChatAPI
from llmtoolbox.prompts import get_prompt_and_response_format
from llmtoolbox.api_calls.async_main import amain_wrapper


class Person(BaseModel):
    name: str
    age: int
    hobbies: List[str]


class Answer(BaseModel):
    ans: str


class TestGoogleGeminiChatAPI:
    @classmethod
    def setup_class(cls):
        api_key = yaml.safe_load(open("/app/tests/api_keys.yaml"))["GOOGLE_API_KEY"]
        cls.api = GoogleGeminiChatAPI(api_key=api_key, model_name="gemini-2.0-flash-lite")

    def test_run(self):
        prompt, response_format = get_prompt_and_response_format('/app/llmtoolbox/prompts/basic.yaml')
        response = self.api.run(prompt=prompt, response_format=response_format)
        try:
            out = Person(**response)
            print(out, self.api.get_price())
        except Exception as e:
            print(e)
            print(response)

    def test_arun(self):
        results = amain_wrapper(
            self.api.arun,
            [
                {"prompt": "Explain the theory of relativity in simple terms.", "response_format": {"ans": {"type": "string"}}},
                {"prompt": "What are the health benefits of regular exercise?", "response_format": {"ans": {"type": "string"}}}
            ]
        )
        for result in results:
            try:
                out = Answer(**result)
                print(out, self.api.get_price())
            except Exception as e:
                print(e)
                print(result)


if __name__ == "__main__":
    obj = TestGoogleGeminiChatAPI()
    obj.setup_class()
    obj.test_arun()
