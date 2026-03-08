---
name: quiz-generator
description: プロジェクト配下のドキュメントをクイズセット化しJSON形式で出力します。
license: MIT
---

# Quiz Generator（汎用化版）

## 概要

**プロジェクト配下のドキュメント**を対話的なクイズセットに自動変換するスキルです。

> **参考資料**
> - 📋 [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) - 出力データの詳細仕様
> - ✅ [JSON スキーマ定義](./schemas/) - 自動バリデーション用のスキーマ（question-schema.json, question-set-schema.json, quizset-metadata-schema.json）

| 特徴 | 説明 |
|------|------|
| ✅ **自動生成** | ドキュメント構造を解析し、シリーズとクイズセットを自動生成 |
| ✅ **単一管理** | すべてのクイズを `tutorial/` に一元管理 |
| ✅ **段階的学習** | beginner → intermediate → advanced で難度を段階化 |
| ✅ **複数形式** | JSON, Markdown での出力に対応 |
| ✅ **拡張性** | 新規セクション追加時も自動的に対応 |

---

## クイックスタート

### 🚀 対話型オートメーション（推奨）

分析→自動判断→生成→検証を **ユーザー入力なしで自動実行**：

```yaml
action: "auto-flow"
doc_path: "docs"
target_audience: "progressive"
output_format: "json"
```

**特徴：**
- ✅ 4ステップを全自動で実行
- ✅ ドキュメント構造から自動判断してセクション構成を決定
- ✅ 段階的難度を自動適用
- ✅ 生成結果を自動検証
- ✅ ユーザーの判断・入力は不要

**結果：**
```
tutorial/github-copilot-skills-tutorial/
├── metadata.json
├── fundamentals/quiz.json
├── basics/quiz.json
├── comparison/quiz.json
├── implementation/quiz.json
├── advanced/quiz.json
├── VALIDATION_REPORT.md
└── README.md
```

### 📊 段階的実行（カスタマイズ）

各ステップで確認・調整しながら実行：

| Step | action | 役割 |
|------|--------|------|
| 1️⃣ | `analyze` | ドキュメント構造を分析、セクション自動検出 |
| 2️⃣ | `configure` | セクション順序・名前を手動調整（オプション） |
| 3️⃣ | `generate` | 確定構成でクイズを生成 |
| 4️⃣ | `validate` | 生成品質を検証（オプション） |

詳細は「[段階的実行フロー](#段階的実行フロー)」を参照してください。

---

## パラメータ仕様

### 対話型オートメーション（action: "auto-flow"）

**4ステップを自動で実行（ユーザー入力不要）**

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|----------|------|
| `action` | ✅ | - | `"auto-flow"` に固定 |
| `doc_path` | ✅ | - | ドキュメントフォルダ（例: `"docs"`) |
| `target_audience` | | `"progressive"` | 難度対象: `"beginner"` / `"intermediate"` / `"advanced"` / `"progressive"` |
| `difficulty_distribution` | | `"balanced"` | 難度配分: `"balanced"` / `"beginner_focused"` / `"advanced_focused"` |
| `output_format` | | `"json"` | 出力形式: `"json"` / `"markdown"` / `"both"` |
| `include_explanation` | | `true` | 各問の解説を含める |
| `auto_section_filter` | | `true` | ドキュメント数が少ないセクションを自動除外 |
| `min_docs_per_section` | | `1` | セクション保持の最小ドキュメント数 |
| `generate_validation_report` | | `true` | 生成完了後に検証レポートを生成 |
| `verbose` | | `false` | 実行ログを詳細出力 |

**実行例：**
```yaml
action: "auto-flow"
doc_path: "docs"
target_audience: "progressive"
output_format: "json"
auto_section_filter: true
min_docs_per_section: 1
```

**実行フロー：**
```
ドキュメント分析
    ↓
自動判断（セクション最適化）
    ↓
クイズセット生成
    ↓
品質検証
    ↓
完了
```

---

