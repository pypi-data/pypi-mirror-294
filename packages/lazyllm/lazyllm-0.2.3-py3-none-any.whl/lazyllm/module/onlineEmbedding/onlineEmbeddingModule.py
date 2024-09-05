from typing import Any, Dict

import lazyllm
from .openaiEmbed import OpenAIEmbedding
from .glmEmbed import GLMEmbedding
from .sensenovaEmbed import SenseNovaEmbedding
from .qwenEmbed import QwenEmbedding
from .onlineEmbeddingModuleBase import OnlineEmbeddingModuleBase

class __EmbedModuleMeta(type):

    def __instancecheck__(self, __instance: Any) -> bool:
        if isinstance(__instance, OnlineEmbeddingModuleBase):
            return True
        return super().__instancecheck__(__instance)


class OnlineEmbeddingModule(metaclass=__EmbedModuleMeta):
    """Used to manage and create online Embedding service modules currently on the market, currently supporting openai, sensenova, glm, qwen.

Args:
    source (str): Specify the type of module to create. Options are  ``openai`` /  ``sensenova`` /  ``glm`` /  ``qwen``.
    embed_url (str): Specify the base link of the platform to be accessed. The default is the official link.
    embed_mode_name (str): Specify the model to access, default is ``text-embedding-ada-002(openai)`` / ``nova-embedding-stable(sensenova)`` / ``embedding-2(glm)`` / ``text-embedding-v1(qwen)`` 


Examples:
    >>> import lazyllm
    >>> m = lazyllm.OnlineEmbeddingModule(source="sensenova")
    >>> emb = m("hello world")
    >>> print(f"emb: {emb}")
    emb: [0.0010528564, 0.0063285828, 0.0049476624, -0.012008667, ..., -0.009124756, 0.0032043457, -0.051696777]
    """
    MODELS = {'openai': OpenAIEmbedding,
              'sensenova': SenseNovaEmbedding,
              'glm': GLMEmbedding,
              'qwen': QwenEmbedding}

    @staticmethod
    def _encapsulate_parameters(embed_url: str,
                                embed_model_name: str) -> Dict[str, Any]:
        params = {}
        if embed_url is not None:
            params["embed_url"] = embed_url
        if embed_model_name is not None:
            params["embed_model_name"] = embed_model_name
        return params

    def __new__(self,
                source: str = None,
                embed_url: str = None,
                embed_model_name: str = None):
        params = OnlineEmbeddingModule._encapsulate_parameters(embed_url, embed_model_name)

        if source is None:
            for source in OnlineEmbeddingModule.MODELS.keys():
                if lazyllm.config[f'{source}_api_key']: break
            else:
                raise KeyError(f"No api_key is configured for any of the models {OnlineEmbeddingModule.MODELS.keys()}.")

        assert source in OnlineEmbeddingModule.MODELS.keys(), f"Unsupported source: {source}"
        return OnlineEmbeddingModule.MODELS[source](**params)
