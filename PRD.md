# Medical Journal Matcher Skill 产品需求文档

| 项目 | 内容 |
|---|---|
| 产品名称 | Medical Journal Matcher |
| Skill 名称 | medical-journal-matcher |
| 文档版本 | 0.1.0 |
| 文档状态 | MVP 开发基线 |
| 日期 | 2026-09-15 |
| 主要用户 | 需要为英文 SCI 稿件选刊的中国科研人员 |
| 首期领域 | 生物医学与生命科学 |
| 默认输出 | 中文决策报告 + 英文原始元数据 |

## 1. 文档目的

本文档定义 Medical Journal Matcher Skill 第一版的产品范围、交互流程、数据边界、筛选与评分逻辑、输出结构、失败降级策略及验收标准，作为后续 Skill 设计、实现、测试与评审的统一依据。

本版本只定义产品需求，不包含 Skill 的实际代码实现。

## 2. 产品摘要

Medical Journal Matcher 是一个面向中国科研人员的英文 SCI 选刊 Skill。它读取用户提供的标题、摘要、关键词或完整稿件，在不默认向外部服务上传完整稿件的前提下，提取研究主题、方法、研究对象、投稿格式、研究设计和目标读者等结构化特征。

系统先根据用户设定的 WoS 索引、JCR 分区、开放获取类型、投稿格式和期刊状态执行资格筛选，再从近三年真实发表论文、期刊官方 Aims & Scope、投稿指南及可核验期刊元数据中构建证据，计算可解释的期刊匹配分。最终以“冲刺、优先、相对稳妥”三个投稿策略梯度输出候选期刊。

产品的核心定位是：

> 提供有来源、可复核的候选期刊检索、相对匹配排序和投稿决策支持，而不是预测或保证录用。

## 3. 背景与问题

科研人员选刊时通常需要同时处理以下问题：

- 稿件研究方向是否属于期刊真实关注范围。
- 期刊近期是否发表过研究对象、方法和贡献类型相近的论文。
- 期刊是否接收当前 submission_format。
- JCR 分区、开放获取和出版节奏是否符合投稿目标。
- 期刊官网、投稿指南、ISSN、出版商和指标信息是否仍然有效。
- 所谓“推荐期刊”是否建立在真实论文和可靠来源上，而不是模型猜测。

现有选刊工具常见局限包括：

- 只做关键词相似度，不核验投稿格式、OA 或期刊状态。
- 直接使用历史发表期刊作为唯一“正确答案”，忽略一篇稿件可适合多本期刊。
- 大型综合刊因发文量大而在相似论文统计中占优。
- 将写作质量、图表质量与期刊方向匹配混为一个分数。
- 在数据缺失时生成看似精确的 IF、分区或审稿周期。
- 将匹配排名暗示为录用概率。

本产品通过“资格门槛—证据检索—匹配评分—置信度—投稿梯度”的分层设计解决上述问题。

## 4. 产品目标

### 4.1 MVP 目标

1. 支持生物医学与生命科学英文稿件选刊，并能细分到超声医学、急诊医学等专科方向。
2. 支持标题、摘要、关键词和完整稿件等多种输入形态。
3. 支持六类用户场景：原始研究、系统综述/Meta-analysis、临床试验、诊断准确性研究、病例报告/病例系列、方法学论文；实现时将投稿格式与研究设计分轴建模。
4. 支持 JCR 分区和完全 OA 硬约束，以及出版节奏、出版社等软偏好。
5. 为每本正式推荐期刊提供近三年内最多 5 篇真实相似论文及可解析 DOI。
6. 输出可解释的 100 分期刊匹配分、分项得分、评分覆盖度和独立的证据置信度。
7. 将稿件就绪度作为独立轻量预检，不混入期刊匹配分。
8. 输出“冲刺 3 本、优先 3–4 本、相对稳妥 1–2 本”的默认候选结构；证据不足时不强行凑数。
9. 所有关键事实均带来源、查询日期和验证状态。
10. 在没有合法 JCR 数据时诚实降级，不用 CiteScore、SJR 或其他指标冒充 JIF/JCR 分区。

### 4.2 成功结果

用户完成一次交互后，应能：

- 看懂系统如何理解自己的研究。
- 快速排除明显不符合硬条件的期刊。
- 从真实相似论文判断期刊是否持续发表同类工作。
- 了解每本候选刊的推荐理由、投稿优势、风险和待核验项。
- 得到一份可供作者团队讨论和人工复核的投稿顺序建议。

## 5. 非目标

MVP 不提供以下能力：

- 不预测录用率，不输出“录用概率”。
- 不承诺任何期刊能够录用稿件。
- 不代替同行评审、统计审查、科研诚信审查或正式语言润色。
- 不在无授权来源时提供或推断 JCR 分区、JIF 数值。
- 不把 CiteScore、SJR、SNIP 等指标标记成 JIF 或 JCR 分区。
- 不自动向期刊投稿，不代替作者完成投稿账户操作。
- 不自动推荐叙述性综述、Letter 或 Commentary；这些类型留待后续版本。
- 不在第一版覆盖工程、人文或社会科学。
- 不以“未被 DOAJ、MEDLINE 或某一数据库收录”单独判定期刊为掠夺性期刊。
- 不长期保存或再分发受版权保护的论文摘要、全文或许可不明的数据。

## 6. 用户与核心场景

### 6.1 目标用户

首要用户是准备投稿英文 SCI 论文的中国生物医学与生命科学研究人员，包括研究生、临床医生、科研人员和课题负责人。

### 6.2 核心用户故事

- 作为作者，我希望上传摘要和关键词，得到与研究内容匹配且满足目标 JCR 分区的期刊清单。
- 作为临床研究者，我希望系统识别我的研究设计和患者人群，而不是只匹配疾病名称。
- 作为病例报告作者，我希望候选刊经过“是否接收病例报告”的硬性检查。
- 作为希望开放获取的作者，我希望结果只包含可验证的完全 OA 期刊。
- 作为关注投稿周期的作者，我希望看到不同时间指标的定义和来源，而不是一个含义不明的“出版快”。
- 作为完整稿件作者，我希望额外得到轻量投稿就绪度预检，但不让语言问题扭曲期刊方向匹配。
- 作为没有 JCR 数据授权的用户，我希望系统明确告诉我哪些候选需要人工核验，而不是伪造分区。

## 7. 产品原则

### 7.1 证据优先

推荐必须由期刊官方信息、可验证元数据和真实相似论文支撑。无法验证的事实显示为“未知”或“待核验”，不得补写或猜测。

### 7.2 先资格筛选，再匹配排序

WoS 索引、JCR 分区、OA、投稿格式和期刊状态属于资格门槛。任何明确不满足的硬约束不得通过其他高分抵消。

### 7.3 三个概念严格分离

- **期刊匹配分**：稿件与期刊的内容和投稿定位是否匹配。
- **证据置信度**：当前推荐由多少、何种质量和一致性的证据支持。
- **稿件就绪度**：稿件当前是否具备投稿准备度。

三者必须分别计算、分别展示。

### 7.4 不把推荐解释为录用预测

“冲刺、优先、相对稳妥”只是投稿策略标签。它们不对应录用概率，不构成录用保证。

### 7.5 隐私最小化

完整稿件默认仅在本地解析。外部数据库只接收经过脱敏和压缩的检索词或结构化研究特征。

### 7.6 不以缺失数据制造精确感

未知不等于符合，也不等于不符合。系统必须明确区分 FAIL、UNVERIFIED 和数据缺失。

### 7.7 “SCI”与 JCR 的产品定义

本产品将用户口语中的“SCI 期刊”默认解释为当前被 Science Citation Index Expanded（SCIE）收录的期刊。JCR 分区、是否拥有 JIF 和是否属于 SCIE 是相关但不同的事实，必须分别核验。

- required_wos_indexes 默认值为 [SCIE]。
- ESCI 不自动视为满足 SCIE 要求。
- 用户可以明确改变索引要求，但报告必须显示实际采用的索引。
- WoS 索引状态是独立硬门槛；JCR 分区是另一独立硬门槛。
- 无法验证当前索引时，状态为 UNVERIFIED。

## 8. MVP 范围

### 8.1 学科范围

MVP 覆盖生物医学与生命科学，并支持如下结构化层级：

- 一级领域，例如 clinical medicine、basic medicine、public health、life sciences。
- 二级或专科领域，例如 emergency medicine、ultrasound medicine、oncology、cardiology。
- 主题实体，例如疾病、器官、分子、生物过程、临床问题或技术对象。

架构应保留领域适配器，未来可增加工程等其他学科，但不得在首版输出中宣称已覆盖。

### 8.2 稿件分类

MVP 支持六类用户场景：

1. 原始研究。
2. 系统综述/Meta-analysis。
3. 临床试验。
4. 诊断准确性研究。
5. 病例报告/病例系列。
6. 方法学论文。

这六类并非互斥的单一枚举。例如临床试验通常同时属于 original article，诊断准确性研究也可以是原始研究。实现必须拆为三个轴：

- **submission_format**：用于核验期刊是否接收该投稿格式，是硬门槛。
- **study_design[]**：用于方法与研究设计匹配，可以多选。
- **reporting_guideline[]**：用于稿件就绪度检查，可以多选。

MVP 映射基线：

| 用户场景 | submission_format | study_design[] 示例 | reporting_guideline[] |
|---|---|---|---|
| 原始研究 | ORIGINAL_ARTICLE | COHORT、CASE_CONTROL、CROSS_SECTIONAL、EXPERIMENTAL 等 | STROBE、ARRIVE 或适用规范 |
| 系统综述/Meta-analysis | REVIEW_ARTICLE | SYSTEMATIC_REVIEW、META_ANALYSIS | PRISMA |
| 临床试验 | ORIGINAL_ARTICLE | CLINICAL_TRIAL，可与 RANDOMIZED_CONTROLLED_TRIAL 并存 | CONSORT |
| 诊断准确性研究 | ORIGINAL_ARTICLE | DIAGNOSTIC_ACCURACY | STARD |
| 病例报告/病例系列 | CASE_REPORT 或 CASE_SERIES | CASE_REPORT、CASE_SERIES | CARE 或适用规范 |
| 方法学论文 | METHODS_ARTICLE；期刊仅使用 ORIGINAL_ARTICLE 时需映射 | METHOD_DEVELOPMENT、METHOD_VALIDATION | 领域适用规范 |

官方投稿指南中的 Research Article、Original Research、Original Investigation 等别名应映射到统一 submission_format。别名映射必须保留原始术语、来源页面和映射置信度；无法确认时门槛为 UNVERIFIED。

用户可以直接指定场景。若未指定，系统可以推断三个轴，但必须展示推断结果和置信度。submission_format 低置信度或存在冲突时，应请求用户确认后再执行投稿格式硬筛选。

### 8.3 输入载体

支持：

- 标题。
- 摘要。
- 关键词。
- 可复制文本。
- Markdown 或纯文本文件。
- 完整 Manuscript 文件；开发阶段优先支持 PDF 和 DOCX。

扫描型 PDF、复杂公式和嵌入式补充材料的完整解析不作为 MVP 必须能力。解析失败时，应允许用户粘贴标题、摘要和关键词继续。

## 9. 用户输入

### 9.1 标准输入