### ワンコマンド実行（action: "generate"）

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|----------|------|
| `action` | ✅ | - | `"generate"` に固定 |
| `doc_path` | ✅ | - | ドキュメントフォルダ（例: `"docs"`) |
| `output_format` | | `"json"` | 出力形式: `"json"` / `"markdown"` / `"both"` |
| `target_audience` | | `"intermediate"` | 難度対象: `"beginner"` / `"intermediate"` / `"advanced"` / `"progressive"` |
| `difficulty_distribution` | | `"balanced"` | 難度配分: `"balanced"` / `"beginner_focused"` / `"advanced_focused"` |
| `question_count` | | `"auto"` | 全体の問題数（`"auto"` で自動計算） |
| `include_explanation` | | `true` | 各問の解説を含める |

### 段階的実行時

#### Step 1: analyze

```yaml
action: "analyze"
doc_path: "docs"
```

**出力:** `tutorial/.analysis.json`

#### Step 2: configure

```yaml
action: "configure"
analysisFile: "tutorial/.analysis.json"
adjustments:
  seriesName: "修正後のシリーズ名"
  sections:
    - id: "fundamentals"
      name: "修正後のセクション名"
      order: 1
      enabled: true
```

**出力:** `tutorial/.series-config.json`

#### Step 3: generate

```yaml
action: "generate"
configFile: "tutorial/.series-config.json"
target_audience: "progressive"  # ← 段階的難度設定
difficulty_distribution: "balanced"
output_format: "json"
```

**出力:** 各セクションの `quiz.json` と `metadata.json`

#### Step 4: validate

```yaml
action: "validate"
outputDir: "tutorial"
```

**出力:** `tutorial/{シリーズID}/VALIDATION_REPORT.md`

### target_audience の難度設定

| 値 | 説明 | 使用シーン |
|----|------|----------|
| `"beginner"` | 初級者向け | 初心者対象のコース |
| `"intermediate"` | 中級者向け | 基本を学んだ学習者 |
| `"advanced"` | 上級者向け | 専門知識が必要な場面 |
| `"progressive"` | **段階的** | beginnerから徐々にadvancedへ（推奨） |

**「progressive」で段階的難度設定：**
```
Section 1: 80% beginner,    20% intermediate
Section 2: 30% beginner,    60% intermediate,  10% advanced
Section 3: 10% intermediate, 70% advanced,     20% expert
...
```

---

## 対話型オートメーション（auto-flow）の自動判断ロジック

`action: "auto-flow"` 実行時、スキルは以下の基準で自動的に判断しながら実行します。ユーザーの入力は一切不要です。

### 1️⃣ セクション検出 & 最適化

**自動判断基準：**

| 判定項目 | 判定基準 | 判定内容 |
|---------|---------|---------|
| **セクション構成** | ドキュメント階層 | フォルダ構造から自動検出 |
| **セクション順序** | フォルダプレフィックス数字 | `01-xxx`, `02-xxx` で自動ソート |
| **セクション有効/無効** | `min_docs_per_section` | ドキュメント数が閾値未満なら自動除外 |
| **セクション名** | フォルダ名 / README.md H1 | 英数字を日本語に自動翻訳（LLM利用） |
| **ID生成** | ケバブケース化 | 自動生成・重複チェック |

**例：**
```
docs/
├── 00-fundamentals/          → セクション有効（2ファイル）
│   ├── skill-format-overview.md
│   └── README.md
├── 01-basics/                → セクション有効（3ファイル）
│   ├── introduction.md
│   ├── vs-traditional.md
│   └── how-skills-work.md
├── 05-advanced-topics/       → セクション有効（3ファイル）
│   ├── composite-skills.md
│   ├── api-integration.md
│   └── best-practices.md
└── extras/                   → セクション除外（1ファイル < 最小2）
    └── appendix.md
```

### 2️⃣ 難度分布の自動決定

**自動判断ロジック：**

- **target_audience: "progressive"** の場合（推奨）
  ```
  Section 1 (1番目):   80% beginner,    20% intermediate
  Section 2 (2番目):   50% beginner,    40% intermediate,  10% advanced
  Section 3 (3番目):   20% beginner,    50% intermediate,  30% advanced
  Section N (最後):    10% intermediate, 50% advanced,      40% expert
  ```
  → セクション進行に従い、難度が段階的に上昇

