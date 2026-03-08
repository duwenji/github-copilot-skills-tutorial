---
name: quiz-generator
description: 任意のMarkdownドキュメントをクイズセット化しJSON形式で出力。複数プロジェクト・複数形式に対応した汎用クイズ生成スキル
license: MIT
---

# Quiz Generator（汎用化版）

## 概要

このスキルは、**任意のMarkdownドキュメント**を対話的なクイズセットに自動変換します。

プロジェクトの種類（技術チュートリアル、学習ガイド、ナレッジベース等）を問わず、以下の機能を提供：

- ✅ **Workspace非依存** - 特定のプロジェクト構造に依存しない完全な汎用化
- ✅ **シリーズ自動生成** - ドキュメント構造から自動的にシリーズ名を生成
- ✅ **クイズセット自動洗い出し** - ドキュメント階層を解析し、クイズセットを自動分類
- ✅ **単一シリーズモデル** - 生成されたすべてのクイズセットが1つのシリーズに統一
- ✅ **難度別問題設計** - beginner/intermediate/advanced で段階的学習に対応
- ✅ **複数形式出力** - JSON, Markdown でのエクスポート対応

学習者は生成されたクイズで理解度を確認し、解説から詳細を学ぶことができます。

## シリーズ構成と自動生成ロジック

### 自動シリーズ生成のプロセス

スキルは、ドキュメント構造を解析して自動的にシリーズを生成します：

```
入力: ドキュメントフォルダ
  ├── 01-introduction/ → Series ID: introduction, Name: "イントロダクション"
  ├── 02-core-concepts/ → Series ID: core-concepts, Name: "コア概念"
  ├── 03-advanced/ → Series ID: advanced, Name: "応用編"
  └── README.md
       ↓
       スキルが自動解析
       ↓
出力: 1つの親シリーズ + 複数の子クイズセット
```

### ドキュメント構造から自動生成されるシリーズ名

| ドキュメント構造 | 自動生成シリーズID | シリーズ名生成ルール |
|--------------|-------------------|-----------------|
| `docs/01-introduction/` | `introduction` | フォルダプレフィックス番号を削除 |
| `docs/setup-guide/` | `setup-guide` | フォルダ名をそのまま使用 |
| `README.md` の H1 | その値 | タイトルから複数単語をハイフン区切りに |
| `02-core-principles/01-solid.md` | `solid` | ファイル名のプレフィックス番号を削除 |

### 例解：GitHub Copilot Skills チュートリアルの場合

ドキュメント構造：
```
docs/
├── 00-fundamentals/01-overview.md
├── 01-basics/01-definition.md, 02-features.md
├── 02-comparison/01-vs-prompt.md, 02-vs-plugin.md
└── 03-implementation/01-pattern.md, 02-example.md
```

自動生成結果：
```json
{
  "seriesId": "github-copilot-skills-tutorial",
  "seriesName": "GitHub Copilot Skills チュートリアル",
  "parentQuizSet": {
    "id": "github-copilot-skills-tutorial",
    "level": 1
  },
  "childQuizSets": [
    {
      "id": "fundamentals",
      "name": "スキル形式の理解",
      "seriesId": "github-copilot-skills-tutorial",
      "level": 2,
      "order": 1,
      "documentPath": "docs/00-fundamentals"
    },
    {
      "id": "basics",
      "name": "Agent Skills 基礎",
      "seriesId": "github-copilot-skills-tutorial",
      "level": 2,
      "order": 2,
      "documentPath": "docs/01-basics"
    },
    ...
  ]
}
```

---

## 入力パラメータ

### 必須

| パラメータ | 型 | 説明 |
|---------|-----|------|
| `doc_path` | string | クイズ生成対象のドキュメントフォルダパス（相対パス例：`docs/`, `tutorials/`) |

### オプション

| パラメータ | 型 | デフォルト | 説明 | 例 |
|---------|-----|----------|------|-----|
| `series_title` | string | フォルダ名から自動生成 | シリーズの表示名 | `GitHub Copilot Skills チュートリアル` |
| `output_dir` | string | `tutorial-quiz-set` | 出力先ディレクトリ | `tutorial-quiz-set`, `learning-materials/` |
| `target_audience` | string | `intermediate` | 対象レベル | `beginner`, `intermediate`, `advanced` |
| `question_count` | number | `自動` | 全クイズセットの合計問題数 | `50`, `100`, `150` |
| `include_explanation` | boolean | `true` | 解説を含める | `true`, `false` |
| `difficulty_distribution` | string | `balanced` | 難度配分 | `balanced` (15:70:15), `beginner_focused` (50:40:10), `advanced_focused` (10:40:50) |
| `output_format` | string | `json` | 出力形式 | `json`, `markdown`, `both` |
| `max_depth` | number | `2` | ドキュメント階層の深さ | `1`, `2`, `3` |
| `quiz_per_section` | number | `auto` | 各セクションあたりの問題数 | `5`, `10`, `15` |

