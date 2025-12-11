import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class Model:
    def __init__(self, model_name="Qwen/Qwen2.5-0.5B-Instruct"):
        self.nomemodelo = model_name
        self.hardware = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def carregarmodelo(self):
        tokenizer = AutoTokenizer.from_pretrained(self.nomemodelo)

        model = AutoModelForCausalLM.from_pretrained(
            self.nomemodelo,
            dtype=torch.float32,
            device_map=self.hardware
        )

        return tokenizer, model

    def gerarsaida(self, model, tokenizer, prompt: str):
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        inputs = tokenizer(prompt, return_tensors="pt").to(self.hardware)

        output = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.eos_token_id,
        )

        resposta = tokenizer.decode(output[0], skip_special_tokens=False)

        if "<|im_start|>assistant" in resposta:
            resposta = resposta.split("<|im_start|>assistant", 1)[1].strip()

        resposta = resposta.replace("<|im_end|>", "").strip()

        return resposta





