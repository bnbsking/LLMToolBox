from langchain_core.runnables import Runnable

from .google_gemini import GoogleGeminiChatAPI


class LangChainGeminiChatAPI(GoogleGeminiChatAPI, Runnable):
    """
    Base on benifits of GoogleGeminiChatAPI,
    also allow scalabilty and `blackboard design pattern` with LangChain.
    Args:
        node_key (str): The key in the global state dict that contains this node's input data.
                        Only this sub-dictionary will be read/written by the node.
        output_key (str): The key within the node's sub-dictionary where the API result will be stored.
    """
    def __init__(
            self,
            api_key: str,
            model_name: str,
            price_csv_path: str = "/app/llmtoolbox/api_calls/price_gemini.csv",
            node_key: str = "default",
            output_key: str = "result"
        ):
        super().__init__(api_key, model_name, price_csv_path)
        self.node_key = node_key
        self.output_key = output_key

    def invoke(self, state: dict, config = None) -> dict:
        node_state = state[self.node_key]
        out = self.run(
            prompt=node_state["prompt"],
            response_format=node_state["response_format"],
            temperature=node_state.get("temperature", 0.7),
            retry_times=node_state.get("retry_times", 3),
            retry_sec=node_state.get("retry_sec", 5)
        )
        state[self.node_key][self.output_key] = out
        return state

    async def ainvoke(self, state: dict, config= None) -> dict:
        node_state = state[self.node_key]
        out = await self.arun(
            prompt=node_state["prompt"],
            response_format=node_state["response_format"],
            temperature=node_state.get("temperature", 0.7),
            retry_times=node_state.get("retry_times", 3),
            retry_sec=node_state.get("retry_sec", 5),
        )
        state[self.node_key][self.output_key] = out
        return state