- **target_audience: "beginner"** の場合
  ```
  全セクション: 80% beginner, 15% intermediate, 5% advanced
  ```

- **target_audience: "intermediate"** の場合  
  ```
  全セクション: 30% beginner, 60% intermediate, 10% advanced
  ```

- **target_audience: "advanced"** の場合
  ```
  全セクション: 10% beginner, 30% intermediate, 60% advanced
  ```

### 3️⃣ クイズ数の自動計算

**自動判断ロジック：**

```
質問総数 = セクション数 × 21問（1セクションあたり）
           + 調整（ドキュメント数が特に多い場合）

例：
- セクション 3個 → 63問（21 × 3）
- セクション 6個 → 126問（21 × 6）
- セクション 10個 → 210問+α
```

### 4️⃣ 品質検証の自動実行

生成完了時に自動的に以下を検証：

- ✅ JSON スキーマ準拠性
- ✅ セクションごとの問題数
- ✅ 難度分布が設定値に準拠
- ✅ ID形式（ケバブケース）の正当性
- ✅ 必須フィールドの存在
- ✅ メタデータの整合性

**検証レポート：** `tutorial/{シリーズID}/VALIDATION_REPORT.md` に自動生成

---

## 段階的実行フロー

複数ステップに分けて実行することで、各段階でユーザーが検証・調整可能です。

### Step 1: コンテンツ分析

ドキュメント構造を解析し、シリーズ構成の候補を生成します。

**実行パラメータ：**
```yaml
action: "analyze"
doc_path: "docs"
```

**出力ファイル：** `tutorial/.analysis.json`

**確認項目：**
- ✅ シリーズID・名前が正確か
- ✅ セクション分類が適切か
- ✅ セクション名は分かりやすいか
- ✅ ドキュメント数が期待値と一致しているか

**確認後の選択肢：**
- ✅ 「次へ」→ Step 2 に進む
- 📝 「調整」→ `.analysis.json` を手動編集後 Step 2 に進む

---

### Step 2: シリーズ構成確定（オプション）

Step 1 の分析結果に対して、セクション順序や名前を手動で調整します。調整が不要な場合は、このステップをスキップして Step 3 に進めます。

**実行パラメータ：**
```yaml
action: "configure"
analysisFile: "tutorial/.analysis.json"
adjustments:
  seriesName: "修正後のシリーズ名"
  sections:
    - id: "fundamentals"
      name: "修正後のセクション名"
      order: 1
      enabled: true
    - id: "advanced"
      name: "上級トピック"
      order: 5
      enabled: false    # ← 特定セクションを除外する場合
```

**出力ファイル：** `tutorial/.series-config.json`

**編集可能な項目：**
- セクション順序の変更
- セクション名の修正
- セクションの有効/無効切り替え
- シリーズ名の変更

---

### Step 3: クイズセット生成

確定した構成に基づいて、各セクションのクイズを生成します。生成されたデータは [JSON スキーマ](./schemas/) に準拠します。

**実行パラメータ（段階的難度設定例）：**
```yaml
action: "generate"
configFile: "tutorial/.series-config.json"
target_audience: "progressive"      # ← beginnerから徐々にadvancedへ
difficulty_distribution: "balanced"
output_format: "json"
include_explanation: true
```

**出力ファイル：**
```
tutorial/github-copilot-skills-tutorial/
├── metadata.json              ← 親シリーズ + セクション一覧
├── fundamentals/quiz.json     ← Section 1（主にbeginner）
├── basics/quiz.json           ← Section 2（beginnerからintermediate）
├── comparison/quiz.json       ← Section 3（intermediateからadvanced）
├── implementation/quiz.json   ← Section 4（advancedが多い）
├── advanced/quiz.json         ← Section 5（mainly advanced）
├── .analysis.json             ← 分析結果（参照用）
└── README.md                  ← 生成レポート
```

