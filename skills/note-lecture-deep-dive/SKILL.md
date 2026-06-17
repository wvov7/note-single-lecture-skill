---
name: note-lecture-deep-dive
description: >-
  Produce in-depth, zero-omission Chinese lecture notes from one or more PDF/PPT
  slides with logic reordering and dynamic depth. Use when the user wants 知识点精讲,
  逐讲复习, 逻辑重排, or deep lecture breakdown with core vs auxiliary topic tiers.
disable-model-invocation: true
metadata:
  author: Youhan Huang
  tool: Cursor Composer 2.5
  source: Distilled from EBU5408 / EBU6230 review workflows
---

# Note Lecture Deep Dive

逐讲课件深度精讲 skill。把 PPT/PDF 打碎、按逻辑重排，动态调整讲解深度（多页反复 = 重点长讲，单页一笔带过 = 简要概括）。

## When to Use

- 用户要「精讲」「彻底掌握某几讲」「按逻辑梳理而非按页码」
- 英方课 PDF 含大量图示、公式、推导，需要图文一并解析
- 分批执行：`继续 L2、3、4` 或 `继续 L11、12、13`

## Output Contract

- 默认输出 Markdown，文件名由用户指定或 `<CourseName>_L<n>_精讲.md`
- 英方课：关键术语保留英文，格式 `中文（English）`
- 每讲完一批课件，文末附 **3 道高价值思考题/测验题**

## Workflow

### 1. Inspect slides

- 读取用户 `@` 引入的 PDF/PPT；若目录有多份，按用户指定的 lecture 编号处理
- 提取文字；对稀疏页、图示页、公式页渲染为图片或 OCR，**不得只依赖纯文本层**
- 统计每知识点在原课件中的页码跨度与出现次数，用于判定重要度

### 2. Write Overview

```markdown
## 1. 本课核心概述 (Overview)
- **一句话核心**：…
- **重构后的逻辑流**：A -> B -> C（或 Markdown 列表）
```

逻辑流必须打破原 Slide 顺序，按「由浅入深 / 因果推导 / 技术架构」重组。

### 3. Detailed Breakdown

按**新逻辑顺序**分块讲解，两类模板：

#### 核心骨干知识点（原课件多页、反复出现）

```markdown
### 📍 [核心骨干] 知识点名称
- **课件原意精粹**：完整提取定义与关键术语，不漏脚注/补充说明
- **通俗化深度化解**：直觉、类比、底层本质
- **数学公式与完整推导（如有）**：列公式并解释每个符号
- **承前启后**：与前后知识点的因果关系
- **潜在考点/应用**：考试/实验常见考法
```

#### 边缘/辅助知识点（原课件仅出现一次）

```markdown
### 📌 [边缘/辅助] 知识点名称
- **概念简述**：1–2 句
- **背景/定位**：在体系中的辅助作用
```

### 4. Dynamic depth rules

- **多页 + 连续推导 + 多例证** → 最高深度，长篇幅
- **单页单次** → 简要概括，不拖泥带水
- **零遗漏**：边缘点可短，但不可删除

### 5. Batch continuation

用户说「继续 Lx」时：

- 只处理新指定的 lecture，不重复已输出内容
- 保持与先前批次相同的结构与术语风格

## Constraints

1. 不得输出「见图」「如图所示」「参考原图」——必须把图示信息文字化
2. 不得机械按 `Slide 1 / Slide 2` 组织正文（页码仅作溯源注）
3. PDF 图片内容与正文同等重要
4. 英方考试语境下，名词优先保留英文原文

## Example Invocation (Cursor Composer 2.5)

```text
用 note-lecture-deep-dive，@lectureSlides 从 L1 开始精讲。多页出现的知识点要深度展开，单页出现的简要概括。先讲 L1，讲完我再让你继续。
```

```text
用 note-lecture-deep-dive 继续 L7–L8。注意 PDF 里的图片也要提取，不要遗漏。
```

## Provenance

- **Author**: Youhan Huang
- **Tool**: Cursor Composer 2.5
- **Validated courses**: 数字音频基础 (EBU5408), 图形与视频处理 (EBU6230)
