---
name: quiz-generator
description: ドキュメントをクイズセット化し、JSON形式で出力。Agent Skills チュートリアルの各Partを対話的に学習できるクイズに変換
license: MIT
---

# Quiz Generator

## 概要

このスキルは、GitHub Copilot Agent Skills チュートリアル（docs/ フォルダ）のドキュメントを、対話的なクイズセットに自動変換します。

各Part（Part 0-5）ごとにシリーズ化され、難度別（beginner/intermediate/advanced）に設計された問題セットを、JSON形式で生成します。

学習者は生成されたクイズで理解度を確認し、解説から詳細を学ぶことができます。

## クイズシリーズ構成

| Series | Part | タイトル | 文書数 | 想定問題数 |
|--------|------|---------|--------|----------|
| **fundamentals** | 0 | スキル形式の理解 | 1 | 5-7 |
| **basics** | 1 | Agent Skills の基礎 | 3 | 12-15 |
| **comparison** | 2 | 他技術との比較 | 4 | 16-20 |
| **implementation** | 3 | 実装編 | 5 | 20-25 |
| **advanced** | 4 | 活用編 | 4 | 16-20 |
| **advanced-topics** | 5 | 高度な活用 | 3 | 12-15 |

**総合計**: 81-102問の学習コンテンツ

---

## 入力パラメータ

### 必須

| パラメータ | 型 | 説明 | 指定可能値 |
|---------|-----|------|----------|
| `series` | string | クイズシリーズ名 | `fundamentals`, `basics`, `comparison`, `implementation`, `advanced`, `advanced-topics` |

### オプション

| パラメータ | 型 | デフォルト | 説明 | 例 |
|---------|-----|----------|------|-----|
| `target_audience` | string | `intermediate` | 対象レベル | `beginner`, `intermediate`, `advanced` |
| `question_count` | number | `自動` | 生成問題数 | `5`, `10`, `15` |
| `include_explanation` | boolean | `true` | 解説を含める | `true`, `false` |
| `difficulty_distribution` | string | `balanced` | 難度配分 | `balanced` (15:70:15), `beginner_focused` (50:40:10), `advanced_focused` (10:40:50) |
| `output_format` | string | `json` | 出力形式 | `json`, `markdown` |

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

### 例1: Basics シリーズのクイズを生成

```
User: "Series: basics でクイズセットを生成してください。
intermediate レベルで、均衡した難度配分でお願いします"

series: basics
target_audience: intermediate
difficulty_distribution: balanced
```

**出力**: `spa-quiz-app/basics/agent-skills-basics.json`
- Part 1-1, 1-2, 1-3 全体をカバーする 12-15 問

### 例2: 初級者向けの Fundamentals クイズ

```
User: "Part 0 (スキル形式の理解) を beginner 向けに、
簡潔なクイズセットで生成してください"

series: fundamentals
target_audience: beginner
question_count: 5
```

**出力**: `spa-quiz-app/fundamentals/skill-format-overview.json`
- 5問（全て初級者向け）
- 推定学習時間: 5-8 分

### 例3: 実装パターンの理解を確認

```
User: "Series: implementation でクイズを生成。
上級者向けで、実装パターン全体の複合理解を問う問題重視で"

series: implementation
target_audience: advanced
difficulty_distribution: advanced_focused
```

**出力**: `spa-quiz-app/implementation/implementation-comprehensive.json`
- 20-25 問（advanced 重視）
- 推定学習時間: 30-40 分

### 例4: Markdown形式での出力

```
User: "Series: comparison をMarkdown形式で出力し、
README.md に含められるようにしてください"

series: comparison
output_format: markdown
```

**出力**: `spa-quiz-app/comparison/quiz-comparison.md`
- 閲覧・編集可能なMarkdown形式

---

## 出力仕様

### メタデータ（metadata.json に追加）
```json
{
  "id": "spa-quiz-app-docs",
  "name": "spa-quiz-app ドキュメント",
  "description": "spa-quiz-appのセットアップ、アーキテクチャ、デプロイ、トラブルシューティングに関するクイズ",
  "category": "技術",
  "icon": "📚",
  "questionCount": 30,
  "difficulty": "intermediate",
  "dataPath": "spa-quiz-app/basics/agent-skills-basics.json",
  "parentId": null,
  "group": null,
  "level": 1,
  "order": 1
}
```

#### フィールド説明
- **id**: クイズセットの一意識別子
- **name**: クイズセット の表示名
- **description**: クイズセットの説明
- **category**: カテゴリ分類
- **icon**: 絵文字アイコン
- **questionCount**: 問題数
- **difficulty**: 難度レベル（beginner/intermediate/advanced）
- **dataPath**: クイズデータファイルの相対パス
- **parentId**: シリーズの親セットID（独立したセットの場合は`null`、シリーズの子の場合は親のID）
- **group**: シリーズグループの識別子（シリーズに属さない場合は`null`）
- **level**: 階層レベル（1=独立または親セット、2=シリーズの子セット）
- **order**: 表示順序（同一グループ内での並び順）

### クイズデータファイル構造
`spa-quiz-app/basics/agent-skills-basics.json`

```json
{
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
      "explanation": "解説文（複数行対応）",
      "difficulty": "beginner|intermediate|advanced"
    }
  ]
}
```

**クイズ JSON のフィールド説明：**

| フィールド | 説明 | 使用例 |
|----------|------|--------|
| `questions` | 問題配列 | `[{ id, question, options, ... }, ...]` |
| `questions[].id` | 問題の一意な番号 | `1`, `2`, `3` |
| `questions[].question` | 問題文 | `"GitHub Copilot Agent Skills は何を教え込むための機能ですか？"` |
| `questions[].options` | 4択選択肢の配列 | `[{ id: "A", text: "選択肢A" }, ...]` |
| `questions[].correctAnswer` | 正答の選択肢ID | `"B"` |
| `questions[].explanation` | 解説（ドキュメント内容に基づく） | `"Agent Skills は..." ` |
| `questions[].difficulty` | 出題難度 | `beginner`, `intermediate`, `advanced` |

**設計のポイント：**
- ✅ **関心の分離**: 表示・管理用メタデータは `metadata.json`、問題データのみをクイズ JSON に保持
- ✅ **保守性向上**: メタデータ修正時にクイズ JSON を編集不要
- ✅ **拡張性**: 複数のクイズセットを同一の `metadata.json` で管理可能

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

これらは出力レポートの `documentIssues` フィールドに含まれます。

---

## 次のステップ

生成されたクイズセットは以下の方法で活用できます：

1. **学習ツール化**: spa-quiz-app に組み込み、対話的学習環境を提供
2. **評価ツール化**: 理解度測定、レベル判定に活用
3. **ドキュメント改善**: 質問から、ドキュメント内の曖昧性を特定
4. **トレーニング教材**: チーム内研修用資料として活用