标准输入为：

- 英文标题。
- 英文摘要。
- 英文关键词。
- 研究领域或专科。
- Web of Science 索引要求；默认 SCIE。
- 目标 JCR 分区或允许的分区集合。
- OA 要求。
- 出版节奏偏好。

### 9.2 最低输入与置信度

| 输入完整度 | 是否允许运行 | 默认输入充分度 |
|---|---:|---|
| 完整稿件 + 标题 + 摘要 + 关键词 | 是 | High |
| 标题 + 摘要 + 关键词 | 是，标准模式 | Medium–High |
| 摘要 + 关键词 | 是 | Medium |
| 仅摘要 | 是 | Low–Medium |
| 仅标题或仅关键词 | 可生成探索性结果 | Low；不得输出高置信度正式结论 |

输入不充分时，不得假设未提供的方法、图表、统计或研究设计信息。

### 9.3 约束输入模型

| 字段 | 类型 | 默认性质 | 说明 |
|---|---|---|---|
| required_wos_indexes | 数组 | 硬约束 | 默认 [SCIE]；ESCI 不自动等同于用户口语中的“SCI” |
| target_jcr_quartiles | 数组 | 硬约束 | 例如 Q1，或 Q1–Q2 |
| target_jcr_categories | 数组/空 | 硬约束的一部分 | 用户可指定；未指定时根据稿件领域映射并确认 |
| jcr_category_match_policy | 枚举 | 硬约束的一部分 | ANY 或 ALL；默认 ANY，但只作用于已确认的相关类别 |
| jcr_release_year | 整数/AUTO | 硬约束的一部分 | 默认 AUTO，使用运行时最新合法可用版本 |
| oa_requirement | 枚举 | 硬约束 | REQUIRED_FULL_OA 或 NO_REQUIREMENT |
| submission_format | 枚举 | 硬约束 | ORIGINAL_ARTICLE、REVIEW_ARTICLE、CASE_REPORT、CASE_SERIES、METHODS_ARTICLE |
| study_designs | 数组 | 匹配条件 | 可多选，例如 CLINICAL_TRIAL、DIAGNOSTIC_ACCURACY |
| reporting_guidelines | 数组 | 就绪度条件 | 可多选，例如 CONSORT、PRISMA、STARD、CARE |
| publication_speed | 对象 | 软偏好 | 首轮决定、投稿到接受、接受到在线、出版频率 |
| publisher_preferences | 数组 | 软偏好 | 偏好而非默认排他条件 |
| preferred_journals | 数组 | 候选种子 | 用户希望比较的期刊 |
| excluded_journals | 数组 | 排除条件 | 曾拒稿或不希望再考虑的期刊 |
| excluded_publishers | 数组 | 排除条件 | 仅在用户明确指定时生效 |
| apc_budget | 金额/空 | 可选条件 | 包含金额和货币 |
| apc_budget_mode | 枚举 | 可选条件 | HARD、SOFT 或 OFF；默认 OFF |
| publication_language | 字符串 | 默认 English | 期刊接收语言 |
| tier_counts | 对象 | 输出偏好 | 默认 3/3/1，上限为 3/4/2 |
| readiness_audit_mode | 枚举 | 独立模块 | OFF、AUTO 或 ON；默认 AUTO |
| privacy_mode | 枚举 | 隐私 | LOCAL_PARSE_ONLY、MODEL_ASSISTED_WITH_CONSENT 或 OFFLINE_ONLY；默认 LOCAL_PARSE_ONLY |

### 9.4 出版节奏字段

必须分开记录：

- submission_to_first_decision。
- submission_to_acceptance。
- acceptance_to_online_publication。
- publication_frequency。

不得用 publication frequency 代替审稿或录用速度。

每个速度值都必须带：

- value 与 unit。
- definition。
- statistic，例如 median、mean 或 publisher-reported。
- sample_n；未知则为 null。
- source_url。
- checked_at。
- evidence_method，例如 official statement 或 article-history estimate。

不同定义或统计口径的数据不得直接生成跨刊精确排名。

### 9.5 Skill 触发边界

当用户表达以下意图且稿件属于生物医学或生命科学时，应考虑调用本 Skill：

- 为英文论文推荐投稿期刊或 target journal。
- 比较若干期刊与稿件的匹配程度。
- 根据摘要、关键词或全文寻找相似研究实际发表的期刊。
- 按 WoS、JCR、OA、投稿格式或出版节奏筛选候选刊。
- 对既有选刊清单进行有证据的复核和排序。

以下情况不应直接进入完整匹配流程：

- 用户只要求润色、改写或翻译论文。
- 用户只查询单一期刊的一个客观字段。
- 稿件明确属于工程、人文或社会科学等 MVP 未覆盖领域。
- 用户要求预测录用概率、保证录用或绕过期刊正常审稿。

建议的 Skill 描述应明确“生物医学与生命科学”“证据驱动选刊”“不预测录用”三个边界，避免被泛化为所有学科的期刊数据库。

MVP 默认允许隐式调用：

~~~yaml
policy:
  allow_implicit_invocation: true
~~~

建议 frontmatter description：

> Recommend and compare evidence-backed target journals for English biomedical and life-science manuscripts using manuscript fit, recent similar articles, and verified submission constraints. Use for journal selection or shortlist review; do not use for acceptance prediction or non-biomedical fields.

### 9.6 Intake 交互协议

Skill 首次响应应先复用用户已经提供的信息，只追问缺失且会改变结果的字段。不得要求用户重复粘贴已上传内容。

推荐的最小 Intake 顺序：

1. 确认输入载体是否足以提取标题、摘要和关键词。
2. 获取或推断研究领域与专科。
3. 将用户场景映射为 submission_format、study_designs 和 reporting_guidelines，并在投稿格式低置信度时确认。
4. 确认 required_wos_indexes；默认要求 SCIE。
5. 获取目标 JCR 分区和相关类别；类别可先自动映射，但进入正式筛选前必须确认。
6. 确认 OA 为 REQUIRED_FULL_OA 或 NO_REQUIREMENT。
7. 收集出版节奏和出版社软偏好。
8. 收集偏好期刊、排除期刊、APC 预算和梯度数量等可选项。
9. 告知当前 JCR 数据模式以及它对正式推荐的影响。

若用户输入已经完整，Skill 应直接生成稿件画像并开始检索，不为形式完整而重复提问。若某项只影响软偏好，可使用明确默认值继续运行并在报告中披露；硬约束不明确时不得擅自假设。

在检索前，Skill 应用简短结构化摘要向用户展示：

- 识别出的研究问题。
- submission_format、study_designs 和适用报告规范。
- 主要方法与对象。
- 启用的硬约束。
- 使用的 jcr_data_mode 与 privacy_mode。

仅当上述内容存在实质性歧义时暂停等待确认。

## 10. 隐私与数据处理

### 10.1 默认隐私规则

本 PRD 中的“本地”专指用户设备或当前受控工作区内的确定性解析进程，不自动包含第三方学术 API、期刊网站或远程模型服务。

默认 LOCAL_PARSE_ONLY 模式要求：

1. 完整稿件只能由本地解析脚本读取。
2. 编排模型只接收允许字段构成的 Manuscript Profile，不接收全文、整段正文或可逆的长原文片段。
3. 第三方学术 API 和期刊网站只接收字段白名单生成的检索请求。
4. 不发送作者姓名、单位、邮箱、基金号、未公开患者标识、致谢、利益冲突信息或未公开的精确数值结果。
5. 不以原始标题、摘要或全文原句直接构造对外查询。
6. 日志、缓存、异常堆栈和重试队列不得保存完整稿件、原文片段或密钥。
7. 如果当前运行环境无法保证上述边界，应停止全文模式并请用户改用标题/摘要/关键词，或在披露接收方和内容后取得单独同意。

MODEL_ASSISTED_WITH_CONSENT 仅在用户针对本次运行明确同意后启用：

- 同意界面必须列出接收组件、使用目的、发送字段或章节、是否保留以及撤回方法。
- 只发送完成用户明确要求的分析所必需的最小片段。
- 稿件正文仍不得发送给 OpenAlex、PubMed、Crossref、DOAJ、期刊网站等第三方学术检索服务。
- consent_record 必须写入运行元数据，但不得包含正文。

用户选择 OFFLINE_ONLY 时：

- 不调用任何第三方学术 API 或网站。
- 只使用当前工作区中用户授权的本地数据。
- 若本地数据不足以完成新鲜度和来源核验，应输出能力不足，不生成看似完整的推荐。

平台本身对用户上传内容的处理受其产品条款和部署方式约束。Skill 不得把“未发送给学术 API”表述成“任何远程系统都未处理”；实施时必须在全文处理前向用户展示准确的信任边界。

### 10.2 对外检索查询

外部查询只允许由以下字段白名单生成：

- 主题与疾病/生物过程。
- 研究对象或人群。
- submission_format 和 study_designs。
- 核心方法、技术或成像模态。
- 归一化的主要结局类别或贡献类型；不含未公开精确数值。
- MeSH 词及必要同义词。

查询生成器必须执行字段 allowlist，而不是依赖自由文本“脱敏”。查询应删除身份信息、罕见可识别组合和无关背景。若外部服务限制文本长度，优先保留规范化的主题、设计、方法和对象，不直接截取稿件开头。

对于完整稿件模式，实现应支持在首次对外请求前展示 outbound query preview。测试环境必须能捕获所有网络请求 payload，并验证正常、重试、超时和异常路径均未泄漏禁止字段。

### 10.3 本地 Readiness 结果契约

LOCAL_PARSE_ONLY 下，readiness_audit_mode=AUTO 只执行本地可确定检查，例如：

- 章节、字数、摘要结构和参考文献交叉引用。
- 图表文件存在性、分辨率、尺寸、编号和正文引用一致性。
- 报告规范清单中的可定位项目是否出现。
- 明确可解析的统计报告字段和伦理/注册字段是否存在。

本地组件只能把以下结构化 ReadinessFinding 传给编排模型：

- check_id。
- category。
- severity。
- status。
- evidence_location。
- observed_value；不得包含长原文。
- expected_value。
- source_rule_id。
- limitation。

科学叙事、英文表达质量、语义层面的统计合理性和其他需要读取原文的定性判断，在默认模式下必须标为 NOT_ASSESSED。只有以下任一条件满足时才能执行：

- 有受信任的本地模型在本地完成，且其组件和数据流已在信任边界中声明；或
- 用户启用 MODEL_ASSISTED_WITH_CONSENT。

## 11. 端到端用户流程

### 11.1 主流程

