# GitHub Copilot Agent Skills {#cover-00-cover}

**実践で学ぶ設計・運用ガイド**

GitHub Copilot の Agent Skills を、基礎概念から実装・評価・運用まで体系的に学ぶための
実践チュートリアルです。

> 💡 ブラウザで https://duwenji.github.io/spa-quiz-app/ を開くと、関連トピックをクイズ形式で復習できます。

- 著者: 杜 文吉
- 対象: Copilot を本格活用したい開発者 / テックリード / 推進担当者
- テーマ: `skills` / evaluation / reusable templates / lifecycle

**この教材で学べること**
- Agent Skills の基本概念と動作メカニズム
- 従来プロンプト運用との違いと使い分け
- 実装パターンとサンプルスキルの設計方法
- 品質評価フレームワークと改善サイクル

# Part 0: スキル形式の選択と実装 {#chapter-00-fundamentals}

## Part 0: スキル形式の選択と実装 {#section-00-fundamentals-00-skill-format-overview}


### 重要な指摘

GitHub公式が推奨する **Agent Skills** の実装形式は **`SKILL.md`**です。  
このドキュメントでは、2つの形式の経緯、関係性、そして各々の利用場面と使い分けを説明します。

#### 🎓 Agent Skills はオープンスタンダード

**重要**: Agent Skills は Anthropic による**オープンスタンダード**です。プロプライエタリ仕様ではなく、複数のプラットフォームで活用できるように設計されています。

| 側面 | 説明 |
|-----|------|
| **標準化主体** | Anthropic（Claude 開発元） |
| **公開仕様** | https://agentskills.io/ |
| **参考実装** | https://github.com/anthropics/skills |
| **コミュニティ** | GitHub Awesome Copilot、その他 |
| **ライセンス** | MIT など自由なライセンスで公開可能 |

---

### � サポートされるプラットフォーム

Agent Skills は、以下の環境で利用できます：

| プラットフォーム | ステータス | 説明 |
|-------|--------|------|
| **Copilot coding agent** | ✅ 利用可能 | GitHub.com の Copilot Editor で実行可能 |
| **GitHub Copilot CLI** | ✅ 利用可能 | コマンドラインから `gh copilot` コマンドで実行 |
| **VS Code Insiders** | ✅ プレビュー | VS Code Insiders 版で実験的にサポート |
| **VS Code（stable）** | 🔜 近日対応 | 通常版 VS Code では近日リリース予定 |
| **GitHub.com UI** | ✅ 利用可能 | GitHub.com のウェブインターフェースで実行 |

#### 今から始める場合の推奨環境

```
【最初の学習】
→ GitHub.com の Copilot Editor（最も簡単）

【CLI作業が多い場合】
→ GitHub Copilot CLI

【VS Code を主に使う場合】
→ VS Code Insiders（安定版は近日リリース）
```

---

### �📋 フォーマットの経緯

#### バージョン進化

```
GitHub Copilot Agent Skills の発展 (2024-2026)

2024年 Q3-Q4: パイロット版
  └─ 初期形式：JSON APIベース
     （開発者向け、内部仕様）

2025年 Q1-Q2: ユーザーフレンドリー化
  └─ SKILL.md形式の導入
     （エンドユーザー向け、人間が読める）

2026年 Q1-現在: 本番運用体制確立
  └─ SKILL.md：エンドユーザー向け標準
  └─ JSON：内部通信フォーマット
  └─ 両者の統合・同期メカニズム
```

#### なぜ SKILL.md が採用されたのか

| 理由 | 詳細 |
|-----|------|
| **ユーザビリティ** | Markdown は開発者にとって自然な形式 |
| **可読性** | 記述と実行結果がほぼ同じ（WYSIWYG的） |
| **バージョン管理** | Git に自然に統合、変更追跡が容易 |
| **拡張性** | スクリプトや補助ファイルを付属させやすい |
| **コラボレーション** | チームでのレビュー・改善が直感的 |

---

### ① SKILL.md形式（公式推奨・エンドユーザー向け）

#### 概要

**GitHub公式が推奨する、エンドユーザーが直接作成・管理するスキル定義形式**

```markdown
SKILL.md = 開発者が読み書きする「手順書」
```

#### ファイル構造

```
myproject/
├── .github/
│   └── skills/
│       ├── code-review/
│       │   ├── SKILL.md          ← スキルの手順書
│       │   ├── checklist.md      ← 補助ドキュメント（選択）
│       │   └── review-script.py  ← 補助スクリプト（選択）
│       │
│       └── github-actions-debug/
│           ├── SKILL.md
│           └── debug-tools.sh
```

または個人スキル：
```
~/.copilot/skills/my-personal-skill/SKILL.md
~/.claude/skills/my-personal-skill/SKILL.md
```

#### 実装例

##### 例1: シンプルなコードレビュースキル

```markdown
---
name: code-review-helper
description: Guide for performing comprehensive code reviews using AI assistance
license: MIT
---

# Code Review Process

When asked to review code, follow these systematic steps:

## 1. Readability Check
- Variable naming: Are names descriptive and follow conventions?
- Code structure: Is the logic flow clear and logical?
- Comments: Are comments helpful and up-to-date?
- Function length: Are functions appropriately sized?

## 2. Performance Analysis
- Algorithmic complexity: Is the algorithm efficient?
- Loop optimization: Are there unnecessary nested loops?
- Memory usage: Is memory efficiently used?
- Database queries: Are queries optimized?

## 3. Security Review
- Input validation: Is user input properly validated?
- Authentication: Are auth checks present?
- Data exposure: Could sensitive data be leaked?
- SQL injection/XSS: Are there injection vulnerabilities?

## 4. Testing Coverage
- Are edge cases tested?
- Are error scenarios handled?
- Is the code testable and modular?

## Output Format

Provide feedback as a structured report with:
- Overall assessment (score 0-100)
- Issues by category (Readability, Performance, Security)
- Actionable recommendations
- Code snippets for fixes (if applicable)
```

##### 例2: GitHub Actions デバッグスキル（補助ファイル付き）

```markdown
---
name: github-actions-failure-debugging
description: Guide for debugging failing GitHub Actions workflows
license: MIT
---

# GitHub Actions Workflow Debugging

When asked to debug a failing GitHub Actions workflow, use these tools and processes:

## Tools Available
See `debug-tools.sh` for available debugging utilities.

## Process

1. **Identify the failed job**
   ```bash
   ./debug-tools.sh list-recent-runs --status failed
   ```

2. **Analyze the logs**
   Use the provided `log-analyzer.py` tool:
   ```bash
   python log-analyzer.py <workflow-run-id>
   ```

3. **Common Issues**
   Refer to `COMMON_ISSUES.md` for solutions

## When to Escalate
If issue is not in the checklist, provide:
- Full log output
- Error message details
- Environment context
```

#### 特徴

✅ **メリット**
- 開発者が直接編集・管理
- Markdown：人間が読みやすい
- Git による版管理が自然
-補助スクリプト・ファイルを附属可能
- リポジトリ自体が「スキルの例」になる
- チームでのコラボレーション容易

⚠️ **制限**
- パラメータの型チェックなし（エージェント側で推測）
- 出力フォーマット検証なし
- スキル間の依存関係管理が限定的

#### 配置ガイド

| スコープ | 場所 | 用途 |
|--------|------|------|
| プロジェクト固有 | `.github/skills/` | そのリポジトリだけで使用 |
| チーム共有 | `.github/skills/` （複数リポで共通） | 複数プロジェクトで使用 |
| 個人スキル | `~/.copilot/skills/` | あなたのマシンでのみ |
| 組織共有 | GitHub Skills Registry | 企業内全体で共有 |

> 💡 複数リポでの共通化や git submodule / subtree を使った配布手順 → [Part 4-6: 複数リポでの SKILL 共通化](#section-04-advanced-06-multi-repo-skill-sharing)

---

### ② JSON形式（内部通信・スキーマ検証用）

#### 概要

**Copilot サーバー側で管理される、内部通信フォーマット**

```json
JSON = SKILL.md から自動抽出される「構造化データ」
```

#### 目的

```
SKILL.md の指示
    ↓
Copilot が解析
    ↓
内部的に JSON へ変換
    ↓
パラメータ抽出・検証
    ↓
LLM 実行
    ↓
出力スキーマ検証
    ↓
ユーザーへ返却
```

#### 実装例

```json
{
  "id": "code-review-helper",
  "version": "1.0.0",
  "name": "code-review-helper",
  "description": "Guide for performing comprehensive code reviews",
  
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "Code to review",
      "maxLength": 5000
    },
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "java", "go"]
    }
  },
  
  "prompt": {
    "system": "You are an expert code reviewer...",
    "template": "Review this code...",
    "variables": ["code_snippet", "language"]
  },
  
  "outputFormat": {
    "type": "object",
    "properties": {
      "readabilityScore": { "type": "number" },
      "performanceScore": { "type": "number" },
      "issues": { "type": "array" }
    },
    "required": ["readabilityScore", "performanceScore", "issues"]
  },
  
  "validation": {
    "timeout": 30,
    "maxRetries": 2
  }
}
```

#### 特徴

✅ **メリット**
- 厳密な型チェック・検証
- パラメータ制約を明示的に定義
- 出力フォーマットを保証
- キャッシング・最適化が可能
- バージョニング・ロールバック容易
- API層での一元管理

⚠️ **デメリット**
- JSONは機械向け（人間にとって読みにくい）
- エンドユーザーが直接編集しにくい

---

### ③ フォーマット選択ガイド

#### 「どの場面で何を使うか」

##### SKILL.md を使うべき 

✅ **こんな時は SKILL.md**

```
□ GitHub/GitLab のリポジトリ内で管理したい
□ チーム全員でスキルを共有したい
□ スクリプトやツール呼び出しが必要
□ シンプルな指示で十分
□ 人間が読める形式が必要
```

**実装例**
- コードレビュー手順
- GitHub Actions デバッグフロー
- セキュリティチェックリスト
- テスト手順書
- リポジトリ固有の運用ガイド

**チェック項目**

```markdown
□ スキルを `.github/skills/` に配置した
□ SKILL.md に frontmatter (name, description) を記述
□ 人間が読める Markdown で手順を記述
□ 補助ファイルが必要なら追加
□ Git で管理・版管理
□ チームメンバーが参照可能

実装時間：30分～2時間
難度：⭐ 初心者向け
```

##### JSON を学ぶべき場面

✅ **こんな時は JSON を理解する**

```
□ Copilot Agent の内部メカニズムを知りたい
□ パラメータ検証やスキーマ設計を学びたい
□ API層での実装を理解したい
□ エンタープライズ向けシステム構築
□ 複数スキルを統合・オーケストレーション
```

**学習用途**
- Copilot Agent の内部アーキテクチャ理解
- スキル設計の深い学習
- 本チュートリアルでの概念説明
- API統合やシステム設計

---

### ④ 推奨される実装フロー

#### ステップバイステップ

```
Step 1: SKILL.md で設計 (30分)
  ├─ 目的・スコープを明確化
  ├─ 手順を Markdown で記述
  ├─ 補助ファイルが必要なら作成
  └─ チームでレビュー・改善
  　　 ↓ Git で管理・版管理

Step 2: 運用開始 (すぐ)
  ├─ リポジトリに配置
  ├─ `.github/skills/` に SKILL.md 配置
  ├─ Copilot が自動検出
  └─ ユーザーが実行開始
  　　 ↓ 効果測定・フィードバック

Step 3（オプション）: JSON スキーマ化 (2時間)
  ├─ 高度なパラメータ検証が必要な場合
  ├─ 複数スキル間の連携が必要な場合
  └─ エンタープライズ運用の場合
  　　 ↓ サーバー側で JSON スキーマ管理
```

#### 実装例：SKILL.md から開始

```
Week 1: SKILL.md で最初のスキルを作成
  └─ 目標：1-2時間で SKILL.md を完成

Week 2: チーム内での利用開始
  └─ 目標：フィードバック収集、改善

Week 3+: 必要に応じて JSON スキーマを追加
  └─ 複雑な検証が必要になった場合のみ
```

---

### ⑤ 比較表：SKILL.md vs JSON

| 観点 | SKILL.md（公式推奨） | JSON（内部仕様） |
|-----|-------|---------|
| **実装対象** | エンドユーザー | システム・API層 |
| **形式** | Markdown + YAML frontmatter | 構造化JSON |
| **保存場所** | `.github/skills/` or `~/.copilot/skills/` | Copilot サーバー |
| **管理方法** | Git での版管理 | API層での管理 |
| **可読性** | ⭐⭐⭐⭐⭐ 優秀 | ⭐⭐ 機械向け |
| **拡張性** | ⭐⭐⭐⭐ 補助ファイル可 | ⭐⭐⭐ スキーマで定義 |
| **パラメータ検証** | なし（エージェント側で推測） | ⭐⭐⭐⭐⭐ 厳密 |
| **学習容易さ** | ⭐⭐⭐⭐⭐ 簡単 | ⭐⭐ 難しい |
| **本番対応** | ✅ 推奨 | 内部用 |
| **バージョン管理** | ✅ Git が自然 | API層で管理 |

---

### ⑥ チュートリアルでの位置づけ

#### このチュートリアルについて

```
このチュートリアルの構成：

Part 1「基礎編」
  └─ SKILL.md の概念と使い方 ← 実装向け

Part 2「比較編」
  └─ MCP、他ツールとの比較

Part 3「実装編」
  ├─ サンプル SKILL.md の実装例 ← 実際の形式
  └─ JSON スキーマも説明 ← 内部メカニズム理解用

Part 4「高度な活用」
  ├─ チーム共有とスキル管理
  └─ 最適化とトラブルシューティング

Part 5「高度なトピック」
  └─ 複合スキル、API統合、ベストプラクティス
```

#### 推奨学習パス

```
初心者向け
  1. Part 1: SKILL.md の基礎
  2. Part 3: サンプル SKILL.md を作成
  3. 実装・運用開始
  4. 必要に応じて JSON スキーマ学習

特にJSON形式の詳細を知りたい方向け
  1. Part 1: SKILL.md の基礎理解
  2. このドキュメント「形式比較」で内部メカニズム理解
  3. Part 3 の JSON 説明で詳細学習
```

---

### ⑦ よくある質問

#### Q1. SKILL.md だけで十分？

**A:** ほとんどの場合、SKILL.md で十分です。

```
SKILL.md で始めましょう
    ↓
タイプチェック・出力検証が必要になったら
    ↓
その时初めて JSON スキーマを検討
```

#### Q2. JSON は必須？

**A:** 不要です。

```
必要な場合：
- 複雑なパラメータ検証
- 複数スキル間の厳密な連携
- エンタープライズシステム

不要な場合：
- シンプルなスキル
- 個人・チーム内での利用
- 初期段階
```

#### Q3. SKILL.md から JSON は自動生成できる？

**A:** 部分的に可能です。

```
現状：
- Copilot が SKILL.md を読んでパラメータを推測
- 完全な JSON スキーマの自動生成ではない
- 複雑な検証が必要な場合は手動作成推奨
```

---

### まとめ

| What | SKILL.md | JSON |
|------|----------|------|
| **使うべき対象** | ほぼすべての開発者 | システム開発者・API設計者 |
| **実装形式** | 公式推奨 | 内部仕様 |
| **学習順序** | 1番目（Part 1）| 2-3番目（理解の深化用） |
| **実装難度** | ⭐ 簡単 | ⭐⭐⭐ 難しい |
| **判断基準** | **先ず SKILL.md で始めよう** | **複雑さが必要になったら検討** |

---

---

### SKILL.md YAML Frontmatter 完全仕様

#### Frontmatter とは

SKILL.md ファイルの最初の YAML ブロック（`---` で挟まれた部分）です。スキルのメタデータと基本設定を記述します。

```yaml
---
name: スキルの識別子
description: スキルの説明と使用時機
【オプション】
license: ライセンス
compatibility: 互換性・環境要件
metadata: 追加情報
allowed-tools: 事前承認ツール
---
```

#### 必須フィールド

##### `name` （必須、64文字以下）

スキルの一意の識別子。

**ルール**
- 小文字、数字、ハイフン（`-`）のみ使用可
- 大文字は不可
- 空白やアンダースコアは不可
- ハイフンで開始・終了しない
- 連続ハイフン（`--`）は不可
- ディレクトリ名と一致する必要がある

**例**
```yaml
# ✅ 有効
name: pdf-processing
name: code-quality-analyzer
name: data-transformation-v2

# ❌ 無効
name: PDF Processing      # 空白・大文字
name: pdf--processing     # 連続ハイフン
name: -pdf-processing     # ハイフンで開始
name: pdf_processing      # アンダースコア
```

##### `description` （必須、1024文字以下）

スキルの説明と使用時機。エージェントがスキルを発見・選択する基準になります。

**推奨要素**
1. **何ができるか** - スキルの機能や処理内容
2. **いつ使うか** - トリガーになるキーワードや文脈
3. **具体的な例** - 実際の使用場面

**例**
```yaml
# ✅ 優秀：機能 + 使用時機 + キーワード
description: Extracts text and tables from PDF files, fills forms, and merges PDFs. Use when working with PDF documents, forms, or when the user mentions PDFs, PDFs, extraction, or document processing.

# ✅ 良好：機能 + 使用時機
description: Analyzes code quality across Python, JavaScript, TypeScript and detects readability, performance and security issues. Use for code reviews or when analyzing code for improvement.

# ❌ 不十分：曖昧
description: Helps with documents
description: Processes data
```

#### オプションフィールド

##### `license` （オプション）

スキルに適用されるライセンス。

```yaml
# ライセンス名
license: MIT
license: Apache-2.0
license: GPL-3.0

# または参照ファイル
license: "Proprietary. See LICENSE.txt for details"
```

##### `compatibility` （オプション、500文字以下）

スキルの環境要件や互換性情報。

```yaml
# 前提環境・ツール要件
compatibility: "Requires Node.js 18+, Python 3.9+, and git"

# 対応プラットフォーム
compatibility: "Designed for Claude Code and GitHub.com Copilot Editor"

# ネットワーク・外部システム要件
compatibility: "Requires internet access and GitHub API authentication"

# 複数条件
compatibility: "Requires: Python 3.8+, pandas, numpy. Supports: Claude Sonnet 3.5+. Git-integrated repositories only."
```

**使用例**
```yaml
---
name: github-actions-debugger
description: Debugs failing GitHub Actions workflows
compatibility: "Requires GitHub API access and repository admin permissions"
---
```

##### `metadata` （オプション）

任意のキー・バリュー情報。スキルについてのメタ情報を記述します。

```yaml
metadata:
  author: "Alice Development Team"
  version: "1.2.0"
  category: "code-quality"
  tags:
    - python
    - javascript
    - testing
  homepage: "https://docs.example.com/my-skill"
```

**推奨キー**
| キー | 例 | 用途 |
|------|-----|------|
| `author` | `"Team Name"` | 作成・管理チーム |
| `version` | `"1.0.0"` | セマンティックバージョン |
| `category` | `"code-analysis"` | スキルの分類 |
| `tags` | `["python", "testing"]` | 検索・フィルタ用タグ |
| `homepage` | URL | ドキュメント・サポート URL |

##### `allowed-tools` （オプション、実験的）

スキルが使用を許可されたツールのリスト（スペース区切り）。

```yaml
# Git と jq の使用を許可
allowed-tools: "Bash(git:*) Bash(jq:*) Read"

# 特定バージョンに制限
allowed-tools: "Python(3.9+) Bash(*)"

# MCP ツール参照
allowed-tools: "GitHub:create_issue GitHub:list_files Read"
```

**形式**: `ToolName(scope:action)` または `ToolName:tool_name`

#### 完全な実装例

##### 例1：シンプルなスキル

```yaml
---
name: commit-message-generator
description: Generates meaningful commit messages from git diffs. Use when writing commit messages, describing changes, or needing help with version control documentation.
license: MIT
---
```

##### 例2：完全な定義

```yaml
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files, forms, document extraction, or PDF manipulation.
license: Apache-2.0
compatibility: "Requires Python 3.8+ with pdfplumber library. Supports Claude Sonnet 3.5+. Optional: OCR requires tesseract-ocr."
metadata:
  author: "Document Processing Team"
  version: "2.1.0"
  category: "document-processing"
  tags:
    - pdf
    - text-extraction
    - forms
    - document-management
  homepage: "https://docs.example.com/pdf-processing"
  updated: "2026-03-09"
allowed-tools: "Python(3.8+) Bash(pdf*) Read"
---
```

##### 例3：エンタープライズスキル

```yaml
---
name: database-migration-assistant
description: Guides database schema migrations with validation and rollback support. Use for schema changes, data transformation, migration planning, or database refactoring tasks.
license: "Proprietary. See LICENSE.md"
compatibility: "Requires: PostgreSQL 12+, Python 3.10+, access to git repository. Supports: production and staging environments only."
metadata:
  author: "Database Engineering Team"
  version: "3.0.1"
  category: "database"
  subcategory: "migrations"
  tags:
    - postgresql
    - migration
    - schema-management
    - data-integrity
  homepage: "https://internal-docs.company.com/db-migrations"
  support-channel: "#database-team"
  sla: "4-hour response time"
allowed-tools: "Bash(psql:*) Bash(git:*) Python(3.10+) Read Write"
---
```

---

### Progressive Disclosure（段階的情報開示）

#### 概念

スキルで使用する情報を複数ファイルに分割し、**必要な時点で段階的に読み込む** パターンです。これにより、エージェントの文脈に余裕が生まれ、より効果的に実行できます。

```
段階1: メタデータ（常に先読み）
├─ name, description
├─ 文脈効率：～100トークン
└─ 目的：スキル選択の判断基準

段階2: 指示内容（スキル起動時に読み込み）
├─ SKILL.md 本文（Markdown の手順・例）
├─ 文脈効率：＜5000トークン、推奨500行以内
└─ 目的：スキルの実行手順・ガイドライン

段階3: 参考資料（必要に応じて読み込み）
├─ references/REFERENCE.md
├─ references/API.md
├─ examples.md
├─ 文脈効率：オンデマンド読み込み
└─ 目的：詳細情報・API仕様・事例集
```

#### 実装パターン

##### パターン1：基本 + 参照ファイル

**ディレクトリ構造**
```
pdf-processing/
├── SKILL.md                  # 主要指示
├── references/
│   ├── FORMS.md             # フォーム入力ガイド
│   ├── API.md               # pdfplumber API リファレンス
│   └── EXAMPLES.md          # 使用例集
└── scripts/
    └── process_pdf.py       # 実行スクリプト
```

**SKILL.md の内容**
```markdown
---
name: pdf-processing
description: ...
---

# PDF Processing

## Quick Start

用 pdfplumber for extraction:
\`\`\`python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
\`\`\`

## Features

- **Text extraction**: [Quick examples](examples.md) | [Full API reference](references/API.md)
- **Form filling**: See [FORMS.md](references/FORMS.md) for step-by-step guide
- **Advanced usage**: See [EXAMPLES.md](references/EXAMPLES.md)
```

**参照ファイルは必要な時だけ読まれます。**

##### パターン2：ドメイン別整理

大規模スキルの場合、複数ドメインを参照ファイルで分割。

**ディレクトリ構造**
```
bigquery-analytics/
├── SKILL.md                  # ナビゲーション・概要
├── datasets/
│   ├── finance.md           # 財務データスキーマ
│   ├── sales.md             # 営業パイプラインスキーマ
│   └── product.md           # プロダクト使用状況スキーマ
└── scripts/
    └── query_builder.py
```

**SKILL.md**
```markdown
---
name: bigquery-analytics
description: Query BigQuery datasets for finance, sales, product data
---

# BigQuery Analytics

Select a domain:

- **Finance data**: Revenue, ARR, margin analysis → See [datasets/finance.md](datasets/finance.md)
- **Sales pipeline**: Opportunities, forecasting → See [datasets/sales.md](datasets/sales.md)
- **Product usage**: API metrics, adoption → See [datasets/product.md](datasets/product.md)
```

**ユーザーが「finance」を求めると、finance.md のみ読み込まれます。**

##### パターン3：基本 + 条件付き詳細

シンプルな手順 + オプション情報

```markdown
---
name: docx-processing
description: Create, edit, and manipulate DOCX documents
---

# DOCX Processing

## Basic Document Creation

Use docx-js library:
\`\`\`python
from docxjs import Document
doc = Document()
doc.add_paragraph("Hello")
doc.save("output.docx")
\`\`\`

## Advanced Features

**Tracked changes** (for collaboration):
→ See [TRACKED_CHANGES.md](TRACKED_CHANGES.md)

**Complex formatting**:
→ See [FORMATTING.md](FORMATTING.md)

**XML manipulation**:
→ See [OOXML_DETAILS.md](OOXML_DETAILS.md)
```

Tracked_CHANGES.md は、ユーザーが「追跡」や「変更」をリクエストした時だけ読まれます。

#### 実装のコツ

##### 1. ファイルサイズに注意

```
SKILL.md（主指示）
├─ 推奨：500行以内
├─ 上限：1000行
└─ 超える場合は参照ファイルに分割

References（参照ファイル）
├─ 1ファイル：100～500行
├─ 目次を含める（100行超える場合）
└─ ネストしない（1段階深さのみ）
```

##### 2. 参照の明確性

```markdown
# ❌ 曖昧
詳細は別ファイルを参照してください

# ✅ 明確
**Advanced options**: See [configuration.md](configuration.md)
**API reference**: See [references/API.md](references/API.md)
**Usage examples**: See [examples.md](examples.md)
```

##### 3. 相対パス（重要）

```markdown
# ✅ 相対パス（すべてのプラットフォームで動作）
See [guide.md](references/guide.md)
Run: python scripts/process.py

# ❌ 絶対パス（Windows で失敗）
See [guide.md](/home/user/skills/references/guide.md)
C:\skills\scripts\process.py
```

##### 4. 目次を含める（100行超える参照ファイル）

```markdown
# API Reference

## Contents
- Authentication
- Core methods (create, read, update)
- Advanced features
- Error handling
- Examples

## Authentication
...

## Core methods
...
```

#### 効果

**トークン効率**
```
レファレンスなし（全て SKILL.md に):
└─ 常に 5000+ トークン消費

Progressive disclosure（参照ファイル分割）:
├─ メタデータ：100 トークン（常に）
├─ SKILL.md 本文：2000 トークン（起動時）
├─ 参照ファイル：オンデマンド（必要時のみ）
└─ → 平均削減：30-50% のトークン節約
```

**ユーザー体験**
- 起動が高速（メタデータのみ先読み）
- 不要な情報を読まない
- 詳細が必要な時だけアクセス

---

### 関連ドキュメント

- 📖 GitHub 公式: [Creating agent skills](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills)
- 📚 本チュートリアル
  - Part 1-1: Agent Skills とは
  - Part 3-1: スキル開発の始め方
  - Part 3-6: スキル評価フレームワーク
  - Part 4-5: スクリプト設計ベストプラクティス

# Basics {#chapter-01-basics}

## Part 1-1: Agent Skills とは何か {#section-01-basics-01-introduction}


### 概要

**GitHub Copilot Agent Skills** は、GitHub Copilotに対して**再利用可能な手順書（スキル）を教え込む機能**です。

開発者が繰り返し使うプロンプトパターンを、一度スキルとして定義すれば、何度でも再利用できます。

こうすることで、チーム全体で統一された作業フローと品質を保つことができます。

#### 📖 オープンスタンダード

⚠️ **重要**: Agent Skills は **Anthropic が管理するオープンスタンダード** です。

```
Agent Skills = Anthropic のオープンスタンダード
         ↓
    GitHub Copilot, GitHub Copilot CLI, Claude など
    複数のプラットフォームで利用可能
```

- **公式ドキュメント**: https://agentskills.io/
- **オープンソース参考実装**: https://github.com/anthropics/skills
- **コミュニティ**: [Awesome Copilot](https://github.com/github/awesome-copilot) - コミュニティスキル集

#### 利用可能なプラットフォーム

- ✅ GitHub.com（Copilot Editor）
- ✅ GitHub Copilot CLI
- ✅ VS Code Insiders（プレビュー）
- 🔜 VS Code（近日対応）

詳細は [README: サポートされるプラットフォーム](../../README.md#サポートされるプラットフォーム)を参照。

---

### Agent Skillsが解決する課題

#### 課題1: 毎回同じプロンプトを書く手間

```
❌ 従来: 毎日、毎回、長いプロンプトを手入力
✅ Agent Skills: 定義したスキルをワンクリックで実行
```

#### 課題2: プロンプトの統一性難

```
❌ 従来: 担当者によってプロンプトの質がばらばら
✅ Agent Skills: チーム全体で統一されたルールを適用
```

#### 課題3: 知識・ノウハウの共有難

```
❌ 従来: 「このプロンプトの工夫」は個人のノウハウで終わり
✅ Agent Skills: スキル化することで、チーム全体で共有・再利用・改善
```

#### 課題4: 複雑なワークフローの管理

```
❌ 従来: 「Step 1, 2, 3...」と複数のプロンプトを手動で順序立てて実行
✅ Agent Skills: スキルをチェーンして自動実行
```

### Agent Skillsの定義

> **Agent Skill** = Copilotに教え込む**再利用可能な作業手順**（プロンプトテンプレート + メタデータ）

#### 実装形式の選択

⚠️ **重要**: スキルを実装する方法は **2 つ** あります。

| 形式 | 保存場所 | 推奨対象 | 学習パス |
|------|---------|---------|--------|
| **SKILL.md**（推奨） | `.github/skills/SKILL.md` | ほぼすべての開発者 | [Part 0: スキル形式の理解](../../00-fundamentals/00-skill-format-overview.md) |
| **JSON**（参考） | API層・内部管理 | システム開発者・複雑なケース | このセクション以降 |

👉 **初めての方は [Part 0: スキル形式の理解](../../00-fundamentals/00-skill-format-overview.md) をお読みください。**

---

#### 構成要素

| 要素 | 説明 | 例 |
|------|------|------|
| **スキル名** | わかりやすい識別子 | `analyze-code-quality` |
| **説明** | スキルが何をするのか | 「Pythonコードのコード品質を分析」 |
| **入力（パラメータ）** | ユーザーが提供する情報 | `code_snippet`, `language` |
| **実行ロジック** | 実際のプロンプト処理 | 「以下のコードについて...」 |
| **出力形式** | 期待される結果の形式 | JSON, Markdown表, など |

### 従来のプロンプト手法との違い

#### 使い方の比較

| 観点 | 一般的なプロンプト | Agent Skills |
|------|------------------|-------------|
| **毎回の入力** | 毎回、長いプロンプトを手入力 | スキル名 + パラメータのみ |
| **学習コスト** | 低い（すぐに始められる） | 中程度（初回セットアップが必要） |
| **スケーラビリティ** | 低い（10個以上のパターンは管理が困難） | 高い（数十個のスキルを管理可能） |
| **チーム共有** | プロンプトテキストを共有 | スキルを登録・共有 |
| **改善の容易さ** | プロンプト改善時に全員にメール | スキル更新時に全員が自動で最新版を利用 |
| **バージョン管理** | 手動で「v1」「v2」と区別 | リポジトリで自動管理 |

### スキルの実行方法

#### 方法1: 明示的なスキル指定

```
User: "スキル: analyze-code-quality で、このコードを分析してください"

Copilot:
  ├─ スキル「analyze-code-quality」を検索
  ├─ パラメータを自動抽出（コード、言語等）
  └─ スキルを実行 → 結果返却
```

**利点：** スキル名が明確で、確実に目的のスキルが実行される

#### 方法2: 自然言語による自動選択（推奨）

```
User: "このコードの品質を分析してください"

Copilot エージェント:
  ├─ ユーザー意図を解析
  ├─ 最適なスキルを自動選択（複数候補がある場合は確認）
  ├─ 必要なパラメータを自動抽出
  └─ スキルを実行 → 結果返却
```

**利点：** ユーザーはスキル名を覚える必要がなく、自然な言葉で指示できる

詳細は [Part 1-3: スキル自動選択メカニズム](#section-01-basics-03-how-skills-work) を参照。

---

### スキルのライフサイクル

```
┌─────────────────────────────────────────────┐
│ 1. 設計フェーズ                              │
│ - スキルの目的を定義                        │
│ - 入出力の仕様を決定                        │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│ 2. 実装フェーズ                              │
│ - スキル定義ファイル（JSON/YAML）を作成    │
│ - プロンプトテンプレートを記述             │
│ - ローカルでテスト                         │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│ 3. インストール・公開フェーズ                │
│ - リポジトリに登録                         │
│ - チーム内で共有                           │
│ - 外部リポジトリで公開（オプション）       │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│ 4. 使用フェーズ                              │
│ - ユーザーがスキルを実行                   │
│ - フィードバックを収集                     │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│ 5. メンテナンス・改善フェーズ               │
│ - ユーザーフィードバックに基づき改善       │
│ - スキルの最適化                           │
│ - 非推奨化・廃止（もし必要）               │
└─────────────────────────────────────────────┘
```

### Agent Skillsの活用シーン

#### シーン1: 企業内コーディング規約の統一

❌ **従来**
```
新入社員が毎日、長い規約テキストをCopilotに貼り付ける
              ↓
「この規約に従ってコードをレビューしてください」
```

✅ **Agent Skillsを利用**
```
Copilot: 「code-review-by-company-standards」スキルで自動レビュー
              ↓
  常に最新の規約が自動適用
```

#### シーン2: ドキュメント自動生成

❌ **従来**
```
毎回、関数の説明フォーマットを手入力してプロンプト作成
```

✅ **Agent Skillsを利用**
```
コードを選択 → 「generate-docstring」スキル実行
              ↓
  ドキュメント自動生成（チーム統一フォーマット）
```

#### シーン3: セキュリティチェック

❌ **従来**
```
セキュリティエキスパートが作ったチェック項目を、
毎回Copilotに説明する
```

✅ **Agent Skillsを利用**
```
「security-vulnerability-check」スキルで自動スキャン
              ↓
  セキュリティエキスパートの知識がコード化され、
  全員が同じレベルでセキュリティチェック可能
```

### このチュートリアルで学べること

| 段階 | 内容 |
|------|------|
| **Part 1: 基礎編** | Agent Skillsの概念と仕組みを理解 |
| **Part 2: 比較分析編** | MCP等の選択肢との使い分けを判断 |
| **Part 3: 実装編** | 実際にスキルを3つ作成 |
| **Part 4: 活用編** | チームで共有・運用する方法 |
| **Part 5: Advanced** | 高度な応用テクニック |

### 次へ進む

→ [Part 1-2: 従来のプロンプト手法との違い](#section-01-basics-02-vs-traditional)

## Part 1-2: 従来のプロンプト手法との違い {#section-01-basics-02-vs-traditional}


### 比較表

| 項目 | 従来（毎回プロンプト手入力） | Agent Skills |
|------|------------------------|------------|
| **再利用性** | 低 | 高 |
| **入力の手軽さ** | 複雑（毎回長いプロンプトを入力） | シンプル（スキル名 + パラメータのみ） |
| **学習曲線** | 短（すぐに始められる） | 中（初回セットアップが必要） |
| **スケーラビリティ** | 低（5-10個のパターンが限度） | 高（数十個のスキルを管理可能） |
| **チーム共有** | 困難（プロンプト文をメール・Slackで共有） | 容易（リポジトリで統一管理） |
| **プロンプト改善** | 毎回 | 初回のみ |
| **バージョン管理** | なし、または手動 | git等で自動管理 |
| **団体での統一性** | ばらばら | 統一 |
| **メンテナンス** | 困難（改善をすべてのユーザーに周知する必要） | 容易（スキル更新で全員に反映） |
| **複雑なワークフロー** | 複数ステップを手動で管理 | スキルのチェーンで自動化 |

### 詳細な比較

#### 1. 再利用性

##### 従来のプロンプト手法

```
Step 1: プロンプトを思い出す（または検索）
Step 2: プロンプトをコピー
Step 3: パラメータを現在のタスクに応じて修正
Step 4: Copilotに貼り付け
Step 5: 実行

※ 毎回、このプロセスを繰り返す
```

**問題点：**
- 毎回時間がかかる
- プロンプトを忘れたら一から書き直し
- チーム内で同じものを何度も作る（無駄）

##### Agent Skillsの場合

```
Step 1: Copilotに「使いたいスキル名」を指定
Step 2: パラメータだけ入力
Step 3: 実行

※ スキルは何度でも再利用可能
※ 改善されたスキルは全員が利用可能
```

**メリット：**
- 毎回シンプル
- スキルは一度作ったら使い続けられる
- チーム全体で知見が蓄積

---

#### 2. 入力の手軽さ

##### 従来の例

あなたは Python コードのコード品質を分析したい：

```
「以下のPythonコードについて、
1. 可読性（変数名、コメント）
2. パフォーマンス（不必要なループ、メモリ使用）
3. セキュリティ（入力検証、エラーハンドリング）
4. テスト容易性（関数の単位性）

の4つの観点から、改善点を指摘してください。
フォーマットはJSON形式で以下の構造でお願いします：
{
  "readability": { "score": X, "issues": [...] },
  ...
}

コード：
```python
[ここにコードを貼り付け]
```
」

← 毎回この長いプロンプトを入力する必要がある
```

##### Agent Skillsの場合

**方法A: 明示的なスキル指定**

```
ユーザー: "スキル: analyze-code-quality で分析して"

Copilot:
  ├─ スキルを検索・確認
  ├─ パラメータ入力を促進（コード・言語等）
  └─ スキル実行
```

**方法B: 自然言語による自動選択（推奨のUX）**

```
ユーザー: "このコードの品質を分析してください"

Copilot エージェント:
  ├─ ユーザー意図を解析
  ├─ 最適スキル「analyze-code-quality」を自動選択
  ├─ 必要パラメータを自動抽出
  └─ スキル実行
```

**どちらの場合も、パラメータを指定するだけでOK スキルのプロンプトロジックは定義済み**

詳細は [Part 1-3: スキルの自動選択メカニズム](#section-01-basics-03-how-skills-work) を参照。

---

#### 3. 学習曲線

##### 従来のプロンプト手法

**学習コスト：低い**
- 今日からすぐに始められる
- プロンプトのコツを少し知れば良い

```
Good: 初心者向け
Bad: 複雑なプロンプトテクニックが必要な場合、また習熟に時間がかかる
```

##### Agent Skillsの場合

**学習コスト：中程度**
- スキル定義の方法を学ぶ必要
- しかし一度習得すれば、スキル作成が効率化

```
学習曲線：
      │     ╱─────── Agent Skillsでの生産性
      │    ╱
      │   ╱
生産性 ├──╱──────────── 従来のプロンプト手法
      │╱
      └─────────────────
         時間
```

初期投資が必要だが、長期的には Agent Skills の方が生産性が高い

---

#### 4. スケーラビリティ

##### 従来のプロンプト手法

```
5個のプロンプトパターン：管理可能
10個のプロンプトパターン：混乱し始める
20個以上：管理不可能
```

**理由：**
- どのプロンプトをどこに保存したか分からなくなる
- プロンプト間の一貫性が保たれない
- 改善時に全て修正する必要

##### Agent Skillsの場合

```
5個のスキル：容易
20個のスキル：管理可能（リポジトリ化すれば）
100個のスキル：組織的に管理可能
```

**理由：**
- リポジトリで一元管理
- メタデータで検索・分類可能
- バージョン管理で改善を追跡

---

#### 5. チーム共有

##### 従来のプロンプト手法

```
❌ プロセス
1. Aさんが優れたプロンプトを作成
2. Slackで共有
3. Bさんがそれを参考に自分用にカスタマイズ
4. Cさんはそれを知らずに同じものを一から作成
5. Aさんがプロンプトを改善しても、
   Bさん、Cさんに通知されず、古いバージョンを使い続ける

→ 知識が組織に蓄積されない & 都度都度、バージョン違いが発生
```

##### Agent Skillsの場合

```
✅ プロセス
1. Aさんが優れたスキルを作成・リポジトリに登録
2. 全員が同じスキルを利用
3. Aさんがスキルを改善
4. 全員が自動で最新版を利用

→ 組織全体で常に最新・統一版を使用
```

---

#### 6. プロンプト改善

##### 従来のプロンプト手法

```
プロンプト v1 を使用中
         ↓
改善案が出た（例：より詳しいフォーマット）
         ↓
プロンプト v2 を新規作成
         ↓
チームメンバーにメール通知
         ↓
❌ 誰が v1, v2 どちらを使ってるか不明確
❌ 古いバージョンを使い続ける人が発生
```

##### Agent Skillsの場合

```
スキル v1.0 を使用中
         ↓
改善案が出た
         ↓
スキル v1.1 をリリース
         ↓
✅ 全員が自動で最新版を利用
✅ 改善による効果がチーム全体で実効
```

---

#### 7. バージョン管理

##### 従来のプロンプト手法

```
- 手動で「prompt_v1.txt」「prompt_v2.txt」と区別
- 誰が、いつ、何を改善したのか不明確
- Git等のVCS（バージョン管理システム）を活用しない
```

##### Agent Skillsの場合

```
- Git で自動管理
- commit メッセージで改善内容を記録
- 誰が何を改善したのかが明確に追跡可能
- 必要に応じて過去バージョンへのロールバックも可能
```

---

#### 8. チーム内の統一性

##### 従来のプロンプト手法

```
Aさんの使用するプロンプト：
  「以下のコードについて品質を評価してください。
   フォーマットは Markdown表でお願いします」

Bさんの使用するプロンプト：
  「コード品質チェック：可読性、パフォーマンス。
   JSONフォーマットで返してください」

❌ 同じタスクなのに、出力フォーマットが異なる
❌ 結果の比較や統合が困難
```

##### Agent Skillsの場合

```
「analyze-code-quality」スキル：
  全員が同じプロンプト・同じ出力フォーマットを使用

✅ チーム全体で統一された品質分析
✅ 結果の比較・統合が容易
```

---

#### 9. メンテナンスの負担

##### 従来のプロンプト手法

**プロンプト改善時：**
```
Step 1: 改善されたプロンプトを作成
Step 2: チームメンバー全員に通知
Step 3: 各自が手動で変更
Step 4: ❌ 誰が対応したか確認する手間
Step 5: ❌ 古いバージョンを使い続ける人がいる
```

**コスト：高い**（毎回チーム全体の手間がかかる）

##### Agent Skillsの場合

**スキル改善時：**
```
Step 1: リポジトリのスキルを更新
Step 2: コミット・プッシュ
Step 3: ✅ 全員が自動で最新版を利用

完了！
```

**コスト：低い**（自動で全員に反映）

---

#### 10. 複雑なワークフロー

##### 従来のプロンプト手法

例：「コード品質分析」→「改善提案」→「テスト生成」という3ステップのワークフロー

```
Step 1: 最初のプロンプトで品質分析
        結果をコピー
        ↓
Step 2: 結果を含む新しいプロンプトで改善提案
        結果をコピー
        ↓
Step 3: 結果を含む新しいプロンプトでテスト生成

❌ 手動でデータを受け渡す
❌ 3ステップ×複数のプロンプト = ミスが増える
```

##### Agent Skillsの場合

```
「code-quality-pipeline」スキル

スキル構成：
  └─ 分析スキル
  └─ 改善提案スキル
  └─ テスト生成スキル

を自動でチェーン実行

✅ ワンコマンドで全ステップ実行
✅ 自動でデータ受け渡し
```

---

### 結論

| 用途 | 向いている手法 |
|------|-------------|
| **1回限りのタスク** | 従来のプロンプト手法 |
| **個人での仕事** | どちらでも OK |
| **繰り返し使うパターン（5個以上）** | Agent Skills |
| **チーム内で統一する必要がある** | Agent Skills |
| **複雑なワークフロー** | Agent Skills |
| **組織全体での知識共有** | Agent Skills |

---

### 次へ進む

→ [Part 1-3: スキルの仕組み理解](#section-01-basics-03-how-skills-work)

## Part 1-3: スキルの仕組み理解 {#section-01-basics-03-how-skills-work}


### スキルの内部構造

#### 概要図

```
User Interface
      ↓
┌─────────────────────────────────────┐
│  スキル実行リクエスト                  │
│  (スキル名 + パラメータ)              │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Copilot Agent Skills                │
│  - メタデータの検証                   │
│  - パラメータの処理                   │
│  - プロンプトテンプレートの展開      │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  LLM（言語モデル）                    │
│  - 生成 API に送信                    │
│  - 応答を生成                         │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  出力処理                             │
│  - フォーマットの検証                 │
│  - 返却形式の変換                     │
└────────────┬────────────────────────┘
             │
             ↓
        出力結果
```

### スキル定義ファイルの構成

#### JSON形式の例

```json
{
  "id": "analyze-code-quality",
  "version": "1.0.0",
  "name": "コード品質分析",
  "description": "Pythonコードのコード品質を複合的に分析し、改善点を提案します",
  
  "metadata": {
    "author": "Copilot Team",
    "created": "2026-01-15",
    "lastUpdated": "2026-03-07",
    "category": "code-analysis",
    "tags": ["python", "quality", "analysis"]
  },
  
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "分析対象のPythonコード",
      "required": true,
      "maxLength": 5000
    },
    "language": {
      "type": "string",
      "description": "プログラミング言語",
      "enum": ["python", "javascript", "typescript", "java"],
      "required": true
    },
    "focusAreas": {
      "type": "array",
      "description": "重点分析エリア",
      "items": { "enum": ["readability", "performance", "security", "testability"] },
      "required": false,
      "default": ["readability", "performance", "security", "testability"]
    }
  },
  
  "prompt": {
    "system": "You are an expert code reviewer with deep knowledge of best practices...",
    "template": "Analyze the following {language} code for quality issues...",
    "variables": ["{code_snippet}", "{focusAreas}"]
  },
  
  "outputFormat": {
    "type": "json",
    "schema": {
      "readability": {
        "score": "number (0-100)",
        "issues": "array of strings"
      },
      "performance": {
        "score": "number (0-100)",
        "issues": "array of strings"
      },
      "security": {
        "score": "number (0-100)",
        "issues": "array of strings"
      },
      "testability": {
        "score": "number (0-100)",
        "issues": "array of strings"
      },
      "overallScore": "number (0-100)",
      "recommendations": "array of strings"
    }
  },
  
  "validation": {
    "timeout": 30,
    "maxRetries": 2
  }
}
```

#### 各要素の説明

| 要素 | 説明 | 例 |
|------|------|------|
| **id** | スキルの一意な識別子（ハイフン区切り） | `analyze-code-quality` |
| **version** | セマンティックバージョニング | `1.0.0` |
| **name** | ユーザーが目にする名前（日本語可） | `コード品質分析` |
| **description** | スキルの説明（複数行可） | 「Pythonコードの...」 |
| **metadata** | スキルのメタ情報 | 作成者、作成日、カテゴリ等 |
| **parameters** | 入力パラメータの定義 | 型、必須性、制約等 |
| **prompt** | LLMに渡す指示文 | システムプロンプト + テンプレート |
| **outputFormat** | 出力の形式・スキーマ | JSON, CSV, Markdown等 |
| **validation** | 実行時の制約 | タイムアウト、リトライ回数等 |

---

### スキルの実行フロー

#### Step-by-Step実行

```
ステップ 1: ユーザーが指示を入力
│
├─ 【方法A】明示的なスキル指定
│   └─ "スキル: analyze-code-quality で、このコードを分析"
│
├─ 【方法B】自然言語による自動選択 ← Copilot エージェント機能
│   └─ "このコードの品質を分析してください"
│       ↓
│       Copilot が自動的にスキルを選択
│
▼ どちらのケースもこのステップへ
ステップ 1.5: スキルの選択（自動選択時）
│
├─ ["analyze-code-quality", {
│     "code_snippet": "def foo():\n  pass",
│     "language": "python"
│  }]
│
▼
ステップ 2: Copilotがスキル定義ファイルをロード
│
├─ metrics.json内の「analyze-code-quality」を検索
├─ メタデータ、パラメータ定義を読み込む
│
▼
ステップ 3: パラメータの検証
│
├─ ✓ code_snippet が存在、5000文字以内
├─ ✓ language が enum 値のいずれか
├─ ✓ 必須パラメータが全て指定されている
│
▼
ステップ 4: プロンプトテンプレートの展開
│
├─ システムプロンプト：「You are an expert code reviewer...」
├─ テンプレート：「Analyze the following {language} code...」
├─ 変数置換：「Analyze the following python code...」
│
▼
ステップ 5: LLM（Claude等）に送信
│
├─ システムプロンプト + 展開済みテンプレート
├─ リクエスト送信
│
▼
ステップ 6: LLM が応答を生成
│
├─ JSON形式で結果を返却
│
▼
ステップ 7: 出力の検証とフォーマット
│
├─ outputSchema に基づいて検証
├─ 型チェック、必須フィールド等を確認
├─ エラーがあれば再試行またはエラー返却
│
▼
ステップ 8: ユーザーに結果を返却
│
└─ {"readability": {...}, "performance": {...}, ...}
```

---

### メタデータの役割

#### メタデータとは

スキル自体ではなく、**スキルについての情報**

```
スキル定義ファイル
│
├─ [メタデータ] ← スキルについての情報
│  ├─ id
│  ├─ version
│  ├─ name
│  ├─ description
│  ├─ author
│  ├─ tags
│  └─ ...
│
├─ [実装] ← スキル本体
│  ├─ parameters
│  ├─ prompt
│  ├─ outputFormat
│  └─ ...
```

#### メタデータの利用場面

| 場面 | 利用方法 |
|------|---------|
| **検索・ディスカバリー** | `tags: ["python", "quality"]` で検索可能 |
| **バージョン管理** | `version: 1.0.0` でバージョン追跡 |
| **保守性** | `author`, `lastUpdated` で責任者を特定 |
| **分類** | `category: "code-analysis"` でカテゴリ分類 |
| **アクセス制御** | 将来的に `visibility: "private"` 等で制御可能 |

---

### パラメータの定義

#### パラメータの型

```json
{
  "parameters": {
    
    "string_param": {
      "type": "string",
      "description": "テキスト入力",
      "required": true,
      "pattern": "^[a-z]+$",      // 正規表現による制約
      "minLength": 1,
      "maxLength": 100
    },
    
    "number_param": {
      "type": "number",
      "description": "数値入力",
      "minimum": 0,
      "maximum": 100
    },
    
    "boolean_param": {
      "type": "boolean",
      "description": "真偽値",
      "default": true
    },
    
    "array_param": {
      "type": "array",
      "description": "配列",
      "items": {"type": "string"},
      "minItems": 1,
      "maxItems": 10
    },
    
    "enum_param": {
      "type": "string",
      "description": "選択肢（複数値から1つ選択）",
      "enum": ["option1", "option2", "option3"]
    }
  }
}
```

#### パラメータの検証例

```
入力パラメータ：
{
  "code_snippet": "def foo():\n  x = 1\n  return x",
  "language": "python",
  "focusAreas": ["readability", "security"]
}

検証ルール：
✓ code_snippet: string型、5000文字以内 → OK
✓ language: enum ["python", ...] → OK
✓ focusAreas: enum要素の配列 → OK

全て合格！ → 次のステップへ
```

---

### プロンプトテンプレート

#### テンプレートの変数置換

```json
{
  "prompt": {
    "template": "Analyze the following {language} code for {focusAreas}:\n\n{code_snippet}"
  }
}
```

**実行時に以下のように展開される：**

```
入力：
{
  "code_snippet": "def foo():\n  pass",
  "language": "python",
  "focusAreas": ["readability", "performance"]
}

展開後：
"Analyze the following python code for readability, performance:\n\nde
f foo():\n  pass"

↓ LLMに送信
```

#### 複雑なテンプレート例

```json
{
  "prompt": {
    "template": "You are analyzing {language} code.\n\nContext: {context}\n\nFocus areas: {focusAreas|join(', ')}\n\nCode:\n{code_snippet|escape}\n\nProvide analysis in JSON format."
  }
}
```

**テンプレート関数（オプション）：**
- `|join(', ')` - 配列を指定の区切り文字で連結
- `|escape` - 特殊文字をエスケープ
- `|uppercase` - 大文字化
- など

---

### 出力形式の定義

#### スキーマベースの出力検証

```json
{
  "outputFormat": {
    "type": "json",
    "schema": {
      "title": "CodeQualityAnalysis",
      "type": "object",
      "properties": {
        "readability": {
          "type": "object",
          "properties": {
            "score": {"type": "number", "minimum": 0, "maximum": 100},
            "issues": {"type": "array", "items": {"type": "string"}}
          },
          "required": ["score", "issues"]
        },
        "overallScore": {"type": "number"}
      },
      "required": ["readability", "overallScore"]
    }
  }
}
```

**LLMから返却されたJSONが、このスキーマに適合しているかを検証。**

不適合の場合：
- 再試行を実行
- または詳細なエラーをユーザーに返却

---

### Copilotとの相互作用

#### Copilot API との連携

```
Copilot Client
     │
     ├─► JSON-RPC over WebSocket
     │
Copilot Server
     │
     ├─► スキルマネージャー
     │   ├─► スキルの登録・更新・削除
     │   ├─► スキルメタデータの検索
     │   └─► スキルのバージョン管理
     │
     ├─► スキル実行エンジン
     │   ├─► パラメータ検証
     │   ├─► プロンプト展開
     │   └─► LLM呼び出し
     │
     └─► 出力プロセッサー
         ├─► 出力検証
         ├─► フォーマット変換
         └─► キャッシング
```

#### スキル実行時のデータフロー

```
User Input
   ↓
┌──────────────────────────────────┐
│ Copilot Client                     │
│ (IDE extension, GitHub Copilot)   │
└─────────────────┬──────────────────┘
                  │
    リクエスト：{"skill": "analyze-code-quality", "params": {...}}
                  │
                  ▼
┌──────────────────────────────────┐
│ Copilot Server                     │
│ 1. スキルローダー                 │
│ 2. 検証エンジン                    │
│ 3. プロンプト生成                 │
└─────────────────┬──────────────────┘
                  │
    プロンプト：「Analyze the following python code...」
                  │
                  ▼
┌──────────────────────────────────┐
│ LLM (Claude / GPT-4 等)           │
│ - テキスト生成                     │
└─────────────────┬──────────────────┘
                  │
    応答：{"readability": {...}, ...}
                  │
                  ▼
┌──────────────────────────────────┐
│ Copilot Server                     │
│ - 出力検証                        │
│ - フォーマット変換                │
└─────────────────┬──────────────────┘
                  │
    結果：検証済みの構造化データ
                  │
                  ▼
┌──────────────────────────────────┐
│ Copilot Client                     │
│ (ユーザーに表示)                  │
└──────────────────────────────────┘
```

---

### スキルのキャッシング メカニズム

#### キャッシュが有効な場合

```
同じパラメータでスキルを2回連続実行

実行 1回目：
  パラメータ検証 → プロンプト生成 → LLM呼び出し → キャッシュ保存

実行 2回目：
  パラメータ検証 → キャッシュ命中！ → LLM呼び出しをスキップ
  
  ※ 結果は即座に返却（高速化）
```

#### キャッシュキーの生成

```json
キャッシュキー = MD5(skill_id + version + parameters_json)

例：
{
  "skill_id": "analyze-code-quality",
  "version": "1.0.0",
  "parameters": {
    "code_snippet": "def foo():\n  pass",
    "language": "python"
  }
}

↓

キャッシュキー: "a3f5b2c9e7d1..."
```

**キャッシュは有効期限付き**（例：1日、または無期限）

---

### スキルの自動選択メカニズム

#### 自動選択とは

ユーザーが **スキル名を明示しなくても**、Copilot エージェントが自動的に最適なスキルを選択・実行する機能。

```
【明示的指定】
User: "analyze-code-quality スキルでこのコードを分析"
  ↓ ユーザーが指定
  → analyze-code-quality が実行

【自動選択】
User: "このコードの品質を分析してください"
  ↓ Copilot が候補スキルから選択
  → analyze-code-quality が実行（ユーザーは指定しない）
```

#### 自動選択アルゴリズム

```
ユーザー入力：「このコード分析して」

↓ Step 1: ユーザー意図の抽出

Intent: "code_analysis"
Parameters: { code: ..., context: "code quality" }

↓ Step 2: スキル候補の検索

すべてのスキルメタデータを検索：
├─ analyze-code-quality  ← description: "コードの品質を分析"
├─ generate-documentation
├─ generate-unit-tests
└─ ... その他のスキル

↓ Step 3: 最適スキルのマッチング

スコアリング：
├─ analyze-code-quality  : 95点 ← 「品質」「分析」がヒット
├─ generate-unit-tests   : 30点 ← その他のスキル
└─ generate-documentation: 20点

↓ Step 4: 最高スコアスキルを実行

analyze-code-quality が選定 → 実行！

↓ Result: 結果返却
```

#### スキルメタデータの活用

各スキルの **description** と **tags** が自動選択の鍵：

```json
{
  "id": "analyze-code-quality",
  "name": "コード品質分析",
  "description": "Python, JavaScript, TypeScript, Java, Go のコードの品質を多次元的に分析し、改善提案を提供するスキル",
  
  "metadata": {
    "category": "code-analysis",
    "tags": [
      "python", "javascript", "typescript", "java", "go",
      "code-quality",
      "code-review",
      "team-productivity"
    ]
  }
}
```

**ユーザー入力をこれらと照合：**

| ユーザー入力 | マッチタグ | 結果 |
|-----------|----------|------|
| 「コード品質」 | "code-quality" ✓ | analyze-code-quality 選定 |
| 「レビュー」 | "code-review" ✓ | analyze-code-quality 選定 |
| 「テスト生成」 | "unit-test" ✓ | generate-unit-tests 選定 |
| 「ドキュメント」 | "documentation" ✓ | generate-documentation 選定 |

#### マッチング戦略

##### 戦略1: キーワード マッチング（シンプル）

```
ユーザー入力：「このコードの品質を分析してください」

キーワード抽出：「品質」「分析」「コード」

スキルのtags/description から検索：
├─ "品質" → "code-quality" ✓
├─ "分析" → "code-analysis" ✓
└─ "コード" → 多くのスキルに該当

最高スコア: analyze-code-quality
```

##### 戦略2: セマンティック マッチング（高度）

```
ユーザー入力をEmbedding化：
  「このコードの品質を分析してください」
  → [0.23, 0.87, 0.45, ..., 0.92]

各スキルのdescription をEmbedding化：
  
  analyze-code-quality:
    「コードの品質を多次元的に分析し、改善提案を提供」
    → [0.22, 0.89, 0.43, ..., 0.94]  ← 類似度 97% ✓✓
  
  generate-unit-tests:
    「テストコードを自動生成」
    → [0.12, 0.34, 0.11, ..., 0.28]  ← 類似度 22%

最高スコア: analyze-code-quality
```

#### 自動選択の利点・課題

##### 利点

| 利点 | 効果 |
|------|------|
| **UX向上** | ユーザーがスキル名を覚える必要がない |
| **生産性向上** | 入力が短く済む |
| **一貫性** | 同じ意図には常に同じスキルが選ばれる |

##### 課題と対策

| 課題 | 対策 |
|------|------|
| **誤選択** | ユーザー提示時に「このスキルを使います」と確認 |
| **複数候補同点** | ユーザーに選択肢を提示 |
| **言語の揺らぎ** | セマンティック検索 + フォールバック |

#### 実装例（疑似コード）

```python
def auto_select_skill(user_input: str) -> Skill:
    """ユーザー入力から最適なスキルを自動選択"""
    
    # Step 1: 意図抽出
    intent = extract_intent(user_input)
    
    # Step 2: スキル候補を検索
    all_skills = load_all_skills()
    
    # Step 3: マッチングスコアを計算
    scores = {}
    for skill in all_skills:
        # キーワードマッチング
        keyword_score = calculate_keyword_match(
            user_input, 
            skill.description, 
            skill.tags
        )
        # セマンティックマッチング
        semantic_score = calculate_semantic_similarity(
            user_input,
            skill.description
        )
        
        # 総合スコア
        scores[skill.id] = (
            0.3 * keyword_score + 
            0.7 * semantic_score
        )
    
    # Step 4: 最高スコアスキルを返す
    best_skill_id = max(scores, key=scores.get)
    best_score = scores[best_skill_id]
    
    # Step 5: 信頼度チェック
    if best_score < 0.6:  # 閾値以下なら確認を取る
        return prompt_user_selection(scores)
    
    return load_skill(best_skill_id)


# 使用例
user_input = "このコードの品質を分析してください"
skill = auto_select_skill(user_input)
print(f"Selected: {skill.name}")  # → "Selected: コード品質分析"
```

#### 複数スキルの組み合わせ

```
ユーザー入力：「コードを分析して、テストを生成して、ドキュメント書いて」

自動選択結果：
├─ Step 1: analyze-code-quality で分析
├─ Step 2: generate-unit-tests でテスト生成
└─ Step 3: generate-documentation でドキュメント生成

このような "複合スキル" 実行可能
（Part 5-1 参照: 複合スキルの詳細）
```

---

### エラーハンドリング


#### エラーリトライ メカニズム

```
スキル実行
  │
  ├─► Attempt 1
  │   ├─ LLM に送信
  │   └─ タイムアウト／エラー発生
  │       │
  │       └─ リトライ回数 < 最大？
  │           └─ Yes → Attempt 2
  │               
  ├─► Attempt 2
  │   ├─ LLM に再送信
  │   └─ 成功 / エラー継続
  │       │
  │       └─ 成功？Yes → 結果返却
  │           No → Attempt 3
  │
  └─► Attempt 3 が失敗
      └─ ユーザーにエラーを返却
```

#### エラー応答例

```json
{
  "success": false,
  "error": {
    "code": "LLM_TIMEOUT",
    "message": "Language model response timed out",
    "details": "The skill execution exceeded 30 seconds",
    "attempts": 3,
    "recommendation": "Try again with simpler input"
  }
}
```

---

### 次へ進む

→ [Part 2: 比較分析編](#section-02-comparison-01-vs-mcp) - MCPとの違いを詳しく学ぶ

# Comparison {#chapter-02-comparison}

## Part 2-0: 4つのLLM拡張方法の統一解説 {#section-02-comparison-00-four-concepts}


### はじめに

LLM（ChatGPT、Claude）の能力を拡張する方法は、大きく4つのカテゴリーに分けられます。

- **Prompt（プロンプト）**
- **Custom Instructions（カスタム指示）**
- **Skill（スキル）**
- **MCP（Model Context Protocol）**

このセクションでは、これら4つを **メリット・デメリット・活用パターン** の観点から比較し、どれを選ぶべきかを判断するためのフレームワークを提供します。

---

### 1. 4つの概念の定義

#### 1-1. Prompt（プロンプト）

**定義：** LLMに対する **単発の指示書**

```
構成：
┌──────────────────────┐
│ Prompt               │
├──────────────────────┤
│ Context（背景情報）  │
│ Task（タスク）       │
│ Format（形式指定）   │
│ Examples（例）       │
└──────────────────────┘
```

**特徴：**
- 一度使う、または単発の処理
- テキスト形式（通常は数百～数千トークン）
- カスタマイズが自由
- チャット/API での直接入力

**具体例：**
```
「以下の記事を3文で要約してください：
[記事本文]

出力形式は JSON で、以下のスキーマに従ってください：
{
  "title": "要約タイトル",
  "summary": "3文の要約",
  "keywords": ["キーワード"]
}」
```

---

#### 1-2. Custom Instructions（カスタム指示）

**定義：** 特定のLLMツール（例：ChatGPT、Claude）に **永続的に保存される プロンプトテンプレート**

```
構成：
┌──────────────────────────────┐
│ Custom Instructions          │
├──────────────────────────────┤
│ スコープ：特定のツール内     │
│ 寿命：永続（削除まで）       │
│ 適用：すべての会話に自動適用 │
│ パラメータ化：可能           │
└──────────────────────────────┘
```

**特徴：**
- 一度設定すれば、その後のすべての会話に適用
- ツール内に保存（ChatGPT設定、Claude設定等）
- テンプレート化が可能（変数埋め込み）
- 個人またはチーム単位で設定

**具体例：**

```
[ChatGPT の Custom Instructions 設定例]

「About you」セクション：
「あなたはシニアソフトウェアエンジニアです。15年の経験を持ち、
Pythonと TypeScript に精通しています。」

「How you should respond」セクション：
「1. すべての回答は JSON 形式で返してください
2. セキュリティ上の懸念があれば必ず言及してください
3. ベストプラクティスの参考ファイルを提示してください」
```

---

#### 1-3. Skill（スキル）

**定義：** GitHub Copilot に登録する **再利用可能な手順書（Agent Skill）**

```
構成：
┌─────────────────────────────┐
│ Skill（Agent Skill）        │
├─────────────────────────────┤
│ 定義：JSON/YAMLファイル      │
│ スコープ：GitHub Copilot専用 │
│ 寿命：リポジトリで管理      │
│ リユース：何度でも実行      │
│ version管理：Git で追跡      │
└─────────────────────────────┘
```

**特徴：**
- GitHub Copilot に統合
- 構造化されたファイル形式（JSON/YAML）
- パラメータ、出力スキーマを定義
- チーム全体で共有・バージョン管理
- 実行するたびに統一した結果を得る

**具体例：**

```json
{
  "id": "code-review",
  "name": "コードレビュー",
  "description": "コードの品質をチェック",
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "レビュー対象のコード"
    },
    "language": {
      "type": "string",
      "enum": ["python", "typescript", "java"],
      "description": "プログラミング言語"
    }
  },
  "prompt": {
    "instruction": "以下のコードを {language} のベストプラクティスに基づいてレビューしてください",
    "content": "{code_snippet}"
  },
  "outputFormat": {
    "type": "json",
    "schema": {
      "issues": ["配列"],
      "score": "0-100の数値",
      "recommendations": ["配列"]
    }
  }
}
```

---

#### 1-4. MCP（Model Context Protocol）

**定義：** LLMが **外部ツール・データへ安全にアクセス** するためのプロトコルと実装

```
構成：
┌──────────────────────────────────┐
│ MCP（Model Context Protocol）    │
├──────────────────────────────────┤
│ 定義：専用サーバー実装            │
│ スコープ：複数のLLMに対応        │
│ リソース接続：外部ツール・API    │
│ セキュリティ：権限管理・認証      │
│ 複雑度：高い                     │
└──────────────────────────────────┘
```

**特徴：**
- Claude、GPT-4など複数のLLMで使用可
- 外部API、データベース、クラウドサービスへのアクセス
- セキュリティ・権限管理が組み込まれている
- サーバーの実装が必要（Node.js等）
- リアルタイムデータの取得が可能

**具体例：**

```javascript
// MCP Server の例：Database へのアクセスを提供

const server = new Server({
  name: "database-server",
  version: "1.0.0",
});

server.setRequestHandler(ExecuteCommand, async (request) => {
  // LLMから「user テーブルをクエリ」リクエストが来た
  const result = await db.query(request.command);
  return { contents: [{ type: "text", text: JSON.stringify(result) }] };
});
```

LLMはこのサーバーを通じて、安全に Database にアクセス可能に。

---

### 2. 4つの概念を4象限で可視化

```
                高い
           複雑度
              ▲
              │
         ┌────┼────┐
         │    │    │
         │ MCP│Skill│
    セットアップ │    │    │
    費用大  │    │    │
         └────┼────┘
              │
              │
    ─────────┼────────→ スコープ（チーム内 ← → 多言語汎用）
              │
         ┌────┼────┐
         │    │    │
         │Prompt│Custom│
         │      │ Instr│
    セットアップ │      │    │
    費用小  └────┴────┘
              低い
           複雑度
```

#### 象限別の特徴

| 象限 | 技術 | 特徴 | セットアップ | 推奨シーン |
|------|------|------|----------|---------|
| **左下** | Prompt | 最小限、使い捨て | 5分 | 単発タスク、プロト |
| **右下** | Custom Instr | パーソナライズ、永続 | 30分 | 個人向け設定 |
| **左上** | Skill | チーム共有、手順化 | 1-2時間 | チーム内の繰り返し |
| **右上** | MCP | 汎用、外部統合 | 1-2日 | システム連携 |

---

### 3. メリット・デメリット一覧表

#### 簡潔版

| 項目 | Prompt | Custom Instr | Skill | MCP |
|------|--------|-----------|-------|-----|
| **セットアップ時間** | 5分 | 30分 | 1-2時間 | 8-16時間 |
| **学習曲線** | 即習得 | 30分 | 2-4時間 | 1-2日 |
| **再利用性** | 低 | 中 | 高 | 非常に高 |
| **チーム共有** | △困難 | △中程度 | ✓容易 | ✓容易 |
| **外部ツール連携** | ×不可 | △限定的 | △限定的 | ✓可能 |
| **複数LLM対応** | ✓可能 | ×1つのツールのみ | ×Copilot専用 | ✓可能 |
| **インフラ・運用コスト** | 最小限 | 最小限 | 最小限 | 中程度 |
| **推奨スケール** | 1-3個 | 5-10個 | 10-100個+ | 複雑な統合 |

※ インフラ・運用コストは LLM API 使用料を除いた「専用サーバー、保守、人員」等のコスト

---

### 4. 活用パターン（早見表）

#### 「あなたはどれを選ぶべき？」フローチャート

```
Q1: これは何度も繰り返すタスクか？
  │
  ├─ No → Prompt で十分
  │
  └─ Yes → Q2へ
       │
       Q2: チーム内で共有したいか？
         │
         ├─ No → Custom Instructions で OK
         │
         └─ Yes → Q3へ
              │
              Q3: 外部ツール（DB、API等）へのアクセスが必須か？
                │
                ├─ No → Skill で OK
                │
                └─ Yes → MCP を検討
```

#### 実践パターン集

| パターン | 該当技術 | 理由 |
|---------|--------|------|
| 一度きりの記事要約 | **Prompt** | セットアップが最小限 |
| 毎日の個人作業環境設定 | **Custom Instr** | 個人向け、永続保存 |
| チーム全体でのコードレビュー統一化 | **Skill** | チーム共有、バージョン管理 |
| Slack通知 + DB クエリ + ドキュメント生成 | **Skill + MCP** | 複数システムの統合 |
| 複数のLLM（ChatGPT/Claude）で同じワークフロー | **MCP** | LLM非依存の統合 |

---

### 5. 組み合わせ活用（重要）

実務では、これら4つを **組み合わせて使うことが最適** です。

#### 例：企業のドキュメント自動生成システム

```
レイヤー1: ユーザーインタフェース
  │
  ├─ Prompt
  │ 「生成するドキュメントの種類を選択」
  │ （テンプレート的なプロンプト）
  │
レイヤー2: 個人設定
  │
  ├─ Custom Instructions
  │ 「社内スタイルガイド、個人の執筆スタイル」
  │ （ChatGPT の Custom Instr で永続設定）
  │
レイヤー3: チーム標準化
  │
  ├─ Skill
  │ 「doc-generator スキル」
  │ （GitHub Copilot で、すべてのメンバーが統一フォーマット）
  │
レイヤー4: 外部連携
  │
  └─ MCP
    「社内ナレッジベースから検索」
    「Slack に通知」
    「Google Docs に自動保存」
```

---

### 6. 選択基準サマリー

#### ステップバイステップの判断

| ステップ | 質問 | 結論 |
|---------|------|------|
| 1 | 一度きりのタスク？ | → **Prompt** で完全に十分 |
| 2 | 何度も使うが、個人用？ | → **Custom Instructions** で設定 |
| 3 | チーム内で統一したい？ | → **Skill** を作成・共有 |
| 4 | 外部ツール連携が必須？ | → **MCP** サーバーを実装 |
| 5 | 複数言語・複数LLM？ | → **MCP** で実装（汎用性） |
| N | 1つでは不足？ | → **複数を組み合わせ** |

---

### 7. 次のステップ

- **詳細比較** → [Part 2-1: MCP との違い](#section-02-comparison-01-vs-mcp)
- **その他ツール比較** → [Part 2-2: その他の関連技術との比較](#section-02-comparison-02-vs-other-tools)
- **メリット・デメリット** → [Part 2-3: 詳細比較表](#section-02-comparison-03-pros-cons)
- **実践ケース** → [Part 2-4: 応用ケース](#section-02-comparison-04-use-cases)

## Part 2-1: MCP（Model Context Protocol）との違い {#section-02-comparison-01-vs-mcp}


### はじめに

GitHub Copilot Agent Skills と MCP（Model Context Protocol）はどちらも **LLMの能力を拡張する技術** ですが、目的と設計哲学が異なります。

このセクションでは、両者の違いを詳しく解説し、どのような場面で何を選ぶべきかを判断するためのフレームワークを提供します。

---

### 簡潔な違い

| 項目 | Agent Skills | MCP |
|------|-------------|-----|
| **何をするか** | LLMに **手順書（スキル）** を教え込む | LLM が **外部ツール・データ** に安全にアクセス |
| **対象** | Copilot（GitHub）専用 | 複数のLLM（Claude, GPT-4等）対応 |
| **使用場面** | 繰り返し使う作業の効率化 | 外部システム統合 |
| **実装場所** | Copilot 内蔵 | 専用サーバー（MCP Server） |
| **学習コスト** | 中程度 | 高め |
| **複雑度** | 単純 | 複雑 |

---

### 詳細比較

#### 1. 目的の違い

##### Agent Skills

```
目的：
  LLMに「このタスクは必ず、この方法で」と手順書を教える

例：
  「コード品質分析は、必ず
   1. 可読性チェック
   2. パフォーマンス分析
   3. セキュリティスキャン
   この3点セットで実行する」

  → チーム全体で統一された品質基準を保つ
```

##### MCP

```
目的：
  LLMに「これらの外部ツールを使うことができる」
  という権限・方法を与える

例：
  「Database に SQL クエリを実行する権限」
  「File System に読み書きする権限」
  「HTTP API を呼び出す権限」

  → LLM が外部システムと安全に連携
```

#### 2. アーキテクチャの違い

##### Agent Skills アーキテクチャ

```
┌───────────────────────────────────┐
│ Copilot Client                     │
│ (VS Code Extension等)              │
└────────────┬──────────────────────┘
             │
    リクエスト
             │
             ▼
┌───────────────────────────────────┐
│ Copilot Server                     │
│ （Skillsエンジン組み込み）         │
│                                    │
│ ┌──────────────────────────────┐  │
│ │ スキル定義ファイル           │  │
│ │ (JSON/YAML)                  │  │
│ └──────────────────────────────┘  │
│                                    │
│ ┌──────────────────────────────┐  │
│ │ プロンプト加工エンジン       │  │
│ │ + パラメータ処理             │  │
│ └──────────────────────────────┘  │
└────────────┬──────────────────────┘
             │
    加工済みプロンプト
             │
             ▼
┌───────────────────────────────────┐
│ LLM (Claude等)                     │
└───────────────────────────────────┘

特徴：
- Copilot に統合
- スキルは内蔵メカニズム
- 外部との連携は限定的
```

##### MCP アーキテクチャ

```
┌───────────────────────────────────┐
│ LLM Client                         │
│ (Claude Desktop等)                 │
└────────────┬──────────────────────┘
             │
    JSON-RPC通信
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ MCP Server 1 │  │ MCP Server 2 │
│   (Database) │  │  (File FS)   │
└──────────────┘  └──────────────┘
    │                 │
    └────────┬────────┘
             │
    各 MCP サーバーが外部ツール・データを提供

特徴：
- LLM Client と MCP Server は分離
- 複数の MCP Server を組み合わせ可能
- 標準プロトコルで相互運用
```

#### 3. データフロー の違い

##### Agent Skills のデータフロー

```
ユーザー入力（スキル名 + パラメータ）
   ↓
Copilot Server がスキル定義を検索
   ↓
パラメータを仕様に従って検証
   ↓
プロンプトテンプレートに変数を代入
   ↓
LLM に送信
   ↓
応答を出力スキーマで検証
   ↓
ユーザーに返却

（注）すべてが Copilot 内で完結
```

##### MCP のデータフロー

```
ユーザー（またはLLM）からのリクエスト
   ↓
MCP Client が Tool/Resource を解決
   ↓
該当する MCP Server にリクエスト転送
   ↓
MCP Server が外部システムをコール
   ↓
結果を返却
   ↓
LLM に結果を提供
   ↓
LLM が結果に基づいて判断・応答

（注）複数のシステム間で連携
```

#### 4. 拡張性の違い

##### Agent Skills

```
拡張できること：
✓ スキル定義の追加
✓ スキル定義の修正
✓ スキルのチェーン実行

拡張できないこと：
✗ 外部ツールの直接統合
✗ LLM 以外への連携
✗ 複雑なロジック処理
```

##### MCP

```
拡張できること：
✓ 新しい MCP Server の実装
✓ 任意の外部ツール・データソースの統合
✓ 複雑なビジネスロジック処理
✓ リアルタイムデータの提供
✓ ストリーミングレスポンス

拡張できないこと：
✗ LLM の振る舞いそのものを変更（それ以上は LLM の学習）
```

---

### 使用シーンの比較

#### シーン1: チーム内のコーディング規約チェック

##### Agent Skills の場合（最適）

```
要件：
- チーム全体で統一された規約をチェック
- 規約が変わったら全員に自動反映
- LLM の出力を一貫させたい

実装：
「code-style-checker」スキル
  ├─ 入力：コード
  └─ 出力：規約違反リスト（固定フォーマット）

メリット：
✓ すべてのチームメンバーが同じロジックを適用
✓ 一度スキル化すると改善が自動反映
✓ 出力フォーマットが統一される
```

##### MCP の場合（オーバースペック）

```
可能だが必要ない。MCP はむしろ以下の場合に有用：

「コーディング規約チェック + 社内 Wiki との連携」
  MCP Server 1: コード規約チェッカー
  MCP Server 2: 社内 Wiki API
  └─ LLM が Wiki から最新の規約を取得しながらチェック

この場合、MCP の複合性が活きる
```

---

#### シーン2: リアルタイムデータベースクエリ

##### Agent Skills の場合（不向き）

```
問題：
- Agent Skills は LLM へのプロンプト加工が中心
- 実際の DB アクセスは直接できない

無理やり実装すれば：
「query-database」スキル
  ├─ DB 接続情報を秘密にする複雑さ
  ├─ 動的な SQL 生成の安全性確保
  ├─ リアルタイム結果の検証
  └─ 困難・セキュリティリスク高

結論：Not Recommended
```

##### MCP の場合（最適）

```
実装：
MCP Server: Database Connector
  ├─ セキュアな認証
  ├─ SQL インジェクション対策
  ├─ クエリ実行
  └─ 結果を構造化して返却

LLM が MCP Server 経由でクエリ実行
  └─ LLM は安全に DB にアクセス

メリット：
✓ セキュリティ確保
✓ リアルタイム環境変数を活用可能
✓ 複雑なビジネスロジックを実装可能
```

---

#### シーン3: 会社固有の分析フロー（分析→改善提案→テスト生成）

##### Agent Skills の場合（最適）

```
スキル1: 「code-analysis」
  入力：コード → 出力：分析結果（JSON）

スキル2: 「improvement-suggestion」
  入力：分析結果 → 出力：改善提案（JSON）

スキル3: 「test-generation」
  入力：改善提案 → 出力：テストコード

これらをチェーン実行：
  code-analysis → improvement-suggestion → test-generation

メリット：
✓ 3つのステップが一つの定義で管理される
✓ チーム全体で同じフロー
✓ 各ステップの出力フォーマットが一貫
```

##### MCP の場合（過度に複雑）

```
可能だが、複雑すぎる

MCP は「外部システムへのアクセス」が主目的
3つの分析ステップは全て LLM の能力の範囲で、
外部ツールアクセスが不要なため、
MCP を利用するメリットが薄い

むしろ Agent Skills で十分
```

---

#### シーン4: 複数の外部サービス統合（AI + DB + API）

##### Agent Skills の場合（限界あり）

```
複数の外部サービス統合は難しい

スキル内で複数の外部サービスをコール
  → セキュリティ、認証、エラーハンドリング の複雑さが増す

理論的には可能だが、ベストプラクティスではない
```

##### MCP の場合（最適）

```
複数の MCP Server を組み合わせ

MCP Server 1: Slack Integration
  └─ Slack API へのセキュアなアクセス

MCP Server 2: Database
  └─ DB へのセキュアなアクセス

MCP Server 3: External API
  └─ Third-party API へのセキュアなアクセス

LLM がこれらを組み合わせて実行
  └─ 複雑なワークフドル自動化

メリット：
✓ 各サービス統合のセキュリティが個別に保証
✓ スケーラブルな設計
✓ 複雑なロジック処理が可能
```

---

### 比較表: 決定フローチャート

#### どちらを選ぶ？

```
質問1: 複数の外部システム (DB, API) を統合したい？
│
├─ Yes → 質問3へ
├─ No  → 質問2へ

質問2: チーム内で統一された作業フローを保ちたい？
│
├─ Yes → 質問3へ
├─ No  → 質問4へ

質問3: リアルタイム環境データ（最新レート、ユーザー情報等）が必要？
│
├─ Yes → ★ MCP を選ぶ
├─ No  → Agent Skills OR MCP（どちらでも可）

質問4: 複雑なビジネスロジック処理が必要？
│
├─ Yes → ★ MCP を選ぶ
├─ No  → ★ Agent Skills を選ぶ
```

---

### メリット・デメリット比較

#### Agent Skills

| メリット | デメリット |
|---------|----------|
| セットアップが簡単 | Copilot 専用 |
| GitHub ネイティブ統合 | 外部ツールアクセスが限定的 |
| チーム管理がシンプル | 複雑なロジックに不向き |
| 出力フォーマットが統一可能 | リアルタイムデータ取得が困難 |
| バージョン管理が容易 | スケーラビリティに限界 |

#### MCP

| メリット | デメリット |
|---------|----------|
| 複数の LLM で利用可能 | セットアップが複雑 |
| 複雑なロジック実装可能 | MCP Server を構築・運用する必要 |
| 外部ツール統合が自由 | セキュリティ設定が複雑 |
| リアルタイムデータ連携可能 | デバッグが難しい |
| エンタープライズ対応 | コストが高い場合がある |

---

### 将来の発展

#### Agent Skills の発展方向

```
短期（2026年）：
- Copilot の機能強化
- SKill マーケットプレイスの充実

中期（2027年以降）：
- 他の IDE への対応検討？
- MCP との統合？
```

#### MCP の発展方向

```
既に確定：
- Claude Desktop 対応
- 複数の LLM サポート拡大（GPT-4等）

将来の期待：
- セキュリティ・認証の標準化
- パフォーマンス最適化
- より多くのサービス統合
```

---

### 結論

| 選択基準 | 推奨 |
|-------|------|
| **チーム内の統一性が最優先** | **Agent Skills** |
| **単純な繰り返しタスク** | **Agent Skills** |
| **Copilot のみで完結したい** | **Agent Skills** |
| **複数の外部システムを連携** | **MCP** |
| **複雑なビジネスロジック** | **MCP** |
| **リアルタイムデータ必須** | **MCP** |
| **セキュアな認証・エラーハンドリング** | **MCP** |
| **複数の LLM を使いたい** | **MCP** |

---

### 次へ進む

→ [Part 2-2: その他の関連技術との比較](#section-02-comparison-02-vs-other-tools)

## Part 2-2: その他の関連技術との比較 {#section-02-comparison-02-vs-other-tools}


### 概要

AI/LLM 関連技術には多くの選択肢があります。Agent Skills と同じく LLM の能力を拡張する他の技術との違いを理解しましょう。

> **💡 事前知識:** まずは [Part 2-0: 4つのLLM拡張方法の統一解説](#section-02-comparison-00-four-concepts) で、Prompt・Custom Instructions・Skill・MCP の概念フレームワークを理解することを推奨します。

---

### 技術比較表

| 技術 | 目的 | 実装難度 | セットアップ時間 | インフラ・運用コスト | 推奨シーン |
|------|------|--------|----------|---------------|----------|
| **Prompt** | 単発の指示書 | ほぼ 0 | 5分 | 最小限 | 一度きりのタスク |
| **Custom Instructions** | 個人向け永続設定 | 低い | 30分 | 最小限 | 個人の作業環境 |
| **Agent Skills** | 再利用可能な手順書 | 低い | 1-2時間 | 最小限 | チーム内統一 |
| **プロンプトチェーニング** | 複数ステップの処理 | 低い | 30分 | 低い | 単発の複雑タスク |
| **RAG** | 外部ナレッジの統合 | 中程度 | 4-8時間 | 中程度 | ドキュメント検索・QA |
| **ファインチューニング** | モデルの学習 | 高い | 1-2日 | 高い | 専門分野の最適化 |
| **MCP** | 外部システム安全連携 | 高い | 8-16時間 | 中程度 | エンタープライズ統合 |

**注釈:** インフラ・運用コストは LLM API 使用料を除いた「専用サーバー、保守、人員」等のコスト

---

### 1. Prompt（プロンプト）

#### 概要

**Prompt** は、LLMへの **単発の指示書** です。最もシンプルな拡張方法です。

```
使用例：
「以下のテキストを3文で要約してください：
[テキスト]

出力形式：JSON」
```

#### Skill との比較

| 項目 | Prompt | Skill |
|------|--------|-------|
| **再利用性** | 低（毎回新規作成） | 高（登録すればいつでも使用） |
| **チーム共有** | △困難（コピペで共有） | ✓容易（Git管理） |
| **セットアップ** | ほぼ即座 | 1-2時間 |
| **統一性** | ばらばら | 統一される |
| **バージョン管理** | 不可 | Git で自動追跡 |

#### 使い分け

```
Prompt を選ぶべき場面：
✓ 一度きりのタスク
✓ 急ぎで対応が必要
✓ プロトタイピング段階
✓ 複雑な指示が必要（単発）

Skill を選ぶべき場面：
✓ 何度も繰り返すタスク
✓ チーム内で共有したい
✓ 結果フォーマットを統一したい
✓ バージョン管理が必要
```

#### 実例

```
Prompt の例：
「Python で Fibonacci 数列を生成する関数を書いてください。
出力形式は JSON Schema で定義してください。」

→ すぐに結果が得られるが、2回目は また同じプロンプトを入力
  （毎回少し異なる結果になる可能性）


Skill の例：
「fibonacci スキル」を登録
→ 何度実行しても統一フォーマット
→ チーム全員がアクセス可能
→ Git で履歴管理
```

---

### 2. Custom Instructions（カスタム指示）

#### 概要

**Custom Instructions** は、特定のLLMツール（ChatGPT、Claude等）に **永続的に保存される設定** です。その後のすべての会話に自動適用されます。

```
設定例（ChatGPT の Custom Instructions）：

「About you」：
「あなたはシニアエンジニアです。セキュリティを重視します。」

「How you should respond」：
「すべての回答を JSON で返してください。
セキュリティリスクあれば必ず言及してください。」

→ 以降、全てのチャットでこの指示が自動適用
```

#### Skill との比較

| 項目 | Custom Instructions | Skill |
|------|-------------------|-------|
| **スコープ** | 1つのツール内 | GitHub Copilot（複数ツール対応予定） |
| **寿命** | 永続（削除まで） | リポジトリ内で管理 |
| **チーム共有** | △中程度（設定を共有） | ✓容易（Git管理） |
| **自動適用** | ✓すべての会話に適用 | 明示的に選択して実行 |
| **バージョン管理** | △手動で管理 | ✓自動（Git） |
| **複数LLM対応** | ×各ツール個別設定 | ×Copilot 専用 |

#### 使い分け

```
Custom Instructions を選ぶべき場面：
✓ 個人の作業スタイル・ポリシーを固定化したい
✓ すべてのチャットで共通設定を適用したい
✓ 「このツールを使う時は常にこうしてほしい」という設定
✓ 個人またはチーム単位の好みをツールに記憶させたい

Skill を選ぶべき場面：
✓ チーム全体で統一したい（Git 管理）
✓ 複数のバージョンを並行管理したい
✓ 特定のタスクを何度も繰り返す
✓ プロンプトの改善履歴を追跡したい
```

#### 実例

```
Custom Instructions の例：

[ChatGPT に設定]
「About you」：
「日本語を話すシニアエンジニア。
PythonとTypeScriptが得意。セキュリティに厳しい。」

「How you should respond」：
「1. すべてのコード例を JSON Schema で返す
2. セキュリティリスクを必ず言及
3. 参考ドキュメントを提示」

→ 以降、この人がチャットする時は 常にこの指示が適用


Skill の例：

[リポジトリに登録]
「security-code-review」スキル
→ チーム全員が実行可能
→ 統一フォーマットで結果取得
→ スキル改善時は全員が恩恵
```

---

### 3. Agent Skills と Custom Instructions の統合パターン

両者を組み合わせることで、更に強力な体系が実現できます：

```
Layer 1: 個人設定（Custom Instructions）
  └─ 「セキュリティを最優先」
  └─ 「すべてのコードを TypeScript で」
  └─ 「JSON 出力フォーマット統一」

Layer 2: チーム標準（Skill）
  └─ 「code-review スキル」（セキュリティガイドライン含む）
  └─ 「document-generator スキル」（企業テンプレート含む）
  
結果：
✓ 個人のこだわり + チーム標準 が両立
✓ 出力フォーマットが統一される
✓ セキュリティ基準が自動適用される
```

---

### 4. プロンプトチェーニング

#### 概要

複数のプロンプトを順序立てて実行し、途中の結果を次のプロンプトに渡すテクニック

```
プロンプト1
  ↓ 出力
プロンプト2（出力1を入力）
  ↓ 出力
プロンプト3（出力2を入力）
  ↓
最終結果
```

#### 使用例

```
ステップ1: テキスト要約
入力：「長い記事」
出力：「要約」

ステップ2: キーワード抽出
入力：「要約」
出力：「キーワード」

ステップ3: SEO タイトル生成
入力：「キーワード」
出力：「SEO最適なタイトル」
```

#### Agent Skills との比較

| 項目 | Agent Skills | プロンプトチェーニング |
|------|------------|-------------|
| **実装方法** | スキル定義ファイル（JSON） | スクリプト（Python/JS） |
| **再利用性** | ✓ 高い | △ 低い（スクリプト依存） |
| **チーム共有** | ✓ 容易（リポジトリで管理） | △ 困難（環境構築が必要） |
| **統一性** | ✓ 統一される | △ バラバラ |
| **複雑性** | 低い | 中程度 |
| **学習曲線** | 急 | ゆるい |

#### 使い分け

```
プロンプトチェーニングを選ぶべき場面：
✓ 一度のみの複雑なタスク
✓ プロトタイピング段階
✓ 快速試行錯誤を重視

Agent Skills を選ぶべき場面：
✓ チーム内で何度も繰り返すワークフロー
✓ ワークフローの改善を頻繁にしたい
✓ チーム全体で統一したい
```

---

### 5. RAG (Retrieval Augmented Generation)

#### 概要

LLM に追加の知識（ドキュメント、データベース）を検索・提供することで、より正確な応答を生成する手法

```
ユーザー質問
   ↓
知識ベースから関連情報を検索
   ↓
LLM に「質問 + 関連情報」を渡す
   ↓
より正確な応答を生成
```

#### 使用例

```
例：社内ナレッジ QA システム

ユーザー：「弊社にはどんな福利厚生がありますか？」

システム：
1. 社内 Wiki から福利厚生のドキュメントを検索
2. LLM に「質問」と「検索結果」を渡す
3. LLM が検索結果に基づいて回答を生成

結果：「弊社の福利厚生は...」（正確な情報に基づく）
```

#### Agent Skills との比較

| 項目 | Agent Skills | RAG |
|------|------------|-----|
| **目的** | 手順書の統一 | 知識ベースの活用 |
| **外部データ連携** | △ 限定的 | ✓ 主要機能 |
| **実装難度** | 低い | 中程度 |
| **セットアップ時間** | 1-2時間 | 4-8時間 |
| **運用コスト** | 低い | 中程度 |

#### 組み合わせの例

```
最強の組み合わせ：Agent Skills + RAG

スキル定義：「social-benefit-qa」
  ├─ 質問の受け取り
  └─ RAG で社内 Wiki から関連情報を検索
     └─ 検索結果を含めて LLM に質問

メリット：
✓ チーム全体で同じ知識源を参照
✓ 回答フォーマットが統一
✓ 知識ベースの更新が自動反映
```

---

### 6. ファインチューニング

#### 概要

モデルの重みを調整して、特定の分野や タスク に最適化することで、より高精度な応答を得る技術

```
既存モデル
   ↓
大量の専門データで学習
   ↓
微調整されたモデル
   ↓
より精密な応答
```

#### 使用例

```
例：医療診断補助システム

汎用モデル（Claude等）
  └─ 医学論文・診断事例で微調整
      → 医療分野でより高精度な診断補助が可能
```

#### Agent Skills との比較

| 項目 | Agent Skills | ファインチューニング |
|------|------------|----------|
| **目的** | 手順書統一 | モデル最適化 |
| **学習のレベル** | 表層（プロンプト） | 深層（重み調整） |
| **実装難度** | 低い | 非常に高い |
| **セットアップ時間** | 1-2時間 | 1-2週間+ |
| **出力の安定性** | 高い | 中程度 |
| **コスト** | 低い | 高い |
| **汎用性** | 高い | 低い |

#### 使い分け

```
Agent Skills を選ぶべき理由：
✓ 低コスト
✓ セットアップが早い
✓ 変更が容易

ファインチューニングを選ぶべき理由：
✓ 非常に専門的な分野
✓ より高精度が絶対必要
✓ 既存モデルでは対応不可
□ コスト・時間が十分にある
```

#### 組み合わせの例

```
医療診断補助システム：Agent Skills + ファインチューニング

ファインチューニング：医学知識をモデルに組み込む
Agent Skills：「diagnostic-assistance」スキルで統一フロー確保

メリット：
✓ 基盤となるモデルは医学最適化
✓ 診断フロー・出力は全医師で統一
✓ 高精度 + チーム統一性
```

---

### 7. カスタム統合 (Copilot Extensions / API Integration)

#### 概要

Copilot や LLM に新しい機能・ツールを完全にカスタム実装して、直接統合する方法

```
カスタムコード
   │
   ├─ 独自のビジネスロジック
   ├─ 外部システム連携
   └─ 認証・エラーハンドリング
   
Copilot に完全組み込み
   │
   └─ ユーザーに提供
```

#### 使用例

```
例：社内CRM統合

Copilot Extension を開発
  ├─ CRM API へのセキュアアクセス
  ├─ 顧客データ検索
  ├─ 受注入力フォーム
  └─ 営業レポート生成

CRM データに自由にアクセス可能
   └─ LLM が営業支援
```

#### Agent Skills との比較

| 項目 | Agent Skills | カスタム統合 |
|------|------------|---------|
| **自由度** | 中程度 | 非常に高い |
| **実装難度** | 低い | 非常に高い |
| **セットアップ時間** | 1-2時間 | 1-2週間+ |
| **メンテナンス** | 容易 | 複雑 |
| **セキュリティ** | 標準的 | カスタム設定が必要 |
| **スケーラビリティ** | 中程度 | 高い |

#### 使い分け

```
Agent Skills で十分な場合：
✓ チーム内での作業統一
✓ LLM の応答をより良い形式にしたい
✓ 外部システムアクセスが不要

カスタム統合が必要な場合：
✓ 複雑なセキュリティ要件
✓ 複数の外部システムを深く統合
✓ 特殊なビジネスロジック
✓ 大規模エンタープライズ導入
```

---

### 総合比較表

```
              セットアップ  実装難度  再利用性  チーム共有  ランニング  適用範囲
              時間       難度      性        容易性      コスト      広さ
────────────────────────────────────────────────────────────────────────
Agent Skills   ★         ★        ★★★      ★★★       ★          ★★
Prompt Chain   ★★       ★        ★★       ★          ★★         ★★
RAG           ★★★       ★★       ★★       ★★        ★★         ★★
Fine-tuning    ★★★★     ★★★★    ★        ★          ★★★        ★
Custom API     ★★★★     ★★★★    ★★       ★★        ★★★        ★★★

★が多いほど優れている
```

---

### シーン別選択ガイド

#### シーン1: 「社員が毎日使う分析ツール」

```
要件：
- 毎日何度も繰り返す
- チーム全体で統一性が必要
- セキュリティは中程度でよい

推奨：★ Agent Skills

理由：
✓ セットアップが簡単
✓ メンテナンスが容易
✓ チーム全体で統一可能
✓ 改善がすぐに全員に反映
```

#### シーン2: 「複数の複雑なステップを自動化」

```
要件：
- データ抽出 → 分析 → レポート生成
- 複数のシステムが必要
- 高度なセキュリティが必要

推奨：★ RAG + カスタム統合 OR MCP

理由：
✓ 複数データソースの統合が必要
✓ 複雑なロジック処理
✓ セキュリティが重要
```

#### シーン3: 「プロトタイピング」

```
要件：
- 試行錯誤が必要
- 最短時間で試したい
- コストは最小限

推奨：★ プロンプトチェーニング

理由：
✓ セットアップが最速
✓ 修正が簡単
✓ 本格化したら Agent Skills に移行可能
```

#### シーン4: 「医療診断補助（超高精度必須）」

```
要件：
- 最高精度が必須
- 医学知識が重要
- 誤診のリスクを最小化

推奨：★ ファインチューニング + Agent Skills

理由：
✓ ファインチューニング：医学知識をモデルに組み込む
✓ Agent Skills：診断フローを統一
✓ 両者は補完的
```

---

### 決定フローチャート

```
質問1: チーム内での統一性が必要？
│
├─ Yes → 質問2へ
└─ No  → プロンプトチェーニングで十分

質問2: 複数のシステム（DB, API等）を統合？
│
├─ Yes → 質問3へ
└─ No  → Agent Skills で OK

質問3: セキュリティ要件が厳しい？
│
├─ Yes → カスタム統合 OR MCP
└─ No  → RAG でも可

質問4: 専門分野の超高精度が必須？
│
├─ Yes → ファインチューニング + Agent Skills
└─ No  → Agent Skills のみで OK
```

---

### まとめ

|  | Agent Skills | 他の技術 |
|---|------------|--------|
| **得意分野** | チーム内の統一・再利用 | 個別の深い課題解決 |
| **セットアップ** | 簡単・早い | 複雑・時間がかかる |
| **保守性** | 高い | 低い傾向 |
| **スケーラビリティ** | 中程度 | バリエーション豊か |

---

### 次へ進む

→ [Part 2-3: メリット・デメリット比較表](#section-02-comparison-03-pros-cons)

## Part 2-3: 4つの方法のメリット・デメリット詳細比較 {#section-02-comparison-03-pros-cons}


### はじめに

Prompt、Custom Instructions、Agent Skills、MCP の4つ方法について、詳細なメリット・デメリットを比較します。

> **💡 参考：** より広い視点については [Part 2-0: 4つのLLM拡張方法の統一解説](#section-02-comparison-00-four-concepts) を参照してください。

---

### 1. Prompt（プロンプト）

#### メリット

| # | メリット | 詳細 |
|---|---------|------|
| 1 | **最速セットアップ** | テキスト入力するだけで即座に使用可能（5分以内） |
| 2 | **学習コスト 0** | 特別な知識不要、誰でもできる |
| 3 | **完全な自由度** | プロンプトを細かくカスタマイズ可能 |
| 4 | **複雑な指示にも対応** | 一度きりの複雑なタスクに最適 |
| 5 | **プロトタイピング高速** | アイデアを即座に試行錯誤できる |
| 6 | **複数 LLM 対応** | ChatGPT、Claude など複数のツールで使用可 |

#### デメリット

| # | デメリット | 詳細 | 対策 |
|----|----------|------|------|
| 1 | **再利用性がない** | 毎回同じプロンプトを入力する必要あり | Custom Instructions で部分保存 |
| 2 | **チーム共有が困難** | コピペで共有する必要があり、管理されない | Skill に昇格 |
| 3 | **出力ばらばら** | 実行するたびに結果フォーマットが異なる可能性 | プロンプトで厳密に指定 |
| 4 | **バージョン管理がない** | 改善履歴が追跡されない | Git で手動管理 |
| 5 | **スケーリングできない** | 10個以上のプロンプト管理は混乱 | Skill で組織化 |
| 6 | **自動化できない** | ワークフロー組み込みが困難 | 他の方法を検討 |

---

### 2. Custom Instructions（カスタム指示）

#### メリット

| # | メリット | 詳細 |
|---|---------|------|
| 1 | **簡単な永続化** | ツール内保存で、以降すべての会話に適用 |
| 2 | **個人スタイルを固定** | 作業効率を向上させる基本設定を一度設定 |
| 3 | **セットアップが短い** | 30分で個人・チーム向け基本設定が完成 |
| 4 | **チーム共有が容易** | 設定テキストをコピペで共有 |
| 5 | **複数の会話に自動適用** | 毎回指示する必要なし |
| 6 | **複数 LLM 対応** | ChatGPT、Claude 等で各々設定可能 |

#### デメリット

| # | デメリット | 詳細 | 対策 |
|----|----------|------|------|
| 1 | **ツール依存** | 各ツール個別で設定が必要（CloudとChatGPT別々など） | 汎用性が必要なら MCP 検討 |
| 2 | **バージョン管理がない** | 改善履歴が追跡されない | 手動で記録・管理 |
| 3 | **チーム規模での管理困難** | 数十個以上の設定管理は複雑 | Skill に昇格 |
| 4 | **アクセス制御がない** | ユーザー単位での権限管理ができない | 大規模組織では Skill/MCP |
| 5 | **出力フォーマットが限定的** | テキスト設定のため複雑な構造化出力は困難 | Skill の JSON Schema を活用 |
| 6 | **自動化ワークフロー非対応** | マークダウンな処理フローは実装困難 | API 統合や Skill が必須 |

---

### 3. Agent Skills（スキル）

#### メリット

| # | メリット | 詳細説明 | 実例 |
|---|---------|--------|------|
| 1 | **再利用性が高い** | 一度作ったスキルを何度でも使える | 「code-review」スキルを毎日実行 |
| 2 | **チーム共有が容易** | リポジトリで一元管理、全員がアクセス | git に push するだけで全員が更新版を利用 |
| 3 | **セットアップが簡単** | JSON/YAML を書くだけ、プログラミング不要 | 1-2時間で完成 |
| 4 | **メンテナンスが容易** | スキル１つを修正すれば全員に反映 | バグ修正時に全員への連絡・対応不要 |
| 5 | **出力フォーマットが統一** | すべてのユーザーが同じ形式の結果を得る | 全員が JSON の同じスキーマで結果を得る |
| 6 | **バージョン管理が自動** | Git で自動追跡、誰が何を改善したかが明確 | Commit メッセージで改善内容を記録 |
| 7 | **パフォーマンスが予測可能** | LLM のみへの呼び出しなので計算量が安定 | キャッシングで高速化も可能 |
| 8 | **セキュリティが一元管理** | 認証・アクセス制御を一度設定すれば OK | API Key を１つだけ管理 |
| 9 | **ドキュメント要件が少ない** | スキル定義自体がドキュメント | メタデータがあれば説明書は不要 |
| 10 | **テストが簡単** | 入力と出力のテストのみ | 複雑な統合テスト不要 |

#### デメリット

| # | デメリット | 詳細説明 | 対策 |
|----|----------|--------|------|
| 1 | **外部ツール連携が限定的** | DB や API への直接アクセスが困難 | 必要に応じて MCP を併用 |
| 2 | **複雑なロジック処理が困難** | 条件分岐、ループなどのプログラムはできない | プロンプトの工夫で対応、または外部ロジック化 |
| 3 | **Copilot 専用** | GitHub Copilot でしか使えない | 他の LLM を使いたい場合は MCP 検討 |
| 4 | **リアルタイムデータが難しい** | 実行時の動的データ（最新レート等）を入手困難 | RAG + MCP で対応 |
| 5 | **初期学習コスト** | スキル定義の仕様を学ぶ必要がある | 本チュートリアルで習得可能 |
| 6 | **複雑なパラメータ型が限定的** | 基本的な型（string, number, array）が中心 | JSON Schema で拡張可能 |
| 7 | **エラーハンドリングが限定的** | LLM のエラーのみ対応 | 外部エラーが必要に応じて MCP |
| 8 | **マーケットプレイスの未成熟** | スキルの品質管理が未確立 | 信頼できるソースからのみインストール |
| 9 | **スケーラビリティに限界** | 数千個のスキル管理は困難 | 組織化・分類の工夫で対応 |
| 10 | **デバッグが眼鏡的** | LLM の生成プロセスが不透明 | ログ出力、テスト済みプロンプトの利用 |

---

### 4. MCP（Model Context Protocol）

#### メリット

| # | メリット | 詳細説明 |
|---|---------|--------|
| 1 | **複数 LLM 対応** | Claude、GPT-4 など複数のLLMで使用可能（汎用性） |
| 2 | **外部ツール統合** | Database、API、クラウドサービス等への安全なアクセス |
| 3 | **リアルタイムデータ取得** | 実行時の動的データ（最新レート、リアルタイム検索等）に対応 |
| 4 | **セキュリティ強化** | 認証・権限管理・監査ログが組み込まれている |
| 5 | **スケーラビリティ** | 複雑な統合システムに対応できる |
| 6 | **汎用プロトコル** | LLM非依存で複数システムで再利用可能 |
| 7 | **自動化深度** | ワークフロー全体の自動化が可能 |
| 8 | **エラーハンドリング** | 外部ツール側のエラーも適切に処理 |

#### デメリット

| # | デメリット | 詳細説明 | 対策 |
|----|----------|--------|------|
| 1 | **セットアップが複雑** | 専用サーバー実装が必要（8-16時間以上） | チーム内の企業向けなら価値あり |
| 2 | **学習コストが高い** | Protocol 仕様、サーバー実装に関する知識が必須 | ドキュメントと実例で学習 |
| 3 | **実装負担が大きい** | Node.js、Python等での実装が必要 | 既製 MCP Server の利用で軽減 |
| 4 | **運用・保守が必須** | MCP Server の監視、更新、故障対応が必要 | DevOps リソースが必要 |
| 5 | **セキュリティ責任** | サーバー側の認証・アクセス制御は実装者の責任 | セキュリティ人材が必須 |
| 6 | **初期投資が大きい** | 設計、実装、テスト、本番化に相応の時間・コストが必要 | エンタープライズ規模の導入向け |
| 7 | **顧客環境への対応** | 企業の IT ポリシー（ネットワーク、ファイアウォール等） への対応が必要 | 設計段階での事前調査が重要 |

---

### 5. 4つの方法の総合比較表

#### 全体比較

| 評価軸 | Prompt | Custom Instr | Skill | MCP |
|--------|--------|-----------|-------|-----|
| **セットアップ時間** | 5分 | 30分 | 1-2時間 | 8-16時間+ |
| **学習曲線** | 即習得 | 30分で十分 | 2-4時間 | 1-2週間以上 |
| **再利用性** | △低 | ◎中～高 | ◎◎高 | ◎◎◎非常に高 |
| **チーム共有** | △困難 | ◎中程度 | ◎◎容易 | ◎◎容易 |
| **バージョン管理** | ✗不可 | △手動 | ◎Git自動 | ◎Git自動 |
| **複数LLM対応** | ◎◎対応 | ◎各々設定 | ✗Copilot専用 | ◎◎対応 |
| **外部連携** | ✗不可 | ✗不可 | △限定的 | ◎◎◎対応 |
| **出力統一性** | △不確実 | ◎中程度 | ◎◎統一 | ◎◎統一 |
| **運用コスト**※ | ◎最小限 | ◎最小限 | ◎最小限 | △中程度 |
| **組織スケール** | 1-3個 | 5-10個 | 10-100個+ | 複雑統合全般 |

※ 運用コスト = LLM API 使用料を除いた「専用サーバー、インフラ、人員」等のコスト

---

### 6. シーン別の選択ガイド

#### 判断フローチャート（Phase 改訂版）

```
あなたのシーンは？

▼
Q1: これは何度も繰り返すタスク？
  │
  ├─ No
  │  └─→ Q1a: 個人のみで使う？
  │       ├─ Yes → ★ Prompt で OK
  │       └─ No  → ★ Prompt（複数人で共有可能）
  │
  └─ Yes
     └─→ Q2: チーム全体で統一したい？
          │
          ├─ No
          │  └─→ Q2a: 個人設定レベルの永続化でいい？
          │       ├─ Yes → ★ Custom Instructions
          │       └─ No  → ★ Skill でも OK
          │
          └─ Yes
             └─→ Q3: 外部ツール（DB、API等）への連携が必須？
                  │
                  ├─ No  → ★ Agent Skill
                  └─ Yes → Q3a: 複数 LLM で同じワークフロー？
                       ├─ No  → ★ Agent Skill + MCP
                       └─ Yes → ★ MCP（汎用性重視）
```

---

### 他の技術との詳細比較

#### 7. プロンプトチェーニング との メリット・デメリット

##### メリット

| メリット | 例 |
|---------|-----|
| セットアップが超高速 | 30分で実装 |
| 学習が簡単 | プロンプトの知識で十分 |
| 試行錯誤が容易 | コードを少し修正 |
| スケジュールが短い | 新規タスクもすぐ対応 |

##### デメリット

| デメリット | 影響 |
|----------|------|
| チーム内でばらばら | 出力フォーマットが異なる |
| 改善が全に周知されない | 古いプロンプトを使い続ける |
| 長期保守が困難 | 誰が何のために書いたか不明に |
| スケーリングで混乱 | 10個以上のプロンプトで管理困難 |

##### 使い分け基準

```
プロンプトチェーニング → 単発タスク、プロトタイピング
Agent Skills        → 繰り返し使うタスク、チーム共有
```

---

#### 8. RAG との比較

##### Agent Skills + RAG のメリット

| メリット | 詳細 |
|---------|------|
| 知識ベースを活用できる | 最新のドキュメント・データに基づく回答 |
| 外部データへの安全なアクセス | 検索機能を通じた間接的なアクセス |
| 正確性向上 | LLM 単独より高精度 |
| カスタマイズ可能 | 検索アルゴリズムを調整可能 |

##### Agent Skills vs RAG のデメリット

| 技術 | デメリット |
|------|-----------|
| **Agent Skills のみ** | ナレッジベースをアクセスできない |
| **RAG のみ** | チーム内で異なる検索・生成ロジック |
| **両方を統合** | 複雑さが増す |

##### ベストプラクティス

```
推奨構成：Agent Skills + RAG

「faq-chatbot」スキル
  ├─ 定義：チーム全体で統一の FAQ 応答パターン
  └─ 内部で RAG を実行
    ├─ 社内 Wiki から関連情報を検索
    ├─ 検索結果に基づいて応答を生成
    └─ 常に最新情報・統一フォーマット
```

---

#### 9. ファインチューニング との比較

##### どれをすぐ使う？

```
直近 1ヶ月：Agent Skills
↓
6ヶ月のデータ蓄積後：ファインチューニングの検討
```

##### 段階的な導入モデル

```
Phase 1: Agent Skills でスキルを整備
  └─ 日々の作業を統一化

Phase 2: フィードバック収集
  └─ LLM の出力品質の傾向を把握

Phase 3: ファインチューニング候補を定義
  └─ どの分野で超高精度が必須？

Phase 4: ファインチューニング実施
  └─ 専門分野のみに限定

Phase 5: ファインチューニング + Agent Skills
  └─ 基盤モデル + スキルで最適化
```

---

#### 10. カスタム統合 との比較

##### エンタープライズ導入時の選択

```
┌─────────────────────────────────┐
│ 企業内でのロールアウト要件       │
│ (100人以上の組織)                │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
外部システム    簡単な統一パターン
複雑統合？      のみ？
      │             │
      │             ▼
    Yes → カスタム統合  ★ Agent Skills
              ↑       (+ RAG/MCP)
              │
      複雑度が高い
```

##### 選択チェックリスト

```
□ 複数の外部 API を統合する必要があるか？
  Yes → カスタム統合 必須

□ エンタープライズレベルのセキュリティが必要？
  Yes → カスタム統合 推奨

□ チーム内での統一性が重要？
  Yes → Agent Skills + カスタム統合 の組み合わせ

□ 短期（1-2ヶ月）で導入必須？
  Yes → Agent Skills のみで開始
```

---

### 比較マトリックス: 10個の重要指標

#### 評価基準

```
★★★★★ : 非常に高い/優れている
★★★★☆ : 高い/優れている
★★★☆☆ : 中程度
★★☆☆☆ : 低い/劣っている
★☆☆☆☆ : 非常に低い/劣っている
```

#### マトリックス表

| 指標 | Agent Skills | プロンプトチェーニング | RAG | ファインチューニング | カスタム統合 |
|------|------------|-------------|-----|----------|---------|
| **再利用性** | ★★★★★ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ |
| **セットアップの早さ** | ★★★★☆ | ★★★★★ | ★★☆☆☆ | ★☆☆☆☆ | ★★☆☆☆ |
| **保守のしやすさ** | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★☆☆☆ |
| **チーム共有容易性** | ★★★★★ | ★★☆☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ |
| **学習曲線** | ★★★☆☆ (中程度) | ★★★★★ (浅い) | ★★★☆☆ | ★☆☆☆☆ (急) | ★★☆☆☆ |
| **拡張性** | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ |
| **出力安定性** | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ |
| **セキュリティ性** | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ |
| **コスト効率** | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | ★★☆☆☆ |
| **実行速度** | ★★★★☆ | ★★★★☆ | ★★☆☆☆ | ★★★★☆ | ★★★★☆ |

#### インサイト

```
最もバランスが優れている：★ Agent Skills
  - 再利用性、チーム共有、コストで圧倒的
  - 初期投資が最小限

最も拡張性が高い：★ カスタム統合
  - 複雑なロジック・セキュリティ対応可能
  - ただしコスト・時間が必要

最も学習が早い：★ プロンプトチェーニング
  - 今日からすぐ始められる
  - ただしスケーリング性に難

最も精度が高い：★ ファインチューニング
  - 専門分野での超高精度を実現
  - ただしコスト・時間・データが必要
```

---

### シナリオ別の推奨スタック

#### シナリオ1: スタートアップ（5-10人チーム）

```
推奨：Agent Skills + プロンプトチェーニング

理由：
✓ 低コスト
✓ すぐに開始可能
✓ チーム内の統一も確保
✓ 試行錯誤も容易

構成：
- 繰り返しタスク → Agent Skills
- 新規・複雑タスク → プロンプトチェーニング
```

#### シナリオ2: 成長期スタートアップ（10-50人）

```
推奨：Agent Skills + RAG

理由：
✓ チーム規模に対応
✓ 外部ナレッジ活用で精度向上
✓ スケーラビリティ確保
✓ 保守が容易

構成：
- 社内 FAQ → Agent Skills + RAG
- コード分析 → Agent Skills
- ドキュメント検索 → RAG
```

#### シナリオ3: 大企業（1000人以上）

```
推奨：Agent Skills + RAG + MCP + カスタム統合

理由：
✓ 複雑な業務フロー対応
✓ セキュリティ要件を満たす
✓ 複数システムを統合
✓ エンタープライズスケール

構成：
- 定型業務 → Agent Skills
- 社内データ利用 → Agent Skills + RAG + MCP
- 重要システム連携 → カスタム統合
```

#### シナリオ4: 超専門領域（医療・法律・金融）

```
推奨：ファインチューニング + Agent Skills

理由：
✓ 超高精度が必須
✓ 専門知識をモデルに組み込む
✓ 誤信のリスク最小化
✓ ガイドラインを遵守

構成：
- 基盤：ファインチューニング済みモデル
- 運用：Agent Skills で診断/相談フロー統一
```

---

### 決定木: 「何を選ぶべきか」

```
開始
  │
  ├─ Q1: 今すぐ始めたい？
  │    │
  │    ├─ Yes → プロンプトチェーニング
  │    │
  │    └─ No → Q2へ
  │
  ├─ Q2: チーム内での統一性が必要？
  │    │
  │    ├─ Yes → Q3へ
  │    │
  │    └─ No → プロンプトチェーニング
  │
  ├─ Q3: 複数の外部システム（DB, API）を統合？
  │    │
  │    ├─ Yes → Q5へ
  │    │
  │    └─ No → Q4へ
  │
  ├─ Q4: 知識ベース（Wiki, FAQ）を活用？
  │    │
  │    ├─ Yes → ★ Agent Skills + RAG
  │    │
  │    └─ No → ★ Agent Skills
  │
  ├─ Q5: セキュリティ要件が厳しい？
  │    │
  │    ├─ Yes → カスタム統合 OR MCP
  │    │
  │    └─ No → ★ Agent Skills + RAG + MCP
  │
  └─ Q6: 専門分野の超高精度が必須？
       │
       ├─ Yes → ファインチューニング + Agent Skills
       │
       └─ No → 上記の推奨に従う
```

---

### 次へ進む

→ [Part 2-4: 応用ケース](#section-02-comparison-04-use-cases)

## Part 2-4: 実践的なケーススタディ {#section-02-comparison-04-use-cases}


このセクションでは、Prompt、Custom Instructions、Agent Skills、MCP の4つの方法が、実際のビジネス・開発シーンでどのように活用できるのかを、具体的なケースで紹介します。

> **💡 参考：** より詳細な比較については [Part 2-0: 4つのLLM拡張方法の統一解説](#section-02-comparison-00-four-concepts) を参照してください。

---

### ケース1: Prompt を使った単発の高度な分析

#### シナリオ

```
状況：
- スタートアップの経営企画部門
- 競合分析のため、市場トレンドを急速に把握する必要がある
- 分析は今週限定の単発プロジェクト
- 複数の異なる視点からの分析が必要

課題：
□ 分析手法は複雑だが、一度きりのタスク
□ 社内で統一フォーマットは不要（経営層への説明用）
□ プロトタイピング的に複数の分析方法を試したい
```

#### Prompt での解決

```
[Prompt の例]

「以下は売上高成長率が高い 3社の事業説明です。
これらの企業について、ビジネスモデル、主な成長要因、今後の課題を分析してください。

企業A: [情報]
企業B: [情報]
企業C: [情報]

出力形式：
{
  "business_model_comparison": "3社のビジネスモデルの共通点と相違点",
  "growth_drivers": {
    "CompanyA": ["要因1", "要因2"],
    "CompanyB": ["要因1", "要因2"],
    "CompanyC": ["要因1", "要因2"]
  },
  "future_challenges": ["業界全体の課題"],
  "investment_implications": "当社への示唆"
}

詳細な JSON 形式で返してください」
```

#### なぜ Prompt を選んだのか？

| 理由 | 詳細 |
|------|------|
| **一度きり** | 今週のプロジェクトのため、長期的なメンテナンス不要 |
| **複雑な指示** | 特殊な分析フレームワークを厳密に指定可能 |
| **試行錯誤** | 分析方法を調整しながらプロンプトを改善 |
| **迅速性** | 実装に5分、すぐに分析開始可能 |
| **複数LLM試行** | ChatGPT と Claude 両方で試して比較 |

#### メリット

✅ 最小の手間で複雑な分析実施
✅ 分析方法を細かくカスタマイズ可能
✅ 複数 LLM での比較検証が容易

#### デメリット・対策

⚠️ **形式が毎回異なる可能性**
→ JSON 形式を厳密に指定

⚠️ **チーム内で共有しにくい**
→ 今週限定なので問題なし
→ 来月以降も活用するなら Skill に昇格

---

### ケース2: Custom Instructions で個人の作業効率を統一化

#### シナリオ

```
状況：
- テクニカルライター 5名のチーム
- 各自が ChatGPT を使用してドキュメント作成
- 現在の問題：
  □ ドキュメントのトーン・スタイルがばらばら
  □ 毎回「テクニカルライター向けの指示」を入力するのは面倒
  □ 社内スタイルガイドを遵守しているかが不確実
```

#### Custom Instructions での解決

```
[ChatGPT の Custom Instructions に設定]

【About you】
「あなたはシニアテクニカルライターです。
当社の製品ドキュメント作成に16年の経験があります。
技術的正確性と読みやすさを両立させることが得意です。」

【How you should respond】
「1. すべてのドキュメントは以下のスタイルで作成してください：
   - 対象：初級～中級エンジニア
   - トーン：親しみやすいが専門的
   - 使用言葉：専門用語は説明付きで）

2. 当社スタイルガイド（下記）を必ず遵守してください：
   - 見出しは H2, H3 のみ（H1 は不使用）
   - リスト項目は最大5項目に統一
   - コード例は常に「正例」「悪い例」両方を提示
   - 注釈は【重要】【補足】【参考】で分類

3. 出力形式は Markdown とし、最後に品質チェックリストを追加

4. セキュリティやコンプライアンス上の懸念があれば必ず指摘」
```

#### なぜ Custom Instructions を選んだのか？

| 理由 | 詳細 |
|------|------|
| **個人設定** | チーム内での一元管理ではなく、各自のChatGPT設定 |
| **永続化** | 一度設定すれば、以降のすべてのチャットに自動適用 |
| **チーム間共有** | 設定テキストを共有すれば、全員が統一スタイル |
| **柔軟性** | 指示を調整したい場合は各自のChatGPT設定を編集 |
| **学習コスト低** | テキスト設定を記入するだけで導入完了 |

#### メリット

✅ すべてのチャットで自動的に統一テンプレ適用
✅ チーム間で設定を共有しやすい
✅ スタイルガイド遵守が自動化される

#### デメリット・対策

⚠️ **各ツール個別設定が必要**
→ ChatGPT、Claude で別々に設定する必要がある
→ 両方使うなら両方に同じ設定

⚠️ **改善履歴が追跡されない**
→ 改善したら Google Doc などで改訂版を記録

⚠️ **大規模チームでの管理困難**
→ 50名超の場合は Skill への昇格を検討

---

### ケース3: 企業内ナレッジの体系化と共有（Agent Skills）

#### シナリオ

```
状況：
- 100人規模の SaaS スタートアップ
- エンジニア・営業・CS の3職種
- 現在の問題：
  □ コーディング規約をメモで管理 → 新人は何度も同じ質問
  □ 営業トークは属人的 → 商談成功率がばらばら
  □ CS のトラブル対応も個人のノウハウ → ナレッジが蓄積されない
```

#### Agent Skills での解決

##### スキル1: 「code-style-checker」

```json
{
  "id": "code-style-checker",
  "name": "コーディング規約チェッカー",
  "description": "会社のコーディング規約に従ったコード品質をチェック",
  
  "parameters": {
    "code_snippet": { "type": "string", "required": true },
    "language": { "type": "string", "enum": ["python", "typescript", "go"] }
  },
  
  "prompt": {
    "template": "チェック対象言語：{language}\n\n当社コーディング規約に基づいて、以下のコードを分析してください：\n\n{code_snippet}\n\nチェック項目：\n1. 命名規約（スネークケース/キャメルケース）\n2. 関数の長さ（最大30行）\n3. コメント率（10-20%推奨）\n4. エラーハンドリング\n\nJSON形式で結果を返してください"
  },
  
  "outputFormat": {
    "type": "json",
    "schema": {
      "violations": ["array of violation descriptions"],
      "score": 0-100,
      "recommendations": ["array of improvement suggestions"]
    }
  }
}
```

**ユースケース：**
```
新人エンジニアの PR レビュー
  ↓
「code-style-checker」で自動チェック
  ↓
チーム全体で統一された基準を適用
  ↓
レビューコメントが一貫性を持つ
```

##### スキル2: 「sales-pitch-generator」

```
営業が商談前に使用するスキル

入力：
- 顧客の業種
- 現在の課題（顧客が述べた内容）
- 予算規模

出力：
- 統一された営業トーク（会社の強みに基づく）
- 導入効果の推定値
- よくある質問への回答集
```

**メリット：**
```
✓ 新人営業も経験豊富な営業と同じレベルのトークでき
✓ 商談成功率が向上（チーム全体で統一）
✓ 営業のベストプラクティスが自動適用
```

##### スキル3: 「cs-troubleshooting」

```
CS チーム：顧客からの問題報告への対応

入力：
- 顧客の問題内容
- エラーメッセージ
- 利用環境（OS、ブラウザ等）

出力：
- 解決手順（ステップバイステップ）
- よくある原因と対策
- エスカレーション判定（開発チームに報告すべき？）
```

**メリット：**
```
✓ CS チーム全体で対応品質が統一
✓ ノウハウが蓄積される
✓ 初心者でも経験者レベルで対応可能
```

#### 導入期間

```
Phase 1（第1週）：スキル設計
  └─ 各部門のベストプラクティスをヒアリング

Phase 2（第2週）：スキル実装
  └─ 3つのスキルを実装・テスト

Phase 3（第3週）：パイロット運用
  └─ 各部門で試験的に運用

Phase 4（第4週以降）：本格運用
  └─ 全社で利用開始、フィードバック収集

効果測定（3ヶ月後）：
✓ コード品質スコアが平均 15 点向上
✓ 営業の商談成功率が 8% 向上
✓ CS 初期対応時間が 30% 短縮
```

#### なぜ Agent Skills を選んだのか？

| 理由 | 詳細 |
|------|------|
| **何度も繰り返す** | 毎日のコードレビュー、営業トークが必須 |
| **チーム共有** | 全員が統一基準で活動する必要がある |
| **バージョン管理** | スキルの改善を Git で追跡可能 |
| **統一フォーマット** | 全員が同じ JSON スキーマで出力取得 |

---

### ケース4: 業界別活用例

#### ケース4-1: 金融機関 - コンプライアンスチェック

##### スキル：「financial-compliance-checker」

```
金融機関の融資審査業務の自動化

入力：
- 申込者の財務情報
- 申込額
- 業界カテゴリ

処理：
1. コンプライアンスルール（反社勢力チェック、与信限度等）
2. 規制要件（業法、ローカルルール）
3. リスク評価（業績トレンド、負債比率）

出力：
- 合否判定
- リスク評価スコア
- 追加調査が必要な項目
- 根拠（なぜこの判定か）
```

**メリット：**
```
✓ 融資審査の「属人性」を排除
✓ 規制要件を自動遵守
✓ 監査対応が容易（判定根拠が明確）
✓ 処理速度が向上（手作業から自動化）
```

#### ケース4-2: 医療機関 - 医学診断補助

##### スキル：「medical-diagnosis-assistant」

```
医師の初期診断を補助するスキル

入力：
- 患者の症状
- 検査結果
- 既往歴
- 薬歴

処理：
1. 症状の差別診断（可能性のある疾患を列挙）
2. 検査結果の解釈
3. 薬物相互作用チェック

出力：
- 考えられる疾患（優先順）
- 追加検査の提案
- 用量・用法の最適化案
- 医学画像解釈の支援
```

**メリット：**
```
✓ 医師の診断精度が向上
✓ 誤診を減らす
✓ 効率的な検査計画
✓ 医学知識の最新化をスキルで実装
```

**注）医療業では特にファインチューニングと Agent Skills の組み合わせを推奨**
```
基盤：医学専門知識でファインチューニング済みモデル
  +
スキル：診断フロー・患者情報の入力形式を統一
  =
医学知識 + 効率性 + チーム共有
```

#### ケース4-3: 法律事務所 - 契約書分析

##### スキル：「contract-analysis」

```
契約書の自動分析スキル

入力：
- 契約書テキスト（または PDF）
- 契約タイプ（売買、賃貸、NDA等）
- 懸念点（何が気になるのか）

処理：
1. リスク条項の抽出
2. 業界標準との比較
3. 法的リスク評価
4. 修正提案

出力：
- 要点サマリー
- リスク箇所のハイライト
- 修正案の提案
- 業界全般の参考情報
```

**メリット：**
```
✓ 初級弁護士も経験者レベルで分析可能
✓ 分析速度が 5 倍以上に高速化
✓ 見落としが減る
```

---

### ケース5: 開発フロー最適化

#### ケース5-1: CI/CD パイプライン設定

##### スキル：「ci-cd-generator」

```
CI/CD パイプラインの自動生成

入力：
- プロジェクト言語（Python, Node.js等）
- インフラ（GitHub Actions, GitLab CI等）
- デプロイ先（AWS, GCP等）
- テスト要件（カバレッジ％）

出力：
- .github/workflows/ci.yml（完全な設定ファイル）
- 説明付きコメント
- 実装チェックリスト
```

**メリット：**
```
✓ 新規プロジェクトでも最初から最適な CI/CD 設定
✓ チーム全体で設定の品質が統一
✓ ベストプラクティスが自動適用
```

#### ケース3-2: パフォーマンス診断

##### スキル：「performance-diagnostic」

```
アプリケーションのパフォーマンス問題を診断

入力：
- パフォーマンスログ（レスポンスタイム等）
- CPU/メモリ使用率
- ボトルネック疑疑
- 実装の詳細

処理：
1. ボトルネック特定
2. 原因仮説の提案
3. 改善案の優先順付け

出力：
- 問題分析サマリー
- 根本原因の候補
- 改善施策（優先度付き）
- コード修正例
```

#### ケース3-3: コードレビュー自動化（段階1）

##### スキル：「code-review-starter」

```
開発者の PR に対して自動レビューコメント生成

入力：
- 変更ファイル群
- 変更内容（diff）
- PR の説明

処理：
1. スタイル問題の指摘
2. セキュリティ問題の検出
3. テストカバレッジのチェック
4. パフォーマンス懸念事項

出力：
- レビューコメント（PR へ自動投稿可能な形式）
- 優先度付けされた指摘
```

**メリット：**
```
✓ 初期レビューの時間短縮（人間のレビュアーが重要度の高い議論に集中可能）
✓ 初級レビュアーも経験者レベルの指摘ができる
✓ 見落とされやすいミスを自動検出
```

**注）本格的なコードレビューは人間が実施することを推奨**
```
段階1（自動）：スタイル・セキュリティの明らかな問題を検出
       ↓
段階2（人間）：アーキテクチャ・ビジネスロジックの適切性を判断
```

---

### ケース4: 営業・カスタマーサクセス

#### ケース4-1: 営業提案書自動生成

##### スキル：「sales-proposal-builder」

```
営業から顧客への提案書（RFP対応書等）を自動生成

入力：
- 顧客企業の基本情報
- 現在の課題
- 期待効果
- 予算

出力：
- Word/PDF 形式の提案書
- 導入スケジュール案
- ROI 計算表
- 参考事例
```

**メリット：**
```
✓ 提案書作成時間が 80% 削減
✓ 全営業が統一品質のプロ級提案書を作成可能
✓ 顧客対応速度が向上（受注率向上）
```

#### ケース4-2: カスタマーサクセス - チャーン防止

##### スキル：「churn-risk-assessment」

```
既存顧客のチャーン（解約）リスク診断

入力：
- 顧客の利用状況データ
- サポートチケット履歴
- 最近の利用トレンド

処理：
1. チャーンリスク評価
2. 懸念事項の特定
3. ハイリスク顧客向けの提案テンプレート生成

出力：
- ChURN リスクスコア（0-100）
- 推奨フォローアップアクション
- パーソナライズされたカスタマーサクセス提案
```

**メリット：**
```
✓ CSS チームが主動的にリスク顧客に対応可能
✓ チャーン率が低下（顧客維持率向上）
✓ 顧客満足度が向上
```

---

### ケース5: マーケティング

#### ケース5-1: コンテンツカレンダー自動生成

##### スキル：「content-calendar-generator」

```
ブログ・SNS のコンテンツカレンダー生成

入力：
- ターゲットオーディエンス
- 業界トレンド
- 季節性
- ブランドメッセージ

出力：
- 月次コンテンツカレンダー（タイトル、トピック、公開日）
- 各コンテンツの概要
- SEO キーワード案
- SNS 投稿用キャプション
```

#### ケース5-2: マーケティング分析

##### スキル：「marketing-campaign-analyzer」

```
キャンペーン終了後の分析

入力：
- キャンペーンメトリクス（CTR, CPC, conversion等）
- 競合データ
- 市場トレンド

出力：
- キャンペーン成功度評価
- 改善提案
- 次期キャンペーンへの推奨事項
```

---

### ケース6: 教育 / トレーニング

#### スキル：「employee-training-generator」

```
新人研修プログラムの自動生成

入力：
- 職種
- 経験レベル
- 研修期間

出力：
- 週ごとの研修カリキュラム
- 学習目標
- 評価方法
```

**メリット：**
```
✓ 会社の知識体系を統一した形で伝達
✓ 新人の成長速度が向上
✓ 担当トレーナーの負担軽減
```

---

### ケース7: セキュリティ・監査

#### スキル：「security-audit-assistant」

```
セキュリティ監査の自動化

入力：
- 監査対象システムの情報
- チェックリスト要件

処理：
1. セキュリティ脆弱性のスキャン
2. コンプライアンス要件の確認
3. リスク評価

出力：
- 監査報告書ドラフト
- 脆弱性リスト（優先度付き）
- 改善提案
```

---

### ROI 試算例：規模別

#### シナリオ A: 10人スタートアップ

```
投資：
- スキル開発：40時間 × $50/時 = $2,000
- 導入・トレーニング：10時間 × $50/時 = $500
- 合計：$2,500

効果（年間）：
- 生産性向上：年 500時間削減 = $25,000
- 品質向上による顧客満足度向上：年 $5,000
- 合計：$30,000

ROI = ($30,000 - $2,500) / $2,500 = 11倍
ペイバック期間：1ヶ月
```

#### シナリオ B: 100人中堅企業

```
投資：
- スキル開発：200時間 × $60/時 = $12,000
- インフラ・導入：50時間 × $60/時 = $3,000
- トレーニング：20時間 × $50/時 = $1,000
- 合計：$16,000

効果（年間）：
- 生産性向上：年 5,000時間削減 = $300,000
- 品質・統一性向上：年 $50,000
- 顧客満足度向上：年 $40,000
- 合計：$390,000

ROI = ($390,000 - $16,000) / $16,000 = 23倍
ペイバック期間：2週間
```

---

### ケース：MCP を使った複数システム統合

#### シナリオ

```
状況：
- 大規模企業（1000+ 人）
- 複数の LLM を活用（ChatGPT、Claude、内部モデル）
- 複数の外部システムと統合が必須
  □ 社内データベース（顧客情報、売上データ）
  □ Slack（ナレッジ共有、アラート）
  □ Google Workspace（ドキュメント作成）
  □ 外部 API（天気、株価等）

課題：
□ 複数 LLM で同じワークフローを実行したい
□ 外部ツール・API への安全なアクセスが必須
□ セキュリティと監査ログが重要
□ リアルタイムデータ取得が必須

例：「市場分析レポート自動生成スキル」
```

#### MCP での解決

```
MCP Server 実装図：

┌──────────────────────────────────┐
│ MCP Server                       │
│ (Node.js / Python 実装)          │
├──────────────────────────────────┤
│                                  │
│ ┌──────────────┐                 │
│ │ Resource     │                 │
│ │ Handlers     │                 │
│ └──────┬───────┘                 │
│        │                         │
│  ┌─────┴────────────────────┐   │
│  │                          │   │
│  ▼                          ▼   │
│ Database       (社内システム)   │
│ Connection     API Gateway      │
├──────────────────────────────────┤
│ 認証・権限管理                   │
│ インスタンスログ                 │
└──────────────────────────────────┘
   │
   ├─ Claude ──→
   ├─ ChatGPT ──→
   └─ Internal LLM ──→
```

**ケース：市場分析レポート生成**

```javascript
// MCP Server の例（Node.js）

const server = new Server({
  name: "market-analysis-server",
  version: "1.0.0",
});

// Resource 1: Database クエリ実行権限
server.setRequestHandler(ExecuteCommand, async (request) => {
  if (request.method === "query_sales_data") {
    // 売上データを取得
    const result = await db.query(
      "SELECT * FROM sales WHERE date >= ?",
      [request.params.start_date]
    );
    return { contents: [{ type: "text", text: JSON.stringify(result) }] };
  }
  
  if (request.method === "get_competitor_intel") {
    // 競合情報（外部 API から取得）
    const result = await fetch("https://api.market-data.com/competitors");
    return { contents: [{ type: "text", text: await result.text() }] };
  }
});

// Resource 2: Slack 通知送信
server.setRequestHandler(ExecuteCommand, async (request) => {
  if (request.method === "notify_slack") {
    await slack.chat.postMessage({
      channel: request.params.channel,
      text: request.params.message
    });
    return { contents: [{ type: "text", text: "Slack notification sent" }] };
  }
});

// Resource 3: Google Docs 作成
server.setRequestHandler(ExecuteCommand, async (request) => {
  if (request.method === "create_gdoc") {
    const doc = await googleDocs.create({
      title: request.params.title,
      content: request.params.content
    });
    return { contents: [{ type: "text", text: doc.url }] };
  }
});
```

**LLM 側の使用**

```
Claude に MCP Server を連携させると：

Claude：「市場分析レポートを生成してください」
  ↓
MCP にアクセス：「過去3ヶ月の売上データ」を取得
  ↓
MCP にアクセス：「競合企業の最新情報」を取得
  ↓
Claude：自動でレポート生成
  ↓
MCP にアクセス：「Google Docs に保存」
  ↓
MCP にアクセス：「Slack で通知」
  ↓
レポート完成＋チーム全体が通知を受け取る
```

#### なぜ MCP を選んだのか？

| 理由 | 詳細 |
|------|------|
| **複数 LLM 対応** | Claude、ChatGPT、内部モデル全てで使用可 |
| **外部連携** | Database、API、Slack等への安全なアクセス |
| **セキュリティ** | 認証・権限管理・監査ログが組み込まれている |
| **リアルタイム** | 実行時に最新データを動的に取得 |
| **エンタープライズ規模** | 大規模組織の複雑な要件に対応 |

#### メリット

✅ 複数 LLM で同一のワークフロー実行
✅ 外部システムへの安全アクセス
✅ リアルタイムデータに対応
✅ 監査コンプライアンス要件をクリア
✅ セキュリティ部門の承認を取得しやすい

#### デメリット・対策

⚠️ **セットアップが複雑**
→ 専任の DevOps / インフラエンジニアが必須

⚠️ **初期投資が大きい**
→ エンタープライズ規模での ROI 計算で正当化

⚠️ **運用・保守が必須**
→ SRE チームでの継続的な監視

---

### 4つの方法の使い分けまとめ

```
シーン                  → 推奨方法

単発の複雑分析          → Prompt
個人の効率化            → Custom Instructions
チーム内の統一運用      → Agent Skills
複数 LLM との汎用連携   → MCP


段階的な導入パターン：

Phase 1（小規模）
  ├─ Prompt で各種タスクを試行
  └─ 成功したら → Custom Instructions で個人化

Phase 2（チーム化）
  ├─ Custom Instructions を Skill に昇格
  └─ Git で共有・バージョン管理開始

Phase 3（エンタープライズ化）
  ├─ 複数 LLM での運用が必要に
  └─ MCP で統一的にアクセス制御

Phase 4（最適化）
  └─ Prompt + Custom Instr + Skill + MCP を組み合わせ活用
```

---

### 実装チェックリスト: スキル導入手順

```
□ Phase 1: 計画（1週間）
  □ 導入対象のスキルを3つ選定
  □ 各スキルの入出力仕様を定義
  □ ステークホルダーからの承認取得

□ Phase 2: 開発（1-2週間）
  □ スキル定義ファイル（JSON）の作成
  □ プロンプトテンプレートの作成・テスト
  □ 出力スキーマの定義
  □ エラーハンドリングの実装

□ Phase 3: テスト（1週間）
  □ 単体テスト（各スキルの動作確認）
  □ 統合テスト（複数スキルの組み合わせ）
  □ ユーザー受け入れテスト（実部門での試用）
  □ パフォーマンステスト（応答時間測定）

□ Phase 4: 展開（1週間）
  □ トレーニング資料作成
  □ チームメンバーへのトレーニング実施
  □ 本番環境への導入
  □ 初期サポート体制構築

□ Phase 5: 運用・改善（継続）
  □ ユーザーフィードバック収集
  □ 月ごとのスキル改善
  □ 新スキルの開発検討
  □ ROI 測定
```

---

### 次へ進む

→ [Part 3: 実装編](#section-03-implementation-01-getting-started) - 実際にスキルを作成してみよう

# Implementation {#chapter-03-implementation}

## Part 3-1: スキル作成のステップバイステップガイド {#section-03-implementation-01-getting-started}


### 概要

このセクションでは、実際に Agent Skill を一から作成するための完全なガイドを提供します。

---

### スキル作成の5つのフェーズ

```
┌──────────────────────────────────────────┐
│ Phase 1: 要件定義                        │
│ 「何をするスキルか」を明確化             │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│ Phase 2: スキル設計                      │
│ 入出力、パラメータを決定                 │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│ Phase 3: 実装                            │
│ スキル定義ファイル（JSON）に記述        │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│ Phase 4: テスト                          │
│ 複数のテストケースで動作確認            │
└──────────────┬───────────────────────────┘
               │
┌──────────────▼───────────────────────────┐
│ Phase 5: デプロイ & ドキュメント         │
│ リポジトリに登録、使用方法説明          │
└──────────────────────────────────────────┘
```

---

### Phase 1: 要件定義

#### ステップ1-1: スキルの目的を明確化

```
質問フレームワーク：

1. 「このスキルで何を解決するのか？」
   例：「開発者が毎回、同じコード品質チェックを手で実行している」
   
2. 「現在、どのように実施されているのか？」
   例：「手で Copilot に長いプロンプトを毎回入力」
   
3. 「理想的なはどうなるべきか？」
   例：「コードを選択してスキルをワンクリック、結果が統一フォーマットで得られる」
   
4. 「どのくらいの時間短縮が期待できるか？」
   例：「1回あたり 5 分削減、週 5 回使用なら週 25 分削減」

5. 「チーム全体でいくつの人が使うか？」
   例：「15人のエンジニア」
```

#### ステップ1-2: スキルの対象ユーザーを定義

```
例1: コード品質分析スキル

対象ユーザー：
- 経験レベル：全レベル（初心者から経験者）
- 職種：エンジニア（QA含む）
- ユースケース：
  □ PR レビュー時
  □ 新人教育時
  □ リファクタリング前の分析
  □ セキュリティ審査

対象メンバー数：15人（R&D チーム）

期待される効果：
- 初心者でも経験者レベルの品質分析ができる
- レビュー時間が 30% 短縮
```

#### ステップ1-3: スキルの範囲を限定

```
「何をするか」だけでなく「何をしないか」も明確化

コード品質分析スキルの場合：

✓ するもの：
  - コードの可読性評価
  - パフォーマンス上の問題検出
  - セキュリティ脆弱性の指摘
  
✗ しないもの：
  - コードの自動修正（提案のみ）
  - 複数ファイルの解析（単一ファイルのみ）
  - リアルタイムの CI/CD 統合（手動実行のみ）
```

---

### Phase 2: スキル設計

#### ステップ2-1: 入力パラメータを定義

```
テーブルで整理：

| パラメータ名 | 型 | 必須 | 制約 | 例 |
|-----------|-----|------|------|-----|
| code_snippet | string | Yes | Max 5000 chars | def foo():\n  pass |
| language | string | Yes | enum: python,js,... | python |
| focusAreas | array | No | enum values list | ["readability", "performance"] |
| detail_level | string | No | enum: basic, detailed | detailed |

チェックリスト：
□ 各パラメータの目的が明確か？
□ 必須・オプションの区別は適切か？
□ 制約条件（最大文字数等）は設定されているか？
□ デフォルト値は定義されているか？
```

#### ステップ2-2: 出力フォーマットを設計

```
JSON Schema で定義：

{
  "skills": {
    "format": "JSON",
    "structure": {
      "overallScore": "number (0-100)",
      "categories": [
        {
          "name": "readability",
          "score": "number (0-100)",
          "issues": ["array of strings"],
          "severity": ["HIGH", "MEDIUM", "LOW"]
        }
      ],
      "recommendations": ["array of actionable suggestions"],
      "examples": ["array of code examples"]
    }
  }
}

チェックリスト：
□ 出力フォーマットはキャッシング・検索に適しているか？
□ ユーザーが簡単にパースできる形式か？
□ 出力例をいくつか用意したか？
```

#### ステップ2-3: 依存関係と制約を識別

```
例：コード品質分析スキル

依存関係：
- LLM API（Claude 3.5 Sonnet 以上推奨）
- 構文解析（軽度 - LLM 側で対応）

制約：
- タイムアウト：30 秒
- 入力サイズ：最大 5000 文字
- 言語対応：Python, JavaScript, TypeScript, Java, Go のみ
- 定期的なモデル更新に対応可能か？

リスク評価：
□ LLM が新しいセキュリティ脆弱性を検出できるか？
   → YES: LLM は常に学習中のため対応可能
□ 言語環境の違いで結果が変わるか？
   → YES: テンプレートで言語固有のベストプラクティスを組み込み
```

---

### Phase 3: 実装

#### ℹ️ フォーマット選択ガイド

スキルを実装する方法は **2 つ** あります：

| 項目 | SKILL.md（推奨）| JSON（高度）|
|------|-----|-----|
| **形式** | Markdown + YAML | JSON |
| **保存場所** | `.github/skills/SKILL.md` | API層/内部管理 |
| **推奨対象** | ほぼすべての開発者 | システム開発者・複雑なケース |
| **学習パス** | Part 0 を確認 | このセクションを続行 |

👉 **初めてなら [Part 0: スキル形式の理解](../../00-fundamentals/00-skill-format-overview.md) で SKILL.md フォーマットを学んでください。**

---

#### ステップ3-1: スキル定義ファイルの骨組みを作成

**SKILL.md フォーマットを使う場合（推奨）:**

`.github/skills/code-quality-analyzer/SKILL.md` を作成

```markdown
---
name: code-quality-analyzer
description: 提供されたコードの品質を多面的に分析します
license: MIT
---

# コード品質分析スキル

## 概要
このスキルでコード品質を以下の観点から分析します：
- 可読性
- パフォーマンス
- セキュリティ
- テスト可能性

## 使い方

コードを選択してスキルを実行してください。

## パラメータ

### code_snippet (必須)
分析対象のコード

### language (必須)  
プログラミング言語: python, javascript, typescript, java, go

### focusAreas (オプション)
重点分析エリア（カンマ区切り）
デフォルト: readability,performance,security,testability

### detailLevel (オプション)
結果の詳細度: basic / detailed
デフォルト: detailed
```

---

**JSON フォーマットを使う場合（内部管理向け）:**

```json
{
  "id": "skill-id",
  "version": "1.0.0",
  "name": "スキル名（日本語）",
  "description": "スキルの説明",
  
  "metadata": {
    "author": "作成者名",
    "created": "2026-03-07",
    "lastUpdated": "2026-03-07",
    "category": "category-name",
    "tags": ["tag1", "tag2"],
    "documentation": "https://..."
  },
  
  "parameters": {},
  "prompt": {},
  "outputFormat": {},
  "validation": {}
}
```

#### ステップ3-2: パラメータを実装

```json
{
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "分析対象のコード",
      "required": true,
      "minLength": 1,
      "maxLength": 5000
    },
    
    "language": {
      "type": "string",
      "description": "プログラミング言語",
      "required": true,
      "enum": ["python", "javascript", "typescript", "java", "go"]
    },
    
    "focusAreas": {
      "type": "array",
      "description": "重点分析エリア",
      "items": {
        "type": "string",
        "enum": ["readability", "performance", "security", "testability"]
      },
      "default": ["readability", "performance", "security", "testability"]
    },
    
    "detailLevel": {
      "type": "string",
      "description": "結果の詳細度",
      "enum": ["basic", "detailed"],
      "default": "detailed"
    }
  }
}
```

#### ステップ3-3: プロンプトテンプレートを実装

```json
{
  "prompt": {
    "system": "You are an expert code reviewer specializing in software quality...",
    
    "template": "Analyze the following {language} code for quality issues:\n\nCode:\n{code_snippet}\n\nFocus areas: {focusAreas|join(', ')}\n\nDetail level: {detailLevel}\n\nProvide analysis in JSON format as specified."
  }
}
```

**プロンプト作成のコツ：**
```
1. システムプロンプト：
   - LLM に役割（専門家など）を与える
   - 期待される動作を説明
   
2. テンプレート：
   - 変数は {変数名} で記述
   - ユーザーが提供した値を埋め込む
   - 期待される出力形式を明示（JSON, Markdown等）
   
3. テンプレート関数（オプション）：
   - |join(', ') - 配列を連結
   - |escape - 特殊文字をエスケープ
   - |uppercase - 大文字化
```

#### ステップ3-4: 出力フォーマットを実装

```json
{
  "outputFormat": {
    "type": "json",
    "schema": {
      "type": "object",
      "properties": {
        "overallScore": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "Overall quality score"
        },
        "categories": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "enum": ["readability", "performance", "security", "testability"]
              },
              "score": { "type": "number", "minimum": 0, "maximum": 100 },
              "issues": {
                "type": "array",
                "items": { "type": "string" }
              }
            },
            "required": ["name", "score", "issues"]
          }
        },
        "recommendations": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["overallScore", "categories", "recommendations"]
    }
  }
}
```

#### ステップ3-5: 検証ルールを実装

```json
{
  "validation": {
    "timeout": 30,
    "maxRetries": 2,
    "cacheEnabled": true,
    "cacheTTL": 3600,
    "rateLimit": {
      "requestsPerMinute": 30,
      "requestsPerHour": 1000
    }
  }
}
```

---

### Phase 4: テスト

#### ステップ4-1: テストケースを設計

```
テストケース例：

Test Case 1: 基本的な Python コード
  入力：
    code_snippet: "def hello():\n    print('hello')"
    language: "python"
  期待される出力：
    - overallScore: 70-85
    - readability 指摘なし
    - security 指摘なし
  実行手順：
    1. スキルを実行
    2. 出力スキーマの検証
    3. スコアの妥当性を確認

Test Case 2: セキュリティ問題を含むコード
  入力：
    code_snippet: "sql = 'SELECT * FROM users WHERE id=' + user_input"
    language: "python"
  期待される出力：
    - security スコアが低い（0-30）
    - SQL インジェクション警告が含まれる

Test Case 3: 性能問題を含むコード
  入力：
    code_snippet: "for i in range(1000000):\n    for j in range(1000000):\n        x += i*j"
    language: "python"
  期待される出力：
    - performance スコアが低い
    - ネストループの警告

Test Case 4: エッジケース - 最大サイズ
  入力：
    code_snippet: [5000文字の長いコード]
  期待される出力：
    - スキーマ検証に成功
    - タイムアウトしない（30秒以内）

Test Case 5: エッジケース - 無効な言語
  入力：
    language: "ruby"
  期待される出力：
    - エラー応答
    - 有効な言語リストを返却
```

#### ステップ4-2: テストの実行

```
実行手順：

1. 各テストケースを個別に実行
   └─ 出力がスキーマに適合しているか確認

2. 複数のテストケースを連続実行
   └─ メモリリークやキャッシュ問題がないか確認

3. エラーリトライをテスト
   └─ 失敗時に適切に再試行されるか確認

4. パフォーマンステスト
   └─ 平均応答時間、P99応答時間を測定
```

#### ステップ4-3: テスト結果のドキュメント化

```
テスト結果レポート：

| テストケース | 結果 | 応答時間 | 備考 |
|-----------|------|--------|------|
| Test 1 | Pass | 2.3s | - |
| Test 2 | Pass | 3.1s | - |
| Test 3 | Pass | 2.8s | - |
| Test 4 | Pass | 8.9s | 最大入力サイズ |
| Test 5 | Pass | 0.5s | エラー応答 |

全テストで PASS。本番環境へ進む
```

---

### Phase 5: デプロイ & ドキュメント

#### ステップ5-1: リポジトリへの登録

```
GitHub公式推奨のディレクトリ構成：

.github/
└── skills/
    └── code-quality-analyzer/
        └── SKILL.md                    # スキル定義ファイル（推奨形式）
```
    └── analyze-code-quality-test.json # テストケース

Git コマンド：

git add .github/skills/code-quality-analyzer/SKILL.md
git add .github/skills/code-quality-analyzer/
git commit -m "Add skill: code-quality-analyzer v1.0.0"
git push origin main
git push origin v1.0.0
```

### ステップ5-2: ドキュメントを作成

```
README.md の内容：

# Skill: analyze-code-quality

### 説明
Python, JavaScript, Java, Go コードの品質を分析し、
改善点を提案するスキル

### 使用方法
```

スキル名: analyze-code-quality
入力: code_snippet, language, focusAreas
出力: JSON（スコア + 指摘事項）

```

### 使用例
...

### パラメータ
...

### 出力フォーマット
...

### サンプル実行結果
...

### 制限事項
...

### トラブルシューティング
...
```

### ステップ5-3: マーケットプレイスに登録（オプション）

```
GitHub Marketplace への登録手順：
1. README + ドキュメントが完備されているか確認
2. セキュリティスキャンを実行
3. ライセンス（MIT, Apache 2.0等）を付与
4. Marketplace に登録リクエスト
```

---

## チェックリスト: スキル完成まで

```
□ Phase 1: 要件定義
  □ スキルの目的が明確化されているか
  □ 対象ユーザーが定義されているか
  □ スキルの範囲（何をするか/しないか）が明確か

□ Phase 2: スキル設計
  □ 入力パラメータが全て定義されているか
  □ 出力フォーマットが詳細に設計されているか
  □ 依存関係と制約が明確か

□ Phase 3: 実装
  □ スキル定義ファイル（JSON）が完成しているか
  □ システムプロンプト + テンプレートが効果的か
  □ パラメータの検証ルールが設定されているか
  □ 出力スキーマが定義されているか

□ Phase 4: テスト
  □ 複数のテストケースで動作確認を実施したか
  □ エッジケースも含めてテストしたか
  □ パフォーマンス要件を満たしているか
  □ エラーハンドリングが適切か

□ Phase 5: デプロイ & ドキュメント
  □ リポジトリに登録されたか
  □ 使用方法のドキュメントが完成しているか
  □ チーム内でトレーニングを実施したか
  □ 本番環境で正常に動作するか確認したか
  □ ユーザーサポート体制が構築されているか
```

---

## よくある失敗パターン と対策

### 失敗1: プロンプトテンプレートが曖昧

```
❌ 悪い例：
"Analyze this code and provide feedback"

✅ 良い例：
"Analyze the following {language} code for {focusAreas}.
Provide output in JSON format with these fields:
- overallScore (0-100)
- categories (array with name, score, issues)
- recommendations (array of actionable suggestions)"
```

### 失敗2: 出力スキーマが厳しすぎる / 緩すぎる

```
❌ 厳しすぎる：
LLM が常に正確な数値を出力できない

✅ 適切：
score: number, minimum 0, maximum 100
(LLM は 0-100 の範囲で出力できる)

❌ 緩すぎる：
score: any
(スキーマとして意味をなさない)

✅ 適切：
score: number (recommended 0-100)
```

### 失敗3: テストケースが不十分

```
❌ テストケースが少ない：
- 正常系のみテスト
- エッジケースをテストしない

✅ 十分なテスト：
- 正常系（複数パターン）
- 異常系（無効な入力）
- エッジケース（最大入力等）
- パフォーマンス（最大負荷）
```

### 失敗4: ドキュメントが不足

```
❌ 不足：
- 使用方法が書いていない
- パラメータの説明がない

✅ 完全：
- スキルの詳細説明
- パラメータ一覧とその説明
- 使用例（複数パターン）
- 出力例
- FAQ
- トラブルシューティング
```

---

## 次へ進む

→ [Part 3-2: スキルの構成要素](02-skill-structure.md)

その後、3つの実装例を見ていきます：
→ [Part 3-3: サンプルスキル #1 - コード分析](03-sample-code-analysis.md)

## Part 3-2: スキルの構成要素 {#section-03-implementation-02-skill-structure}


このセクションでは、スキル定義の詳細な要素を解説します。

---

### ℹ️ SKILL.md と JSON の関係

このセクションでは **JSON フォーマットの内部構造** を詳しく説明しています。

- **SKILL.md フォーマット**: ユーザーが `.github/skills/` に保存する **Markdown形式**（Part 3-3, 3-4, 3-5 で学習）
- **JSON フォーマット**: SKILL.md 内容や内部管理を **構造化・検証** するための形式（このセクション）

#### JSON が活躍する場所

```
┌─────────────────────────────┐
│  SKILL.md（ユーザー向け）    │
│  .github/skills/SKILL.md    │
└────────────┬────────────────┘
             │ 内部で変換 / 検証
             ▼
┌─────────────────────────────┐
│  JSON（システム向け）        │
│  スキマ定義・型検証・API    │
└─────────────────────────────┘
```

**このセクション（Part 3-2）**: 上図の JSON 部分の詳細を学びます。

---

### スキル定義ファイルの全体構造

```json
{
  "id": "スキルの一意識別子",
  "version": "セマンティックバージョン",
  "name": "ユーザーが見る名前",
  "description": "スキルの説明",
  "metadata": { /* スキル情報 */ },
  "parameters": { /* 入力パラメータ */ },
  "prompt": { /* LLM への指示 */ },
  "outputFormat": { /* 出力形式定義 */ },
  "validation": { /* 実行時制約 */ }
}
```

---

### 1. メタデータ（metadata）

#### 概要

スキル自体ではなく、**スキルについての情報**を記述します。

#### 詳細説明

```json
{
  "metadata": {
    "author": "作成者名（個人またはチーム）",
    "authorEmail": "author@example.com",
    
    "created": "2026-03-07",
    "lastUpdated": "2026-03-15",
    
    "category": "code-analysis",
    "subcategory": "quality",
    
    "tags": ["python", "javascript", "code-quality", "team-productivity"],
    
    "documentation": "https://docs.example.com/skills/code-quality",
    "externalLinks": [
      { "label": "GitHub Repository", "url": "https://github.com/..." },
      { "label": "Video Tutorial", "url": "https://youtube.com/..." }
    ],
    
    "compatibility": {
      "minCopilotVersion": "1.0.0",
      "supportedLanguages": ["en", "ja"]
    },
    
    "license": "MIT",
    "visibility": "public"
  }
}
```

#### 各フィールドの説明

| フィールド | 型 | 必須 | 説明 |
|----------|-----|------|------|
| **author** | string | Yes | スキル作成者 |
| **created** | string (ISO 8601) | Yes | 作成日（YYYY-MM-DD） |
| **lastUpdated** | string (ISO 8601) | Yes | 最終更新日 |
| **category** | string | Yes | カテゴリ（code-analysis, docs-generation等） |
| **tags** | array | Yes | 検索用タグ |
| **documentation** | string (URL) | No | ドキュメント URL |
| **license** | string | No | ライセンス（MIT, Apache 2.0等） |
| **visibility** | string | No | 公開範囲（public, private, org） |

#### 用途

1. **検索・ディスカバリー**
   ```
   ユーザー検索：tags が ["python", "code-quality"] のスキル
   → 該当スキルを発見
   ```

2. **バージョン管理**
   ```
   created: "2026-03-07"
   lastUpdated: "2026-03-15"
   → 更新頻度を追跡可能
   ```

3. **保守性**
   ```
   author: "Alice Team"
   → 質問時の連絡先が明確
   ```

---

### 2. パラメータ（parameters）

#### 概要

ユーザーが **スキル実行時に提供するデータ** を定義します。

#### 完全な例

```json
{
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "分析対象のコード",
      "required": true,
      "minLength": 1,
      "maxLength": 5000,
      "pattern": "^[\\s\\S]*$",
      "example": "def hello():\n    print('hello')"
    },
    
    "language": {
      "type": "string",
      "description": "プログラミング言語",
      "required": true,
      "enum": ["python", "javascript", "typescript", "java", "go"],
      "default": "javascript"
    },
    
    "focusAreas": {
      "type": "array",
      "description": "重点分析エリア",
      "items": {
        "type": "string",
        "enum": ["readability", "performance", "security", "testability"]
      },
      "minItems": 1,
      "maxItems": 4,
      "default": ["readability", "performance", "security", "testability"]
    },
    
    "detailLevel": {
      "type": "string",
      "description": "出力の詳細度",
      "enum": ["basic", "detailed", "comprehensive"],
      "default": "detailed"
    },
    
    "maxIssues": {
      "type": "number",
      "description": "返却する最大指摘件数",
      "minimum": 1,
      "maximum": 100,
      "default": 20
    }
  }
}
```

#### サポートされる型

| 型 | 説明 | 例 |
|----|------|-----|
| **string** | テキスト | "python" |
| **number** | 数値（整数・小数） | 42, 3.14 |
| **boolean** | 真偽値 | true, false |
| **array** | 配列 | ["a", "b", "c"] |
| **object** | オブジェクト（複雑型） | { "key": "value" } |

#### パラメータの制約

```json
// String 型の制約
{
  "type": "string",
  "minLength": 1,        // 最小文字数
  "maxLength": 5000,     // 最大文字数
  "pattern": "^[a-z]+$", // 正規表現による制約
  "enum": ["a", "b", "c"] // 選択肢から選ぶ
}

// Number 型の制約
{
  "type": "number",
  "minimum": 0,          // 最小値（包括）
  "maximum": 100,        // 最大値（包括）
  "exclusiveMinimum": 0, // 最小値（排他）
  "exclusiveMaximum": 100, // 最大値（排他）
  "multipleOf": 5        // 倍数制約（5の倍数）
}

// Array 型の制約
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": ["a", "b", "c"]
  },
  "minItems": 1,         // 最小要素数
  "maxItems": 10,        // 最大要素数
  "uniqueItems": true    // 重複禁止
}
```

---

### 3. プロンプト（prompt）

#### 概要

**LLM に送信する指示文** を定義します。

#### 完全な例

```json
{
  "prompt": {
    "system": "You are an expert code reviewer with 10+ years of experience...",
    
    "template": "Analyze the following {language} code for quality issues:\n\nCode:\n{code_snippet}\n\nFocus areas: {focusAreas|join(', ')}\nDetail level: {detailLevel}\n\nProvide analysis in JSON format.",
    
    "variables": [
      {
        "name": "code_snippet",
        "type": "string",
        "source": "parameter"
      },
      {
        "name": "language",
        "type": "string",
        "source": "parameter"
      },
      {
        "name": "focusAreas",
        "type": "array",
        "source": "parameter",
        "processor": "join-comma"
      }
    ],
    
    "advancedOptions": {
      "temperature": 0.3,
      "topP": 0.9,
      "maxTokens": 2000
    }
  }
}
```

#### 要素説明

##### System Prompt

```
役割と背景を LLM に与える

例1（専門家として）：
"You are an expert Python developer with 15+ years of experience..."

例2（トーン指定）：
"Respond in a professional, technical manner. Use JSON format exclusively."

例3（制約指定）：
"You must respond in valid JSON format. Do not include markdown formatting."
```

##### Template

```
ユーザー入力を埋め込むテンプレート

変数置換：
{code_snippet} → ユーザーが入力したコード
{language} → "python", "javascript" 等

フィルタ関数（オプション）：
{focusAreas|join(', ')} → ["readability", "security"] → "readability, security"
{text|uppercase} → "hello world" → "HELLO WORLD"
{code|escape} → コード内の特殊文字をエスケープ
```

#### テンプレート作成のベストプラクティス

```
❌ 悪い例：
"Analyze the code:\n{code_snippet}"

✅ 良い例：
"You are analyzing {language} code.

Code to analyze:
{code_snippet}

Analysis focus areas: {focusAreas|join(', ')}
Detail level: {detailLevel}

Provide your analysis in the following JSON format:
{
  'overallScore': <number 0-100>,
  'categories': [
    {'name': <category>, 'score': <number 0-100>, 'issues': [<string>]}
  ]
}"

なぜ良いか：
1. 言語を明示的に指定
2. 出力形式を詳細に説明
3. JSON 形式の例を示す
4. パースが容易
```

#### Advanced Options

```json
{
  "advancedOptions": {
    "temperature": 0.3,      // 0-2: 低いほど決定的、高いほど創造的
    "topP": 0.9,             // 0-1: 核サンプリングの多様性
    "frequencyPenalty": 0.0, // -2-2: 繰り返し単語のペナルティ
    "presencePenalty": 0.0,  // -2-2: 新しい単語の奨励
    "maxTokens": 2000        // 最大出力トークン数
  }
}
```

**推奨値：**
```
分析的・正確性重視のタスク：
  temperature: 0.2-0.5
  topP: 0.8-0.9
  
創造的・多様性重視のタスク：
  temperature: 0.7-1.0
  topP: 0.9-1.0
```

---

### 4. 出力フォーマット（outputFormat）

#### 概要

**LLM からの応答が期待スキーマに従っているか検証** する定義です。

#### 完全な例

```json
{
  "outputFormat": {
    "type": "json",
    
    "schema": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      
      "type": "object",
      
      "title": "CodeQualityAnalysis",
      
      "description": "Analysis result for code quality",
      
      "properties": {
        "overallScore": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "Overall quality score"
        },
        
        "categories": {
          "type": "array",
          
          "items": {
            "type": "object",
            
            "properties": {
              "name": {
                "type": "string",
                "enum": ["readability", "performance", "security", "testability"]
              },
              "score": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "issues": {
                "type": "array",
                "items": { "type": "string" }
              },
              "severity": {
                "type": "array",
                "items": {
                  "type": "string",
                  "enum": ["HIGH", "MEDIUM", "LOW"]
                }
              }
            },
            
            "required": ["name", "score", "issues"],
            "additionalProperties": false
          },
          
          "minItems": 1,
          "maxItems": 10
        },
        
        "recommendations": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Actionable improvement suggestions"
        }
      },
      
      "required": ["overallScore", "categories", "recommendations"],
      "additionalProperties": false
    },
    
    "examples": [
      {
        "overallScore": 75,
        "categories": [
          {
            "name": "readability",
            "score": 85,
            "issues": [],
            "severity": []
          },
          {
            "name": "security",
            "score": 60,
            "issues": ["SQL injection risk detected"],
            "severity": ["HIGH"]
          }
        ],
        "recommendations": ["Use parameterized queries for SQL statements"]
      }
    ]
  }
}
```

#### JSON Schema の重要な制約

| キーワード | 説明 | 例 |
|----------|------|-----|
| **type** | データ型を指定 | "string", "number", "object", "array" |
| **properties** | オブジェクトのフィールドを定義 | { "name": { "type": "string" } } |
| **required** | 必須フィールドを指定 | ["name", "score"] |
| **enum** | 選択可能な値を限定 | ["HIGH", "MEDIUM", "LOW"] |
| **minimum/maximum** | 数値の範囲制約 | { "minimum": 0, "maximum": 100 } |
| **minItems/maxItems** | 配列サイズ制約 | { "minItems": 1, "maxItems": 10 } |
| **additionalProperties** | オブジェクトに追加フィールドを許可 | true / false |

#### 出力フォーマットの検証フロー

```
LLM が出力を生成
   ↓
JSON パースが可能か？
   ├─ No → エラー、リトライ
   └─ Yes ↓
Schemaに適合しているか？
   ├─ No → エラー、リトライ
   └─ Yes ↓
ユーザーに返却
```

---

### 5. 検証（validation）

#### 概要

**スキル実行時の制約や動作ルール** を定義します。

#### 完全な例

```json
{
  "validation": {
    "timeout": 30,
    
    "maxRetries": 2,
    
    "retryStrategy": {
      "backoff": "exponential",
      "initialDelayMs": 1000,
      "maxDelayMs": 10000
    },
    
    "caching": {
      "enabled": true,
      "ttl": 3600,
      "keyStrategy": "md5-hash-of-inputs"
    },
    
    "rateLimit": {
      "requestsPerMinute": 30,
      "requestsPerHour": 1000,
      "requestsPerDay": 10000
    },
    
    "authentication": {
      "required": true,
      "scope": ["read:code", "write:analysis"]
    },
    
    "costControl": {
      "maxTokensPerRequest": 2000,
      "estimatedCostPerRequest": 0.01,
      "dailyBudget": 100
    }
  }
}
```

#### 各フィールドの説明

##### Timeout

```
スキル実行の最大待機時間（秒）

timeout: 30
  → LLM が 30 秒以内に応答しなければエラー
  
推奨値：
  - 高速タスク（スタイルチェック）：10-15秒
  - 中程度（分析・生成）：20-30秒
  - 複雑タスク（ドキュメント生成）：30-60秒
```

##### MaxRetries

```
失敗時の再試行回数

maxRetries: 2
  → 失敗時に最大 2 回リトライ
  → 合計 3 回試行
  
推奨値：2-3回
```

##### Caching

```
同じ入力に対する結果をキャッシュ

caching:
  enabled: true
  ttl: 3600  // 1 時間有効

メリット：
  - 応答時間が 99%+ 高速化（キャッシュヒット時）
  - LLM API 呼び出し削減
  - コスト削減
  
キャッシュキーの生成：
  MD5(skill_id + version + parameters_json)
```

##### RateLimit

```
API 呼び出し頻度の制限

rateLimit:
  requestsPerMinute: 30   // 1分間に30回まで
  requestsPerHour: 1000   // 1時間に1000回まで
  requestsPerDay: 10000   // 1日に10000回まで
```

##### Authentication

```
実行権限・スコープの定義

authentication:
  required: true
  scope: ["read:code", "write:analysis"]
  
スコープの例：
  - read:code       : コード読み取り権限
  - write:analysis  : 分析結果書き込み権限
  - read:private    : プライベートコード読み取り
```

##### CostControl

```
API 使用料金の制御

maxTokensPerRequest: 2000
  → 1回のリクエストで最大 2000 トークン使用

estimatedCostPerRequest: 0.01
  → 1回あたりの推定料金：$0.01

dailyBudget: 100
  → 1日の最大料金：$100
```

---

### スキル定義ファイル全体の例

```json
{
  "id": "analyze-code-quality",
  "version": "1.0.0",
  "name": "コード品質分析",
  "description": "Python, JavaScript, Java, Go コードの品質分析スキル",
  
  "metadata": {
    "author": "AI Engineering Team",
    "created": "2026-03-07",
    "lastUpdated": "2026-03-07",
    "category": "code-analysis",
    "tags": ["python", "javascript", "typescript", "java", "go", "quality"],
    "documentation": "https://docs.example.com/skills/code-quality",
    "license": "MIT"
  },
  
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "分析対象のコード",
      "required": true,
      "maxLength": 5000
    },
    "language": {
      "type": "string",
      "required": true,
      "enum": ["python", "javascript", "typescript", "java", "go"]
    },
    "focusAreas": {
      "type": "array",
      "items": { "type": "string", "enum": ["readability", "performance", "security", "testability"] },
      "default": ["readability", "performance", "security", "testability"]
    }
  },
  
  "prompt": {
    "system": "You are an expert code reviewer...",
    "template": "Analyze the {language} code:\n{code_snippet}\n\nFocus: {focusAreas|join(', ')}"
  },
  
  "outputFormat": {
    "type": "json",
    "schema": {
      "type": "object",
      "properties": {
        "overallScore": { "type": "number", "minimum": 0, "maximum": 100 },
        "categories": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "score": { "type": "number" },
              "issues": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      },
      "required": ["overallScore", "categories"]
    }
  },
  
  "validation": {
    "timeout": 30,
    "maxRetries": 2,
    "caching": { "enabled": true, "ttl": 3600 }
  }
}
```

---

### 次へ進む

→ [Part 3-3: サンプルスキル #1 - コード分析](#section-03-implementation-03-sample-code-analysis)

## Part 3-3: サンプルスキル #1 - コード品質分析 {#section-03-implementation-03-sample-code-analysis}


このセクションでは、**実際に使用できる完全なコード分析スキル** を SKILL.md フォーマットで実装します。

---

### スキル概要

```
スキル名：analyze-code-quality
目的：Python, JavaScript, TypeScript, Java, Go のコードの品質を分析
難度：★★☆☆☆（初級）
実装時間：30分～1時間
推奨フォーマット：SKILL.md
```

---

### SKILL.md フォーマット（推奨）

#### ファイル：`.github/skills/code-quality-analyzer/SKILL.md`

```markdown
---
name: code-quality-analyzer
description: Python, JavaScript, TypeScript, Java, Go コードの品質を多次元的に分析し、改善提案を提供します
license: MIT
---

# コード品質分析スキル

## 概要

このスキルはあなたが提供するコードを以下の観点から分析します：

- **可読性**: 変数名、関数名、コメント、構造化の質
- **パフォーマンス**: 非効率なアルゴリズム、無駄なループ、メモリ使用量
- **セキュリティ**: 潜在的な脆弱性、入力検証、認証・認可の問題
- **テスト可能性**: 単位テスト作成の容易さ、依存性注入の対応

## 使い方

1. VS Code でコードを選択
2. Copilot に「コード品質分析スキルを実行」と指示
3. 結果が統一フォーマットで表示されます

## パラメータ

### code_snippet (必須)
分析対象のコード（1～5000文字）

### language (必須)
プログラミング言語を指定
- `python`
- `javascript`  
- `typescript`
- `java`
- `go`

### focusAreas (オプション)
重点分析エリアをカンマ区切りで指定（複数選択可）
- `readability`
- `performance`
- `security`
- `testability`

デフォルト: すべてのエリアを分析

### detailLevel (オプション)
結果の詳細度レベル
- `basic`: 主要な問題のみ
- `detailed`: 詳細な分析と複数の改善提案

デフォルト: `detailed`

## 出力フォーマット

```json
{
  "overallScore": 85,
  "scoreRanges": {
    "readability": 90,
    "performance": 78,
    "security": 85,
    "testability": 82
  },
  "categories": [
    {
      "name": "Readability",
      "score": 90,
      "issues": [
        {
          "severity": "MEDIUM",
          "issue": "変数名 'x' は不明確",
          "suggestion": "変数を 'user_age' に改名",
          "example": "age = user.get_age()  # 変更前\nuser_age = user.get_age()  # 変更後"
        }
      ]
    },
    {
      "name": "Performance",
      "score": 78,
      "issues": [...]
    },
    {
      "name": "Security", 
      "score": 85,
      "issues": [...]
    },
    {
      "name": "Testability",
      "score": 82,
      "issues": [...]
    }
  ],
  "summary": "全体的に質の高いコードです...",
  "recommendations": [
    "型ヒントを追加してテスト容易性を向上させる",
    "ユーザー入力の検証をより厳密に..."
  ]
}
```

## 実装例

### Example 1: Python コード分析

入力:
```python
def process_data(data):
    for i in range(len(data)):
        x = data[i]
        # process x
        print(x * 2)
    return None
```

期待される出力:
```json
{
  "overallScore": 62,
  "categories": [
    {
      "name": "Readability",
      "score": 60,
      "issues": [
        {
          "severity": "HIGH",
          "issue": "関数名 'process_data' は曖昧",
          "suggestion": "動作を反映した名前に変更（例: convert_items_to_doubled, log_data_values）"
        },
        {
          "severity": "MEDIUM",
          "issue": "変数名 'x' は不適切",
          "suggestion": "'item', 'value', 'data_point' など意味のある名前を使用"
        }
      ]
    },
    {
      "name": "Performance",
      "score": 55,
      "issues": [
        {
          "severity": "HIGH",
          "issue": "for i in range(len(data)) はPython的でない",
          "suggestion": "enumerate() または直接イテレーション使用:\nfor item in data:\n    print(item * 2)"
        }
      ]
    },
    {
      "name": "Security",
      "score": 80,
      "issues": []
    },
    {
      "name": "Testability",
      "score": 70,
      "issues": [
        {
          "severity": "MEDIUM",
          "issue": "戻り値が常に None で結果を返していない",
          "suggestion": "処理結果を返すように修正して単位テスト可能にする"
        }
      ]
    }
  ],
  "recommendations": [
    "for ループを Pythonic に書き直す",
    "関数から結果を返す",
    "型ヒントを追加する",
    "docstring を追加する"
  ]
}
```

---

## JSON フォーマット（参考：内部管理向け）

⚠️ **注記**: 実装では SKILL.md フォーマット（上記）を使用してください。JSON形式はシステム内部管理向けの参考情報です。

### 参考：内部API形式

従来のJSON APIフォーマットは以下の様に構造化されていますが、新規実装では SKILL.md 形式を推奨します：

```json
{
  "id": "code-quality-analyzer",
  "name": "code-quality-analyzer",

```json
{
  "id": "analyze-code-quality",
  "version": "1.0.0",
  "name": "コード品質分析",
  "description": "Python, JavaScript, TypeScript, Java, Go コードの品質を多次元的に分析し、改善提案を提供するスキル",
  
  "metadata": {
    "author": "Development Productivity Team",
    "authorEmail": "devprod@example.com",
    "created": "2026-03-07",
    "lastUpdated": "2026-03-07",
    "category": "code-analysis",
    "subcategory": "quality",
    "tags": [
      "python",
      "javascript",
      "typescript",
      "java",
      "go",
      "code-quality",
      "code-review",
      "team-productivity"
    ],
    "documentation": "https://docs.example.com/skills/code-quality",
    "license": "MIT",
    "visibility": "public"
  },
  
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "分析対象のコード（最大5000文字）",
      "required": true,
      "minLength": 10,
      "maxLength": 5000,
      "example": "def calculate_sum(numbers):\n    result = 0\n    for n in numbers:\n        result = result + n\n    return result"
    },
    
    "language": {
      "type": "string",
      "description": "プログラミング言語",
      "required": true,
      "enum": [
        "python",
        "javascript",
        "typescript",
        "java",
        "go"
      ],
      "example": "python"
    },
    
    "focusAreas": {
      "type": "array",
      "description": "重点分析エリア。複数選択可能。すべて選択がデフォルト",
      "items": {
        "type": "string",
        "enum": [
          "readability",
          "performance",
          "security",
          "testability"
        ]
      },
      "minItems": 1,
      "maxItems": 4,
      "default": [
        "readability",
        "performance",
        "security",
        "testability"
      ],
      "example": [
        "readability",
        "security"
      ]
    },
    
    "detailLevel": {
      "type": "string",
      "description": "結果の詳細度",
      "enum": [
        "basic",
        "detailed",
        "comprehensive"
      ],
      "default": "detailed",
      "example": "detailed"
    },
    
    "maxIssues": {
      "type": "number",
      "description": "返却する最大指摘件数（スコアが高い順）",
      "minimum": 1,
      "maximum": 50,
      "default": 20,
      "example": 15
    }
  },
  
  "prompt": {
    "system": "You are an expert code reviewer with over 15 years of experience across multiple programming languages. Your task is to analyze code for quality issues in a professional, constructive manner. Provide actionable recommendations, not criticism. Always be specific about what needs improvement and why.",
    
    "template": "Analyze the following {language} code for quality issues.\n\nCode to analyze:\n```{language}\n{code_snippet}\n```\n\nAnalysis criteria:\n- Readability: Code clarity, naming conventions, comment quality\n- Performance: Efficiency, algorithmic complexity, unnecessary loops/operations\n- Security: Input validation, vulnerable patterns, data handling\n- Testability: Modularity, function size, separation of concerns\n\nFocus areas: {focusAreas|join(', ')}\nDetail level: {detailLevel}\nMaximum issues to report: {maxIssues}\n\nProvide your analysis in the following JSON format only (no markdown):\n{{\n  \"overallScore\": <number 0-100>,\n  \"categories\": [\n    {{\n      \"name\": <string>,\n      \"score\": <number 0-100>,\n      \"issues\": [<issue1>, <issue2>, ...],\n      \"severity\": [<HIGH|MEDIUM|LOW>, ...]\n    }}\n  ],\n  \"recommendations\": [<actionable suggestion 1>, ...],\n  \"codeSmells\": [<smell 1>, <smell 2>, ...],\n  \"positiveAspects\": [<positive 1>, <positive 2>, ...]\n}}",
    
    "variables": [
      {
        "name": "language",
        "type": "string",
        "source": "parameter"
      },
      {
        "name": "code_snippet",
        "type": "string",
        "source": "parameter"
      },
      {
        "name": "focusAreas",
        "type": "array",
        "source": "parameter",
        "processor": "join-comma"
      },
      {
        "name": "detailLevel",
        "type": "string",
        "source": "parameter"
      },
      {
        "name": "maxIssues",
        "type": "number",
        "source": "parameter"
      }
    ],
    
    "advancedOptions": {
      "temperature": 0.3,
      "topP": 0.9,
      "maxTokens": 2000
    }
  },
  
  "outputFormat": {
    "type": "json",
    
    "schema": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "title": "CodeQualityAnalysis",
      "description": "Comprehensive code quality analysis result",
      
      "properties": {
        "overallScore": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "Overall quality score (0=poor, 100=excellent)"
        },
        
        "categories": {
          "type": "array",
          "description": "Analysis results by category",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "enum": [
                  "readability",
                  "performance",
                  "security",
                  "testability"
                ],
                "description": "Category name"
              },
              "score": {
                "type": "number",
                "minimum": 0,
                "maximum": 100,
                "description": "Score for this category"
              },
              "issues": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "List of specific issues found"
              },
              "severity": {
                "type": "array",
                "items": {
                  "type": "string",
                  "enum": [
                    "HIGH",
                    "MEDIUM",
                    "LOW"
                  ]
                },
                "description": "Severity level of each issue"
              }
            },
            "required": [
              "name",
              "score",
              "issues",
              "severity"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "maxItems": 4
        },
        
        "recommendations": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Actionable recommendations for improvement",
          "maxItems": 50
        },
        
        "codeSmells": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Code smells or anti-patterns detected",
          "maxItems": 20
        },
        
        "positiveAspects": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Positive aspects of the code",
          "maxItems": 20
        }
      },
      
      "required": [
        "overallScore",
        "categories",
        "recommendations"
      ],
      
      "additionalProperties": false
    },
    
    "examples": [
      {
        "overallScore": 72,
        "categories": [
          {
            "name": "readability",
            "score": 80,
            "issues": [
              "Variable name 'x' is not descriptive"
            ],
            "severity": [
              "LOW"
            ]
          },
          {
            "name": "performance",
            "score": 65,
            "issues": [
              "Inefficient loop structure - consider using list comprehension"
            ],
            "severity": [
              "MEDIUM"
            ]
          },
          {
            "name": "security",
            "score": 75,
            "issues": [],
            "severity": []
          },
          {
            "name": "testability",
            "score": 70,
            "issues": [
              "Function is too large (over 20 lines)"
            ],
            "severity": [
              "MEDIUM"
            ]
          }
        ],
        "recommendations": [
          "Break down the function into smaller, more focused functions",
          "Use more descriptive variable names (e.g., 'count' instead of 'x')",
          "Add type hints for better IDE support and maintainability",
          "Add unit tests to cover edge cases"
        ],
        "codeSmells": [
          "Long function",
          "Vague variable naming",
          "Missing type hints"
        ],
        "positiveAspects": [
          "Good use of comments",
          "No obvious security vulnerabilities",
          "Logical flow is clear"
        ]
      }
    ]
  },
  
  "validation": {
    "timeout": 30,
    "maxRetries": 2,
    
    "retryStrategy": {
      "backoff": "exponential",
      "initialDelayMs": 1000,
      "maxDelayMs": 10000
    },
    
    "caching": {
      "enabled": true,
      "ttl": 3600,
      "keyStrategy": "md5-hash-of-inputs"
    },
    
    "rateLimit": {
      "requestsPerMinute": 30,
      "requestsPerHour": 1000,
      "requestsPerDay": 10000
    },
    
    "costControl": {
      "maxTokensPerRequest": 2000,
      "estimatedCostPerRequest": 0.015,
      "dailyBudget": 100
    }
  }
}
```

---

### 使用例

#### 例1: 基本的な使用方法

```json
リクエスト：
{
  "skill": "analyze-code-quality",
  "parameters": {
    "code_snippet": "def calculate(a, b):\n    return a + b",
    "language": "python"
  }
}

レスポンス（成功例）：
{
  "overallScore": 85,
  "categories": [
    {
      "name": "readability",
      "score": 90,
      "issues": [],
      "severity": []
    },
    {
      "name": "performance",
      "score": 90,
      "issues": [],
      "severity": []
    },
    {
      "name": "security",
      "score": 85,
      "issues": [
        "No input validation - consider adding type hints"
      ],
      "severity": ["LOW"]
    },
    {
      "name": "testability",
      "score": 75,
      "issues": [
        "No docstring to explain function behavior"
      ],
      "severity": ["LOW"]
    }
  ],
  "recommendations": [
    "Add type hints: def calculate(a: int, b: int) -> int:",
    "Add a docstring explaining what the function does"
  ],
  "codeSmells": ["Missing documentation"],
  "positiveAspects": ["Simple and clear", "No unnecessary complexity"]
}
```

#### 例2: 全オプション指定版

```json
リクエスト：
{
  "skill": "analyze-code-quality",
  "parameters": {
    "code_snippet": "for i in range(1000000):\n    for j in range(1000000):\n        x = i * j",
    "language": "python",
    "focusAreas": ["performance", "readability"],
    "detailLevel": "comprehensive",
    "maxIssues": 30
  }
}

レスポンス：
{
  "overallScore": 35,
  "categories": [
    {
      "name": "performance",
      "score": 20,
      "issues": [
        "Nested loop with O(n²) complexity - extremely inefficient",
        "Large iteration range (1 billion iterations) - will hang on most systems",
        "Unused computation result (x) - unnecessary CPU usage"
      ],
      "severity": ["HIGH", "HIGH", "MEDIUM"]
    },
    {
      "name": "readability",
      "score": 40,
      "issues": [
        "Variable name 'i', 'j', 'x' are not descriptive",
        "No comments explaining the purpose",
        "Magic numbers (1000000) should be extracted as constants"
      ],
      "severity": ["LOW", "MEDIUM", "MEDIUM"]
    }
  ],
  "recommendations": [
    "Use vectorized operations (NumPy) instead of nested loops",
    "If nested iteration is needed, consider using numpy.outer() or similar",
    "Move magic number to a named constant: MAX_ITERATIONS = 1000000",
    "Add meaningful variable names: outer_index, inner_index, product",
    "Consider if this computation is actually necessary"
  ],
  "codeSmells": [
    "Nested loops with high complexity",
    "Unused computation",
    "Magic numbers",
    "Vague naming"
  ],
  "positiveAspects": [
    "Code is syntactically valid"
  ]
}
```

---

### カスタマイズガイド

#### カスタマイズ1: 言語を追加

現在対応：Python, JavaScript, TypeScript, Java, Go
追加したい：C++, Rust, Go

```json
// スキル定義ファイルを修正

// 修正箇所1：parameterのenum
"language": {
  "enum": [
    "python",
    "javascript",
    "typescript",
    "java",
    "go",
    "cpp",           // ← 追加
    "rust",          // ← 追加
    "csharp"         // ← 追加
  ]
},

// 修正箇所2：promptのテンプレートを言語別に最適化
// （各言語のベストプラクティスに合わせて調整）
```

#### カスタマイズ2: 重点分析エリアを追加

現在：readability, performance, security, testability
追加したい：maintainability, documentation

```json
"focusAreas": {
  "items": {
    "enum": [
      "readability",
      "performance",
      "security",
      "testability",
      "maintainability",    // ← 追加
      "documentation"       // ← 追加
    ]
  }
},

// promptも修正：新しい分析基準を追加
```

#### カスタマイズ3: スコアの厳しさを調整

デフォルト：バランス型
企業要件：セキュリティを最重視

```json
// prompt のテンプレートに重み付けを追加

"Security is your TOP PRIORITY. 
If ANY security issue is found, score must be ≤ 50.
Apply strict scrutiny to input validation, authentication, data handling.
"
```

#### カスタマイズ4: 出力フォーマットを簡潔に

デフォルト：詳細な JSON
シンプル版：最小限の情報のみ

```json
// outputFormat.schema を簡略化

// シンプル版の出力例：
{
  "overallScore": 75,
  "topIssues": ["Variable naming", "Add type hints"],
  "summary": "Good code structure, add type hints for better maintainability"
}
```

---

### トラブルシューティング

#### 問題1: タイムアウトが頻繁に発生

**原因：** 入力コードが大きすぎる
**解決策：**

```json
// Option A: maxLength を減らす
"code_snippet": {
  "maxLength": 2000  // 5000から2000に削減
},

// Option B: timeout を増やす
"timeout": 60  // 30から60秒に増加
```

#### 問題2: 出力フォーマットが毎回異なる

**原因：** プロンプトテンプレートの指示が曖昧
**解決策：**

```json
// より詳細な出力フォーマット指定
"Respond ONLY with valid JSON. No markdown, no text before or after JSON.
Your output must match this exact structure:
{
  \"overallScore\": <number>,
  \"categories\": [...]
}
"
```

#### 問題3: セキュリティ指摘が不足

**原因：** システムプロンプトが弱い
**解決策：**

```json
"system": "You are a SECURITY EXPERT code reviewer. 
Your primary focus is identifying security vulnerabilities and risks.
Check for: SQL injection, XSS, authentication bypasses, 
data exposure, input validation gaps, and insecure patterns.
Flag even subtle security risks.
"
```

---

### テストケース

#### テストケース1: 正常系

```bash
入力：
{
  "code_snippet": "def hello():\n    print('hello')",
  "language": "python"
}

期待される出力：
✓ overallScore が 0-100 の数値
✓ categories に readability, performance, security, testability が含まれる
✓ 各カテゴリに score (0-100), issues (配列), severity (配列) がある
✓ recommendations が配列
```

#### テストケース2: セキュリティ問題

```bash
入力：
{
  "code_snippet": "query = \"SELECT * FROM users WHERE id=\" + user_input",
  "language": "python"
}

期待される結果：
✓ security スコアが低い（< 50）
✓ "SQL injection" または "user_input" に関する指摘がある
✓ severity に HIGH が含まれる
```

#### テストケース3: 最大サイズ

```bash
入力：5000文字のコード

期待される結果：
✓ タイムアウトしない（30秒以内）
✓ スキーマに準拠した出力
```

---

### 実装チェックリスト

```
□ スキル定義ファイルが有効な JSON か確認
□ すべてのパラメータが定義されているか確認
□ 出力スキーマの例が実際の出力と一致するか検証
□ 複数の言語でテストを実行
□ エッジケース（大型コード、エラーコード等）をテスト
□ ドキュメント（README）が完成している
□ チーム内で試験運用したか
□ ユーザーフィードバックを収集したか
□ リポジトリに登録、タグを付与
```

---

### 次へ進む

→ [Part 3-4: サンプルスキル #2 - ドキュメント生成](#section-03-implementation-04-sample-doc-generation)

## Part 3-4: サンプルスキル #2 - ドキュメント自動生成 {#section-03-implementation-04-sample-doc-generation}


このセクションでは、**コード内のDocstring を自動生成するスキル** を SKILL.md フォーマットで実装します。

難度は Part 3-3 より少し高く、複数の出力フォーマット対応です。

---

### スキル概要

```
スキル名：generate-documentation
目的：関数・クラスのドキュメント（docstring）を自動生成
難度：★★★☆☆（中級）
実装時間：1～1.5時間
対応言語：Python, JavaScript/TypeScript, Java, Go
対応フォーマット：Google Style, NumPy Style, JSDoc, JavaDoc
推奨形式：SKILL.md
```

---

### SKILL.md フォーマット（推奨）

#### ファイル：`.github/skills/doc-generator/SKILL.md`

```markdown
---
name: doc-generator
description: 関数・メソッド・クラスの Docstring を複数形式で自動生成します
license: MIT
---

# ドキュメント自動生成スキル

## 概要

このスキルは以下の種類のドキュメント（Docstring）を自動生成します：

- **Google Style**: Python で一般的
- **NumPy Style**: 科学計算向け
- **JSDoc**: JavaScript/TypeScript 向け
- **JavaDoc**: Java 向け
- **Go Doc**: Go 向け

生成されるドキュメントは：
- 関数の目的を明確に説明
- パラメータの型と説明を記載
- 戻り値の説明
- 使用例（オプション）
- 例外情報（該当時）

## 使い方

1. 関数またはクラスを選択
2. Copilot に「ドキュメント自動生成スキルを実行」と指示
3. 選択したドキュメント形式で Docstring が生成されます

## パラメータ

### codeSnippet (必須)
ドキュメント対象のコード（関数またはクラス）
- 5～500 行

### language (必須)
ソースコード言語
- `python`
- `javascript`
- `typescript`
- `java`
- `go`

### docStyle (必須)
ドキュメント形式
- `google`: Google 形式（Python 推奨）
- `numpy`: NumPy 形式（科学計算向け）
- `jsdoc`: JSDoc 形式（JavaScript/TypeScript）
- `javadoc`: JavaDoc 形式（Java）
- `godoc`: Go Doc 形式（Go）

### includeExamples (オプション)
使用例を含めるか
- `true`: 含める（詳細）
- `false`: 含めない（簡潔）

デフォルト: `true`

### includeTypeHints (オプション)
型ヒント情報を含めるか
- `true`: 含める
- `false`: 含めない

デフォルト: `true`

## 出力フォーマット

```json
{
  "generatedDocstring": "...",
  "format": "google|numpy|jsdoc|javadoc|godoc",
  "language": "...",
  "insertionPoint": {
    "lineNumber": 5,
    "position": "above|inside"
  },
  "estimatedReadabilityIncrease": 0.25,
  "suggestions": [
    "より詳細な説明を追加できます",
    "例外処理について記載することをお勧めします"
  ]
}
```

## 実装例

### Example 1: Python 関数（Google Style）

入力コード:
```python
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)
```

生成される Docstring:
```python
def calculate_average(numbers):
    """
    数値リストの平均値を計算します。
    
    Args:
        numbers (list): 数値のリスト。最低でも1つの要素が必要です。
        
    Returns:
        float: 計算された平均値。
        
    Raises:
        ValueError: リストが空の場合。
        TypeError: 数値以外の値がリストに含まれている場合。
        
    Examples:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
        >>> calculate_average([10, 20])
        15.0
    """
    if not numbers:
        raise ValueError("リストは空にできません")
    total = sum(numbers)
    return total / len(numbers)
```

### Example 2: TypeScript クラス（JSDoc）

入力コード:
```typescript
class UserService {
    constructor(database) {
        this.database = database;
    }
    
    async getUserById(id) {
        return this.database.query('users', id);
    }
}
```

生成される JSDoc:
```typescript
/**
 * ユーザー情報を管理するサービスクラス
 * @class UserService
 */
class UserService {
    /**
     * UserService を初期化します
     * @param {Database} database - データベースインスタンス
     */
    constructor(database) {
        this.database = database;
    }
    
    /**
     * ID でユーザーを取得します
     * @async
     * @param {string} id - ユーザー ID
     * @returns {Promise<User>} ユーザーオブジェクト
     * @throws {Error} ユーザーが見つからない場合
     * @example
     * const user = await userService.getUserById('user123');
     */
    async getUserById(id) {
        return this.database.query('users', id);
    }
}
```

---

## JSON フォーマット（参考：内部管理向け）

```json
{
  "id": "generate-documentation",
  "version": "1.0.0",
  "name": "ドキュメント自動生成",
  "description": "関数・メソッド・クラスのドキュメンテーション（docstring）を自動生成するスキル。複数のドキュメンテーションスタイル（Google, NumPy, JSDoc等）に対応。",
  
  "metadata": {
    "author": "Documentation Engineers",
    "authorEmail": "docs@example.com",
    "created": "2026-03-07",
    "lastUpdated": "2026-03-07",
    "category": "documentation",
    "subcategory": "code-documentation",
    "tags": [
      "documentation",
      "docstring",
      "python",
      "javascript",
      "typescript",
      "java",
      "go",
      "productivity"
    ],
    "documentation": "https://docs.example.com/skills/generate-documentation",
    "license": "MIT"
  },
  
  "parameters": {
    "code_element": {
      "type": "string",
      "description": "ドキュメント化する関数・メソッド・クラスの定義（署名を含む）",
      "required": true,
      "minLength": 20,
      "maxLength": 3000,
      "example": "def calculate_fibonacci(n: int, memo: dict = None) -> int:"
    },
    
    "language": {
      "type": "string",
      "description": "プログラミング言語",
      "required": true,
      "enum": [
        "python",
        "javascript",
        "typescript",
        "java",
        "go"
      ],
      "example": "python"
    },
    
    "docstyle": {
      "type": "string",
      "description": "ドキュメンテーションスタイル（言語に応じて自動選択されます）",
      "enum": [
        "google",
        "numpy",
        "sphinx",
        "jsdoc",
        "javadoc",
        "godoc"
      ],
      "default": "google",
      "example": "google"
    },
    
    "includeSummary": {
      "type": "boolean",
      "description": "1行概要を含める",
      "default": true
    },
    
    "includeArgs": {
      "type": "boolean",
      "description": "引数の説明を含める",
      "default": true
    },
    
    "includeReturns": {
      "type": "boolean",
      "description": "戻り値の説明を含める",
      "default": true
    },
    
    "includeRaises": {
      "type": "boolean",
      "description": "発生する例外の説明を含める",
      "default": true
    },
    
    "includeExamples": {
      "type": "boolean",
      "description": "使用例を含める",
      "default": true
    },
    
    "detailLevel": {
      "type": "string",
      "description": "ドキュメントの詳細度",
      "enum": [
        "brief",
        "standard",
        "detailed"
      ],
      "default": "standard"
    }
  },
  
  "prompt": {
    "system": "You are an expert technical documentation writer with extensive experience in API documentation, code documentation, and developer experience. Your documentation should be clear, concise, professional, and immediately useful to developers. Always include practical information and avoid vague descriptions.",
    
    "template": "Generate professional documentation for the following {language} code element.\n\nCode element:\n{code_element}\n\nDocumentation style: {docstyle}\nDetail level: {detailLevel}\n\nInclude:\n{includeSection_summary}{includeSection_args}{includeSection_returns}{includeSection_raises}{includeSection_examples}\n\nRequirements:\n1. Use ONLY the specified documentation style ({docstyle})\n2. Make the documentation precise and immediately useful\n3. Include type hints where applicable\n4. Use professional, clear language\n5. Avoid redundancy\n6. Return ONLY the documentation block without any code before/after\n\nReturn the complete documentation block in the appropriate format:",
    
    "advancedOptions": {
      "temperature": 0.2,
      "topP": 0.9,
      "maxTokens": 1500
    }
  },
  
  "outputFormat": {
    "type": "text",
    
    "schema": {
      "type": "object",
      "properties": {
        "documentation": {
          "type": "string",
          "description": "The generated documentation block (docstring/comment)"
        },
        "language": {
          "type": "string",
          "description": "The programming language"
        },
        "style": {
          "type": "string",
          "description": "Documentation style used"
        },
        "sections": {
          "type": "object",
          "properties": {
            "summary": { "type": "string" },
            "args": { "type": "array", "items": { "type": "string" } },
            "returns": { "type": "string" },
            "raises": { "type": "array", "items": { "type": "string" } },
            "examples": { "type": "string" }
          }
        }
      },
      "required": [
        "documentation",
        "language",
        "style"
      ]
    }
  },
  
  "validation": {
    "timeout": 25,
    "maxRetries": 2,
    "caching": {
      "enabled": true,
      "ttl": 7200
    },
    "rateLimit": {
      "requestsPerMinute": 40,
      "requestsPerHour": 1200
    },
    "costControl": {
      "maxTokensPerRequest": 1500,
      "estimatedCostPerRequest": 0.012
    }
  }
}
```

---

## 拡張テンプレート変数の生成

スキル内で動的に生成される変数：

```python
# スキル内部で生成される補助変数

# includeSection_summary
if includeSummary:
    includeSection_summary = "- Summary/Description: A brief 1-3 sentence description"
else:
    includeSection_summary = ""

# includeSection_args
if includeArgs:
    includeSection_args = "- Arguments/Parameters: Description of each argument with types"
else:
    includeSection_args = ""

# ... 同様に他のセクションも生成
```

---

## 使用例

### 例1: Python 関数のドキュメント（Google Style）

```json
リクエスト：
{
  "skill": "generate-documentation",
  "parameters": {
    "code_element": "def calculate_factorial(n: int) -> int:",
    "language": "python",
    "docstyle": "google",
    "detailLevel": "standard"
  }
}

レスポンス：
{
  "documentation": "\"\"\"Calculate the factorial of a non-negative integer.\n\n    Args:\n        n: A non-negative integer.\n\n    Returns:\n        The factorial of n.\n\n    Raises:\n        ValueError: If n is negative.\n\n    Examples:\n        >>> calculate_factorial(5)\n        120\n        >>> calculate_factorial(0)\n        1\n    \"\"\"",
  "language": "python",
  "style": "google",
  "sections": {
    "summary": "Calculate the factorial of a non-negative integer.",
    "args": ["n: A non-negative integer."],
    "returns": "The factorial of n.",
    "raises": ["ValueError: If n is negative."],
    "examples": ">>> calculate_factorial(5)\n120\n>>> calculate_factorial(0)\n1"
  }
}
```

### 例2: JavaScript 関数のドキュメント（JSDoc）

```json
リクエスト：
{
  "skill": "generate-documentation",
  "parameters": {
    "code_element": "async function fetchUserData(userId, options = {}) {",
    "language": "javascript",
    "docstyle": "jsdoc",
    "detailLevel": "detailed",
    "includeExamples": true
  }
}

レスポンス：
{
  "documentation": "/**\n * Fetches user data from the server asynchronously.\n * Retrieves comprehensive user information including profile, preferences, and settings.\n *\n * @async\n * @function fetchUserData\n * @param {number} userId - The unique identifier of the user to fetch\n * @param {Object} [options={}] - Optional configuration object\n * @param {boolean} [options.includePreferences=false] - Whether to include user preferences\n * @param {boolean} [options.includeSettings=false] - Whether to include user settings\n * @param {number} [options.timeout=5000] - Request timeout in milliseconds\n *\n * @returns {Promise<Object>} A promise that resolves to an object containing:\n *   - {number} id - User ID\n *   - {string} name - User's full name\n *   - {string} email - User's email address\n *   - {Object} [preferences] - User preferences (if requested)\n *   - {Object} [settings] - User settings (if requested)\n *\n * @throws {Error} If userId is not a valid number\n * @throws {NetworkError} If the network request fails\n * @throws {TimeoutError} If the request exceeds the timeout duration\n *\n * @example\n * // Basic usage\n * const user = await fetchUserData(123);\n * console.log(user.name);\n *\n * @example\n * // With options\n * const user = await fetchUserData(123, {\n *   includePreferences: true,\n *   timeout: 10000\n * });\n */",
  "language": "javascript",
  "style": "jsdoc"
}
```

### 例3: Java クラスのドキュメント（JavaDoc）

```json
リクエスト：
{
  "skill": "generate-documentation",
  "parameters": {
    "code_element": "public class UserAuthenticationService {",
    "language": "java",
    "docstyle": "javadoc",
    "detailLevel": "detailed"
  }
}

レスポンス：
{
  "documentation": "/**\n * Service class for handling user authentication and authorization.\n * \n * This class provides methods for user login, token validation, and permission checking.\n * It handles both basic authentication and OAuth2 flows.\n * \n * <p>Thread-safe and designed for use in concurrent environments.\n * \n * @author Development Team\n * @version 1.0\n * @since 2026-03-07\n * \n * @see AuthToken\n * @see UserRepository\n * @see PermissionChecker\n * \n * @example\n * UserAuthenticationService authService = new UserAuthenticationService();\n * AuthToken token = authService.authenticate(username, password);\n * if (authService.isTokenValid(token)) {\n *     // Proceed with authenticated request\n * }\n */",
  "language": "java",
  "style": "javadoc"
}
```

---

## カスタマイズガイド

### カスタマイズ1: スタイルガイドの詳細化

```json
// prompt のテンプレートを言語・スタイル別に最適化

for Python + Google Style:
"Follow Google's Python style guide for docstrings:
- Use triple double quotes
- Start with a summary line ending with period
- Use Args:, Returns:, Raises:, Examples: sections
- Type hints in the function signature, not in docstring"

for JavaScript + JSDoc:
"Follow JSDoc 3 standards:
- Use /** */ format
- Use @param, @returns, @throws, @example tags
- Include type information in curly braces {type}
- Use @async tag for async functions"
```

### カスタマイズ2: エクスポート フォーマット

```json
// レスポンス形式をカスタマイズ

// Option 1: ドキュメント文字列のみ（シンプル）
{
  "documentation": "\"\"\"...\"\"\""
}

// Option 2: セクション分割（詳細）
{
  "documentation": "\"\"\"...\"\"\""
  "sections": {
    "summary": "...",
    "args": [...],
    "returns": "..."
  }
}

// Option 3: 埋め込みコード形式（実装例）
{
  "code_with_documentation": "def func():\n    \"\"\"...\"\"\"\n    pass"
}
```

### カスタマイズ3:言語別ドキュメント生成

言語によって自動でスタイルを選択：

```json
language_style_mapping: {
  "python": ["google", "numpy", "sphinx"],
  "javascript": ["jsdoc"],
  "typescript": ["jsdoc"],
  "java": ["javadoc"],
  "go": ["godoc"]
}
```

---

## 実装技法： includeSection 変数の出力

```
こちらはサーバーサイドで実装される機能のため、
スキル定義ファイルには含まれませんが、
実装時は以下のロジックが必要です：

テンプレート変数の動的生成：

def generate_prompt(parameters):
    include_sections = []
    
    if parameters['includeSummary']:
        include_sections.append("- Summary/Description")
    
    if parameters['includeArgs']:
        include_sections.append("- Arguments/Parameters")
    
    if parameters['includeReturns']:
        include_sections.append("- Return value/type")
    
    if parameters['includeRaises']:
        include_sections.append("- Exceptions/Errors")
    
    if parameters['includeExamples']:
        include_sections.append("- Usage examples")
    
    sections_text = "\n".join(include_sections)
    
    # テンプレート内の {includeSection_*} を置換
    template = template.replace("{includeSection_text}", sections_text)
    
    return template
```

---

## トラブルシューティング

### 問題1: ドキュメンテーションスタイルが混在

**症状：** Google Style を指定したはずなのに、他のスタイルが混在している

**原因：** プロンプトの指示が不明確

**修正：**

```json
"prompt": {
  "template": "...IMPORTANT: Use ONLY {docstyle} style. No other styles. If docstyle is 'google', use ONLY Google style docstring format. If 'jsdoc', use ONLY JSDoc format..."
}
```

### 問題2: 型情報が不正確

**症状：** 戻り値の型が `Any` や曖昧な説明になっている

**原因：** 入力コードに型ヒントがない

**修正：**

```json
"code_element": "def process(data: dict, timeout: int = 30) -> Optional[Result]:",
// 型ヒントを含めることで、より正確なドキュメント生成が可能
```

### 問題3: 生成が遅い

**症状：** detailLevel を "detailed" にするとタイムアウトが頻繁に発生

**修正：**

```json
"validation": {
  "timeout": 35,  // 25から35に増加
  "maxTokens": 2000  // トークン上限を増加
}
```

---

## テストケース

### テストケース1: 単純な関数（Python）

```bash
入力：
{
  "code_element": "def add(a, b):",
  "language": "python",
  "docstyle": "google"
}

期待される出力：
✓ triple double quotes で囲まれている
✓ Args: セクションを含む
✓ Returns: セクションを含む
✓ 言語は "python"
```

### テストケース2: 複雑なクラス（Java）

```bash
入力：
{
  "code_element": "public class DatabaseConnection implements AutoCloseable {",
  "language": "java",
  "docstyle": "javadoc",
  "detailLevel": "detailed"
}

期待される出力：
✓ JavaDoc 形式（/** */ で囲まれた）
✓ @since, @author タグを含む
✓ @see タグで関連クラスを参照している
```

### テストケース3: モダンな JavaScript（JSDoc）

```bash
入力：
{
  "code_element": "async function* streamData(url, options = {}) {",
  "language": "javascript",
  "docstyle": "jsdoc"
}

期待される出力：
✓ @async タグを含む
✓ @generator または @yields タグを含む
✓ @param で options オブジェクトを説明している
```

---

## 実装チェックリスト

```
□ スキル定義ファイルが有効な JSON か確認
□ すべての docstyle（google, numpy, jsdoc等）でテスト
□ 複数の言語でテスト
□ detailLevel（brief, standard, detailed）でそれぞれテスト
□ includeSummary, includeArgs等の boolean オプションでテスト
□ 複雑なシグネチャ（デフォルト値、可変長引数等）をテスト
□ ジェネリック型（Java の List<String> など）に対応しているか確認
□ 非同期関数（async/await）に正しくタグを付けているか確認
□ ドキュメント出力がコードに貼り付け可能か確認
□ リポジトリに登録、ドキュメント完備
```

---

## 実装のバリエーション

### マルチステップワークフロー：コード + ドキュメント生成

このスキルと Part 3-3 のコード品質分析スキルを組み合わせ：

```
ワークフロー：
1. code-quality-analyze スキルで品質分析
2. 出力から改善提案を抽出
3. コードを改善（ユーザーが実施）
4. generate-documentation スキルで改善後のコードをドキュメント化

結果：
- 品質が良く
- 十分にドキュメント化されたコード
```

---

## 次へ進む

→ [Part 3-5: サンプルスキル #3 - テスト生成](05-sample-test-generation.md)

テスト生成スキルは、さらに複雑で実用的な例として、
複数の出力ファイル、複数のテストフレームワーク対応を示します。

## Part 3-5: サンプルスキル #3 - テスト生成【応用的なスキル】 {#section-03-implementation-05-sample-test-generation}


このセクションでは、**関数・メソッドのユニットテストコードを自動生成するスキル** を SKILL.md フォーマットで実装します。

難度は最も高く、複数のテストフレームワーク対応、複数ケース生成を含みます。

---

### スキル概要

```
スキル名：generate-unit-tests
目的：ユニットテストコードを自動生成
難度：★★★★☆（上級）
実装時間：1～2時間
対応言語：Python, JavaScript/TypeScript, Java, Go
対応フレームワーク：pytest, unittest, Jest, Mocha, JUnit, Go testing
特徴：正常系・異常系・エッジケースをカバー
推奨形式：SKILL.md
```

---

### SKILL.md フォーマット（推奨）

#### ファイル：`.github/skills/test-generator/SKILL.md`

```markdown
---
name: test-generator
description: 関数・メソッドのユニットテストコードを複数のテストフレームワーク形式で自動生成します
license: MIT
---

# ユニットテスト自動生成スキル

## 概要

このスキルは以下のテスト種別をカバーしたユニットテストを自動生成します：

- **正常系テスト**: 期待される入力に対する結果の検証
- **境界値テスト**: 最小値・最大値・境界条件の検証
- **異常系テスト**: エラーハンドリング、例外発生の検証
- **エッジケーステスト**: null、空配列など特殊な入力の検証

対応するテストフレームワーク：
- **Python**: pytest、unittest
- **JavaScript/TypeScript**: Jest、Mocha + Chai
- **Java**: JUnit 4/5
- **Go**: Go testing

## 使い方

1. 関数またはメソッド定義を選択
2. Copilot に「ユニットテスト自動生成スキルを実行」と指示
3. テストコードが選択したフレームワーク形式で生成されます

## パラメータ

### codeSnippet (必須)
テスト対象のコード（関数またはクラスメソッド）
- 5～200 行まで対応

### language (必須)
ソースコード言語
- `python`
- `javascript`
- `typescript`
- `java`
- `go`

### testFramework (必須)
使用するテストフレームワーク
- Python: `pytest` / `unittest`
- JS/TS: `jest` / `mocha`
- Java: `junit4` / `junit5`
- Go: `testing`

### coverageTarget (オプション)
テストカバレッジ目標（%）
- デフォルト: `80`
- 範囲: 50～100

### includeDocumentation (オプション)
テストコード内にコメント・説明を含めるか
- `true`: 含める（学習向け）
- `false`: 含めない（本番向け）

デフォルト: `true`

## 出力フォーマット

```json
{
  "testCode": "...",
  "framework": "pytest|jest|junit|testing",
  "language": "...",
  "testCases": [
    {
      "name": "test_normal_case_1",
      "type": "normal|boundary|error|edge",
      "description": "..." 
    }
  ],
  "estimatedCoverage": 0.85,
  "runInstructions": "pytest test_function.py -v",
  "suggestions": [
    "統合テストの追加を検討してください",
    "パフォーマンステストの追加をお勧めします"
  ]
}
```

## 実装例

### Example 1: Python 関数（pytest）

入力コード:
```python
def divide(a, b):
    if b == 0:
        raise ValueError("0で除算することはできません")
    return a / b
```

生成されるテストコード:
```python
import pytest
from math_utils import divide

class TestDivide:
    """divide 関数のテストスイート"""
    
    def test_normal_case_positive_numbers(self):
        """正常系: 正の数同士の除算"""
        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5
    
    def test_normal_case_negative_numbers(self):
        """正常系: 負の数を含む除算"""
        assert divide(-10, 2) == -5.0
        assert divide(10, -2) == -5.0
        assert divide(-10, -2) == 5.0
    
    def test_boundary_case_zero_numerator(self):
        """境界値: 分子が 0"""
        assert divide(0, 5) == 0.0
    
    def test_boundary_case_small_denominator(self):
        """境界値: 分母が 1"""
        assert divide(42, 1) == 42.0
    
    def test_error_case_zero_denominator(self):
        """異常系: 分母が 0（例外発生）"""
        with pytest.raises(ValueError):
            divide(10, 0)
    
    def test_error_case_invalid_type_numerator(self):
        """異常系: 分子が数値でない"""
        with pytest.raises(TypeError):
            divide("10", 2)
    
    def test_edge_case_float_division(self):
        """エッジケース: 浮動小数点演算"""
        result = divide(1, 3)
        assert abs(result - 0.333333) < 0.0001
```

### Example 2: JavaScript 関数（Jest）

入力コード:
```javascript
function fetchUserData(userId) {
    if (!userId) {
        throw new Error("User ID is required");
    }
    return api.get(`/users/${userId}`);
}
```

生成されるテストコード:
```javascript
import { fetchUserData } from './userService';
import * as api from './api';

jest.mock('./api');

describe('fetchUserData', () => {
    afterEach(() => {
        jest.clearAllMocks();
    });
    
    test('正常系: 有効なユーザーIDでデータを取得', async () => {
        const userData = { id: '123', name: 'John Doe' };
        api.get.mockResolvedValue(userData);
        
        const result = await fetchUserData('123');
        
        expect(result).toEqual(userData);
        expect(api.get).toHaveBeenCalledWith('/users/123');
    });
    
    test('異常系: ユーザーID未指定で例外発生', () => {
        expect(() => fetchUserData(null)).toThrow('User ID is required');
        expect(() => fetchUserData('')).toThrow('User ID is required');
    });
    
    test('異常系: API呼び出し失敗時のエラーハンドリング', async () => {
        api.get.mockRejectedValue(new Error('API Error'));
        
        await expect(fetchUserData('123')).rejects.toThrow('API Error');
    });
    
    test('境界値: 最小限のユーザーIDでリクエスト', async () => {
        api.get.mockResolvedValue({});
        
        await fetchUserData('a');
        
        expect(api.get).toHaveBeenCalledWith('/users/a');
    });
});
```

---

## JSON フォーマット（参考：内部管理向け）

```json
{
  "id": "generate-unit-tests",
  "version": "1.0.0",
  "name": "ユニットテスト自動生成",
  "description": "関数・メソッドのユニットテストコードを自動生成するスキル。複数のテストフレームワークに対応し、正常系・異常系・エッジケースを包括的にカバーしたテストを生成します。",
  
  "metadata": {
    "author": "QA/Testing Team",
    "authorEmail": "qa@example.com",
    "created": "2026-03-07",
    "lastUpdated": "2026-03-07",
    "category": "testing",
    "subcategory": "unit-testing",
    "tags": [
      "testing",
      "unit-test",
      "pytest",
      "jest",
      "junit",
      "python",
      "javascript",
      "typescript",
      "java",
      "go"
    ],
    "documentation": "https://docs.example.com/skills/generate-unit-tests",
    "license": "MIT"
  },
  
  "parameters": {
    "function_signature": {
      "type": "string",
      "description": "テスト対象の関数・メソッドの完全なシグネチャと通常は関数本体を含む（またはシグネチャのみでも可）",
      "required": true,
      "minLength": 20,
      "maxLength": 5000,
      "example": "def merge_sorted_lists(list1: List[int], list2: List[int]) -> List[int]:"
    },
    
    "language": {
      "type": "string",
      "description": "プログラミング言語",
      "required": true,
      "enum": [
        "python",
        "javascript",
        "typescript",
        "java",
        "go"
      ]
    },
    
    "testFramework": {
      "type": "string",
      "description": "テストフレームワーク（言語に応じて選択）",
      "enum": [
        "pytest",
        "unittest",
        "jest",
        "mocha",
        "chai",
        "junit",
        "testng",
        "gotest"
      ],
      "default": "pytest"
    },
    
    "coverage": {
      "type": "string",
      "description": "テストカバレッジレベル",
      "enum": [
        "basic",
        "standard",
        "comprehensive"
      ],
      "default": "standard",
      "example": "comprehensive"
    },
    
    "includeNormalCases": {
      "type": "boolean",
      "description": "正常系テストを含める",
      "default": true
    },
    
    "includeEdgeCases": {
      "type": "boolean",
      "description": "エッジケーステストを含める",
      "default": true
    },
    
    "includeErrorCases": {
      "type": "boolean",
      "description": "エラーケース・例外テストを含める",
      "default": true
    },
    
    "mockExternalDependencies": {
      "type": "boolean",
      "description": "外部依存関係をモックする",
      "default": true
    },
    
    "includePerformanceTests": {
      "type": "boolean",
      "description": "パフォーマンステストを含める（オプション）",
      "default": false
    }
  },
  
  "prompt": {
    "system": "You are an expert quality assurance engineer and test architect. Your task is to generate comprehensive, professional unit tests that cover normal cases, edge cases, and error scenarios. Tests should be clear, maintainable, and follow industry best practices. Use appropriate assertions and test structures for the specified framework.",
    
    "template": "Generate professional unit tests for the following {language} function.\n\nFunction to test:\n{function_signature}\n\nTest framework: {testFramework}\nCoverage level: {coverage}\n\nInclude:\n{coverageInstructions}\n\nRequirements:\n1. Generate {coverage} coverage tests\n2. Follow {testFramework} conventions and best practices\n3. Use descriptive test names (test_<scenario> format)\n4. Include setup/teardown if needed\n5. Add comments explaining complex test logic\n6. Group related tests in test classes/suites\n7. Use appropriate assertions for {language}\n{mockingInstructions}\n\n{coverageDetails}\n\nGenerate the complete test file content in {language} syntax:",
    
    "advancedOptions": {
      "temperature": 0.3,
      "topP": 0.9,
      "maxTokens": 3000
    }
  },
  
  "outputFormat": {
    "type": "object",
    
    "schema": {
      "type": "object",
      "properties": {
        "test_code": {
          "type": "string",
          "description": "The generated test code (complete and runnable)"
        },
        "language": {
          "type": "string",
          "description": "Programming language"
        },
        "framework": {
          "type": "string",
          "description": "Test framework used"
        },
        "test_cases": {
          "type": "array",
          "description": "List of generated test cases",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "Test case name"
              },
              "type": {
                "type": "string",
                "enum": ["normal", "edge_case", "error_case", "performance"],
                "description": "Type of test"
              },
              "description": {
                "type": "string",
                "description": "What this test validates"
              }
            }
          }
        },
        "imports": {
          "type": "array",
          "description": "Required imports/dependencies",
          "items": { "type": "string" }
        },
        "setup_instructions": {
          "type": "string",
          "description": "Setup instructions (dependencies, configs, etc.)"
        },
        "run_instructions": {
          "type": "string",
          "description": "How to run the tests"
        }
      },
      "required": [
        "test_code",
        "language",
        "framework"
      ]
    },
    
    "examples": [
      {
        "test_code": "import pytest\nfrom typing import List\n\n\nclass TestMergeSortedLists:\n    \"\"\"Test suite for merge_sorted_lists function.\"\"\"\n    \n    # Normal cases\n    def test_merge_two_non_empty_lists(self):\n        \"\"\"Test merging two non-empty sorted lists.\"\"\"\n        result = merge_sorted_lists([1, 3, 5], [2, 4, 6])\n        assert result == [1, 2, 3, 4, 5, 6]\n    \n    # Edge cases\n    def test_merge_with_empty_first_list(self):\n        \"\"\"Test merging when first list is empty.\"\"\"\n        result = merge_sorted_lists([], [1, 2, 3])\n        assert result == [1, 2, 3]\n    \n    def test_merge_with_empty_second_list(self):\n        \"\"\"Test merging when second list is empty.\"\"\"\n        result = merge_sorted_lists([1, 2, 3], [])\n        assert result == [1, 2, 3]\n    \n    def test_merge_both_empty_lists(self):\n        \"\"\"Test merging two empty lists.\"\"\"\n        result = merge_sorted_lists([], [])\n        assert result == []\n    \n    # Error cases\n    def test_merge_with_unsorted_input(self):\n        \"\"\"Test behavior with unsorted input lists.\"\"\"\n        # Should still produce sorted result if function handles it\n        result = merge_sorted_lists([3, 1], [4, 2])\n        # Verify result is sorted\n        assert result == sorted(result)",
        "language": "python",
        "framework": "pytest",
        "test_cases": [
          {
            "name": "test_merge_two_non_empty_lists",
            "type": "normal",
            "description": "Merge two non-empty sorted lists"
          },
          {
            "name": "test_merge_with_empty_first_list",
            "type": "edge_case",
            "description": "Handle empty first list"
          },
          {
            "name": "test_merge_with_empty_second_list",
            "type": "edge_case",
            "description": "Handle empty second list"
          },
          {
            "name": "test_merge_both_empty_lists",
            "type": "edge_case",
            "description": "Handle both lists empty"
          },
          {
            "name": "test_merge_with_unsorted_input",
            "type": "error_case",
            "description": "Handle unsorted input"
          }
        ],
        "imports": [
          "pytest",
          "from typing import List"
        ],
        "run_instructions": "Run with: pytest test_merge_sorted_lists.py -v"
      }
    ]
  },
  
  "validation": {
    "timeout": 40,
    "maxRetries": 2,
    "caching": {
      "enabled": true,
      "ttl": 7200
    },
    "rateLimit": {
      "requestsPerMinute": 20,
      "requestsPerHour": 600
    },
    "costControl": {
      "maxTokensPerRequest": 3000,
      "estimatedCostPerRequest": 0.025
    }
  }
}
```

---

## 補助説明テンプレート変数

スキル内部で生成される動的な説明文：

```python
def generate_coverage_instructions(coverage_level):
    if coverage_level == "basic":
        return "- Happy path (normal operation)\n- At least 1 edge case\n- Essential error cases"
    elif coverage_level == "standard":
        return "- Multiple normal scenario paths\n- All edge cases (empty, null, boundary values)\n- All specified error conditions"
    elif coverage_level == "comprehensive":
        return "- All normal scenario variations\n- All edge cases and boundary conditions\n- All error types and recovery paths\n- Integration with related functions if applicable"

def generate_mocking_instructions(mock_enabled):
    if mock_enabled:
        return "Mock external dependencies using appropriate mocking library."
    else:
        return "Assume all dependencies are available."

def generate_coverage_details(coverage_level):
    details = {
        "basic": "Aim for 60-70% code coverage",
        "standard": "Aim for 80-85% code coverage",
        "comprehensive": "Aim for 95%+ code coverage"
    }
    return details.get(coverage_level, "")
```

---

## 使用例

### 例1: Python (pytest) - 標準的なテスト生成

```json
リクエスト：
{
  "skill": "generate-unit-tests",
  "parameters": {
    "function_signature": "def validate_email(email: str) -> bool:",
    "language": "python",
    "testFramework": "pytest",
    "coverage": "standard",
    "includeErrorCases": true
  }
}

レスポンス（一部）：
{
  "test_code": "import pytest\n\nclass TestValidateEmail:\n    \"\"\"Test suite for validate_email function.\"\"\"\n    \n    # Normal cases\n    def test_valid_email_simple(self):\n        \"\"\"Test with a simple valid email.\"\"\"\n        assert validate_email('user@example.com') == True\n    \n    def test_valid_email_with_subdomain(self):\n        \"\"\"Test with valid email containing subdomain.\"\"\"\n        assert validate_email('user@mail.example.co.uk') == True\n    \n    # Edge cases\n    def test_empty_string(self):\n        \"\"\"Test with empty string.\"\"\"\n        assert validate_email('') == False\n    \n    def test_email_without_domain(self):\n        \"\"\"Test email with no domain.\"\"\"\n        assert validate_email('user@') == False\n    \n    def test_email_without_local_part(self):\n        \"\"\"Test email with no local part.\"\"\"\n        assert validate_email('@example.com') == False\n    \n    # Error cases\n    def test_none_input(self):\n        \"\"\"Test with None input.\"\"\"\n        with pytest.raises(TypeError):\n            validate_email(None)\n    \n    def test_numeric_input(self):\n        \"\"\"Test with numeric input.\"\"\"\n        with pytest.raises(TypeError):\n            validate_email(12345)",
  "language": "python",
  "framework": "pytest",
  "test_cases": [
    {"name": "test_valid_email_simple", "type": "normal", "description": "Valid simple email"},
    {"name": "test_valid_email_with_subdomain", "type": "normal", "description": "Valid email with subdomain"},
    {"name": "test_empty_string", "type": "edge_case", "description": "Empty string input"},
    {"name": "test_email_without_domain", "type": "edge_case", "description": "Missing domain"},
    {"name": "test_email_without_local_part", "type": "edge_case", "description": "Missing local part"},
    {"name": "test_none_input", "type": "error_case", "description": "None input"},
    {"name": "test_numeric_input", "type": "error_case", "description": "Non-string input"}
  ],
  "imports": ["pytest"],
  "run_instructions": "pytest test_validate_email.py -v"
}
```

### 例2: JavaScript (Jest) - 包括的テスト生成

```json
リクエスト：
{
  "skill": "generate-unit-tests",
  "parameters": {
    "function_signature": "async function fetchUser(userId) { ... }",
    "language": "javascript",
    "testFramework": "jest",
    "coverage": "comprehensive",
    "mockExternalDependencies": true,
    "includePerformanceTests": true
  }
}

レスポンス（部分）：
{
  "test_code": "jest jest.mock('./api');\nconst { fetchUser } = require('./userService');\nconst api = require('./api');\n\ndescribe('fetchUser', () => {\n  beforeEach(() => {\n    jest.clearAllMocks();\n  });\n\n  describe('Normal cases', () => {\n    test('should fetch user data successfully', async () => {\n      const mockUser = { id: 1, name: 'John Doe' };\n      api.get.mockResolvedValue(mockUser);\n\n      const result = await fetchUser(1);\n\n      expect(result).toEqual(mockUser);\n      expect(api.get).toHaveBeenCalledWith('/users/1');\n    });\n  });\n\n  describe('Edge cases', () => {\n    test('should handle userId 0', async () => {\n      const mockUser = { id: 0, name: 'System User' };\n      api.get.mockResolvedValue(mockUser);\n\n      const result = await fetchUser(0);\n\n      expect(result).toEqual(mockUser);\n    });\n\n    test('should handle very large userId', async () => {\n      const largeId = Number.MAX_SAFE_INTEGER;\n      api.get.mockResolvedValue({ id: largeId });\n\n      const result = await fetchUser(largeId);\n\n      expect(api.get).toHaveBeenCalledWith(`/users/${largeId}`);\n    });\n  });\n\n  describe('Error cases', () => {\n    test('should throw on API failure', async () => {\n      api.get.mockRejectedValue(new Error('API Error'));\n\n      await expect(fetchUser(1)).rejects.toThrow('API Error');\n    });\n\n    test('should handle network timeout', async () => {\n      api.get.mockRejectedValue(new Error('TIMEOUT'));\n\n      await expect(fetchUser(1)).rejects.toThrow('TIMEOUT');\n    });\n  });\n\n  describe('Performance', () => {\n    test('should complete within 1 second', async () => {\n      api.get.mockResolvedValue({ id: 1 });\n\n      const startTime = Date.now();\n      await fetchUser(1);\n      const duration = Date.now() - startTime;\n\n      expect(duration).toBeLessThan(1000);\n    });\n  });\n});",
  "language": "javascript",
  "framework": "jest",
  "imports": ["jest", "require('./api')"]
}
```

### 例3: Java (JUnit) - エンタープライズグレード

```json
リクエスト：
{
  "skill": "generate-unit-tests",
  "parameters": {
    "function_signature": "public class UserService { public User getUser(String id) throws UserNotFoundException { ... } }",
    "language": "java",
    "testFramework": "junit",
    "coverage": "comprehensive"
  }
}

レスポンス（部分）：
{
  "test_code": "import org.junit.jupiter.api.Test;\nimport org.junit.jupiter.api.BeforeEach;\nimport static org.junit.jupiter.api.Assertions.*;\nimport static org.mockito.Mockito.*;\n\nclass UserServiceTest {\n    private UserService userService;\n    private UserRepository mockRepository;\n\n    @BeforeEach\n    void setUp() {\n        mockRepository = mock(UserRepository.class);\n        userService = new UserService(mockRepository);\n    }\n\n    @Test\n    void testGetUserWithValidId() throws UserNotFoundException {\n        // Arrange\n        String userId = \"123\";\n        User expectedUser = new User(\"123\", \"John Doe\");\n        when(mockRepository.findById(userId)).thenReturn(expectedUser);\n\n        // Act\n        User result = userService.getUser(userId);\n\n        // Assert\n        assertEquals(expectedUser, result);\n        verify(mockRepository).findById(userId);\n    }\n\n    @Test\n    void testGetUserWithNullId() {\n        assertThrows(IllegalArgumentException.class, () -> {\n            userService.getUser(null);\n        });\n    }\n\n    @Test\n    void testGetUserWithInvalidId() throws UserNotFoundException {\n        when(mockRepository.findById(\"invalid\")).thenThrow(new UserNotFoundException());\n\n        assertThrows(UserNotFoundException.class, () -> {\n            userService.getUser(\"invalid\");\n        });\n    }\n}",
  "language": "java",
  "framework": "junit"
}
```

---

## 高度なカスタマイズ

### カスタマイズ1: テストカバレッジの詳細設定

```json
// coverageLevel を拡張して、より細かい制御を可能にする例

"coverageLevel": "custom",
"customCoverage": {
  "normalCases": 3,      // 正常系テストを最低3つ生成
  "edgeCases": 5,        // エッジケース最低5つ
  "errorCases": 3,       // エラーケース最低3つ
  "targetCoverage": 90   // コードカバレッジ 90% を目指す
}
```

### カスタマイズ2: テストデータ生成戦略

```json
"testDataGeneration": {
  "strategy": "use_fixtures",  // or "use_factories", "use_builders"
  "fixturesPath": "./tests/fixtures",
  "generateFactories": true,
  "generateBuilders": true
}
```

### カスタマイズ3: CI/CD 統合

```json
"cicdIntegration": {
  "generateGitHubActions": true,
  "generateGitLabCI": true,
  "generateJenkins": false,
  "includeCodeCoverageBadge": true
}
```

---

## トラブルシューティング

### 問題1: 生成されたテストが実行できない

**原因：** インポートやモック設定が不正

**修正：**

```json
"setup_instructions": "Run: pip install pytest pytest-mock\n npm install jest @testing-library/react"
```

### 問題2: エッジケースが不足

**原因：** 関数シグネチャから推測できない領域域がある

**修正：** function_signature に追加情報を含める

```json
"function_signature": "def process_payment(amount: float, currency: str, retry_count: int = 3) -> bool:\n    '''Process payment. Raises InsufficientFunds, NetworkError.'''"
```

### 問題3: 外部依存のモック化が複雑

**原因：** 多層の依存関係

**修正：**

```json
"mockExternalDependencies": true,
"mockingStrategy": "use_factories"  // より高度なモック戦略を指定
```

---

## テストコード品質イ評価チェックリスト

生成されたテストを評価して、品質が十分か確認：

```
✓ 明確な Arrange-Act-Assert パターン
✓ 各テストが1つの動作のみを検証
✓ テスト名が何をテストしているか明確
✓ 正常系、エッジケース、エラーケースの均衡
✓ 外部依存がモックされている
✓ 重複するテストがない
✓ 実行が速い（各テスト < 100ms）
✓ ランダムな順序で実行しても成功
✓ セットアップ/クリーンアップが適切
✓ アサーション が具体的（assertFalse() より assertEqual()）
```

---

## 実装チェックリスト

```
□ スキル定義ファイルが有効な JSON か確認
□ 全言語でテスト（Python, JS, Java, Go）
□ 全テストフレームワークでテスト（pytest, jest, junit等）
□ 全 coverage レベルでテスト（basic, standard, comprehensive）
□ 各テストが実際に実行可能か確認
□ モック設定が正しいか確認
□ エラーハンドリングをテスト
□ パフォーマンステストが実現可能か確認
□ ドキュメント完備（使用方法、セットアップ手順）
□ リポジトリに登録
```

---

## Part 3 の総括

```
実装した3つのサンプルスキル：

1. 【初級】analyze-code-quality
   - シンプルな入力・出力
   - 単一の出力形式（JSON）
   - 分析的なタスク

2. 【中級】generate-documentation
   - 複数のドキュメント形式対応
   - テキスト出力
   - セクション分割

3. 【上級】generate-unit-tests
   - 複数のテストフレームワーク対応
   - 複雑なテンプレート展開
   - 多段階の出力
   - エラーハンドリングが豊富

これらのパターンを学ぶことで、
あらゆるスキルを設計・実装できるようになります。
```

---

## 次へ進む

→ [Part 4: 活用編](../04-advanced/01-team-sharing.md) - チーム内でのスキル共有と運用

Part 3 の実装編が完了しました。
次は Part 4 で、これらのスキルをチーム全体で活用する方法を学びます。

## Part 3-6: スキル評価フレームワーク（evals） {#section-03-implementation-06-skill-evaluation}


スキルが意図したとおりに機能しているかを測定し、改善するための **評価駆動開発（EDD）** アプローチです。

---

### 概要：なぜ評価が必要か？

開発したスキルが本当に良いのか、を客観的に確認する必要があります。

```
問題：
└─ スキルを作成 → 試した → 「これでいいでしょう」？

リスク：
├─ 実は他のプロンプトでは失敗している
├─ 追加要件で改善が難しくなる
├─ エッジケースで崩れる
└─ ユーザーが望んでいない結果を生んでいる

解決策：
└─ 評価駆動開発（EDD）
    ├─ テストケースを定義
    ├─ with-skill と without-skill で比較実行
    ├─ 結果を採点・集計
    └─ データに基づいて改善
```

---

### Phase 1: テストケース設計

#### evals.json 構造

スキルのテストケースを `evals/evals.json` に記録します。

```json
{
  "skill_name": "pdf-processing",
  "evals": [
    {
      "id": 1,
      "prompt": "実際のユーザープロンプト",
      "expected_output": "成功の定義",
      "files": ["evals/files/sample.pdf"],
      "assertions": ["検証可能なステートメント"]
    }
  ]
}
```

#### テストケースの設計方針

##### 1. 最初は3つのテストケースから開始

**理由**
- リソース効率（時間・トークン節約）
- 反復が容易
- 大量のテストで圧倒されない

```
Week 1: 3個のテストケース設計 & 実行
Week 2: 結果評価 & 改善
Week 3: テストケース追加（必要に応じて）
```

##### 2. 現実的なプロンプトを使う

```json
{
  "id": 1,
  "prompt": "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?",
  "expected_output": "A bar chart image showing top 3 months by revenue with labeled axes and values.",
  "files": ["evals/files/sales_2025.csv"]
}
```

**ポイント**
- ファイルパスを含める（ユーザーは常にファイルを参照する）
- 個人的な文脈を含める（「data/...」など）
- 自然な言い回し

##### 3. バリエーションを含める

**良い例**
```json
{
  "id": 1,
  "prompt": "Hey, can you clean up this CSV? customers.csv has some missing emails."
},
{
  "id": 2,
  "prompt": "Parse the CSV at data/input.csv, drop rows where column B is null, and save to data/output.csv"
},
{
  "id": 3,
  "prompt": "I have a corrupted CSV with mixed delimiters. Can you fix it?"
}
```

**理由**
- カジュアルな言い回し（id: 1）
- 技術的で詳細（id: 2）
- エッジケース（id: 3）
- 異なる文脈で動作確認

##### 4. エッジケースを最低1つ含める

```json
{
  "id": 3,
  "prompt": "This CSV file is smaller than usual and has missing headers. Can you analyze it anyway?",
  "expected_output": "Analysis that handles missing headers gracefully",
  "files": ["evals/files/malformed.csv"]
}
```

#### 実装例：完全な evals.json

```json
{
  "skill_name": "csv-analyzer",
  "evals": [
    {
      "id": 1,
      "name": "basic-sales-analysis",
      "prompt": "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?",
      "expected_output": "A bar chart image showing the top 3 months by revenue, with labeled axes and values.",
      "files": ["evals/files/sales_2025.csv"],
      "assertions": [
        "The output includes a bar chart image file",
        "The chart shows exactly 3 months",
        "Both axes are labeled",
        "The chart title or caption mentions revenue"
      ]
    },
    {
      "id": 2,
      "name": "data-cleaning",
      "prompt": "There's a CSV in my downloads called customers.csv with some rows having missing emails — can you clean it up and tell me how many were missing?",
      "expected_output": "A cleaned CSV with missing emails handled, plus a count of how many were missing.",
      "files": ["evals/files/customers.csv"],
      "assertions": [
        "Output file is valid CSV format",
        "Missing email rows are removed",
        "Count of removed rows is reported",
        "No data corruption in remaining rows"
      ]
    },
    {
      "id": 3,
      "name": "edge-case-malformed",
      "prompt": "This CSV file has mixed delimiters and some missing headers. Can you parse it and tell me what you found?",
      "expected_output": "Analysis of the CSV structure identifying delimiters, missing headers, and an assessment of data quality.",
      "files": ["evals/files/malformed.csv"],
      "assertions": [
        "Parsing completes without error",
        "Missing headers are identified",
        "Data quality assessment is provided",
        "Recommendations for fixing are included"
      ]
    }
  ]
}
```

---

### Phase 2: ベースライン実行

#### with-skill vs without-skill 比較

**ディレクトリ構造**

```
csv-analyzer-workspace/
└── iteration-1/
    ├── eval-1-sales-analysis/
    │   ├── with_skill/
    │   │   ├── outputs/          # スキル実行後の出力ファイル
    │   │   ├── timing.json       # 実行時間・トークン数
    │   │   └── grading.json      # Assertion評点
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    ├── eval-2-data-cleaning/
    │   ├── with_skill/
    │   └── without_skill/
    ├── eval-3-edge-case/
    │   ├── with_skill/
    │   └── without_skill/
    └── benchmark.json            # 統計集約
```

#### 実行方法

##### 1. with-skill 実行（スキル使用）

**指示**
```
Execute this task:
- Skill path: /path/to/csv-analyzer
- Task: "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?"
- Input files: evals/files/sales_2025.csv
- Save outputs to: csv-analyzer-workspace/iteration-1/eval-1-sales-analysis/with_skill/outputs/
```

**期待値**
```
実行結果：
├─ outputs/ に出力ファイル（chart.png等）
├─ timing.json に実行統計
└─ grading.json に評価結果
```

##### 2. without-skill 実行（ベースライン）

**指示**
```
Execute this task WITHOUT any skills:
- Task: "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?"
- Input files: evals/files/sales_2025.csv  
- Save outputs to: csv-analyzer-workspace/iteration-1/eval-1-sales-analysis/without_skill/outputs/
```

---

### Phase 3: Assertions 定義

#### Assertions とは

検証可能で、客観的に判定できるステートメント。

```
✅ 良い Assertion
├─ "Output includes a valid JSON file"（ファイル存在・形式チェック可能）
├─ "Chart has labeled axes"（視覚的に確認可能）
└─ "Count of records is exactly 150"（数値チェック可能）

❌ 悪い Assertion
├─ "Output is good"（曖昧）
├─ "Uses the exact phrase 'Total Revenue: $X'"（脆弱、文言変更で失敗）
└─ "Feels right"（主観的）
```

#### Assertions 設計のコツ

##### 1. 実装後に追加（最初は期待値のみでOK）

```json
{
  "id": 1,
  "prompt": "...",
  "expected_output": "A bar chart...",
  "files": ["..."],
  "assertions": []  // 最初は空で良い
}

// 実行後、結果を見てから assertions を追加
"assertions": [
  "The output includes a bar chart image file",
  "The chart shows exactly 3 months",
  "Both axes are labeled"
]
```

**理由**
- 実際の出力を見ないと「良い」assertionが書けない
- 実装前の想定と実装後の現実は異なる

##### 2. 数値や構造で検証

```json
{
  "assertions": [
    "Output file size > 50KB",
    "JSON has exactly 3 root-level keys",
    "All required fields present: id, name, score",
    "No null values in critical fields"
  ]
}
```

##### 3. 客観的な証拠を求める

```
❌ 弱い評価方法
「これはいいですね」

✅ 強い評価方法
「Found chart.png (87KB) in outputs/」← ファイル証拠
「Title text: 'Top 3 Months by Revenue'」← 実内容
「X-axis labels: January, July, November」← 具体的データ
```

---

### Phase 4: Grading（採点）

#### grading.json 構造

各 assertion に対して PASS/FAIL を記録。

```json
{
  "assertion_results": [
    {
      "text": "The output includes a bar chart image file",
      "passed": true,
      "evidence": "Found chart.png (87KB) in outputs directory"
    },
    {
      "text": "The chart shows exactly 3 months",
      "passed": true,
      "evidence": "Chart displays bars for March, July, and November"
    },
    {
      "text": "Both axes are labeled",
      "passed": false,
      "evidence": "Y-axis labeled 'Revenue ($)' but X-axis has no label"
    },
    {
      "text": "The chart title mentions revenue",
      "passed": true,
      "evidence": "Chart title: 'Top 3 Months by Revenue'"
    }
  ],
  "summary": {
    "passed": 3,
    "failed": 1,
    "total": 4,
    "pass_rate": 0.75
  }
}
```

#### 採点原則

1. **強い証拠を求める**
   - FAIL なら、FAIL の具体的な理由を
   - PASS なら、PASS を示す証拠を

2. **Assertion 自体も見直す**
   - 常に PASS している → 実質価値がない、削除または強化
   - 常に FAIL している → Assertion が要件に合致していない、修正

3. **スクリプトで検証可能なものはコード化**
   ```python
   # JSON 有効性チェック
   try:
       json.loads(output)
       return PASS
   except:
       return FAIL
   ```

---

### Phase 5: 集計（Benchmarking）

#### benchmark.json 作成

全テストケースの統計を集約。

```json
{
  "run_summary": {
    "with_skill": {
      "pass_rate": {
        "mean": 0.83,
        "stddev": 0.06
      },
      "time_seconds": {
        "mean": 45.0,
        "stddev": 12.0
      },
      "tokens": {
        "mean": 3800,
        "stddev": 400
      }
    },
    "without_skill": {
      "pass_rate": {
        "mean": 0.33,
        "stddev": 0.10
      },
      "time_seconds": {
        "mean": 32.0,
        "stddev": 8.0
      },
      "tokens": {
        "mean": 2100,
        "stddev": 300
      }
    },
    "delta": {
      "pass_rate": 0.50,
      "time_seconds": 13.0,
      "tokens": 1700
    }
  }
}
```

#### 解釈

```
delta.pass_rate = 0.50 (50ポイント改善)
delta.time_seconds = 13.0 (+13秒）
delta.tokens = 1700 (+1700トークン)

判断：
├─ Pass rate が 50 ポイント改善 → スキルの価値は大きい
├─ +13 秒の追加時間 → 許容範囲
└─ +1700 トークン → 50% の改善に見合う投資
→ ✅ スキルは有效
```

#### パターン認識

##### パターン1：スキルが有効

```
with_skill：pass_rate 0.85、time +15秒、tokens +2000
without_skill：pass_rate 0.35、time 30秒、tokens 1500

分析：
├─ 50ポイント改善は大きい
├─ 時間・トークンの追加は許容範囲
└─ ✅ スキル採用すべき
```

##### パターン2：スキルが過度に複雑

```
with_skill：pass_rate 0.37、time +45秒、tokens +5000
without_skill：pass_rate 0.35、time 25秒、tokens 1000

分析：
├─ 2ポイント改善は微小
├─ +45秒は大きな追加コスト
├─ +5000トークンは過度
└─ ❌ スキル簡略化が必要、または破棄検討
```

##### パターン3：エッジケース未対応

```
Test 1-2：pass_rate 0.95 (with-skill)
Test 3  ：pass_rate 0.10 (with-skill エッジケースで失敗)

分析：
├─ 通常ケースは優秀
├─ エッジケースで脆弱
└─ → エッジケースハンドリングを改善
```

---

### Phase 6: 人間によるレビュー

#### feedback.json 作成

採点だけでなく、人間の目で確認。

```json
{
  "eval-1-sales-analysis": {
    "comment": "Chart is missing X-axis labels and months are in alphabetical order, not chronological. Data accuracy is correct.",
    "rating": "PARTIAL_PASS"
  },
  "eval-2-data-cleaning": {
    "comment": "Output CSV is clean and correct. Count reporting is clear.",
    "rating": "PASS"
  },
  "eval-3-edge-case": {
    "comment": "Skill crashes on completely malformed CSV. Need better error handling.",
    "rating": "FAIL"
  }
}
```

#### フィードバック要素

```
✅ 具体的で改善可能
├─ "Missing X-axis labels"
├─ "Months are alphabetical, not chronological"
└─ "Need error handling for complete malformation"

❌ 曖昧で改善困難
├─ "Looks bad"
├─ "Not quite right"
└─ "Could be better"
```

---

### Phase 7: 改善ループ

#### 改善サイクル

```
1. テストケース & Assertion 実行
         ↓
2. 結果評価（数値 + 人間レビュー）
         ↓
3. 改善シグナル収集
   ├─ 失敗 Assertion = 実装ギャップ
   ├─ フィードバック = 品質問題
   └─ Transcript = デバッグ情報
         ↓
4. SKILL.md 改善提案（LLM利用）
         ↓
5. 改善実装
         ↓
6. 新しい iteration 実行（ iteration-2/）
         ↓
7. 改善されたか確認
```

#### 改善の優先順位

```
優先度1：通常ケースの失敗
└─ 最も影響が大きい

優先度2：エッジケースの失敗
└─ 重要だけど頻度は低い

優先度3：品質・UX問題
└─ 機能は動くが改善の余地がある

優先度4：トークン最適化
└─ 動作は満足も、コスト削減の余地
```

#### 改善指示（LLM 向け）

```
Analyze these eval results and propose improvements to the SKILL.md:

Current SKILL.md:
[SKILL.md 全文]

Failed assertions:
- Test 1: "X-axis labels missing" (but Y-axis is labeled)
- Test 3: Crashes on malformed CSV

Human feedback:
- "Months shown in alphabetical order, not chronological"
- "Need graceful error handling"

Execution transcript:
[LLM が何をしたか、どこで失敗したか]

Generalize from these failures. What broader instructions need to
improve to prevent this across many different prompts?
```

---

### 実装チェックリスト

#### テストケース設計段階
- [ ] 少なくとも3つのテストケース定義
- [ ] evals/evals.json に記録
- [ ] カジュアル・技術的・エッジケースを混在
- [ ] 現実的なファイルパス・文脈を含める

#### ベースライン実行
- [ ] with-skill 実行 → outputs/ に保存
- [ ] without-skill 実行 → baseline で比較
- [ ] timing.json に実行統計記録

#### Assertion & Grading
- [ ] Assertion は実行後に追加（結果見てから）
- [ ] grading.json に具体的な証拠を記録
- [ ] 常に PASS/FAIL している Assertion を見直し

#### 集計 & 分析
- [ ] benchmark.json に統計集約
- [ ] delta を解釈（改善ポイントと追加コスト）
- [ ] パターン認識（スキルの価値判定）

#### 人間レビュー & 改善
- [ ] feedback.json に具体的コメント
- [ ] 失敗原因を特定
- [ ] 改善提案を SKILL.md に反映
- [ ] 新しい iteration で再実行

---

### よくある質問

#### Q1. Assertion で LLM 判定 vs スクリプト判定、どちらを使う？

**A:** 両方を使い分ける

```
スクリプト検証（信頼性高）
├─ JSON 有効性
├─ ファイル存在・サイズ
├─ レコード数・カラム数
└─ 構造的検証

LLM 判定（柔軟性高）
├─ 内容品質「レポートは有用か」
├─ スタイル「書き方は適切か」
├─ ユーザビリティ「使いやすいか」
└─ 定性的判定
```

#### Q2. 何個のテストケースが必要？

**A:** 段階的に増加

```
Phase 1（初期）：3-5個
Phase 2（安定化）：5-10個
Phase 3（本番化）：10-20+個

ただし「質 > 量」
├─ 1つの良いテストケース
└─ 10個の無駄なテストケースより価値がある
```

#### Q3. スキルの改善をどこまで続ける？

**A:** これらの条件で停止

```
停止条件：
├─ Pass rate が target（例：85%）に達した
├─ 連続2 iteration で改善がない
├─ 時間・トークンコストが許容範囲
└─ フィードバックが「OK」に統一

それ以降は：
├─ 本番運用開始
├─ ユーザーフィードバック収集
└─ 定期レビュー（月1回等）
```

---

### 関連資料

- [agentskills.io - Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- Part 3-3: スキル品質分析（サンプル JSON 例）
- Part 4-2: スキル管理とライフサイクル（運用フェーズ）

# Advanced {#chapter-04-advanced}

## Part 4-1: チーム内スキル共有戦略 {#section-04-advanced-01-team-sharing}


Agent Skills を個人で使うだけでなく、チーム全体で効果的に活用するための戦略を学びます。

---

### Part 4-1: スキル共有と組織化

### チーム内スキル共有の重要性

#### 共有がもたらす効果

```
個人の生産性向上 → チーム全体の生産性向上
        ↓
スキル・ノウハウの標準化
        ↓
新人研修期間の短縮
        ↓
品質の均一化
```

**実績例：** 10人チームが同一スキルを共有すると、スキル作成に5時間かかった場合でも
- 10人 × スキル使用時間削減2時間 = 20時間の削減
- ROI: 4倍以上

---

### スキル共有の3つの戦略

#### 戦略1: リポジトリベース共有

```yaml
github-copilot-skills/
├── .github/
│   ├── CONTRIBUTING.md       # 貢献ガイドライン
│   ├── CODE_OF_CONDUCT.md
│   └── PULL_REQUEST_TEMPLATE.md
├── skills/
│   ├── analyze-code-quality/
│   ├── generate-documentation/
│   └── generate-unit-tests/
├── docs/
│   ├── USAGE.md              # 使用方法
│   ├── API.md                # API仕様
│   └── EXAMPLES.md           # 使用例
├── tests/
│   └── test_all_skills.py    # テストスイート
├── REGISTRY.md               # スキルレジストリ
└── README.md
```

**メリット：**
- バージョン管理が容易
- コードレビュー可能
- 変更履歴を追跡可能
- CI/CD統合可能

**デメリット：**
- セットアップが複雑
- リポジトリ管理の手間

#### 戦略2: パッケージ（npm, PyPI）での配布

```bash
# Python example
pip install copilot-skills

# JavaScript example
npm install @company/copilot-skills
```

**メリット：**
- インストール・更新が簡単
- バージョン管理が自動
- 依存関係解決が容易

**デメリット：**
- PyPI/npm のセットアップが必要
- 公開か非公開か決定が必要

#### 戦略3: 組織内ポータル

```
Copilot Skills Portal
├── スキルカタログ
│   ├── フィルタリング（言語、カテゴリ）
│   ├── 検索機能
│   └── レーティング・コメント
├── インストール手順
├── 使用例・チュートリアル
├── 質問Q&A
└── 利用統計ダッシュボード
```

**メリット：**
- ユーザーフレンドリー
- 検出可能性が高い
- エンゲージメント向上

**デメリット：**
- インフラの構築・管理が必要

---

### スキルレジストリの設計

#### スキルメタデータの標準化

```json
{
  "id": "skill-unique-id",
  "name": "スキル表示名",
  "version": "1.0.0",
  "status": "published",  // draft, published, deprecated, archived
  "description": "説明",
  "category": "code-analysis",
  "difficulty": "beginner",   // beginner, intermediate, advanced
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "organization": "Org"
  },
  "tags": ["python", "testing", "automation"],
  "supportedLanguages": ["python", "javascript"],
  "requiredLicenses": [],
  "dependencies": [
    {"id": "some-other-skill", "version": ">=1.0.0"}
  ],
  "usage": {
    "timesUsed": 1234,
    "lastUsed": "2026-03-07T14:30:00Z",
    "rating": 4.5,
    "reviews": 23
  },
  "documentation": {
    "url": "https://docs.example.com/skills/skill-id",
    "apiDocs": "https://docs.example.com/api/skill-id"
  },
  "codeRepository": {
    "url": "https://github.com/org/copilot-skills",
    "path": "skills/skill-id",
    "branch": "main"
  },
  "versionHistory": [
    {
      "version": "1.1.0",
      "releaseDate": "2026-03-07",
      "changelog": "Added new feature X"
    }
  ]
}
```

#### スキルカタログ（REGISTRY.md）

```markdown
# Copilot Skills Catalog

## Code Analysis & Quality

| Skill ID | Name | Version | Author | Status | Difficulty |
|----------|------|---------|--------|--------|------------|
| analyze-code-quality | Code Quality Analysis | 1.0.0 | QA Team | Published | Intermediate |
| generate-unit-tests | Test Generation | 1.0.0 | QA Team | Published | Advanced |
| detect-security-issues | Security Issue Detection | 1.2.0 | Security Team | Published | Intermediate |

## Documentation & Code Generation

| Skill ID | Name | Version | Author | Status | Difficulty |
|----------|------|---------|--------|--------|------------|
| generate-documentation | Doc Generation | 1.0.0 | Dev Team | Published | Intermediate |
| generate-api-docs | API Doc Generation | 0.9.0 | Dev Team | Draft | Intermediate |
```

---

### スキル共有のベストプラクティス

#### Practice 0: 補助リソース（スクリプト・テンプレート）の管理戦略

**補助リソースの種類：**

```yaml
補助スクリプト:
  - 入力値検証: validate-input.py
  - 出力形式変換: format-converter.sh
  - テスト実行: test-harness.py
  - パフォーマンス計測: performance-profiler.js

テンプレート・サンプル:
  - LLMプロンプトテンプレート: prompt-template.md
  - 出力形式スキーマ: output-schema.json
  - テストケース集: test-cases.json
  - チェックリスト: checklist.md

ツール・ユーティリティ:
  - 互換性チェッカー: compatibility-checker.py
  - パフォーマンス診断: performance-analyzer.py
  - バージョン管理: version-manager.sh
```

**スキル配布時の構成例：**

```
skills/analyze-code-quality/
├── SKILL.md                    # スキル定義
├── README.md                   # オーバービュー
├── scripts/                    # 補助スクリプト
│   ├── validate_input.py
│   ├── format_output.py
│   └── test_harness.py
├── templates/                  # テンプレート
│   ├── output-schema.json
│   └── test-cases.json
├── tools/                      # 診断ツール
│   └── performance-profiler.py
└── docs/                       # ドキュメント
    ├── API.md
    ├── EXAMPLES.md
    └── TROUBLESHOOTING.md
```

**配布方法別のファイル含有:**

| 配布方法 | 補助ファイル | 強力な機能 |
|--------|-----------|----------|
| **GitHub リポジトリ** | すべて | CI/CD統合、バージョン管理 |
| **npm パッケージ** | scripts/, templates/ | 自動インストール |
| **Python パッケージ** | scripts/, templates/ | pip でインストール |
| **組織ポータル** | すべて | ビジュアルガイド |

#### Practice 1: 明確な命名規則

```
悪い例：
- skill1, skill2, test_gen, doc_auto

良い例：
- generate-unit-tests           # skill-id: 単語をハイフンで区切る
- コード品質分析スキル          # display name: 日本語で意図を明確に
- code-quality-analyzer         # 英語: 動詞-名詞で構成
```

#### Practice 2: バージョニング (Semantic Versioning)

```
Version Format: MAJOR.MINOR.PATCH

例：
- 1.0.0 → 1.1.0 (新機能追加、後方互換性あり)
- 1.0.0 → 2.0.0 (破壊的変更、パラメータ削除など)
- 1.0.0 → 1.0.1 (バグ修正、内部改善)
- 1.0.0 → 1.0.0-beta.1 (プレリリース)

変更ルール：
- パラメータ削除 → MAJOR版上げ
- 新パラメータ（デフォルト値あり） → MINOR版上げ
- バグ修正、内部最適化 → PATCH版上げ
```

#### Practice 3: 互換性の管理

```json
// バージョン2.0へのマイグレーション

// v1.x の使用方法
{
  "parameter": {
    "language": "python",
    "code": "def foo(): pass",
    "style": "google"
  }
}

// v2.0（互換性を保つ方法）
{
  "parameter": {
    "language": "python",
    "code_snippet": "def foo(): pass",  // 新しい名前
    "docstyle": "google",              // 新しい名前
    "_compat": {
      "v1_language_mapped_to": "language",
      "v1_code_mapped_to": "code_snippet",
      "v1_style_mapped_to": "docstyle"
    }
  }
}
```

---

### スキル共有プロセス

#### ステップ1: スキル準備

```
□ スキル定義の完成度確認
  - JSONスキーマが有効か
  - 全パラメータがドキュメント化されているか
  - 計3個以上のテストケースがあるか

□ ドキュメント完備
  - 概要説明
  - 使用例
  - パラメータ説明
  - 出力形式の説明
  - トラブルシューティング

□ テストケースの作成
```

#### ステップ2: チームレビュー

```
レビュー項目：
□ スキル定義が明確か
□ テンプレートが適切か
□ パラメータ名が直感的か
□ エラーハンドリングが十分か
□ パフォーマンスに問題ないか
□ セキュリティ上の問題がないか
□ ドキュメントが完全か

レビュー参加者：
- QA/Testing チーム
- セキュリティチーム
- ドキュメンチーム（技術文書）
- 利用予定チーム
```

#### ステップ3: 公開・告知

実運用への接続を標準化するため、公開時点で運用手法も合わせて案内します。

- 参照: [Part 4-7: 運用手法（Runbook / Gate / Evidence / Scope / Rollout）](#section-04-advanced-07-operations-methodology)

```
公開チェックリスト：
□ スキルレジストリに登録
□ リポジトリに提出（PR）
□ パッケージレジストリに公開（PyPI/npm）
□ ドキュメントサイトに掲載
□ チーム内告知メール送信
□ オンボーディングセッション開催
□ Q&A チャネル（Slack等）を開設
```

---

### スキル利用状況の追跡

#### メトリクスの定義

```json
{
  "metrics": {
    "adoption": {
      "uniqueUsers": 45,
      "totalUsages": 2304,
      "activeUsers": 28,
      "adoptionRate": "72%"
    },
    "performance": {
      "averageExecutionTime": 2.3,
      "successRate": 98.5,
      "errorRate": 1.5
    },
    "quality": {
      "userRating": 4.2,
      "reviewCount": 18,
      "reportedBugs": 2
    },
    "adoption_curve": {
      "week_1": 5,
      "week_2": 12,
      "week_3": 28,
      "week_4": 45
    }
  }
}
```

#### ダッシュボード例

```
[Copilot Skills Dashboard]

全スキル統計：
- 利用可能スキル：47個
- 利用中スキル：31個
- 非アクティブ：8個
- 廃止予定：2個

トップ10スキル（この月）：
1. generate-unit-tests (634使用)
2. analyze-code-quality (521使用)
3. generate-documentation (412使用)
4. find-security-issues (308使用)
5. ...

スキル採用トレンド：
[グラフ]
```

---

### チーム別スキル管理

#### チーム毎のスキル責任配分

```
【開発チーム】責任スキル：
- generate-unit-tests
- analyze-code-quality
- generate-documentation
- code-review-assist

【QA/テストチーム】責任スキル：
- generate-test-data
- test-case-generation
- test-failure-analysis

【セキュリティチーム】責任スキル：
- find-security-issues
- perform-security-audit
- dependency-analyze

【DevOpsチーム】責任スキル：
- optimize-performance
- analyze-logs
- infrastructure-config
```

#### 責任スキルの義務

```
各スキルオーナーは：
✓ 月1回以上、利用統計をレビュー
✓ 報告されたバグに2日以内に対応
✓ 四半期ごとにアップデート提案を検討
✓ ドキュメントを最新に保つ
✓ ユーザーからの質問に対応
✓ 非推奨化する場合は3ヶ月前に通知
```

---

### トラブル対応

#### 問題1: スキル采用率が低い

**原因の特定：**
```
□ ユーザーがスキルを知らない
□ スキル学習コストが高い
□ 既存ツール/プロセスで十分
□ スキル品質に問題がある
□ UIが使いづらい
```

**対策：**
```
1. 採用率が低いスキルの理由を調査
   - アンケート実施
   - ユーザーインタビュー

2. 認知度向上
   - デモセッション
   - ドキュメント改善
   - 社内ブログ記事

3. 品質改善
   - バグ修正
   - パフォーマンス向上
   - UXの改善

4. インセンティブ
   - スキル使用へのゲーミフィケーション
   - チームランキング
```

#### 問題2: スキル依存による事故

**シナリオ：** 複数のスキルが同一の根底となるスキルに依存している場合、
その根底スキルが壊れるとカスケード障害が発生

**対策：**
```
□ 依存関係グラフの可視化
□ 破壊的変更の伝播シミュレーション
□ レイアウト的テスト（すべての組み合わせ）
□ 段階的な廃止（deprecated フェーズ）
□ フォールバック機構
```

---

### インボーディング・トレーニング

#### 新人向けスキルトレーニングプログラム

**Week 1: 基礎**
```
Day 1: Copilot Agent Skills 概要
Day 2: スキル利用方法 101
Day 3: よく使う3つのスキル（分析、生成、テスト）
Day 4: 実習（簡単なスキルを使用）
Day 5: Q&A セッション
```

**Week 2: 実務**
```
Day 1: チームで使用しているスキル紹介
Day 2: スキル活用例（ベストプラクティス）
Day 3: トラブルシューティング
Day 4: カスタムスキル作成 101（簡単な例）
Day 5: 実習＆フィードバック
```

---

### 実装チェックリスト

```
スキル共有体制の構築：
□ スキルレジストリ（REGISTRY.md）を作成
□ リポジトリ構成を整備
□ CI/CD パイプラインを設定（テスト・ドキュメント検証）
□ スキルメタデータのスキーマを定義
□ CONTRIBUTING.md を作成

チーム運用：
□ スキルオーナーを指定
□ 定期レビュー（月1回）のスケジュール
□ SLA（応答時間、バグ対応時間）を定義
□ アップデート・リリース процеス を確立
□ ドキュメント更新ルールを確立

トレーニング：
□ オンボーディング資料を作成
□ デモビデオを録画
□ チュートリアル文書を作成
□ Q&Aフォーラムを構築
□ 定期トレーニングセッションのスケジュール
```

---

### まとめ

| 側面 | ポイント |
|------|---------|
| **共有戦略** | リポジトリ、パッケージ、ポータルから組織にあわせて選択 |
| **レジストリ化** | メタデータを標準化して検出性を向上 |
| **バージョン管理** | Semantic Versioning で破壊的変更を明確に |
| **利用追跡** | メトリクス収集で改善の根拠を示す |
| **責任分担** | スキルオーナー制で持続可能な運用を実現 |
| **トレーニング** | 組織化により中長期の成功を確保 |

→ 実装ガイド: [Part 4-6: 複数リポでの SKILL 共通化](#section-04-advanced-06-multi-repo-skill-sharing)  
→ 次へ: [Part 4-2: スキル管理とライフサイクル](#section-04-advanced-02-management)

## Part 4-2: スキル管理とライフサイクル {#section-04-advanced-02-management}


スキルを長期にわたって効果的に運用するための管理戦略を解説します。

---

### スキルのライフサイクル

#### 5つのステージ

```
┌────────────────────────────────────────────────────────┐
│           Skill Lifecycle Management                  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. Draft → 2. Beta → 3. Published → 4. Mature → 5. Deprecated
│  設計作成    テスト    公開         安定運用      廃止
│                                                        │
│  期間      1-2w      2-4w      3-6m      6m-2y      3m
│  ステータス草案      検証      利用中    確立済み    廃止予定中
│                                                        │
└────────────────────────────────────────────────────────┘
```

#### Stage 1: Draft（設計・開発）

**目的:** スキル定義の完成

**期間:** 1-2週間

**活動:**
```yaml
スキル設計:
  - ユースケースの検証
  - パラメータ設計
  - 出力形式の決定

実装:
  - JSONスキーマの作成
  - プロンプトテンプレートの作成
  - 基本的なテストの実装

品質確認:
  - パラメータ妥当性チェック
  - プロンプト精度チェック
  - 基本的なテストケース実行
```

**成果物:**
```
□ skill-definition.json
□ README.md（スキル説明）
□ USAGE.md（使用方法）
□ test_cases.json（テストケース5個以上）
□ CHANGELOG.md（変更履歴）

【補助リソース】
□ scripts/ ディレクトリ
  ├─ validate_input.py（入力値検証スクリプト）
  └─ test-harness.py（テスト実行ツール）
□ templates/ ディレクトリ
  ├─ prompt-template.md
  └─ output-schema.json
□ docs/API.md（パラメータ・出力形式の詳細説明）
```

**出口基準:**
```
✓ JSONスキーマが有効
✓ 最低5個のテストケースが全て成功
✓ ドキュメントが完成
✓ チーム内での形式レビューが完了
```

---

#### Stage 2: Beta（テスト・フィードバック）

**目的:** スキルの品質検証と改善

**期間:** 2-4週間

**ユーザー:** 限定的なユーザーグループ（5-10人）

**活動:**
```yaml
限定公開:
  - ベータユーザーの募集
  - アクセス権の付与
  - 初期サポート体制の構築

フィードバック収集:
  - 定期チェックイン（週1回）
  - 使用パターンの分析
  - 不具合報告の受け取り
  - UX フィードバック

改善実施:
  - バグ修正
  - パラメータ調整
  - プロンプト最適化
  - ドキュメント改善
```

**メトリクス追跡:**
```json
{
  "beta_metrics": {
    "daily_active_users": [3, 5, 7, 8, 8],
    "average_execution_time": 2.3,
    "success_rate": 96.5,
    "error_rate": 3.5,
    "reported_issues": [
      {"id": "ISSUE-001", "severity": "high", "status": "fixed"},
      {"id": "ISSUE-002", "severity": "medium", "status": "fixed"}
    ],
    "user_satisfaction": 4.1
  }
}
```

**成果物:**
```
□ Beta Feedback Report（フィードバック集約）
□ Bug Fix Log（修正ログ）
□ Updated Documentation
□ Performance Metrics
```

**出口基準:**
```
✓ ベータユーザー満足度 >= 4.0/5.0
✓ 成功率 >= 95%
✓ 報告されたバグが全て修正
✓ ドキュメントが完全に更新
✓ パフォーマンスが安定
```

---

#### Stage 3: Published（公開）

**目的:** 全チームでの利用開始

**期間:** 継続

**活動:**
```yaml
学習・採用支援:
  - オンボーディング資料の提供
  - デモセッションの開催
  - チームへの告知メール

利用監視:
  - 採用率の追跡
  - エラーログの監視
  - サポートチケット対応

品質維持:
  - 週1回のメトリクスレビュー
  - バグ報告への対応（SLA: 2営業日以内）
  - パフォーマンス監視
```

**SLA（サービスレベルアグリーメント）:**
```
重大度     レスポンス時間    修正目標時間
──────────────────────────────
Critical   1時間以内        24時間以内
High       4時間以内        3日以内
Medium     1営業日以内      1週間以内
Low        2営業日以内      2週間以内
```

**成果物:**
```
□ Weekly Metrics Report
□ Support Ticket Log
□ Performance Dashboard
□ User Documentation Updates
```

---

#### Stage 4: Mature（成熟）

**目的:** 長期安定運用

**期間:** 6ヶ月〜2年

**指標:**
```
✓ 利用者数が安定
✓ エラー率が低い（< 2%）
✓ 新規バグがない（< 1件/月）
✓ ユーザー満足度が高い（>= 4.2/5.0）
✓ パフォーマンス最適化が完了
```

**活動:**
```yaml
最小限の監視:
  - 月1回のメトリクスレビュー
  - 定期メンテナンス（セキュリティパッチ等）
  - サポート引き継ぎ

拡張・統合:
  - 新機能提案の検討
  - 他スキルとの統合
  - パフォーマンス最適化
```

---

#### Stage 5: Deprecated（廃止予定）

**目的:** スキルの段階的な廃止

**期間:** 3ヶ月

**廃止判定基準:**
```
以下のいずれかに該当する場合、廃止を検討：

□ 採用率が3ヶ月連続で50%以下
□ よりよい代替スキルが出現
□ 関連技術が廃止予定（言語のEOL等）
□ メンテナンスコストが高い
□ セキュリティリスクがある
```

**廃止プロセス:**
```
Month 1: Deprecated 宣言
──────────────────────────
□ ステータスを "deprecated" に変更
□ 全ドキュメントに "DEPRECATED" マークを追加
□ 代替スキル（あれば）の推奨
□ チーム全体への告知メール（重要度：高）
□ スキルレジストリから検索結果から除外

Month 2: 移行支援
──────────────────────────
□ 移行ガイド作成
□ 移行ワークショップ実施
□ 個別チームへのサポート提供
□ Q&Aフォーラムでの支援

Month 3: サンセット
──────────────────────────
□ 最終期限を設定（例：3ヶ月後）
□ 最終リマインダーメール送信
□ アーカイブ URL に移動
□ 本番環境から削除
```

**廃止時の確認:**
```
□ 全ユーザーが移行完了したか
□ 記録・履歴がアーカイブされたか
□ 代替スキルが十分に成熟しているか
□ サポート体制が廃止可能か
```

---

### バージョン管理戦略

#### Semantic Versioning

```
Version: MAJOR.MINOR.PATCH

MAJOR: 破壊的変更
  例：パラメータ削除、データ型変更、出力形式変更
  更新：1.0.0 → 2.0.0

MINOR: 後方互換製品互換性を保った新機能追加
  例：新しいオプションパラメータ、拡張された出力形式
  更新：1.0.0 → 1.1.0

PATCH: 後方互換性を保ったバグ修正・改善
  例：パフォーマンス改善、ドキュメント修正、内部リファクタリング
  更新：1.0.0 → 1.0.1

Pre-release: リリース前のテストバージョン
  例：1.0.0-alpha.1, 1.0.0-beta.1, 1.0.0-rc.1
```

#### 互換性维持の原則

```
版上げなしでの変更（パッチ版）:
✓ バグ修正
✓ パフォーマンス改善
✓ ドキュメント更新
✓ 内部コード整理
✓ エラーメッセージ改善

MINOR版上げが必要な変更:
✓ 新しいオプションパラメータ追加（デフォルト値あり）
✓ 新しい出力フィールド追加
✓ 対応言語の拡張
✓ 新しいフレームワークサポート追加

MAJOR版上げが必要な変更:
✓ 既存パラメータ削除
✓ パラメータ名変更
✓ パラメータ型変更
✓ 出力形式の大幅変更
✓ デフォルト動作の変更
```

#### バージョン管理の実装

```yaml
CHANGELOG.md:
---
## [2.0.0] - 2026-03-15

### Changed
- BREAKING: Renamed parameter `style` to `docstyle` (#123)
- BREAKING: Changed output format from string to JSON object (#128)

### Added
- New `include_examples` boolean parameter (default: true)
- Support for Sphinx documentation style

### Deprecated
- Parameter `old_parameter` (will be removed in v3.0.0)

### Fixed
- Fixed timeout issue with large code snippets (#119)
- Fixed incorrect formatting in certain edge cases (#124)

## [1.2.0] - 2026-02-28

### Added
- Support for Go language
- New `detailLevel` parameter for output customization

### Fixed
- Performance improvement for large inputs

---

version.json:
{
  "current": "2.0.0",
  "previous": ["1.2.0", "1.1.0", "1.0.0"],
  "latest": "2.0.0",
  "lts": "1.2.0",
  "supportedVersions": ["2.0.0", "1.2.0"],
  "deprecatedVersions": ["1.1.0", "1.0.0"],
  "eolDate": "2023-06-01"
}
```

---

### スキル更新プロセス

#### 計画フェーズ（1週間）

```
□ 変更内容の分析
  - 互換性への影響を評価
  - バージョン番号を決定
  - 移行方法を計画

□ 変更の優先度を評価
  - ユーザーへの影響度
  - 追加される価値
  - 実装の複雑さ

□ リリース計画
  - 目標リリース日を設定
  - テストスケジュール
  - コミュニケーション計画
```

#### 開発フェーズ（1-2週間）

```
□ コード変更
  - 新機能実装
  - バグ修正
  - 内部最適化

□ テスト
  - 回帰テスト（変わらない部分が正常に動作するか）
  - 新機能テスト
  - 互換性テスト（古いバージョンのuser cases）

□ ドキュメント更新
  - パラメータ説明の更新
  - 使用例の追加
  - CHANGELOG の作成
  - 移行ガイド（MAJOR版の場合）
```

#### ベータテスト（1-2週間）

```
□ リミテッドリリース
  - 10人程度の限定ユーザーで検証
  - フィードバック収集

□ 問題対応
  - 報告されたバグを修正
  - フィードバックを反映
```

#### リリース（1日）

```
□ リリース実行
  - パッケージを公開（PyPI/npm等）
  - リポジトリにタグを付与
  - ドキュメントサイト更新
  - リリースノート公開

□ 告知
  - チーム全体にメール送信
  - チャットに投稿
  - 必要に応じてデモセッション開催
```

#### サポート（継続）

```
□ ホットスター対応
  - 重大なバグへの即座の対応
  - ユーザーサポート強化
  - 質問・不具合の事前対応
```

---

### 依存関係管理

#### スキル間の依存関係

```
例：実務的なスキル間の依存関係

generate-unit-tests
  ├── depends: analyze-code-quality
  │   (テスト前にコード品質を確認)
  └── depends: import test data
      (テストデータ生成スキルなど)

optimize-performance
  └── depends: analyze-code-quality
      (性能最適化前に品質分析)

generate-documentation
  └── depends: parse-code (内部スキル)
```

#### 依存関係の管理

```json
{
  "dependencies": {
    "analyze-code-quality": {
      "version": ">=1.0.0, <2.0.0",
      "required": false,
      "description": "Optional: analyze code before optimization"
    },
    "import-test-data": {
      "version": ">=1.1.0",
      "required": true,
      "description": "Required for test case generation"
    }
  },
  "dependents": [
    "optimize-performance",
    "database-migration-helper"
  ]
}
```

#### 破壊的変更時の処理

```
スキルA v1.0 を v2.0 に更新し、
出力形式が変わる場合：

1. 事前通知（2週間前）
   □ 依存スキルのオーナーに通知

2. 段階的な廃止
   □ v1.0 のサポート期間を明確化
   □ v1.0 → v2.0 移行スケジュール提示

3. 互換性レイヤーの提供（optional）
   □ v1互換モードをv2で提供
   □ 段階的な削除計画
```

---

### セキュリティ と メンテナンス

#### セキュリティパッチ対応

```
発見後の対応：
1. 評価（1時間以内）
  - 重大度判定
  - 影響範囲確認

2. 修正開発（4時間以内）
  - パッチコードの実装
  - クイックテスト

3. 公開（24時間以内）
  - ホットフィックスリリース
  - セキュリティアラート配信

4. フォローアップ
  - 利用者への対応確認
  - 根本原因分析
```

#### 依存関係のセキュリティアップデート

```
Weekly:
□ 依存する外部ライブラリをスキャン
□ 脆弱性データベースを確認
□ 必要なアップデートをリスト化

Bi-weekly:
□ 脆弱性なしの依存パッケージをアップデート
□ テース実行
□ リリース（パッチ版）

Critical:
□ 緊急のセキュリティパッチは即座に適用
□ ホットフィックス版を公開
```

---

### 長期運用のベストプラクティス

| 側面 | ベストプラクティス |
|------|-----------------|
| **バージョニング** | Semantic Versioning を厳密に従う |
| **後方互換性** | 可能な限り保つ（MAJOR版でのみ破棄） |
| **段階的廃止** | 最低3ヶ月の通知期間を確保 |
| **ドキュメント** | コード変更と同時に更新 |
| **テスト** | リグレッションテストを自動化 |
| **SLA** | レベル別に明確に定義 |
| **監視** | メトリクス追跡きランダッシュボード |
| **コミュニケーション** | 変更予定は事前に共有 |

---

### 実装チェックリスト

```
ライフサイクル管理：
□ 各ステージの入口・出口基準を定義
□ ステージ遷移の責任者を指定
□ ライフサイクル管理ツール（GitHub Projects等）を導入

バージョン管理：
□ Semantic Versioning ルール文書化
□ 互換性マトリックス作成
□ CHANGELOG テンプレート作成

更新プロセス：
□ 更新プロセス文書化
□ チェックリスト化
□ 自動化可能な部分（テスト等）を自動化

セキュリティ：
□ セキュリティスキャンを自動化
□ セキュリティパッチ対応 SLA を定義
□ ホットフィックスプロセスを確立
```

---

### まとめ

| ステージ | 期間 | 焦点 | 成功基準 |
|--------|-----|------|---------|
| Draft | 1-2w | スキル設計・実装 | テストが全て成功 |
| Beta | 2-4w | ユーザーフィードバック | 満足度4.0以上 |
| Published | 継続 | 採用・学習支援 | 採用率70%以上 |
| Mature | 6m-2y | 安定運用 | エラー率 < 2% |
| Deprecated | 3m | 段階的廃止 | ユーザー移行完了 |

→ 次へ: [Part 4-3: パフォーマンス最適化](#section-04-advanced-03-optimization)

## Part 4-3: パフォーマンス最適化と監視 {#section-04-advanced-03-optimization}


スキルのパフォーマンスを測定し、ボトルネックを特定して最適化する方法を学びます。

---

### パフォーマンスのキーメトリクス

#### 実行時間の最適化

```
目標実行時間の設定：

スキルタイプ          目指すべき実行時間   最大許容時間
─────────────────────────────────────────────────
分析スキル            1-3秒              5秒
生成スキル            2-5秒              10秒
テストスキル          3-8秒              15秒
複雑な処理            5-10秒             20秒
```

#### メトリクス追跡の例

```json
{
  "execution_time_metrics": {
    "min": 1.2,
    "max": 8.5,
    "avg": 3.4,
    "median": 3.1,
    "p99": 7.8,
    "p95": 6.2,
    "p90": 5.1,
    "trend": "stable"
  },
  "success_rate": 98.5,
  "error_types": {
    "timeout": 0.8,
    "invalid_input": 0.4,
    "api_error": 0.3
  },
  "throughput": {
    "requests_per_minute": 45,
    "concurrent_users": 12
  }
}
```

---

### 実行時間のプロファイリング

#### プロンプト処理時間の分析

```
ユーザーリクエスト
    ↓ [100ms] 入力バリデーション
パラメータ解析
    ↓ [50ms] テンプレート変数展開
プロンプト構築
    ↓ [2000ms] LLM 処理 ★ ボトルネック
LLM レスポンセ
    ↓ [100ms] 出力フォーマット
ユーザーへの返却

合計時間: 約2250ms

最適化の機会:
1. LLM処理 (40% → 30%): プロンプト簡潔化
2. テンプレート処理 (2% → 1%): キャッシング
3. 入力バリデーション (4% → 2%): 最適化
```

---

### パフォーマンス計測スクリプト

#### performance-profiler.py（推奨実装）

以下は、スキルのパフォーマンスを包括的に計測・分析するPythonスクリプトの例です。

```python
#!/usr/bin/env python3
\"\"\"Performance profiler for Copilot Skills\"\"\"

import time
import json
from functools import wraps
from datetime import datetime
from typing import Dict, Any

class PerformanceProfiler:
    \"\"\"各段階のパフォーマンスを計測・分析\"\"\"
    
    def __init__(self, skill_name: str, target_exec_time_ms: float = 5000):
        self.skill_name = skill_name
        self.target_time = target_exec_time_ms / 1000  # 秒に変換
        self.measurements = {}
    
    def measure(self, func):
        \"\"\"デコレータで実行時間を計測\"\"\"
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            
            func_name = func.__name__
            if func_name not in self.measurements:
                self.measurements[func_name] = []
            self.measurements[func_name].append(elapsed)
            
            return result
        return wrapper
    
    def generate_report(self) -> Dict[str, Any]:
        \"\"\"詳細レポート生成\"\"\"
        report = {\"skill\": self.skill_name, \"stages\": {}, \"summary\": {}}
        total = sum(sum(t) for t in self.measurements.values())
        
        for stage, timings in self.measurements.items():
            avg = sum(timings) / len(timings)
            report[\"stages\"][stage] = {
                \"count\": len(timings),
                \"avg_ms\": avg * 1000,
                \"min_ms\": min(timings) * 1000,
                \"max_ms\": max(timings) * 1000,
                \"pct\": (sum(timings) / total * 100) if total > 0 else 0
            }
        
        report[\"summary\"][\"total_ms\"] = total * 1000
        report[\"summary\"][\"status\"] = (
            \"Excellent\" if total < self.target_time * 0.7 else
            \"Good\" if total < self.target_time else
            \"Needs Optimization\"
        )
        
        return report
    
    def print_report(self):
        \"\"\"見やすいレポート表示\"\"\"
        report = self.generate_report()
        print(f\"\\n{'='*60}\\n📊 {report['skill']}\\n{'='*60}\")
        
        for stage, metrics in report[\"stages\"].items():
            print(f\"{stage}: {metrics['avg_ms']:.1f}ms avg \"\n                  f\"({metrics['pct']:.1f}%) - Min: {metrics['min_ms']:.1f}ms, \"\n                  f\"Max: {metrics['max_ms']:.1f}ms\")
        
        summary = report[\"summary\"]
        print(f\"\\n⏱️  Total: {summary['total_ms']:.1f}ms | Status: {summary['status']}\")
        print(f\"{'='*60}\\n\")

# 使用例
if __name__ == \"__main__\":
    profiler = PerformanceProfiler(\"analyze-code-quality\")
    
    @profiler.measure
    def validate(): time.sleep(0.1)
    
    @profiler.measure  
    def build_prompt(): time.sleep(0.05)
    
    @profiler.measure
    def call_llm(): time.sleep(2.0)
    
    @profiler.measure
    def format(): time.sleep(0.1)
    
    # 実行＆レポート
    validate()
    build_prompt()
    call_llm()
    format()
    profiler.print_report()
```

#### 段階別の最適化

```python
# 実装例：パフォーマンス計測

import time
from functools import wraps

def measure_performance(func):
    """デコレータで各段階のパフォーマンスを計測"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__}: {duration:.3f}s")
        return result
    return wrapper

# 各段階の計測
@measure_performance
def validate_input(params):
    # 入力バリデーション
    pass

@measure_performance
def build_prompt(template, variables):
    # プロンプト構築
    pass

@measure_performance
def call_llm(prompt):
    # LLM呼び出し
    pass

@measure_performance
def format_output(raw_output):
    # 出力フォーマット
    pass
```

---

### プロンプト最適化による高速化

#### テクニック1: プロンプト圧縮

```
最適化前（2000トークン）:
─────────────────────
"You are an expert code reviewer. Your role is to analyze 
Python code and provide detailed feedback on multiple dimensions. 
You should consider code readability, performance issues, 
security vulnerabilities, and testability. For each issue found, 
provide the line number, issue type, severity level (critical, 
high, medium, low), detailed explanation, and recommended fix. 
Format your response as a JSON..."

処理時間: 2500ms

最適化後（800トークン）:
──────────────────────
"Review Python code across: readability, performance, security, 
testability. For each issue list: line number, type (critical/
high/medium/low), explanation, fix. Output as JSON with 
structure: {issues: [{line, type, severity, explanation, fix}]}"

処理時間: 800ms
→ 68% の処理時間削減
```

#### テクニック2: 条件付き処理

```python
def generate_prompt(template, variables, detail_level):
    """detail_levelに応じてプロンプトサイズを調整"""
    
    base_prompt = f"Your task: {template}\n"
    
    if detail_level == "brief":
        # 必須情報のみ
        prompt = base_prompt + f"Input: {variables['code']}\nOutput: JSON"
        
    elif detail_level == "standard":
        # 一般的な詳細度
        prompt = base_prompt + f"""
Input code:
{variables['code']}

Focus areas: {variables['focus_areas']}
Output format: JSON with issues and recommendations
"""
        
    elif detail_level == "comprehensive":
        # 詳細な指示
        prompt = base_prompt + f"""
Input code:
{variables['code']}

Analyze these dimensions:
{variables['dimensions']}

For each issue provide:
- Line number and code snippet
- Type and severity
- Explanation and fix
- Testing strategy

Output: JSON with full details
"""
    return prompt
```

#### テクニック3: キャッシング

```json
キャッシング戦略

静的なプロンプト部分をキャッシュ:
{
  "cache": {
    "system_prompt": false,  // システムプロンプトは毎回
    "parameter_definitions": true,  // パラメータ定義は再利用可
    "output_schema": true,    // 出力スキーマは再利用可
    "examples": true,         // 使用例は再利用可
    "ttl": 3600               // 1時間のキャッシュ
  }
}

キャッシュキーの生成:
hash(language + output_format + detail_level + focus_areas)

例：
Input 1: Python, JSON, standard, [readability, security]
  → Cache Key: abc123 (初回キャッシュ)

Input 2: Python, JSON, standard, [readability, security]
  → Cache Key: abc123 (キャッシュヒット!)
  → 処理時間削減: 2500ms → 100ms
```

---

### 並列処理による高速化

#### 複数スキルの並列実行

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def analyze_code_parallel(code_samples):
    """複数のコード分析を並列実行"""
    
    tasks = [
        asyncio.create_task(analyze_readability(code))
        for code in code_samples
    ]
    
    # すべてが完了するまで待機
    results = await asyncio.gather(*tasks)
    return results

# 実行時間の比較
# 順序実行: 5 samples × 2秒 = 10秒
# 並列実行: max(2秒, 2秒, 2秒, ...) = 2秒
# 高速化: 5倍!
```

#### スキル内での並列処理

```json
複雑なテスト生成スキルの場合：

順序処理フロー:
正常系テスト生成 (3秒) → 
エッジケーステスト生成 (2秒) → 
エラーケーステスト生成 (2秒) → 
合計: 7秒

並列処理フロー:
正常系テスト生成 (3秒) ┐
エッジケーステスト生成 (2秒) ├→ max = 3秒
エラーケーステスト生成 (2秒) ┘
合計: 3秒

効果: 7秒 → 3秒 (57% 削減)
```

---

### メモリ効率の改善

#### 大規模入力の処理

```python
# ❌ 非効率：全体をメモリに読み込む
def analyze_large_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()  # メモリオーバーフロー！
    return analyze(content)

# ✓ 効率的：チャンク処理
def analyze_large_file_chunked(file_path, chunk_size=1000):
    results = []
    with open(file_path, 'r') as f:
        chunk = ""
        for line in f:
            chunk += line
            if len(chunk) >= chunk_size:
                results.append(analyze_chunk(chunk))
                chunk = ""
        if chunk:
            results.append(analyze_chunk(chunk))
    return merge_results(results)
```

---

### スキルの監視と診断

#### リアルタイム監視ダッシュボード

```
┌──────────────────────────────────────────┐
│   Copilot Skills Performance Dashboard   │
├──────────────────────────────────────────┤
│                                          │
│ Skill: analyze-code-quality              │
│                                          │
│ Status: ✓ Healthy                        │
│                                          │
│ Last 60 minutes:                         │
│ • Response time: 3.2s ± 0.8s (avg)       │
│ • Success rate: 98.2%                    │
│ • Requests: 1,245/min                    │
│ • Error rate: 1.8%                       │
│ • P99 latency: 5.1s                      │
│                                          │
│ Errors:                                  │
│ ├─ Timeout (0.8%)                        │
│ ├─ Invalid input (0.6%)                  │
│ └─ API error (0.4%)                      │
│                                          │
│ Recommendations:                         │
│ • Response time増加傾向 → キャッシュの確認
│ • エラー率わずかに上昇 → LLM APIの状態確認
│                                          │
└──────────────────────────────────────────┘
```

#### ログとアラート

```yaml
monitoring:
  metrics:
    response_time:
      warning_threshold: 5.0s
      critical_threshold: 10.0s
      alert_message: "Skill response time exceeded threshold"
    
    error_rate:
      warning_threshold: 5%
      critical_threshold: 10%
      alert_message: "Error rate exceeds threshold"
    
    success_rate:
      warning_threshold: 95%
      critical_threshold: 90%
      alert_message: "Success rate fell below threshold"
  
  logging:
    format: "json"
    fields:
      - timestamp
      - skill_id
      - request_id
      - response_time
      - status_code
      - error_type (if any)
      - user_id
      - parameters_hash
```

---

### スケーリング戦略

#### 段階的なスケーリング

```
Phase 1: 単一インスタンス（1-100 req/min）
┌─────────────────────┐
│  Copilot Skill API  │ (1インスタンス)
└─────────────────────┘
処理能力: 最大100 req/min

Phase 2: 複数インスタンス + ロードバランサー（100-500 req/min）
┌──────────────────────────────┐
│   Load Balancer              │
├──────────────────────────────┤
│ Instance 1 │ Instance 2 │ Instance 3
│ (50req/min)│ (50req/min)│ (50req/min) → 合計150 req/min
└──────────────────────────────┘

Phase 3: オートスケーリング + キャッシュ（500+ req/min）
┌──────────────────────────────┐
│   Kubernetes Orchestration    │
│   (自動スケーリング)           │
├──────────────────────────────┤
│ Distributed Cache (Redis)    │
└──────────────────────────────┘
```

---

### トラブルシューティング

#### 問題1: 急激な速度低下

```
診断ステップ：

1. メトリクス確認
   □ 平均応答時間が増加しているか
   □ エラー率が増加しているか
   □ メモリ使用率が高くなっているか

2. LLM側の問題確認
   □ LLM API のレイテンシをチェック
   □ レート制限に達しているか
   □ API status page を確認

3. スキル側の問題確認
   □ 最近の変更を確認
   □ プロンプットサイズが増加していないか
   □ 依存スキルの状態確認

4. 対応策
   □ キャッシュを有効化
   □ プロンプット圧縮
   □ インスタンス数を増加
   □ レート制限を調整
```

#### 問題2: 高いエラー率

```
根本原因分析：

エラータイプ別対応：

Timeout エラー (> 20% of errors):
  原因: プロンプットが大きすぎる、LLMが遅い
  対応: 
    □ プロンプット簡潔化
    □ タイムアウト値調整
    □ リトライロジック追加

Invalid Input エラー:
  原因: ユーザー入力の検証不足
  対応:
    □ 入力検証を強化
    □ エラーメッセージを改善
    □ 使用例を充実

API エラー:
  原因: 外部API（LLM）の信頼性
  対応:
    □ リトライ戦略の導入
    □ フォールバック実装
    □ サーキットブレーカーパターン
```

---

### パフォーマンステスト

#### ロードテストの実施

```python
import concurrent.futures
import time

def load_test_skill(skill_id, num_requests=1000, concurrency=10):
    """スキルのロードテスト"""
    
    results = {
        'total_requests': num_requests,
        'response_times': [],
        'errors': 0,
        'start_time': time.time()
    }
    
    def make_request():
        try:
            start = time.time()
            response = call_skill(skill_id, sample_params)
            elapsed = time.time() - start
            return elapsed, True
        except Exception as e:
            return None, False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        
        for future in concurrent.futures.as_completed(futures):
            elapsed, success = future.result()
            if success:
                results['response_times'].append(elapsed)
            else:
                results['errors'] += 1
    
    results['duration'] = time.time() - results['start_time']
    results['avg_response_time'] = sum(results['response_times']) / len(results['response_times'])
    results['error_rate'] = results['errors'] / num_requests * 100
    
    return results

# テスト結果
test_results = load_test_skill('analyze-code-quality', num_requests=100, concurrency=5)
print(f"Average Response Time: {test_results['avg_response_time']:.2f}s")
print(f"Error Rate: {test_results['error_rate']:.1f}%")
```

---

### 実装チェックリスト

```
パフォーマンス最適化：
□ キーメトリクスを定義（実行時間、成功率など）
□ プロンプト最適化（圧縮、条件付き処理）
□ キャッシング戦略を実装
□ 並列処理を導入（可能な場合）
□ メモリ効率を改善

監視・診断：
□ リアルタイムダッシュボードを構築
□ アラート機構を実装
□ ロギングを確立
□ SLA を定義

スケーリング：
□ ロードテスト計画を立案
□ スケーリングアーキテクチャを設計
□ オートスケーリング構成
□ キャッシュインフラ（Redis等）の検討
```

---

### ベストプラクティス

| 側面 | ポイント |
|------|---------|
| **計測** | 本番環境で継続的に計測、メトリクスベースの最適化 |
| **プロンプト** | シンプルで明確、不要な詳細は削除 |
| **キャッシング** | 静的部分を徹底的にキャッシュ |
| **並列化** | 独立した処理は並列実行 |
| **監視** | プロアクティブなアラート (反応的ではなく) |
| **段階的改善** | 一度にすべて最適化せず、優先順位を付けて改善 |

→ 次へ: [Part 4-4:トラブルシューティング](#section-04-advanced-04-troubleshooting)

## Part 4-4: トラブルシューティングと問題解決 {#section-04-advanced-04-troubleshooting}


実運用で発生しやすい問題と解決方法を実装例付きで解説します。

### 現場運用でよく使う用語

| 用語 | 意味（本教材での定義） |
|------|------------------------|
| runbook | 現場向けの作業手順書 |
| remediation | 不具合の是正対応 |
| gate | 次に進むための確認ポイント |
| evidence / trace | 作業証跡 |
| scope | 対象範囲 |
| rollout | 横展開 |

#### 運用フローの要点

runbookに沿って、確認ポイント（gate）を通過しながら、証跡（evidence/trace）を残して、対象範囲（scope）を漏れなく是正（remediation）し、最後に横展開（rollout）する。

詳細な手法・テンプレートは以下を参照:

- [Part 4-7: 運用手法（Runbook / Gate / Evidence / Scope / Rollout）](#section-04-advanced-07-operations-methodology)

---

### よくある問題と解決策

#### 問題カテゴリ

```
スキル開発者向け (Development Issues)
  ├─ スキル定義エラー
  ├─ プロンプトの精度不足
  ├─ パフォーマンス問題
  └─ テスト失敗

ユーザー向け (Usage Issues)
  ├─ スキルが見つからない
  ├─ 使い方がわからない
  ├─ 予期しない結果
  └─ エラーが発生

運用チーム向け (Operations Issues)
  ├─ 依存スキルの問題
  ├─ 互換性破損
  ├─ スケーリング問題
  └─ セキュリティ懸念
```

---

### 問題1: スキル定義エラー

#### 問題: JSONスキーマが無効

```
エラーメッセージ：
"InvalidSkillDefinition: JSON validation failed"

❌ 原因の例：

{
  "parameters": {
    "code": {
      "type": "string",
      "required": true    // ❌ "required" は parameters.codeプロパティではなく、
                          //   parameters配列で指定すべき
    }
  }
}

✓ 正しい定義：

{
  "parameters": {
    "code": {
      "type": "string",
      "description": "Code to analyze"
    }
  },
  "requiredParameters": ["code"]  // または jsonschemaの "required"
}
```

#### 解決方法

```python
# JSONスキーマの検証ツール

import json
import jsonschema

def validate_skill_definition(skill_json_path):
    """スキル定義を検証"""
    
    with open(skill_json_path, 'r') as f:
        skill = json.load(f)
    
    # 必須フィールドの確認
    required_fields = ['id', 'version', 'name', 'parameters', 'prompt', 'outputFormat']
    for field in required_fields:
        if field not in skill:
            raise ValueError(f"Missing required field: {field}")
    
    # JSONスキーマの検証
    skill_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
            "version": {"type": "string", "pattern": "^[0-9]+\.[0-9]+\.[0-9]+$"},
            "parameters": {"type": "object"}
        },
        "required": required_fields
    }
    
    try:
        jsonschema.validate(skill, skill_schema)
        print("✓ Skill definition is valid")
        return True
    except jsonschema.ValidationError as e:
        print(f"❌ Validation error: {e.message}")
        return False

# 使用
validate_skill_definition('skill-definition.json')
```

---

#### 問題: 不正なパラメータ定義

```
❌ 悪い例：

{
  "parameters": {
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "java"],
      "default": "c++"  // ❌ enum に c++ が含まれていない
    }
  }
}

✓ 修正：

{
  "parameters": {
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "java", "c++"],
      "default": "python"  // enum に含まれる値に変更
    }
  }
}
```

#### チェックリスト（スキル定義の検証）

```
□ JSON 形式が正しい（JSONLint等で確認）
□ 全ての必須フィールドが存在
  ├─ id (英数字とハイフンのみ)
  ├─ version (X.Y.Z形式)
  ├─ name
  ├─ parameters
  ├─ prompt (system + template)
  └─ outputFormat
□ 補助リソース（スクリプト等）のチェック
  ├─ scripts/ ディレクトリが存在するか
  ├─ 各スクリプトが実行可能か（chmod +x）
  ├─ スクリプト言語がドキュメント化されているか
  └─ 依存パッケージがrequirements.txt等で指定されているか
□ templates/ フォルダが存在する場合
  ├─ 各テンプレートが有効な形式か
  └─ パス参照が正しいか
```

#### 補助スクリプト：自動検証ツール（skill-validator.py）

スキル定義と補助リソースを自動で検証するツール：

```python
#!/usr/bin/env python3
"""Skill definition validator with auxiliary resource checks"""

import json
import os
import re
import sys
from pathlib import Path

class SkillValidator:
    """スキル定義と補助リソースを検証"""
    
    REQUIRED = ['id', 'version', 'name', 'description', 'parameters', 'prompt', 'outputFormat']
    ID_PATTERN = re.compile(r'^[a-z0-9-]+$')
    VERSION_PATTERN = re.compile(r'^\d+\.\d+\.\d+$')
    
    def __init__(self, skill_dir: str):
        self.skill_dir = Path(skill_dir)
        self.skill_file = self.skill_dir / 'SKILL.md.json'
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """検証実行"""
        if not self.skill_file.exists():
            self.errors.append(f"❌ Skill file not found: {self.skill_file}")
            return False
        
        try:
            with open(self.skill_file) as f:
                self.skill = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"❌ Invalid JSON: {e}")
            return False
        
        # 各検証を実行
        self._validate_required_fields()
        self._validate_id_format()
        self._validate_version_format()
        self._validate_auxiliary_resources()
        
        return len(self.errors) == 0
    
    def _validate_required_fields(self):
        """必須フィールド確認"""
        for field in self.REQUIRED:
            if field not in self.skill:
                self.errors.append(f"❌ Missing field: {field}")
    
    def _validate_id_format(self):
        """ID形式確認"""
        skill_id = self.skill.get('id', '')
        if not self.ID_PATTERN.match(skill_id):
            self.errors.append(f"❌ Invalid ID format: {skill_id}")
    
    def _validate_version_format(self):
        """バージョン形式確認"""
        version = self.skill.get('version', '')
        if not self.VERSION_PATTERN.match(version):
            self.errors.append(f"❌ Invalid version format: {version}")
    
    def _validate_auxiliary_resources(self):
        """補助リソース確認"""
        aux = self.skill.get('auxiliaryResources', {})
        if not aux:
            return
        
        # スクリプト確認
        scripts = aux.get('scripts', [])
        scripts_dir = self.skill_dir / 'scripts'
        
        for script in scripts:
            script_name = script.get('name')
            script_path = scripts_dir / script_name
            
            if not script_path.exists():
                self.warnings.append(f"⚠️  Script not found: {script_path}")
            elif not os.access(script_path, os.X_OK):
                self.warnings.append(f"⚠️  Script not executable: {script_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python skill-validator.py <skill-directory>")
        sys.exit(1)
    
    validator = SkillValidator(sys.argv[1])
    is_valid = validator.validate()
    print(f"Valid: {is_valid} (Errors: {len(validator.errors)}, Warnings: {len(validator.warnings)})")
    sys.exit(0 if is_valid else 1)
```

**使用例：**

```bash
python3 skill-validator.py skills/analyze-code-quality/
```

□ パラメータの定義が正しい
  ├─ type が正当な値
  ├─ required フラグが正しい
  ├─ default 値が型と一致
  ├─ enum 時に default が enum に含まれる
  └─ minLength/maxLength 等の制約が論理的

□ プロンプトテンプレートの変数名が全て有効
  └─ {variable_name} がパラメータに対応

□ 出力スキーマが実装と整合
  └─ required フィールドが全て出力される
```

---

## 問題2: プロンプト精度の問題

### 問題: 出力形式が指定通りでない

```
期待：JSON形式
{
  "result": "success",
  "score": 85
}

実際：テキスト形式
"The analysis shows a score of 85 and is successful."

❌ 原因：プロンプトが曖昧

"Return your analysis."  // 何形式でかが不明

✓ 修正：明確な指示

"Return your analysis as valid JSON with this exact structure:
{
  \"result\": \"<success|failure>\",
  \"score\": <0-100>
}

Example:
{
  \"result\": \"success\",
  \"score\": 85
}"
```

### 出力フォーマット検証の実装

```python
import json
import re
from typing import Union

def validate_output_format(output: str, expected_format: str) -> Union[dict, str, bool]:
    """出力形式を検証"""
    
    if expected_format == "json":
        # JSON形式の検証
        try:
            # JSONブロックを抽出（```json ... ``` に囲まれている可能性）
            json_match = re.search(r'```json\n(.*?)\n```', output, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = output
            
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON output: {e}")
    
    elif expected_format == "text":
        # テキスト形式（常に有効）
        return output
    
    elif expected_format == "boolean":
        # ブール値形式
        normalized = output.lower().strip()
        if normalized in ['true', 'yes', '1']:
            return True
        elif normalized in ['false', 'no', '0']:
            return False
        else:
            raise ValueError(f"Cannot parse as boolean: {output}")

# 使用例
def test_output_format():
    # テスト1: 正しいJSON
    valid_json = '{"result": "success", "score": 85}'
    assert validate_output_format(valid_json, "json") == {"result": "success", "score": 85}
    
    # テスト2: 不正なJSON
    invalid_json = '{"result": "success" score: 85}'  # コロン不足
    try:
        validate_output_format(invalid_json, "json")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Caught error: {e}")
    
    # テスト3: JSONブロック形式
    json_block = """
    ```json
    {"result": "success"}
    ```
    """
    assert validate_output_format(json_block, "json") == {"result": "success"}
```

### プロンプト改善のテンプレート

```
現在のプロンプト：
"Analyze this code and tell me about the quality."

改善されたプロンプト：
"Analyze the provided code for quality issues.

Focus on:
1. Readability (variable names, structure)
2. Performance (efficiency, complexity)
3. Security (vulnerabilities, best practices)
4. Testability (test coverage, structure)

Return results as JSON:
{
  \"readability\": {\"score\": <0-100>, \"issues\": [...]},
  \"performance\": {\"score\": <0-100>, \"issues\": [...]},
  \"security\": {\"score\": <0-100>, \"issues\": [...]},
  \"testability\": {\"score\": <0-100>, \"issues\": [...]}
}

Each issue should include:
- line_number: where in the code
- severity: critical, high, medium, low
- description: what's wrong
- suggestion: how to fix it"
```

---

## 問題3: スキルが見つからない（ユーザー側）

### 原因の特定

```yaml
診断フロー：

1. スキルレジストリに登録されているか？
   □ REGISTRY.md に listed されているか
   □ リポジトリのスキル一覧に含まれているか
   □ パッケージレジストリ（PyPI/npm）に公開されているか

2. ユーザーがアクセス権を持っているか？
   □ プライベートスキル か? → アクセス権の確認
   □ 組織内限定スキル か? → チームメンバーシップの確認

3. スキル名の問題か?
   □ 正しいスキル ID を使用しているか
   □ 大文字小文字の区別の有無

4. Copilot のセットアップが正しいか?
   □ Copilot がインストールされているか
   □ 最新版に更新されているか
   □ スキルローダーが有効か
```

### ユーザー向けトラブルシューティング

```markdown
# "スキルが見つからない"時の対応

1. **スキルが存在するか確認**
   ```
   スキルレジストリを確認:
   https://github.com/org/copilot-skills/blob/main/REGISTRY.md
   ```

2. **スキル ID が正しいか確認**
   ```
   スキル ID は小文字とハイフンのみ
   例: generate-unit-tests ✓
      GenerateUnitTests ✗
      generate_unit_tests ✗
   ```

3. **Copilot をインストール/更新**
   ```bash
   # VS Code の場合
   命令パレット > "Github Copilot: Check for updates"
   ```

4. **它の設定確認**
   - Copilot 拡張機能が有効か確認
   - チームのスキルカタログにアクセス権があるか確認

5. **サポートに連絡**
   - スキル名と ID を記載
   - Copilot バージョンを記載
   - エラーメッセージをコピー
```

---

## 問題4: 予期しない結果

### デバッグテクニック

```python
def debug_skill_output(skill_id, parameters, expected_pattern=None):
    """スキル実行をデバッグ"""
    
    import json
    from datetime import datetime
    
    # ログファイルに出力
    debug_log = {
        "timestamp": datetime.now().isoformat(),
        "skill_id": skill_id,
        "parameters": parameters,
        "steps": []
    }
    
    try:
        # Step 1: 入力検証
        debug_log["steps"].append({
            "name": "Input Validation",
            "status": "start"
        })
        validate_parameters(parameters)
        debug_log["steps"][-1]["status"] = "success"
        
        # Step 2: プロンプト構築
        debug_log["steps"].append({
            "name": "Prompt Building",
            "status": "start"
        })
        prompt = build_prompt(skill_id, parameters)
        debug_log["steps"][-1].update({
            "status": "success",
            "prompt_length": len(prompt),
            "prompt_preview": prompt[:500]  # 最初の500文字
        })
        
        # Step 3: LLM呼び出し
        debug_log["steps"].append({
            "name": "LLM Call",
            "status": "start"
        })
        output = call_llm(prompt)
        debug_log["steps"][-1].update({
            "status": "success",
            "output_length": len(output),
            "output_preview": output[:500]
        })
        
        # Step 4: 出力検証
        debug_log["steps"].append({
            "name": "Output Validation",
            "status": "start"
        })
        validate_output(output, skill_id)
        debug_log["steps"][-1]["status"] = "success"
        
        # パターンマッチング（オプション）
        if expected_pattern:
            import re
            if re.search(expected_pattern, output):
                debug_log["pattern_match"] = "matched"
            else:
                debug_log["pattern_match"] = "not_matched"
        
        debug_log["result"] = "success"
        
    except Exception as e:
        debug_log["result"] = "error"
        debug_log["error"] = str(e)
        debug_log["error_type"] = type(e).__name__
    
    # ログを保存・出力
    with open(f"debug_{skill_id}_{datetime.now().timestamp()}.json", 'w') as f:
        json.dump(debug_log, f, indent=2)
    
    print(json.dumps(debug_log, indent=2))
    return debug_log

# 使用例
debug_log = debug_skill_output(
    "analyze-code-quality",
    {"code": "def foo(): pass", "language": "python"},
    expected_pattern=r'"score":\s*\d+'
)
```

### ステップバイステップのデバッグ出力例

```
[2026-03-07 14:30:00] Debugging: generate-documentation

Step 1: Input Validation ✓
  - language: python ✓
  - docstyle: google ✓
  - code_element length: 245 chars ✓

Step 2: Prompt Building ✓
  - Template variables expanded: 8 ✓
  - Prompt length: 1,234 tokens
  - Sample: "Generate documentation in Google style for the following Python..."

Step 3: LLM Call ✓
  - Request time: 2.3s
  - Token usage: 2,100 tokens
  - Response length: 512 chars

Step 4: Output Validation ✓
  - Format: Text ✓
  - Contains expected sections:
    ├─ Summary: ✓
    ├─ Args: ✓
    ├─ Returns: ✓
    └─ Examples: ✓

Pattern Match: "Google style format" ✓

Status: SUCCESS ✓
```

---

## 問題5: パフォーマンス低下

### 症状別診断

```
症状: 実行時間が極端に長い（> 20秒）

診断フロー：

1. 単発テスト vs 継続的な低下
   □ 単発のみ → 一時的な LLM API 遅延
   □ 継続的 → スキル内のボトルネック

2. 特定の条件下のみか?
   □ 特定パラメータ値でのみ → パラメータ依存
   □ 入力サイズに依存 → 入力大きさが問題
   □ 常に → スキル自体の問題

3. 影響範囲
   □ このスキルのみ → スキル固有の問題
   □ 全スキル → インフラ/LLM側の問題

推奨対応：
  - 入力を小さくしてリトライ
  - キャッシュクリア
  - スキル version を確認（回帰がないか）
  - LLM API Status を確認
```

### パフォーマンス計測

```python
import time
import statistics

def measure_skill_performance(skill_id, test_cases, iterations=5):
    """スキルのパフォーマンス計測"""
    
    results = {
        "skill_id": skill_id,
        "test_cases": len(test_cases),
        "iterations": iterations,
        "measurements": []
    }
    
    for i, test_case in enumerate(test_cases):
        case_results = {
            "test_case": i,
            "times": []
        }
        
        for _ in range(iterations):
            start = time.time()
            try:
                output = execute_skill(skill_id, test_case["parameters"])
                elapsed = time.time() - start
                case_results["times"].append(elapsed)
            except Exception as e:
                case_results["error"] = str(e)
                break
        
        if case_results["times"]:
            case_results["stats"] = {
                "min": min(case_results["times"]),
                "max": max(case_results["times"]),
                "avg": statistics.mean(case_results["times"]),
                "median": statistics.median(case_results["times"]),
                "stdev": statistics.stdev(case_results["times"])
            }
        
        results["measurements"].append(case_results)
    
    # 統計
    all_times = [t for m in results["measurements"] if "times" in m for t in m["times"]]
    if all_times:
        results["overall"] = {
            "avg": statistics.mean(all_times),
            "median": statistics.median(all_times),
            "max": max(all_times),
            "p99": sorted(all_times)[int(len(all_times) * 0.99)]
        }
    
    return results

# 使用例
perf_results = measure_skill_performance(
    "analyze-code-quality",
    test_cases=[
        {"parameters": {"code": small_code}},
        {"parameters": {"code": medium_code}},
        {"parameters": {"code": large_code}}
    ],
    iterations=3
)

print("Performance Report:")
print(f"Average: {perf_results['overall']['avg']:.2f}s")
print(f"Median: {perf_results['overall']['median']:.2f}s")
print(f"P99: {perf_results['overall']['p99']:.2f}s")
```

---

## 問題6: 互換性破損

### スキル更新による破損

```
状況：
  - スキル generate-doc を v1.0 → v2.0 に更新
  - パラメータ "style" を "docstyle" に変更
  - v1 で動いていたスクリプトが break

❌ 破損例：
v1.0 で動いていたコード：
{
  "skill": "generate-doc",
  "parameters": {
    "style": "google"  // こういう呼び出し
  }
}

v2.0 にアップデート後：
エラー: "Unknown parameter: style"

✓ 修正（互換性レイヤー）：
v2.0 のスキル定義で:
{
  "parameters": {
    "docstyle": { ... },  // 新しい名前
    "_compat_v1_style": {
      "type": "string",
      "description": "DEPRECATED: use docstyle instead",
      "hidden": true
    }
  }
}

プロンプトテンプレート内：
"{{ docstyle if docstyle else _compat_v1_style }}"
```

### 移行ガイドの作成

```markdown
# v1.x → v2.0 移行ガイド

### 主な変更

#### パラメータ名の変更
| v1.0 | v2.0 |
|------|------|
| `style` | `docstyle` |
| `code_input` | `code_element` |

#### 出力形式の変更
v1.0: テキスト形式
```
def hello():
    """
    Hello world function.
    """
```

v2.0: JSON形式
```json
{
  "documentation": "...",
  "format": "google",
  "sections": {...}
}
```

### 移行ステップ

#### 方法1: 自動に実行（v2.0の互換性モード）
アップデートするだけで動作（推奨）

#### 方法2: 手動移行
1. パラメータ名を更新
2. 出力形式解析を変更
3. テストを再実行

### 問題が発生した場合
v1.0 のサポートは2026-06-01までです。
その後のアップデートでは互換性を保証しません。
```

---

## 実装チェックリスト

```
スキル検証：
□ JSONスキーマをバリデート
□ パラメータ定義をチェック
□ テンプレート変数を確認

プロンプト調整：
□ 出力形式を明確に指定
□ 例を含める
□ エッジケースを言及

デバッグ：
□ デバッグログを実装
□ ステップバイステップの追跡
□ 各段階の出力を確認

パフォーマンス：
□ ベースラインを計測
□ ボトルネックを特定
□ 改善を実装・検証

互換性：
□ CHANGELOG を更新
□ 互換性マトリックスを作成
□ 移行ガイドを提供
```

---

## サポート体制

### 問題報告のテンプレート

```
### Bug Report Template

**Skill:** [skill-id]
**Version:** [version number]
**OS/Environment:** [Windows/macOS/Linux, VS Code version]

**Description:**
[Clear description of the issue]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. ...

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Logs/Screenshots:**
[Include error messages, screenshots]

**Additional Context:**
[Any additional information]
```

### サポート優先度

```
Priority     Response Time    Fix Timeline
──────────────────────────────────────
Critical     1 hour          24 hours
High         4 hours         3 days
Medium       1 day           1 week
Low          2 days          2 weeks
```

---

## 実装チェックリスト

```
エラーハンドリング：
□ 全ての入力エラーをキャッチ
□ LLM エラーに対応
□ タイムアウト処理
□ ユーザーフレンドリーなエラーメッセージ

デバッグ機能：
□ ステップバイステップログ
□ パフォーマンスログ
□ パラメータ/出力のダンプ機能

テスト：
□ 正常系テスト
□ 異常系テスト
□ エッジケーステスト
□ パフォーマンステスト

ドキュメント：
□ トラブルシューティングガイド
□ FAQ
□ サンプルコード
□ よくあるエラーとその解決法
```

---

## まとめ

成功するスキル運用の鍵：

1. **予防** - 良い設計、包括的なテスト
2. **監視** - メトリクス追跡、早期検出
3. **対応** - SLA遵守、素早い修正
4. **学習** - postmortem, 知識共有

困ったときは：
→ [支援チャネル](https://github.com/org/copilot-skills/discussions)
→ [FAQ](FAQ.md)
→ [スキル作成者向けドキュメント](../docs/DEVELOPER_GUIDE.md)

## Part 4-5: スクリプト設計ベストプラクティス {#section-04-advanced-05-scripts-best-practices}


スキルに含める実行可能なスクリプト（Python、Bash、JavaScript等）を効果的に設計するガイドです。

---

### 概要

スキルには単なる指示（Markdown）だけでなく、実行可能なスクリプトを同梱できます。

```
SKILL.md（指示文）
└─ エージェントが読んで理解

scripts/（実行可能）
├─ validate.py      ← エージェントが実行
├─ process.sh       ← 結果をエージェントに返す
└─ analyze.py
```

スクリプト設計の原則を守ることで、エージェントが確実に実行でき、結果を正しく解釈できます。

---

### 原則1: 非インタラクティブ設計（必須）

#### エージェント環境の制限

エージェントが実行する環境は **非インタラクティブシェル** です。

```
❌ 動作しない
$ python scripts/deploy.py
Target environment: _  # ← 入力待ち → エージェントが応答不可 → ハング

✅ 動作する
$ python scripts/deploy.py --env production
[実行開始]
```

#### 実装パターン

##### パターン1：コマンドラインフラグ

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env', required=True, choices=['dev', 'staging', 'prod'])
parser.add_argument('--tag', default='latest')
args = parser.parse_args()

print(f"Deploying {args.tag} to {args.env}")
```

**使用方法**
```bash
python scripts/deploy.py --env prod --tag v1.2.3
```

##### パターン2：環境変数

```python
import os

env = os.getenv('TARGET_ENV')
if not env:
    raise ValueError("TARGET_ENV environment variable required")

print(f"Deploying to {env}")
```

**使用方法**
```bash
TARGET_ENV=production python scripts/deploy.py
```

##### パターン3：標準入力（複数値）

```bash
#!/bin/bash
# stdin から CSV データを読む
while IFS=, read -r id name email; do
    process_user "$id" "$name" "$email"
done
```

**使用方法**
```bash
echo "1,Alice,alice@example.com
2,Bob,bob@example.com" | bash scripts/process_users.sh
```

---

### 原則2: 明確なエラーメッセージ

#### 悪い例

```python
if not validate_input():
    print("Error")  # ← これでなぜ失敗したか不明
    sys.exit(1)
```

**エージェントの反応**
```
エージェント「エラーが出た。何が悪いのかわからない。
どう修正すればいいの？」
→ 次のステップに進めない
```

#### 良い例

```python
import sys

def validate_input(data):
    if not data:
        raise ValueError("Input data is empty. Provide CSV content via stdin or --input")
    if ',' not in data:
        raise ValueError("Input format error: expected CSV. Column separator ',' not found.")
    return True

try:
    process_data(input_data)
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    print("\nUsage: python scripts/process.py [--input FILE]", file=sys.stderr)
    sys.exit(1)
```

**エージェントの反応**
```
Error: Input format error: expected CSV. Column separator ',' not found.

エージェント「',' がないんだ。CSVじゃない形式で来たのか。
ユーザーの入力を修正するか、別の形式で試そう」
→ 次のステップが明確
```

#### パターン：`--help` の充実

```bash
$ python scripts/analyze.py --help

Usage: analyze.py [OPTIONS] INPUT_FILE

Analyze text data and generate statistics.

Options:
  --format FORMAT     Output format: json, csv, markdown (default: json)
  --output FILE       Save output to FILE (default: stdout)
  --verbose           Print progress to stderr
  --help              Show this message

Examples:
  analyze.py data.txt
  analyze.py --format csv --output report.csv data.txt
  analyze.py --verbose --output results.json large_file.txt

Error codes:
  0: Success
  1: Input file not found
  2: Invalid format option
  3: Permission denied on output file
```

**メリット**
- エージェントが `--help` でスクリプトの使い方を理解
- ユーザーもドキュメント参照不要
- トラブル時の参照資料

---

### 原則3: 構造化出力

#### 出力形式の選択

```
テキスト出力：人向け
├─ ❌ 機械解析困難
└─ ❌ 他スクリプトとの連携困難

構造化出力：機械解析向け
├─ ✅ JSON
├─ ✅ CSV
└─ ✅ TSV
```

#### 悪い例（自由形式テキスト）

```python
# ❌ 自由形式
print("Results:")
print(f"  Successfully processed: {success_count}")
print(f"  Failed: {failed_count}")
print(f"  Total time: {elapsed_time:.2f}s")
```

**問題**
- 別のスクリプトで解析しにくい
- フォーマットが変わると他のツール が破綻
- エージェントが「成功数は何個か」を抽出するのに力を使う

#### 良い例（JSON）

```python
# ✅ JSON 構造化
import json
result = {
    "status": "success",
    "summary": {
        "processed": success_count,
        "failed": failed_count,
        "elapsed_seconds": elapsed_time
    }
}
print(json.dumps(result))
```

**メリット**
- `jq` で簡単にフィルタ可能
- 別スクリプトと連携容易
- エージェントが構造を理解可能

##### データと診断の分離

```python
# ✅ データは stdout、診断は stderr
print(json.dumps(results), file=sys.stdout)  # 構造化データ
print(f"Processed {count} items in {elapsed}s", file=sys.stderr)  # 進捗情報
```

**効果**
- エージェント：stdout を次のステップに渡す
- ユーザー：stderr で進捗を確認

---

### 原則4：べき等性（Idempotency）

#### エージェントは再試行する

スクリプトが失敗した場合、エージェントは同じコマンドを再実行する可能性があります。

```
実行1: create_backup.py
  → ディスク満杯でエラー

エージェント「失敗した。もう一度試そう」

実行2: create_backup.py  
  ← 前回のバックアップは？重複する？
```

#### 悪い実装（非べき等）

```python
# ❌ 2回実行すると2つのバックアップができる
def backup_database():
    timestamp = datetime.now().isoformat()
    backup_file = f"backup_{timestamp}.sql"
    create_backup(backup_file)
    print("Backup created")
```

#### 良い実装（べき等）

```python
# ✅ 何度実行しても同じ結果
def backup_database():
    backup_file = "latest_backup.sql"
    
    # 既に存在していたら上書き
    if os.path.exists(backup_file):
        os.remove(backup_file)
    
    create_backup(backup_file)
    print(f"Backup saved to {backup_file}")
```

#### パターン：「create if not exists」

```python
def ensure_config():
    config_file = ".config/settings.json"
    
    if os.path.exists(config_file):
        # 既存設定を使用
        with open(config_file) as f:
            config = json.load(f)
        print(f"Using existing config: {config_file}")
    else:
        # 新規作成
        config = create_default_config()
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f)
        print(f"Created new config: {config_file}")
    
    return config
```

---

### 原則5：明示的なパラメータ

#### 「魔法の数字」を避ける

```python
# ❌ なぜ 47？
TIMEOUT = 47
MAX_RETRIES = 5
BATCH_SIZE = 100

# ✅ 理由を説明
# HTTP リクエストは通常 30 秒以内に完了
# より長いタイムアウトは低速接続対応
REQUEST_TIMEOUT = 30

# 3 リトライが大多数の一時的エラーを解決
# 3 回以上は時間の無駄
MAX_RETRIES = 3

# バッチ処理：メモリ使用とスループッドのバランス
# 100 件でメモリ効率と処理速度のベストバランス
BATCH_SIZE = 100
```

---

### 原則6：明確な出力形式定義

#### SKILL.md での説明

```markdown
## 補助スクリプト

Run these scripts to perform specific tasks:

### validate_input.py

Validates data format and structure.

**Usage:**
\`\`\`bash
python scripts/validate_input.py input.csv
\`\`\`

**Output format (JSON):**
\`\`\`json
{
  "valid": true,
  "rows": 1000,
  "columns": ["id", "name", "email"],
  "encoding": "utf-8",
  "issues": []
}
\`\`\`

**Exit codes:**
- 0: Valid
- 1: Invalid format
- 2: File not found
- 3: Encoding error
```

**例**
```markdown
### process_data.py

Processes CSV and outputs cleaned result.

**Usage:**
\`\`\`bash
python scripts/process_data.py --input raw.csv --output clean.csv --strict
\`\`\`

**Output:**
- Cleaned CSV file
- Summary printed to stdout:
  \`\`\`json
  {"processed": 1000, "removed": 23, "warnings": 5}
  \`\`\`
```

---

### 原則7：入力制約の明示

#### 許可・禁止を明確に

```python
def process_image(image_path):
    ALLOWED_EXTENSIONS = ['.jpg', '.png', '.gif', '.webp']
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported image format: {ext}\n"
            f"Supported: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    if os.path.getsize(image_path) > 50_000_000:  # 50MB
        raise ValueError(
            f"Image too large: {os.path.getsize(image_path)} bytes\n"
            "Maximum file size: 50MB"
        )
    
    return process(image_path)
```

---

### 原則8：ドライラン（事前確認）

#### 破壊的な操作に対して

```python
parser.add_argument('--dry-run', action='store_true',
                    help='Show what would be done without making changes')

if args.dry_run:
    print("DRY RUN MODE - No changes will be made\n")
    print(f"Would delete: {files_to_delete}")
    print(f"Would modify: {files_to_modify}")
    sys.exit(0)

# 実際の削除・修正処理
apply_changes(files_to_delete, files_to_modify)
```

---

### 原則9：意味のある終了コード

```python
#!/usr/bin/env python3

try:
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)  # File not found
    
    if not validate_format(input_file):
        print(f"Error: Invalid format", file=sys.stderr)
        sys.exit(2)  # Invalid format
    
    if not has_permission(output_dir):
        print(f"Error: Permission denied: {output_dir}", file=sys.stderr)
        sys.exit(3)  # Permission error
    
    result = process(input_file)
    save_result(result, output_dir)
    
    sys.exit(0)  # Success
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(255)  # Unexpected error
```

**エージェント側の処理**
```
成功（exit 0）
└─ 結果を解釈して次へ

ファイルなし（exit 1）
└─ ファイル名を修正して再実行

形式エラー（exit 2）
└─ 入力形式の修正を提案

権限エラー（exit 3）
└─ 権限の確認を提案

予期しないエラー（exit 255）
└─ エージェントに任せる
```

---

### 実装例：完全なスクリプト

```python
#!/usr/bin/env python3
"""
Process and validate CSV files.

More info: python scripts/csv_processor.py --help
"""

import argparse
import json
import sys
import os
from pathlib import Path

# 設定（理由付き）
# CSV の 1 行当たり平均 100 バイト程度、メモリ効率と処理速度のバランス
BATCH_SIZE = 1000

# CSV ファイルの最大サイズ。超える場合は事前フィルタを提案
MAX_FILE_SIZE = 500_000_000  # 500MB


def validate_input_file(filepath):
    """Input ファイルが有効か確認"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    if not filepath.endswith('.csv'):
        raise ValueError(f"Expected CSV file, got: {filepath}")
    
    size = os.path.getsize(filepath)
    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large ({size} bytes). "
            f"Maximum size: {MAX_FILE_SIZE} bytes. "
            f"Consider splitting the file."
        )
    
    if size == 0:
        raise ValueError("Input file is empty")


def process_csv(input_path, output_path, remove_duplicates=False):
    """CSV を処理"""
    validate_input_file(input_path)
    
    result = {
        "status": "success",
        "input_file": input_path,
        "output_file": output_path,
        "statistics": {
            "rows_processed": 0,
            "rows_removed": 0,
            "warnings": []
        }
    }
    
    try:
        # 処理実装（省略）
        with open(input_path) as f:
            lines = f.readlines()
        
        result["statistics"]["rows_processed"] = len(lines)
        
        # 結果を保存
        with open(output_path, 'w') as f:
            for line in lines:
                f.write(line)
        
        return result
    
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Process and validate CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/csv_processor.py data.csv
  python scripts/csv_processor.py --input raw.csv --output clean.csv --dedup
  python scripts/csv_processor.py --dry-run data.csv

Output format:
  JSON to stdout containing: status, statistics, errors (if any)
  Progress messages to stderr

Exit codes:
  0: Success
  1: File not found / Invalid input
  2: Format error / Invalid option
  3: Permission denied
  255: Unexpected error
        """
    )
    
    parser.add_argument('input', nargs='?', default=None, help='Input CSV file')
    parser.add_argument('--input', dest='input_arg', help='Input file (alternative)')
    parser.add_argument('--output', default=None, help='Output file (default: stdout)')
   parser.add_argument('--dedup', action='store_true', help='Remove duplicate rows')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    
    args = parser.parse_args()
    
    # 入力ファイルの確定
    input_file = args.input or args.input_arg
    if not input_file:
        parser.print_help()
        sys.exit(2)
    
    # ドライラン
    if args.dry_run:
        print(f"DRY RUN: Would process {input_file}", file=sys.stderr)
        result = {
            "status": "dry_run",
            "input_file": input_file,
            "would_output": args.output or "stdout"
        }
        print(json.dumps(result))
        sys.exit(0)
    
    try:
        validate_input_file(input_file)
        output_file = args.output or "-"  # "-" は stdout を意味する
        
        result = process_csv(input_file, output_file, remove_duplicates=args.dedup)
        
        # 結果をJSON で出力
        print(json.dumps(result))
        
        # 進捗・統計を stderr に出力
        print(f"Processed {result['statistics']['rows_processed']} rows", file=sys.stderr)
        
        sys.exit(0)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except PermissionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(255)


if __name__ == '__main__':
    main()
```

---

### チェックリスト

#### スクリプト設計
- [ ] 非インタラクティブ（コマンドフラグ・環境変数のみ）
- [ ] `--help` が充実したドキュメント
- [ ] エラーメッセージが具体的・改善提案を含む
- [ ] 構造化出力（JSON/CSV）
- [ ] stdoutデータ・stderrログを分離
- [ ] べき等性（何度実行しても安全）
- [ ] 入力制約を明示（許可形式・サイズ制限）
- [ ] ドライラン対応（破壊的操作の場合）
- [ ] 意味のある終了コード（0=success、1-3=具体的エラー、255=予期外）

#### SKILL.md での説明
- [ ] スクリプト一覧（available scripts セクション）
- [ ] 各スクリプトの使い方（bash コマンド例）
- [ ] 出力形式を明記（JSON/CSV 例+スキーマ）
- [ ] ワークフロー内でのスクリプト呼び出し順序
- [ ] エラーハンドリング（失敗時の対応）

---

### 関連資料

- [agentskills.io - Using scripts in skills](https://agentskills.io/skill-creation/using-scripts)
- [PEP 723 - Inline script metadata](https://peps.python.org/pep-0723/)
- Part 3-6: スキル評価フレームワーク（テスト実装例）

## Part 4-6: 複数リポでの SKILL 共通化（実装ガイド） {#section-04-advanced-06-multi-repo-skill-sharing}


同一の SKILL を複数のリポジトリで共有・再利用するための実装パターンを解説します。

[Part 4-1: チーム内スキル共有戦略](#section-04-advanced-01-team-sharing) の「戦略・方針」に対して、本章では **手を動かせる実装手順** を提供します。

---

### この章の進め方（再編版）

最短で理解したい場合は、次の順で読み進めてください。

1. 「5分クイック導線」で方式を決める
2. 「シナリオ別おすすめ」で採用理由を確認する
3. 採用した方式の実装手順を実行する
4. 「失敗駆動ハンズオン」で運用時の詰まりどころを先に潰す
5. 「運用ポリシー」でチームルールを固定する

---

### 5分クイック導線: どのパターンを選ぶか

```
個人利用のみ？
  │
  YES → パターン1: Personal Skills（最短・設定不要）
  │
  NO
  │
チームで使う？（複数メンバー）
  │
  YES
  │
  ├─ 更新を中央リポジトリで一元管理したい？
  │    YES → パターン2: Git submodule（版を固定して配布）
  │    NO  → パターン3: Git subtree（クローン設定不要でシンプル）
  │
  └─ さらに: スクリプト共通 × リポ別設定に分離したい？
           → パターン4: Config 駆動設計（上 3 つと組み合わせ可）
```

#### submodule と subtree のコンセプト早見表

| 観点 | Git submodule | Git subtree |
|------|----------------|-------------|
| 正体 | 別リポジトリを「参照（特定コミット）」として保持 | 別リポジトリの内容を親リポジトリの履歴に取り込む |
| 親リポに保存されるもの | 子リポジトリの参照先コミット | 取り込まれたファイルとコミット |
| clone 時の挙動 | 追加取得が必要（`--recurse-submodules`） | 通常 clone でそのまま使える |
| バージョン固定 | 強い（参照コミットで明示） | pull タイミングで反映 |
| 運用の主な難所 | 初期化忘れ、同期忘れ | 履歴・競合解消の理解 |

この章では、submodule を「厳密な版管理」、subtree を「導入簡便性」として使い分けます。

---

### シナリオ別おすすめ（先に結論）

| 代表シナリオ | 推奨パターン | 理由 |
|---|---|---|
| まず 1 人で試したい | Personal Skills | 設定最小で検証速度が最も高い |
| 複数リポで同じ版を厳密管理したい | Git submodule | 参照コミットを明示して安全に更新できる |
| 利用側の clone / CI を単純化したい | Git subtree | 利用者側の追加設定が不要 |
| 共通スクリプトを複数リポで使い回したい | Config 駆動設計 + 上記いずれか | 差分を設定ファイルに分離できる |

---

### 実装パターン詳細

以下は方式ごとの実装手順です。採用方式だけ先に実装して問題ありません。

---

### パターン1: Personal Skills（個人・全リポ共通）

**最短。設定不要。自分のマシン上の全リポジトリから同一 SKILL を参照できる。**

#### 配置場所

| OS | パス |
|----|------|
| Windows | `%USERPROFILE%\.copilot\skills\<skill-name>\SKILL.md` |
| macOS / Linux | `~/.copilot/skills/<skill-name>/SKILL.md` |

#### 手順

```powershell
# Windows の例
$skillName = "my-skill"
$skillDir  = "$env:USERPROFILE\.copilot\skills\$skillName"

New-Item -ItemType Directory -Force -Path $skillDir
Copy-Item .\path\to\SKILL.md "$skillDir\SKILL.md"
# スクリプトや補助ファイルもここに置く
Copy-Item .\path\to\scripts "$skillDir\scripts" -Recurse
```

```bash
# macOS / Linux の例
SKILL_NAME="my-skill"
mkdir -p ~/.copilot/skills/$SKILL_NAME
cp ./path/to/SKILL.md ~/.copilot/skills/$SKILL_NAME/SKILL.md
cp -r ./path/to/scripts ~/.copilot/skills/$SKILL_NAME/scripts
```

スクリプトや参照ファイルも同フォルダ配下に置き、SKILL.md からは `./scripts/...` の相対パスで参照します。

#### 動作確認

VS Code Copilot Chat でチャット入力欄に `/` を入力し、スキル名が表示されることを確認します。表示されない場合はフォルダ名と SKILL.md の `name` フィールドが一致しているか確認してください。

#### メリット・デメリット

| 項目 | 内容 |
|------|------|
| ✅ 設定不要 | git や submodule の設定が一切不要 |
| ✅ 即時反映 | リポジトリをまたいで自動参照される |
| ✅ 試しやすい | プロトタイプを素早く検証できる |
| ❌ 個人マシン限定 | チームメンバーには届かない |
| ❌ バージョン管理外 | 変更履歴を git で追いにくい |

**推奨シーン:** 個人の生産性向上スキル、まず動かして試すプロトタイプ

---

### パターン2: Git submodule（チーム共有・中央管理）

**SKILL 専用リポジトリを 1 つ作成し、各業務リポに submodule として取り込む。**  
更新は中央リポジトリで行い、各業務リポは `git submodule update --remote` で同期します。

#### コンセプト（先にここだけ理解する）

submodule は「フォルダそのものを共有」する方式ではなく、親リポジトリが「別リポジトリのどのコミットを参照するか」を持つ方式です。

```
中央リポを更新
  ↓
業務リポは自動追従しない
  ↓
必要なタイミングで update --remote して追従
```

この性質により、業務リポごとに異なるバージョンを安全に運用できます。

#### ディレクトリ構造

```
shared-skills/              ← SKILL 専用リポジトリ（中央管理）
├── my-skill/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── invoke.ps1
│   └── assets/
└── another-skill/
    └── SKILL.md

repo-A/                     ← 業務リポジトリ A
├── .github/
│   └── skills/
│       └── my-skill/       ← submodule として取り込み
├── src/
└── ...

repo-B/                     ← 業務リポジトリ B
├── .github/
│   └── skills/
│       └── my-skill/       ← 同じ submodule（独立したポインタで版管理）
└── ...
```

#### 手順: 初回セットアップ

```bash
# Step 1: 専用リポジトリを作成（一度だけ）
mkdir shared-skills && cd shared-skills
git init
mkdir -p my-skill/scripts

# SKILL.md を作成して...
git add .
git commit -m "feat: add my-skill"
git remote add origin https://github.com/<org>/shared-skills.git
git push -u origin main
```

```bash
# Step 2: 各業務リポにサブモジュールとして追加（リポごとに一度だけ）
cd repo-A
git submodule add \
  https://github.com/<org>/shared-skills.git \
  .github/skills/shared-skills
git commit -m "feat: add shared-skills submodule"
git push
```

> 重要: `git submodule` はリポジトリ単位で取り込むため、`my-skill` のような個別スキルのみを選択して導入することはできません。導入対象は `shared-skills` リポジトリ全体です。

#### 手順: 更新フロー（中央リポで更新 → 業務リポへ反映）

```bash
# 1. 中央リポでスキルを更新
cd shared-skills
# SKILL.md を編集...
git add . && git commit -m "fix: update procedure" && git push

# 2. 業務リポ側で同期
cd repo-A
git submodule update --remote --merge .github/skills/shared-skills
git add .github/skills/shared-skills
git commit -m "chore: update shared-skills to latest"
git push
```

#### 注意: クローン時の設定

submodule を含むリポジトリをクローンした人は以下が必要です。

```bash
# 最初から submodule を含めてクローン
git clone --recurse-submodules https://github.com/<org>/repo-A.git

# または既存クローン後に初期化
git submodule update --init --recursive
```

CI/CD（GitHub Actions 等）でも `actions/checkout` に `submodules: recursive` を追加してください。

```yaml
- uses: actions/checkout@v4
  with:
    submodules: recursive
```

#### メリット・デメリット

| 項目 | 内容 |
|------|------|
| ✅ バージョン固定 | 業務リポで使う版を明示的にピン留めできる |
| ✅ 中央管理 | 更新は専用リポ 1 箇所で行える |
| ✅ CI/CD 統合 | GitHub Actions 等と組み合わせやすい |
| ❌ クローン設定が必要 | `--recurse-submodules` を忘れると空フォルダになる |
| ❌ 手動同期 | 各リポで `update --remote` の実行が必要 |

**推奨シーン:** バージョンを厳密に管理したい組織・大規模チーム・CI/CD 統合が必要

---

### 失敗駆動ハンズオン（submodule）

実運用で発生しやすい失敗を、意図的に再現して復旧手順を確認します。

#### 演習A: clone 後に `.github/skills` が空になる

**症状**

- `git clone` 後に `.github/skills` が空、または期待ファイルが見えない

**確認**

```bash
git submodule status
```

**復旧**

```bash
git submodule update --init --recursive
```

**再発防止**

- 新規 clone は `git clone --recurse-submodules ...` を標準化する
- CI は `actions/checkout` に `submodules: recursive` を必須化する

#### 演習B: 共有側を更新したのに利用側で反映されない

**症状**

- shared-skills 側は更新済みだが、業務リポに変更が現れない

**確認**

```bash
git submodule status
git diff -- .github/skills/shared-skills
```

**復旧**

```bash
git submodule update --remote --merge .github/skills/shared-skills
git add .github/skills/shared-skills
git commit -m "chore: update shared-skills submodule pointer"
```

**再発防止**

- 「共有リポ更新」と「利用リポのポインタ更新」を別タスクとして管理する
- PR テンプレートに「submodule pointer update 確認」チェックを追加する

---

### パターン3: Git subtree（チーム共有・シンプル）

**`git subtree` で SKILL ファイルを業務リポジトリの歴史として直接取り込む。**  
submodule と異なり、クローンする人に特別な設定が不要なのが最大のメリットです。

#### コンセプト（先にここだけ理解する）

subtree は「参照」ではなく「取り込み」です。親リポジトリにファイル実体と履歴を取り込むため、利用側は通常の clone だけで利用できます。

```
中央リポを更新
  ↓
業務リポで subtree pull
  ↓
取り込みコミットとして反映
```

この性質により、導入時のハードルは下がりますが、履歴の扱いと競合解消はやや重くなります。

#### 手順: 初回セットアップ

```bash
# 業務リポに shared-skills 全体を subtree として追加
cd repo-A
git subtree add \
  --prefix=.github/skills/shared-skills \
  https://github.com/<org>/shared-skills.git main \
  --squash
git push
```

> `--squash` を付けると、中央リポの細かいコミット履歴を業務リポに持ち込まずに済みます。
>
> 重要: このコマンドは `shared-skills` リポジトリ全体を取り込みます。`my-skill` のような 1 つのスキルだけを直接 `.github/skills/my-skill` に配置するわけではありません。
>
> たとえば中央リポが次の構造なら:
>
> ```text
> shared-skills/
> ├── my-skill/
> │   └── SKILL.md
> └── another-skill/
>     └── SKILL.md
> ```
>
> 業務リポでは次のように展開されます:
>
> ```text
> .github/skills/shared-skills/my-skill/SKILL.md
> .github/skills/shared-skills/another-skill/SKILL.md
> ```

#### 手順: 更新フロー（中央リポが更新されたとき）

```bash
cd repo-A
git subtree pull \
  --prefix=.github/skills/shared-skills \
  https://github.com/<org>/shared-skills.git main \
  --squash
git push
```

#### 1 つのスキルだけを取り込みたい場合

`git subtree` 単体では、相手リポジトリの一部ディレクトリだけを直接取り込む運用には向きません。`shared-skills` が複数スキルを持つ単一リポジトリである場合、1 スキルだけを `.github/skills/my-skill` に置きたいなら、先にそのディレクトリを独立ブランチとして切り出します。

```bash
# shared-skills 側: my-skill ディレクトリだけの履歴を切り出す
cd shared-skills
git subtree split --prefix=my-skill -b my-skill-branch
git push origin my-skill-branch
```

```bash
# repo-A 側: 切り出したブランチを 1 スキルとして取り込む
cd repo-A
git subtree add \
  --prefix=.github/skills/my-skill \
  https://github.com/<org>/shared-skills.git my-skill-branch \
  --squash
git push
```

この方式なら、業務リポ側の配置は次のようにシンプルになります。

```text
.github/skills/my-skill/SKILL.md
.github/skills/my-skill/scripts/...
```

更新時も同じブランチを pull します。

```bash
cd repo-A
git subtree pull \
  --prefix=.github/skills/my-skill \
  https://github.com/<org>/shared-skills.git my-skill-branch \
  --squash
git push
```

> 補足: 1 スキルごとに独立リポジトリを作れるなら、その方が `submodule` / `subtree` ともに運用は単純です。`subtree split` は「中央では 1 リポにまとめたいが、利用側では個別導入したい」場合の折衷案です。

#### URL を毎回書かないための設定（任意）

`remote` として別名を登録しておくと便利です。

```bash
git remote add shared-skills https://github.com/<org>/shared-skills.git

# shared-skills 全体を取り込む場合
git subtree pull --prefix=.github/skills/shared-skills shared-skills main --squash

# 1 スキル用に split 済みブランチを使う場合
git subtree pull --prefix=.github/skills/my-skill shared-skills my-skill-branch --squash
```

#### メリット・デメリット

| 項目 | 内容 |
|------|------|
| ✅ クローン設定不要 | 通常の `git clone` でそのまま使える |
| ✅ 平坦な履歴 | 業務リポの `git log` に自然に溶け込む |
| ✅ サブモジュール知識不要 | チームの git スキル差を吸収しやすい |
| ✅ 個別導入にも拡張可能 | `subtree split` 用ブランチを作れば 1 スキル単位にもできる |
| ❌ 逆方向の push が複雑 | 業務リポから中央リポへの反映は `git subtree push` が必要 |
| ❌ そのままでは個別導入できない | 単一リポに複数スキルがある場合はリポ全体を取り込む |
| ❌ 衝突時の解決が煩雑 | 大きな変更が重なると難しくなる場合がある |

**推奨シーン:** CI 設定をシンプルに保ちたい・チームの git スキルレベルが混在している

---

### パターン4: Config 駆動設計（スクリプト共通 + リポ別設定）

**パターン1〜3 と組み合わせる設計原則。**  
スクリプト本体を共通化しつつ、リポジトリ固有の値（パス・出力先・メタデータ等）は設定ファイル（JSON / YAML）に切り出します。

#### 先に結論: 配置先は 2 パターンある

リポ固有設定の置き場所は、次のどちらでも構成できます。

1. 共通リポ配置版
   共通スクリプトと設定ファイルを同じ shared-skills 側で管理する方式です。
2. 利用側リポ配置版
   共通スクリプトは shared-skills 側に置き、各リポ固有の設定だけを業務リポ側に置く方式です。

一般には、リポ固有の値が多いほど「利用側リポ配置版」のほうが責務分離が明確です。逆に、設定ファイルも含めて中央管理したいなら「共通リポ配置版」が向いています。

#### 方式A: 共通リポ配置版

設定ファイルも shared-skills 側に置く構成です。複数リポの設定を 1 箇所で見渡せます。

##### ディレクトリ構造

```
shared-skills/
└── my-skill/
    ├── SKILL.md
    ├── scripts/
    │   └── invoke.ps1          ← スクリプトは共通（リポ差分なし）
    ├── configs/
  │   ├── repo-A.build.json   ← repo-A 用設定
  │   └── repo-B.build.json   ← repo-B 用設定
    └── assets/
        └── style.css
```

##### 設定ファイルの例

```json
// configs/repo-A.build.json
{
  "sourceRoot":    "C:/dev/apps/repo-A",
  "outputDir":     "C:/dev/apps/repo-A/output",
  "projectName":   "repo-a-product",
  "metadataFile":  "./.github/skills/my-skill/configs/repo-A.metadata.yaml",
  "styleFile":     "./.github/skills/my-skill/assets/style.css"
}
```

  ##### 呼び出し方

  ```powershell
  # repo-A 向け
  .\.github\skills\my-skill\scripts\invoke.ps1 `
    -ConfigFile .\.github\skills\my-skill\configs\repo-A.build.json

  # repo-B 向け
  .\.github\skills\my-skill\scripts\invoke.ps1 `
    -ConfigFile .\.github\skills\my-skill\configs\repo-B.build.json
  ```

  ##### 向いているケース

  - 設定ファイルも中央でレビュー・配布したい
  - 利用側リポに設定ファイル配置ルールを増やしたくない
  - repo ごとの差分がまだ小さい

  ##### 注意点

  - repo-A 専用設定が shared-skills に混ざるため、責務がやや曖昧になりやすい
  - 利用側リポから見て「自分専用設定の所在」が直感的でない場合がある

  #### 方式B: 利用側リポ配置版

  共通スクリプトは shared-skills に置き、repo 固有の設定は各業務リポジトリ側に置く構成です。通常はこちらのほうが設計意図が明確です。

  ##### ディレクトリ構造

  ```text
  shared-skills/
  └── my-skill/
    ├── SKILL.md
    ├── scripts/
    │   └── invoke.ps1          ← スクリプトは共通
    └── assets/
      └── style.css

  repo-A/
  └── .github/
    ├── skills/
    │   └── my-skill/
    │       ├── SKILL.md
    │       ├── scripts/
    │       └── assets/
    └── skill-configs/
      └── my-skill/
        └── repo-A.build.json
  ```

  ##### 設定ファイルの例

  ```json
  // .github/skill-configs/my-skill/repo-A.build.json
  {
    "sourceRoot":    ".",
    "outputDir":     "./output",
    "projectName":   "repo-a-product",
    "metadataFile":  "./.github/skill-configs/my-skill/repo-A.metadata.yaml",
    "styleFile":     "./.github/skills/my-skill/assets/style.css"
  }
  ```

  ##### 呼び出し方

  ```powershell
  # repo-A 側に置いた設定を渡す
  .\.github\skills\my-skill\scripts\invoke.ps1 `
    -ConfigFile .\.github\skill-configs\my-skill\repo-A.build.json
  ```

  ##### 向いているケース

  - リポごとのパスや出力先が大きく異なる
  - repo 固有設定をその repo の PR で閉じて管理したい
  - 共通リポに repo 個別事情を持ち込みたくない

  ##### 注意点

  - 利用側リポごとに設定ファイル配置ルールをチームで統一する必要がある
  - SKILL.md や運用ドキュメントで、設定ファイルの想定配置先を明記する必要がある

  #### スクリプトでの受け取り方（PowerShell 例）

```powershell
param(
    [Parameter(Mandatory)][string]$ConfigFile
)

$config      = Get-Content $ConfigFile | ConvertFrom-Json
$sourceRoot  = $config.sourceRoot
$outputDir   = $config.outputDir
$projectName = $config.projectName

Write-Host "Building: $projectName from $sourceRoot"
# ... 以降は $config の値だけで処理する
```

エージェントから実行するときも、SKILL.md に「`-ConfigFile` を指定してください」と動作手順として明記しておくと自動実行精度が上がります。

#### 設計のコツ

```
✅ DO   スクリプトにリポ名やパスをハードコードしない
✅ DO   設定ファイルに「何が違うか」だけを書く
✅ DO   配置先を決めたら命名規則を統一する
     例: shared 側なら configs/<repo-name>.build.json
     例: 利用側なら .github/skill-configs/<skill-name>/<repo-name>.build.json
✅ DO   スクリプトは引数なしで実行したときにヘルプを表示する

❌ AVOID if ($projectName -eq "repo-A") { ... } とスクリプト内で分岐する
❌ AVOID デフォルト値に特定リポのパスを埋め込む
❌ AVOID SKILL.md に環境依存の絶対パスを書く
```

---

### 運用ポリシー（実運用で迷わないために）

実運用ルールは次のドキュメントを正としてください。

- [shared-copilot-skills README](../../.github/skills/README.md)
- [OPERATIONS](../../.github/skills/docs/OPERATIONS.md)

最低限の統一ルール:

- shared 側の変更は shared リポジトリで先に確定する
- 利用側は submodule ポインタ更新を PR で明示する
- `.gitignore` で `.github/skills` の変更を隠して管理しない

---

### パターン比較まとめ

| パターン | 対象 | git 設定 | 更新方法 | 難易度 |
|---------|------|---------|---------|-------|
| **Personal Skills** | 個人 | 不要 | 手動コピー | ★☆☆ |
| **Git submodule** | チーム | 必要（clone に `--recurse`）| `submodule update --remote` | ★★★ |
| **Git subtree** | チーム | 不要 | `subtree pull` | ★★☆ |
| **Config 駆動設計** | どちらでも | —（上 3 つと組み合わせ） | —（スクリプト共通） | ★★☆ |

---

### 共通チェックリスト

SKILL を共通化・配置する前に確認してください。

```
□ SKILL.md の name フィールドとフォルダ名が一致している
□ description に「いつ使うか」「検索されるキーワード」が入っている
□ スクリプト・参照ファイルの相対パスが ./scripts/... 形式になっている
□ リポ固有の値（パス・プロジェクト名等）を SKILL.md / スクリプトに書いていない
  → shared 側の configs/ または利用側リポの設定ファイルに分離されている
□ チャットで / 入力時にスキル名が表示される
□ 自然文のリクエスト（「〇〇を△△したい」）で自動ロードされる
□ submodule の場合: CI/CD に submodules: recursive が設定されている
```

---

→ 前へ: [Part 4-5: スクリプト設計ベストプラクティス](#section-04-advanced-05-scripts-best-practices)  
→ 次へ: [Part 5-1: 複合スキルと高度なパターン](#section-05-advanced-topics-01-composite-skills)

## Part 4-7: 運用手法（Runbook / Gate / Evidence / Scope / Rollout） {#section-04-advanced-07-operations-methodology}


スキルを継続的かつ監査可能に運用するための標準手法を解説します。

---

### 本章の目的

本章の目的は、次の状態をチーム標準として定着させることです。

- runbook に基づき、手順逸脱を防ぐ
- gate で進行可否を客観判定する
- evidence / trace により事後検証可能にする
- scope 漏れを防ぎ、remediation を完遂する
- rollout を段階的に実施し、影響を制御する

---

### 用語定義

| 用語 | 定義 |
|------|------|
| runbook | 現場向けの作業手順書 |
| remediation | 不具合の是正対応 |
| gate | 次に進むための確認ポイント |
| evidence / trace | 作業証跡 |
| scope | 対象範囲 |
| rollout | 横展開 |

---

### 標準フロー（6フェーズ）

#### フェーズ1: 事前準備（runbook確定）

目的: 現場条件に合わせた実行計画を確定する

チェック項目:
- 対象システム、責任者、実施時間帯を確定
- 依存関係と事前条件を明記
- ロールバック手順を記載

Gate:
- runbook がレビュー承認済み
- エスカレーション経路が確定

証跡:
- runbook 版数
- レビュー記録
- 承認ログ

#### フェーズ2: scope確定

目的: 対象漏れと重複を防ぐ

チェック項目:
- 対象母集団を固定（インベントリ作成）
- 除外対象と理由を文書化
- リスク区分（高/中/低）を付与

Gate:
- 対象一覧が一意
- 除外理由が承認済み

証跡:
- 対象インベントリ
- 除外リスト
- リスク評価表

#### フェーズ3: remediation実行

目的: 是正作業を安全かつ再現可能に実施する

チェック項目:
- runbook 通りに実行
- 失敗時は停止条件に従って中断
- 必要時にロールバック実行

Gate:
- 重大エラーなし
- 変更後検証が合格

証跡:
- 実行ログ
- 変更差分
- 実施者と時刻

#### フェーズ4: gate判定

目的: 次工程へ進める品質を判定する

チェック項目:
- 機能確認
- 性能確認
- セキュリティ確認

Gate:
- 必須観点すべて合格
- 未達項目は是正計画付きで記録

証跡:
- テスト結果
- 監視値
- 判定チェックシート

#### フェーズ5: scope完了確認

目的: 範囲内の取りこぼしをゼロにする

チェック項目:
- 対象件数と完了件数の照合
- 例外対象の妥当性確認
- 未対応の残件確認

Gate:
- 未対応ゼロ、または承認済み例外のみ

証跡:
- 完了台帳
- 差分照合結果
- 例外承認記録

#### フェーズ6: rollout

目的: 影響を制御しながら横展開する

チェック項目:
- 少量先行で検証
- 段階展開で反復評価
- 全面展開で最終確認

Gate:
- 波次ごとの合格基準を満たす
- 中止基準と連絡経路が明確

証跡:
- 展開計画
- 波次別結果
- 障害報告と是正履歴

---

### 手法1: Gate設計

原則:
- 合否は定量条件で定義する
- 不合格時の分岐を runbook に明記する
- 判定者を実施者と分離する

Gate定義テンプレート:

| 項目 | 記入例 |
|------|--------|
| Gate名 | G3: remediation完了判定 |
| 判定条件 | 失敗率 < 1%、重大アラート 0 |
| 判定データ | 実行ログ、監視ダッシュボード |
| 不合格時対応 | 停止 → 原因分析 → 再実行 |
| 判定責任者 | 運用責任者 |

---

### 手法2: Evidence / Trace設計

原則:
- 誰が・いつ・何を・なぜを追跡可能にする
- スクリーンショットだけでなく機械可読ログを残す
- チケットIDや変更番号で相互参照する

最低証跡セット:
- 実行ログ
- 変更差分
- 判定結果
- 承認記録
- 例外記録

保管ルール例:
- 保存先: 監査用ストレージ
- 命名規則: yyyyMMdd-system-phase-ticketId
- 保管期間: 12か月以上

---

### 手法3: Scope管理

原則:
- 作業開始前に母集団を固定する
- 対象変更は差分承認を必須にする
- 例外を未対応として可視化し続ける

漏れ防止チェック:
- 対象一覧に重複がない
- 対象IDの連番欠落がない
- 除外理由が文書化されている

---

### 手法4: Remediation実行

実行サイクル:
1. 事前検証
2. 是正適用
3. 直後検証
4. 記録確定
5. 次対象へ進行

品質担保ポイント:
- 冪等性を考慮した手順
- 失敗時の自動停止条件
- ロールバックの即時実行性

---

### 手法5: Rollout管理

推奨波次:
1. カナリア（小規模）
2. 段階展開（部門・環境単位）
3. 全面展開

各波次の必須運用:
- 同一Gateを再評価
- 学びを runbook へ即時反映
- 利用部門への周知と窓口維持

---

### KPIと監査観点

KPI例:
- Gate合格率
- Scope完了率
- 証跡充足率
- 再発率
- Rollout中断率

監査観点:
- 手順逸脱が記録されているか
- 判定根拠が追跡可能か
- 例外承認の責任所在が明確か

---

### 1ページ運用チェックリスト

```
[準備]
□ runbook 承認済み
□ ロールバック手順確認済み

[scope]
□ 対象母集団を固定
□ 除外理由を承認

[実行]
□ remediation を手順どおり実施
□ 実行ログと差分を保存

[判定]
□ Gateを定量条件で判定
□ 不合格時の分岐を実施

[完了]
□ scope 完了率を照合
□ 未対応ゼロまたは例外承認済み

[展開]
□ カナリア → 段階展開 → 全面展開
□ 各波次の結果を記録
```

---

### 関連章

- Part 4-1: チーム共有プロセス
- Part 4-2: ライフサイクル管理
- Part 4-4: トラブルシューティング
- Part 4-5: スクリプト設計ベストプラクティス

# Advanced Topics {#chapter-05-advanced-topics}

## Part 5-1: 複合スキルと高度なパターン {#section-05-advanced-topics-01-composite-skills}


複数のスキルを組み合わせてより強力な機能を実現する高度なパターンを学びます。

---

### 複合スキルとは

#### 複合スキルとは

複数の基本スキルを組み合わせて、より高度な処理を実現するスキル：

```
例：「コード品質向上パイプライン」

Input: コード
  ↓
[Skill 1] analyze-code-quality
  → 問題点抽出
  ↓
[Skill 2] generate-fixes
  → 修正コード提案
  ↓
[Skill 3] generate-unit-tests
  → テストコード生成
  ↓
Output: 修正済みコード + テスト

これらを順序立てて実行する複合スキル
```

#### 複合スキル 例1: コード品質改善パイプライン

```json
{
  "id": "improve-code-quality-pipeline",
  "version": "1.0.0",
  "name": "コード品質改善パイプライン",
  "description": "コード分析→修正提案→テスト生成を一度に実行",
  
  "dependencies": [
    {"id": "analyze-code-quality", "version": ">=1.0.0", "required": true},
    {"id": "generate-fixes", "version": ">=1.0.0", "required": true},
    {"id": "generate-unit-tests", "version": ">=1.0.0", "required": true}
  ],
  
  "parameters": {
    "code": {
      "type": "string",
      "description": "改善対象のコード",
      "maxLength": 10000
    },
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "typescript", "java"],
      "required": true
    },
    "focusAreas": {
      "type": "array",
      "description": "重点改善領域",
      "items": {"type": "string"},
      "enum": ["readability", "performance", "security", "testability"]
    },
    "autoApply": {
      "type": "boolean",
      "description": "推奨修正を自動適用",
      "default": false
    }
  },
  
  "compositeDefinition": {
    "workflow": "sequential",  // sequential または parallel
    "steps": [
      {
        "id": "step1",
        "skill": "analyze-code-quality",
        "inputs": {
          "code": "${code}",
          "language": "${language}",
          "focusAreas": "${focusAreas}"
        },
        "outputs": ["analysis_result"]
      },
      {
        "id": "step2",
        "skill": "generate-fixes",
        "dependsOn": ["step1"],
        "inputs": {
          "code": "${code}",
          "analysis": "${step1.analysis_result}",
          "language": "${language}"
        },
        "outputs": ["fixed_code", "explanation"]
      },
      {
        "id": "step3",
        "skill": "generate-unit-tests",
        "dependsOn": ["step2"],
        "condition": "${autoApply}",  // autoApplyがtrueの場合のみ実行
        "inputs": {
          "function_signature": "${step2.fixed_code}",
          "language": "${language}",
          "coverage": "comprehensive"
        },
        "outputs": ["test_code"]
      }
    ]
  },
  
  "outputFormat": {
    "type": "object",
    "schema": {
      "properties": {
        "analysis": {
          "description": "初期分析結果",
          "type": "object"
        },
        "fixed_code": {
          "description": "改修されたコード",
          "type": "string"
        },
        "fixes_explanation": {
          "description": "修正内容の説明",
          "type": "string"
        },
        "test_code": {
          "description": "生成されたテストコード（autoApply: trueの場合のみ）",
          "type": "string"
        },
        "summary": {
          "description": "処理全体のサマリー",
          "type": "object",
          "properties": {
            "issues_found": {"type": "number"},
            "fixes_applied": {"type": "number"},
            "tests_generated": {"type": "number"},
            "total_time": {"type": "string"}
          }
        }
      }
    }
  }
}
```

#### 複合スキル実装例（Python）

```python
import asyncio
import json
from typing import Dict, Any
from datetime import datetime

class CompositeSkillOrchestrator:
    """複合スキルのオーケストレーター"""
    
    def __init__(self, skill_executor):
        self.executor = skill_executor
        self.results = {}
        self.start_time = None
    
    async def execute_composite_skill(self, 
                                      code: str,
                                      language: str,
                                      focus_areas: list,
                                      auto_apply: bool = False) -> Dict[str, Any]:
        """複合スキルを順序実行"""
        
        self.start_time = datetime.now()
        
        try:
            # Step 1: コード分析
            print("Step 1: Analyzing code quality...")
            analysis = await self.executor.execute(
                skill_id="analyze-code-quality",
                parameters={
                    "code_snippet": code,
                    "language": language,
                    "focusAreas": focus_areas,
                    "detailLevel": "detailed"
                }
            )
            self.results['step1_analysis'] = analysis
            
            # Step 2: 修正コード生成
            print("Step 2: Generating fixes...")
            fixes = await self.executor.execute(
                skill_id="generate-fixes",
                parameters={
                    "code": code,
                    "issues": analysis['issues'],
                    "language": language
                }
            )
            self.results['step2_fixes'] = fixes
            
            # Step 3: テスト生成（条件付き）
            test_code = None
            if auto_apply:
                print("Step 3: Generating unit tests...")
                tests = await self.executor.execute(
                    skill_id="generate-unit-tests",
                    parameters={
                        "function_signature": fixes['fixed_code'],
                        "language": language,
                        "coverage": "comprehensive"
                    }
                )
                self.results['step3_tests'] = tests
                test_code = tests['test_code']
            
            # 結果を集約
            duration = (datetime.now() - self.start_time).total_seconds()
            
            return {
                "analysis": analysis,
                "fixed_code": fixes['fixed_code'],
                "fixes_explanation": fixes['explanation'],
                "test_code": test_code,
                "summary": {
                    "issues_found": len(analysis.get('issues', [])),
                    "fixes_applied": len(fixes.get('fixes', [])),
                    "tests_generated": 1 if test_code else 0,
                    "total_time": f"{duration:.2f}s"
                }
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "failed_step": self._get_failed_step(),
                "partial_results": self.results
            }
    
    def _get_failed_step(self):
        """失敗したステップを特定"""
        if 'step1_analysis' not in self.results:
            return "analyze-code-quality"
        elif 'step2_fixes' not in self.results:
            return "generate-fixes"
        elif 'step3_tests' not in self.results:
            return "generate-unit-tests"
        return "unknown"

# 使用例
async def main():
    orchestrator = CompositeSkillOrchestrator(executor)
    
    result = await orchestrator.execute_composite_skill(
        code="""
def merge_lists(a, b):
    return a + b  # ★ 品質問題あり
        """,
        language="python",
        focus_areas=["readability", "performance"],
        auto_apply=True
    )
    
    print(json.dumps(result, indent=2))

# asyncio.run(main())
```

---

### 複合スキルの設計パターン

#### パターン1: Sequential（順序実行）

```
入力 → [Skill A] → [Skill B] → [Skill C] → 出力

特徴：
- 前のスキルの出力が次のスキルの入力
- シンプルで予測可能
- スキル間の依存関係が明確

使用例：
- パイプライン処理
- 段階的な変換
- エラーハンドリングが簡単
```

#### パターン2: Parallel（並列実行）

```
入力 ┌→ [Skill A] ┐
     ├→ [Skill B] ├→ 結果統合 → 出力
     ├→ [Skill C] ┘
     └→ [Skill D] ┘

特徴：
- 独立したスキルを同時実行
- 処理時間が短縮
- 複雑な同期が必要

使用例：
- 複数観点の同時分析
- リソース利用の最適化
```

#### パターン3: Conditional（条件付き実行）

```
[Skill A] の結果
    ↓
┌─ if condition
│  └→ [Skill B]
└─ else
   └→ [Skill C]
    ↓
 [Skill D]

特徴：
- 条件に応じて異なるパス
- 柔軟な処理フロー
- ロジック複雑化の可能性
```

#### パターン4: Loop（反復実行）

```
入力 → [初期化]
      ↓
    ┌→ [処理スキル]
    │  ↓
    └─ [終了条件] ─N→ 出力
           ↓Y
        [結果統合]

特徴：
- 複数の同じ処理を繰り返し
- 累積結果の処理
- バッチ処理向け

使用例：
- バッチコード分析
- 複数ファイルの処理
```

---

### 複合スキルの実装例2: API 統合パイプライン

```json
{
  "id": "api-documentation-generator",
  "name": "API ドキュメント生成パイプライン",
  "compositeDefinition": {
    "workflow": "sequential",
    "steps": [
      {
        "id": "parse_api",
        "skill": "parse-api-spec",
        "inputs": {"spec": "${openapi_spec}"},
        "outputs": ["endpoints", "models"]
      },
      {
        "id": "analyze_endpoints",
        "skill": "analyze-api-endpoints",
        "dependsOn": ["parse_api"],
        "inputs": {"endpoints": "${parse_api.endpoints}"},
        "outputs": ["endpoint_analysis"]
      },
      {
        "id": "generate_docs",
        "skill": "generate-api-docs",
        "dependsOn": ["analyze_endpoints"],
        "parallelize": [
          {
            "skill": "generate-usage-examples",
            "inputs": {"endpoints": "${parse_api.endpoints}"}
          },
          {
            "skill": "generate-error-docs",
            "inputs": {"endpoints": "${parse_api.endpoints}"}
          }
        ]
      }
    ]
  }
}
```

---

### 複合スキルのテスト

```python
def test_composite_skill_improvement_pipeline():
    """複合スキルのテスト"""
    
    test_code = """
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total
    """
    
    # テストケース1: 正常系
    result = execute_composite_skill(
        code=test_code,
        language="python",
        focus_areas=["performance", "readability"]
    )
    
    assert 'analysis' in result
    assert 'fixed_code' in result
    assert result['summary']['issues_found'] > 0
    
    # テストケース2: auto_apply = True
    result_with_tests = execute_composite_skill(
        code=test_code,
        language="python",
        focus_areas=["readability"],
        auto_apply=True
    )
    
    assert result_with_tests['test_code'] is not None
    
    # テストケース3: エラーハンドリング
    result_error = execute_composite_skill(
        code="invalid",
        language="invalid_language"  # 無効な言語
    )
    
    assert "error" in result_error or result_error['summary']['issues_found'] == 0
```

---

### 複合スキルのベストプラクティス

```
1. 依存関係を明確に
   □ 各ステップの出力が明示的
   □ 次のステップの入力と一致
   □ 失敗時の代替手段を用意

2. エラーハンドリング
   □ 各ステップでエラーをキャッチ
   □ 部分的な失敗時の対応を定義
   □ ロールバック機構を用意

3. パフォーマンス
   □ 並列化できる部分は並列実行
   □ スキム間の矛盾を解決
   □ キャッシング機構を検討

4. 監視・トレーサビリティ
   □ 各ステップの実行時間を計測
   □ 中間結果をログに記録
   □ エラーの根本原因を特定可能に

5. バージョン管理
   □ 依存スキルのバージョンを指定
   □ 互換性マトリックスを管理
   □ 破壊的変更時の対応を計画
```

---

### チェックリスト（複合スキル実装）

```
設計フェーズ：
□ 個別スキルでテスト
□ ワークフローを図示
□ 各ステップの入力/出力を定義
□ エラーケースを想定

実装フェーズ：
□ ステップを1つずつ実装
□ 中間状態のテスト
□ エラーハンドリング実装
□ ロギング・計測実装

テストフェーズ：
□ 単体テスト（各ステップ）
□ 統合テスト（全体フロー）
□ エッジケーステスト
□ パフォーマンステスト
□ 失敗シナリオテスト

配備フェーズ：
□ ドキュメント完成
□ 依存スキルの準備確認
□ 段階的なロールアウト
□ 監視・アラート設定
```

---

### まとめ

複合スキルは：

| 側面 | ポイント |
|------|---------|
| **威力** | 単独スキルより大きな価値を提供 |
| **設計** | 明確な依存関係と明示的な入力/出力 |
| **エラー** | 各ステップでの堅牢なハンドリング |
| **パフォーマンス** | 可能な限り並列化 |
| **テスト** | 統合テストが特に重要 |
| **保守** | 依存スキルの更新に注意 |

→ 次へ: [Part 5-2: API統合と外部ツール連携](#section-05-advanced-topics-02-api-integration)

## Part 5-2: API統合と外部ツール連携 {#section-05-advanced-topics-02-api-integration}


Agent Skills で外部 API やツールと統合し、より強力な機能を実現する方法を学びます。

---

### 外部 API 統合パターン

#### パターン1: LLM API への直接統合

Agent Skills は Copilot の内部 LLM を利用していますが、さらに外部 LLM API を活用することも可能です：

```json
{
  "id": "multi-llm-analysis",
  "name": "複数LLMによる分析",
  "description": "OpenAI, Claude, Gemini など複数 LLM を使用して、より信頼性の高い分析を実施",
  
  "externalAPIs": [
    {
      "id": "openai-api",
      "type": "llm",
      "endpoint": "https://api.openai.com/v1/chat/completions",
      "authenticationType": "bearer_token",
      "requiredToken": "OPENAI_API_KEY"
    },
    {
      "id": "anthropic-api",
      "type": "llm",
      "endpoint": "https://api.anthropic.com/v1/messages",
      "authenticationType": "bearer_token",
      "requiredToken": "ANTHROPIC_API_KEY"
    }
  ],
  
  "parameters": {
    "code": {
      "type": "string",
      "description": "分析対象のコード"
    },
    "useLLMs": {
      "type": "array",
      "description": "使用するLLMサービス",
      "items": {"type": "string"},
      "enum": ["copilot", "openai", "anthropic"],
      "default": ["copilot"]
    }
  },
  
  "outputFormat": {
    "type": "object",
    "schema": {
      "properties": {
        "analyses": {
          "type": "array",
          "items": {
            "properties": {
              "llm": {"type": "string"},
              "result": {"type": "object"},
              "confidence": {"type": "number"}
            }
          }
        },
        "consensus": {
          "type": "object",
          "description": "複数LLMの結果をマージした最終結果"
        }
      }
    }
  }
}
```

#### 複数 LLM 統合の実装例

```python
import asyncio
from typing import List, Dict, Any

class MultiLLMAnalyzer:
    """複数 LLM による分析"""
    
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.analyzers = {
            "openai": OpenAIAnalyzer(api_keys.get("OPENAI_API_KEY")),
            "anthropic": AnthropicAnalyzer(api_keys.get("ANTHROPIC_API_KEY")),
            "copilot": CopilotAnalyzer()  # 内部LLM
        }
    
    async def analyze_with_multiple_llms(self, 
                                        code: str,
                                        llms: List[str]) -> Dict[str, Any]:
        """複数のLLMで並列分析"""
        
        tasks = []
        for llm_name in llms:
            if llm_name in self.analyzers:
                task = self._analyze_with_llm(llm_name, code)
                tasks.append(task)
        
        # 並列実行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 結果を統合
        return self._aggregate_results(results, llms)
    
    async def _analyze_with_llm(self, llm_name: str, code: str) -> Dict[str, Any]:
        """単一のLLMで分析"""
        
        analyzer = self.analyzers[llm_name]
        
        try:
            result = await analyzer.analyze(code)
            return {
                "llm": llm_name,
                "status": "success",
                "result": result,
                "confidence": self._calculate_confidence(result)
            }
        except Exception as e:
            return {
                "llm": llm_name,
                "status": "error",
                "error": str(e)
            }
    
    def _aggregate_results(self, 
                          results: List[Dict],
                          llms: List[str]) -> Dict[str, Any]:
        """複数の分析結果を統合"""
        
        successful_results = [r for r in results 
                             if r.get("status") == "success"]
        
        if not successful_results:
            return {
                "error": "All LLM analyses failed",
                "details": results
            }
        
        # コンセンサスを計算
        consensus = self._calculate_consensus(successful_results)
        
        return {
            "analyses": results,
            "consensus": consensus,
            "success_rate": len(successful_results) / len(results),
            "recommendation": self._generate_recommendation(consensus)
        }
    
    def _calculate_consensus(self, results: List[Dict]) -> Dict[str, Any]:
        """複数結果からコンセンサスを生成"""
        # スコアの平均化、投票ベースの判定等
        scores = [r['result'].get('score', 0) for r in results]
        
        return {
            "average_score": sum(scores) / len(scores),
            "high_confidence_findings": self._find_common_issues(results)
        }
    
    def _find_common_issues(self, results: List[Dict]) -> List[str]:
        """複数LLMが指摘した共通の問題"""
        # 複数LLMが同じ問題を指摘した場合、信頼度が高い
        all_issues = []
        for r in results:
            all_issues.extend(r['result'].get('issues', []))
        
        # カウント して、複数回指摘された問題をフィルタ
        from collections import Counter
        issue_counts = Counter(all_issues)
        return [issue for issue, count in issue_counts.items() 
                if count >= len(results) // 2]  # 過半数が指摘した問題
```

---

#### パターン2: データベース / データソース統合

```json
{
  "id": "code-review-with-kb",
  "name": "ナレッジベース連携コードレビュー",
  "description": "組織のナレッジベースとコーディング標準を参照して、カスタマイズされたコードレビューを実施",
  
  "externalDataSources": [
    {
      "id": "knowledge-base",
      "type": "database",
      "connection": {
        "type": "rest_api",
        "baseUrl": "https://api.company.com/kb",
        "authentication": "api_key"
      },
      "queryTemplate": "/search?query={query}&limit=5"
    },
    {
      "id": "code-standards",
      "type": "configuration",
      "connection": {
        "type": "github_repo",
        "repo": "org/coding-standards",
        "branch": "main"
      }
    }
  ],
  
  "prompt": {
    "system": "You are a code reviewer with access to company knowledge base and coding standards.",
    "template": "Review this {language} code:\n{code}\n\nConsider:\n1. Company coding standards (from {coding_standards_content})\n2. Similar past issues (from knowledge base): {kb_results}\n\nProvide review with focus on: {focus_areas}"
  }
}
```

#### ナレッジベース統合の実装例

```python
import aiohttp
import json
from typing import List, Dict

class KnowledgeBaseIntegration:
    """組織のナレッジベースと統合"""
    
    def __init__(self, kb_endpoint: str, api_key: str):
        self.kb_endpoint = kb_endpoint
        self.api_key = api_key
        self.kb_cache = {}
    
    async def search_knowledge_base(self, query: str, limit: int = 5) -> List[Dict]:
        """ナレッジベースで検索"""
        
        cache_key = f"{query}:{limit}"
        if cache_key in self.kb_cache:
            return self.kb_cache[cache_key]
        
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"{self.kb_endpoint}/search"
            params = {"query": query, "limit": limit}
            
            async with session.get(url, params=params, headers=headers) as resp:
                if resp.status == 200:
                    results = await resp.json()
                    self.kb_cache[cache_key] = results
                    return results
                else:
                    raise Exception(f"KB search failed: {resp.status}")
    
    async def fetch_coding_standards(self, language: str) -> str:
        """言語別のコーディング標準を取得"""
        
        cache_key = f"standards:{language}"
        if cache_key in self.kb_cache:
            return self.kb_cache[cache_key]
        
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"{self.kb_endpoint}/standards/{language}"
            
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    standards = await resp.text()
                    self.kb_cache[cache_key] = standards
                    return standards
                else:
                    return f"No standards found for {language}"
    
    async def enhance_prompt_with_knowledge(self, 
                                           template: str,
                                           code: str,
                                           language: str) -> str:
        """ナレッジベース情報を含むプロンプトを生成"""
        
        # 関連するナレッジ項目を検索
        relevant_kb = await self.search_knowledge_base(
            query=f"code review for {language}",
            limit=3
        )
        
        # コーディング標準を取得
        standards = await self.fetch_coding_standards(language)
        
        # プロンプトを拡張
        kb_text = "\n".join([
            f"- {item['title']}: {item['content'][:200]}"
            for item in relevant_kb
        ])
        
        enhanced_prompt = template.format(
            language=language,
            code=code,
            kb_results=kb_text,
            coding_standards_content=standards[:1000]
        )
        
        return enhanced_prompt
```

---

### GitHub / GitLab 統合

#### スキルとGit統合の例

```json
{
  "id": "auto-code-review",
  "name": "自動コードレビュー",
  "description": "PRを自動的にレビューしてコメントを追加",
  
  "cicdIntegration": {
    "triggers": [
      "pull_request_opened",
      "pull_request_synchronize"
    ],
    "webhookEndpoint": "https://your-skill-server.com/webhook"
  },
  
  "gitIntegration": {
    "type": "github",
    "requiredScopes": [
      "pull_request:read",
      "pull_request:comment",
      "contents:read"
    ],
    "actions": [
      {
        "trigger": "changes_detected",
        "action": "post_review_comment",
        "format": "github_review"
      }
    ]
  }
}
```

#### GitHub Actions ワークフロー統合

```yaml
# .github/workflows/copilot-skill-review.yml
name: Copilot Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Get changed files
        id: changed-files
        run: |
          git diff --name-only ${{ github.event.pull_request.base.sha }} HEAD > /tmp/changed_files.txt
          cat /tmp/changed_files.txt
      
      - name: Run Copilot Skill Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          COPILOT_API_KEY: ${{ secrets.COPILOT_API_KEY }}
        run: |
          python scripts/run_skill_review.py \
            --pr ${{ github.event.pull_request.number }} \
            --skill auto-code-review
      
      - name: Post review comments
        if: always()
        run: |
          python scripts/post_review_comments.py \
            --pr ${{ github.event.pull_request.number }}
```

#### PR レビュー実装例

```python
import os
from github import Github

class AutoCodeReviewSkill:
    """GitHub PR への自動コードレビュー"""
    
    def __init__(self, github_token: str, skill_api: SkillAPI):
        self.github = Github(github_token)
        self.skill_api = skill_api
    
    async def review_pull_request(self, org: str, repo: str, pr_number: int):
        """プルリクエストをレビュー"""
        
        repo = self.github.get_repo(f"{org}/{repo}")
        pr = repo.get_pull(pr_number)
        
        # PR内の全てのファイルを取得
        files = pr.get_files()
        
        for file in files:
            if not self._should_review(file.filename):
                continue
            
            # ファイルのコンテンツを取得
            content = repo.get_contents(file.filename, ref=pr.head.sha).decoded_content
            
            # Skillで分析
            review_result = await self.skill_api.execute(
                skill_id="analyze-code-quality",
                parameters={
                    "code": content,
                    "language": self._detect_language(file.filename)
                }
            )
            
            # コメントを投稿
            for issue in review_result.get('issues', []):
                self._post_review_comment(
                    pr=pr,
                    filename=file.filename,
                    line=issue['line_number'],
                    comment=f"{issue['severity']}: {issue['description']}"
                )
    
    def _should_review(self, filename: str) -> bool:
        """review対象のファイルか判定"""
        skip_patterns = ['.md', '.txt', '.json', 'package-lock.json']
        return not any(filename.endswith(p) for p in skip_patterns)
    
    def _detect_language(self, filename: str) -> str:
        """ファイル拡張子から言語を判定"""
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go'
        }
        for ext, lang in ext_to_lang.items():
            if filename.endswith(ext):
                return lang
        return 'unknown'
    
    def _post_review_comment(self, pr, filename: str, line: int, comment: str):
        """PR にコメントを投稿"""
        pr.create_review_comment(
            body=comment,
            commit=pr.head.commit,
            path=filename,
            line=line
        )
```

---

### Slack / Teams 統合

#### スキル結果を Slack に通知

```python
import aiohttp
from typing import Dict, Any

class SlackNotifier:
    """Slack への通知"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_skill_result(self, 
                               skill_id: str,
                               result: Dict[str, Any],
                               channel: str = None):
        """スキルの実行結果を Slack に投稿"""
        
        message = self._format_result_as_slack_message(skill_id, result)
        
        payload = {
            "channel": channel,
            "blocks": message
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.webhook_url, json=payload) as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to post to Slack: {resp.status}")
    
    def _format_result_as_slack_message(self, 
                                       skill_id: str,
                                       result: Dict) -> List[Dict]:
        """実行結果を Slack メッセージ形式に変換"""
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"✓ Skill Executed: {skill_id}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\nSuccess"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Execution Time:*\n{result.get('execution_time', 'N/A')}"
                    }
                ]
            }
        ]
        
        # 結果に応じてブロックを追加
        if 'issues' in result:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Issues Found:* {len(result['issues'])}\n" +
                            "\n".join([f"• {issue['description']}" 
                                      for issue in result['issues'][:5]])
                }
            })
        
        return blocks
```

---

### 外部 API の認証とセキュリティ

#### API キー管理

```python
import os
from typing import Dict
from cryptography.fernet import Fernet

class SecureAPIKeyManager:
    """API キーの安全な管理"""
    
    def __init__(self, master_key: str = None):
        # 環境変数から master key を取得
        self.master_key = master_key or os.getenv('MASTER_ENCRYPTION_KEY')
        self.cipher = Fernet(self.master_key.encode())
    
    def store_api_key(self, service: str, api_key: str):
        """API キーを暗号化して保存"""
        encrypted = self.cipher.encrypt(api_key.encode())
        
        # 環境変数として保存（本番環境では安全なシークレット管理サービスを使用）
        os.environ[f"{service.upper()}_API_KEY_ENCRYPTED"] = encrypted.decode()
    
    def retrieve_api_key(self, service: str) -> str:
        """API キーを取得"""
        encrypted_key = os.getenv(f"{service.upper()}_API_KEY_ENCRYPTED")
        
        if not encrypted_key:
            raise ValueError(f"API key for {service} not found")
        
        try:
            decrypted = self.cipher.decrypt(encrypted_key.encode())
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt API key: {e}")
    
    def validate_api_key_format(self, service: str, api_key: str) -> bool:
        """API キーの形式をバリデート"""
        patterns = {
            "openai": r"^sk-",
            "anthropic": r"^sk-ant-",
            "github": r"^ghp_"
        }
        
        pattern = patterns.get(service.lower())
        if not pattern:
            return True  # パターン不明な場合はスキップ
        
        import re
        return bool(re.match(pattern, api_key))
```

---

### チェックリスト（API統合実装）

```
設計フェーズ：
□ 外部 API の選定・評価
□ 認証方式の決定
□ フォールバック戦略の計画
□ セキュリティリスク評価

実装フェーズ：
□ API クライアントの実装
□ エラーハンドリング
□ リトライ・タイムアウト設定
□ キャッシング戦略

セキュリティ：
□ API キーの安全な保管
□ 通信の暗号化（HTTPS）
□ レート制限への対応
□ 入力バリデーション

テスト・監視：
□ API エラーのテスト
□ レート制限下での動作
□ パフォーマンステスト
□ アラート・監視の設定
```

---

### まとめ

| 統合タイプ | ポイント |
|----------|---------|
| **複数LLM** | 信頼性向上、多角的な分析 |
| **ナレッジベース** | 組織固有のコンテキスト追加 |
| **GitHub/GitLab** | 開発フローへの統合 |
| **ChatOps** | リアルタイムな通知・操作 |
| **セキュリティ** | API キーの安全管理が重要 |

→ 次へ: [Part 5-3:ベストプラクティスと推奨パターン](#section-05-advanced-topics-03-best-practices)

## Part 5-3: ベストプラクティスと推奨パターン {#section-05-advanced-topics-03-best-practices}


GitHub Copilot Agent Skills の設計・実装・運用における最良の実践をまとめます。

---

### スキル設計の黄金法則

#### 原則1: 単一責任の原則（Single Responsibility）

```
❌ 悪い例：
スキル ID: all-in-one-code-helper
説明: "コード分析、修正提案、テスト生成、ドキュメント作成を全てやる"

問題:
- テストが複雑になる
- 1つ失敗すると全体が停止
- 再利用が困難
- 保守が難しい

✓ 良い例：
スキル1: analyze-code-quality
スキル2: generate-code-fixes
スキル3: generate-unit-tests
スキル4: generate-documentation

利点:
- 各スキルが明確な責務を持つ
- 独立してテスト・改善可能
- 他のスキルと組み合わせ可能
- 保守が容易
```

#### 原則2: 明確な入出力契約

```json
例: analyze-code-quality スキル

✓ 明確な入力定義：
{
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "Python, JavaScript, TypeScript, Java, Go のコード",
      "minLength": 10,
      "maxLength": 10000,
      "required": true
    },
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "typescript", "java", "go"],
      "description": "プログラミング言語の明示的な指定",
      "required": true
    }
  }
}

✓ 明確な出力定義：
{
  "outputFormat": {
    "type": "object",
    "schema": {
      "type": "object",
      "properties": {
        "issues": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "line_number": {"type": "integer"},
              "severity": {"enum": ["critical", "high", "medium", "low"]},
              "category": {"type": "string"},
              "description": {"type": "string"},
              "suggestion": {"type": "string"}
            },
            "required": ["line_number", "severity", "description"]
          }
        }
      },
      "required": ["issues"]
    }
  }
}
```

#### 原則3: エラーに強い設計

```python
# ❌ エラーハンドリング不足
def analyze_code(code, language):
    prompt = f"Analyze {language} code: {code}"
    return call_llm(prompt)

# ✓ エラー処理を含む
def analyze_code(code: str, language: str) -> Dict[str, Any]:
    """コード分析（エラーハンドリング付き）"""
    
    try:
        # 入力バリデーション
        validate_inputs(code, language)
        
        # プロンプト構築
        prompt = build_prompt(code, language)
        
        # LLM呼び出し（タイムアウト設定）
        response = call_llm(prompt, timeout=10)
        
        # 出力バリデーション
        output = validate_output(response)
        
        return {
            "status": "success",
            "result": output
        }
    
    except ValueError as e:
        # 入力エラー
        return {
            "status": "error",
            "error_type": "invalid_input",
            "message": str(e)
        }
    
    except TimeoutError:
        return {
            "status": "error",
            "error_type": "timeout",
            "message": "Analysis took too long"
        }
    
    except Exception as e:
        # 予期しないエラーをログして、ユーザーフレンドリーなメッセージを返す
        logger.error(f"Unexpected error: {e}")
        return {
            "status": "error",
            "error_type": "internal_error",
            "message": "An error occurred during analysis"
        }
```

---

### スキル実装のパターン

#### パターン1: ストレートスルー（Simple Pass-Through）

最もシンプルで共通なパターン。ユーザー入力をそのまま LLM に渡し、結果をフォーマット：

```python
def execute_simple_skill(code: str, language: str) -> Dict:
    """シンプルなスキル（パイプラインなし）"""
    
    prompt = f"""
    Analyze this {language} code:
    
    {code}
    
    Return analysis as JSON:
    {{
      "readability": <score>,
      "performance": <score>,
      "security": <score>
    }}
    """
    
    response = call_llm(prompt)
    return parse_json(response)
```

**使用例:** analyze-code-quality, generate-documentation

#### パターン2: エンリッチメント（Enrichment）

入力に情報を追加して、より文脈豊かなプロンプトを構築：

```python
def execute_enriched_skill(code: str, language: str, context: str = None) -> Dict:
    """コンテキスト情報で拡張したスキル"""
    
    # 追加情報を収集
    imports = extract_imports(code)
    complexity = measure_complexity(code)
    
    # コンテキストと共に LLM に渡す
    prompt = f"""
    Analyze this {language} code:
    
    Metadata:
    - Complexity: {complexity}
    - Imports: {imports}
    - Context: {context or 'None'}
    
    Code:
    {code}
    
    Provide detailed analysis...
    """
    
    return call_llm(prompt)
```

**使用例:** classify-code-issues, recommend-refactoring

#### パターン3: アグリゲーション（Aggregation）

複数の部分結果を集約して最終結果を生成：

```python
def execute_aggregated_skill(code: str) -> Dict:
    """複数の観点から分析して集約"""
    
    # 並列で複数の分析を実行
    analyses = asyncio.gather(
        analyze_readability(code),
        analyze_performance(code),
        analyze_security(code)
    )
    
    # 結果を集約
    return aggregate_results(analyses)
```

**使用例:** comprehensive-code-review, multi-dimensional-analysis

#### パターン4: フィルタリング（Filtering）

大量のデータから重要な部分を抽出：

```python
def execute_filtered_skill(logs: str, error_type: str) -> Dict:
    """ログから特定エラーをフィルタ"""
    
    # ログから関連部分のみ抽出
    relevant_lines = filter_logs(logs, error_type)
    
    # 抽出した部分のみを LLM で分析
    prompt = f"""
    Analyze these {error_type} errors:
    
    {relevant_lines}
    
    Provide root cause analysis and solutions.
    """
    
    return call_llm(prompt)
```

**使用例:** error-log-analyzer, trace-debugger

---

### テストのベストプラクティス

#### テスト構造

```python
import pytest
from skill import AnalyzeCodeQualitySkill

class TestAnalyzeCodeQualitySkill:
    """スキルの包括的テスト"""
    
    @pytest.fixture
    def skill(self):
        return AnalyzeCodeQualitySkill()
    
    # カテゴリー1: 正常系テスト
    def test_valid_python_code(self, skill):
        """有効な Python コードの分析"""
        code = "def hello():\n    print('Hello')"
        result = skill.execute(code, "python")
        
        assert result['status'] == 'success'
        assert 'issues' in result
        assert isinstance(result['issues'], list)
    
    # カテゴリー2: エッジケーステスト
    def test_empty_code(self, skill):
        """空のコード"""
        result = skill.execute("", "python")
        assert result['status'] == 'error'
        assert 'code_too_short' in result['error_type']
    
    def test_very_large_code(self, skill):
        """非常に大きなコード"""
        large_code = "x = 1\n" * 5000
        result = skill.execute(large_code, "python")
        
        # タイムアウトのテスト
        assert 'timeout' not in result.get('error_type', '')
    
    # カテゴリー3: エラー処理テスト
    def test_invalid_language(self, skill):
        """サポートされない言語"""
        code = "print('hello')"
        result = skill.execute(code, "cobol")
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'unsupported_language'
    
    def test_malformed_code(self, skill):
        """文法エラーのあるコード"""
        code = "def hello(\n    print('hi')"  # 括弧閉じ忘れ
        result = skill.execute(code, "python")
        
        # 文法エラーも分析対象
        assert result['status'] == 'success'
        assert len(result['issues']) > 0
    
    # カテゴリー4: パフォーマンステスト
    def test_response_time_sla(self, skill):
        """SLA: 3秒以内"""
        code = "x = 1\n" * 100
        
        import time
        start = time.time()
        skill.execute(code, "python")
        duration = time.time() - start
        
        assert duration < 3.0
    
    # カテゴリー5: 出力形式テスト
    def test_output_schema_validation(self, skill):
        """出力スキーマの検証"""
        code = "x = 1"
        result = skill.execute(code, "python")
        
        # スキーマ検証
        assert isinstance(result, dict)
        assert 'issues' in result
        
        for issue in result['issues']:
            assert 'line_number' in issue
            assert 'severity' in issue
            assert issue['severity'] in ['critical', 'high', 'medium', 'low']
```

---

### ドキュメンテーションの標準

#### README テンプレート

```markdown
# [Skill Name]

## 概要
1文で何をするスキルか説明。

## 使用例

### 基本的な使い方
```
コード例
```

### 応用例
```
高度な使用方法
```

## パラメータ

| パラメータ | 型 | 必須 | 説明 | 例 |
|----------|----|----|------|-----|
| param1 | string | ✓ | 説明 | example |

## 出力形式

```json
{
  "result": "...",
  "metadata": {...}
}
```

## 制限事項

- 最大入力: 10,000文字
- タイムアウト: 10秒
- 対応言語: Python, JavaScript

## よくある質問

### Q: 入力サイズの制限は?
A: ...

## トラブルシューティング

### エラー: "Invalid input"
A: ...

## 参考資料
- [スキル設計ガイド]
- [API ドキュメント]
```

---

### 運用のベストプラクティス

#### モニタリングメトリクス

```yaml
Primary Metrics (見守るべき主要指標):
  Response Time:
    Target: < 3 秒
    Alert: > 5 秒
  
  Success Rate:
    Target: > 99%
    Alert: < 95%
  
  Error Rate by Type:
    Critical Errors: 0 件/日
    User Errors: < 1% of requests

Secondary Metrics (傾向把握):
  Adoption:
    Daily Active Users: 増加傾向？
    Usage Pattern: どのパラメータが人気？
  
  Quality:
    User Rating: 4.0以上？
    Support Tickets: 減少傾向？
```

#### インシデント対応の流れ

```
1. 検出（Detection）
   └─ アラートが発火
   └─ 利用者からの報告

2. 応答（Response）
   └─ SLA確認・緊急度判定（1時間以内）
   └─ デバッグ開始
   └─ 利用者への対応報告

3. 修復（Mitigation）
   └─ ホットフィックス作成（4時間以内）
   └─ テスト実行
   └─ デプロイ・検証

4. 解決（Resolution）
   └─ 修復の確認・検証
   └─ 利用者への通知
   └─ Post-mortem 開催（24時間以内）

5. 学習（Learning）
   └─ 根本原因分析
   └─ 再発防止策の立案
   └─ 文書化・知識共有
```

---

### スキル開発フローチャート

```
START
  ↓
1. 要件定義
  □ 何を実現するか
  □ 誰が使うか
  □ 成功基準は
  ↓
2. 設計（低忠実度モックアップ）
  □ パラメータ定義
  □ 出力形式案
  □ プロンプトの大枠
  ↓
3. 実装
  □ スキル定義 JSON
  □ プロンプト最適化
  □ 基本テスト
  ↓
4. 内部テスト（作成者）
  □ 機能テスト
  □ エッジケーステスト
  └─ NO → 修正・改善 → テスト再実行
  ↓ YES
5. ベータテスト（限定ユーザー）
  □ 実運用での動作確認
  □ パフォーマンス計測
  □ UX フィードバック収集
  └─ NO → 改善 → 再テスト
  ↓ YES
6. ドキュメント完成
  □ README 作成
  □ トラブルシューティング
  □ 使用例充実
  ↓
7. リリース準備
  □ リリースノート作成
  □ 告知文準備
  □ SLA 文書化
  ↓
8. 公開・告知
  □ パッケージ公開
  □ ドキュメント公開
  □ チーム告知
  □ デモセッション（オプション）
  ↓
9. 運用開始
  □ メトリクス監視
  □ ユーザーサポート
  □ 定期レビュー
  ↓
10. 改善サイクル
  □ フィードバック収集
  □ 改善提案まとめ
  □ マイナー版更新
  ↓
END（継続監視）
```

---

### チェックリスト（スキル開発完了時）

#### 設計フェーズ
```
□ ユースケースが明確
□ 他のスキルとの関係が定義
□ パラメータが直感的
□ 出力形式が明確
```

#### 実装フェーズ
```
□ JSON スキーマが有効
□ プロンプトが最適化
□ エラーハンドリングが完全
□ API 呼び出しにタイムアウト設定
```

#### テストフェーズ
```
□ 正常系テストが全て成功
□ エッジケーステストが全て成功
□ エラーケーステストが全て成功
□ パフォーマンスが SLA を満たす
□ 出力形式が定義通り
```

#### ドキュメンテーション
```
□ README が完成（使用例含む）
□ パラメータが全て説明
□ FAQ / トラブルシューティングがある
□ よくあるエラーと対処法がある
```

#### 運用準備
```
□ モニタリングが設定
□ アラート閾値が定義
□ SLA が文書化
□ サポート体制が整備
□ リリースノートが準備
```

---

### 年間キャパシティプランニング例

小規模チーム（10人）の場合：

```
Q1: インフラ / 基礎スキル整備
  - 3スキル開発・リリース
  - 既存スキル最適化 (2スキル)

Q2: 実務スキル充実
  - 4スキル開発・リリース
  - ベータプログラム運営

Q3: AI/ML統合
  - 2スキル開発（高度）
  - 既存スキル改善 (3スキル)

Q4: 運用効率化
  - 1スキル開発
  - モニタリング・運用体制改善
  - 年間レビュー・計画策定

年間合計: 10新規スキル + 8既存スキル改善
= チーム全体で20スキルのライフサイクル管理
```

---

### 業界別専門パターン

#### FinTech（金融）

```
重視すべき側面：
- セキュリティ / コンプライアンス
- 精度 / 誤差管理
- 監査ログ

推奨スキル：
1. compliance-checker (規制要件チェック)
2. risk-analyzer (リスク分析)
3. audit-report-generator (監査レポート)
4. financial-code-reviewer (金融コードレビュー)
```

#### Healthcare（医療）

```
重視すべき側面：
- プライバシー / HIPAA
- 精度（診断補助）
- 国際標準準拠

推奨スキル：
1. privacy-validator (プライバシー検証)
2. medical-code-analyzer (医療コード解析)
3. clinical-documentation-helper (臨床文書作成支援)
4. standards-compliance-checker (標準準拠チェック)
```

#### Enterprise（エンタープライズ）

```
重視すべき側面：
- スケーラビリティ
- エンタープライズセキュリティ
- 統合（既存システムとの）

推奨スキル：
1. legacy-code-analyzer (レガシーコード分析)
2. api-migrator (API マイグレーション支援)
3. security-audit (セキュ
リティ監査)
4. performance-optimizer (パフォーマンス最適化)
```

---

### まとめ：スキル開発の黄金原則

```
1. 単一責任の原則を守る
   → 組み合わせやすく、テストしやすい

2. 明確な入出力契約
   → ユーザーが期待を持てる

3. エラーに強い設計
   → 本番で信頼されるスキル

4. 包括的なテスト
   → 品質の確保

5. 充実したドキュメント
   → ユーザー采用の促進

6. 継続的な監視・改善
   → 長期の成功を確保

7. ユーザーから学ぶ
   → フィードバック→改善のサイクル
```

---

### リソース

#### 内部ドキュメント
- [スキル設計ガイド](../../docs/DESIGN_GUIDE.md)
- [実装テンプレート](../../samples/skill-template.json)
- [テストテンプレート](../../samples/test-template.py)

#### 外部リソース
- [GitHub Copilot 公式ドキュメント](https://docs.github.com/copilot)
- [LLM ベストプラクティス](https://platform.openai.com/docs/guides/prompt-engineering)
- [API 設計ガイド](https://swagger.io/resources/articles/best-practices-in-api-design/)

#### コミュニティ
- [Q&A フォーラム](#)
- [スキル共有レジストリ](#)
- [月1回のお疲れさま会](#)

---

🎉 **チュートリアル完了！**

ここまで学んだことで、あなたは GitHub Copilot Agent Skills について、
以下ができるようになっています：

✓ スキルの基本を理解している
✓ 複数の実装パターンの違いがわかる
✓ 本番対応のスキルを設計できる
✓ チーム内でスキルを共有できる
✓ パフォーマンスを最適化できる
✓ 問題が発生しても解決できる
✓ 複合スキルや API 統合ができる
✓ ベストプラクティスを実践できる

---

### スキル作成のベストプラクティス

#### 1. 命名規則（Naming Conventions）

##### ルール

```
推奨：動名詞形（verb + -ing）
├─ processing-pdfs
├─ analyzing-spreadsheets
├─ managing-databases
└─ testing-code

許容：名詞句
├─ pdf-processing
├─ spreadsheet-analysis
└─ database-management

❌ 避けるべき
├─ helper（曖昧）
├─ utils（スコープ不明）
├─ tools（汎用すぎ）
├─ anthropic-helper（予約語）
└─ claude-tools（予約語）
```

##### 効果

```
一貫性のあるネーミング
├─ スキルの機能が一目で判断できる
├─ 複数スキルを参照しやすい
└─ 専門的な整理が可能

例：チーム内スキル一覧
processing-*
├─ processing-pdfs
├─ processing-csvs
└─ processing-images

analyzing-*
├─ analyzing-code-quality
├─ analyzing-performance
└─ analyzing-security

managing-*
├─ managing-databases
├─ managing-dependencies
└─ managing-configurations
```

#### 2. 簡潔さ（Conciseness）

##### 原則：トークンは共有資源

```
SKILL.md 読み込み時点でのトークン効率：

メタデータ（常に先読み）
└─ ～100トークン

SKILL.md 本文（スキル起動時）
├─ 推奨：<500行
├─ 上限：1000行
└─ ～5000トークン

参考資料（オンデマンド）
├─ references/*.md
└─ 不要な時は読まない
```

##### チェック項目

```
✓ 「このパラグラフは必須か？」
├─ Claude は既にこれを知っているのか
└─ 削除してもスキルは動作するか

✓ 説明の冗長さを除去
├─ 「PDFは Portable Document Format の略で...」
│   → 削除（Claude は知っている）
├─ 「Python の open() 関数で...」
│   → 削除（詳細は不要）
└─ 「with文を使ってきちんとファイルを閉じる」
    → 簡略化：「with を使う」
```

#### 3. モデル別テスト（Model-Specific Testing）

##### テスト対象

```
Claude Haiku
├─ 速度：⭐⭐⭐⭐⭐
├─ 推論：⭐⭐
│   問題：詳しい指示がないと簡潔に実行
│   対策：具体的な例・ステップ・制約を明確に
└─ 低コスト・高速

Claude Sonnet
├─ 速度：⭐⭐⭐⭐
├─ 推論：⭐⭐⭐⭐
│   バランスが取れた性能
└─ 推奨モデル

Claude Opus
├─ 速度：⭐⭐⭐
├─ 推論：⭐⭐⭐⭐⭐
│   問題：オーバーエンジニアリングの危険
│   対策：冗長な指示を削除
└─ 複雑な タスク向け
```

##### テスト方法

```
ステップ1：Haiku でテスト
└─ 「詳細さが足りている？」
   - NO → 指示を明確化

ステップ2：Sonnet でテスト
└─ 「バランスが取れている？」

ステップ3：Opus でテスト
└─ 「オーバースペック設計がない？」
   - YES → 不要な指示を削除

結論：Haiku で成功 → 他のモデルも成功する傾向
```

#### 4. Anti-Patterns（避けるべきパターン）

##### Anti-Pattern 1: Windows パス

```
❌ Windows スタイル
├─ scripts\helper.py
├─ C:\path\to\skill
└─ reference\guide.md

✅ Unix スタイル（推奨）
├─ scripts/helper.py
├─ /path/to/skill
└─ reference/guide.md
```

**理由**
- Unix パスは全プラットフォームで動作
- Windows パスは Unix で失敗

##### Anti-Pattern 2: 過度な選択肢

```
❌ 複数アプローチの提示
"You can use pypdf, pdfplumber, PyMuPDF, pdf2image, 
 or several other libraries..."

✅ デフォルト + エスケープハッチ
"Use pdfplumber for text extraction.
For scanned PDFs requiring OCR, use pdf2image 
with pytesseract."
```

**メリット**
- エージェントの判断負荷が減る
- エスケープハッチで対応可能

##### Anti-Pattern 3: 時間依存情報

```
❌ 期限付き情報（すぐ陳腐化）
"If you're doing this before August 2025, 
use the old API."

✅ 履歴セクション
"## Current method
Use v2 API: api.example.com/v2/...

## Legacy patterns (deprecated Aug 2025)
<details>
<summary>Old v1 API</summary>
Use v1 API: api.example.com/v1/...
</details>"
```

##### Anti-Pattern 4: 曖昧な説明

```
❌ 有効性を説明しない
REQUEST_TIMEOUT = 47
MAX_RETRIES = 5

✅ 設計根拠を説明
# HTTP リクエストは通常 30 秒以内に完了
# より長いタイムアウトは低速接続対応
REQUEST_TIMEOUT = 30

# 3 リトライが大多数の一時的エラーを解決
MAX_RETRIES = 3
```

#### 5. 簡潔さチェックリスト

```
□ SKILL.md 本文が500行以内
□ 各セクションが明確な目的を持つ
□ 冗長な説明がない（Claude は多くを知っている）
□ パラメータの制約が明記
□ エラーメッセージが具体的
□ ファイル参照は相対パス（Unix スタイル）
□ 例は最小限で実用的
□ 難しい概念のみ説明、簡単なことは説明しない
□ 説明は3文以内を目指す
□ すべての指示に理由がある
```

#### 6. テスト駆動開発（Evaluation-Driven Development）

##### 流れ

```
1. テストケース設計（MIN 3個）
   ├─ 通常ケース（1-2個）
   └─ エッジケース（1個）

2. ベースライン実行（with/without スキル）
   ├─ Pass rate 計測
   ├─ Token 計測
   └─ 実行時間計測

3. Assertion 追加
   └─ 結果見てから追加（結果見ないと良い Assertion は書けない）

4. Pass rate が目標到達 or 改善停滞 → 完了
```

##### チェックリスト

```
評価フェーズ
□ evals.json に3個以上のテストケース
□ 通常ケース、技術的、エッジケースを混在
□ （オプション）with/without スキル比較実行
□ Pass rate 計測

改善フェーズ
□ 失敗パターンをデータで特定
□ SKILL.md を改善
□ 新しい iteration で再実行
□ 改善手止められるまで繰り返し
```

---

#### 次のステップ

1. **独自スキルの開発**
   実際に自分たちの課題を解決するスキルを作ってみましょう

2. **チーム内での展開**
   スキルを共有し、チームの生産性を向上させましょう

3. **コミュニティへの貢献**
   良いスキルは公開し、他のチームの役に立てましょう

4. **先進的なパターンの探索**
   複合スキル、API 統合、カスタム運用など、
   より高度なパターンに挑戦しください

頑張ってください！ 🚀
