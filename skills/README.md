# Skills Catalog

英方课复习 skill 合集。除根目录 `note-single-lecture` 外，本目录收录 Youhan Huang 基于 **Cursor Composer 2.5** 实际复习流程整理的扩展 skill。

| Skill | 路径 | 适用场景 | 典型输出 |
|-------|------|----------|----------|
| **note-single-lecture** | [`../SKILL.md`](../SKILL.md) | 单讲高精度笔记：思维导图 → 提示词 → 课程笔记 | `note-single-lecture/<stem>_课程笔记.md` |
| **note-lecture-deep-dive** | [`note-lecture-deep-dive/SKILL.md`](note-lecture-deep-dive/SKILL.md) | 逐讲深度精讲，逻辑重排，动态深度 | `<Course>_L<n>_精讲.md` |
| **note-exam-lecture-map** | [`note-exam-lecture-map/SKILL.md`](note-exam-lecture-map/SKILL.md) | 课件逐页概括 + 往年题考点权重 | `exam_lecture_stat.md` |
| **note-open-book-index** | [`note-open-book-index/SKILL.md`](note-open-book-index/SKILL.md) | 开卷考试：知识点 → 页码索引 + 押题 | `revision_exam.md` |
| **note-qa-with-citation** | [`note-qa-with-citation/SKILL.md`](note-qa-with-citation/SKILL.md) | 问答 / 整卷作答，严格附课件页码 | `answer.md` |

## 如何选择

```text
只复习某一讲、要高质量中文笔记     → note-single-lecture
要彻底吃透几讲、愿意读长文精讲     → note-lecture-deep-dive
考前盘考点、对照往年题             → note-exam-lecture-map
开卷考、考场只要页码不要解释       → note-open-book-index
零散问题或整卷练习、要溯源         → note-qa-with-citation
```

## 安装到 Cursor

将整个仓库 clone 到本地后，把需要的 skill **子目录** 复制或链接到 Cursor skills 目录：

```powershell
# 示例：安装 deep-dive skill
Copy-Item -Recurse "D:\Study\skill\note-single-lecture-skill\skills\note-lecture-deep-dive" `
  "$env:USERPROFILE\.cursor\skills\note-lecture-deep-dive"
```

根目录 `note-single-lecture` 安装方式见 [README.md](../README.md)。

## 作者与工具

| 字段 | 值 |
|------|-----|
| **扩展 skill 作者** | Youhan Huang |
| **开发工具** | Cursor Composer 2.5 |
| **来源** | 从 `D:\Study\大三\` 多门课真实复习 prompt 归纳 |
| **根 skill** | 仓库原作者维护的 `note-single-lecture` |

## 已验证课程

| Skill | 课程 |
|-------|------|
| note-single-lecture | 交互式媒体设计 (Lecture 4 等) |
| note-lecture-deep-dive | 数字音频基础, 图形与视频处理 |
| note-exam-lecture-map | 交互式媒体设计, 数字音频基础 |
| note-open-book-index | 软件工程 |
| note-qa-with-citation | 图形与视频处理, 外国文学鉴赏 |
