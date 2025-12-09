import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from copy import deepcopy

class Model:
    def __init__(self, model_name="Qwen/Qwen2.5-1.5B-Instruct"):
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

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        )
        inputs = {k: v.to(self.hardware) for k, v in inputs.items()}

        config = deepcopy(model.generation_config)
        config.do_sample = False

        output = model.generate(
            **inputs,
            max_new_tokens=300
        )

        resposta = tokenizer.decode(output[0], skip_special_tokens=True)


        if resposta.startswith(prompt):
            resposta = resposta[len(prompt):].strip()

        return resposta