**生成内容：**
- 21問/セクション（デフォルト）
- 段階的に難度が上昇
- 各問に日本語の解説付き
- すべて [JSON スキーマ](./schemas/) 準拠

---

### Step 4: 検証（オプション）

すべてのクイズセットが正しく生成されたか品質を検証します。**この段階は省略可能です。**

**実行パラメータ：**
```yaml
action: "validate"
outputDir: "tutorial"
```

**出力ファイル：** `tutorial/{シリーズID}/VALIDATION_REPORT.md`

**検証内容：**
- ✅ 生成されたクイズセット数
- ✅ 各セクションの問題数・難度分布
- ✅ メタデータの整合性
- ✅ JSON スキーマ準拠性
- ✅ ID形式（ケバブケース）
- ✅ 必須フィールドの存在

---

## 処理フロー図

### 対話型オートメーション（auto-flow）

```
┌─────────────────────────────────────────────────┐
│   action: "auto-flow"                           │
│   doc_path: "docs"                              │
│   target_audience: "progressive"                │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│ [内部Step 1] ドキュメント構造を自動解析          │
│ ・フォルダ検出                                   │
│ ・ドキュメント数カウント                         │
│ ・セクション順序決定（プレフィックス数字基準）   │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│ [内部Step 2] セクション自動最適化                │
│ ・min_docs_per_section 未満は自動除外           │
│ ・セクション名を自動生成（LLM利用）              │
│ ・ID をケバブケース化                            │
│ ★ ユーザー判断なし                              │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│ [内部Step 3] クイズセット生成                    │
│ ・難度分布を自動決定（progressive対応）         │
│ ・各セクションで問題を生成                       │
│ ・メタデータ統合                                 │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│ [内部Step 4] 生成品質を自動検証                  │
│ ・JSON スキーマ対応確認                          │
│ ・難度分布検証                                   │
│ ・メタデータ整合性チェック                       │
└─────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────┐
│ 出力ファイル生成                                │
│ tutorial/{シリーズID}/                          │
│ ├── metadata.json                               │
│ ├── {section}/quiz.json (複数)                  │
│ ├── VALIDATION_REPORT.md                        │
│ └── README.md                                   │
└─────────────────────────────────────────────────┘
```

**実行時間目安：** 3～5 秒（セクション数や質問数に依存）

---

### 従来の段階的実行フロー

```
ドキュメントを自動解析
        ↓
   [Step 1: analyze]
  フォルダ構造検出 → セクション自動分類 → ID・名前自動生成
        ↓
  [Step 2: configure] ← ユーザーが手動調整（オプション）
 セクション順序・名前を修正
        ↓
  [Step 3: generate]
各セクションからクイズを生成 → 難度を段階的に適用 → メタデータ統合
        ↓
tutorial/{シリーズID}/
├── metadata.json
├── {section}/quiz.json
└── README.md
        ↓
  [Step 4: validate] ← オプション（品質確認）
  JSON スキーマ検証 → 難度分布確認 → レポート生成
```

### ID 生成ルール

| ドキュメント | ID自動生成 | 例 |
|-----------|----------|-----|
| `01-introduction/` | `introduction` | フォルダプレフィックス数字削除 |
| `setup-guide/` | `setup-guide` | ケバブケースで使用 |
| `README.md` の H1 | `タイトルをハイフン化` | \"Clean Architecture\" → `clean-architecture` |
| `02-section/01-file.md` | `file` | ファイル名のプレフィックス削除 |

---

## 使用シナリオ

---

### 例0: 対話型オートメーション（推奨）

分析→自動判断→生成→検証を **完全自動実行**：

```yaml
action: "auto-flow"
doc_path: "docs"
target_audience: "progressive"
output_format: "json"
```

**特徴：**
- ✅ 4ステップを自動で実行（ユーザー判断不要）
- ✅ ドキュメント構造から最適なセクション構成を自動決定
- ✅ セクション最適化：ドキュメント数が少ないセクションを自動除外
- ✅ 難度分布を自動設定（progressive対応）
- ✅ 生成結果を自動検証＋レポート生成

