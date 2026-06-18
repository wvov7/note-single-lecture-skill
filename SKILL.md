---
name: note-single-lecture
description: "Create high-fidelity study notes for one lecture PDF/PPT using a generated mind map first. Store intermediate artifacts in note-single-lecture-work/pdf-stem/ and final notes in note-single-lecture/. Write descriptive prose mainly in Chinese, preserve key English terms and important English descriptive source sentences, and preserve original answers and complete concept definitions without visible source-label boilerplate; when preserving an English descriptive sentence, attach its direct Chinese translation immediately in the same paragraph."
---

# Note Single Lecture

## Output Contract

For one lecture file, create these workspace-relative output folders unless the user asks otherwise:

- Intermediate folder: `note-single-lecture-work/<pdf-stem>/`
- Final notes folder: `note-single-lecture/`

Put every intermediate/generated working artifact in `note-single-lecture-work/<pdf-stem>/`, including extracted text, rendered page images, outline JSON, mind map PNG, prompt MD, scratch audits, and temporary checks.

Put the final classroom note Markdown only in `note-single-lecture/`.

Produce exactly these named artifacts unless the user asks otherwise:

1. `note-single-lecture-work/<pdf-stem>/<pdf-stem>_思维导图.png`
2. `note-single-lecture-work/<pdf-stem>/<pdf-stem>_笔记生成提示词.md`
3. `note-single-lecture/<pdf-stem>_课程笔记.md`

Use the source lecture PDF/PPT, generated mind map, and generated prompt as inputs for the final notes. Copy the final Markdown notes to the clipboard only when the user explicitly wants Feishu-ready output.

## Workflow

### 1. Inspect the lecture

- Identify the single source lecture file. If multiple candidate PDFs/PPTs exist, ask which one.
- Define `<pdf-stem>` from the source file name without extension.
- Create `note-single-lecture-work/<pdf-stem>/` for intermediate artifacts and `note-single-lecture/` for final notes.
- Extract slide/page text with `pdftotext -layout` for PDFs when available. For PPTX, use available Office/Python extraction tools.
- Get page/slide count and a title list.
- Render sparse or visual-heavy pages to images using `pdftoppm` or another local renderer, especially pages with diagrams, screenshots, code images, tables, examples, exercises, or answer slides.
- Treat the current lecture file as authoritative; prior notes are only examples.
- Ignore non-course-content administrative information by default, including opening lecturer names/affiliations and closing email/contact/forum/Q&A-channel slides, unless the user explicitly asks to preserve administrative information.

### 2. Build the mind map first

Create a complete hierarchical outline that covers all course content without mechanically following slide order. The mind map should resemble a study framework:

- Root: lecture title.
- First-level branches: major themes.
- Lower-level branches: definitions, processes, comparisons, diagrams, workflows, examples, exercises, answer slides, practice requirements, exam points.
- For concepts with explicit definitions in the lecture, preserve the complete source-language definition before adding the Chinese translation/explanation. Do not replace a full source definition with a shorter paraphrase. Do not introduce visible boilerplate labels that announce the source-language status. If the source sentence is English, put the direct Chinese translation immediately after the English sentence in the same paragraph or list item, with no blank line, no line break, and no added separator label.
- Include English for important terms in parentheses, e.g. `版本控制（Version Control）`.
- Include diagram/screenshot meanings as nodes, not just text slides.
- Include all examples, exercises, quizzes, past-paper questions, and answer slides as nodes when they are part of the course content.
- Place examples, exercises, quizzes, questions, and answer slides directly under the concept, process step, diagram, workflow, or definition they test or illustrate. Do not group them into a separate standalone examples/questions section, because that weakens the association between the prompt and the related content.
- For examples/exercises/questions, preserve any original answer from the lecture completely and verbatim enough for study use, especially numbered or bulleted sub-points. Do not shorten an original answer into a summary. Add a Chinese translation/explanation after the complete original answer.
- When creating a supplemental reference answer because the lecture has no answer, write the supplemental answer in English first, then provide a complete Chinese translation that preserves the same points and structure. Do not use a shorter Chinese explanation in place of the translation.
- If the lecture has no answer for an example/exercise/question, create a bilingual reference answer and label it as `补充参考答案（Supplemental Reference Answer）`.

Save the mind map outline JSON in `note-single-lecture-work/<pdf-stem>/`, then render the outline to PNG in the same folder. Prefer the bundled script:

```bash
python <skill-dir>/scripts/render_mindmap.py note-single-lecture-work/<pdf-stem>/outline.json note-single-lecture-work/<pdf-stem>/<pdf-stem>_思维导图.png
```

The script expects JSON:

```json
{
  "title": "Lecture 4：生产与管理（Production and Management）",
  "children": [
    {
      "title": "敏捷管理（Agile Management）",
      "children": [
        {"title": "迭代（Sprint）：短周期开发"}
      ]
    }
  ]
}
```

If rendering fails, create the PNG by another reliable local method, but still deliver a PNG file.

### 3. Generate the note prompt

Readability override for all note generation:

- Do not mechanically reproduce every English source text plus Chinese translation. Ordinary descriptive content should be written mainly in Chinese, but preserve selected important English descriptive source sentences when they are central lecture claims, exam-worthy wording, summary bullets, design warnings, or concise principle statements. Keep English for key terms in parentheses, complete source definitions, selected important descriptive source sentences, examples/exercises/questions, existing answers, supplemental answers, and code/literal source content.
- Use unordered lists for short feature lists, design considerations, term groups, and parallel points.
- Use ordered lists for steps, procedures, sequences, and methods.
- Use Markdown tables for necessary comparisons when the lecture contains similar concepts, media properties, workflows, design tradeoffs, criteria, examples with contrasting outcomes, or good/bad design cases. Insert each comparison table immediately after the concept, diagram, workflow, or example it clarifies; do not collect comparison tables into a separate comparison-only section unless the lecture itself is organized that way. Use unordered or ordered lists only for lightweight comparisons where a table would reduce readability.
- Use quote blocks only for course-content examples, exercises, questions, existing source answers, and supplemental reference answers. Do not use quote blocks for ordinary definitions, explanations, design considerations, comparisons, feature lists, or short source/translation pairs.
- For numbered bilingual examples/exercises/questions/answers inside quote blocks, do not put Markdown ordered-list markers on each quoted line. Prefer a quoted label such as `Point 1:` / `第 1 点：`, or keep one answer point together as one quoted paragraph, so renderers cannot renumber English and Chinese lines incorrectly.
- Do not put bilingual line-by-line lists inside quote blocks. If a complete source definition or descriptive English sentence must keep English outside examples/exercises/questions/answers, keep the English and direct Chinese translation in the same normal paragraph or list item without source-language boilerplate labels. Put the Chinese translation immediately after the English sentence, with no blank line, no line break, and no extra space used as a visual separator.
- Reserve code blocks for actual code or literal formatted source content.
- English source text and direct Chinese translation may appear in normal paragraphs, unordered lists, or ordered lists when exact source wording is important for an exam, definition, important descriptive lecture claim, example, exercise, question, or answer. For descriptive source statements, preserve only selected high-value sentences instead of every slide bullet; the English sentence and direct Chinese translation must stay together in the same paragraph, with the Chinese translation immediately following the English sentence. Quote blocks are reserved for examples, exercises, questions, and their answers.
- Do not use visible source/translation boilerplate labels such as `英文原文`, `课件定义`, `Source`, or `Translation`; put explanatory Chinese prose directly after the source, translation, paragraph, or list as ordinary Markdown text.
- Avoid duplicate content: if a Chinese sentence has already explained the same meaning, do not immediately repeat it again as English source plus direct translation unless exact source wording is important for an exam, definition, important descriptive lecture claim, or answer. For low-value descriptive slide text, prefer a faithful Chinese paraphrase rather than preserving the full English sentence.
- Hard heading-numbering constraint: except for the final `## 重点对比总结` and `## 考试与复习重点` sections, every level-2 Markdown heading must begin with an uppercase Chinese section number such as `一、`, `二、`, `三、`; every level-3 Markdown heading must begin with a lowercase Arabic number such as `1.`, `2.`, `3.`. Restart level-3 numbering inside each level-2 section.

Create `note-single-lecture-work/<pdf-stem>/<pdf-stem>_笔记生成提示词.md` before writing notes. The prompt must:

