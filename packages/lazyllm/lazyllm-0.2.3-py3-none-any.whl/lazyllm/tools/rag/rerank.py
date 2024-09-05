from functools import lru_cache
from typing import Callable, List, Optional
from lazyllm import ModuleBase, config, LOG
from lazyllm.tools.rag.store import DocNode, MetadataMode
from lazyllm.components.utils.downloader import ModelManager
import numpy as np


class Reranker(ModuleBase):
    """Initializes a Rerank module for postprocessing and reranking of nodes (documents).
This constructor initializes a Reranker module that configures a reranking process based on a specified reranking type. It allows for the dynamic selection and instantiation of reranking kernels (algorithms) based on the type and provided keyword arguments.

Args:
    name: The type of reranker to be used for the postprocessing and reranking process. Defaults to 'Reranker'.
    kwargs: Additional keyword arguments that are passed to the reranker upon its instantiation.

**Detailed explanation of reranker types**

- Reranker: This registered reranking function instantiates a SentenceTransformerRerank reranker with a specified model and top_n parameter. It is designed to rerank nodes based on sentence transformer embeddings.

- KeywordFilter: This registered reranking function instantiates a KeywordNodePostprocessor with specified required and excluded keywords. It filters nodes based on the presence or absence of these keywords.


Examples:
    
    >>> import lazyllm
    >>> from lazyllm.tools import Document, Reranker, Retriever
    >>> m = lazyllm.OnlineEmbeddingModule()
    >>> documents = Document(dataset_path='rag_master', embed=m, create_ui=False)
    >>> retriever = Retriever(documents, group_name='CoarseChunk', similarity='bm25', similarity_cut_off=0.01, topk=6)
    >>> reranker = Reranker(name='ModuleReranker', model='bg-reranker-large', topk=1)
    >>> ppl = lazyllm.ActionModule(retriever, reranker)
    >>> ppl.start()
    >>> print(ppl("query"))
    """
    registered_reranker = dict()

    def __init__(self, name: str = "ModuleReranker", **kwargs) -> None:
        super().__init__()
        self.name = name
        self.kwargs = kwargs

    def forward(self, nodes: List[DocNode], query: str = "") -> List[DocNode]:
        results = self.registered_reranker[self.name](nodes, query=query, **self.kwargs)
        LOG.debug(f"Rerank use `{self.name}` and get nodes: {results}")
        return results

    @classmethod
    def register_reranker(
        cls: "Reranker", func: Optional[Callable] = None, batch: bool = False
    ):
        def decorator(f):
            def wrapper(nodes, **kwargs):
                if batch:
                    return f(nodes, **kwargs)
                else:
                    results = [f(node, **kwargs) for node in nodes]
                    return [result for result in results if result]

            cls.registered_reranker[f.__name__] = wrapper
            return wrapper

        return decorator(func) if func else decorator


@lru_cache(maxsize=None)
def get_nlp_and_matchers(language):
    import spacy
    from spacy.matcher import PhraseMatcher

    nlp = spacy.blank(language)
    required_matcher = PhraseMatcher(nlp.vocab)
    exclude_matcher = PhraseMatcher(nlp.vocab)
    return nlp, required_matcher, exclude_matcher


@Reranker.register_reranker
def KeywordFilter(
    node: DocNode,
    required_keys: List[str],
    exclude_keys: List[str],
    language: str = "en",
    **kwargs,
) -> Optional[DocNode]:
    nlp, required_matcher, exclude_matcher = get_nlp_and_matchers(language)
    if required_keys:
        required_matcher.add("RequiredKeywords", list(nlp.pipe(required_keys)))
    if exclude_keys:
        exclude_matcher.add("ExcludeKeywords", list(nlp.pipe(exclude_keys)))

    doc = nlp(node.get_text())
    if required_keys and not required_matcher(doc):
        return None
    if exclude_keys and exclude_matcher(doc):
        return None
    return node


@lru_cache(maxsize=None)
def get_cross_encoder_model(model_name: str):
    from sentence_transformers import CrossEncoder

    model = ModelManager(config["model_source"]).download(model_name)
    return CrossEncoder(model)


@Reranker.register_reranker(batch=True)
def ModuleReranker(
    nodes: List[DocNode], model: str, query: str, topk: int = -1, **kwargs
) -> List[DocNode]:
    if not nodes:
        return []
    cross_encoder = get_cross_encoder_model(model)
    query_pairs = [
        (query, node.get_text(metadata_mode=MetadataMode.EMBED)) for node in nodes
    ]
    scores = cross_encoder.predict(query_pairs)
    sorted_indices = np.argsort(scores)[::-1]  # Descending order
    if topk > 0:
        sorted_indices = sorted_indices[:topk]

    return [nodes[i] for i in sorted_indices]


# User-defined similarity decorator
def register_reranker(func=None, batch=False):
    return Reranker.register_reranker(func, batch)
