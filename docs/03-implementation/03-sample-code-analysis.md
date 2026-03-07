# Part 3-3: サンプルスキル #1 - コード品質分析

このセクションでは、**実際に使用できる完全なコード分析スキル** を SKILL.md フォーマットで実装します。

---

## スキル概要

```
スキル名：analyze-code-quality
目的：Python, JavaScript, TypeScript, Java, Go のコードの品質を分析
難度：★★☆☆☆（初級）
実装時間：30分～1時間
推奨フォーマット：SKILL.md
```

---

## SKILL.md フォーマット（推奨）

### ファイル：`.github/skills/code-quality-analyzer.md`

```markdown
---
id: analyze-code-quality
version: 1.0.0
name: コード品質分析
description: Python, JavaScript, TypeScript, Java, Go コードの品質を多次元的に分析し、改善提案を提供します
author: Development Productivity Team
tags: [python, javascript, typescript, java, go, code-quality, review]
category: code-analysis
documentation: https://docs.example.com/skills/code-quality
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

### ファイル：`analyze-code-quality.json`

ファイルパス：`skills/definitions/analyze-code-quality.json`

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

## 使用例

### 例1: 基本的な使用方法

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

### 例2: 全オプション指定版

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

## カスタマイズガイド

### カスタマイズ1: 言語を追加

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

### カスタマイズ2: 重点分析エリアを追加

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

### カスタマイズ3: スコアの厳しさを調整

デフォルト：バランス型
企業要件：セキュリティを最重視

```json
// prompt のテンプレートに重み付けを追加

"Security is your TOP PRIORITY. 
If ANY security issue is found, score must be ≤ 50.
Apply strict scrutiny to input validation, authentication, data handling.
"
```

### カスタマイズ4: 出力フォーマットを簡潔に

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

## トラブルシューティング

### 問題1: タイムアウトが頻繁に発生

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

### 問題2: 出力フォーマットが毎回異なる

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

### 問題3: セキュリティ指摘が不足

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

## テストケース

### テストケース1: 正常系

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

### テストケース2: セキュリティ問題

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

### テストケース3: 最大サイズ

```bash
入力：5000文字のコード

期待される結果：
✓ タイムアウトしない（30秒以内）
✓ スキーマに準拠した出力
```

---

## 実装チェックリスト

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

## 次へ進む

→ [Part 3-4: サンプルスキル #2 - ドキュメント生成](04-sample-doc-generation.md)
