import time
import logging
from mlc_llm import MLCEngine
from mlc_llm.serve.config import EngineConfig
from prompt import system_prompt

logging.basicConfig(
    filename="chat_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s"
)

model = "HF://mlc-ai/Llama-3-8B-Instruct-q0f16-MLC"
engine_config = EngineConfig(prefill_chunk_size=2800)
engine = MLCEngine(model)

conversation_history = [{"role": "system", "content": system_prompt}]

while True:
    print("*" * 100)
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    conversation_history.append({"role": "user", "content": user_input})

    start_time = time.time()
    response_text = ""
    first_token = False
    first_token_time = None
    for response in engine.chat.completions.create(
        messages=conversation_history,
        model=model,
        stream=True,
    ):

        for choice in response.choices:
            if not first_token:
                time_taken = (time.time() - start_time) * 1000
                first_token = True
                first_token_time = time_taken

            print(choice.delta.content, end="", flush=True)
            response_text += choice.delta.content

    with open("chat_log.txt", "a") as f:
        f.write(f"Response {response_text[:5]}, Time: {first_token_time:.2f} ms\n")
        # start_time = None
    print("\n")

    conversation_history.append({"role": "assistant", "content": response_text})

engine.terminate()
