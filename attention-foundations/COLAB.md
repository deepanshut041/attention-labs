# Run Attention Foundations in Google Colab

Use the same source and tests as the local project. A CPU runtime is sufficient; Linux installs the pinned CPU PyTorch wheel even if a GPU runtime is selected.

## Prepare the source pair

From this project's source checkout:

~~~bash
uv run --frozen python src/export_colab.py
~~~

The default output is artifacts/colab:

- attention_foundations_colab.ipynb — output-cleared runner.
- attention-foundations-source.zip — public source, tests, notebook and locked dependency files.
- source-manifest.json — matching archive/member SHA-256 hashes and Git source identity.

Use a ZIP and manifest from the same export. Git history, environments, private study docs, captions, data, weights and runtime outputs are excluded. Hashes establish consistency of your exported files, not the identity of an unknown sender.

## Run the notebook

1. Open [Google Colab](https://colab.research.google.com/), choose File → Upload notebook and select attention_foundations_colab.ipynb.
2. Connect to a CPU runtime and run from the first cell.
3. Select both the source ZIP and source-manifest.json when the upload picker appears.
4. Run installation, environment, setup and test cells in order. Installation requires internet and creates a separate Python 3.12.13 environment; Colab's kernel packages do not substitute for it.
5. Run the download cell and retain attention-foundations-colab-results.zip before ending the runtime.

The current notebook runs boilerplate/setup tests. Later implementation phases add real mechanism checks to the same project suite. A successful setup probe is not an attention correctness result.

## Read the result

The downloaded archive includes source-manifest.json, actual environment versions, command logs, status/setup JSON, pytest's JUnit report and a receipt. Failed or skipped tests stop before a success receipt. The receipt identifies the exact uploaded source and explicitly reports boilerplate status rather than claiming completed attention algorithms.

After Disconnect and delete runtime, reconnect and repeat from the first cell with the same source pair. This project currently has no long-running training state to restore. Future training would need the workspace's full optimizer/RNG/progress persistence contract; replaying tests is not recovery of optimizer state.

Local execution of the operational cells with a simulated Colab upload/download interface is checked separately from an actual Google-hosted run. Hosted acceptance remains pending until the notebook is run there and its downloaded receipt is reviewed.

[Google's Colab FAQ](https://research.google.com/colaboratory/faq.html) documents notebook upload, temporary VMs and variable resource limits. [uv's lock/sync documentation](https://docs.astral.sh/uv/concepts/projects/sync/) explains frozen dependency synchronization. This runner uses subprocesses in the locked environment so it can run with a different notebook-kernel Python version.
