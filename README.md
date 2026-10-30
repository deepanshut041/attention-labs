# Attention Labs

A collection for studying attention mechanisms through worked mathematics, runnable references and the original lecture presentations. It is an independent Git repository and a submodule of ai_projects. The new material follows Vizuara's [The Attention Family playlist](https://www.youtube.com/playlist?list=PLVomdvPuJ1po) with original explanations and examples; Lecture 9 is excluded.

| Study folder | Current route | Scope |
| --- | --- | --- |
| [Attention Foundations](attention-foundations/README.md) | Lectures 1–7 | One folder for the fixed-summary motivation, additive/dot scoring, self-attention, Q/K/V and causal masking/dropout |
| [Attention Heads](attention-heads/README.md) | Lecture 8 | MHA, output projection, tensor packing and output/gradient equivalence; future GQA/MQA work stays here |

There are no separate project folders for the basic attention types. The detailed shared tutorials are under `ai_projects/docs/tutorials/projects/attention-labs/`. Each included lecture has its original video and live presentation, alongside original prose, figures and code. The original slide applications remain hosted by Vizuara. The author reviewed all eight English automatic subtitle/transcript texts and all 181 slides. DownSub VTT captions are saved for Lectures 1–8; Lecture 6 was also cross-checked against Transcript.you, with all 1,417 segment texts matching. Raw captions remain in the ignored workspace source archive; technical terms are checked against the slides and primary references.

Attention Foundations now also contains runnable project boilerplate: a locked Python environment, explicit build/test goals, setup checks, source responsibility folders and a source-upload Colab notebook. Its six attention implementations remain pending. Attention Heads remains a study entry point. The runnable teaching references stay with the shared tutorials; no trained model or learner result is implied. The existing Attention Is All You Need project remains separate. Local bare origin: workspace `.ai/repositories/attention-labs.git`.
