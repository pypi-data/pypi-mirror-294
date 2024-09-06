# Welcome to Byaldi
_Did you know? In the movie RAGatouille, the dish Remy makes is not actually a ratatouille, but a refined version of the dish called "Confit Byaldi"._

Byaldi is [RAGatouille](https://github.com/answerdotai/ragatouille)'s mini sister project. It is a simple wrapper around the [ColPali](https://github.com/illuin-tech/colpali) repository to make it easy to use late-interaction multi-modal models such as ColPALI with a familiar API.

## Getting started

First, a warning: This is a pre-release library, using uncompressed indexes and lacking other kinds of refinements. Eventually, we'll add an HNSW indexing mechanism, pooling, and, who knows, maybe 2-bit quantization?

IIt'll get updated as the multi-modal ecosystem develops further!

### Pre-requisites

#### ColPali access

ColPali is currently the only model of its kind. As it is based on PaliGemma, you will need to accept [Google's license agreement for PaliGemma on HuggingFace](https://huggingface.co/google/paligemma-3b-mix-448), and use your own HF token to download the model.

#### Poppler

To convert pdf to images with a friendly license, we use the `pdf2image` library. This library requires `poppler` to be installed on your system. Poppler is very easy to install by following the instructions [on their website](https://poppler.freedesktop.org/). The tl;dr is:

__MacOS with homebrew__

```bash
brew install poppler
```

__Debian/Ubuntu__

```bash
sudo apt-get install -y poppler-utils
```