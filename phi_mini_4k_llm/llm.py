import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
)
from threading import Thread


class LLM_chat:
    def __init__(self):
        torch.random.manual_seed(0)
        torch.set_default_tensor_type(torch.cuda.FloatTensor)

        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            device_map="auto",
            torch_dtype="auto",
            trust_remote_code=True,
            cache_dir="model/",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct", cache_dir="model/"
        )

        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")

    def generate_stream(self, text):
        encoded_input = self.tokenizer(
            [
                f"<|system|>You are a smart virtual assistant, please answer briefly and talk to me like a friend.<|end|>"
                f"<|user|>{text}<|end|><|assistant|>"
            ],
            return_tensors="pt",
        )

        streamer = TextIteratorStreamer(self.tokenizer)

        generation_kwargs = dict(
            encoded_input,
            streamer=streamer,
            max_new_tokens=250,
        )

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for answer in streamer:
            if answer.startswith("<|"):
                continue
            yield answer
