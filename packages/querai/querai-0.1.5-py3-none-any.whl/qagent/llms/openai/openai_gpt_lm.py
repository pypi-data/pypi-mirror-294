import decouple
import openai

from ..base_lm import BaseLLM


class OpenAILM(BaseLLM):
    def __init__(
        self,
        api_key:str = None
    ) -> None:
        super().__init__()
        api_key = api_key or decouple.config('OPENAI_API_KEY')
        self.client = openai.OpenAI(api_key=api_key)
        print("OpenAI LLM initialized.")

    def generate(
        self,
        prompt: str,
        prompt_sys: str = ""
    ) -> str:

        resp = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            # model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt_sys},
                {"role": "user", "content": prompt}])

        first_choice = resp.choices[0]
        answer = first_choice.message.content
        # print(f"OpenAISays: {answer}\nPROMPT: {prompt}")
        return answer