### パラメータの詳細説明

#### series_title の自動生成ルール

1. **フォルダ名から** - `docs/` → "Documentation"
2. **README.md の H1 から** - 最初の H1 タイトルを使用
3. **フォルダの数字プレフィックスを削除** - `02-core-concepts/` → "Core Concepts"
4. **複数単語の場合は タイトルケース化** - `github-copilot-skills` → "GitHub Copilot Skills"

#### output_dir の決定ロジック

- デフォルト: `{doc_path}/quizzes/` に自動出力
- カスタム指定時: `/output_dir/{series_id}/` に出力
- Workspace依存性なし: 相対パスで対応

---

## クイズデータ構造

クイズセットは以下の設計に従います：

### ✅ メタデータ一元管理アーキテクチャ

```
spa-quiz-app/
├── metadata.json                    ← 全クイズセットのメタデータを一元管理
├── basics/
│   └── agent-skills-basics.json     ← questions のみ
├── comparison/
│   └── comparison-comprehensive.json ← questions のみ
└── ...
```

**構造の利点：**
1. **関心の分離**: メタデータ（表示・管理用）と問題データ（実行用）を分離
2. **保守性**: メタデータ修正時にクイズ JSON を編集不要
3. **拡張性**: 新しいクイズセット追加時は metadata.json に追記するだけ
4. **UI連携**: SPA フロントエンドは metadata.json から一括に情報を取得して表示

