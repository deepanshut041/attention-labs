# Attention Foundations — build and test basic attention

Build the basic single-head attention mechanisms from explicit tensor operations, explain the intermediate scores/weights/contexts, and test their numerical behavior, gradients, masks and training/evaluation differences. Run the same source and tests locally and in Google Colab Free.

**Status — 2026-10-30:** runnable project boilerplate and a Colab runner are prepared. Attention implementations and their correctness tests are the next work. The environment probe checks dependencies and autograd; it does not implement attention or establish hosted execution.

## Mechanisms to build

| Mechanism | Implementation goal | Required evidence |
| --- | --- | --- |
| Additive/Bahdanau | Learned query/key projections, nonlinear scorer and value mixture | Hand calculation, unequal source/query lengths and gradient checks |
| Dot product | Pairwise comparison and stable row normalization | Explicit scores/contexts; magnitude and negative-score cases |
| Scaled dot product | Scale by key width before normalization | Independent reference, width changes and numerical stability |
| Simplified self-attention | Query, key and value supplied by the same input | All rows and axes, symmetric-score/asymmetric-weight case |
| Projected self-attention | Separate learned Q/K/V and a task-loss update | Forward reference and input/parameter gradient comparisons |
| Causal single-head attention | Restrict each query to its available prefix | Shifted targets, zero forbidden weights and future-token intervention |

Padding validity, real zero inputs, all-masked rows, additive versus dot scoring, and attention dropout belong to the relevant mechanism checks. Use small synthetic inputs first; the three tutorial rows are provided as an input fixture. Add a separate genuine-zero/padding case without treating zero vectors as invalid automatically.

MHA and future GQA/MQA/MLA belong in the sibling [Attention Heads](../attention-heads/README.md). Positional Lecture 9 and a complete translation model are outside this project's scope.

## Read and build together

The [detailed tutorial](../../../docs/tutorials/projects/attention-labs/attention-foundations/v1/lessons/01-context-and-map.md) stays in the shared tutorial folder. It includes the original slides and original worked references. This project's source is the separate implementation we will build and test; the tutorial's executed examples do not count as implemented project mechanisms.

Follow this build route:

| Phase | Work | Exit |
| --- | --- | --- |
| 00 — Setup and source transfer | Locked environment, commands, tests and Colab source bundle | Local setup and notebook-cell checks; actual hosted run recorded separately |
| 01 — Query-dependent retrieval | Stable softmax and additive scoring | One complete numerical retrieval and independent gradients |
| 02 — Dot and scaled scoring | Replace the scorer while keeping the retrieval contract | Matched fixtures and dimensional scaling checks |
| 03 — Self-attention projections | Raw self-attention, Q/K/V and one small update | Full matrices, separate value width and checked derivatives |
| 04 — Visibility and dropout | Causal/padding masks, invalid support and train/eval behavior | Future invariance, mask edge cases and dropout expectation |
| 05 — Independent comparisons and Colab | Consolidated component suite, reports and fresh-runtime rerun | Same source/test results locally and on a real Colab runtime |

Detailed personal phase and setup records live in ignored docs/phases and docs/implementation. Complete one phase before starting the next.

## Run locally

From this project folder:

~~~bash
uv sync --frozen
uv run --frozen python src/check_setup.py
uv run --frozen attention-foundations status
uv run --frozen python src/show_config.py
uv run --frozen pytest -q
uv build
~~~

The workspace TUI exposes **Projects → Attention Labs → Attention Foundations**, with **Project status**, **Check setup**, **Show configuration** and **Export for Colab** runners. Setup, Checks and Build use this project's independent environment.

An unimplemented mechanism fails explicitly:

~~~bash
uv run --frozen attention-foundations mechanism --name additive
~~~

It returns status not_implemented, exit code 2, and creates no result. No implementation or test pass is simulated.

## Source layout

Entry scripts live directly in src. core owns configuration and future scoring/attention; data owns synthetic fixtures; evaluation will own independent numerical/gradient comparisons; utils owns command and source-transfer helpers. The package has no redundant outer package folder. Each project uses its own environment.

Python 3.12.13, PyTorch 2.14.1, NumPy 2.5.4, pytest 9.1.1 and the build backend are pinned and resolved in uv.lock. Linux uses the CPU PyTorch index. GPU acceleration is unnecessary for these small correctness checks; a GPU runtime does not change this CPU lock.

## Work in Google Colab

~~~bash
uv run --frozen python src/export_colab.py
~~~

This creates artifacts/colab/attention_foundations_colab.ipynb, attention-foundations-source.zip and source-manifest.json. Upload the notebook to Colab, then select the ZIP and manifest when its first cell asks for files. Run in order and download the result archive. Full steps are in [COLAB.md](COLAB.md); the [source notebook](notebooks/attention_foundations_colab.ipynb) is also available directly.

The notebook verifies source hashes before extraction, installs a separate locked Python environment, records actual versions, runs setup and pytest, and downloads logs plus a source receipt. It needs no public GitHub repository, Drive mount, paid runtime or credentials. Runtime storage is temporary; retain the downloaded receipt and rerun from the same source export after a disconnect.

Next implementation step: establish the additive-attention input/output contract, then implement and independently test one retrieval. No learner result or Google-hosted execution is inferred from preparation.
