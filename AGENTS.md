# Attention Labs ownership

This is the independent Attention Labs collection repository, registered in ai_projects at projects/attention-labs. Local bare origin: workspace .ai/repositories/attention-labs.git. Individual study projects are ordinary folders owned by this collection; do not make a repository per basic attention type.

Keep all single-head foundation material together in attention-foundations. Multi-head attention belongs in attention-heads, with GQA and related head/KV arrangements added there only when requested. The current source is Vizuara's The Attention Family Lectures 1–8; Lecture 9 is excluded. Shared authored tutorials live in the Projects Docs submodule, under tutorials/projects/attention-labs. Preserve the existing Attention Is All You Need tutorial and all learner/model checkpoints.

Use the existing shared developer-learning-tutorials workflow and workspace CLI. Write original prose and examples, retain primary-source attribution and the original presentation links/viewers. Keep source transcripts and raw captures in ignored workspace .ai; do not claim that a transcript or complete spoken lecture was inspected if it was unavailable. Commit changes here, make new commits available in the local bare origin, then update this collection's pointer in ai_projects. No external publication is implied.

Attention Foundations setup (2026-10-30): the existing child now owns a locked Python boilerplate and Colab source-upload runner. Keep src/core, src/data, src/evaluation and src/utils responsibilities and direct entry scripts. Report setup tests separately from pending attention correctness and actual hosted execution. Detailed personal phase/implementation records remain ignored under the child docs; do not package them in source exports.


## Standalone execution contract

Every runnable project must own its dependency manifest/lock, configuration and documented native entry points. From a standalone collection checkout, setup, run, test and build must work from the project folder without the workspace CLI, `AI_WORKSPACE`, an injected `PYTHONPATH` or sibling repositories. Shared workspace documentation links are optional context outside the workspace, not runtime requirements.

The workspace CLI/TUI is an optional adapter to those same entry points. Keep model logic in the project; do not import `ai_cli` or duplicate the launcher inside collections. Document both native and workspace commands, and verify a clean project copy outside the workspace when changing execution or packaging. Use the project's actual test framework; Python projects can declare `[tool.ai-workspace] test-args` for the optional adapter. Documentation-only projects remain planned until their boilerplate is explicitly prepared; require both launch paths before calling a new scaffold ready.
