# Medical Journal Matcher

Evidence-backed journal selection for biomedical and life-science manuscripts.

<p align="center">
  <a href="#zh-cn">简体中文</a> · <a href="#english">English</a>
</p>

---

<a id="zh-cn"></a>

## 简体中文

### 项目简介

Medical Journal Matcher 是一个面向生物医学与生命科学英文稿件的智能选刊 Skill。它根据稿件主题、研究设计、研究对象和投稿要求，筛选并比较候选期刊，生成有来源、可解释、可人工复核的选刊建议。

它解决的是“哪些期刊更值得优先考虑”，而不是预测录用率或保证录用。

### 核心功能

- **稿件画像**：从标题、摘要、关键词或本地稿件中提取研究主题、方法、对象、投稿格式和研究设计。
- **硬条件筛选**：核验 WoS 索引、JCR 分区、完全 OA、投稿格式、APC 预算和期刊状态。
- **真实证据匹配**：结合期刊官方 Aims & Scope、投稿指南和近三年相似论文判断匹配程度。
- **可解释评分**：分别展示期刊匹配分、评分覆盖度和证据置信度。
- **投稿梯度**：将符合条件的期刊分为“冲刺、优先、相对稳妥”，但不把梯度解释为录用概率。
- **稿件就绪度检查**：在信息足够时检查结构、图表、报告规范和可识别的投稿准备问题；结果不混入期刊匹配分。
- **双格式输出**：生成中文 Markdown 决策报告，并可提供符合 Schema `1.0.0` 的 JSON 数据。

### 主要特色

#### 证据优先

所有关键结论都应有来源。JIF、JCR 分区、OA、APC、DOI、投稿范围或出版速度无法确认时，系统会标记为 `UNVERIFIED`，不会猜测。

#### 先筛选，再排序

硬条件必须先通过。任一硬条件失败的期刊会被排除；存在未核验硬条件的期刊只进入“待核验候选”，不会进入正式推荐榜单。

#### 三类结果相互独立

- **期刊匹配分**：稿件与期刊是否契合。
- **证据置信度**：当前结论有多少可靠证据支持。
- **稿件就绪度**：稿件是否已准备好投稿。

高匹配分不代表高录用率，也不能掩盖证据不足。

#### 隐私优先

默认使用 `LOCAL_PARSE_ONLY`：完整稿件只在本地解析。外部检索仅使用允许的结构化主题、方法、研究设计和对象，不发送完整稿件、作者身份、单位、患者标识或未公开的精确结果。

#### 如实处理 JCR 数据

没有合法 JCR 数据时，系统使用 `PUBLIC` 模式，将 JCR 条件标为 `UNVERIFIED`。它不会用 CiteScore、SJR 或其他指标冒充 JIF/JCR。

### 工作流程

1. 读取用户已经提供的稿件信息和投稿要求。
2. 在本地解析稿件并生成结构化 Manuscript Profile。
3. 确认投稿格式、JCR 类别等关键歧义。
4. 检索相似论文并建立候选期刊池。
5. 归一化期刊名称和 ISSN，核验官方资料。
6. 执行硬条件筛选、确定性评分和证据置信度计算。
7. 输出正式梯度、待核验候选、排除原因和人工复核建议。

### 快速开始

