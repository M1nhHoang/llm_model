import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    AutoConfig,
)
from threading import Thread


class LLM_chat:
    def __init__(self):
        model_path = "vinai/PhoGPT-4B-Chat"
        config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
        config.init_device = "cuda"
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            config=config,
            torch_dtype=torch.float16,
            trust_remote_code=True,
            cache_dir="model/",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, trust_remote_code=True, cache_dir="model/"
        )

        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")
        print("======== Init Done ========")

    def generate(self, text):
        messages = [
            {"role": "user", "content": f"{text}"},
        ]
        input_prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        input_ids = self.tokenizer(input_prompt, return_tensors="pt")

        outputs = self.model.generate(
            inputs=input_ids["input_ids"].to("cuda"),
            attention_mask=input_ids["attention_mask"].to("cuda"),
            max_new_tokens=50,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
        )

        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        response = response.split("### Trả lời:")[1]

        return response

    def generate_stream(self, text, chat_template):
        messages = [{"role": "user", "content": f"{chat_template} {text}"}]
        input_prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        input_ids = self.tokenizer(input_prompt, return_tensors="pt")

        streamer = TextIteratorStreamer(self.tokenizer)

        generation_kwargs = dict(
            inputs=input_ids["input_ids"].to("cuda"),
            streamer=streamer,
            max_new_tokens=250,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
        )

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for answer in streamer:
            if "###" in answer:
                continue
            yield answer.replace("lời:", "")
