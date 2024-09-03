import lazyllm
from typing import Any, Dict
from .openaiModule import OpenAIModule
from .glmModule import GLMModule
from .kimiModule import KimiModule
from .sensenovaModule import SenseNovaModule
from .qwenModule import QwenModule
from .doubaoModule import DoubaoModule
from .onlineChatModuleBase import OnlineChatModuleBase

class _ChatModuleMeta(type):

    def __instancecheck__(self, __instance: Any) -> bool:
        if isinstance(__instance, OnlineChatModuleBase):
            return True
        return super().__instancecheck__(__instance)


class OnlineChatModule(metaclass=_ChatModuleMeta):
    """Used to manage and create access modules for large model platforms currently available on the market. Currently, it supports openai, sensenova, glm, kimi, qwen and doubao (since the platform is not currently being developed for individual users, access is not currently supported). For how to obtain the platform's API key, please visit [Getting Started](/#platform)

Args:
    model (str): Specify the model to access, default is ``gpt-3.5-turbo(openai)`` / ``SenseChat-5(sensenova)`` / ``glm-4(glm)`` / ``moonshot-v1-8k(kimi)`` / ``qwen-plus(qwen)`` .
    source (str): Specify the type of module to create. Options include  ``openai`` /  ``sensenova`` /  ``glm`` /  ``kimi`` /  ``qwen`` / ``doubao (not yet supported)`` .
    base_url (str): Specify the base link of the platform to be accessed. The default is the official link.
    system_prompt (str): Specify the requested system prompt. The default is the official system prompt.
    stream (bool): Whether to request and output in streaming mode, default is streaming.
    return_trace (bool): Whether to record the results in trace, default is False.      


Examples:
    >>> import lazyllm
    >>> m = lazyllm.OnlineChatModule(source="sensenova", stream=True)
    >>> query = "Hello!"
    >>> resp = m(query)
    >>> for r in resp:
    ...     print(r)
    ...
    {'content': '你好'}
    {'content': '！'}
    {'content': '有什么'}
    {'content': '我可以'}
    {'content': '帮助'}
    {'content': '你的'}
    {'content': '吗'}
    {'content': '？'}
    {'content': ''}
    >>> m = lazyllm.OnlineChatModule(source="sensenova", model="nova-ptc-s-v2", stream=False)
    >>> train_file = "toy_chat_fine_tuning.jsonl"
    >>> m.set_train_tasks(train_file=train_file, upload_url="https://file.sensenova.cn/v1/files")
    >>> m._get_train_tasks()
    Num examples:
    First example:
    {'role': 'system', 'content': 'Marv is a factual chatbot that is also sarcastic.'}
    {'role': 'user', 'content': "What's the capital of France?"}
    {'role': 'assistant', 'content': "Paris, as if everyone doesn't know that already."}
    No errors found
    train file id: 7193d9a3-8b6e-4332-99cc-724dec75d9dd
    toy_chat_fine_tuning.jsonl upload success! file id is d632e591-f668-43a1-b5bf-49418e9c0fec
    fine tuning job ft-85f7bc96034441f2b64f9a5fff5d5b9c created, status: SUBMITTED
    fine tuning job ft-85f7bc96034441f2b64f9a5fff5d5b9c status: RUNNING
    ...
    fine tuning job ft-85f7bc96034441f2b64f9a5fff5d5b9c status: SUCCEEDED
    fine tuned model: nova-ptc-s-v2:ft-fee492082cbe4a6d880d396f34f1bc50 finished  
    >>> m._get_deploy_tasks()
    deployment c5aaf3bf-ef9b-4797-8c15-12ff04ed5372 created, status: SUBMITTED
    ...
    deployment c5aaf3bf-ef9b-4797-8c15-12ff04ed5372 status: PENDING
    ...
    deployment c5aaf3bf-ef9b-4797-8c15-12ff04ed5372 status: RUNNING
    deployment c5aaf3bf-ef9b-4797-8c15-12ff04ed5372 finished
    """
    MODELS = {'openai': OpenAIModule,
              'sensenova': SenseNovaModule,
              'glm': GLMModule,
              'kimi': KimiModule,
              'qwen': QwenModule,
              'doubao': DoubaoModule}

    @staticmethod
    def _encapsulate_parameters(base_url: str,
                                model: str,
                                stream: bool,
                                return_trace: bool,
                                **kwargs) -> Dict[str, Any]:
        params = {"stream": stream, "return_trace": return_trace}
        if base_url is not None:
            params['base_url'] = base_url
        if model is not None:
            params['model'] = model
        params.update(kwargs)

        return params

    def __new__(self,
                model: str = None,
                source: str = None,
                base_url: str = None,
                stream: bool = True,
                return_trace: bool = False,
                **kwargs):
        if model in OnlineChatModule.MODELS.keys() and source is None: source, model = model, source

        params = OnlineChatModule._encapsulate_parameters(base_url, model, stream, return_trace, **kwargs)

        if source is None:
            for source in OnlineChatModule.MODELS.keys():
                if lazyllm.config[f'{source}_api_key']: break
            else:
                raise KeyError(f"No api_key is configured for any of the models {OnlineChatModule.MODELS.keys()}.")

        assert source in OnlineChatModule.MODELS.keys(), f"Unsupported source: {source}"
        return OnlineChatModule.MODELS[source](**params)
