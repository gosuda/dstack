# Quality checklist reference

Read the draft once through, then work this list top to bottom. Every checked item must hold before the README ships. Skip an item only when the README claims no such surface (for example, no badges means the badge item does not apply). Anything the README does claim must pass.

## Structure

- [ ] Opens with the project name and a one-line tagline.
- [ ] Shows a visual separator after the opening shop-window block.
- [ ] Has an Installation section that matches the project type.
- [ ] Has a Quick Start section the reader can run.
- [ ] Has a Features section.
- [ ] Has a Usage section.
- [ ] Has a Contributing section.
- [ ] Has a License section.

## Content

- [ ] Installation instructions are complete and correct for the project's actual package manager.
- [ ] Quick Start commands are copy-pasteable and reach a working result from a clean machine.
- [ ] Features describe what the reader can do, not how the code is built.
- [ ] Usage examples run against the current API and produce the described result.
- [ ] Contributing names the workflow: fork, branch, test, and pull request.
- [ ] License names the license and links to its full text.

## Accuracy

- [ ] No command needs a tool outside those named in Installation.
- [ ] No hardcoded path contradicts the project's actual layout.
- [ ] No version number contradicts the project manifest.
- [ ] No claimed feature is missing from the project.

## Presentation

- [ ] Every badge image loads and shows its real value.
- [ ] No relative link is broken.
- [ ] Every code block names its language.
- [ ] Dense paragraphs are split into lists or short paragraphs a skimmer can scan.
- [ ] Heading levels stay consistent through the file.
