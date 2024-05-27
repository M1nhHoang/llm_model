import queue
import threading

from threading import Semaphore
from llama_cpp import Llama


class LLM_chat:
    def __init__(self):
        self.llm = Llama(
            model_path="model/PhoGPT-4B-Chat-Q4_K_M.gguf",
            n_ctx=8192,
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
        """
        Hàm này chuyển đổi danh sách các dictionaries thành chuỗi chat có định dạng:
        <|role|>content<|end|>
        """

        chat_string = ""
        for message in messages:
            content = message["content"]
            chat_string += f"### Câu hỏi:{content}\n"  # Thêm xuống dòng để dễ đọc
        return chat_string + "### Trả lời:"

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