1. **收集输入**：读取稿件内容、领域、JCR、OA 和节奏偏好。
2. **隐私预检**：确认完整稿件只在本地解析；必要时执行脱敏。
3. **稿件画像**：提取主题、MeSH、submission_format、study_designs、方法、对象和贡献类型。
4. **关键信息确认**：只有在投稿格式、领域、JCR 类别或其他硬约束存在低置信度冲突时才向用户确认。
5. **生成相似论文候选**：执行语义检索、关键词/MeSH 检索和相似论文扩展。
6. **生成期刊候选池**：聚合相似论文真实发表期刊、官方 Scope 匹配期刊和用户种子期刊。
7. **期刊归一化**：通过 ISSN-L、pISSN、eISSN、标题变更和出版商信息去重。
8. **验证候选**：核验官网、投稿指南、投稿格式、WoS 索引、OA、APC 硬预算、期刊状态、JCR 数据和风险状态。
9. **执行硬门槛**：标记 PASS、FAIL、UNVERIFIED 或 NOT_APPLICABLE。
10. **计算匹配分**：仅对未 FAIL 的候选计算内容匹配；正式榜单只接收所有硬门槛均 PASS 的期刊。
11. **计算证据置信度**：结合输入、来源、证据数量、一致性、稳定性和新鲜度。
12. **生成策略梯度**：在满足资格的候选中输出冲刺、优先、相对稳妥三档。
13. **可选稿件预检**：仅在有足够正文时输出独立 Submission Readiness Audit。
14. **生成报告**：输出总表、详细期刊卡片、待核验候选、排除原因和数据声明。

### 11.2 无 JCR 授权时的两阶段流程

公开数据模式下不得声称目标分区已经通过：

1. 第一阶段按内容、WoS、OA、投稿格式和状态生成候选。
2. 将 JCR 分区标为 UNVERIFIED。
3. 候选进入“待核验候选”，不进入正式三梯度榜单。
4. 用户可提供其有权使用的 JCR 导出数据或逐项核验结果。
5. 系统重新执行 JCR 硬门槛后生成正式梯度。

若用户拒绝补充 JCR 数据，报告仍可提供内容匹配参考，但标题必须明确为“未完成 JCR 硬约束核验的候选”，不能称为最终推荐。

## 12. 稿件画像

系统应输出可供用户检查的 Manuscript Profile。

### 12.1 通用画像字段

- title。
- primary_domain。
- specialties。
- submission_format。
- study_designs。
- reporting_guidelines。
- research_question。
- contribution_type。
- entities_and_topics。
- MeSH terms 与同义词。
- study_design。
- methods_and_technologies。
- population_or_research_object。
- setting。
- primary_outcomes。
- keywords_original。
- keywords_expanded。
- unsupported_or_missing_information。
- profile_confidence。

### 12.2 临床研究画像

适用时提取：

- Population。
- Intervention 或 Index test。
- Comparator 或 Reference standard。
- Outcome。
- Study setting。
- Prospective/retrospective。
- Single-center/multicenter。

### 12.3 基础生命科学画像

基础研究不强制套用 PICO，改用：

- Organism。
- Tissue/cell type。
- Perturbation/exposure。
- Assay/technology。
- Molecular or phenotypic endpoint。
- Mechanistic contribution。

## 13. 候选与相似论文检索

### 13.1 候选来源

候选池由以下集合的并集构成：

1. 近三年相似论文真实发表的期刊。
2. 官方 Aims & Scope 与稿件画像匹配的期刊。
3. 用户指定的偏好期刊。
4. 根据 MeSH、专科和方法扩展得到的同领域期刊。

用户排除的期刊或出版社应在生成正式候选前移除，并在报告中记录排除原因。

### 13.2 检索策略

MVP 采用混合检索：

- 语义检索：用结构化研究描述召回表达不同但含义相近的论文。
- 词法检索：保留疾病名、方法名、设备名、分子名和研究设计等精确命中。
- MeSH 扩展：加入同义词和受控词，但不能用过宽的上位词淹没原始主题。
- Similar Articles 扩展：先寻找高相关 PMID 种子，再使用 PubMed 预计算相似文章扩展。
- 时间过滤：默认使用查询日前近 3 年论文。
- 证据类型过滤：优先匹配与目标稿件 submission_format、study_designs 相同或直接兼容的研究。

### 13.3 相似论文级初始评分

以下为 MVP 初始启发式权重，必须版本化并在测试中校准，不应描述为经过临床或统计验证：

| 维度 | 权重 |
|---|---:|
| 文档语义相似 | 45% |
| 词法与 MeSH 重合 | 25% |
| 方法和研究设计相似 | 20% |
| 文章/贡献类型相似 | 10% |

每条相似论文证据至少记录：

- title。
- publication_year。
- journal_title。
- article_type。
- DOI。
- PMID/PMCID/OpenAlex ID；如存在。
- topic_match。
- method_match。
- object_or_population_match。
- contribution_match。
- similarity_score。
- source_records。
- retrieved_at。
- integrity_status。

### 13.4 DOI 和论文完整性要求

正式展示的相似论文必须：

1. DOI 能通过 Crossref 或 doi.org 解析；确实无 DOI 的记录不进入默认展示。
2. 标题、期刊和年份由至少一个主元数据源返回。
3. 不带有已知 Retracted Publication、Retraction Watch 撤稿或当前 Expression of Concern 标记。
4. 不使用 preprint、editorial 或 commentary 充当原始研究证据。
5. 不复制大段受版权保护的摘要。

存在 Correction 但未撤稿的论文可以保留，但必须显示 correction 状态并链接相关更新；更正已实质改变与本次匹配有关的结论时，不作为正式证据。

### 13.5 每刊相似论文数量

- 默认时间窗口：[运行日期减 3 个日历年，运行日期]，首尾均包含。
- 日期优先级：published-online > issued/正式出版日期 > Crossref published；实际采用字段必须记录。
- 报告展示：每刊最多 5 篇。
- 推荐目标：3–5 篇。
- 正式候选最低要求：至少 1 篇有效 DOI；0 篇时不得进入正式榜单。
- 不足 3 篇时允许展示 1–2 篇，但证据置信度最高为 MEDIUM。
- 不使用低相关、年代过久或已撤稿论文凑数。
- 后台评分可使用多于 5 篇候选；前台只展示最相关且具有代表性的 3–5 篇。

不同稿件场景的证据类型必须兼容：

- 系统综述/Meta-analysis 优先使用同类 review/meta-analysis，也可用高度相关原始研究辅助主题判断。
- 临床试验、诊断准确性研究和方法学论文必须至少有一条证据在 study_designs 或 contribution_type 上兼容。
- 病例报告/病例系列不得仅以普通原始研究证明该刊接收该投稿格式；接收能力仍以官方指南为准。

### 13.6 期刊体量归一化

不得直接按相似论文命中数量排名，否则高发文量综合刊会系统性占优。

MVP 可采用如下初始聚合：

- 60%：该刊 top 3 相似论文的平均相似度。
- 20%：该刊最高单篇相似度。
- 20%：经发文总量归一化并做收缩处理的相似论文密度。

top 3 平均按 min(3, 有效论文数) 篇现有证据计算，不补零；只有 1–2 篇时由 evidence_sufficiency 组件降低置信度。0 篇时本维度为 0 且不得正式入榜。

同一期特刊或同一研究团队的高度重复证据应限制贡献。可使用时间衰减，但衰减参数必须配置化并通过离线测试校准。

## 14. 期刊归一化与元数据

### 14.1 期刊主键

优先使用 ISSN-L 作为期刊家族主键，并保存：

- journal_title。
- alternative_titles。
- ISSN-L。
- pISSN。
- eISSN。
- publisher。
- previous_titles。
- successor_or_predecessor。

不得仅以期刊名称字符串去重。

### 14.2 核心元数据

每本候选至少需要：

- 期刊名称。
- 出版商。
- pISSN/eISSN。
- 官方主页。
- 官方 Aims & Scope。
- 投稿指南。
- 当前投稿入口。
- submission_format 支持状态及官方原始术语。
- OA 类型。
- APC；若可核验。
- JIF 与数据年份；若合法可用。
- JCR 发布年份、类别、排名和分区；若合法可用。
- 出版节奏字段。
- 期刊活跃状态。
- 数据来源与查询日期。

### 14.3 指标建模

禁止仅保存一个无年份的“IF”或“Q 区”。应至少建模：

- jif_value。
- jif_data_year。
- jcr_release_year。
- jcr_categories[]。
- 每个 category 下的 rank、total_journals 和 quartile。
- jcr_source_mode：LICENSED_API、USER_SUPPLIED、UNVERIFIED。

同一期刊可能属于多个 JCR 类别并拥有不同分区。报告必须展示所有可用类别，并明确本次硬门槛采用的相关类别。

JCR 版本与类别规则：

1. jcr_release_year=AUTO 时使用运行时最新合法可用的 JCR release，并记录对应数据年。
2. 若只能获得更早版本，默认标为 STALE/UNVERIFIED；只有用户明确要求历史分析时才按指定旧版本判断。
3. 用户指定一个相关类别时，只按该类别判断。
4. 用户确认多个相关类别时，按 jcr_category_match_policy 判断：ANY 表示任一已确认相关类别满足即可，ALL 表示全部满足。
5. 默认策略为 ANY，但它只能作用于已确认的 manuscript-relevant categories，不能在所有类别中挑选最有利结果。
6. 用户未指定类别时，系统根据稿件专科生成建议类别；正式筛选前必须由用户确认。未确认时 JCR 门槛为 UNVERIFIED。

## 15. 数据模式与来源

### 15.1 数据模式

#### 模式 A：授权 JCR 模式

适用条件：

- 有合法的 Clarivate Web of Science Journals API 访问权；或
- 用户提供其有权使用的 JCR 导出文件。

能力：

- 读取带年份的 JIF、类别、排名和分区。
- 执行目标 JCR 分区硬过滤。

要求：

- 不超出许可证允许范围存储、展示或再分发数据。
- 用户提供的数据标为 USER_SUPPLIED。
- 默认只接受运行时最新 JCR release；旧版本按 14.3 的陈旧规则处理。

#### 模式 B：公开数据模式

适用条件：无 Clarivate 授权数据。

能力：

- 生成内容匹配候选。
- 核验公开可验证的 OA、ISSN、文章、期刊状态和官方链接。
- 可记录公开可核验的 WoS index 状态或期刊方 JIF 声明。

限制：

- JIF 数值和 JCR 分区必须标为 UNVERIFIED。
- 出版社或期刊网页中的 JIF 声明只能标为 PUBLIC_CLAIM，不得升级为当前 JIF/JCR VERIFIED。
- 不能执行已验证的 JCR 硬过滤。
- 相关候选只能进入“待核验候选”。

#### 用户 JCR 数据导入契约

支持 CSV 或 XLSX。一个期刊属于多个类别时，每个类别占一行。

用于通过 JCR 分区门槛的必需字段：

- journal_name。
- 至少一个 p_issn、e_issn 或 issn_l。
- jcr_release_year。
- jif_data_year。
- jcr_category。
- quartile。
- wos_indexes。

建议字段：

- jif_value。
- rank。
- total_journals。
- source_export_name。

导入规则：

1. 以 ISSN-L 或 pISSN/eISSN 与候选匹配，期刊名只作为辅助。
2. 标题匹配但 ISSN 冲突时不得自动合并，状态为 CONFLICT。
3. quartile 仅接受 Q1、Q2、Q3、Q4。
4. 同一期刊同一类别出现冲突值时，JCR 门槛为 UNVERIFIED。
5. 用户口头提供“某刊是 Q1”只能记录为 USER_ASSERTED，不能直接成为 PASS；必须同时提供年份、类别和可核验的导出行或来源证据。
6. 导入完成后应保存候选匹配摘要，并从先前运行的 unverified_candidates 恢复硬门槛、评分和分档流程，无需重新上传稿件。

### 15.2 MVP 推荐数据源

