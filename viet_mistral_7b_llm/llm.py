import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    BitsAndBytesConfig,
)
from threading import Thread
from huggingface_hub import login


class LLM_chat:
    def __init__(self):
        login()  # push ur token here

        self.tokenizer = AutoTokenizer.from_pretrained("Viet-Mistral/Vistral-7B-Chat")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,  # Set compute type here
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "Viet-Mistral/Vistral-7B-Chat", quantization_config=bnb_config
        )

        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")

    def generate_stream(self, messages):
        input_ids = self.tokenizer.apply_chat_template(
            messages, return_tensors="pt"
        ).to(self.model.device)

        streamer = TextIteratorStreamer(self.tokenizer)

        generation_kwargs = dict(
            input_ids=input_ids,
            streamer=streamer,
            max_new_tokens=768,
            # do_sample=True,
            # top_p=0.95,
            # top_k=40,
            # temperature=0.1,
            # repetition_penalty=1.05,
        )

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for answer in streamer:
            print(answer)
            yield answer
