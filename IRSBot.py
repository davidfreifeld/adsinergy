import os
# from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# env_path = Path(__file__).resolve().parent / ".env"
# loaded = load_dotenv(env_path)
loaded = load_dotenv()

# api_key = os.environ["OPENAI_API_KEY"]  # or os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
client = OpenAI()

# # # 1) Create a vector store
# vector_store = client.vector_stores.create(name="irs-reg-docs")

# # find regulatory pdfs
# file_paths = []
# path = "./docs/"
# for name in os.listdir(path):
#     full = os.path.join(path, name)
#     if os.path.isfile(full):
#         file_paths.append(full)

# file_streams = [open(p, "rb") for p in file_paths]

# client.vector_stores.file_batches.upload_and_poll(
#     vector_store_id = vector_store.id,
#     files=file_streams,
# )

first_vector_store_id = client.vector_stores.list().data[0].id
print(first_vector_store_id)

# response = client.responses.create(
#     model="gpt-5",
#     input="Give me all the information about plans with 26 or fewer participants.",
#     # tools=[
#     #     {
#     #         "type": "file_search",
#     #         "vector_store_ids": [first_vector_store_id]
#     #     }
#     # ]
# )

# print(response.output_text)