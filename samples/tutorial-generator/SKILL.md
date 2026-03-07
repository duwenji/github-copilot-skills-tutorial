---
name: tutorial-generator
description: 技術トピック・既存資料からチュートリアルを自動生成。構成設計→執筆ガイド→サンプル配置→品質評価を一貫サポート
license: MIT
---

# Tutorial Generator

## 概要

このスキルは、技術トピックやドキュメント資料から、GitHub Copilot Agent Skills チュートリアル作成で得られた最適な構成を備えたチュートリアルを自動生成します。

単なる文章生成ではなく、**学習効果を最大化する構成設計** から **品質確保まで** を一貫してサポートする複合スキルです。

## 3つの生成モード

### モード 1️⃣: **構成自動生成**（Outline Generation）
トピック情報から、最適なセクション構成を自動生成

### モード 2️⃣: **執筆支援**（Content Generation）
各セクションのテンプレート・ガイド・サンプル配置を提案

### モード 3️⃣: **資料変換**（Content Conversion）
ブログ記事・既存ドキュメントをチュートリアル形式に自動変換

---

## 入力パラメータ

### 必須

| パラメータ | 型 | 説明 | 例 |
|---------|-----|------|-----|
| `mode` | string | 生成モード | `outline`, `content`, `conversion` |
| `topic` | string | チュートリアル対象トピック | `GitHub Copilot Agent Skills`, `REST API Design` |
| `target_audience` | string | 対象レベル | `beginner`, `intermediate`, `advanced` |

### オプション（モード別）

#### Outline Generation用

| パラメータ | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `estimated_duration` | string | `120` | 推定学習時間（分） |
| `part_count` | number | 自動計算 | パート分割数 |
| `include_samples` | boolean | `true` | サンプルスキル・コードを含めるか |
| `reference_spec` | string | なし | 準拠すべき仕様・標準 |

#### Content Generation用

| パラメータ | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `section_id` | string | required | セクションID（例: `part-1-2`) |
| `outline` | object | required | アウトラインから参照した構成情報 |
| `style_guide` | string | `technical` | 執筆スタイル |

#### Content Conversion用

| パラメータ | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `source_content` | string | required | 変換元のドキュメント本文 |
| `source_format` | string | `blog` | ソース形式：`blog`, `documentation`, `whitepaper`, `specification` |
| `target_structure` | string | `multi-part` | ターゲット構成 |

---

## 使用例

### 例1: 新しい技術トピックのチュートリアル構成生成

```
User: "REST API Design の初級～上級向け、150分のチュートリアル構成を生成してください。
GitHub公式仕様の同じレベルで品質を確保してください"

mode: outline
topic: REST API Design
target_audience: beginner-to-advanced
estimated_duration: 150
references_spec: "https://restfulapi.net/ + OpenAPI 3.0 Specification"
```

### 例2: 既存ブログからチュートリアルへの自動変換

```
User: "マイクロサービス設計の5回のブログシリーズを、
構造化チュートリアルに変換してください"

mode: conversion
source_content: [5つのブログ記事テキスト]
source_format: blog
topic: Microservices Architecture
target_audience: intermediate
target_structure: multi-part
```

### 例3: 特定セクションの詳細コンテンツ生成

```
User: "Part 2-3『実装パターン』のセクションコンテンツを生成してください。
サンプルコードと図式を含めてください"

mode: content
section_id: part-2-3
section_title: 実装パターン集
topic: REST API Design
outline: [自動生成されたアウトラインから参照]
include_diagrams: true
include_samples: true
```

---

## 出力形式

### モード1: Outline Generation の出力