詳細は「[出力ファイル構成](#出力ファイル構成)」を参照してください。

---

## 使用例

### 例1：自動シリーズ生成（最もシンプル）

```
ユーザー入力:
"docs フォルダからクイズセットを生成してください。
シリーズは自動生成、intermediate レベルでお願いします"

パラメータ:
doc_path: "docs"
target_audience: intermediate
```

**処理フロー**:
1. `docs/` フォルダ構造を自動解析
2. サブフォルダ（01-xxx/, 02-yyy/）を検出
3. シリーズID・名前を自動生成
4. 各セクション単位でクイズセットを生成
5. 親セット（シリーズ全体）を自動作成

**出力例**:
```
tutorial-quiz-set/
├── metadata.json （親シリーズ情報）
├── fundamentals/quiz.json （子クイズセット1）
├── basics/quiz.json （子クイズセット2）
├── advanced/quiz.json （子クイズセット3）
└── README.md
```

### 例2：カスタムシリーズタイトル + 出力先指定

```
ユーザー入力:
"clean-architecture フォルダからクイズを生成。
シリーズ名を『クリーンアーキテクチャ完全ガイド』にして、
learning-materials フォルダに出力してください"

パラメータ:
doc_path: "clean-architecture"
series_title: "クリーンアーキテクチャ完全ガイド"
target_audience: intermediate
```

**出力**:
```
tutorial-quiz-set/
├── metadata.json （親: クリーンアーキテクチャ完全ガイド）
├── core-principles/quiz.json
├── architecture-layers/quiz.json
├── design-patterns/quiz.json
└── implementation/quiz.json
```

### 例3：初級者向け、問題数指定

```
ユーザー入力:
"パイソン入門 (python-tutorial) からクイズを生成。
初級者向けで、合計30問でお願いします"

パラメータ:
doc_path: "python-tutorial"
target_audience: beginner
question_count: 30
difficulty_distribution: beginner_focused
```

**特徴**:
- ドキュメント全体から自動生成
- 総問題数: 30問（各セクション按分配置）
- 難度: 50% beginner, 40% intermediate, 10% advanced

### 例4：複数形式での出力

```
ユーザー入力:
"tutorials フォルダからクイズを生成。
JSON と Markdown の両形式でお願いします"

パラメータ:
doc_path: "tutorials"
output_format: "both"
```

**出力**:
```
tutorial-quiz-set/
├── metadata.json
├── module-1/
│   ├── quiz.json
│   └── quiz.md
├── module-2/
│   ├── quiz.json
│   └── quiz.md
└── ...
```

---

## 出力仕様

### 自動生成されるシリーズ構造

すべてのクイズセットは、1つの親シリーズに属します：

```
Parent Series (Level 1)
  ├─ Child Quiz Set 1 (Level 2)
  ├─ Child Quiz Set 2 (Level 2)
  ├─ Child Quiz Set 3 (Level 2)
  └─ Child Quiz Set N (Level 2)
```

### メタデータファイル（metadata.json）

`{output_dir}/metadata.json` - シリーズ情報一元管理

```json
{
  "series": {
    "id": "github-copilot-skills-tutorial",
    "name": "GitHub Copilot Skills チュートリアル",
    "description": "ドキュメント全体の説明",
    "icon": "🎓",
    "level": 1,
    "parentId": null,
    "group": "github-copilot-skills-tutorial-series",
    "questionCount": 84,
    "difficulty": "beginner to advanced",
    "childCount": 6,
    "metadata": {
      "generatedAt": "2026-03-08T10:00:00Z",
      "sourceDocPath": "docs",
      "docStructure": "auto-detected",
      "skillVersion": "2.0"
    }
  },
  "quizSets": [
    {
      "id": "fundamentals",
      "name": "スキル形式の理解",
      "description": "セクション説明",
      "category": "自動検出",
      "icon": "📚",
      "level": 2,
      "parentId": "github-copilot-skills-tutorial",
      "group": "github-copilot-skills-tutorial-series",
      "order": 1,
      "questionCount": 7,
      "difficulty": "beginner",
      "dataPath": "fundamentals/quiz.json",
      "documentPath": "docs/00-fundamentals",
      "order": 1
    },
    {
      "id": "basics",
      "name": "Agent Skills 基礎",
      "description": "セクション説明",
      "category": "自動検出",
      "icon": "🎯",
      "level": 2,
      "parentId": "github-copilot-skills-tutorial",
      "group": "github-copilot-skills-tutorial-series",
      "questionCount": 15,
      "difficulty": "intermediate",
      "dataPath": "basics/quiz.json",
      "documentPath": "docs/01-basics",
      "order": 2
    }
  ]
}
```

#### メタデータフィールド説明

**series オブジェクト**:
- `id` - シリーズの一意識別子（ドキュメントフォルダ名から自動生成）
- `name` - シリーズの表示名（自動生成またはユーザー指定）
- `description` - README.md または最初のファイルの説明
- `level` - 常に `1`（親シリーズ）
- `group` - シリーズグループの識別子
- `questionCount` - すべての子クイズセットの合計問題数
- `childCount` - 子クイズセットの数

**quizSets 配列**:
- 各子クイズセットの情報
- `level`: 常に `2`（子セット）
- `parentId`: 親シリーズのID
- `order`: シリーズ内での並び順（ドキュメント順序から自動決定）

### クイズデータファイル構造

`{output_dir}/{series_id}/quiz.json`

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
      "id": "1",
      "question": "質問文",
      "options": [
        {"id": "A", "text": "選択肢A"},
        {"id": "B", "text": "選択肢B"},
        {"id": "C", "text": "選択肢C"},
        {"id": "D", "text": "選択肢D"}
      ],
      "correctAnswer": "A",
      "explanation": "解説文",
      "difficulty": "beginner|intermediate|advanced"
    }
  ]
}
```

**フィールド説明**:
- `metadata.seriesId` - 所属するシリーズのID
- `metadata.seriesName` - 所属するシリーズの名前
- `metadata.sourcePath` - 生成元のドキュメントパス
- `questions[].difficulty` - 出題難度

---

## シリーズ管理構造の実装例

### 単一シリーズモデル

すべての生成されたクイズセットは、1つの親シリーズに統一されます：

```
📚 [親シリーズ] （レベル1）
 ├─ [子クイズセット1] - 01セクション（レベル2）
 ├─ [子クイズセット2] - 02セクション（レベル2）
 ├─ [子クイズセット3] - 03セクション（レベル2）
 └─ [子クイズセットN] - NNセクション（レベル2）
```

### 構造例1：GitHub Copilot Skills チュートリアル

```
📚 GitHub Copilot Skills チュートリアル（親）
 ├─ 📖 スキル形式の理解（01、5問）
 ├─ 🎯 Agent Skills 基礎（02、15問）
 ├─ 📊 他技術との比較（03、20問）
 ├─ ⚙️ 実装編（04、25問）
 ├─ 🚀 活用編（05、12問）
 └─ 🏆 高度な活用（06、7問）
  
 総計: 84問、6つのクイズセット
```

**metadata.json での記述**:

親シリーズ:
```json
{
  "series": {
    "id": "github-copilot-skills-tutorial",
    "name": "GitHub Copilot Skills チュートリアル",
    "description": "Agent Skills の完全学習ガイド",
    "level": 1,
    "parentId": null,
    "group": "github-copilot-skills-tutorial-series",
    "questionCount": 84,
    "childCount": 6
  }
}
```

### 構造例2：Clean Architecture ガイド

```
🏗️ Clean Architecture 完全ガイド（親）
 ├─ 📋 SOLID 原則（01、21問）
 ├─ 🎯 レイヤー設計（02、18問）
 ├─ 🔧 デザインパターン（03、22問）
 ├─ ⚙️ 実装ガイド（04、20問）
 └─ 📦 ベストプラクティス（05、15問）

 総計: 96問、5つのクイズセット
