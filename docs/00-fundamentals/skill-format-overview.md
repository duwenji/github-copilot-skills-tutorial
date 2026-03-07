# Part 0: スキル形式の選択と実装

## 重要な指摘

GitHub公式が推奨する **Agent Skills** の実装形式は **`SKILL.md`**です。  
このドキュメントでは、2つの形式の経緯、関係性、そして各々の利用場面と使い分けを説明します。

### 🎓 Agent Skills はオープンスタンダード

**重要**: Agent Skills は Anthropic による**オープンスタンダード**です。プロプライエタリ仕様ではなく、複数のプラットフォームで活用できるように設計されています。

| 側面 | 説明 |
|-----|------|
| **標準化主体** | Anthropic（Claude 開発元） |
| **公開仕様** | https://agentskills.io/ |
| **参考実装** | https://github.com/anthropics/skills |
| **コミュニティ** | GitHub Awesome Copilot、その他 |
| **ライセンス** | MIT など自由なライセンスで公開可能 |

---

## � サポートされるプラットフォーム

Agent Skills は、以下の環境で利用できます：

| プラットフォーム | ステータス | 説明 |
|-------|--------|------|
| **Copilot coding agent** | ✅ 利用可能 | GitHub.com の Copilot Editor で実行可能 |
| **GitHub Copilot CLI** | ✅ 利用可能 | コマンドラインから `gh copilot` コマンドで実行 |
| **VS Code Insiders** | ✅ プレビュー | VS Code Insiders 版で実験的にサポート |
| **VS Code（stable）** | 🔜 近日対応 | 通常版 VS Code では近日リリース予定 |
| **GitHub.com UI** | ✅ 利用可能 | GitHub.com のウェブインターフェースで実行 |

### 今から始める場合の推奨環境

```
【最初の学習】
→ GitHub.com の Copilot Editor（最も簡単）

【CLI作業が多い場合】
→ GitHub Copilot CLI

【VS Code を主に使う場合】
→ VS Code Insiders（安定版は近日リリース）
```

---

## �📋 フォーマットの経緯

### バージョン進化

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

### なぜ SKILL.md が採用されたのか

| 理由 | 詳細 |
|-----|------|
| **ユーザビリティ** | Markdown は開発者にとって自然な形式 |
| **可読性** | 記述と実行結果がほぼ同じ（WYSIWYG的） |
| **バージョン管理** | Git に自然に統合、変更追跡が容易 |
| **拡張性** | スクリプトや補助ファイルを付属させやすい |
| **コラボレーション** | チームでのレビュー・改善が直感的 |

---

## ① SKILL.md形式（公式推奨・エンドユーザー向け）

### 概要

**GitHub公式が推奨する、エンドユーザーが直接作成・管理するスキル定義形式**

```markdown
SKILL.md = 開発者が読み書きする「手順書」
```

### ファイル構造

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

### 実装例

#### 例1: シンプルなコードレビュースキル

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

#### 例2: GitHub Actions デバッグスキル（補助ファイル付き）

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

### 特徴

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

### 配置ガイド

| スコープ | 場所 | 用途 |
|--------|------|------|
| プロジェクト固有 | `.github/skills/` | そのリポジトリだけで使用 |
| チーム共有 | `.github/skills/` （複数リポで共通） | 複数プロジェクトで使用 |
| 個人スキル | `~/.copilot/skills/` | あなたのマシンでのみ |
| 組織共有 | GitHub Skills Registry | 企業内全体で共有 |

---

## ② JSON形式（内部通信・スキーマ検証用）

### 概要

**Copilot サーバー側で管理される、内部通信フォーマット**

```json
JSON = SKILL.md から自動抽出される「構造化データ」
```

### 目的

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

### 実装例

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

### 特徴

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

## ③ フォーマット選択ガイド

### 「どの場面で何を使うか」

#### SKILL.md を使うべき 

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

#### JSON を学ぶべき場面

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

## ④ 推奨される実装フロー

### ステップバイステップ

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

### 実装例：SKILL.md から開始

```
Week 1: SKILL.md で最初のスキルを作成
  └─ 目標：1-2時間で SKILL.md を完成

Week 2: チーム内での利用開始
  └─ 目標：フィードバック収集、改善

Week 3+: 必要に応じて JSON スキーマを追加
  └─ 複雑な検証が必要になった場合のみ
```

---

## ⑤ 比較表：SKILL.md vs JSON

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

## ⑥ チュートリアルでの位置づけ

### このチュートリアルについて

```
このチュートリアルの構成：

Part 1「基礎編」
  └─ SKILL.md の概念と使い方 ← 実装向け

Part 3「実装編」
  ├─ サンプル SKILL.md の実装例 ← 実際の形式
  └─ JSON スキーマも説明 ← 内部メカニズム理解用

Part 5「高度な活用」
  └─ 複合スキル、API統合 ← JSON スキーマご必要に応じて
```

### 推奨学習パス

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

## ⑦ よくある質問

### Q1. SKILL.md だけで十分？

**A:** ほとんどの場合、SKILL.md で十分です。

```
SKILL.md で始めましょう
    ↓
タイプチェック・出力検証が必要になったら
    ↓
その时初めて JSON スキーマを検討
```

### Q2. JSON は必須？

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

### Q3. SKILL.md から JSON は自動生成できる？

**A:** 部分的に可能です。

```
現状：
- Copilot が SKILL.md を読んでパラメータを推測
- 完全な JSON スキーマの自動生成ではない
- 複雑な検証が必要な場合は手動作成推奨
```

---

## まとめ

| What | SKILL.md | JSON |
|------|----------|------|
| **使うべき対象** | ほぼすべての開発者 | システム開発者・API設計者 |
| **実装形式** | 公式推奨 | 内部仕様 |
| **学習順序** | 1番目（Part 1）| 2-3番目（理解の深化用） |
| **実装難度** | ⭐ 簡単 | ⭐⭐⭐ 難しい |
| **判断基準** | **先ず SKILL.md で始めよう** | **複雑さが必要になったら検討** |

---

## 関連ドキュメント

- 📖 GitHub 公式: [Creating agent skills](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills)
- 📚 本チュートリアル
  - Part 1-1: Agent Skills とは
  - Part 3-1: スキル開発の始め方
