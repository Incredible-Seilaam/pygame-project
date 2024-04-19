from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", device_map="auto", trust_remote_code=True)
prompt = input('Zadej prompt:')

# Code for generating output based on user input
with torch.no_grad():
    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    output_ids = model.generate(
        token_ids.to(model.device),
        max_new_tokens=40,
        do_sample=True,
        temperature=0.3
    )
output = tokenizer.decode(output_ids[0][token_ids.size(1):])
print(output)