from pathlib import Path
from typing import Any, List, Optional, Union
from uuid import uuid4

from PIL import Image

from byaldi.colpali import ColPaliModel


class RAGMultiModalModel:
    """
    Wrapper class for a pretrained RAG multi-modal model, and all the associated utilities.
    Allows you to load a pretrained model from disk or from the hub, build or query an index.

    ## Usage

    Load a pre-trained checkpoint:

    ```python
    from byaldi import RAGMultiModalModel

    RAG = RAGMultiModalModel.from_pretrained("vidore/colpali")
    ```

    Both methods will load a fully initialised instance of ColPali, which you can use to build and query indexes.

    ```python
    RAG.search("How many people live in France?")
    ```
    """

    model: Optional[ColPaliModel] = None

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: Union[str, Path],
        device: str = "cuda",
    ):
        """Load a ColPali model from a pre-trained checkpoint.

        Parameters:
            pretrained_model_name_or_path (str): Local path or huggingface model name.
            device (str): The device to load the model on. Default is "cuda".

        Returns:
            cls (RAGMultiModalModel): The current instance of RAGMultiModalModel, with the model initialised.
        """
        instance = cls()
        instance.model = ColPaliModel.from_pretrained(
            pretrained_model_name_or_path, device=device
        )
        return instance

    @classmethod
    def from_index(cls, index_path: Union[str, Path], device: str = "cuda"):
        """Load an Index and the associated ColPali model from an existing document index.

        Parameters:
            index_path (Union[str, Path]): Path to the index.
            device (str): The device to load the model on. Default is "cuda".

        Returns:
            cls (RAGMultiModalModel): The current instance of RAGMultiModalModel, with the model and index initialised.
        """
        instance = cls()
        index_path = Path(index_path)
        instance.model = ColPaliModel.from_index(index_path, device=device)

        return instance

    def index(
        self,
        texts: List[str],
        images: List[Image.Image],
        index_name: str = "colpali_index",
    ):
        """Build an index from a list of texts and images.

        Parameters:
            texts (List[str]): The collection of texts to index.
            images (List[Image.Image]): The collection of images to index.
            index_name (str): The name of the index that will be built.

        Returns:
            None
        """
        self.model.index(texts, images, index_name)

    def add_to_index(
        self,
        input_item: Union[str, Path, Image.Image],
        store_collection_with_index: bool,
        doc_id: Union[str, int],
    ):
        """Add an item to an existing index.

        Parameters:
            input_item (Union[str, Path, Image.Image]): The item to add to the index.
            store_collection_with_index (bool): Whether to store the collection with the index.
            doc_id (Union[str, int]): The document ID for the item being added.

        Returns:
            None
        """
        self.model.add_to_index(input_item, store_collection_with_index, doc_id)

    def search(
        self,
        query: str,
        image: Optional[Image.Image] = None,
        k: int = 10,
        index_name: str = "colpali_index",
    ):
        """Query an index.

        Parameters:
            query (str): The query to search for.
            image (Optional[Image.Image]): An optional image to include in the query.
            k (int): The number of results to return.
            index_name (str): The name of the index to query.

        Returns:
            results (List[dict]): A list of dicts containing individual results.
        """
        return self.model.search(query, image, k, index_name)