| 数据源 | 主要用途 | MVP 地位 | 关键限制 |
|---|---|---|---|
| Clarivate Journals API / 用户 JCR 导出 | JIF、JCR 类别、排名、分区 | 条件适配器 | API 需要付费许可 |
| Clarivate Master Journal List | 当前 WoS 索引和覆盖状态人工/公开核验 | 核心 | 不提供可替代付费 Journals API 的公开 JIF/JCR 分区接口 |
| DOAJ | 完全 OA、ISSN、出版商、APC、投稿指南、Scope、投稿到出版平均周数 | 核心 | 只覆盖 DOAJ 收录 OA 期刊；部分信息为期刊申报 |
| OpenAlex | 语义检索、论文与来源期刊、ISSN-L、主题和引用关系 | 核心 | 需要交叉验证；不能作为期刊质量背书 |
| PubMed / NCBI E-utilities | 生物医学文章、MeSH、Publication Type、Similar Articles、撤稿标记 | 核心 | PubMed 收录不等于 MEDLINE 收录 |
| Europe PMC | 生物医学元数据、实体/方法注释、文章类型交叉验证 | 核心/备用 | 全文使用受单篇许可限制 |
| Crossref | DOI 解析、标题、ISSN、出版商、日期和更新关系 | 核心 | 出版商提交字段可能缺失或冲突 |
| Crossref Retraction Watch | DOI 级撤稿和相关更新核查 | 核心 | 不得用原始撤稿数直接评价期刊 |
| NLM Catalog | 医学期刊状态、频率、MEDLINE/PubMed/PMC 覆盖 | 核心 | 仅适用于医学与生命科学 |
| 期刊/出版社官网 | Scope、投稿指南、投稿格式、APC、速度和投稿入口的最终核验 | 核心 | 只核验最终少量候选，遵守网站条款 |
| Unpaywall | DOI 级 OA 状态补充验证 | 可选 | 文章 OA 不等于期刊完全 OA |
| ISSN Portal / ROAD | ISSN 权威或 OA serial 辅助核验 | 可选 | 完整 API 和批量能力可能需要付费 |

### 15.3 来源优先级

不同字段使用不同来源优先级：

- **JIF/JCR**：合法 Clarivate API或用户授权数据 > UNVERIFIED；其他指标不得替代。
- **WoS 索引**：Clarivate Master Journal List/授权数据 > 出版社声明；出版社声明单独为 PUBLIC_CLAIM。
- **投稿格式是否接收**：当前期刊投稿指南 > 出版社期刊页 > 其他来源。
- **完全 OA**：当前 DOAJ 记录 + 期刊 OA 声明；OpenAlex 或 Unpaywall 仅作交叉信号。
- **APC**：当前期刊官方费用页 > DOAJ。
- **期刊状态**：官方期刊页 + NLM Catalog/DOAJ > OpenAlex 最近发文提示。
- **DOI**：Crossref/doi.org > PubMed/Europe PMC/OpenAlex 交叉记录。
- **出版节奏**：官方定义清晰的统计 > 可复算文章日期 > DOAJ 综合出版时间。
- **ISSN**：权威 ISSN 记录；公开模式下以 NLM、DOAJ、Crossref、OpenAlex 交叉验证。

### 15.4 来源证据对象

任何关键事实都应保存为 SourceFact：

~~~yaml
field: jcr_quartile
value: Q1
status: VERIFIED
source_type: LICENSED_API
source_url: https://example.invalid/source
source_record_id: optional
retrieved_at: 2026-09-15T12:00:00+08:00
data_year: 2025
confidence: HIGH
conflict_notes: null
~~~

其中 VERIFIED 只表示来源和字段已核验，不表示期刊质量或稿件必然适合该刊。

## 16. 完全 OA 判定

### 16.1 用户未要求 OA

可推荐完全 OA、混合 OA 或订阅期刊，但必须如实展示类型。

### 16.2 用户要求 OA

只允许可验证的完全 OA 期刊通过硬门槛：

- DOAJ 记录 admin.in_doaj=true。
- discontinued_date 为空，或没有证据表明该记录已经终止。
- DOAJ 中的 pISSN/eISSN 与候选规范化期刊身份一致。
- DOAJ 记录与期刊当前 OA 声明一致。
- 期刊官网和许可页面可访问并无明显冲突。
- 保存 DOAJ last_updated/last_manual_update 和本次查询时间。

结果状态：

- PASS：满足上述验证。
- FAIL：官方信息明确为 hybrid 或 subscription。
- UNVERIFIED：无法通过 DOAJ/官网验证或来源冲突。

不在 DOAJ 只能得出“当前无法按 MVP 规则验证为完全 OA”，不能直接宣称该刊不是 OA 或属于掠夺性期刊。

### 16.3 APC

APC 应展示：

- 金额与货币。
- 税费是否包含；如可知。
- 豁免或减免链接；如存在。
- 来源和查询日期。

APC 未核验时不得显示估算值。用户设置硬预算时，APC 未知应进入 UNVERIFIED，而不是默认符合。

## 17. 资格门槛

### 17.1 状态枚举

- PASS：有足够证据确认符合。
- FAIL：有足够证据确认不符合。
- UNVERIFIED：证据缺失、过期或冲突。
- NOT_APPLICABLE：用户未启用该约束。

### 17.2 硬门槛

| 门槛 | PASS 条件 | FAIL 条件 | UNVERIFIED 条件 |
|---|---|---|---|
| WoS 索引 | 权威记录确认当前属于 required_wos_indexes；默认 SCIE | 权威记录确认不属于要求的索引 | 当前索引无法核验或来源冲突 |
| JCR 分区 | 合法数据中相关类别满足目标 | 合法数据中相关类别不满足 | 无授权数据、年份不明或类别映射不确定 |
| 完全 OA | 用户要求 OA 且 DOAJ/官网验证通过 | 明确为 hybrid/subscription | 无法验证或来源冲突 |
| 投稿格式 | 当前官方指南明确接收 submission_format 或已验证等价别名 | 当前官方指南明确不接收 | 指南缺失、表述不清或别名映射不确定 |
| APC 硬预算 | HARD 模式下，当前可核验最高必付费用不超过预算 | 当前可核验最低必付费用已超过预算 | 金额/币种/税费未知，或区间跨越预算 |
| 正常收稿 | 官网与投稿入口有效且状态正常 | 已停刊、停止收稿或入口确认关闭 | 当前状态无法核验 |
| 官网/投稿入口 | 官方链接可核验 | 确认是错误、冒名或失效入口 | 身份或入口存在冲突 |
| 关键风险 | 无触发默认排除项 | 触发已确认排除项 | 风险事实无法消解 |

### 17.3 正式榜单规则

- 所有启用的硬门槛均 PASS，才能进入正式三梯度榜单。
- 任一硬门槛 FAIL，候选被排除并记录主要原因。
- 无 FAIL 但存在 UNVERIFIED，进入“待核验候选”。
- 不允许将 UNVERIFIED 自动转换为 PASS。
- APC 的币种换算必须记录汇率来源和换算日期；税费未知时不得假设包含。
- 候选不足时减少输出数量，不放宽用户硬约束。

## 18. 默认风险排除

以下已确认情况默认排除：

- 已停刊、停止收稿或当前状态无法确认。
- 不接收对应 submission_format。
- 官方官网或投稿入口无法验证。
- 存在已确认冒名期刊或劫持期刊风险。
- 已知撤销索引但仍冒用旧指标。
- 关键元数据互相冲突且无法消解。

实现时应把“无法确认”建模为 UNVERIFIED 并移出正式榜单，而不是在内部写成对期刊的不当事实断言。

风险字段应拆开呈现：

- journal_active_status。
- oa_directory_status。
- medline_status。
- pubmed_coverage。
- pmc_coverage。
- wos_status。
- jcr_suppression_status。
- official_site_identity_status。
- article_integrity_status。

不得把“PubMed 有文章”“PMC 收全文”“当前 MEDLINE indexed”视为同一件事。不得仅凭出版社规模、国家或单一数据库缺失判为不可信。

## 19. 期刊匹配分

### 19.1 总体规则

匹配分回答“该稿件与该期刊是否匹配”，不回答：

- 稿件是否一定能通过审稿。
- 期刊是否会录用。
- 当前英语或图表是否合格。

总分为 0–100，初始权重如下：

| 维度 | 分值 |
|---|---:|
| 研究主题与期刊 Scope | 30 |
| 方法与研究设计 | 20 |
| 人群、疾病、场景或研究对象 | 10 |
| 近期相似论文证据 | 25 |
| 目标读者与期刊定位 | 10 |
| 出版节奏等软偏好 | 5 |
| **总计** | **100** |

### 19.2 分项定义

#### A. 研究主题与期刊 Scope：30 分

考查：

- 稿件核心主题与期刊官方 Aims & Scope 的语义一致性。
- MeSH、疾病、器官、生物过程或专科主题是否重合。
- 主题属于期刊长期范围，还是仅出现在一次特刊。

评分必须引用官方 Scope，并列出具体命中与不匹配点。

#### B. 方法与研究设计：20 分

考查：

- 期刊是否近期发表相同研究设计。
- 方法、技术、统计或成像模态是否具有可比性。
- 期刊是否适合该贡献类型。

“期刊接收 submission_format”属于硬门槛；本项评价通过门槛后 study_designs 和具体方法的契合程度。

#### C. 人群、疾病、场景或研究对象：10 分

临床研究考查人群、疾病谱、临床场景和结局；基础研究考查生物体、组织/细胞、干预、检测技术和终点。

#### D. 近期相似论文证据：25 分

考查：

- 近三年相似论文的最高与平均相似度。
- 证据数量与多样性。
- 时间新鲜度。
- 经期刊发文量归一化后的相似研究密度。

不得只使用命中篇数。

#### E. 目标读者与期刊定位：10 分

考查：

- 研究结论对期刊主要读者是否有直接价值。
- 期刊偏临床实践、基础机制、诊断技术、方法开发或综合传播的定位。
- 研究贡献层级是否与期刊常见内容一致。

#### F. 出版节奏等软偏好：5 分

仅在有可比较来源时评价：

- 出版速度偏好。
- 出版商偏好。
- APC 软预算。
- 其他用户明确的非硬性条件。

未知数据不得被写成“快”或“慢”。

### 19.3 MVP 可执行评分 Rubric

六个维度必须由版本化特征计算，语言模型可以抽取标签和生成解释，但不得自由决定最终数值。所有连续相似度都要保存原始值、归一化方法、模型名称和版本。

| 维度 | 可执行子项 | 分值 |
|---|---|---:|
| 研究主题与 Scope | 官方 Scope 契合度 | 15 |
|  | MeSH/受控主题加权重合 | 10 |
|  | 最近 3 个自然年主题持续覆盖度 | 5 |
| 方法与研究设计 | study_designs 多标签契合 | 8 |
|  | 具体方法/技术语义与词法契合 | 7 |
|  | contribution_type 契合 | 5 |
| 人群/疾病/场景/对象 | 核心实体加权重合 | 6 |
|  | 场景或研究对象契合 | 4 |
| 近期相似论文 | top 3 平均论文相似度 | 15 |
|  | 最高单篇相似度 | 5 |
|  | 归一化相似论文密度 | 5 |
| 目标读者与定位 | 官方 audience/Scope 与预期读者契合 | 6 |
|  | 临床/基础/方法/综合传播定位契合 | 4 |
| 软偏好 | 出版节奏 | 3 |
|  | 出版商偏好 | 1 |
|  | APC 软预算 | 1 |

