import json
import os
from typing import Callable, Dict, TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import Runnable
import yaml

from llmtoolbox.api_calls.langchain_gemini import LangChainGeminiChatAPI
from llmtoolbox.prompts import get_prompt_and_response_format


def get_query_generator(json_path: str):
    with open(json_path, "r") as f:
        data_dict = json.load(f)
    for data in data_dict:
        yield data["simple_instruction"], data["id"]


class Code2Plot(Runnable):
    def __init__(self, save_folder: str):
        os.makedirs(save_folder, exist_ok=True)
        self.save_folder = save_folder
        self.cnt = 0

    def _get_code(self, state: dict) -> str:
        # depends on previous node output structure
        return state.get("fix", "gen")["code"]

    def invoke(self, state: dict, config = None) -> dict:
        node_state = state["code2plot"]
 
        save_png_path = os.path.join(self.save_folder, f"{node_state['data_id']}.png")
        save_py_path = os.path.join(self.save_folder, f"{node_state['data_id']}.py")

        code = self._get_code(state)
        code = code.strip("```python").strip("```").strip("\n")
        code = code.replace("plt.show()", f"plt.savefig('{save_png_path}'); plt.close()")
        open(save_py_path, "w").write(code)
        try:
            exec(code)
            state["code2plot"] |= {"img_path": save_png_path, "error": None}
        except Exception as e:
            state["code2plot"] |= {"img_path": save_png_path, "error": str(e)}
        return state


def decide_fix_or_eval(state: dict) -> str:
    if state["code2plot"].get("error") and state.get("retry_count", 0) < 2:
        state["retry_count"] = state.get("retry_count", 0) + 1
        return "fix"  # go to fix node
    return "eval"


def decide_refine_or_end(state: dict) -> str:
    score = state["eval"]["score"]["score"]
    if score < 0.7 and state.get("refine_count", 0) < 2:
        state["refine_count"] = state.get("refine_count", 0) + 1
        return "refine"
    return END


class GraphState(TypedDict, total=False):
    pass


if __name__ == "__main__":
    cfg = yaml.safe_load(open("/app/agents/text2chart/v1/agents_text2chart_v1.yaml"))
    cfg_api = cfg["api"]
    cfg_pmt = cfg["prompts"]
    api_key = yaml.safe_load(open(cfg_api["api_key_path"]))[cfg_api["api_key_env"]]

    gen_node = LangChainGeminiChatAPI(
        api_key=api_key,
        model_name=cfg_api["model_name"],
        node_key="gen",
        output_key="code"
    )
    code2plot_node = Code2Plot(os.path.join(cfg["save_folder"], "code"))
    fix_node = LangChainGeminiChatAPI(
        api_key=api_key,
        model_name=cfg_api["model_name"],
        node_key="fix",
        output_key="code"
    )
    eval_node = LangChainGeminiChatAPI(
        api_key=api_key,
        model_name=cfg_api["model_name"],
        node_key="eval",
        output_key="score"
    )
    refine_node = LangChainGeminiChatAPI(
        api_key=api_key,
        model_name=cfg_api["model_name"],
        node_key="refine",
        output_key="code"
    )

    query_generator = get_query_generator(cfg["data_path"])
    gen_prompt, gen_response_format = get_prompt_and_response_format(cfg_pmt["gen_path"])
    fix_prompt, fix_response_format = get_prompt_and_response_format(cfg_pmt["fix_path"])
    eval_prompt, eval_response_format = get_prompt_and_response_format(cfg_pmt["eval_path"])
    refine_prompt, refine_response_format = get_prompt_and_response_format(cfg_pmt["refine_path"])

    graph_builder = StateGraph(GraphState)
    graph_builder.add_node("gen", gen_node)
    graph_builder.add_node("code2plot", code2plot_node)
    graph_builder.add_node("fix", fix_node)
    graph_builder.add_node("eval", eval_node)
    graph_builder.add_node("refine", refine_node)

    graph_builder.add_edge(START, "gen")
    graph_builder.add_edge("gen", "code2plot")
    graph_builder.add_conditional_edges("code2plot", decide_fix_or_eval,
                                    path_map={"fix": "fix", "eval": "eval"})
    graph_builder.add_edge("fix", "code2plot")
    graph_builder.add_edge("code2plot", "eval")
    graph_builder.add_conditional_edges("eval", decide_refine_or_end,
                                    path_map={"refine": "refine", END: END})
    graph_builder.add_edge("refine", "code2plot")

    graph = graph_builder.compile()

    graph_image = graph.get_graph().draw_mermaid_png()
    with open(f"{cfg['save_folder']}/graph.png", "wb") as f:
        f.write(graph_image)

    raise

    for query, data_id in query_generator:
        state = {
            "gen": {
                "prompt": gen_prompt.replace("{{ query }}", query),
                "response_format": gen_response_format,
            },
            "code2plot": {
                "data_id": data_id
            },
            "fix": {
                "prompt": fix_prompt.replace("{{ query }}", query),
                "response_format": fix_response_format
            },
            "eval": {
                "prompt": eval_prompt.replace("{{ query }}", query),
                "response_format": eval_response_format
            },
            "refine": {
                "prompt": refine_prompt.replace("{{ query }}", query),
                "response_format": refine_response_format
            }
        }
        share = graph.invoke(state)
        print(share)
        break
        
    