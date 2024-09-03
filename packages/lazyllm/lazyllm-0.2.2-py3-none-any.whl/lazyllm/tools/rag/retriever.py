from lazyllm import ModuleBase, pipeline
from .store import DocNode
from typing import List


class Retriever(ModuleBase):
    """
Create a retrieval module for document querying and retrieval. This constructor initializes a retrieval module that configures the document retrieval process based on the specified similarity metric.

Args:
    doc: An instance of the document module.
    group_name: The name of the node group on which to perform the retrieval.
    similarity: The similarity function to use for setting up document retrieval. Defaults to 'dummy'. Candidates include ["bm25", "bm25_chinese", "cosine"].
    similarity_cut_off: Discard the document when the similarity is below the specified value.
    index: The type of index to use for document retrieval. Currently, only 'default' is supported.
    topk: The number of documents to retrieve with the highest similarity.
    similarity_kw: Additional parameters to pass to the similarity calculation function.

The `group_name` has three built-in splitting strategies, all of which use `SentenceSplitter` for splitting, with the difference being in the chunk size:

- CoarseChunk: Chunk size is 1024, with an overlap length of 100
- MediumChunk: Chunk size is 256, with an overlap length of 25
- FineChunk: Chunk size is 128, with an overlap length of 12


Examples:
    
    >>> import lazyllm
    >>> from lazyllm.tools import Retriever
    >>> from lazyllm.tools import Document
    >>> m = lazyllm.OnlineEmbeddingModule()
    >>> documents = Document(dataset_path='your_doc_path', embed=m, create_ui=False)
    >>> rm = Retriever(documents, group_name='CoarseChunk', similarity='bm25', similarity_cut_off=0.01, topk=6)
    >>> rm.start()
    >>> print(rm("query"))
    """
    __enable_request__ = False

    def __init__(
        self,
        doc: object,
        group_name: str,
        similarity: str = "dummy",
        similarity_cut_off: float = float("-inf"),
        index: str = "default",
        topk: int = 6,
        **kwargs,
    ):
        super().__init__()
        self.doc = doc
        self.group_name = group_name
        self.similarity = similarity  # similarity function str
        self.similarity_cut_off = similarity_cut_off
        self.index = index
        self.topk = topk
        self.similarity_kw = kwargs  # kw parameters

    def _get_post_process_tasks(self):
        return pipeline(lambda *a: self('Test Query'))

    def forward(self, query: str) -> List[DocNode]:
        return self.doc.forward(
            func_name="retrieve",
            query=query,
            group_name=self.group_name,
            similarity=self.similarity,
            similarity_cut_off=self.similarity_cut_off,
            index=self.index,
            topk=self.topk,
            similarity_kws=self.similarity_kw,
        )