```

### シリーズ管理のキーポイント

| 項目 | 説明 |
|------|------|
| **親シリーズ** | 1つのみ自動生成。ID は doc_path から決定 |
| **子クイズセット** | ドキュメントのセクション/フォルダごとに自動生成 |
| **order** | ドキュメントの フォルダプレフィックス番号から自動決定 |
| **group** | 親シリーズのIDと同一値で統一 |
| **parentId** | 子セットは必ず親シリーズのIDを参照 |

### 自動生成ロジック

以下のルールで自動的にクイズセットが分類されます：

```
docs/
├── 00-introduction/ → order: 1, id: "introduction"
├── 01-basics/ → order: 2, id: "basics"
├── 02-advanced/ → order: 3, id: "advanced"
└── 03-implementation/ → order: 4, id: "implementation"
        ↓
すべて parent_id = "docs" (親シリーズ) に統一
group = "docs-series" に統一
```

---

## 品質基準

生成されるクイズセットは以下の品質基準を満たします：

### 出題内容
- ✅ ドキュメント内容を正確に反映
- ✅ ドキュメント内の具体例や図表を参照
- ✅ 実践的で理解度を確認できる問題設計
- ✅ 誤答選択肢が紛らわしく、思考を促す

### 詳細度と解説
- ✅ 各問の解説がドキュメント内容と一致
- ✅ 正答のみでなく、誤答理由も示唆
- ✅ 関連トピックへのリンク情報を含む
- ✅ 複合理解が必要な場合はその旨を明記

### 難度分布
- ✅ balanced: 15% beginner : 70% intermediate : 15% advanced
- ✅ beginner_focused: 50% beginner : 40% intermediate : 10% advanced
- ✅ advanced_focused: 10% beginner : 40% intermediate : 50% advanced

### テスト実施
- ✅ ドキュメント内容との矛盾がない
- ✅ 選択肢の長さが極端に異なっていない
- ✅ 文法・表記が統一されている
- ✅ 日本語の自然性を保証

---

## 補足：ドキュメント品質との連携

このスキル実行時に、ドキュメント自体の以下の問題を検出した場合は報告します：

- ❓ 矛盾・不整合（同じ内容が異なる説明）
- ⚠️ 曖昧性（定義や説明が不明確）
- 📝 誤りや古い情報
- 🔗 参照関係の不完全性
- 🔄 複数ファイル間の一貫性の問題

これらは出力レポートの `documentIssues` フィールドに含まれます。

---

## 汎用化版の主な改善点

| 項目 | 既存版 | 汎用版 |
|------|--------|--------|
| **Workspace依存性** | spa-quiz-app に固定 | 完全に独立（相対パスのみ）|
| **シリーズ構成** | 固定的（6シリーズ） | 自動生成（ドキュメント構造から） |
| **シリーズ名生成** | 手動指定のみ | 自動生成（フォルダ名または README タイトルから） |
| **クイズセット分類** | 手動定義（series_config） | 自動洗い出し（フォルダ構造から）|
| **シリーズモデル** | 複数シリーズ対応 | 単一親シリーズ（すべてのクイズセットが属する） |
| **出力パス** | プロジェクト別に指定 | `{doc_path}/quizzes/` がデフォルト |
| **パラメータ数** | 多い（10+） | 少ない（必須1+オプション8） |

### 改善による効果

✅ **シンプル化**
- 必須パラメータは `doc_path` のみ
- 自動生成によりユーザー入力を削減

✅ **完全汎用化**
- 特定プロジェクト・ワークスペース名への依存なし
- どのプロジェクトでも同じスキルで対応

✅ **自動化**
- シリーズ名から クイズセット分類まで自動生成
- 保守性向上、エラー削減

✅ **予測可能性**
- 明確な親子関係（1つの親 + N個の子）
- UI表示が統一される

## 次のステップ

生成されたクイズセットは以下の方法で活用できます：

### ✅ クイズセット活用例

**親シリーズの機能**
1. 学習ロードマップとしての表示
2. 全体的な理解度測定
3. シリーズの進捗管理

**子クイズセットの機能**
1. 各セクション単位での理解確認
2. 段階的な難度上昇による学習
3. セクション別の弱点分析

### 📊 メトリクス活用

生成されたクイズセットのメタデータから：
- ドキュメント品質の測定（テスト対象範囲）
- 学習カバレッジの検証（セクション別問題数）
- シリーズ全体の学習パス設計
- ドキュメント更新による影響度の追跡（sourcePath 記録）

### 🔄 継続的改善サイクル

```
ドキュメント更新
    ↓
自動クイズ再生成
    ↓
シリーズ・クイズセット自動更新
    ↓
学習者からのフィードバック
    ↓
ドキュメント改善
```