环境要求：Python 3.12+、[uv](https://docs.astral.sh/uv/) 和 Git。

```powershell
git clone git@github.com:17ayyy/medical-journal-matcher.git
Set-Location medical-journal-matcher
uv sync
Copy-Item .env.example .env
uv run pytest
```

如需让 Codex 自动发现该 Skill，请将仓库放在 Codex Skills 目录下，并在新任务中调用 `$medical-journal-matcher`。

### 配置

`.env.example` 提供了安全默认值：

```dotenv
JOURNAL_MATCHER_JCR_DATA_MODE=PUBLIC
JOURNAL_MATCHER_PRIVACY_MODE=LOCAL_PARSE_ONLY
JOURNAL_MATCHER_LOG_LEVEL=INFO
```

API 密钥和联系邮箱只在启用对应数据源时填写。`.env` 已加入 `.gitignore`，请勿提交密钥或稿件内容。

### 使用示例

#### 示例 1：根据摘要推荐期刊

```text
$medical-journal-matcher

请根据下面的英文摘要推荐生物医学期刊。要求：
- 当前为 SCIE；
- 目标 JCR Q1–Q2；
- 不强制完全 OA；
- 投稿格式为 Original Article；
- 优先考虑首轮决定较快的期刊。

Title: ...
Abstract: ...
Keywords: ...
```

#### 示例 2：为病例报告筛选期刊

```text
$medical-journal-matcher

这是一篇心血管病例报告。请只保留官网明确接收 Case Report、当前仍正常收稿且为完全 OA 的期刊。APC 硬预算为 2,000 USD；无法核验费用的期刊请放入待核验列表。
```

#### 示例 3：比较已有候选名单

```text
$medical-journal-matcher

请比较以下期刊与我的诊断准确性研究是否匹配：Journal A、Journal B、Journal C。重点核验 STARD 相关性、近三年相似论文、投稿格式和 JCR 分区，并说明每本期刊的优势、风险和待核验项。
```

#### 示例 4：没有 JCR 授权数据

```text
$medical-journal-matcher

我暂时无法提供 JCR 数据。请使用公开数据模式生成内容匹配候选，并明确列出需要我在 JCR 中人工核验的类别和分区信息。
```

### 本地工具

仓库内已提供一组确定性基础工具：

```powershell
# 本地解析 TXT、Markdown、PDF 或 DOCX；只输出文件名和字符数，不回显正文
uv run journal-matcher parse manuscript.docx

# 规范化并检查 DOI 语法；语法通过不等于 DOI 已在线解析
uv run journal-matcher validate-doi "https://doi.org/10.1000/example"

# 校验机器输出的 Schema 和正式推荐约束
uv run journal-matcher validate-output result.json
```

### 当前状态

项目目前处于 **MVP 基础结构阶段**。已完成：

- Skill 入口和双语交互边界；
- 隐私 allowlist 与安全默认配置；
- 硬门槛状态机；
- DOI/ISSN 规范化；
- 缺失数据感知的评分与置信度计算；
- PDF/DOCX/TXT/Markdown 本地解析基础；
- 输出 Schema、语义校验和首批离线测试；
- 外部数据源适配器接口。

OpenAlex、PubMed、Crossref、DOAJ、NLM Catalog、期刊官网和授权 JCR 的完整在线适配器，以及 PRD 中 A01–A18 的全部验收用例仍需继续实现。

### 项目结构

```text
medical-journal-matcher/
├── SKILL.md                  # Skill 入口与核心规则
├── agents/openai.yaml        # Codex 展示与调用策略
├── references/               # 工作流、隐私、数据源、评分和输出规范
├── config/                   # 版本化评分配置
├── src/medical_journal_matcher/
│   ├── adapters/             # 外部数据源接口
│   ├── gates.py              # 硬门槛状态机
│   ├── scoring.py            # 确定性评分与置信度
│   ├── privacy.py            # 对外查询字段 allowlist
│   └── validation.py         # 输出校验
├── scripts/                  # 可重复执行的命令行工具
├── tests/                    # 离线测试
├── pyproject.toml            # Python 与 uv 配置
└── PRD.md                    # 产品需求基线
```

完整产品规则请阅读 [PRD.md](PRD.md)，Skill 运行规则请阅读 [SKILL.md](SKILL.md)。

[返回语言选择](#medical-journal-matcher)

---

<a id="english"></a>

## English

### Overview

Medical Journal Matcher is a journal-selection Skill for English biomedical and life-science manuscripts. It uses manuscript topics, study design, research objects, and submission requirements to screen and compare journals, then produces source-backed recommendations that users can review.

It helps answer “Which journals should I consider first?” It does not predict acceptance or guarantee publication.

### Core capabilities

- **Manuscript profiling**: Extract topics, methods, research objects, submission format, and study design from a title, abstract, keywords, or a locally parsed manuscript.
- **Hard-constraint screening**: Verify WoS index, JCR quartile, full OA status, submission format, APC budget, and journal status.
- **Evidence-backed matching**: Use official Aims & Scope, author guidelines, and similar articles from the latest three years.
- **Explainable scoring**: Report journal match score, score coverage, and evidence confidence separately.
- **Submission tiers**: Group eligible journals into Sprint, Priority, and Relatively Safe tiers without treating them as acceptance probabilities.
- **Readiness audit**: Check structure, figures, reporting guidelines, and observable submission-preparation issues when enough content is available. Readiness does not affect journal match scores.
- **Two output formats**: Produce a Chinese Markdown decision report and optional JSON that follows Schema `1.0.0`.

### What makes it different

#### Evidence first

Material claims require sources. If JIF, JCR quartile, OA, APC, DOI, scope, submission policy, or publication speed cannot be verified, the value remains `UNVERIFIED` instead of being guessed.

#### Screen before ranking

Hard constraints are evaluated first. A failed gate excludes a journal. An unverified enabled gate moves it to the unverified list, never into the formal ranking.

#### Three separate results

- **Match score**: How well the manuscript fits the journal.
- **Evidence confidence**: How strongly current evidence supports the conclusion.
- **Manuscript readiness**: How prepared the manuscript is for submission.

A high match score is not an acceptance probability and cannot hide weak evidence.

#### Privacy by default

The default mode is `LOCAL_PARSE_ONLY`: full manuscripts stay in local parsing. External searches use only approved structured topics, methods, designs, and research objects. They do not receive manuscript text, author identities, affiliations, patient identifiers, or unpublished exact results.

#### Honest JCR handling

Without licensed or authorized JCR data, the Skill runs in `PUBLIC` mode and marks the JCR gate as `UNVERIFIED`. It never presents CiteScore, SJR, or another metric as JIF/JCR.

### How it works

1. Reuse the manuscript information and constraints already provided.
2. Parse the manuscript locally and build a structured Manuscript Profile.
3. Confirm material ambiguity in submission format or JCR categories.
4. Retrieve similar articles and build a journal candidate pool.
5. Normalize journal identity and verify official facts.
6. Apply hard gates, deterministic scoring, and evidence-confidence rules.
7. Return formal tiers, unverified candidates, exclusions, and manual checks.

### Quick start

Requirements: Python 3.12+, [uv](https://docs.astral.sh/uv/), and Git.

```powershell
git clone git@github.com:17ayyy/medical-journal-matcher.git
Set-Location medical-journal-matcher
uv sync
Copy-Item .env.example .env
uv run pytest
```

To make the Skill discoverable by Codex, place the repository in your Codex Skills directory and invoke `$medical-journal-matcher` in a new task.

### Configuration

`.env.example` starts with safe defaults:

```dotenv
JOURNAL_MATCHER_JCR_DATA_MODE=PUBLIC
JOURNAL_MATCHER_PRIVACY_MODE=LOCAL_PARSE_ONLY
JOURNAL_MATCHER_LOG_LEVEL=INFO
```

Add API keys or contact emails only for data sources you enable. `.env` is ignored by Git; never commit credentials or manuscript content.

### Usage examples

#### Example 1: Recommend journals from an abstract

```text
$medical-journal-matcher

Recommend biomedical journals for the English abstract below. Requirements:
- currently indexed in SCIE;
- target JCR Q1–Q2;
- full OA is not required;
- submission format is Original Article;
- prefer journals with a shorter time to first decision.

Title: ...
Abstract: ...
Keywords: ...
```

#### Example 2: Screen journals for a case report

```text
$medical-journal-matcher

This is a cardiovascular case report. Keep only active, fully OA journals whose current author guidelines clearly accept Case Reports. The hard APC budget is USD 2,000. Put journals with unverifiable fees in the unverified list.
```

#### Example 3: Compare an existing shortlist

```text
$medical-journal-matcher

Compare Journal A, Journal B, and Journal C for my diagnostic-accuracy study. Focus on STARD relevance, similar articles from the latest three years, submission format, and JCR quartile. Explain each journal's strengths, risks, and facts that still need manual verification.
```

#### Example 4: Work without licensed JCR data

```text
$medical-journal-matcher

I cannot provide JCR data yet. Use public-data mode to create a content-fit shortlist and clearly list the JCR categories and quartiles I need to verify manually.
```

### Local utilities

The repository includes deterministic foundation tools:

```powershell
# Parse TXT, Markdown, PDF, or DOCX locally; report only file name and character count
uv run journal-matcher parse manuscript.docx

# Normalize and validate DOI syntax; syntax validity does not prove online resolution
uv run journal-matcher validate-doi "https://doi.org/10.1000/example"

# Validate machine output against the schema and formal-recommendation rules
uv run journal-matcher validate-output result.json
```

### Current status

The project is currently at the **MVP foundation stage**. The repository already includes:

- the Skill entry point and bilingual interaction boundaries;
- a privacy allowlist and safe defaults;
- the hard-gate state machine;
- DOI/ISSN normalization;
- missing-data-aware score and confidence calculations;
- foundational local PDF/DOCX/TXT/Markdown parsing;
- output schema, semantic validation, and initial offline tests;
- external data-source adapter interfaces.

Full online adapters for OpenAlex, PubMed, Crossref, DOAJ, NLM Catalog, journal websites, and authorized JCR data—as well as the complete A01–A18 acceptance suite in the PRD—remain to be implemented.

### Project structure

```text
medical-journal-matcher/
├── SKILL.md                  # Skill entry point and core rules
├── agents/openai.yaml        # Codex UI and invocation policy
├── references/               # Workflow, privacy, sources, scoring, and output rules
├── config/                   # Versioned scoring configuration
├── src/medical_journal_matcher/
│   ├── adapters/             # External data-source interfaces
│   ├── gates.py              # Hard-gate state machine
│   ├── scoring.py            # Deterministic scoring and confidence
│   ├── privacy.py            # Outbound-query field allowlist
│   └── validation.py         # Output validation
├── scripts/                  # Repeatable command-line utilities
├── tests/                    # Offline tests
├── pyproject.toml            # Python and uv configuration
└── PRD.md                    # Product requirements baseline
```

Read [PRD.md](PRD.md) for the complete product rules and [SKILL.md](SKILL.md) for runtime behavior.

[Back to language selection](#medical-journal-matcher)