基础特征计算规则：

- **受控词重合**：对用户稿件与期刊证据集合使用带层级权重的 Jaccard；精确 MeSH 匹配权重 1，相邻上/下位词权重 0.5，仅过宽祖先词权重 0.25。
- **多标签设计契合**：study_designs 的加权 Jaccard；核心设计标签缺失时不得用其他方法词完全补偿。
- **语义契合**：使用固定版本科学文本 embedding 或 NLI scorer；对原始分数使用冻结校准表映射到 0–1，不得在每次运行临时改变阈值。
- **主题持续覆盖**：过去 3 个完整自然年中，至少有 1 篇有效相似论文的年份数除以 3。
- **具体方法契合**：精确规范化方法命中与语义相似按配置版本组合。
- **相似论文聚合**：遵循 13.6 的 60%/20%/20% 聚合；三项分别对应本表 15/5/5 分。
- **归一化密度**：相似有效论文数除以该刊同窗口内可识别的研究论文总量，再经预先冻结的收缩函数处理；只按候选池临时 min-max 不得作为唯一归一化。
- **官方 Scope/读者契合**：只使用当前官方页面文本；页面无法获取时为 null，而不是由期刊名猜测。
- **类别型偏好**：明确匹配=1，明确不匹配=0，部分匹配按配置表取 0.5；未知为 null。

缺失与负证据判定：

- 数据源调用失败、页面不可访问或许可不允许读取：null。
- 检索成功且覆盖要求满足，但没有发现对应主题/方法/论文：0。
- 官方 Scope 或指南明确排除：0；如果同时触发硬门槛则候选直接 FAIL。
- 未提供某项用户软偏好：该子项为 NOT_APPLICABLE，不进入已评估权重。
- 相似论文检索成功但 3 年窗口内有效 DOI 为 0：近期相似论文维度为 0，且不满足正式候选最低证据量。

MVP 正式入榜最低要求：

- 所有启用硬门槛均 PASS。
- final_match_score ≥ 65.0。
- score_coverage ≥ 80%。
- evidence_confidence 至少为 MEDIUM。
- 至少 1 篇近 3 年有效相似论文 DOI。

上述阈值属于 scoring_version=0.1.0，后续只能通过版本化评估更新。

### 19.4 出版节奏与软偏好计算

速度数据只有定义一致时才能比较：

- 首轮决定只接受期刊/出版社官方统计，不从已录用论文反推。
- 投稿到接受、接受到在线可使用官方统计；缺失时可基于近 3 年文章历史估算中位数和 IQR。
- 文章历史估算至少需要 20 篇具有所需日期对的论文，且日期字段完整率至少 50%；否则为 null。
- article-history estimate 不包含被拒稿件，报告必须提示选择偏差。

用户提供数值上限时，较短为优：

- value ≤ target 时子分为 1。
- target < value < 2 × target 时，从 1 线性下降到 0。
- value ≥ 2 × target 时子分为 0。

用户只表达“越快越好”时，只在相同定义、统计量和证据方法的候选中使用百分位排名；最快为 1，最慢为 0。不可比的期刊为 null。

出版节奏 3 分固定拆分：

| 节奏字段 | 分值 |
|---|---:|
| submission_to_first_decision | 1.2 |
| submission_to_acceptance | 0.9 |
| acceptance_to_online_publication | 0.6 |
| publication_frequency | 0.3 |

聚合规则：

- 每个启用且可评估的字段独立计算 0–1 子分，再乘以固定分值后相加。
- 未启用或不可评估字段为 null，其分值不重分配给其他速度字段。
- 用户只说“越快越好”时，默认启用前三个时长字段；publication_frequency 只有用户明确提出时才启用。
- 用户为不同字段给出 priority 时，仅用于报告排序，不改变上述固定分值；若需自定义权重，必须产生新的 scoring_version。
- publication_frequency 使用 issues_per_year 最低目标时：达到目标得 1；位于 0.5×target 与 target 之间线性从 0 升至 1；低于或等于 0.5×target 得 0。Continuous publication 作为独立布尔偏好评分，不能虚构 issues_per_year。

软偏好其余固定分配为出版社 1 分、APC 软预算 1 分。某项未启用或不可评估时为 null，不允许其他软偏好占用其权重。APC 软预算使用与速度数值上限相同的线性规则，并记录币种换算日期。

assessed_weight 必须按这些最小子项累计，而不是把整个 5 分维度一次性标为已评估。

### 19.5 缺失数据与评分覆盖度

每个分项可以是 0–1 的子分，也可以是 null：

- 0：有证据显示明确不匹配。
- null：没有足够证据评估。

计算：

- assessed_weight = 所有非 null 分项权重之和。
- raw_weighted_points = 所有已评估分项的权重乘子分之和。
- final_match_score = raw_weighted_points / assessed_weight × 100。
- score_coverage = assessed_weight / 100。

规则：

- final_match_score 必须与 score_coverage 同时展示。
- score_coverage 低于 80% 时，不得进入正式排序，进入待核验候选。
- 不能用高分掩盖低覆盖度。
- 权重、阈值和模型版本必须写入运行记录。

### 19.6 解释要求

每个分项需输出：

- score。
- weight。
- supporting_evidence。
- negative_evidence。
- source_urls。
- missing_information。

“投稿优势”必须来自可观察证据，例如：

- 期刊近三年持续发表同类诊断设计。
- 该刊读者与稿件临床场景高度一致。
- 官方投稿指南明确接收病例系列。

不得生成如下无来源断言：

- 编辑会喜欢这篇文章。
- 录用机会很高。
- 很容易中。

## 20. 证据置信度

证据置信度与匹配分独立，取 HIGH、MEDIUM、LOW。

### 20.1 置信度维度

- **Input sufficiency**：完整稿件优于标准摘要输入，标准摘要优于仅标题/关键词。
- **Evidence sufficiency**：相似 DOI 数量、来源多样性、不同团队和期次。
- **Provenance completeness**：Scope、DOI、ISSN、OA、JCR 和速度是否有来源。
- **Multi-signal agreement**：语义、词法、MeSH、官方 Scope 是否一致。
- **Stability**：移除一条证据或轻微改写查询后排名是否稳定。
- **Freshness**：期刊信息和指标的查询日期。

### 20.2 初始分级规则

置信度使用 0–1 的确定性组件和固定权重：

| 组件 | 权重 | 计算 |
|---|---:|---|
| input_sufficiency | 15% | 完整稿件或标题+摘要+关键词=1.0；摘要+关键词=0.8；仅摘要=0.6；仅标题或关键词=0.2 |
| evidence_sufficiency | 25% | 3 篇及以上有效 DOI 且至少来自 2 个团队/期次=1.0；2 篇=0.67；1 篇=0.33；0 篇=0 |
| provenance_completeness | 25% | 已 VERIFIED 的必需 SourceFact 数 / 本次适用的必需 SourceFact 总数 |
| signal_agreement | 15% | 支持该候选达到冻结相关阈值的语义、词法、MeSH、官方 Scope 信号数 / 可用信号数；可用信号少于 2 个时固定为 0.25 |
| stability | 10% | 删除一条证据与同义改写两次 top-5 Jaccard 的平均值；无法执行时为 0 |
| freshness | 10% | 未过期的必需 SourceFact 数 / 本次适用的必需 SourceFact 总数 |

confidence_score 为上述加权和，保留 2 位小数。

决策顺序：

1. 任一启用硬门槛为 UNVERIFIED 或 FAIL，最终置信度强制为 LOW。
2. 否则，confidence_score ≥ 0.80 且没有任何组件低于 0.50，为 HIGH。
3. 否则，confidence_score ≥ 0.60，为 MEDIUM。
4. 其余为 LOW。

来源冲突按以下方式进入组件：

- 未消解的必需事实冲突使相应事实不计入 VERIFIED，降低 provenance_completeness。
- 超过配置新鲜度的事实不计入 freshness。
- 检索信号方向冲突降低 signal_agreement。
- 排名扰动低于 27.4 的稳定性建议值时按实际 Jaccard 计分。

置信度版本必须随 scoring_version 保存。输入相同、SourceFact 冻结且版本相同时，置信度等级必须唯一。

## 21. 投稿策略梯度

### 21.1 默认数量

- 冲刺：最多 3 本。
- 优先：默认 3 本，用户可要求 4 本。
- 相对稳妥：默认 1 本，用户可要求 2 本。

不足时如实输出实际数量，并说明短缺原因。

### 21.2 定义

#### 冲刺

- 已通过所有硬门槛。
- 内容匹配度高。
- 期刊在用户目标范围内定位相对更具挑战，或位于目标分区/类别的较高位置。
- 有真实相似论文证据支持。

#### 优先

- 已通过所有硬门槛。
- 内容、方法、读者和证据质量最平衡。
- 是建议用户优先人工核验和讨论的主要候选。

#### 相对稳妥

- 已通过所有硬门槛和最低内容匹配要求。
- Scope 相对更宽，近期同类论文证据较充分，定位相对温和。
- 仍不表示保证录用。

### 21.3 分档规则

先使用 19.3 的正式入榜条件生成 eligible pool。分档只使用合法 JCR 数据中的 manuscript-relevant category。

期刊位置分计算：

- total_journals > 1 时，journal_position_score = 1 - (rank - 1) / (total_journals - 1)。
- total_journals = 1 时 journal_position_score=1；rank 或 total_journals 缺失时为 null。
- 分数越接近 1，表示在该类别排名越靠前。
- 多个已确认相关类别按用户的 ANY/ALL 政策保留各自结果。
- 用于分档的 journal_position_score 固定取本次政策下所有通过类别 position score 的最小值，即最保守位置；ALL 模式取所有已确认且通过类别的最小值。
- ANY 模式中未通过目标分区的相关类别不参与 position score，但必须在报告中展示；不得静默取所有类别中的最有利位置。

在 eligible pool 内按 journal_position_score 排成三等分：

- 上三分之一为 HIGH_POSITION。
- 中三分之一为 MID_POSITION。
- 下三分之一为 LOWER_POSITION。
- 边界并列的期刊保持同一 position band。

初始分档条件：

- **冲刺**：HIGH_POSITION，final_match_score ≥ 75，evidence_confidence ≥ MEDIUM。
- **相对稳妥**：LOWER_POSITION，final_match_score ≥ 65，近期相似论文子分 ≥ 0.60，且 scope_breadth_score ≥ 0.60。
- **优先**：满足正式入榜条件，但未进入上述两档；或缺少可比较位置数据但整体匹配与证据满足正式入榜条件。

scope_breadth_score 必须由固定版本分类器对官方 Scope 和近三年受控主题覆盖计算，取 0–1；不能由模型凭印象给分。该特征缺失时不得进入“相对稳妥”，但可以进入“优先”。

候选可能同时满足多个条件时，优先级为冲刺 > 相对稳妥 > 优先，确保每本期刊只出现一次。各档内部排序键依次为：

