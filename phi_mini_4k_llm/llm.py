import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
)
from threading import Thread


class LLM_chat:
    def __init__(self):
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

    def generate_stream(self, messages):
        input_prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        input_ids = self.tokenizer(input_prompt, return_tensors="pt")

        streamer = TextIteratorStreamer(self.tokenizer)

        generation_kwargs = dict(
            inputs=input_ids["input_ids"].to("cuda"),
            streamer=streamer,
            temperature=0.0,
            max_new_tokens=1000,
        )

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for answer in streamer:
            if answer.startswith("<|"):
                continue
            yield answer
