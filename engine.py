
from llama_index.core import Settings
from transformers import AutoTokenizer
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)
from llama_index.embeddings.huggingface_optimum import OptimumEmbedding
from langchain.prompts import PromptTemplate
from llama_index.core.memory import ChatMemoryBuffer

from indexing import index

print("executing...")



llm = LlamaCPP(
    model_url=None,
    model_path="model/llama-2-7b-chat.Q2_K.gguf",
    temperature=0.0,
    max_new_tokens=1024,
    
    # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=3900,  # note, this sets n_ctx in the model_kwargs below, so you don't need to pass it there.
    
    # kwargs to pass to __call__()
    generate_kwargs={},
    
    # transform inputs into Llama2 format
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)

print("llm build done")


Settings.chunk_size = 512
Settings.chunk_overlap = 20
Settings.llm = llm
Settings.embed_model = OptimumEmbedding(folder_name="store/embedding")
Settings.tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")

print("settings done")

# Build prompt
template = """User is a mentally tired person, who came to you for guidance as you are a mental health expert. Use the following pieces of context to answer the question. Answer must be short maximum of 100 words. If you can, wrap up the answer in 50 words or less only.
{context}
Question: {question}
Helpful Answer:"""
# PROMPT = PromptTemplate.from_template(template)
PROMPT=PromptTemplate(template=template, input_variables=["context", "question"])
print("prompt done")

memory = ChatMemoryBuffer.from_defaults()

chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=PROMPT
)

print("executed!!")