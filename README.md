# note-single-lecture

自用英方课单讲课件复习 skill。用于把一个 lecture PDF/PPT 整理成：

1. 思维导图 PNG
2. 笔记生成提示词 MD
3. 中文课程笔记 MD

## 安装

把仓库放到 Codex skills 目录下，例如：

```powershell
git clone https://github.com/wvov7/note-single-lecture.git C:\Users\asus\.codex\skills\note-single-lecture
```

如果目录已存在，可以进入目录后更新：

```powershell
cd C:\Users\asus\.codex\skills\note-single-lecture
git pull
```

## 使用方式

在包含课件的工作目录中，让 Codex 使用该 skill，例如：

```text
用 note-single-lecture，根据仓库中的 lecture 5 先生成思维导图 PNG，再生成笔记提示词 MD，最后生成课程笔记 MD。
```

如果目录中有多个可能的 lecture 文件，需要明确指定文件名，例如：

```text
用 note-single-lecture 处理 Lecture 5. AI-Led Development.pdf。
```

## 输出目录

假设源文件为：

```text
Lecture 5. AI-Led Development.pdf
```

中间产物会放在：

```text
note-single-lecture-work/Lecture 5. AI-Led Development/
```

包括：

- 抽取文本
- 渲染页图片
- `outline.json`
- `Lecture 5. AI-Led Development_思维导图.png`
- `Lecture 5. AI-Led Development_笔记生成提示词.md`
- 其他临时检查文件

最终课程笔记只放在：

```text
note-single-lecture/Lecture 5. AI-Led Development_课程笔记.md
```

## 关键规则

- 笔记必须按主题组织，不按 `Slide 1`、`Slide 2` 逐页整理。
- 关键术语保留英文名，例如 `AI 主导开发（AI-Led Development）`。
- 图示、截图、表格不能只略过，要解释其含义。
- 示例、练习、quiz、past-paper question 必须处理答案。
- 如果课件给了答案，必须完整保留原文答案，尤其编号列表、分点回答、`(a)` / `(b)` 子项等结构，然后再给中文翻译或解释。
- 如果课件没有答案，才写 `补充参考答案（Supplemental Reference Answer）`。
- 默认忽略非课程内容，例如开头讲师信息、结尾邮箱、论坛、Questions/Q&A 渠道。

## 依赖

推荐本机可用：

- Python 3
- Pillow
- `pdftotext`
- `pdftoppm`

其中思维导图渲染脚本位于：

```text
scripts/render_mindmap.py
```

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── lecture4-example.md
└── scripts/
    └── render_mindmap.py
```
