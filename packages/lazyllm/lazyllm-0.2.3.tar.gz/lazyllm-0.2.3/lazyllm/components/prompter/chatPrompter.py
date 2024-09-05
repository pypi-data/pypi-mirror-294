from typing import List, Union, Optional, Dict
from .builtinPrompt import LazyLLMPrompterBase

class ChatPrompter(LazyLLMPrompterBase):
    """chat prompt, supports tool calls and historical dialogue.

Args:
    instruction (Option[str]): Task instructions for the large model, with 0 to multiple fillable slot, represented by ``{}``. For user instructions, you can pass a dictionary with fields ``user`` and ``system``.
    extro_keys (Option[List]): Additional fields that will be filled with user input.
    show (bool): Flag indicating whether to print the generated Prompt, default is False.

**Examples:**

```python
>>> from lazyllm import ChatPrompter
>>> p = ChatPrompter('hello world')
>>> p.generate_prompt('this is my input')
'<|start_system|>You are an AI-Agent developed by LazyLLM.hello world\\n\\n<|end_system|>\\n\\n\\n<|Human|>:\\nthis is my input\\n<|Assistant|>:\\n'
>>> p.generate_prompt('this is my input', return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\nhello world\\n\\n'}, {'role': 'user', 'content': 'this is my input'}]}
>>>
>>> p = ChatPrompter('hello world {instruction}', extro_keys=['knowledge'])
>>> p.generate_prompt(dict(instruction='this is my ins', input='this is my inp', knowledge='LazyLLM-Knowledge'))
'<|start_system|>You are an AI-Agent developed by LazyLLM.hello world this is my ins\\nHere are some extra messages you can referred to:\\n\\n### knowledge:\\nLazyLLM-Knowledge\\n\\n\\n<|end_system|>\\n\\n\\n<|Human|>:\\nthis is my inp\\n<|Assistant|>:\\n'
>>> p.generate_prompt(dict(instruction='this is my ins', input='this is my inp', knowledge='LazyLLM-Knowledge'), return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\nhello world this is my ins\\nHere are some extra messages you can referred to:\\n\\n### knowledge:\\nLazyLLM-Knowledge\\n\\n\\n'}, {'role': 'user', 'content': 'this is my inp'}]}
>>> p.generate_prompt(dict(instruction='this is my ins', input='this is my inp', knowledge='LazyLLM-Knowledge'), history=[['s1', 'e1'], ['s2', 'e2']])
'<|start_system|>You are an AI-Agent developed by LazyLLM.hello world this is my ins\\nHere are some extra messages you can referred to:\\n\\n### knowledge:\\nLazyLLM-Knowledge\\n\\n\\n<|end_system|>\\n\\n<|Human|>:s1<|Assistant|>:e1<|Human|>:s2<|Assistant|>:e2\\n<|Human|>:\\nthis is my inp\\n<|Assistant|>:\\n'
>>>
>>> p = ChatPrompter(dict(system="hello world", user="this is user instruction {input} "))
>>> p.generate_prompt(dict(input="my input", query="this is user query"))
'<|start_system|>You are an AI-Agent developed by LazyLLM.hello world\\n\\n<|end_system|>\\n\\n\\n<|Human|>:\\nthis is user instruction my input this is user query\\n<|Assistant|>:\\n'
>>> p.generate_prompt(dict(input="my input", query="this is user query"), return_dict=True)
{'messages': [{'role': 'system', 'content': 'You are an AI-Agent developed by LazyLLM.\\nhello world\\n\\n'}, {'role': 'user', 'content': 'this is user instruction my input this is user query'}]}
```
<span style="font-size: 20px;">**`generate_prompt(input: str | Dict[str, str] | None = None, history: List[List[str] | Dict[str, Any]] | None = None, tools: List[Dict[str, Any]] | None = None, label: str | None = None, *, show: bool = False, return_dict: bool = False)→ str | Dict `**</span>

Based on the user's input, generate the corresponding Prompt.

Args:
    instruction (Option[str]): Task instructionspecify the ``system`` and ``user`` instructions.

    extro_keys (Option[List]): Additional fields that will be filled with user input.

    show (bool): Flag indicating whether to print the generated Prompt, default is False.

    tools (Option[list]): Tool-set which is provived for LLMs, default is None.



<span style="font-size: 20px;">**`get_response(output: str, input: str | None = None)→ str`**</span>

Used to truncate the Prompt, only retaining valuable outputs.

Args:
    output (str) :The output of the large model
    input (Optional[str]) :The input to the large model. If this parameter is specified, the function will truncate any part of the output that contains the input. Default is None.                

"""
    def __init__(self, instruction: Union[None, str, Dict[str, str]] = None,
                 extro_keys: Union[None, List[str]] = None, show: bool = False, tools: Optional[List] = None):
        super(__class__, self).__init__(show, tools=tools)
        if isinstance(instruction, dict):
            splice_instruction = instruction.get("system", "") + \
                ChatPrompter.ISA + instruction.get("user", "") + ChatPrompter.ISE
            instruction = splice_instruction
        instruction_template = f'{instruction}\n{{extro_keys}}\n'.replace(
            '{extro_keys}', LazyLLMPrompterBase._get_extro_key_template(extro_keys)) if instruction else ""
        self._init_prompt("{sos}{system}{instruction}{tools}{eos}\n\n{history}\n{soh}\n{user}{input}\n{eoh}{soa}\n",
                          instruction_template)

    @property
    def _split(self): return self._soa if self._soa else None