**適用シーン：**
- 最も簡潔に実行したい
- セクション名や順序は自動判断に任せたい
- ドキュメント構造が変わっても自動対応したい

**実行時間：** 3～5秒

**出力例：**
```
tutorial/github-copilot-skills-tutorial/
├── metadata.json
├── fundamentals/quiz.json        (初級向け)
├── basics/quiz.json              (初→中級)
├── comparison/quiz.json          (中級)
├── implementation/quiz.json      (中→上級)
├── advanced/quiz.json            (上級向け)
├── VALIDATION_REPORT.md          ← 自動生成レポート
└── README.md
```

**オプション調整：**
```yaml
action: "auto-flow"
doc_path: "docs"
target_audience: "progressive"
output_format: "json"
auto_section_filter: true         # ← 少数ドキュメントで自動除外
min_docs_per_section: 1           # ← 最小ドキュメント数
generate_validation_report: true  # ← 検証レポート自動生成
verbose: false                    # ← 詳細ログは出力しない
```

---

### 例1: ワンコマンドで全セクションを生成

少ない手数で、すべてのセクションを段階的難度で生成：

```yaml
action: "generate"
doc_path: "docs"
target_audience: "progressive"
output_format: "json"
```

**適用シーン：**
- ドキュメント構造がシンプル
- セクション名・順序を変更不要
- 段階的学習が目的
- 検証レポートは不要

**出力例：**
```
tutorial/github-copilot-skills-tutorial/
├── metadata.json
├── fundamentals/quiz.json        (初級向け)
├── basics/quiz.json              (初→中級)
├── comparison/quiz.json          (中級)
├── implementation/quiz.json      (中→上級)
├── advanced/quiz.json            (上級向け)
└── README.md
```

---

### 例2: 段階的実行で調整

セクションのカスタマイズが必要な場合：

**Step 1: 分析**
```yaml
action: "analyze"
doc_path: "docs"
```

**Step 2: セクションを調整（上級トピックのみ除外）**
```yaml
action: "configure"
analysisFile: "tutorial/.analysis.json"
adjustments:
  sections:
    - id: "fundamentals"
      enabled: true
    - id: "advanced-topics"
      enabled: false    # ← 除外
```

**Step 3: 生成**
```yaml
action: "generate"
configFile: "tutorial/.series-config.json"
target_audience: "progressive"
```

---

### 例3: 初心者向け＋少ない問題数

```yaml
action: "generate"
doc_path: "docs"
target_audience: "beginner"
question_count: 30
difficulty_distribution: "beginner_focused"
```

**出力特性：**
- 問題数: 30問（全セクション合計）
- 難度: 50% beginner, 40% intermediate, 10% advanced

---

### 例4: 複数形式で出力（JSON + Markdown）

```yaml
action: "generate"
configFile: "tutorial/.series-config.json"
output_format: "both"
```

**出力ファイル：**
- `metadata.json`
- `{section}/quiz.json`
- `{section}/quiz.md` ← Markdown版も追加

---

## 出力ファイル構造と仕様

### メタデータファイル: metadata.json

**ファイルパス：** `tutorial/{シリーズID}/metadata.json`

**用途：** 親シリーズとセクション一覧の統合管理

> **スキーマ**: [quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json) に準拠

```json
{
  "series": {
    "id": "github-copilot-skills-tutorial",
    "name": "GitHub Copilot Skills チュートリアル",
    "level": 1,
    "parentId": null,
    "questionCount": 126,
    "childCount": 6
  },
  "quizSets": [
    {
      "id": "fundamentals",
      "name": "スキル形式の理解",
      "level": 2,
      "parentId": "github-copilot-skills-tutorial",
      "order": 1,
      "questionCount": 21,
      "difficulty": "beginner",
      "dataPath": "fundamentals/quiz.json"
    },
    {
      "id": "basics",
      "name": "基本概念",
      "level": 2,
      "parentId": "github-copilot-skills-tutorial",
      "order": 2,
      "questionCount": 21,
      "difficulty": "beginner to intermediate",
      "dataPath": "basics/quiz.json"
    }
  ]
}
```