- State the concrete goal.
- Name the source lecture file and generated mind map file.
- Require theme-based Markdown headings, not slide-by-slide notes.
- Require Chinese explanation and mostly Chinese descriptive prose; allow selected important English descriptive source sentences outside preserved definitions/examples/questions/answers when the source wording is useful for review or exams.
- Require any follow-up Chinese explanation to be a normal Markdown paragraph outside source quote/code blocks when quote blocks are used, without visible source/translation boilerplate labels.
- Require complete definition handling: when the lecture provides a concept definition, include the source-language definition in full, then add a Chinese translation/explanation. Do not compress the source definition into a summary, and do not prefix it with source-language boilerplate labels. If the source definition or descriptive source sentence is English, place the Chinese direct translation immediately after it in the same paragraph or list item, with no blank line, no line break, and no extra separator space.
- Require key terms and definitions as `中文（English）`.
- Require diagram/screenshot explanations.
- Require example/exercise/question handling for every course-content example, exercise, quiz, or past-paper question in the lecture: include the English prompt when useful, a Chinese translation/explanation, and an answer section.
- Require examples, exercises, quizzes, questions, their existing source answers, and supplemental reference answers to use quote blocks for the preserved prompt/answer content.
- Require all non-example/non-exercise/non-question content to avoid quote blocks and use ordinary paragraphs plus unordered or ordered lists according to the content structure.
- Require examples, exercises, quizzes, questions, and answer slides to appear immediately after the corresponding concept/process/diagram/workflow they illustrate or test. Do not create a separate examples/questions/exercises section unless the whole lecture is itself organized as a question bank.
- If the PDF provides an answer, preserve the source-language answer completely, including all numbered or bulleted sub-points, and then add a Chinese translation/explanation. Do not compress, paraphrase away, or replace a source answer with a shorter "strong answer" summary.
- For supplemental reference answers, require a complete Chinese translation of the supplemental English answer, preserving all numbered/bulleted points and sub-points. Do not replace the Chinese translation with a shorter explanation or study note.
- If no answer is provided, write a plausible reference answer in both English and Chinese and mark it as `补充参考答案（Supplemental Reference Answer）`.
- Ignore non-course-content administrative information such as the opening lecturer name/affiliation and closing email/contact/forum/Q&A channel unless the user explicitly asks to include it.
- Require highlight syntax for key points: `==注意：...==`.
- Require concept comparisons when the lecture contains similar terms, workflows, media properties, design tradeoffs, evaluation criteria, or good/bad examples. Use Markdown tables for necessary comparisons and insert each table immediately after the related concept/process/diagram/workflow/example it clarifies. Use unordered or ordered lists only for lightweight comparisons where a table would reduce readability.
- Require final output named `note-single-lecture/<pdf-stem>_课程笔记.md`.

### 4. Write the final notes

Use the generated prompt, mind map, and source lecture to write `note-single-lecture/<pdf-stem>_课程笔记.md`.

Recommended structure:

```markdown
# Lecture N：中文标题（English Title）
## 课程基础信息
## 整体框架 / 主题总览
## 一、主题一（English）
### 关键定义
### 流程解释
### 图示说明
### 示例、练习与答案
## 二、主题二（English）
...
## 重点对比总结
## 考试与复习重点
```

Do not use `## Slide 1`, `## Slide 2`, etc. It is acceptable to mention slide numbers only as traceability notes when useful, but the document must be organized by concepts.

Examples, exercises, quizzes, questions, and answer slides must stay attached to their related concept sections instead of being moved to a separate final block. For example, a question about project purpose belongs under the project-goal subsection, and a question about target users belongs under the target-audience subsection.

Use the lightest readable Markdown structure. For example, short design considerations should be written as a list:

```markdown
- Navigation: 导航。
- Use of Controls: 控件使用。
```

Use Markdown tables for necessary comparisons. Place each table at the immediate point of need, directly after the concept, workflow, diagram, or example being compared. Do not postpone all comparisons to the final summary. Good candidates include similar concepts, media property tradeoffs, design choices, good/bad examples, scoring criteria, and workflow variants.

Do not repeat the same idea in a Chinese sentence and then immediately repeat it again as English source plus direct Chinese translation, unless the exact source wording belongs to an example, exercise, question, existing answer, or supplemental reference answer.

Use quote blocks only for examples, exercises, questions, existing answers, and supplemental reference answers. Keep definitions, explanations, design considerations, comparisons, and short source/translation pairs as ordinary paragraphs, unordered lists, or ordered lists. When an English descriptive sentence is preserved with a direct Chinese translation, keep the pair in one paragraph/list item and join the translation directly after the English sentence without a blank line, line break, or boilerplate label.

