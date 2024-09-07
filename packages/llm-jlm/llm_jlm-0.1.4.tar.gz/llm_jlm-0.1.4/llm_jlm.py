import llm
import tlid

@llm.hookimpl
def register_models(register):
    register(JLM())
    
class JLM(llm.Model):
    model_id = "jlm"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #print("JLM.Cls.__init__")

    def execute(self, prompt, **kwargs):
        #print("JLM.execute")
        #print(prompt)
        #print(prompt.__dict__)
        """
Prompt(prompt='Hey hey', model=<Model 'jlm'>, system=None, prompt_json=None, options=Options())
{'prompt': 'Hey hey', 'model': <Model 'jlm'>, 'system': None, 'prompt_json': None, 'options': Options()}
Error: 'Prompt' object is not iterable
"""     
        prompt_str = prompt.prompt
        # Simple echo model that returns the prompt as the response
        return prompt_str + " from JLM"
    # def execute(self, prompt, stream, response, conversation):
    #     return ["hello world"]



