from transformers import GenerationConfig, AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify
import random, torch

'''
Pipelines are made of a TOKENIZER and a model
TOKENIZER: mapping raw textual input to token
MODEL: make predictions frokm the input


Frameworks have a .generate() method implemented.
Pytorch's generate() is implemented in GenerationMixin
.generate() method can be parameterized with a GenerationConfig class instance.

.generate() generates a sequence of token ids for models with a language
modeling head
'''

app = Flask(__name__)

torch.cuda.empty_cache()
torch.cuda.memory_summary(device=None, abbreviated=False)

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

generation_config = GenerationConfig(
    temperature=0.8,
    top_k = 50,
    top_p = 0.95,   # Use nucleus sampling (?)
    num_beams = 3,
    max_new_tokens = 512,
    early_stopping = True,
    do_sample=True,  # Sampling for randomness
    return_full_text = False,
)


model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    #device_map="cuda",
    torch_dtype="auto",
    trust_remote_code=True
)

seed = random.randint(0,2**32-1)
torch.manual_seed(seed)

system_prompt = '''
You are a coding companion and assistant designed to help with code autocompletion, suggestions, and explanations. Your goal is to provide accurate and efficient code suggestions based on the user's input. Here are some guidelines to follow:

1. **Language Proficiency**: Be proficient in the Python programming language.
2. **Context Awareness**: Use the context of the code provided to make relevant suggestions. Consider variable names, function definitions, and any comments provided by the user.
3. **Code Suggestions**: When the user starts typing a line of code, provide suggestions to complete the line or offer relevant snippets that might be useful.
4. **Best Practices**: Utilize  best coding practices and optimizations where applicable.

Example 1:

User:
```python
def fibonacci(n):

Assistant:
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

Example 2:

User:
def is_prime(n):

Assistant:

def is_prime(n):
    """Check if a number is a prime number."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

Example 3:

User:
def merge_sort(arr):

Assistant:
def merge_sort(arr):
    """Sort an array using merge sort algorithm."""
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
'''

inputs = [f"{system_prompt}"]
inputs = tokenizer(inputs, return_tensors='pt')
model.generate(**inputs, generation_config=generation_config)


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    input = data.get('text', '')
    if not input:
        return jsonify({'error':'No input provided'}), 400
    inputs = tokenizer([input], return_tensors='pt')
    outputs = model.generate(**inputs, generation_config=generation_config)
    output =  tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({'result': output})

