import json

class SimpleAIPipeline:
    def __init__(self, max_tokens=100):
        self.max_tokens = max_tokens
        self.history = []

    def process_input(self, user_prompt):
        # Step 1: Simple prompt cleaning
        cleaned_prompt = user_prompt.strip()
        # Step 2: Validate input length
        if len(cleaned_prompt) > self.max_tokens:
            raise ValueError("Prompt exceeds maximum token limit!")
        # Step 3: Store the query in the pipeline's temporary memory
        response_data = {"status": "success", "echo": cleaned_prompt}
        self.history.append(response_data)
        return response_data

    def get_average_prompt_length(self):
        # Step 4: Calculate the average length of previous prompts in history
        total_length = sum([len(item["echo"]) for item in self.history])
        return total_length / len(self.history)
        # <-- Think: what's the hidden engineering issue here if history is empty?

# Test run
pipeline = SimpleAIPipeline(max_tokens=50)
print(pipeline.process_input("Hello AI, optimize this code."))

# Try calculating the average before adding anything,
# or in a specific edge case...
# print(pipeline.get_average_prompt_length())
