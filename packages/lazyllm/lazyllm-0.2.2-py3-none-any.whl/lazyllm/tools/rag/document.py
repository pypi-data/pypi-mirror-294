from functools import partial
import os

from typing import Callable
import lazyllm
from lazyllm import ModuleBase, ServerModule

from .web import DocWebModule
from .doc_manager import DocManager
from .group_doc import DocGroupImpl
from .store import LAZY_ROOT_NAME


class Document(ModuleBase):
    """Initialize a document module with an optional user interface.

This constructor initializes a document module that can have an optional user interface. If the user interface is enabled, it also provides a UI to manage the document operation interface and offers a web page for user interface interaction.

Args:
    dataset_path (str): The path to the dataset directory. This directory should contain the documents to be managed by the document module.
    embed: The object used to generate document embeddings.
    create_ui (bool, optional): A flag indicating whether to create a user interface for the document module. Defaults to True.
    launcher (optional): An object or function responsible for launching the server module. If not provided, the default asynchronous launcher from `lazyllm.launchers` is used (`sync=False`).


Examples:
    >>> import lazyllm
    >>> from lazyllm.tools import Document
    >>> m = lazyllm.OnlineEmbeddingModule(source="glm")
    >>> documents = Document(dataset_path='your_doc_path', embed=m, create_ui=False)
    """
    def __init__(self, dataset_path: str, embed, create_ui: bool = True, launcher=None):
        super().__init__()
        if not os.path.exists(dataset_path):
            defatult_path = os.path.join(lazyllm.config["data_path"], dataset_path)
            if os.path.exists(defatult_path):
                dataset_path = defatult_path
        self._create_ui = create_ui
        launcher = launcher if launcher else lazyllm.launchers.remote(sync=False)

        if create_ui:
            self._impl = DocGroupImpl(dataset_path=dataset_path, embed=embed)
            doc_manager = DocManager(self._impl)
            self.doc_server = ServerModule(doc_manager, launcher=launcher)

            self.web = DocWebModule(doc_server=self.doc_server)
        else:
            self._impl = DocGroupImpl(dataset_path=dataset_path, embed=embed)

    def forward(self, func_name: str, *args, **kwargs):
        if self._create_ui:
            kwargs["func_name"] = func_name
            return self.doc_server.forward(*args, **kwargs)
        else:
            return getattr(self._impl, func_name)(*args, **kwargs)

    def find_parent(self, group: str) -> Callable:
        """
Find the parent node of the specified node.

Args:
    group (str): The name of the node for which to find the parent.


Examples:
    
    >>> import lazyllm
    >>> from lazyllm.tools import Document, SentenceSplitter
    >>> m = lazyllm.OnlineEmbeddingModule(source="glm")
    >>> documents = Document(dataset_path='your_doc_path', embed=m, create_ui=False)
    >>> documents.create_node_group(name="parent", transform=SentenceSplitter, chunk_size=1024, chunk_overlap=100)
    >>> documents.create_node_group(name="children", transform=SentenceSplitter, parent="parent", chunk_size=1024, chunk_overlap=100)
    >>> documents.find_parent('children')
    """
        return partial(self.forward, "find_parent", group=group)

    def find_children(self, group: str) -> Callable:
        """
Find the child nodes of the specified node.

Args:
    group (str): The name of the node for which to find the children.


Examples:
    
    >>> import lazyllm
    >>> from lazyllm.tools import Document, SentenceSplitter
    >>> m = lazyllm.OnlineEmbeddingModule(source="glm")
    >>> documents = Document(dataset_path='your_doc_path', embed=m, create_ui=False)
    >>> documents.create_node_group(name="parent", transform=SentenceSplitter, chunk_size=1024, chunk_overlap=100)
    >>> documents.create_node_group(name="children", transform=SentenceSplitter, parent="parent", chunk_size=1024, chunk_overlap=100)
    >>> documents.find_children('parent')
    """
        return partial(self.forward, "find_children", group=group)

    def __repr__(self):
        return lazyllm.make_repr("Module", "Document", create_ui=self._create_ui)

    def create_node_group(
        self, name: str, transform: Callable, parent: str = LAZY_ROOT_NAME, **kwargs
    ) -> None:
        """
Generate a node group produced by the specified rule.

Args:
    name (str): The name of the node group.
    transform (Callable): The transformation rule that converts a node into a node group. The function prototype is `(DocNode, group_name, **kwargs) -> List[DocNode]`. Currently built-in options include [SentenceSplitter][lazyllm.tools.SentenceSplitter], and users can define their own transformation rules.
    parent (str): The node that needs further transformation. The series of new nodes obtained after transformation will be child nodes of this parent node. If not specified, the transformation starts from the root node.
    kwargs: Parameters related to the specific implementation.


Examples:
    
    >>> import lazyllm
    >>> from lazyllm.tools import Document, SentenceSplitter
    >>> m = lazyllm.OnlineEmbeddingModule(source="glm")
    >>> documents = Document(dataset_path='your_doc_path', embed=m, create_ui=False)
    >>> documents.create_node_group(name="sentences", transform=SentenceSplitter, chunk_size=1024, chunk_overlap=100)
    """
        self._impl.create_node_group(name, transform, parent, **kwargs)
