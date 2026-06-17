# note-single-lecture-skill

英方课复习 skill 合集仓库。根目录为 **note-single-lecture**（单讲笔记）；[`skills/`](skills/README.md) 目录含更多由 **Youhan Huang** 用 **Cursor Composer 2.5** 归纳的复习 workflow。

## Skill 一览

| Skill | 说明 |
|-------|------|
| [note-single-lecture](SKILL.md) | 单讲：思维导图 → 提示词 → 课程笔记 |
| [note-lecture-deep-dive](skills/note-lecture-deep-dive/SKILL.md) | 逐讲深度精讲，逻辑重排 |
| [note-exam-lecture-map](skills/note-exam-lecture-map/SKILL.md) | 课件 + 往年题考点权重 |
| [note-open-book-index](skills/note-open-book-index/SKILL.md) | 开卷索引（知识点 → 页码） |
| [note-qa-with-citation](skills/note-qa-with-citation/SKILL.md) | 问答/整卷，附课件页码 |

详见 [skills/README.md](skills/README.md)。

---

## note-single-lecture

把一个 lecture PDF/PPT 整理成：

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

## 推荐复习方式

生成课程笔记后，建议把最终笔记和原课件双开一起复习：

推荐生成笔记后不要只看笔记本身，而是和课件双开对照复习，这样更利于理解、记忆和背诵。

- 先看课程笔记，快速建立本讲的主题框架、关键概念和流程关系。
- 再回到原课件，核对图示、表格、示例题和原文答案的细节。
- 遇到示例、练习或带分点的原文答案时，以课件原文为准，用笔记中的中文解释辅助理解。
- 复习前期可以依赖笔记梳理结构；临近考试或提交作业前，应回到课件逐项确认要求没有遗漏。

这种方式可以避免只看整理后的笔记而忽略课件里的图示信息、英文术语和原始分点要求。

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
├── SKILL.md                          # note-single-lecture（根 skill）
├── skills/
│   ├── README.md                     # skill 索引与选型指南
│   ├── note-lecture-deep-dive/
│   ├── note-exam-lecture-map/
│   ├── note-open-book-index/
│   └── note-qa-with-citation/
├── agents/
│   └── openai.yaml
├── references/
│   └── lecture4-example.md
└── scripts/
    └── render_mindmap.py
```

## 贡献者

| 贡献 | 作者 | 工具 |
|------|------|------|
| `note-single-lecture` 及脚本 | 仓库维护者 | — |
| `skills/` 下扩展 workflow | Youhan Huang | Cursor Composer 2.5 |
