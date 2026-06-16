# Lecture 4 Example Pattern

Use this reference when a user asks for the same workflow on another lecture.

## Source Example

- Source PDF: `Lecture 4. Production and Management.pdf`
- User-provided mind map style: one root with major branches for course info, production process, agile management, version control, collaborative coding, global community, and practice requirements.
- Intermediate artifacts folder: `note-single-lecture-work/Lecture 4. Production and Management/`
- Final notes folder: `note-single-lecture/`
- Final notes: `note-single-lecture/Lecture 4. Production and Management_课程笔记.md`

## Successful Final Structure

```markdown
# Lecture 4：生产与管理（Production and Management）

## 课程基础信息
## 整体生产流程（Production Process）
## 一、敏捷管理（Agile Management）
### 传统模式：瀑布式管理（Waterfall Management）
### 统一流程：迭代增量式开发（Unified Process / Iterative and Incremental Development）
### 敏捷项目管理图示（Agile Project Management）
### 看板（Kanban）
### 不要一开始目标过高（Don’t be too ambitious）
### 敏捷优势（Benefits of Agile）
### 实验课中的敏捷实践（Your Agile Practice in Labs）
## 二、版本控制（Version Control）
### 核心工具：GitHub
### 版本控制的核心价值
### 项目开发图示（Project Development）
### Git/GitHub 专业术语（Git/GitHub Terminologies）
### Git 操作关系（Git Commands Diagram）
### GitHub 比较代码（GitHub – Compare Code）
### 分支与合并（Branch and Merge）
### 合并策略（Merge Strategies）
### Issues：问题、需求和任务追踪
## 三、协作编码（Collaborative Coding）
### 协作角色
### 协作流程 1：优化他人项目
### 协作流程 2：同步他人更新
### PR 作为质量关卡（Pull Requests as Quality Gates）
### GitHub 中的 Kanban
### GitHub 学生开发者包（GitHub Student Developer Pack）
## 四、全球开源社区（Global Community）
### GitHub 不只是版本控制服务
### 主流开源平台对比
### GitHub 平台规模（Scale of GitHub）
### 编程语言生态（Programming Languages）
### GitHub 作为数字图书馆（GitHub as a Digital Library）
### GitHub 作品集（GitHub Portfolio）
## 五、课程实践要求
## 六、重点对比总结
## 七、考试与复习重点
```

## Style Rules That Worked

- Do not create `## Slide N` sections.
- Use Chinese explanations throughout.
- Keep English names inside parentheses for important terms:
  - 敏捷管理（Agile Management）
  - 版本控制（Version Control）
  - 拉取请求（Pull Request, PR）
  - 合并冲突（Merge Conflict）
- Explain diagrams as concepts:
  - Green/red project nodes as main line, branch, and merge.
  - Git commands diagram as working directory, staging area, local repository, remote repository.
  - GitHub search screenshot as digital library search with filters such as stars, repositories, issues, pull requests.
- Treat examples, exercises, questions, and past-paper items explicitly:
  - If the lecture provides an English answer, include the English answer and a Chinese translation.
  - If the lecture does not provide an answer, create `补充参考答案（Supplemental Reference Answer）` with both English and Chinese versions.
- Include a comparison table for confusing terms.
- Highlight important points with `==注意：...==`.

## Prompt Pattern

The generated prompt should tell the agent to:

1. Use the lecture PDF and generated PNG mind map.
2. Organize by the mind map’s theme hierarchy, not slides.
3. Cover every lecture theme, diagram, workflow, definition, and example.
4. Include bilingual answer treatment for examples/exercises/questions: existing English answers plus Chinese translations, or bilingual supplemental reference answers when missing.
5. Write Chinese explanations and keep English term names.
6. Put intermediate artifacts in `note-single-lecture-work/<pdf-stem>/`.
7. Produce final notes as `note-single-lecture/<pdf-stem>_课程笔记.md`.
8. Copy the final Markdown to clipboard when the user wants Feishu-ready notes.