---

### クイズファイル: {section}/quiz.json

**ファイルパス：** `tutorial/{シリーズID}/{section}/quiz.json`

**用途：** 各セクションの問題データ

> **スキーマ**: [question-set-schema.json](./schemas/question-set-schema.json) に準拠
> **個別問題**: [question-schema.json](./schemas/question-schema.json) に準拠

```json
{
  "metadata": {
    "generatedAt": "2026-03-08T10:00:00Z",
    "version": "2.0",
    "sourcePath": "docs/01-basics",
    "seriesId": "github-copilot-skills-tutorial",
    "seriesName": "GitHub Copilot Skills チュートリアル"
  },
  "questions": [
    {
      "id": 1,
      "question": "GitHub Copilot Skills とは、どのような仕組みですか？",
      "options": [
        {
          "id": "A",
          "text": "Copilot の動作を自動化するスクリプト"
        },
        {
          "id": "B",
          "text": "特定のドメイン知識をプロンプト+ドキュメントで定義するもの"
        },
        {
          "id": "C",
          "text": "Copilot の新機能追加パッチ"
        },
        {
          "id": "D",
          "text": "ユーザーの VS Code 拡張機能"
        }
      ],
      "correctAnswer": "B",
      "explanation": "Skills は、プロンプトやドキュメントを組み合わせて、特定分野の知識をCopilot に教えるものです..."
    },
    {
      "id": 2,
      "question": "問題文...",
      "options": [
        {"id": "A", "text": "..."},
        {"id": "B", "text": "..."},
        {"id": "C", "text": "..."},
        {"id": "D", "text": "..."}
      ],
      "correctAnswer": "A",
      "explanation": "..."
    }
  ]
}
```

**フィールド説明**:
- `metadata.seriesId` - 所属するシリーズのID
- `metadata.seriesName` - 所属するシリーズの名前
- `metadata.sourcePath` - 生成元のドキュメントパス
- `questions[].id` - セクション内での問題番号（連番）
- `questions[].correctAnswer` - 正解（A/B/C/D のいずれか）

詳細は [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) を参照してください。

---

### 検証レポート: VALIDATION_REPORT.md

**ファイルパス：** `tutorial/{シリーズID}/VALIDATION_REPORT.md`

**用途：** Step 4 で生成される品質チェックレポート

```markdown
# Quiz Set Validation Report

## Summary
- Total Quiz Sets: 6
- Total Questions: 126
- Generation Date: 2026-03-08T10:00:00Z
- Target Audience: progressive
- Difficulty Distribution: balanced

## Per-Section Details
- fundamentals: 21 questions
  - Difficulty: beginner (100%)
  - Schema: ✅ Valid
  
- basics: 21 questions
  - Difficulty: beginner (50%), intermediate (50%)
  - Schema: ✅ Valid

- ... (other sections)

## Quality Checks
- ✅ All metadata is valid (quizset-metadata-schema.json)
- ✅ All question sets are valid (question-set-schema.json)
- ✅ All individual questions are valid (question-schema.json)
- ✅ ID format: kebab-case compliant
- ✅ Required fields present in all objects
- ✅ Parent-child relationships valid
```

---

## メタデータ一元管理の設計

> **根拠**: [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) で定義されるメタデータ一元管理設計

**構造の利点：**

1. **関心の分離** - メタデータ（表示・管理用）と問題データ（実行用）を分離
   - UI は `metadata.json` から全情報を取得
   - 学習アプリは各 `quiz.json` から問題データを取得

2. **保守性** - メタデータ修正時にクイズJSONを編集不要
   - セクション名の変更 → `metadata.json` のみ更新
   - 問題データは変更なし

3. **拡張性** - 新しいクイズセット追加時は`metadata.json`に追記するだけ
   - 新セクション追加 → `metadata.json` の `quizSets` に 1 行追加
   - `{section}/quiz.json` を作成

4. **UI連携** - SPAフロントエンドは`metadata.json`から一括に情報を取得
   - ナビゲーション構築
   - セクション進捗管理
   - 統計情報の表示

