import queue
import threading

from threading import Semaphore
from llama_cpp import Llama
from huggingface_hub import login
from transformers import AutoTokenizer


class LLM_chat:
    def __init__(self):
        login("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")

        self.llm = Llama(
            model_path="model/ggml-vistral-7B-chat-q8.gguf",
            n_ctx=2048,
            n_gpu_layers=-1,
        )

        self.max_concurrent_requests = 1  # Giới hạn số request đồng thời
        self.request_semaphore = Semaphore(self.max_concurrent_requests)

        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")

    def _apply_chat_template(self, messages):
        prompt = "<s>[INST] <<SYS>>\n"

        for message in messages:
            if message["role"] == "system":
                prompt += f"{message['content']}\n"
            elif message["role"] == "user":
                prompt += f"{message['content']} [/INST]"
            elif message["role"] == "assistant":
                prompt += f"[INST] {message['content']} [/INST]"

        prompt += "\n<</SYS>>\n\n"
        return prompt

    def generate_stream(self, messages):
        output_queue = queue.Queue()

        def generate_thread(messages):  # Truyền messages vào hàm generate_thread
            with self.request_semaphore:
                for output in self.llm.create_completion(
                    self._apply_chat_template(messages),
                    max_tokens=1024,
                    stop=["<|end|>"],
                    stream=True,
                ):
                    output_queue.put(output["choices"][0]["text"])
                output_queue.put(None)

        thread = threading.Thread(
            target=generate_thread, args=(messages,)
        )  # Truyền messages khi khởi tạo luồng
        thread.start()

        while True:
            chunk = output_queue.get()
            if chunk is None:
                break
            yield chunk
