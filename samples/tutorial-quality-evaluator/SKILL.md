---
name: tutorial-quality-evaluator
description: チュートリアル・技術ドキュメントの品質を多観点から評価し、改善提案を提供。整合性チェック・構成設計最適化・品質評価を統合
license: MIT
---

# Tutorial Quality Evaluator

## 概要

このスキルは、技術チュートリアルやドキュメントの品質を包括的に評価します。GitHub Copilot Skillsチュートリアル作成プロセスから得られた知見を反映し、以下の3つの観点から高速に品質向上を実現します：

- **整合性チェック**: 複数セクション間の一貫性、外部仕様との整合性
- **構成最適化**: 学習パス、難易度配置、サンプルの効果性
- **品質評価**: 可読性、完全性、正確性、実用性

## 対応ドキュメント種別

- 📚 **チュートリアル**: 段階的学習教材
- 📖 **API ドキュメント**: 仕様・リファレンス
- 🛠️ **ハウツーガイド**: 実装ガイド・ベストプラクティス
- 📋 **技術仕様**: 標準・要件定義書
- 🎓 **学習教材**: オンライン講座・研修資料

## 入力パラメータ

### 必須

| パラメータ | 型 | 説明 | 例 |
|---------|-----|------|-----|
| `document_type` | string | ドキュメント種別 | `tutorial`, `api`, `howto` |
| `content` | string | 評価対象のドキュメント本文 | `# Part 1...` |
| `target_audience` | string | 対象ユーザーレベル | `beginner`, `intermediate`, `advanced` |

### オプション

| パラメータ | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `reference_spec` | string | なし | 準拠すべき公式仕様またはスタイルガイド |
| `evaluation_focus` | array | `[consistency, structure, quality]` | 評価重視項目 |
| `section_count` | number | 自動検出 | セクション数（構成評価用） |
| `language` | string | `japanese` | ドキュメント言語 |

## 評価観点

### 1️⃣ 整合性チェック（Consistency）

複数セクション・リソース間の一貫性を検証：

| 項目 | チェック内容 | 重要度 |
|------|-----------|--------|
| **用語の統一性** | 同じ概念に複数の呼び方がないか | HIGH |
| **フォーマット統一** | コード例・テンプレートのスタイル | HIGH |
| **ファイルパス統一** | ファイル・ディレクトリ構造の参照 | HIGH |
| **外部仕様整合** | 公式ドキュメント・標準との齟齬 | CRITICAL |
| **相互参照正確性** | セクション間リンク、参照の正確さ | MEDIUM |
| **命名規則統一** | 変数名・パラメータ名の一貫性 | MEDIUM |
| **バージョン情報** | 対応バージョン・非推奨機能の記載 | MEDIUM |

### 2️⃣ 構成最適化（Structure）

学習効果を最大化する構成設計を評価：

| 項目 | チェック内容 | 重要度 |
|------|-----------|--------|
| **学習パス設計** | セクションの順序が論理的か | HIGH |
| **難易度配置** | 初級→中級→上級の段階的成長 | HIGH |
| **サンプル効果性** | コード例が学習内容と整合しているか | HIGH |
| **前提知識明記** | 各セクションの前提条件が明確か | MEDIUM |
| **セクションバランス** | 各セクションボリュームが適切か | MEDIUM |
| **サマリー効果** | 学習内容をまとめるセクションがあるか | MEDIUM |
| **実践性** | 読者が実際に試せるサンプルがあるか | MEDIUM |

### 3️⃣ 品質評価（Quality）

ドキュメント自体の品質を多角的に評価：

| 項目 | チェック内容 | 重要度 |
|------|-----------|--------|
| **可読性** | 文章の明確性、段落構成、視認性 | HIGH |
| **完全性** | 説明対象の要素すべてが記載されているか | HIGH |
| **正確性** | 技術的な誤りがないか | CRITICAL |
| **明確性** | あいまいな表現がないか | HIGH |
| **実用性** | 読者が即座に活用できるレベルか | MEDIUM |
| **トーン統一** | 文体・敬語・専門用語が一貫しているか | MEDIUM |
| **図解効果** | 図・表・図式が効果的に使われているか | MEDIUM |

## 使用例

### ユースケース1: チュートリアル全体の品質精査

```
User: "このチュートリアル全体を評価してください。
GitHub Copilot Agent Skills のオープンスタンダード仕様に準拠する
という要件があります"

document_type: tutorial
language: japanese
target_audience: intermediate
reference_spec: "https://agentskills.io/ - SKILL.md format, file structure .github/skills/"
evaluation_focus: [consistency, structure, quality]
```

### ユースケース2: セクション間の整合性チェック

```
User: "Part 1 と Part 3 の実装例でスキル命名を確認してください"

document_type: tutorial
content: [複数セクションのテキスト]
evaluation_focus: [consistency]
section_count: 5
```

### ユースケース3: 構成設計の最適化

```
User: "初心者向けチュートリアルの学習パスを評価して、
セクション順序の改善提案をしてください"

document_type: tutorial
target_audience: beginner
evaluation_focus: [structure]
```

## 出力形式

包括的な評価レポートを JSON で返却します：

