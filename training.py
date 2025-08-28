from voyager import Voyager
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import AIMessage
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
import copy
import os
import re

mc_port = 25565
if "VOYAGER_MC_PORT" in os.environ:
    mc_port = os.environ["VOYAGER_MC_PORT"]


if "OPENAI_API_MODEL" in os.environ:
    model = os.environ["OPENAPI_API_MODEL"]
else:
    model = "meta-llama/llama-3.1-405b-instruct:free"


if "OPENAI_API_BASE" not in os.environ:
    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1" #openrouter
    # os.environ["OPENAI_API_BASE"] = "http://localhost:12434/engines/llama.cpp/v1" #locally hosting llama
    # os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1" #locally hosting vllm


debug_print = "VOYAGER_DEBUG_PRINT" in os.environ

thinking_pattern = r"<think>.*<\/think>\n?\n?";
def llm_invoker(llm, in_messages, retries = 3):
    try:
        if debug_print:
            print(f"=====================================SENT TO AI=====================================")
            print(str(in_messages))
        messages = copy.deepcopy(in_messages)
        result = llm.invoke(messages)
        
        if debug_print:
            print(f"=====================FINAL RESULT=====================")
            print(result.content)
            print(f"=====================================END OF AI=====================================")
        
        result.content = re.sub(thinking_pattern, "", result.content,flags=re.DOTALL) # dirty fix for some hosters which keep the reasoning text in the content
        
        return result
    except Exception as e:
        print(f"LLM ERROR {e}")
        print(f"{retries} RETRIES LEFT")
        if retries==0:
            print(f"NO RETRIES LEFT, RETURNING EMPTY")
            return AIMessage("")
        return llm_invoker(llm, in_messages, retries-1)

def llm_preprocesser(llm):
    return llm

request_timeout = 300 #model request_timeout


# embedding_function = HuggingFaceEndpointEmbeddings( # huggingface example
#     model="http://localhost:8080", # if you're using Text Embeddings Interface locally, set it to the url
#     huggingfacehub_api_token="", # not needed if running locally
#     request_timeout=request_timeout,
# )
# embedding_function = OpenAIEmbeddings(
#     base_url = "http://localhost:8080/v1", # currently using llamacpp
#     model="", #unused if llamacpp
#     request_timeout=request_timeout,
# )
embedding_function = HuggingFaceEndpointEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",
    provider="nebius",
    # huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"]
)

# use_pre_planning_prompt is to decide if it uses _no_pre_planning prompts (in voyager/prompts)
# originally made for possibly switching between reasoning and non reasoning models, in the theory that
# reasoning models shouldn't need to be pre-prompted to write out plans

voyager = Voyager(
    mc_port=mc_port,
    
    action_agent_model=llm_preprocesser(ChatOpenAI(
        model=model,
        request_timeout=request_timeout,
    )),
    action_agent_use_pre_planning_prompt = True,
    
    curriculum_agent_qa_model=llm_preprocesser(ChatOpenAI(
        model=model,
        request_timeout=request_timeout,
    )),
    curriculum_agent_qa_use_pre_planning_prompt = True,
    
    curriculum_agent_model=llm_preprocesser(ChatOpenAI(
        model=model,
        request_timeout=request_timeout,
    )),
    curriculum_agent_use_pre_planning_prompt = True,
    
    critic_agent_model=llm_preprocesser(ChatOpenAI(
        model=model,
        request_timeout=request_timeout,
    )),
    critic_agent_use_pre_planning_prompt = True,
    
    skill_manager_model=llm_preprocesser(ChatOpenAI(
        model=model,
        request_timeout=request_timeout,
    )),
    skill_manager_use_pre_planning_prompt = True,
    
    curriculum_agent_embedding_function=embedding_function,
    skill_manager_embedding_function=embedding_function,
    llm_invoker=llm_invoker,
    resume=False, #set to True if you're resuming from a checkpoint, if an error occurs during startup when it's False, you may want to try removing the ckpt folder
)

# start lifelong learning
voyager.learn()
