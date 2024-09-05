# CellGen PyPI Distribution
## CellGen: Computational Modelling of Cellular Responses to Diverse Perturbations Using Single-Cell RNA Sequencing

<p align='center'><img src='assets/Fig1_main.png' alt='Overview.' width='100%'> </p>

**Abstract**. Accurate prediction of cellular responses to perturbations in single-cell RNA sequencing (scRNA-seq) data is critical for advancing our understanding of complex biological processes and dis-ease mechanisms. Existing methods often struggle with generalization, particularly in out-of-sample (OOS) and out-of-distribution (OOD) scenarios, where the absence of curated cell type information or novel cell types presents significant challenges. To address these limitations, we developed a generative adversarial network (GAN)-based model called CellGen that integrates Feature-wise Linear Modulation (FiLM) layers and a modified multi-head attention mechanism to effectively model gene expression changes across diverse biological contexts. Our model excels in preserving the biological fidelity of gene expression distributions, maintaining robust gene-gene interactions, and accurately forecasting future cel-lular states, such as during the epithelial-to-mesenchymal transition (EMT). Benchmarking against state-of-the-art methods demonstrates its superior performance in both OOS and OOD predictions, without the need for cell type annotations. This study underscores the model's potential for robust and biologically relevant single-cell perturbation analysis, with implications for improving our understanding of dynamic cellular processes and disease progression.

For reproducing the result in the paper. Please refer to this [link](https://github.com/JinmiaoChenLab/CellGen)

## Installation of the dependency library:

We recommend to install the miniconda and then we can create the virtual environment

```conda create --name CellGen python=3.10```

Next, we recommend to install the [Pytorch](https://pytorch.org/get-started/locally/) GPU version as our model is a GPU based for training.

then all the rest of the dependency using pip installation

```conda activate CellGen```

```python -m pip install -r requirements.txt```

## Installation fo the CellGen model using pip

To be implementated
``` ```


## Citation for Dataset

**Out of sample and out of distribution Dataset:**
1. [Kang et al. "Multiplexed droplet single-cell RNA-sequencing using natural genetic variation." Nature Biotechnology volume 36, pages89–94 (2018)](https://www.nature.com/articles/nbt.4042)

**Time trajectory Dataset:**

2. [Paul I, Bolzan D, Youssef A, Gagnon KA et al. Parallelized multidimensional analytic framework applied to mammary epithelial cells uncovers regulatory principles in EMT. Nat Commun 2023 Feb 8;14(1):688.](https://pubmed.ncbi.nlm.nih.gov/36755019/)

## Follow us on our Github
[JinmiaoChenLab Github Repo](https://github.com/JinmiaoChenLab)
[Vathanak Github Repo](https://github.com/uddamvathanak)