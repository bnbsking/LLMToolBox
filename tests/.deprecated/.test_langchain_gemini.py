from pydantic import BaseModel
from typing import List
import yaml

from llmtoolbox.api_calls.langchain_gemini import LangChainGeminiChatAPI
from llmtoolbox.common.async_main import amain_wrapper
from llmtoolbox.common.formatting import get_response_model
from llmtoolbox.prompts import get_prompt_and_response_format


class TestLangChainGeminiChatAPI:
    @classmethod
    def setup_class(cls):
        api_key = yaml.safe_load(open("/app/tests/api_keys.yaml"))["GOOGLE_API_KEY"]
        cls.api = LangChainGeminiChatAPI(api_key=api_key, model_name="gemini-2.0-flash-lite")

    def test_run(self):
        prompt, response_format = get_prompt_and_response_format(
            prompt_path='/app/llmtoolbox/prompts/basic.yaml',
            response_process='model'
        )
        response = self.api.run(prompt=prompt, response_format=response_format)
        #
        assert isinstance(response, dict)
        print(response, self.api.get_price())
    
    def test_arun(self):
        response_format = get_response_model({"ans": {"type": "string"}})
        args_list = [
            {
                "prompt": "Explain the theory of relativity in simple terms.",
                "response_format": response_format
            },
            {
                "prompt": "What are the health benefits of regular exercise?",
                "response_format": response_format
            }
        ]
        results = amain_wrapper(self.api.arun, args_list)
        #
        for result in results:
            response_format(**result)
        print(results, self.api.get_price())
    
    def test_arun_img(self):
        response_format = get_response_model({"ans": {"type": "string"}})
        args_list = [
            {
                "prompt": [
                    {"type": "text", "text": "What's in this picture?"},
                    {"type": "image", "data": open("/app/tests/api_calls/dog.jpg", "rb").read()}
                ],
                "response_format": response_format
            },
        ]
        results = amain_wrapper(self.api.arun, args_list)
        #
        for result in results:
            response_format(**result)
        print(results, self.api.get_price())


if __name__ == "__main__":
    test_instance = TestLangChainGeminiChatAPI()
    test_instance.setup_class()
    test_instance.test_run()
    