---
name: note-open-book-index
description: >-
  Build open-book exam indexes that map topics to slide file/page locations, plus
  optional past-paper frequency analysis and mock papers. Use for 开卷考试, revision_exam,
  知识索引, 课件页码 lookup, or exam prediction from historical papers.
disable-model-invocation: true
metadata:
  author: Youhan Huang
  tool: Cursor Composer 2.5
  source: Distilled from EBU6304 Software Engineering review workflow
---

# Note Open Book Index

开卷考试专用复习索引 skill。**不解释知识点**，只提供「考什么 → 去哪个 PDF 哪一页找」的检索结构；可叠加历年真题分析与模拟卷。

## When to Use

- 用户明确说「开卷」「不需要解释，只要页码」「快速查阅」
- 需要 `revision_exam.md` 或《知识索引与复习手册》类输出
- 已有全部 lecture PDF + 可选 `oldResource/` 历年卷

## Core Principles

1. **完整覆盖优先于简洁**
2. **不遗漏优先于压缩**
3. **知识结构优先于原课件顺序**（Part 1 用 Block/主题组织）
4. **开卷模式：只索引，不讲课**（除非用户另请解释）

## Output Contract

默认文件 `revision_exam.md`，推荐三段式：

```markdown
# <Course> Open-Book Revision Index

## Part 1 — Course Map（思维导图 + 课件索引）
### Block A: <theme>（English Title）
- Mermaid 思维导图：课程分块 → 课件列表
- 每份 PDF 一张表：| 知识点（缩写首次带全称） | 页码 |

## Part 2 — Exam Focus（唯一总表）
| Topic | Freq | Priority | Lecture PDF | Pages | Notes |
（合并历年频率、押题、A/B/C 分级，**只保留一张 Master Table**）

## Part 3 — Mock Paper（可选）
- 模拟题 + 每问对应的 PDF 页码指引
```

英方考试：缩写**第一次出现必须带全称**，如 `SOLID (Single responsibility, Open-closed, …)`。

## Workflow

### Phase A — Full corpus ingestion

读取全部 PDF/PPT。必须分析：

- 正文、图片、流程图、UML（用例/类/时序/状态/活动）、架构图、表格、公式
- 箭头关系与图内标注

禁止输出「见图」——全部转为可检索文字条目。

对每张重要图片提取：

1. 核心概念
2. 组成部分
3. 关系
4. 要说明的问题
5. 对应考点
6. 与周围知识点的联系

### Phase B — Build Part 1 (Course Map)

1. 将整门课分为若干 Block（如 A–G），每 Block 映射一组 PDF
2. Mermaid 思维导图概览（节点含英文 + 中文）
3. 每份 PDF：**知识点 → 页码** 全表（要全，简称有全称）
4. 附录：关键图表索引（图名 → PDF + 页码）

### Phase C — Past-paper analysis (feeds Part 2)

若用户提供历年真题：

1. 按年份提取题型结构、占分、覆盖知识点
2. 建考点数据库，统计重复频率与演化趋势
3. 结合「今年是否开卷」调整预测
4. 输出**唯一 Master Topic Table**（不要重复多张排名表）

### Phase D — Iterative refinement

用户常见迭代指令：

- 「多用英文，名词尤其保留英文」
- 「减少重复，两文档合一为 revision_exam.md」
- 「Part 2 只要一个总表」
- 「检查所有简称首次出现有全称」

## Constraints

- Part 1 / Part 2 职责分离：Part 1 = 去哪找；Part 2 = 考什么、多重要
- 页码必须对应 `@lectureSlides` 中**真实文件名**
- 删除旧中间文件前需用户确认（若用户要求「只保留 revision_exam.md」则执行清理）

## Example Invocation (Cursor Composer 2.5)

```text
用 note-open-book-index，@lectureSlides 构建开卷复习索引 revision_exam.md。Part 1 思维导图+每课件知识点页码表；Part 2 合并考点总表；不要解释知识点。
```

```text
用 note-open-book-index 第二阶段：结合 @oldResource 历年真题做考点频率统计，预测今年重点，并入 revision_exam.md Part 2。
```

## Provenance

- **Author**: Youhan Huang
- **Tool**: Cursor Composer 2.5
- **Validated courses**: 软件工程 (EBU6304)
