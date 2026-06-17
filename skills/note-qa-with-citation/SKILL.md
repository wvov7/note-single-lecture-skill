---
name: note-qa-with-citation
description: >-
  Answer course questions strictly from lecture PDFs/PPTs with file name and page
  citations, optional mind maps, and batch exam grading. Use when the user asks
  课件依据, 第几页, 思维导图梳理, answer.md from 期末考试, or Q&A grounded in slides only.
disable-model-invocation: true
metadata:
  author: Youhan Huang
  tool: Cursor Composer 2.5
  source: Distilled from EBU6230 / foreign literature exam workflows
---

# Note QA With Citation

基于课件的问答 + 页码溯源 skill。每个结论必须标明来源 PDF 与页码；不允许超出课件臆测。

## When to Use

- 「解答这个问题，并说明哪个课件第几页」
- 「根据课件回答 `@期末考试` 全部题目，写入 answer.md」
- 「梳理某章节概念，形成思维导图」
- 需要对已有答案做全量复核（如 80 题检查）

## Output Contract

### 单问单答

```markdown
## 问题：…

### 回答
…

### 来源
- `7 3-1_Edges-I.pdf` **第 12 页**：…
- `8 3-2_Edges-II.pdf` **第 5–7 页**：…
```

### 批量试卷

- 输出 `answer.md`（或用户指定路径）
- 每题格式：`题号 | 答案 | 依据（PDF + 页码）`
- 图片题 / 扫描卷：先 OCR 再作答；OCR 不确定处标注并复核

### 思维导图（用户要求时）

- 优先 Mermaid `mindmap` 或 `flowchart`
- **避免** Mermaid 不兼容字符：`<br/>`、`/`、`→`、`×`、`[-1,0,+1]` 等；用「乘」「到」替代符号

## Workflow

### 1. Locate authoritative sources

- 使用用户 `@` 的课件目录或已提取的 `lecture_extracted.txt` / `_extracted/*.json`
- 无提取文件时：PyMuPDF / pdftotext 逐页提取，保留 `(file, page)` 元数据

### 2. Answer from slides only

- 先检索相关页，再组织答案
- 课件无明确说法 → 写「课件未直接给出」，可给推理但须标注为推断
- 英方课保留关键英文术语

### 3. Citation rules

- 页码 = PDF 内页序（非课程全局 Slide 编号），若课件内有 printed slide number 可同时注明
- 多页支撑同一结论：全部列出
- 对比类问题（如 Intensity vs Brightness）：表格 + 分来源列举

### 4. Visual / OCR quality loop

若用户反馈 OCR 错误：

1. 反思提取方式（换 OCR 引擎、提高 DPI、直读 PDF 文本层）
2. 对争议题回到原始 PDF 单页核对
3. 批量复核时逐题输出「原答案 | 修正 | 依据页码」

### 5. Follow-up deep dives

用户追问单点（如「具体介绍 Canny」「解释 Harris 的 E、M、λ」）：

- 在同一 citation 标准下扩展
- 公式逐符号解释，仍附页码

## Constraints

- **不得**给出与课件矛盾的「常见知识」
- **不得**省略来源
- 思维导图须可渲染；报错则降级为 flowchart 或缩略节点名

## Example Invocation (Cursor Composer 2.5)

```text
用 note-qa-with-citation：对比 Intensity 和 Brightness，并梳理 edge/corner detection 所有 filter/mask 形成思维导图。每个结论标明 PDF 文件名和页码。
```

```text
用 note-qa-with-citation，根据课件回答 @期末考试 全部问题，先提取 PPT 和图片文字，写入 answer.md。不要遗漏任何一题。
```

```text
用 note-qa-with-citation 检查 answer.md 全部 80 题，给出每题课件依据的序号和页数。
```

## Provenance

- **Author**: Youhan Huang
- **Tool**: Cursor Composer 2.5
- **Validated courses**: 图形与视频处理 (EBU6230), 外国文学鉴赏
