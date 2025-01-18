import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    BitsAndBytesConfig,
)
from threading import Thread


class LLM_chat:
    def __init__(self):
        # bnb_config = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_use_double_quant=True,
        #     bnb_4bit_quant_type="nf4",
        #     bnb_4bit_compute_dtype=torch.float16,  # Set compute type here
        # )
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            # quantization_config=bnb_config,
            trust_remote_code=True,
            device_map="auto",
            torch_dtype="auto",
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
        system_role = None
        for message in messages:
            print(message)
            if message.get("role", "") == "system":
                system_role = message.get("content")
                break

        input_prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        print(input_prompt)
        input_prompt = (
            f"<s><s><|system|>{system_role}<|end|>{input_prompt.replace('<s>', '')}"
            if system_role
            else input_prompt
        )
        print(input_prompt)

        input_ids = self.tokenizer(input_prompt, return_tensors="pt")

        streamer = TextIteratorStreamer(self.tokenizer)

        generation_kwargs = dict(
            inputs=input_ids["input_ids"].to("cuda"),
            streamer=streamer,
            temperature=0.0,
            max_new_tokens=1024,
        )

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for answer in streamer:
            if answer.startswith("<|"):
                continue
            yield answer
