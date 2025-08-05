import json
from typing import Literal

from faiss.contrib.exhaustive_search import apply_maxres
from langchain_core.messages import AIMessage
from langgraph.graph import END
from langgraph.types import Command

from app.agents import retriever_agent
from app.agents.llm import get_llm_by_type
from app.agents.retriever_agent import retriever_agent
from app.config.agents import AGENT_LLM_MAP
from app.graph.schema import GlobalState, Router
from app.prompts.template import apply_prompt_template

"""def amparo_node(state: GlobalState) -> Command[Literal["supervisor", "__end__"]]:
    print("Este es el mensaje que recibe Amparo: \n")
    print(state["messages"])

    # org. messages = [{"role": "system", "content": system_prompt_amparo}, ] + state["messages"]
    messages = apply_prompt_template("amparo", state)
    #org. response = llm.invoke(messages)
    response = get_llm_by_type(AGENT_LLM_MAP["amparo"]).invoke(messages)
    print("RESPUESTA RAW--:", response)
    print("INTENTA ENTRAR A TRY")
    try:
        print("ENTRA AL TRY")
        data = json.loads(response.content)  # Asegúrate que devuelva JSON
        print("ESTE ES EL JASON QUE DEVUELVE AMPARO", data)
        goto = data["next"]
        if goto == "FINISH":
            goto = END
            return Command(goto=goto,update={"messages": state["messages"] + [AIMessage(content=data["response"])],"task_completed": True  # ✅ esto faltaba
                }
            )
        return Command(goto=goto, update={"next": goto})
    except Exception as e:
        print("ERROR en JSON de Amparo:", e)
        return Command(goto=END, update={
            "messages": state["messages"] + [AIMessage(content="Disculpa, no pude procesar tu solicitud.")]})"""


def amparo_node(state: GlobalState) -> Command[Literal["supervisor", "__end__"]]:
    print("Este es el mensaje que recibe Amparo: \n")
    print(state["messages"])

    messages = apply_prompt_template("amparo", state)
    response = get_llm_by_type(AGENT_LLM_MAP["amparo"]).invoke(messages)

    print("RESPUESTA RAW--:", response)
    print("INTENTA ENTRAR A TRY")

    try:
        print("ENTRA AL TRY")
        data = json.loads(response.content)
        print("ESTE ES EL JSON QUE DEVUELVE AMPARO", data)

        goto = data["next"]
        print("ESTE ES GOTO ", goto)
        # amparo_reply = AIMessage(content=data["response"])
        # print("RESPUETA DE AMPARO ", [AIMessage(content=data["response"])])

        if goto == "FINISH":
            print("🟢 AMPARO FINALIZA EL FLUJO")
            # return Command(goto=END, update={"messages": state["messages"] + [amparo_reply], "task_completed": True})
            return Command(goto=goto, update={"messages": state["messages"] + [AIMessage(content=data["response"])],
                                              "task_completed": True})

        print(f"🔁 AMPARO DERIVA A: {goto}")
        return Command(goto=goto, update={"messages": state["messages"], "next": goto})

    except Exception as e:
        print("❌ ERROR en JSON de Amparo:", e)
        return Command(
            goto=END,
            update={
                "messages": state["messages"] + [AIMessage(content="Disculpa, no pude procesar tu solicitud.")],
                "task_completed": True
            }
        )


def supervisor_node(state: GlobalState) -> Command[Literal["consultas", "__end__"]]:
    print("Mensaje recibido por el supervisor: \n", state["messages"])
    # ✅ Si la tarea ya está resuelta, termina el flujo
    if state.get("task_completed") is True:
        print("✅ Tarea completada. Finalizando flujo.")
        return Command(goto=END)
    # org. messages = [{"role": "system", "content": system_prompt_supervisor}] + state["messages"]
    messages = apply_prompt_template("supervisor", state)
    try:
        # org. response = llm.with_structured_output(Router).invoke(messages)
        # response = get_llm_by_type(AGENT_LLM_MAP["supervisor"]).invoke(messages)
        llm = get_llm_by_type(AGENT_LLM_MAP["supervisor"])
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        print("Supervisor dirige a:", goto)
        if goto == "FINISH":
            goto = END
        return Command(goto=goto, update={"next": goto, "task_completed": True})
    except Exception as e:
        print("Error en la decisión del supervisor:", e)
        return Command(goto=END, update={
            "messages": state["messages"] + [AIMessage(content="No pude decidir a quién derivar tu solicitud.")],
            "task_completed": True})


def retriever_node(state: GlobalState) -> Command[Literal["supervisor", "__end__"]]:
    result = retriever_agent.invoke(state)
    return Command(
        goto="supervisor",
        update={
            "messages": result["messages"],
            "task_completed": True
        }
    )
