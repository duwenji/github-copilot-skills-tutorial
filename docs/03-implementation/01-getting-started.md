# Part 3-1: スキル作成のステップバイステップガイド

## 概要

このセクションでは、実際に Agent Skill を一から作成するための完全なガイドを提供します。

---

## スキル作成の5つのフェーズ

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

## Phase 1: 要件定義

### ステップ1-1: スキルの目的を明確化

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

### ステップ1-2: スキルの対象ユーザーを定義

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

### ステップ1-3: スキルの範囲を限定

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

## Phase 2: スキル設計

### ステップ2-1: 入力パラメータを定義

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

### ステップ2-2: 出力フォーマットを設計

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

### ステップ2-3: 依存関係と制約を識別

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

## Phase 3: 実装

### ℹ️ フォーマット選択ガイド

スキルを実装する方法は **2 つ** あります：

| 項目 | SKILL.md（推奨）| JSON（高度）|
|------|-----|-----|
| **形式** | Markdown + YAML | JSON |
| **保存場所** | `.github/skills/SKILL.md` | API層/内部管理 |
| **推奨対象** | ほぼすべての開発者 | システム開発者・複雑なケース |
| **学習パス** | Part 0 を確認 | このセクションを続行 |

👉 **初めてなら [Part 0: スキル形式の理解](../../00-fundamentals/skill-format-overview.md) で SKILL.md フォーマットを学んでください。**

---

### ステップ3-1: スキル定義ファイルの骨組みを作成

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

### ステップ3-2: パラメータを実装

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

### ステップ3-3: プロンプトテンプレートを実装

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

### ステップ3-4: 出力フォーマットを実装

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

### ステップ3-5: 検証ルールを実装

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

## Phase 4: テスト

### ステップ4-1: テストケースを設計

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

### ステップ4-2: テストの実行

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

### ステップ4-3: テスト結果のドキュメント化

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

## Phase 5: デプロイ & ドキュメント

### ステップ5-1: リポジトリへの登録

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

## 説明
Python, JavaScript, Java, Go コードの品質を分析し、
改善点を提案するスキル

## 使用方法
```

スキル名: analyze-code-quality
入力: code_snippet, language, focusAreas
出力: JSON（スコア + 指摘事項）

```

## 使用例
...

## パラメータ
...

## 出力フォーマット
...

## サンプル実行結果
...

## 制限事項
...

## トラブルシューティング
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
