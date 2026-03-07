---
name: code-quality-analyzer
description: Python, JavaScript, TypeScript, Java, Go コードの品質を多次元的に分析し、改善提案を提供するスキル
license: MIT
---

# Code Quality Analyzer

## 概要

このスキルは、複数の言語に対応したコード品質分析を自動で実行します。可読性、パフォーマンス、セキュリティ、テスト可能性の４つの観点から包括的に分析し、改善提案を提供します。

## 対応言語

- Python
- JavaScript
- TypeScript
- Java
- Go

## 入力パラメータ

### 必須

| パラメータ | 型 | 説明 | 例 |
|---------|-----|------|-----|
| `code_snippet` | string | 分析対象のコード（最大5000文字） | `def calculate_sum(numbers):...` |
| `language` | string | プログラミング言語 | `python` |

### オプション

| パラメータ | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `focusAreas` | array | `[readability, performance, security, testability]` | 重点分析エリア |
| `detailLevel` | string | `detailed` | 結果の詳細度：`basic`, `detailed`, `comprehensive` |
| `maxIssues` | number | `20` | 返却する最大指摘件数 |

## 使用例

```
User: "このPythonコードの品質を詳しく分析してください"

code_snippet: |
  def calculate_sum(numbers):
      result = 0
      for n in numbers:
          result = result + n
      return result

language: python
detailLevel: comprehensive
focusAreas: [readability, performance, security]
```

## 出力形式

JSON形式で以下の情報を返却します：

```json
{
  "overallScore": 75,
  "categories": [
    {
      "name": "readability",
      "score": 80,
      "issues": ["Variable names are unclear"],
      "severity": ["LOW"]
    },
    {
      "name": "performance",
      "score": 70,
      "issues": ["Inefficient loop structure"],
      "severity": ["MEDIUM"]
    },
    {
      "name": "security",
      "score": 85,
      "issues": [],
      "severity": []
    },
    {
      "name": "testability",
      "score": 65,
      "issues": ["Function has no assertions"],
      "severity": ["MEDIUM"]
    }
  ],
  "recommendations": [
    "Use more descriptive variable names",
    "Consider using sum() built-in function for Python",
    "Add type hints for better code clarity"
  ],
  "codeSmells": [
    "Unnecessary loop construction",
    "Missing input validation"
  ],
  "positiveAspects": [
    "Clear function structure",
    "No security vulnerabilities detected",
    "Handles empty lists gracefully"
  ]
}
```

## 分析基準

### Readability（可読性）
- 変数名の説明性
- コード構造の明確さ
- コメント品質
- 関数サイズの適切さ

### Performance（パフォーマンス）
- アルゴリズムの効率性
- ループ最適化
- メモリ使用量
- データベースクエリの最適化

### Security（セキュリティ）
- 入力値検証
- 認証チェック
- データ漏洩のリスク
- インジェクション脆弱性

### Testability（テスト可能性）
- エッジケースのカバレッジ
- エラーシナリオの処理
- コードのモジュール性
- 関数の責任の分離

## 実行オプション

| 設定 | 値 |
|------|-----|
| Temperature | 0.3（精度重視） |
| Top P | 0.9 |
| Max Tokens | 2000 |
| タイムアウト | 30秒 |
| リトライ回数 | 2回 |

## キャッシング

- **有効**: はい
- **TTL**: 3600秒（1時間）
- **戦略**: 入力のMD5ハッシュ

## レート制限

- 1分あたり: 30リクエスト
- 1時間あたり: 1000リクエスト  
- 1日あたり: 10000リクエスト

## コスト管理

- 推定コストが高く見積もられたら、以下を検討してください：
  - コード片を小さくする
  - detailLevel を下げる
  - focusAreas を絞る

