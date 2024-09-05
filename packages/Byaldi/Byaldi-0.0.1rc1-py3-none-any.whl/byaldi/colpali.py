import os
import srsly
import pickle
from typing import Optional, Union, List
from pathlib import Path
import torch
from PIL import Image
from pdf2image import convert_from_path
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoProcessor
from colpali_engine.models.paligemma_colbert_architecture import ColPali
from colpali_engine.trainer.retrieval_evaluator import CustomEvaluator
from colpali_engine.utils.colpali_processing_utils import (
    process_images,
    process_queries,
)
from byaldi.objects import Result


MOCK_IMAGE = Image.new("RGB", (448, 448), (255, 255, 255))


class ColPaliModel:
    def __init__(
        self,
        pretrained_model_name_or_path: Union[str, Path],
        n_gpu: int = -1,
        index_name: Optional[str] = None,
        verbose: int = 1,
        load_from_index: bool = False,
        index_root: str = ".byaldi",
        device: Optional[Union[str, torch.device]] = None,
        **kwargs,
    ):
        if "colpali" not in pretrained_model_name_or_path.lower():
            raise ValueError(
                "This pre-release version of Byaldi only supports ColPali for now. Incorrect model name specified."
            )

        self.pretrained_model_name_or_path = pretrained_model_name_or_path
        self.n_gpu = torch.cuda.device_count() if n_gpu == -1 else n_gpu
        self.index_name = index_name
        self.verbose = verbose
        self.load_from_index = load_from_index
        self.index_root = index_root
        self.kwargs = kwargs
        self.collection = {}
        self.indexed_docs = []
        self.page_id_to_doc_id = {}

        self.model_name = "vidore/colpali"
        self.model = ColPali.from_pretrained(
            "google/paligemma-3b-mix-448",
            torch_dtype=torch.bfloat16,
            device_map="cuda"
            if device == "cuda"
            or (isinstance(device, torch.device) and device.type == "cuda")
            else None,
            token=kwargs.get("hf_token", None) or os.environ.get("HF_TOKEN"),
        ).eval()
        self.model.load_adapter(self.model_name)
        self.processor = AutoProcessor.from_pretrained(
            self.model_name,
            token=kwargs.get("hf_token", None) or os.environ.get("HF_TOKEN"),
        )
        self.device = device
        if device != "cuda" and not (
            isinstance(device, torch.device) and device.type == "cuda"
        ):
            self.model = self.model.to(device)

        if not load_from_index:
            self.full_document_collection = False
            self.highest_doc_id = -1
        else:
            index_path = Path(index_root) / Path(index_name)
            index_config = srsly.read_json(index_path / "index_config.json")
            self.full_document_collection = index_config.get(
                "full_document_collection", False
            )
            if self.full_document_collection:
                self.collection = {}
                collection_path = index_path / "collection"
                json_files = sorted(
                    collection_path.glob("*.json"), key=lambda x: int(x.stem)
                )

                for json_file in json_files:
                    loaded_data = srsly.read_json(json_file)
                    self.collection.update(loaded_data)

                if self.verbose > 0:
                    print(
                        "You are using in-memory collection. This means every image is stored in memory."
                    )
                    print(
                        "You might want to rethink this if you have a large collection!"
                    )
                    print(
                        f"Loaded {len(self.collection)} images from {len(json_files)} JSON files."
                    )

            self.highest_doc_id = max(self.indexed_docs)

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: Union[str, Path],
        n_gpu: int = -1,
        verbose: int = 1,
        device: Optional[Union[str, torch.device]] = None,
        **kwargs,
    ):
        return cls(
            pretrained_model_name_or_path=pretrained_model_name_or_path,
            n_gpu=n_gpu,
            verbose=verbose,
            load_from_index=False,
            device=device,
            **kwargs,
        )

    @classmethod
    def from_index(
        cls,
        index_path: Union[str, Path],
        n_gpu: int = -1,
        verbose: int = 1,
        device: Optional[Union[str, torch.device]] = None,
        **kwargs,
    ):
        index_path = Path(index_path)
        index_config = srsly.read_json(index_path / "index_config.json")

        instance = cls(
            pretrained_model_name_or_path=index_config["model_name"],
            n_gpu=n_gpu,
            index_name=index_path.name,
            verbose=verbose,
            load_from_index=True,
            index_root=str(index_path.parent),
            device=device,
            **kwargs,
        )

        return instance

    def _export_index(self):
        if self.index_name is None:
            raise ValueError("No index name specified. Cannot export.")

        index_path = Path(self.index_root) / Path(self.index_name)
        index_path.mkdir(parents=True, exist_ok=True)

        # Save embeddings
        with open(index_path / "embeddings.pkl", "wb") as f:
            pickle.dump(self.indexed_docs, f)

        # Save index config
        index_config = {
            "model_name": self.model_name,
            "full_document_collection": self.full_document_collection,
            "highest_doc_id": self.highest_doc_id,
        }
        srsly.write_json(index_path / "index_config.json", index_config)

        # Save page_id_to_doc_id mapping
        srsly.write_json(index_path / "page_id_to_doc_id.json", self.page_id_to_doc_id)

        # Save collection if using in-memory collection
        if self.full_document_collection:
            collection_path = index_path / "collection"
            collection_path.mkdir(exist_ok=True)
            for i in range(0, len(self.collection), 1000):
                chunk = dict(list(self.collection.items())[i : i + 1000])
                srsly.write_json(collection_path / f"{i}.json", chunk)

        if self.verbose > 0:
            print(f"Index exported to {index_path}")

    def index(
        self,
        input_path: Union[str, Path],
        index_name: Optional[str] = None,
        doc_ids: Optional[List[Union[str, int]]] = None,
        store_collection_with_index: bool = False,
    ):
        if (
            self.index_name is not None
            and index_name is None
            or self.index_name == index_name
        ):
            print(
                f"An index named {self.index_name} is already loaded.",
                "Use add_to_index() to add to it or search() to query it.",
                "Pass a new index_name to create a new index.",
                "Exiting indexing without doing aything...",
            )
            return None
        if index_name is None:
            raise ValueError("index_name must be specified to create a new index.")
        self.index_name = index_name

        input_path = Path(input_path)
        if not hasattr(self, "highest_doc_id"):
            self.highest_doc_id = -1

        if input_path.is_dir():
            items = list(input_path.iterdir())
            if doc_ids is not None and len(doc_ids) != len(items):
                raise ValueError(
                    f"Number of doc_ids ({len(doc_ids)}) does not match number of documents ({len(items)})"
                )
            for i, item in enumerate(items):
                print(f"Indexing file: {item}")
                doc_id = doc_ids[i] if doc_ids else self.highest_doc_id + 1
                self.add_to_index(item, store_collection_with_index, doc_id=doc_id)
        else:
            doc_id = doc_ids[0] if doc_ids else self.highest_doc_id + 1
            self.add_to_index(input_path, store_collection_with_index, doc_id=doc_id)

        self._export_index()

    def add_to_index(
        self,
        input_item: Union[str, Path, Image.Image],
        store_collection_with_index: bool,
        doc_id: Union[str, int],
    ):
        input_item = Path(input_item) if isinstance(input_item, str) else input_item

        if isinstance(input_item, Path):
            if input_item.is_dir():
                for item in input_item.iterdir():
                    self._add_to_index(item, store_collection_with_index, doc_id)
            elif input_item.suffix.lower() == ".pdf":
                images = convert_from_path(str(input_item))
                for i, image in enumerate(images):
                    self._add_to_index(
                        image, store_collection_with_index, doc_id, page_num=i + 1
                    )
            elif input_item.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp"]:
                image = Image.open(input_item)
                self._add_to_index(image, store_collection_with_index, doc_id)
            else:
                raise ValueError(f"Unsupported input type: {input_item.suffix}")
        elif isinstance(input_item, Image.Image):
            self._add_to_index(input_item, store_collection_with_index, doc_id)
        else:
            raise ValueError(f"Unsupported input type: {type(input_item)}")

    def _add_to_index(
        self,
        image: Image.Image,
        store_collection_with_index: bool,
        doc_id: Union[str, int],
        page_num: int = 1,
    ):
        if doc_id in [entry["doc_id"] for entry in self.page_id_to_doc_id.values()]:
            raise ValueError(f"Document ID {doc_id} already exists in the index")

        processed_image = process_images(self.processor, [image])

        # Generate embedding
        with torch.no_grad():
            processed_image = {k: v.to(self.device) for k, v in processed_image.items()}
            embedding = self.model(**processed_image)

        # Add to index
        page_id = len(self.indexed_docs)
        self.indexed_docs.append(embedding)
        self.page_id_to_doc_id[page_id] = {"doc_id": doc_id, "page": page_num}

        # Update highest_doc_id
        self.highest_doc_id = max(self.highest_doc_id, doc_id)

        if store_collection_with_index:
            import base64
            import io

            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            self.collection[page_id] = img_str

        if self.verbose > 0:
            print(f"Added page {page_num} of document {doc_id} to index.")

    def remove_from_index():
        raise NotImplementedError("This method is not implemented yet.")

    def search(
        self,
        query: Union[str, List[str]],
        k: int = 10,
        return_base64_results: Optional[bool] = None,
    ) -> Union[List[Result], List[List[Result]]]:
        # Set default value for return_base64_results if not provided
        if return_base64_results is None:
            return_base64_results = bool(self.collection)

        # Ensure k is not larger than the number of indexed documents
        k = min(k, len(self.indexed_docs))

        # Process query/queries
        if isinstance(query, str):
            queries = [query]
        else:
            queries = query

        results = []
        for q in queries:
            # Process query
            with torch.no_grad():
                batch_query = process_queries(self.processor, [q], MOCK_IMAGE)
                batch_query = {k: v.to(self.device) for k, v in batch_query.items()}
                embeddings_query = self.model(**batch_query)
                query_embedding = embeddings_query.to("cpu")

            # Compute scores
            retriever_evaluator = CustomEvaluator(is_multi_vector=True)
            scores = retriever_evaluator.evaluate([query_embedding], self.indexed_docs)

            # Get top k relevant pages
            top_pages = scores.argsort(axis=1)[0][-k:][::-1].tolist()

            # Create Result objects
            query_results = []
            for page_id in top_pages:
                doc_info = self.page_id_to_doc_id[page_id]
                result = Result(
                    doc_id=doc_info["doc_id"],
                    page_num=doc_info["page"],
                    score=float(scores[0][page_id]),
                    base64=self.collection.get(page_id)
                    if return_base64_results
                    else None,
                )
                query_results.append(result)

            results.append(query_results)

        return results[0] if isinstance(query, str) else results
