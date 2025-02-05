# Use a pipeline as a high-level helper
from transformers import pipeline, AutoModel, AutoTokenizer, AutoModelForCausalLM

messages = [
    {"role": "user", "content": "Who are you?"},
]
model = AutoModelForCausalLM.from_pretrained(r'C:\Users\59483\.cache\huggingface\hub\models--deepseek-ai--DeepSeek-R1-Distill-Qwen-1.5B\snapshots\6393b7559e403fd1d80bfead361586fd6f630a4d')
tokenizer = AutoTokenizer.from_pretrained(r'C:\Users\59483\.cache\huggingface\hub\models--deepseek-ai--DeepSeek-R1-Distill-Qwen-1.5B\snapshots\6393b7559e403fd1d80bfead361586fd6f630a4d')
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
print(pipe(messages))