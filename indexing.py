from llama_index.core import SimpleDirectoryReader, set_global_tokenizer, VectorStoreIndex, Settings
from transformers import AutoTokenizer
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

from llama_index.embeddings.huggingface_optimum import OptimumEmbedding

import os
from llama_index.core import StorageContext, load_index_from_storage


documents=SimpleDirectoryReader("data").load_data()
print("doc loaded successfully")

# set_global_tokenizer(
#     AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf").encode
# )


if not os.path.exists("store/embedding"):
   OptimumEmbedding.create_and_save_optimum_model(
    "sentence-transformers/all-mpnet-base-v2", "store/embedding"
    )
Settings.embed_model = OptimumEmbedding(folder_name="store/embedding")
print("embedded")

llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([llama_debug])


def load_or_create_index(documents):

    storage_dir = "store/index"  # Customize storage directory if needed

    if not os.path.exists(storage_dir):
        # Create the storage directory if it doesn't exist
        os.makedirs(storage_dir)

    try:
        # Attempt to load the index from storage
        storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
        index = load_index_from_storage(storage_context)
        print("Index loaded successfully from storage.")
        return index
    except FileNotFoundError:
        # If the index isn't found, create a new one and save it
        print("Index not found. Creating a new index and saving it for future use.")
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=storage_dir)
        return index
    
index = load_or_create_index(documents)