```json
{
  "overall_score": 87,
  "evaluation_date": "2026-03-07",
  "document_type": "tutorial",
  "summary": {
    "strengths": [
      "GitHub公式仕様との高い整合性",
      "段階的な学習パスが組まれている",
      "実装サンプルが豊富"
    ],
    "weaknesses": [
      "一部セクションで用語の使い分けが不統一",
      "図解・図式が不足している"
    ],
    "recommendation": "用語統一と図解追加で大幅な改善が期待できます"
  },
  "consistency_check": {
    "score": 85,
    "terminology_consistency": {
      "status": "GOOD",
      "issues": [
        {
          "severity": "MEDIUM",
          "issue": "'Agent Skill' と 'スキル' の混在",
          "locations": ["Part 1-2 line 45", "Part 2-1 line 23"],
          "suggestion": "用語統一ガイドを作成、すべてのセクションで統一"
        }
      ],
      "inconsistency_rate": 5
    },
    "format_consistency": {
      "status": "GOOD",
      "issues": [],
      "consistency_rate": 100
    },
    "filepath_consistency": {
      "status": "GOOD",
      "issues": [],
      "sample_count": 12,
      "correct_count": 12
    },
    "external_spec_compliance": {
      "status": "EXCELLENT",
      "spec_checked": "https://agentskills.io/",
      "compliance_score": 98
    },
    "cross_reference_accuracy": {
      "status": "GOOD",
      "broken_links": 0,
      "outdated_references": 0,
      "total_references": 45
    }
  },
  "structure_check": {
    "score": 88,
    "learning_path": {
      "status": "GOOD",
      "section_count": 20,
      "logical_flow": "EXCELLENT",
      "suggestions": [
        "Part 0 を導入部に配置したことで迷わず学べる構造"
      ]
    },
    "difficulty_progression": {
      "status": "GOOD",
      "distribution": {
        "beginner_sections": 8,
        "intermediate_sections": 7,
        "advanced_sections": 5
      },
      "analysis": "初級から上級への段階が明確"
    },
    "sample_effectiveness": {
      "status": "GOOD",
      "sample_count": 8,
      "executable_samples": 8,
      "issues": []
    },
    "prerequisites_clarity": {
      "status": "GOOD",
      "clearly_marked_sections": 18,
      "missing_prerequisites": 2
    }
  },
  "quality_check": {
    "score": 88,
    "readability": {
      "status": "GOOD",
      "fog_index": 12.3,
      "avg_sentence_length": 18,
      "analysis": "中上級者向けに適切な難易度"
    },
    "completeness": {
      "status": "GOOD",
      "coverage_percentage": 94,
      "missing_sections": [
        "Enterprise/Organization-level skills（記載予定対象外）"
      ]
    },
    "accuracy": {
      "status": "EXCELLENT",
      "technical_errors": 0,
      "outdated_information": 0
    },
    "clarity": {
      "status": "GOOD",
      "ambiguous_phrases": 1,
      "examples": [
        {
          "phrase": "複製可能なスキル",
          "location": "Part 2-3 line 12",
          "clarification": "「再利用可能なスキル」がより正確"
        }
      ]
    },
    "tone_consistency": {
      "status": "EXCELLENT",
      "style_guide_adherence": 97,
      "issues": []
    }
  },
  "priority_improvements": [
    {
      "priority": "HIGH",
      "category": "consistency",
      "issue": "用語の統一",
      "effort": "1-2時間",
      "impact": "品質スコア +3点"
    },
    {
      "priority": "MEDIUM",
      "category": "quality",
      "issue": "図解・図式の強化",
      "effort": "2-3時間",
      "impact": "可読性向上、学習効率 +15%"
    },
    {
      "priority": "LOW",
      "category": "structure",
      "issue": "前提知識の明記強化",
      "effort": "1時間",
      "impact": "初心者対応性向上"
    }
  ],
  "detailed_recommendations": {
    "immediate_actions": [
      "用語統一の優先順位付けリストを作成",
      "全テキスト検索による一括修正"
    ],
    "structural_improvements": [
      "図解テンプレート作成・適用",
      "前提知識セクションの拡充"
    ],
    "quality_enhancements": [
      "技術用語の定義集作成",
      "実装サンプルの実行テスト自動化"
    ]
  },
  "estimated_improvement": {
    "current_score": 87,
    "potential_score": 94,
    "estimated_effort": "3-4時間",
    "roi": "高い（可読性・学習効果の大幅改善）"
  }
}
```

## 実行オプション

| 設定 | 値 |
|------|-----|
| Temperature | 0.2（精度重視） |
| Top P | 0.9 |
| Max Tokens | 4000 |
| タイムアウト | 60秒 |

## このスキルが活用する知見

このスキルは、GitHub Copilot Agent Skills チュートリアル作成で得られた以下の知見を集約しています：

✅ **GitHub公式仕様との整合性確認** - SKILL.md形式、ファイルパス構造  
✅ **多セクション間の用語・フォーマット統一** - 20セクションの調整経験  
✅ **バージョン・プラットフォーム対応情報の管理** - サポート状況の正確な記載  
✅ **段階的な学習構成設計** - 初級→中級→上級の配置最適化  
✅ **実装サンプルの実用性確保** - 実際に動作するコードの提供  
✅ **オープンスタンダード基盤の説明** - Anthropic/Githubの立場の正確な反映

## デモンストレーション

> **使用例**: このチュートリアル全体を評価する場合
> ```
> 入力：20個すべてのセクション + GitHub公式仕様参照
> 出力：3つの観点から総合スコア 87/100 ＋ 優先度付き改善提案
> 実行時間：約 45秒
> ```