1. final_match_score 降序。
2. evidence_confidence：HIGH 优先于 MEDIUM。
3. score_coverage 降序。
4. 近期相似论文子分降序。
5. 有效 DOI 数降序。
6. 规范化期刊名升序，用于稳定解决最终并列。

其他规则：

- 所有三档都必须满足用户的 WoS、JCR、OA、投稿格式及其他启用的硬约束。
- 不得为了生成“相对稳妥”期刊而自动放宽目标 JCR 分区。
- 某档没有满足条件的候选时保留为空并解释原因。
- 无合法、可比较的 JCR rank/total_journals 时，只输出“优先候选”，不得伪造冲刺或相对稳妥。
- 每档必须解释“为何进入此档”并展示使用的 position band。

报告中的固定提示：

> 投稿策略梯度仅表示相对匹配与期刊定位，不代表录用概率，也不构成录用保证。

## 22. Submission Readiness Audit

### 22.1 定位

稿件就绪度是独立可选模块，不进入 Journal Match Score，也不改变期刊的方向匹配结论。

### 22.2 触发条件

- readiness_audit_mode=OFF：不执行。
- readiness_audit_mode=AUTO：按 10.3 执行本地确定性预检；仅摘要时只评估摘要层面信息。
- readiness_audit_mode=ON：执行所有当前 privacy_mode 允许的检查，并明确列出仍需补充或授权的材料。
- 仅有摘要时，全文、图表和统计细节显示 NOT_ASSESSED。
- 不得把未提供内容记为 0 分。

### 22.3 检查维度

- 科学叙事与结构。
- 方法和统计报告完整度。
- 图表可读性、标注与正文自洽性。
- 英文表达和术语一致性。
- 伦理审批、注册和数据可用性信息。
- 对应报告规范，例如 CONSORT、STROBE、PRISMA、STARD、CARE。
- 目标期刊的字数、图表、摘要和 submission_format 要求。

预检分两层：

1. **General readiness**：与特定期刊无关的结构、方法、统计、图表、语言、伦理和报告规范。
2. **Journal-specific compatibility**：只对正式候选执行，逐刊检查字数、摘要结构、图表上限、补充材料和投稿格式。

基础指南映射遵循 8.2；同一稿件可映射多个 reporting_guidelines。无法确定适用规范时显示 UNVERIFIED，不选择最宽松规范。

LOCAL_PARSE_ONLY 下两层都只执行 10.3 的本地可确定检查。需要模型读取正文才能完成的科学叙事、英文表达或语义判断必须为 NOT_ASSESSED；不能因为用户选择 ON 而绕过隐私边界。

### 22.4 输出级别

- BLOCKER。
- MAJOR_REVISION。
- MINOR_REVISION。
- PASS。
- NOT_ASSESSED。

严重度定义：

- **BLOCKER**：缺少投稿或研究报告所必需的关键内容，例如适用时伦理/注册声明缺失、文件不可读、投稿格式不被目标刊接受。
- **MAJOR_REVISION**：方法、统计或报告规范存在影响可评价性的重大缺口，需要实质修改。
- **MINOR_REVISION**：局部表达、格式、图表标注或一致性问题，不改变研究核心。
- **PASS**：在本次可检查范围内未发现 blocker 或 revision 项；不代表科学、统计或伦理已被正式验证。
- **NOT_ASSESSED**：内容未提供或能力范围不支持。

总览等级取所有已评估 finding 中最严重的级别；存在 NOT_ASSESSED 时需同时展示覆盖范围，不能用 PASS 隐藏未评估内容。

输出必须附：

- finding。
- evidence_location。
- why_it_matters。
- suggested_action。
- limitation。

evidence_location 应使用 page/section/paragraph/table/figure 等可定位字段；解析后无法获得页码时至少提供章节和段落索引。

本模块不得声称已经验证科学真实性、统计有效性或伦理合规性。其结果不得进入 Journal Match Score 或投稿策略梯度算法。

## 23. 结构化输出

### 23.1 报告顺序

1. 结论摘要。
2. 输入与约束回顾。
3. Manuscript Profile。
4. JCR 数据模式、privacy_mode、查询日期和关键限制。
5. 三梯度候选总表。
6. 期刊详细卡片。
7. 待核验候选。
8. 已排除候选及主要原因。
9. Submission Readiness Audit；如适用。
10. 数据来源、免责声明和建议的人工复核步骤。

### 23.2 候选总表字段

| 字段 | 要求 |
|---|---|
| 投稿梯度 | 冲刺、优先、相对稳妥 |
| 期刊名称 | 英文官方名称 |
| JCR 类别/分区 | 包含数据年、发布年和验证状态 |
| JIF | 包含数据年和验证状态 |
| 出版商 | 标注来源 |
| ISSN | pISSN/eISSN；如适用 |
| OA 类型 | 完全 OA、Hybrid、Subscription、Unverified |
| APC | 金额、货币、来源和日期 |
| 最终匹配分 | 0–100 |
| 评分覆盖度 | 百分比 |
| 证据置信度 | High/Medium/Low |
| 出版节奏摘要 | 分字段，未知则明确显示 |
| 官网 | 当前官方链接 |
| 投稿指南 | 当前官方链接 |

### 23.3 期刊详细卡片

每本正式候选的卡片包含：

#### 基本信息

- Journal name。
- Publisher。
- ISSN-L、pISSN、eISSN。
- Official homepage。
- Aims & Scope。
- Author guidelines。
- Submission portal。

#### 指标与约束

- JIF 和年份。
- JCR categories、rank、quartile 和年份。
- OA 类型、APC 和许可。
- 四项出版节奏。
- 每个硬门槛的 PASS/FAIL/UNVERIFIED/NOT_APPLICABLE。

#### 最终匹配

- final_match_score。
- score_coverage。
- evidence_confidence。
- strategy_tier。
- tier_rationale。

#### 匹配分构成

- 研究主题与 Scope。
- 方法与研究设计。
- 人群/疾病/场景/研究对象。
- 近期相似论文。
- 目标读者与期刊定位。
- 软偏好。

#### 方向契合

用 2–4 条可验证内容说明：

- 稿件主题与官方 Scope 的具体对应。
- 研究方法与期刊近期论文的对应。
- 期刊读者为什么可能关心该研究。

#### 投稿优势

只陈述证据支持的优势，并同时列出：

- potential_strengths。
- potential_mismatches。
- missing_or_unverified_facts。
- recommended_manual_checks。

#### 近期相似研究

默认 3–5 篇，每篇列出：

- Title。
- Year。
- Article type。
- DOI 链接。
- Topic match。
- Method match。
- Object/population match。
- 为什么可作为选刊证据。

### 23.4 待核验候选

单独列出：

- 期刊名称。
- 内容匹配分和覆盖度。
- 未通过正式榜单的具体 UNVERIFIED 门槛。
- 用户需要提供或人工核验的信息。
- 不得为其分配正式投稿梯度。

### 23.5 机器可读结果

除 Markdown 报告外，实现应保留结构化结果，推荐 JSON 或 YAML：

~~~yaml
schema_version: 1.0.0
run:
  run_id: jm_example
  generated_at: 2026-09-15T12:00:00+08:00
  jcr_data_mode: PUBLIC
  privacy_mode: LOCAL_PARSE_ONLY
  consent_record: null
  scoring_version: 0.1.0
  evidence_window:
    start: 2023-09-15
    end: 2026-09-15
manuscript_profile: {}
constraints: {}
recommendations:
  sprint: []
  priority: []
  relatively_safe: []
unverified_candidates: []
excluded_candidates: []
submission_readiness: null
sources: []
disclaimers: []
~~~

### 23.6 机器输出契约

MVP schema_version 固定为 1.0.0。顶层所有字段均必需；没有结果时使用空数组或 null，不得省略，也不得使用“-”代替 null。

| 对象 | 必需字段 |
|---|---|
| run | run_id、generated_at、jcr_data_mode、privacy_mode、consent_record、scoring_version、evidence_window、source_health、errors |
| manuscript_profile | input_sufficiency、primary_domain、specialties、submission_format、study_designs、reporting_guidelines、methods、population_or_object、profile_confidence |
| constraints | required_wos_indexes、target_jcr_quartiles、target_jcr_categories、jcr_category_match_policy、oa_requirement、apc_budget_mode、publication_speed、publisher_preferences、tier_counts、privacy_mode |
| journal | journal_id、journal_title_original、publisher_original、issn_l、pissn、eissn、official_urls、source_fact_ids |
| gate | gate_key、status、reason_zh、evidence_ref_ids |
| score | final_match_score、score_coverage、scoring_version、dimensions |
| score_dimension | dimension_key、weight、raw_score、weighted_points、status、evidence_ref_ids、explanation_zh |
| confidence | level、reasons_zh、input_sufficiency、evidence_sufficiency、provenance_completeness、signal_agreement、stability、freshness |
| similar_article | title_original、publication_date、date_type、journal_title_original、article_type_original、doi、source_ids、integrity_status、match_reasons_zh |
| recommendation | journal、gates、score、confidence、strategy_tier、tier_rationale_zh、similar_articles、strengths_zh、mismatches_zh、manual_checks_zh |
| source_fact | source_fact_id、field、value、status、source_type、source_url、retrieved_at、data_year、conflict_notes_zh |
| readiness_finding | check_id、layer、category、severity、status、evidence_location、observed_value、expected_value、source_rule_id、suggested_action_zh、limitation_zh |
| error | error_code、stage、source、retryable、impact_zh、occurred_at |

枚举：

- jcr_data_mode：LICENSED_JCR、USER_JCR_IMPORT、PUBLIC。
- privacy_mode：LOCAL_PARSE_ONLY、MODEL_ASSISTED_WITH_CONSENT、OFFLINE_ONLY。
- consent_record：未授权时为 null；授权时包含 consented_at、recipient、purpose、allowed_content 和 retention_notice。
- gate.status：PASS、FAIL、UNVERIFIED、NOT_APPLICABLE。
- strategy_tier：SPRINT、PRIORITY、RELATIVELY_SAFE、null。
- confidence.level：HIGH、MEDIUM、LOW。
- source_fact.status：VERIFIED、PUBLIC_CLAIM、USER_SUPPLIED、USER_ASSERTED、UNVERIFIED、CONFLICT、STALE。
- score_dimension.status：ASSESSED、UNVERIFIED、NOT_APPLICABLE。
- integrity_status：CLEAR、CORRECTED、EXPRESSION_OF_CONCERN、RETRACTED、UNVERIFIED。

类型和空值规则：

- 分数使用 number，保留 1 位小数；raw_score 为 0–1 或 null。
- 日期使用 ISO 8601；只有年份时另存 date_precision=YEAR。
- DOI 存规范化小写值，不含 https://doi.org/ 前缀；展示层生成可点击 URL。
- ISSN 使用 XXXX-XXXX；未知为 null。
- 空字符串不代表未知。
- recommendations、unverified_candidates 和 excluded_candidates 中的每个元素必须带稳定 journal_id。
- excluded_candidates 至少包含 failed_gate 或 exclusion_reason_zh。
- 所有 explanation、reason、strength、mismatch 和 manual_check 使用中文字段。
- journal title、publisher、JCR category、相似论文 title 和来源字段使用 *_original 保存源记录英文原文，不进行翻译或改写。

正式 recommendation 的 schema 校验必须拒绝：

