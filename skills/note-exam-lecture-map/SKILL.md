---
name: note-exam-lecture-map
description: >-
  Build lecture-by-lecture knowledge summaries plus weighted exam-topic tables by
  cross-referencing slide PDFs with past-paper folders. Use when the user mentions
  考点分析, 往年题, exam_lecture_stat, 重点权重, or lectureSlides + oldResource together.
disable-model-invocation: true
metadata:
  author: Youhan Huang
  tool: Cursor Composer 2.5
  source: Distilled from EBU6305 / EBU5408 review workflows
---

# Note Exam Lecture Map

课件逐讲概括 + 往年题考点权重分析 skill。适合「整门课复习前盘考点」。

## When to Use

- 用户同时 `@lectureSlides` 与 `@oldResource`（或类似往年题目录）
- 需要 `exam_lecture_stat.md`、`exam_lecture_summary.md` 或等价报告
- 要回答：「什么最常考、对应课件哪讲哪页、在哪些年份试卷出现过」

## Output Contract

默认生成一份 Markdown 报告，结构如下：

```markdown
# <课程名> 课件与考点分析报告

## Part 1 — 按课件顺序的知识点概括
### Lecture N: <title>
**学习目标**: …
**知识点（按页序）**:
1. P1–P3: … ⭐
2. P4–P8: …
（⭐ = 多页反复出现，高概率重点）

## Part 2 — 考点权重总表
| 考点 | 重要度/权重 | 出现于哪些试卷 | 对应课件（文件 + 页码） |
|------|-------------|----------------|-------------------------|
| …    | …           | …              | …                       |
```

输出文件名默认 `exam_lecture_stat.md`；用户指定时从其。

## Workflow

### 1. Inventory resources

- 列出 `lectureSlides/` 全部 PDF/PPT，确定讲次顺序
- 列出 `oldResource/`（或用户给定路径）中历年卷、quiz、样题
- 扫描件 PDF 需 OCR；先建 `_extracted/` 存放逐页 JSON/Markdown 中间产物

### 2. Extract every slide page

- **每页都要看**，不得跳过
- 图文并重：表格、截图、示意图需文字化描述
- 记录 `(lecture_file, page)` 索引供 Part 2 引用

### 3. Summarize lectures (Part 1)

规则：

- 按课件 PDF **原始顺序**逐讲概括（与 note-lecture-deep-dive 的逻辑重排不同）
- **多页出现** → 标 ⭐，正文注明「高概率重点」
- **单页单次** → 可简写，但不删除

### 4. Analyze past papers (Part 2)

#### 权重规则（可微调，须在报告中说明）

| 信号 | 权重建议 |
|------|----------|
| 往年题占分高 / 大题 | 非常高 |
| 仅在往年题出现（任意年份） | 比较重要 |
| 课件内出现 >1 次 | 一般重要 |
| 课件多页 + 跨多讲出现 | 非常重要 |
| 出现越多、年份越近 | 权重累加 |

实现步骤：

1. 为每份试卷赋基础权重（越新越高，如 24/25 > 23/24 > …）
2. 从试卷提取考点短语，归一化到主题 taxonomy
3. 匹配课件页码索引
4. 汇总为总表，按权重降序

### 5. Large-course strategy

课件 + 试卷数量大时：

1. 先写提取脚本（PyMuPDF / OCR）批量出 `_extracted/`
2. 分 lecture 批次生成 summary（可用 subagent 并行）
3. 最后合并考点表

## Constraints

- 考点必须能回溯到 **具体 PDF 文件名 + 页码**
- 不得编造试卷未出现的考点；不确定时标注「待人工确认」
- 权重公式须在报告开头简短说明

## Example Invocation (Cursor Composer 2.5)

```text
用 note-exam-lecture-map：@lectureSlides 逐页概括知识点，@oldResource 分析考点权重，写入 exam_lecture_stat.md。多页出现=重点，越新的往年题权重越高。
```

```text
用 note-exam-lecture-map，你是课程组老师，根据 @oldResource 和 @lectureSlides 判断今年重点，输出 exam_lecture_summary.md。
```

## Provenance

- **Author**: Youhan Huang
- **Tool**: Cursor Composer 2.5
- **Validated courses**: 交互式媒体设计 (EBU6305), 数字音频基础 (EBU5408)
