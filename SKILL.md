---
name: note-single-lecture
description: "Create high-fidelity study notes for one lecture PDF/PPT using a generated mind map first. Store intermediate artifacts in note-single-lecture-work/<pdf-stem>/ and final notes in note-single-lecture/. Preserve original answers for examples/exercises completely, especially numbered or bulleted answer points."
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
- Include English for important terms in parentheses, e.g. `版本控制（Version Control）`.
- Include diagram/screenshot meanings as nodes, not just text slides.
- Include all examples, exercises, quizzes, past-paper questions, and answer slides as nodes when they are part of the course content.
- For examples/exercises/questions, preserve any original answer from the lecture completely and verbatim enough for study use, especially numbered or bulleted sub-points. Do not shorten an original answer into a summary. Add a Chinese translation/explanation after the complete original answer.
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

Create `note-single-lecture-work/<pdf-stem>/<pdf-stem>_笔记生成提示词.md` before writing notes. The prompt must:

- State the concrete goal.
- Name the source lecture file and generated mind map file.
- Require theme-based Markdown headings, not slide-by-slide notes.
- Require Chinese explanation; no pure-English explanatory prose outside preserved source quotations/code.
- Require key terms and definitions as `中文（English）`.
- Require diagram/screenshot explanations.
- Require example/exercise/question handling for every course-content example, exercise, quiz, or past-paper question in the lecture: include the English prompt when useful, a Chinese translation/explanation, and an answer section.
- If the PDF provides an answer, preserve the original English answer completely, including all numbered or bulleted sub-points, and then add a Chinese translation/explanation. Do not compress, paraphrase away, or replace an original answer with a shorter "strong answer" summary.
- If no answer is provided, write a plausible reference answer in both English and Chinese and mark it as `补充参考答案（Supplemental Reference Answer）`.
- Ignore non-course-content administrative information such as the opening lecturer name/affiliation and closing email/contact/forum/Q&A channel unless the user explicitly asks to include it.
- Require highlight syntax for key points: `==注意：...==`.
- Require a concept comparison table when the lecture contains similar terms/workflows.
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

## Quality Checks

Before final response:

- Confirm all required artifacts exist.
- Confirm intermediate artifacts are in `note-single-lecture-work/<pdf-stem>/`.
- Confirm final notes are in `note-single-lecture/`.
- Confirm final notes are not slide-by-slide: no `^## Slide ` headings.
- Confirm Markdown code fences are balanced.
- Confirm key terms preserve English names.
- Confirm all examples/exercises/questions have answer treatment: existing answers are complete and keep their original numbered/bulleted structure before translation; missing answers have bilingual supplemental reference answers.
- Confirm administrative-only lecturer/contact/forum/Q&A-channel content is omitted unless explicitly requested.
- Confirm non-code, non-source-quote explanatory lines are not pure English.
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
