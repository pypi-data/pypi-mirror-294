class BaseLLM:
    def __init__(self):
        pass

    def generate(
        self,
        prompt: str,
        prompt_sys: str = ""
    ) -> str:
        print("DUMMY LLM RESPOMSE FOR TESTING ...")
        raw_text = '{"name": "John", "age": 30}'
        print(f"LLM uses prompt: {prompt}\nResponse: {raw_text}")
        return raw_text
