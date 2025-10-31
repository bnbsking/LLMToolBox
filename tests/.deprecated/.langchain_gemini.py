from langchain_core.runnables import Runnable

from .google_gemini import GoogleGeminiChatAPI


class LangChainGeminiChatAPI(GoogleGeminiChatAPI, Runnable):
    def invoke(self, input: dict, config = None) -> dict:
        self.run(
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


# class LangChainGeminiChatAPI(BaseAPI):
#     def __init__(
#             self,
#             api_key: str,
#             model_name: str,
#             price_csv_path: str = "/app/ragentools/api_calls/price_gemini.csv"
#         ):
#         super().__init__(api_key, model_name, price_csv_path)

#     def run(
#             self,
#             prompt: Union[str, List],
#             response_format: Type[BaseModel],
#             temperature: float = 0.7,
#             retry_times: int = 3,
#         ) -> dict:
#         prompt = PromptTemplate(template=prompt)
#         model = ChatGoogleGenerativeAI(
#             model=self.model_name,
#             temperature=temperature,
#             max_retries=retry_times,
#             google_api_key=self.api_key
#         )
#         prompt_and_model = prompt | model
#         parser = PydanticOutputParser(pydantic_object=response_format)

#         output = prompt_and_model.invoke({})
#         self.update_acc_tokens(
#             input_tokens=output.usage_metadata["input_tokens"],
#             output_tokens=output.usage_metadata["output_tokens"]
#         )
#         output = parser.invoke(output)
#         return output.dict()

#     # async def arun(
#     #         self,
#     #         prompt: Union[str, List],
#     #         response_format: Type[BaseModel],
#     #         temperature: float = 0.7,
#     #         retry_times: int = 3,
#     #     ) -> dict:
#     #     prompt = PromptTemplate(template=prompt)
#     #     model = ChatGoogleGenerativeAI(
#     #         model=self.model_name,
#     #         temperature=temperature,
#     #         max_retries=retry_times,
#     #         google_api_key=self.api_key
#     #     )
#     #     prompt_and_model = prompt | model
#     #     parser = PydanticOutputParser(pydantic_object=response_format)

#     #     output = await prompt_and_model.ainvoke({})
#     #     self.update_acc_tokens(
#     #         input_tokens=output.usage_metadata["input_tokens"],
#     #         output_tokens=output.usage_metadata["output_tokens"]
#     #     )
#     #     output = await parser.invoke(output)
#     #     return output.dict()

#     async def arun(
#         self,
#         prompt: Union[str, List],
#         response_format: Type[BaseModel],
#         temperature: float = 0.7,
#         retry_times: int = 3,
#     ) -> dict:
#         model = ChatGoogleGenerativeAI(
#             model=self.model_name,
#             temperature=temperature,
#             max_retries=retry_times,
#             google_api_key=self.api_key,
#         )

#         # ✅ construct HumanMessage
#         if isinstance(prompt, str):
#             content = [{"type": "text", "text": prompt}]
#         elif isinstance(prompt, list):
#             content = prompt
#         else:
#             raise TypeError("`prompt` must be str or list of content dicts")

#         message = HumanMessage(content=content)

#         # ✅ call model asynchronously
#         output = await model.ainvoke([message])
#         self.update_acc_tokens(
#             input_tokens=output.usage_metadata["input_tokens"],
#             output_tokens=output.usage_metadata["output_tokens"],
#         )

#         # ✅ structured output parsing
#         parser = PydanticOutputParser(pydantic_object=response_format)
#         parsed_output = parser.invoke(output)  # synchronous parse is fine
#         return parsed_output.dict()