For bilingual quoted answer content, keep each answer point together and avoid Markdown ordered-list markers inside the quote block:

```markdown
> Point 1: Complete English answer point.
> 第 1 点：完整中文翻译。
```

## Quality Checks

Before final response:

- Confirm all required artifacts exist.
- Confirm intermediate artifacts are in `note-single-lecture-work/<pdf-stem>/`.
- Confirm final notes are in `note-single-lecture/`.
- Confirm final notes are not slide-by-slide: no `^## Slide ` headings.
- Confirm every level-2 heading except final `## 重点对比总结` and `## 考试与复习重点` starts with an uppercase Chinese section number such as `一、`, `二、`, `三、`.
- Confirm every level-3 heading starts with a lowercase Arabic number such as `1.`, `2.`, `3.`, and restarts numbering inside each level-2 section.
- Confirm Markdown code fences are balanced.
- Confirm key terms preserve English names.
- Confirm concepts with source definitions preserve the full source-language definition and include a Chinese translation/explanation without underlining requirements.
- Confirm all examples/exercises/questions have answer treatment: existing answers are complete and keep their original numbered/bulleted structure before translation; missing answers have bilingual supplemental reference answers.
- Confirm examples/exercises/questions are placed immediately after their corresponding concept/process/diagram/workflow rather than collected into a separate examples/questions section.
- Confirm short feature lists, design considerations, term groups, and parallel points use unordered lists when that is clearer than quote/code blocks.
- Confirm steps, procedures, sequences, and methods use ordered lists when that is clearer than quote/code blocks.
- Confirm necessary comparisons use Markdown tables and that each table appears immediately after the related concept, process, diagram, workflow, or example rather than being deferred to a separate comparison-only section.
- Confirm quote blocks are used only for examples, exercises, questions, existing answers, and supplemental reference answers.
- Confirm ordinary definitions, explanations, design considerations, comparisons, feature lists, and short source/translation pairs are not placed in quote blocks.
- Confirm quote blocks do not contain Markdown ordered-list markers such as `> 1.` or `> 2.`.
- Confirm bilingual numbered examples/exercises/questions/answers keep English and Chinese for the same point together rather than as separate numbered items.
- Confirm non-question bilingual line-by-line content is not placed inside quote blocks when a normal list or paragraph pair would render more reliably.
- Confirm there is no visible source/translation boilerplate label in the final notes, including labels like `英文原文`, `课件定义`, `Source`, or `Translation`.
- Confirm preserved English descriptive sentences and their direct Chinese translations are in the same paragraph or list item, with the Chinese translation immediately following the English sentence and no blank line or line break between them.
- Confirm repeated English/Chinese source pairs are omitted or merged when they duplicate a preceding explanation and add no new study value.
- Confirm Chinese explanation paragraphs are outside source quote/code blocks, not mixed into the same block as original source and direct translation.
- Confirm supplemental reference answers include a complete Chinese translation matching the English answer's points and structure, not a shorter Chinese explanation.
- Confirm administrative-only lecturer/contact/forum/Q&A-channel content is omitted unless explicitly requested.
- Confirm non-code, non-source-quote explanatory lines are not pure English. Confirm descriptive prose is mainly Chinese, while selected important English descriptive source sentences are preserved with immediate Chinese direct translation in the same paragraph or list item.
- Confirm visual/sparse slides were covered by diagram/screenshot explanations.
- Confirm the final notes file was copied to clipboard only when requested.

Use this pure-English check on the final notes when useful:

```python
from pathlib import Path
import re
text = Path("NOTES.md").read_text(encoding="utf-8-sig")
in_code = False
suspect = []
for i, line in enumerate(text.splitlines(), 1):
    if line.startswith("```"):
        in_code = not in_code
        continue
    s = line.strip()
    if not s or in_code or s.startswith(">"):
        continue
    if re.search(r"[A-Za-z]", s) and not re.search(r"[\u4e00-\u9fff]", s):
        if len(re.sub(r"[`*_()（）\d\W]+", "", s)) > 8:
            suspect.append((i, s))
print(suspect[:50])
```

## Example Reference

For the target style and fidelity, read `references/lecture4-example.md` when the user asks for this workflow or when output structure is unclear. It summarizes the Lecture 4 example process: source PDF + user mind map + final theme-based notes.