```json
{
  "project_title": "REST API Design チュートリアル",
  "target_audience": "beginner-to-advanced",
  "estimated_duration_minutes": 150,
  "structure": {
    "introduction_section": {
      "id": "intro",
      "title": "REST API Design へようこそ",
      "duration_minutes": 15,
      "content_focus": [
        "REST API の定義",
        "このチュートリアルで学べること",
        "前提知識"
      ]
    },
    "parts": [
      {
        "part_id": "part-1",
        "part_title": "基礎編: REST の原則",
        "duration_minutes": 45,
        "difficulty": "beginner",
        "sections": [
          {
            "section_id": "part-1-1",
            "title": "REST とは何か",
            "key_topics": [
              "REST原則の6つの制約",
              "ステートレス性",
              "統一インターフェース"
            ],
            "should_include": [
              "定義図式",
              "対比例（REST vs SOAP）"
            ],
            "duration_minutes": 20,
            "difficulty_level": 1
          },
          {
            "section_id": "part-1-2",
            "title": "HTTP メソッドの完全ガイド",
            "key_topics": [
              "GET, POST, PUT, DELETE, PATCH",
              "メソッド選択の判断基準",
              "idempotentn（冪等性）"
            ],
            "should_include": [
              "メソッド比較表",
              "実装例 3つ"
            ],
            "duration_minutes": 15,
            "difficulty_level": 1
          }
        ]
      },
      {
        "part_id": "part-2",
        "part_title": "実装編: API 設計パターン",
        "duration_minutes": 60,
        "difficulty": "intermediate",
        "sections": [
          {
            "section_id": "part-2-1",
            "title": "リソース設計",
            "key_topics": [
              "リソース識別",
              "URL 命名規則",
              "ネストされたリソース"
            ],
            "should_include": [
              "実装ガイド",
              "実行可能なサンプルコード",
              "よくある間違いと修正"
            ],
            "duration_minutes": 25,
            "difficulty_level": 2
          }
        ]
      },
      {
        "part_id": "part-3",
        "part_title": "高度な活用: エラー処理・セキュリティ",
        "duration_minutes": 45,
        "difficulty": "advanced",
        "sections": [
          {
            "section_id": "part-3-1",
            "title": "包括的なエラーハンドリング",
            "key_topics": [
              "標準 HTTP ステータスコード",
              "エラーレスポンスフォーマット",
              "ユーザーフレンドリーなメッセージ"
            ],
            "duration_minutes": 20,
            "difficulty_level": 3
          }
        ]
      }
    ]
  },
  "cross_cutting_concerns": {
    "samples": [
      {
        "name": "simple-rest-api",
        "description": "基本的な CRUD API サンプル",
        "language": "python",
        "part_references": ["part-1", "part-2-1"]
      },
      {
        "name": "error-handling-patterns",
        "description": "エラーハンドリング実装例",
        "language": "typescript",
        "part_references": ["part-3-1"]
      }
    ],
    "diagrams": [
      {
        "title": "REST API リクエスト/レスポンスフロー",
        "recommended_for_sections": ["part-1-1", "part-1-2"]
      }
    ]
  },
  "estimated_quality_score": 92,
  "quality_assessment_suggestions": [
    "各部の長さが適切（初級から上級への段階的成長）",
    "実装サンプルが配置されている",
    "図解が効果的に配置される見込み"
  ],
  "next_steps": [
    "1. このアウトラインで quality-evaluator スキルで事前検証",
    "2. content モードで各セクションを順番に生成",
    "3. 完成後、tutorial-quality-evaluator で最終検証"
  ]
}
```

### モード2: Content Generation の出力

```markdown
# Part 1-1: REST とは何か

## セクション概要
学習時間：20分
難易度：★☆☆☆☆（初級）

---

## 学習目標

このセクションを完了すると、以下ができるようになります：

✓ REST（Representational State Transfer）の定義を説明できる
✓ REST の 6つの制約を理解し説明できる
✓ SOAP や RPC との違いを比較説明できる
✓ あなたが設計する API が「REST的」であるかを判断できる

---

## 📚 コンテンツ

### REST の基本定義

REST は **Representational State Transfer** の略で、2000年に Roy T. Fielding が博士論文で提唱したアーキテクチャスタイルです。

...（詳細コンテンツ）

---

## 🔍 実装ガイド

このセクションで説明した概念を現実に適用する際のポイント：

✓ あなたの API がステートレス性を保っているか確認
✓ キャッシュ可能性について検討
✓ 統一インターフェースを意識した設計

---

## 📝 演習：このセクションで学んだことをチェック

□ REST の 6つの制約をすべて説明できる
□ ステートレス性がなぜ重要かを説明できる
□ 既存の API（例：Twitter, GitHub）で REST原則がどう使われているか挙げられる

---

## ➡️ 次のセクション

→ [Part 1-2: HTTP メソッドの完全ガイド](./01-http-methods.md)

---

## 📖 詳細な執筆ガイド

**このセクション作成時の推奨事項：**

1. **冒頭の定義（1段落）**
   - 字数目安：80-100文字
   - 読者が「このセクションで何を学ぶのか」直感的に理解できること

2. **背景説明（3-4段落）**
   - なぜ REST が重要か
   - 伝統的なアプローチとの違い

3. **6つの制約の解説**
   - 各制約について、図式 + 実例 + 対比例
   - 推奨図式：制約相互の関係図

4. **実装での注意点**
   - よくある誤解＆実装エラー

```

