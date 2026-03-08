---
name: quiz-generator
description: 任意のMarkdownドキュメントをクイズセット化しJSON形式で出力。複数プロジェクト・複数形式に対応した汎用クイズ生成スキル
license: MIT
---

# Quiz Generator（汎用化版）

## 概要

**任意のMarkdownドキュメント**を対話的なクイズセットに自動変換するスキルです。

> **参考資料**
> - 📋 [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) - 出力データの詳細仕様
> - ✅ [JSON スキーマ定義](./schemas/) - 自動バリデーション用のスキーマ（question-schema.json, question-set-schema.json, quizset-metadata-schema.json）

| 特徴 | 説明 |
|------|------|
| ✅ **自動生成** | ドキュメント構造を解析し、シリーズとクイズセットを自動生成 |
| ✅ **単一管理** | すべてのクイズを `tutorial-quiz-set/` に一元管理 |
| ✅ **段階的学習** | beginner → intermediate → advanced で難度を段階化 |
| ✅ **複数形式** | JSON, Markdown での出力に対応 |
| ✅ **拡張性** | 新規セクション追加時も自動的に対応 |

---

## 実行フロー（マルチステップ）

複数ステップに分けて実行することで、各段階でユーザーが検証・調整可能です。詳細な出力ファイル形式は「[出力仕様](#出力仕様)」を参照してください。

### Step 1: コンテンツ分析

ドキュメント構造を解析し、シリーズ構成の候補を生成します。

**パラメータ:**
```
action: "analyze"
doc_path: "docs"
```

**出力:** `tutorial-quiz-set/.analysis.json`

**ユーザーが確認・調整する項目：**
- ✅ シリーズID・名前が正確か
- ✅ セクション分類が適切か
- ✅ セクション名は分かりやすいか

---

### Step 2: シリーズ構成確定

Step 1 の分析結果をユーザーが調整後、シリーズ構成を確定します。

**パラメータ:**
```
action: "configure"
analysisFile: "tutorial-quiz-set/.analysis.json"
adjustments: {
  "seriesName": "修正後のシリーズ名",
  "sections": [
    {
      "id": "fundamentals",
      "name": "修正後のセクション名",
      "order": 1,
      "enabled": true
    }
  ]
}
```

**出力:** `tutorial-quiz-set/.series-config.json`

**ユーザーが編集可能：**
- セクション順序の変更
- セクション名の修正
- セクションの有効/無効切り替え

---

### Step 3: クイズセット生成

Step 2 の確定構成に基づいて、各セクションのクイズを生成します。生成されたデータは [JSON スキーマ](./schemas/) に準拠します。

**パラメータ:**
```
action: "generate"
configFile: "tutorial-quiz-set/.series-config.json"
target_audience: "intermediate"
question_count: 84
difficulty_distribution: "balanced"
output_format: "json"
```

**出力:**
```
tutorial-quiz-set/
├── metadata.json           ← 親シリーズ＋セクション情報
├── .analysis.json          ← 分析結果（参照用）
├── .series-config.json     ← シリーズ構成（参照用）
├── fundamentals/quiz.json  ← セクション1のクイズ
├── basics/quiz.json        ← セクション2のクイズ
└── README.md               ← 生成レポート
```

---

### Step 4: 検証（オプション）

すべてのクイズセットが正しく生成されたか確認します。

**パラメータ:**
```
action: "validate"
outputDir: "tutorial-quiz-set"
```

**出力:** `tutorial-quiz-set/VALIDATION_REPORT.md`
- 生成されたクイズセット数
- 各セクションの問題数・難度分布
- メタデータの整合性チェック

---

## しくみ

### 処理フロー

```
ドキュメントフォルダ (doc_path)
        ↓
   [自動解析]
  フォルダ構造を検出 → セクション分類 → ID・名前を自動生成
        ↓
  [クイズ生成]
  各セクト毎に問題作成 → 難度分布を適用 → メタデータ統合
        ↓
tutorial-quiz-set/
├── metadata.json
├── {section}/quiz.json
└── README.md
```

### ID 生成ルール

| ドキュメント | ID自動生成 | 例 |
|-----------|----------|-----|
| `01-introduction/` | `introduction` | フォルダプレフィックス数字削除 |
| `setup-guide/` | `setup-guide` | そのまま使用 |
| `README.md` の H1 | `タイトルをハイフン化` | \"Clean Architecture\" → `clean-architecture` |
| `02-section/01-file.md` | `file` | ファイル名のプレフィックス削除 |

---

## パラメータ

### 必須

| パラメータ | 説明 | 値 |
|---------|------|-----|
| `action` | 実行ステップ | `analyze` / `configure` / `generate` / `validate` |
| `doc_path` | ドキュメントフォルダ（analyze時） | `docs`, `tutorials` 等 |
| `configFile` | シリーズ構成ファイル（configure/generate時） | `.series-config.json` |

### オプション（generate時）

| パラメータ | デフォルト | 説明 |
|---------|----------|------|
| `series_title` | 自動生成 | シリーズの表示名（手動設定時） |
| `target_audience` | `intermediate` | 対象難度 |
| `question_count` | 自動 | 全体の問題数 |
| `difficulty_distribution` | `balanced` | 難度配分 |
| `include_explanation` | `true` | 各問の解説を含める |
| `output_format` | `json` | 出力形式: `json` / `markdown` / `both` |
| `max_depth` | `2` | ドキュメント階層の深さ |
| `quiz_per_section` | `auto` | セクション単位の問題数 |

---

## クイズデータ構造

クイズセットは以下の設計に従い、[データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) で詳細に定義されています：

### メタデータ一元管理アーキテクチャ

**根拠**: [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) が定義するメタデータ一元管理設計

**構造の利点：**
1. **関心の分離**: メタデータ（表示・管理用）と問題データ（実行用）を分離
2. **保守性**: メタデータ修正時にクイズ JSON を編集不要
3. **拡張性**: 新しいクイズセット追加時は metadata.json に追記するだけ
4. **UI連携**: SPA フロントエンドは metadata.json から一括に情報を取得して表示

詳細は「[出力ファイル構成](#出力ファイル構成)」を参照してください。

---

## 使用例

### ⚡ 最も簡単な自動生成（ワンコマンド）

最小限のパラメータだけで、分析→生成→検証まで自動実行：

**ユーザー入力：**
```
action: "generate"
doc_path: "docs"
```

**結果：** 以下が自動生成されます
```
tutorial-quiz-set/
├── metadata.json          ← 親シリーズ情報
├── fundamentals/quiz.json ← 自動クイズ生成（21問）
├── basics/quiz.json        ← 自動クイズ生成（21問）
├── comparison/quiz.json    ← 自動クイズ生成（21問）
├── implementation/quiz.json ← 自動クイズ生成（21問）
└── README.md              ← 生成レポート
```

**出力例 (metadata.json):**
```json
{
  "series": {
    "id": "github-copilot-skills-tutorial",
    "name": "GitHub Copilot Skills チュートリアル",
    "questionCount": 84,
    "childCount": 4
  },
  "quizSets": [
    {
      "id": "fundamentals",
      "name": "スキル形式の理解",
      "order": 1,
      "questionCount": 21,
      "dataPath": "fundamentals/quiz.json"
    },
    {
      "id": "basics",
      "name": "基本概念",
      "order": 2,
      "questionCount": 21,
      "dataPath": "basics/quiz.json"
    }
  ]
}
```

---

### 基本的なワークフロー

#### 1️⃣ Step 1: コンテンツ分析

```
action: "analyze"
doc_path: "docs"
```

**確認項目：** シリーズ名、セクション分類が正確か

---

#### 2️⃣ Step 2: シリーズ構成を調整（必要に応じて）

生成された `.analysis.json` を確認し、必要に応じて手動で編集：

```json
{
  "series": {
    "id": "github-copilot-skills-tutorial",
    "name": "修正可能なシリーズ名"
  },
  "quizSets": [
    {
      "id": "fundamentals",
      "name": "修正可能なセクション名",
      "order": 1,
      "enabled": true
    }
  ]
}
```

---

#### 3️⃣ Step 3: クイズセット生成

確定した構成でクイズを生成：

```
action: "generate"
configFile: "tutorial-quiz-set/.series-config.json"
target_audience: "intermediate"
```

**結果：** `metadata.json` + 各 `{section}/quiz.json` 生成

---

#### 4️⃣ Step 4: 検証（オプション）

```
action: "validate"
outputDir: "tutorial-quiz-set"
```

**出力：** 品質チェックレポート

---

### シナリオ例

#### シナリオ1: 初級者向け＆セクション調整

```
# Step 1: 分析
action: "analyze"
doc_path: "python-tutorial"

# Step 2: 構成確定（上級セクションを除外）
action: "configure"
analysisFile: ".analysis.json"
adjustments: {
  "sections": [
    {"id": "basics", "order": 1, "enabled": true},
    {"id": "advanced", "order": 2, "enabled": false}
  ]
}

# Step 3: 初級者向けで生成
action: "generate"
configFile: ".series-config.json"
target_audience: "beginner"
question_count: 30
```

#### シナリオ2: 複数形式同時出力

```
action: "generate"
configFile: ".series-config.json"
output_format: "both"
```

**出力** - JSON + Markdown 同時生成

---

## 出力仕様

> **重要**: 出力ファイルは [JSON スキーマ](./schemas/) に準拠して自動生成されます。
> - 📄 [quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json) - メタデータ検証
> - 📄 [question-set-schema.json](./schemas/question-set-schema.json) - クイズセット検証
> - 📄 [question-schema.json](./schemas/question-schema.json) - 個別問題検証

### ステップ別の生成ファイル

### Step 1 (analyze): 分析結果

**ファイル：** `tutorial-quiz-set/.analysis.json`

ドキュメント構造の分析結果

```json
{
  "analysis": {
    "documentPath": "docs",
    "folderCount": 4,
    "fileCount": 12
  },
  "seriesCandidates": {
    "id": "series-id",
    "name": "Series Name"
  },
  "sectionCandidates": [
    {
      "id": "section-id",
      "name": "Section Name",
      "folderPath": "docs/01-section",
      "estimatedQuestions": 10
    }
  ]
}
```

---

### Step 2 (configure): 構成確定

**ファイル：** `tutorial-quiz-set/.series-config.json`

ユーザーが編集・調整可能な構成ファイル

```json
{
  "series": {
    "id": "series-id",
    "name": "修正可能なシリーズ名"
  },
  "quizSets": [
    {
      "id": "section-id",
      "name": "修正可能なセクション名",
      "order": 1,
      "documentPath": "docs/01-section",
      "enabled": true
    }
  ]
}
```

---

### Step 3 (generate): クイズセット生成

**メインファイル：** `tutorial-quiz-set/metadata.json` (親シリーズ + セクション情報)

> **スキーマ**: [quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json) に準拠

```json
{
  "series": {
    "id": "series-id",
    "name": "GitHub Copilot Skills チュートリアル",
    "level": 1,
    "parentId": null,
    "questionCount": 84,
    "childCount": 4
  },
  "quizSets": [
    {
      "id": "fundamentals",
      "name": "スキル形式の理解",
      "level": 2,
      "parentId": "series-id",
      "order": 1,
      "questionCount": 21,
      "dataPath": "fundamentals/quiz.json"
    }
  ]
}
```

**クイズファイル：** `tutorial-quiz-set/{section}/quiz.json` (各セクションの問題)

> **スキーマ**: [question-set-schema.json](./schemas/question-set-schema.json) に準拠（個別問題は [question-schema.json](./schemas/question-schema.json)）

```json
{
  "metadata": {
    "generatedAt": "2026-03-08T10:00:00Z",
    "version": "2.0",
    "sourcePath": "docs/01-basics",
    "seriesId": "series-id",
    "seriesName": "シリーズ名"
  },
  "questions": [
    {
      "id": 1,
      "question": "質問文",
      "options": [
        {"id": "A", "text": "選択肢A"},
        {"id": "B", "text": "選択肢B"},
        {"id": "C", "text": "選択肢C"},
        {"id": "D", "text": "選択肢D"}
      ],
      "correctAnswer": "A",
      "explanation": "解説文"
    }
  ]
}
```

**フィールド詳細**: [データフォーマット仕様書 § 2. 質問データ形式](./DATA_FORMAT_SPECIFICATION.md#2-質問データ形式)

---

### Step 4 (validate): 品質検証

生成ファイルが [JSON スキーマ](./schemas/) に準拠しているか自動検証します。

**ファイル：** `tutorial-quiz-set/VALIDATION_REPORT.md`

```
# Quiz Set Validation Report

## Summary
- Total Quiz Sets: 4
- Total Questions: 84
- Generation Date: 2026-03-08T10:00:00Z

## Details
- fundamentals: 21 questions (beginner)
- basics: 35 questions (intermediate)
- advanced: 10 questions (advanced)

## Quality Checks
- ✅ All metadata is valid
- ✅ Question count matches expected
- ✅ Difficulty distribution OK
```

**フィールド説明**:
- `metadata.seriesId` - 所属するシリーズのID
- `metadata.seriesName` - 所属するシリーズの名前
- `metadata.sourcePath` - 生成元のドキュメントパス

---

## 対話的実行ガイド

> **データ品質保証**: すべての生成ファイルは [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) と [JSON スキーマ](./schemas/) に準拠します。

このガイドは、ユーザーが各ステップで確認すべき項目と、調整方法を説明します。

### 各ステップでの確認項目

#### Step 1 後の確認

```
【分析結果】
- シリーズ名: GitHub Copilot Skills チュートリアル
- セクション数: 4
  └─ スキル形式の理解 (fundamentals)
  └─ Agent Skills 基礎 (basics)
  └─ ...

確認事項:
✅ シリーズID・名前は正確か
✅ セクション分類は適切か
✅ セクション名は分かりやすいか

→ ユーザー応答:
  「次へ」: Step 2 に進む
  「調整」: 以下の例を参照して調整後 Step 2 に進む
```

#### Step 2 後の確認

```
【確定した構成】
- シリーズ: GitHub Copilot Skills チュートリアル
- クイズセット数: 4
- 予想問題数: 84
- 予想生成時間: 約 30秒

→ ユーザー応答:
  「次へ」: Step 3 (生成) に進む
  「キャンセル」: 処理中止
```

#### Step 3 後の確認

```
【生成結果】
✅ metadata.json: 生成完了
✅ fundamentals/quiz.json: 21 問題
✅ basics/quiz.json: 35 問題
✅ ...

出力先: tutorial-quiz-set/

→ ユーザー応答:
  「次へ」: Step 4 (検証) に進む
  「キャンセル」: ここで終了
```

#### Step 4 後の確認

```
【検証レポート】
✅ すべてのメタデータが有効
✅ 問題数: 84 (期待値: 84)
✅ 難度分布: beginner 15%, intermediate 70%, advanced 15%
✅ 各セクションで必須フィールドが揃っている

→ ユーザー応答:
  「完了」: 処理終了
  「詳細を表示」: VALIDATION_REPORT.md を展開表示
```

### ユーザー調整の例

#### 例 1: シリーズ名の変更

```
Step 1 結果表示後、ユーザーが:
「シリーズ名を『Copilot スキルマスターコース』に変更」

→ 調整を反映して Step 2 に進む
```

#### 例 2: 特定セクションの除外

```
Step 1 結果表示後、ユーザーが:
「basics セクションは除外」

→ .series-config.json で該当セクションの enabled を false に設定して Step 2 に進む
```

#### 例 3: 途中で中止

```
Step 2 または Step 3 の確認で、ユーザーが:
「キャンセル」

→ 処理を中止して、ここまでの出力ファイル（あれば）を保持
```

**詳細フィールド説明**: [データフォーマット仕様書 § 1. メタデータ形式](./DATA_FORMAT_SPECIFICATION.md#1-メタデータ形式)

---

## 詳細仕様

### JSON スキーマに準拠したデータ生成

SKILL.md で説明するすべてのクイズセットは、[schemas](./schemas/) に定義された JSON Schema (Draft-07) に厳密に準拠します。以下のドキュメントを参照してください：

| ドキュメント | 用途 | 参照 |
|-----------|------|-----|
| **データフォーマット仕様書** | クイズデータの詳細要件・ネーミング規則 | [DATA_FORMAT_SPECIFICATION.md](./DATA_FORMAT_SPECIFICATION.md) |
| **question-schema.json** | 個別問題の検証スキーマ | [schemas/question-schema.json](./schemas/question-schema.json) |
| **question-set-schema.json** | クイズセット全体の検証スキーマ | [schemas/question-set-schema.json](./schemas/question-set-schema.json) |
| **quizset-metadata-schema.json** | メタデータ（クイズセット情報）の検証スキーマ | [schemas/quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json) |

### よくある質問への回答

詳細は [データフォーマット仕様書 § 5. よくある質問 (FAQ)](./DATA_FORMAT_SPECIFICATION.md#5-よくある質問-faq) を参照してください：

- **Q1**: 問題と選択肢の数が異なる場合は？
- **Q2**: 複数の正解がある場合は？
- **Q3**: 難易度レベルはどうやって決めればよい？
- **Q4**: 階層的なクイズセット（parentId を使う）の例は？

---

## 品質基準

> **データ検証**: すべての出力は [JSON スキーマ](./schemas/) により自動検証され、[データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) に準拠することが保証されます。

### 出題設計
- ✅ ドキュメント内容を正確に反映
- ✅ ドキュメント内の具体例・図表を参照
- ✅ 実践的で理解度を確認できる問題
- ✅ 誤答選択肢が紛らわしく、思考を深める

### 解説クオリティ
- ✅ 正答・誤答の理由を明示
- ✅ 関連トピックへのリンク情報
- ✅ 日本語の自然性を保証

### データ完全性
- ✅ **ID 形式**: ケバブケース準拠 ([quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json))
- ✅ **選択肢数**: A/B/C/D の 4 つが必須 ([question-schema.json](./schemas/question-schema.json))
- ✅ **難度値**: 有効な難度のみ (`beginner`, `intermediate`, `advanced`)
- ✅ **レベル**: 1（トップレベル）または 2（子セット）
- ✅ **メタデータ整合性**: 親セット・子セット関係が正しく定義されている

### 難度分布

| 配分タイプ | Beginner | Intermediate | Advanced |
|----------|----------|--------------|----------|
| balanced | 15% | 70% | 15% |
| beginner_focused | 50% | 40% | 10% |
| advanced_focused | 10% | 40% | 50% |

---

## スキーマ検証ガイド

### 自動検証の仕組み

生成されたすべての JSON ファイルは、以下のスキーマに対して自動検証されます。詳細は [データフォーマット仕様書](./DATA_FORMAT_SPECIFICATION.md) 内の各スキーマリファレンスを参照してください：

| ファイル | スキーマ | 検証内容 | 参照 |
|---------|---------|----------|------|
| `metadata.json` | [quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json) | ID形式、難度値、順序番号など | [メタデータ仕様](./DATA_FORMAT_SPECIFICATION.md#1-メタデータ形式) |
| `{section}/quiz.json` | [question-set-schema.json](./schemas/question-set-schema.json) | 問題配列の構造と内容 | [質問セット仕様](./DATA_FORMAT_SPECIFICATION.md#2-質問データ形式) |
| 個別問題 | [question-schema.json](./schemas/question-schema.json) | 選択肢数（4つ必須）、ID形式など | [個別問題仕様](./DATA_FORMAT_SPECIFICATION.md#option-オブジェクトの仕様)

### スキーマの主要検証ルール

#### [quizset-metadata-schema.json](./schemas/quizset-metadata-schema.json) - メタデータ検証
- **ID**: ケバブケース (`^[a-z0-9-]+$`) - 例: `github-copilot-skills`
- **difficulty**: 有効値のみ受け入れ (`beginner`, `intermediate`, `advanced`, `beginner to intermediate`, `beginner to advanced`)
- **level**: 1 (トップ) または 2 (子セット)
- **questionCount**: 正の整数 (最小: 1)
- **dataPath**: 相対パス形式またはnull（親セットの場合）

#### [question-set-schema.json](./schemas/question-set-schema.json) - クイズセット検証
- **questions**: 配列必須、最小 1 要素
- 各要素は [question-schema.json](./schemas/question-schema.json) に準拠

#### [question-schema.json](./schemas/question-schema.json) - 個別問題検証
- **id**: 正の整数（クイズセット内で連番）
- **question**: 空でない文字列
- **options**: 正確に 4 つの選択肢（A, B, C, D）
- **correctAnswer**: A/B/C/D のいずれか
- **explanation**: 空でない文字列

### バリデーションレポート

Step 4 の検証では以下も確認されます：
- ✅ スキーマ準拠性（JSON Schema Draft-07）- [スキーマファイル参照](./schemas/)
- ✅ 必須フィールドの存在
- ✅ データ型の正確性
- ✅ ID の一意性
- ✅ メタデータの整合性 - [詳細は仕様書参照](./DATA_FORMAT_SPECIFICATION.md#3-ファイル配置)

---

## 活用パターン

### 親シリーズ
- 学習ロードマップ表示
- 全体的な理解度測定
- シリーズ進捗管理

### 子クイズセット
- セクション単位での理解確認
- 段階的な難度上昇
- セクション別の弱点分析

### メタデータの活用
- ドキュメント品質測定
- 学習カバレッジ検証
- ドキュメント更新による影響度追跡