- 任一启用 gate 不是 PASS。
- strategy_tier 为 null。
- similar_articles 数量小于 1 或大于 5。
- 缺少 DOI 或 DOI integrity_status 不合格。
- final_match_score、score_coverage 或 scoring_version 缺失。

最终 JSON Schema 应作为 MVP 实现产物放入 references/output-schema.json，但其语义必须遵循本节，不得把字段类型继续留作产品决策。

### 23.7 交付位置

- 默认在当前对话中输出 Markdown 决策报告。
- 只有用户要求保存，或后续流程明确需要机器文件时，才在用户授权的工作区写入 journal-match-{run_id}.md 和 journal-match-{run_id}.json。
- 无写入权限时返回聊天内报告和结构化代码块，不改写其他目录。
- 报告文件不得包含完整稿件正文、API 密钥或不必要的个人信息。

## 24. 功能需求

### FR-01 输入解析

系统必须接受标准摘要输入和可选完整稿件，识别输入完整度并报告解析失败项。

### FR-02 稿件分类

系统必须将六类用户场景映射为 submission_format、study_designs 和 reporting_guidelines。submission_format 低置信度时必须请求确认，不能用未经确认的格式执行硬过滤。

### FR-03 本地隐私处理

系统必须执行 LOCAL_PARSE_ONLY、MODEL_ASSISTED_WITH_CONSENT 或 OFFLINE_ONLY 信任边界、出站字段白名单和 payload 测试，阻止未经同意向模型或第三方服务发送全文、长原文片段或身份信息。

### FR-04 结构化稿件画像

系统必须生成可供用户核查的主题、方法、对象、研究设计和贡献类型画像。

### FR-05 混合检索

系统必须结合语义、词法/MeSH 和至少一种生物医学来源检索相似论文。

### FR-06 候选池生成

系统必须聚合真实发表期刊、Scope 候选和用户种子期刊，并尊重排除列表。

### FR-07 期刊归一化

系统必须以 ISSN 系列信息处理别名、更名和重复记录。

### FR-08 资格门槛

系统必须为 WoS 索引、JCR、OA、投稿格式、APC 硬预算、正常收稿、官网身份和风险状态输出 PASS、FAIL、UNVERIFIED 或 NOT_APPLICABLE，并严格执行正式榜单规则。

### FR-09 JCR 降级

没有合法 JCR 数据时，系统必须启用公开数据模式，将相关候选置于待核验列表。

### FR-10 完全 OA

当用户要求 OA 时，正式结果必须是按本 PRD 规则验证的完全 OA 期刊，不得以文章级 OA 或 Hybrid OA 代替。

### FR-11 相似论文证据

每本正式期刊展示近三年 1–5 篇相似论文，按明确日期优先级验证 DOI 与完整性状态；不足时不得凑数。

### FR-12 匹配评分

系统必须使用 19.3 的六维 100 分 Rubric 和正式入榜阈值，展示特征、分项、最终分数、覆盖度和评分版本；模型不得自由决定数值。

### FR-13 证据置信度

系统必须独立输出 High/Medium/Low 置信度及降级原因。

### FR-14 三梯度

系统必须按 21.3 的确定性分档和排序规则生成冲刺、优先、相对稳妥候选；尊重 tier_counts，条件不足时减少数量。

### FR-15 出版节奏

系统必须分开处理四类节奏信息，执行 19.4 的可比性与评分规则，并附定义、统计量、样本量、来源和日期。

### FR-16 稿件就绪度

系统必须支持 OFF/AUTO/ON，分别输出通用预检与逐刊 compatibility；未提供内容显示 NOT_ASSESSED，结果不得进入匹配分或分档。

### FR-17 事实溯源

期刊指标、OA、ISSN、出版商、Scope、投稿指南、APC、速度和 DOI 均必须保留来源与查询时间。

### FR-18 冲突处理

来源冲突不得静默覆盖。系统必须展示冲突字段、各来源和值，并根据来源优先级决定是否降为 UNVERIFIED。

### FR-19 不确定性表达

系统不得把未知、模型推断或低置信度结果写成确定事实。

### FR-20 报告生成

系统必须生成中文 Markdown 报告和符合 schema_version=1.0.0 的结构化结果；英文原始元数据与中文解释字段严格分离。

### FR-21 JCR 数据导入与恢复

系统必须按 15.1 的 CSV/XLSX 契约校验用户 JCR 数据，通过 ISSN 关联候选，并允许从先前待核验运行恢复硬门槛和分档。

### FR-22 Skill 调用策略

Skill 默认允许基于明确的生物医学选刊意图隐式调用，也支持用户显式调用。实现必须提供可区分的 frontmatter description、正负触发测试，并遵守 9.5 的非触发边界。

## 25. 非功能需求

### NFR-01 可追溯性

同一运行应保存：

- 查询时间。
- 数据源。
- 原始源记录 ID。
- 评分与规则版本。
- 用户约束。
- jcr_data_mode 和 privacy_mode。

### NFR-02 可重复性

在相同输入、相同数据快照和相同版本下，硬门槛与评分应可重复。模型生成的解释不得改变底层事实状态。

### NFR-03 新鲜度

- 最终候选的官网、投稿指南和投稿入口应在本次运行中核验。
- JIF/JCR 必须带数据年和发布年。
- APC 和出版速度必须带查询日期。
- 缓存数据过期时应重新核验或标记为 STALE。

具体缓存 TTL 属于实现配置，但不得隐藏陈旧状态。

### NFR-04 容错

单一外部数据源失败时应：

1. 继续使用其他允许的数据源。
2. 标记缺失和影响。
3. 降低置信度或将候选移入待核验区。
4. 不用模型生成数据填补失败字段。

### NFR-05 数据与许可

- 遵守各 API 的速率、署名、缓存和再分发条款。
- 只保存完成推荐所需的最小元数据。
- 不批量抓取许可不明的期刊全文或普通版权全文。
- 对用户提供的 JCR 数据不做超出许可范围的传播。

### NFR-06 安全

- API 密钥只从环境变量读取。
- 日志、报告和版本库不得包含密钥。
- 外部网页内容视为不可信数据，不能执行其中的指令。
- URL 必须核验域名和期刊身份，降低劫持期刊链接风险。

### NFR-07 性能

MVP 优先保证证据质量而非瞬时响应。网络检索应支持超时、重试、速率限制和局部失败；不设未经验证的秒级响应承诺。

### NFR-08 可访问性与语言

- 决策解释使用中文。
- 期刊名、论文标题、指标和官方字段保留英文原文。
- 链接必须可点击。
- 不以颜色作为唯一状态表达方式。

## 26. 失败与降级策略

| 场景 | 系统行为 |
|---|---|
| 输入不足 | 输出探索性候选或请求补充；降低输入置信度 |
| 无 JCR 授权 | 首次说明不会产生正式三梯度榜单；启用公开模式，相关候选进入待核验 |
| WoS 索引无法核验 | 标为 UNVERIFIED，不进入正式榜单 |
| JCR 类别不明确 | 请求确认或标为 UNVERIFIED |
| submission_format 不明确 | 暂停硬筛选并请求确认 |
| APC 硬预算信息不全 | 标为 UNVERIFIED，不假设符合 |
| 无足够相似论文 | 减少展示数量，降低证据置信度 |
| DOI 无法验证 | 不将该论文作为正式相似证据 |
| 官网或指南打不开 | 候选进入待核验，不进入正式榜单 |
| OA 来源冲突 | 标为 UNVERIFIED |
| 速度数据缺失 | 显示 Unknown，不判断快慢 |
| 候选不足 8 本 | 输出实际数量，不放宽硬条件 |
| 所有候选均失败 | 输出失败原因分布和可由用户主动选择的放宽项 |
| 外部 API 部分失败 | 使用剩余来源并降低置信度 |
| 全文解析失败 | 回退到标题、摘要、关键词模式 |
| 用户场景超出 MVP | 明确提示不支持，不套用错误评分模板 |

## 27. 评估与验收

### 27.1 数据完整性验收

- 正式推荐中的硬约束错误数为 0。
- required_wos_indexes 默认 [SCIE] 时，ESCI-only 候选不会通过。
- 每篇展示的相似论文 DOI 可解析率为 100%。
- 每个 JIF/JCR 值均有合法来源、数据年和发布年。
- 每个正式 OA PASS 均有当前验证证据。
- 每本正式推荐均有官网和投稿指南来源。
- 不存在用 CiteScore/SJR 冒充 JIF/JCR 的输出。

### 27.2 行为验收

- 仅摘要输入时，图表和全文写作质量显示 NOT_ASSESSED。
- 任一硬门槛 UNVERIFIED 的期刊不会进入正式三梯度榜单。
- 用户排除的期刊不会再次出现在正式或待核验候选中。
- 条件不足时不会用旧论文或低相关论文凑满 5 篇。
- 候选不足时不会自动放宽 WoS、JCR、OA 或 submission_format 条件。
- 报告始终展示“非录用概率/非录用保证”的提示。
- 同一事实发生来源冲突时，报告能显示冲突而非静默覆盖。
- journal_title_original、publisher_original、JCR category 和论文 title_original 与冻结源记录一致；中文仅出现在解释字段。

### 27.3 可执行验收用例

实现必须在 tests/fixtures/acceptance 下保存冻结 SourceFact 输入与完整 expected JSON。离线测试不得访问网络，并对 gate、score、coverage、confidence、tier 和 schema 执行精确断言。

| 用例 | 冻结输入 | 预期 |
|---|---|---|
| A01 授权 JCR 多类别 ANY | SCIE；两个已确认相关类别仅一个为 Q1 | JCR PASS；报告展示两类；使用实际通过类别分档 |
| A01B 多类别均通过 | 两个相关类别均通过但 position score 不同 | 使用两者最小值分档 |
| A02 授权 JCR 多类别 ALL | 同 A01，政策为 ALL | JCR FAIL |
| A03 公开模式 | 无合法 JCR 数据，内容高度匹配 | JCR UNVERIFIED；正式 recommendations 为空；候选进入待核验 |
| A04 索引差异 | 仅 ESCI，required_wos_indexes=[SCIE] | WoS gate FAIL |
| A05 OA 通过 | in_doaj=true、无 discontinued_date、ISSN 匹配、官网一致 | OA PASS |
| A06 OA 冲突 | DOAJ 与官网身份/许可冲突 | OA UNVERIFIED；不得正式入榜 |
| A07 投稿格式歧义 | 用户说“方法研究”，无法确认 METHODS_ARTICLE/ORIGINAL_ARTICLE | Intake 暂停确认，不执行格式门槛 |
| A08 APC 硬预算未知 | HARD；税费或币种不可核验 | APC gate UNVERIFIED |
| A09 数据源故障 | Scope 请求超时 | Scope 子项 null，不记 0；coverage 降低 |
| A10 明确无近期证据 | 检索成功，窗口内有效 DOI 为 0 | Recent evidence=0；不得正式入榜 |
| A10B 一或两篇证据 | 分别冻结 1 篇和 2 篇有效 DOI | top-3 均值按实际篇数计算；evidence_sufficiency 分别为 0.33/0.67 |
| A11 DOI 上限 | 有 6 篇合格证据 | 只展示按排序最优的 5 篇 |
| A12 边界日期 | 论文日期正好等于窗口起点 | 包含该论文 |
| A13 撤稿与更正 | 一篇撤稿、一篇有非实质更正 | 撤稿排除；更正论文带 CORRECTED |
| A14 仅摘要 readiness | 无正文和图表 | 全文、图表与统计为 NOT_ASSESSED |
| A15 隐私 payload | 完整稿件含姓名、单位、精确未公开结果 | 所有网络 payload、重试和异常日志均不含禁止字段或原文片段 |
| A16 分档与并列 | 固定分数、JCR rank 和 position band | 按 21.3 唯一分档并使用稳定并列顺序 |
| A16B 多速度偏好 | 同时启用三项时长和 publication frequency | 按 1.2/0.9/0.6/0.3 分值独立聚合，null 不重分配 |
| A17 中英字段 | 英文源记录 + 中文解释 | *_original 原样保留；*_zh 字段为中文 |
| A18 负触发 | 纯英文润色请求或工程学选刊 | 不启动完整 Medical Journal Matcher 流程 |

