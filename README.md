# Attention Labs

A collection for studying attention mechanisms through worked mathematics, runnable references and the original lecture presentations. It is an independent Git repository and a submodule of ai_projects. The new material follows Vizuara's [The Attention Family playlist](https://www.youtube.com/playlist?list=PLVomdvPuJ1po) with original explanations and examples; Lecture 9 is excluded.

| Study folder | Current route | Scope |
| --- | --- | --- |
| [Attention Foundations](attention-foundations/README.md) | Lectures 1–7 | One folder for the fixed-summary motivation, additive/dot scoring, self-attention, Q/K/V and causal masking/dropout |
| [Attention Heads](attention-heads/README.md) | Lecture 8 | MHA, output projection, tensor packing and output/gradient equivalence; future GQA/MQA work stays here |

There are no separate project folders for the basic attention types. The detailed shared tutorials are under `ai_projects/docs/tutorials/projects/attention-labs/`. Each included lecture has its original video and live presentation, alongside original prose, figures and code. The original slide applications remain hosted by Vizuara. Caption retrieval was unavailable, so the author review covers the video pages/descriptions and all 181 slides, without claiming a complete spoken-transcript audit.

This collection contains the study entry points. The runnable mathematical examples are packaged with the shared tutorials; no trained model or new learner implementation is implied. The existing Attention Is All You Need project remains separate. Local bare origin: workspace `.ai/repositories/attention-labs.git`.