### モード3: Content Conversion の出力

```
変換完了: 5ブログ記事 → 3パートチュートリアル構成

元のブログ記事           →  チュートリアル内の位置
「マイクロサービス入門」  →  Part 1-1 + Part 1-2（構成を再編成）
「設計の 5つのパターン」  →  Part 2-1 ～ Part 2-5（各パターンを独立セクション化）
「運用とモニタリング」    →  Part 3-1（実装面も追加）
「よくある失敗」        →  Part 3-2（アンチパターン）
「事例研究」           →  各パートの案内例に統合

推奨される追加内容：
- Part 1-0: イントロダクション（前提知識）
- 各部の概要セクション（全体構成を示す図式）
- 段階的な実装サンプル（5ブログには散在）
```

---

## このスキルで活用される知見

このスキルは、GitHub Copilot Agent Skills チュートリアル作成で洗い出された以下の知見を集約しています：

### ✅ 構成設計の知見

```
最適なチュートリアル構成 = K × D × A × S

K = Knowledge Structure（知識構造）
  └─ Part分割のタイミング
  └─ 難易度の段階付け
  └─ 前提知識の配置

D = Duration Balance（時間配分）
  └─ 各部の長さ最適化
  └─ セクション間バランス
  └─ 演習・休息ポイント

A = Audience Adaptation（聴衆適応）
  └─ 初級→中級→上級の段階性
  └─ 用語説明のレベル
  └─ サンプルの複雑性

S = Sample Placement（サンプル配置）
  └─ 学習内容に対応したコード例
  └─ 難易度の段階的上昇
  └─ 実行可能性の確保
```

### ✅ 執筆品質の知見

- 明確な学習目標の設定
- セクション冒頭の概要記述
- 段階的な詳細説明
- 実装ガイドの配置
- 自己評価チェックリスト

### ✅ 資料変換の知見

- ブログ記事の文脈→チュートリアル構造への再構成
- 散在的な情報の統一的な配置
- 前提知識の明確化
- 実装例の拡充

---

## 実行オプション

| 設定 | 値 |
|------|-----|
| Temperature | 0.4（創造性と精度のバランス） |
| Top P | 0.9 |
| Max Tokens | 6000 |
| タイムアウト | 120秒 |

---

## 連携スキル

このスキルは以下と連携して威力を発揮します：

| スキル | 役割 |
|--------|------|
| **tutorial-quality-evaluator** | 生成フェーズ後の品質検証 |
| **code-quality-analyzer** | サンプルコードの品質確認 |
| **doc-generator** | API ドキュメント自動生成 |

---

## 典型的な使用フロー

```
1. Tutorial Generator（このスキル）
   ├─ Mode: outline で構成を生成
   └─ 出力：20～30のセクション定義 + 連携情報

2. Tutorial Generator（Mode: content）
   ├─ 各セクションのテンプレート・ガイド生成
   └─ 出力：執筆ガイド + サンプル配置提案

3. 実装フェーズ（人間）
   └─ テンプレートに基づき、詳細コンテンツを執筆

4. Tutorial Quality Evaluator
   ├─ 整合性チェック
   ├─ 構成最適化の提案
   └─ 最終品質評価 + 改善箇所の優先順位付け

5. 完成・公開
   └─ パッケージ化、バージョニング
```

---

## 想定される成果

```
| 指標 | 従来方式 | Tutorial Generator使用時 |
|------|-------|------------------------|
| チュートリアル構成作成 | 4-8時間 | 15-30分 |
| 執筆ガイド作成 | 2-3時間 | テンプレート自動生成 |
| ブログ→チュートリアル変換 | 6-10時間 | 30-60分 + 調整 |
| 品質評価 | 1-2時間 | tutorial-quality-evaluatorで自動化 |
| **合計時間削減** | 基準 | **70-80%削減** |
```