在线冒烟测试只验证数据源连通性、字段映射和降级，不作为可重复离线验收的替代。

### 27.4 排序质量评估

离线评估：

- 使用时间切分，避免未来论文信息泄漏到历史测试。
- 使用 Recall@5、MRR 和 nDCG 观察历史真实发表期刊是否进入候选。
- 历史发表期刊只作为辅助单标签 proxy，不作为唯一真值。
- 分专科、submission_format、study_designs 和低发文量期刊报告结果。

专家评估：

- 每篇测试稿件由至少 2 名相关专科研究者盲评候选。
- 标签为 relevant、plausible、not plausible。
- 评价 top-k 多标签相关性、解释可信度和硬门槛准确性。
- 记录专家分歧。

稳健性评估：

- 删除一篇相似论文后，原 top 5 与新 top 5 的 Jaccard 建议不低于 0.60；低于时必须降低 stability 置信度。
- 使用同义改写查询后，原 top 5 与新 top 5 的 Jaccard 建议不低于 0.60；低于时必须降低 stability 置信度。
- 对高发文量综合刊和小样本期刊单独检查体量偏差。
- 对新方法、新疾病术语和 MeSH 滞后情况测试降级行为。

### 27.5 MVP 退出标准

进入可用 MVP 前至少满足：

1. 所有数据完整性验收项通过。
2. 在预先定义的生物医学测试集上完成人工多标签评估。
3. 在版本化 MVP 试点集上，正式候选 top 5 被专家评为 relevant 或 plausible 的 micro-average 与六类场景 macro-average 均不低于 80%。试点集至少包含六类场景各 3 篇，共 18 篇；每篇由 2 名专家独立评审，意见不一致时由第 3 名专家裁决。
4. 硬门槛错误率为 0；UNVERIFIED 可以存在，但不得被误判为 PASS。
5. 隐私测试确认未授权情况下不会向外发送完整稿件或身份信息。
6. 至少覆盖六类稿件各 3 个测试样例。
7. 在 API 超时、字段缺失、来源冲突和无候选场景下能正确降级。
8. A01–A18 离线验收用例全部通过。
9. JSON Schema 校验、正触发和负触发测试全部通过。

## 28. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| JCR/JIF 为许可数据 | 无授权时无法执行目标分区硬筛选 | 双数据模式；用户导入；公开模式待核验 |
| 历史发表期刊不是唯一正确期刊 | 训练和评估偏窄 | 候选检索 + 多标签专家评价 |
| 大型期刊发文量偏差 | 大刊霸榜 | top-k 聚合、按总发文量归一和收缩 |
| 近期特刊扭曲画像 | 短期主题被误当长期 Scope | 官方 Scope 复核、跨时间证据和团队去重 |
| MeSH 索引滞后 | 新论文或新技术召回不足 | 原始术语 + 语义检索 + 多源交叉 |
| OA 假阴性 | 未入 DOAJ 的真实 OA 刊被置为未知 | 标为 UNVERIFIED，不直接判 FAIL |
| 速度数据口径不一 | 错误比较快慢 | 分字段、保留定义和样本量、不可比时不排名 |
| DOI/ISSN/改名冲突 | 重复或错误期刊身份 | ISSN-L 归一、来源冲突显式化 |
| 模型幻觉 | 生成虚假指标或理由 | 事实字段只能来自 SourceFact；无来源不输出 |
| 劫持期刊网站 | 用户访问错误投稿入口 | 官方身份交叉核验；无法确认则排除正式榜单 |
| 用户误解“相对稳妥” | 被理解为保证录用 | 固定免责声明；不输出概率 |
| 全文隐私泄露 | 未发表成果或个人信息外传 | 本地解析、脱敏查询、外发需单独同意 |
| API 或网站变更 | 检索失败或字段过期 | 适配器、版本化、超时降级和来源健康检查 |

## 29. 推荐 Skill 包结构

后续实现可按渐进披露组织，避免把所有数据源和评分细节堆入入口说明：

~~~text
medical-journal-matcher/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── data-sources.md
│   ├── scoring-and-confidence.md
│   ├── output-schema.json
│   ├── report-template.md
│   ├── privacy-and-licensing.md
│   └── submission-taxonomy.md
└── scripts/
    ├── parse_manuscript.py
    ├── normalize_journals.py
    ├── validate_dois.py
    ├── score_candidates.py
    └── validate_output.py
~~~

仅在对应逻辑确实需要重复、确定性执行时创建脚本。SKILL.md 应保持简洁，负责触发条件、共享工作流、关键安全边界和按需读取 references 的路由。

## 30. 实现约束

### 30.1 Python 环境

若实现使用 Python：

- 使用 uv 管理 Python 版本与依赖。
- 使用 pyproject.toml 和 uv.lock 固化依赖。
- 在项目中创建 .env 供本地配置，并提供不含秘密的 .env.example。
- 将 .env 加入 .gitignore。
- API 密钥、联系邮箱和运行模式通过环境变量读取。

建议环境变量：

- JOURNAL_MATCHER_JCR_DATA_MODE。
- JOURNAL_MATCHER_PRIVACY_MODE。
- CLARIVATE_API_KEY。
- OPENALEX_API_KEY。
- NCBI_API_KEY。
- CROSSREF_CONTACT_EMAIL。
- UNPAYWALL_CONTACT_EMAIL。

具体变量只有在对应数据源启用时才要求配置。

### 30.2 配置版本

以下参数必须版本化：

- 匹配维度权重。
- 相似论文权重。
- 时间窗口和时间衰减。
- 评分覆盖度阈值。
- 置信度规则。
- 来源优先级。
- 正式推荐最低要求。

### 30.3 确定性校验

以下逻辑优先使用脚本或结构化规则，而不是完全依赖自由文本模型：

- DOI 格式化与解析。
- ISSN 格式与期刊去重。
- 硬门槛状态机。
- 分数计算。
- 输出字段完整性。
- 数据年份校验。
- 正式榜单不得包含 FAIL/UNVERIFIED 硬门槛。

模型适合承担：

- 稿件画像提取。
- 查询扩展。
- 主题、方法和读者契合解释。
- 来源支持下的中文报告撰写。

## 31. MVP 与后续版本

### MVP

- 生物医学与生命科学。
- 六类稿件。
- 标题/摘要/关键词及 PDF/DOCX 全文。
- DOAJ、OpenAlex、PubMed、Europe PMC、Crossref、NLM Catalog 与官网核验。
- 条件式 JCR 适配器。
- Markdown + JSON/YAML 输出。
- 独立轻量稿件就绪度预检。

### 后续版本

- 工程、人文和社会科学领域适配器。
- 叙述性综述、Letter、Commentary。
- 用户机构 APC 协议和 Read & Publish 支持。
- 绿色 OA 与自存档政策。
- 更成熟的期刊竞争性和用户基线模型。
- 本地向量索引与可复现数据快照。
- 多轮投稿历史与已拒稿期刊管理。
- 多人协作和机构级配置。
- 经人工标注校准的评分与分档模型。

## 32. 开发阶段待定项

以下是实现阶段需要通过原型和测试确定的技术选择，不构成当前产品需求缺口：

- 本地解析 PDF/DOCX 的具体库。
- 本地 embedding 模型或远程语义检索的组合。
- 各数据源缓存 TTL。
- 时间衰减参数。
- 低发文量期刊的收缩方法。
- 超出 MVP 最低 18 个样例后的人工评估规模。
- 0–1 语义相似度校准表的训练与更新方式。
- JSON Schema 中不影响 23.6 语义的描述性扩展字段。

这些选择不得改变本文确定的资格门槛、隐私、数据授权、评分分离和不预测录用等产品原则。

## 33. 权威资料与方法依据

### 数据与元数据

- Clarivate Web of Science Journals API：<https://developer.clarivate.com/apis/wos-journal>
- Clarivate JCR journals documentation：<https://journalcitationreports.zendesk.com/hc/en-gb/articles/28351400868625-Browsing-Journals>
- Clarivate Web of Science Core Collection / Master Journal List：<https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/web-of-science-core-collection/>
- DOAJ journal data model：<https://doaj.github.io/doaj-docs/master/data_models/OutgoingAPIJournal.html>
- DOAJ licensing requirements：<https://doaj.org/apply/copyright-and-licensing/>
- OpenAlex semantic search：<https://help.openalex.org/api/semantic-search/>
- OpenAlex works data：<https://help.openalex.org/data/works/>
- PubMed user guide and Similar Articles：<https://pubmed.ncbi.nlm.nih.gov/help/#similar-articles>
- NCBI E-utilities：<https://www.ncbi.nlm.nih.gov/books/NBK25497/>
- Europe PMC developer resources：<https://europepmc.org/developers>
- Crossref REST API：<https://www.crossref.org/documentation/retrieve-metadata/rest-api/>
- Crossref Retraction Watch data：<https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/>
- NLM Catalog journals：<https://www.ncbi.nlm.nih.gov/nlmcatalog/journals/>
- MeSH：<https://www.nlm.nih.gov/mesh/meshhome.html>

### 匹配方法与产品边界

- JANE journal matching paper：<https://pubmed.ncbi.nlm.nih.gov/18227119/>
- WTS venue recommendation study：<https://aclanthology.org/2020.findings-emnlp.78/>
- SPECTER scientific document representations：<https://aclanthology.org/2020.acl-main.207/>
- Topical and temporal journal profiles：<https://doi.org/10.1007/s11257-022-09354-7>
- Neural-network calibration limitations：<https://proceedings.mlr.press/v70/guo17a.html>

### 投稿与报告规范

- ICMJE manuscript preparation recommendations：<https://icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html>
- EQUATOR Network：<https://www.equator-network.org/>
- COPE transparency principles：<https://doi.org/10.24318/cope.2019.1.12>

## 34. 固定免责声明

最终报告必须包含以下含义完整的声明：

> 本结果基于用户提供的稿件信息、可访问数据源和查询当日可核验的期刊资料，仅用于辅助选刊和人工决策。匹配分及“冲刺、优先、相对稳妥”属于相对投稿策略，不是录用概率，也不构成录用保证。JIF、JCR 分区、APC、开放获取政策、投稿范围和出版速度可能变化，投稿前应在期刊官网及用户有权访问的 JCR 数据中再次核验。