---

## データ品質基準

### 出題品質

- ✅ **コンテンツ正確性** - ドキュメント内容を正確に反映
- ✅ **実用性** - ドキュメント内の具体例・図表を参照した問題
- ✅ **理解度測定** - 実践的で理解度を確認できる問題設計
- ✅ **思考性** - 誤答選択肢が紛らわしく、思考を深める設計

### データ完全性

- ✅ **ID形式** - ケバブケース準拠 ([quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json))
- ✅ **選択肢数** - 正確に 4 つ（A/B/C/D）が必須 ([question-schema.json](./schemas/question-schema.json))
- ✅ **難度値** - 有効な難度のみ（`beginner`, `intermediate`, `advanced`）
- ✅ **階層構造** - level は 1（トップレベル）または 2（子セット）
- ✅ **参照整合性** - 親セット・子セット関係が正しく定義される

### 難度分布パターン

| パターン | Beginner | Intermediate | Advanced |
|---------|----------|--------------|----------|
| `balanced` | 15% | 70% | 15% |
| `beginner_focused` | 50% | 40% | 10% |
| `advanced_focused` | 10% | 40% | 50% |

---

### JSON スキーマ検証

すべての生成ファイルは、以下のスキーマに対して自動検証されます：

| ファイル | スキーマ | 検証内容 |
|---------|---------|----------|
| `metadata.json` | [quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json) | ID形式、難度値、順序番号、parent-child関係 |
| `{section}/quiz.json` | [question-set-schema.json](./schemas/question-set-schema.json) | 問題配列の構造、メタデータ |
| 個別問題 | [question-schema.json](./schemas/question-schema.json) | 選択肢数（4つ必須）、ID形式、正答の妥当性 |

詳細は [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) を参照してください。

---

## トラブルシューティング

### Q: ドキュメント構造が複雑で、セクション分類が正確でない

**A:** Step 1（analyze）の結果を確認し、Step 2（configure）で手動調整してください

```yaml
action: "configure"
analysisFile: "tutorial/.analysis.json"
adjustments:
  sections:
    # フォルダ順を変更
    - id: "advanced-topics"
      order: 3
    - id: "basics"
      order: 4
```

---

### Q: 特定セクションのみ生成したい

**A:** Step 2 で `enabled: false` に設定してください

```yaml
action: "configure"
analysisFile: "tutorial/.analysis.json"
adjustments:
  sections:
    - id: "fundamentals"
      enabled: true
    - id: "advanced"
      enabled: false    # ← このセクションをスキップ
```

---

### Q: 生成された問題の品質が低い、または内容が不正確

**A:** 以下を確認してください：

1. **ドキュメント品質**：タイトル、見出しが明確か
2. **形式**：H1/H2 の階層構造が適切か
3. **内容**：具体例や説明が十分か

改善後、再度実行してください。

---

### Q: 難度分布が期待と異なる

**A:** `difficulty_distribution` パラメータを調整してください

```yaml
action: "generate"
configFile: "tutorial/.series-config.json"
target_audience: "progressive"
difficulty_distribution: "beginner_focused"  # ← 初級向けに変更
```

---

## 参考資料

| 資料 | 内容 |
|----|----|
| [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) | クイズデータの詳細仕様、ネーミング規則、FAQ など |
| [question-schema.json](./schemas/question-schema.json) | 個別問題の JSON Schema (Draft-07) |
| [question-set-schema.json](./schemas/question-set-schema.json) | クイズセット全体の JSON Schema |
| [quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json) | メタデータの JSON Schema |

---

## 活用パターン

### 親シリーズの活用
- 学習ロードマップ表示
- 全体的な理解度測定
- シリーズ進捗管理

### 子クイズセットの活用
- セクション単位での理解確認
- 段階的な難度上昇対応
- セクション別の弱点分析

### メタデータの活用
- UI から全セクション一覧を表示
- ドキュメント品質測定
- 学習カバレッジ検証
- ドキュメント更新による影響度追跡