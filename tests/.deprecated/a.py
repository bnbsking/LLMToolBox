from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1️⃣ Define state structure
class GraphState(TypedDict, total=False):
    prompt: str
    code: str
    img_path: str
    error: str
    retry_count: int

# 2️⃣ Build graph
graph_builder = StateGraph(GraphState)

def generate_node(state: GraphState) -> GraphState:
    print("Generating code…")
    code = "print('hello world')"  # placeholder
    return {**state, "code": code}

def execute_node(state: GraphState) -> GraphState:
    print("Executing code…")
    try:
        exec(state["code"])
        img_path = "/tmp/output.png"
        return {**state, "img_path": img_path, "error": None}
    except Exception as e:
        import traceback
        return {**state, "error": traceback.format_exc()}

def fix_node(state: GraphState) -> GraphState:
    print("Fixing code…")
    if state.get("error"):
        new_code = "print('fixed version')"
        return {
            **state,
            "code": new_code,
            "retry_count": state.get("retry_count", 0) + 1,
        }
    return state

# 3️⃣ Add nodes
graph_builder.add_node("generate", generate_node)
graph_builder.add_node("execute", execute_node)
graph_builder.add_node("fix", fix_node)

# 4️⃣ Add edges
graph_builder.add_edge(START, "generate")
graph_builder.add_edge("generate", "execute")

def decide_next(state: GraphState) -> str:
    if state.get("error"):
        if state.get("retry_count", 0) < 2:
            return "fix"
        else:
            return END
    return END

graph_builder.add_conditional_edges("execute", decide_next,
                                    path_map={"fix": "fix", END: END})
    # if execute returns fix, go to fix; else end
graph_builder.add_edge("fix", "execute")

# 5️⃣ Compile the graph (this is the key step)
graph = graph_builder.compile()
graph_image = graph.get_graph().draw_mermaid_png()
with open("/app/tests/.deprecated/graph.png", "wb") as f:
    f.write(graph_image)

# 6️⃣ Run the graph
initial_state: GraphState = {"prompt": "Draw a cat chart"}
result = graph.invoke(initial_state)

print("\n✅ Final result:", result)

