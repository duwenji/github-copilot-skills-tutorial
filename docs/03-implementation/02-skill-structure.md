# Part 3-2: スキルの構成要素

このセクションでは、スキル定義の詳細な要素を解説します。

---

## ℹ️ SKILL.md と JSON の関係

このセクションでは **JSON フォーマットの内部構造** を詳しく説明しています。

- **SKILL.md フォーマット**: ユーザーが `.github/skills/` に保存する **Markdown形式**（Part 3-3, 3-4, 3-5 で学習）
- **JSON フォーマット**: SKILL.md 内容や内部管理を **構造化・検証** するための形式（このセクション）

### JSON が活躍する場所

```
┌─────────────────────────────┐
│  SKILL.md（ユーザー向け）    │
│  .github/skills/SKILL.md    │
└────────────┬────────────────┘
             │ 内部で変換 / 検証
             ▼
┌─────────────────────────────┐
│  JSON（システム向け）        │
│  スキマ定義・型検証・API    │
└─────────────────────────────┘
```

**このセクション（Part 3-2）**: 上図の JSON 部分の詳細を学びます。

---

## スキル定義ファイルの全体構造

```json
{
  "id": "スキルの一意識別子",
  "version": "セマンティックバージョン",
  "name": "ユーザーが見る名前",
  "description": "スキルの説明",
  "metadata": { /* スキル情報 */ },
  "parameters": { /* 入力パラメータ */ },
  "prompt": { /* LLM への指示 */ },
  "outputFormat": { /* 出力形式定義 */ },
  "validation": { /* 実行時制約 */ }
}
```

---

## 1. メタデータ（metadata）

### 概要

スキル自体ではなく、**スキルについての情報**を記述します。

### 詳細説明

```json
{
  "metadata": {
    "author": "作成者名（個人またはチーム）",
    "authorEmail": "author@example.com",
    
    "created": "2026-03-07",
    "lastUpdated": "2026-03-15",
    
    "category": "code-analysis",
    "subcategory": "quality",
    
    "tags": ["python", "javascript", "code-quality", "team-productivity"],
    
    "documentation": "https://docs.example.com/skills/code-quality",
    "externalLinks": [
      { "label": "GitHub Repository", "url": "https://github.com/..." },
      { "label": "Video Tutorial", "url": "https://youtube.com/..." }
    ],
    
    "compatibility": {
      "minCopilotVersion": "1.0.0",
      "supportedLanguages": ["en", "ja"]
    },
    
    "license": "MIT",
    "visibility": "public"
  }
}
```

### 各フィールドの説明

| フィールド | 型 | 必須 | 説明 |
|----------|-----|------|------|
| **author** | string | Yes | スキル作成者 |
| **created** | string (ISO 8601) | Yes | 作成日（YYYY-MM-DD） |
| **lastUpdated** | string (ISO 8601) | Yes | 最終更新日 |
| **category** | string | Yes | カテゴリ（code-analysis, docs-generation等） |
| **tags** | array | Yes | 検索用タグ |
| **documentation** | string (URL) | No | ドキュメント URL |
| **license** | string | No | ライセンス（MIT, Apache 2.0等） |
| **visibility** | string | No | 公開範囲（public, private, org） |

### 用途

1. **検索・ディスカバリー**
   ```
   ユーザー検索：tags が ["python", "code-quality"] のスキル
   → 該当スキルを発見
   ```

2. **バージョン管理**
   ```
   created: "2026-03-07"
   lastUpdated: "2026-03-15"
   → 更新頻度を追跡可能
   ```

3. **保守性**
   ```
   author: "Alice Team"
   → 質問時の連絡先が明確
   ```

---

## 2. パラメータ（parameters）

### 概要

ユーザーが **スキル実行時に提供するデータ** を定義します。

### 完全な例

```json
{
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "分析対象のコード",
      "required": true,
      "minLength": 1,
      "maxLength": 5000,
      "pattern": "^[\\s\\S]*$",
      "example": "def hello():\n    print('hello')"
    },
    
    "language": {
      "type": "string",
      "description": "プログラミング言語",
      "required": true,
      "enum": ["python", "javascript", "typescript", "java", "go"],
      "default": "javascript"
    },
    
    "focusAreas": {
      "type": "array",
      "description": "重点分析エリア",
      "items": {
        "type": "string",
        "enum": ["readability", "performance", "security", "testability"]
      },
      "minItems": 1,
      "maxItems": 4,
      "default": ["readability", "performance", "security", "testability"]
    },
    
    "detailLevel": {
      "type": "string",
      "description": "出力の詳細度",
      "enum": ["basic", "detailed", "comprehensive"],
      "default": "detailed"
    },
    
    "maxIssues": {
      "type": "number",
      "description": "返却する最大指摘件数",
      "minimum": 1,
      "maximum": 100,
      "default": 20
    }
  }
}
```

### サポートされる型

| 型 | 説明 | 例 |
|----|------|-----|
| **string** | テキスト | "python" |
| **number** | 数値（整数・小数） | 42, 3.14 |
| **boolean** | 真偽値 | true, false |
| **array** | 配列 | ["a", "b", "c"] |
| **object** | オブジェクト（複雑型） | { "key": "value" } |

### パラメータの制約

```json
// String 型の制約
{
  "type": "string",
  "minLength": 1,        // 最小文字数
  "maxLength": 5000,     // 最大文字数
  "pattern": "^[a-z]+$", // 正規表現による制約
  "enum": ["a", "b", "c"] // 選択肢から選ぶ
}

// Number 型の制約
{
  "type": "number",
  "minimum": 0,          // 最小値（包括）
  "maximum": 100,        // 最大値（包括）
  "exclusiveMinimum": 0, // 最小値（排他）
  "exclusiveMaximum": 100, // 最大値（排他）
  "multipleOf": 5        // 倍数制約（5の倍数）
}

// Array 型の制約
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": ["a", "b", "c"]
  },
  "minItems": 1,         // 最小要素数
  "maxItems": 10,        // 最大要素数
  "uniqueItems": true    // 重複禁止
}
```

---

## 3. プロンプト（prompt）

### 概要

**LLM に送信する指示文** を定義します。

### 完全な例

```json
{
  "prompt": {
    "system": "You are an expert code reviewer with 10+ years of experience...",
    
    "template": "Analyze the following {language} code for quality issues:\n\nCode:\n{code_snippet}\n\nFocus areas: {focusAreas|join(', ')}\nDetail level: {detailLevel}\n\nProvide analysis in JSON format.",
    
    "variables": [
      {
        "name": "code_snippet",
        "type": "string",
        "source": "parameter"
      },
      {
        "name": "language",
        "type": "string",
        "source": "parameter"
      },
      {
        "name": "focusAreas",
        "type": "array",
        "source": "parameter",
        "processor": "join-comma"
      }
    ],
    
    "advancedOptions": {
      "temperature": 0.3,
      "topP": 0.9,
      "maxTokens": 2000
    }
  }
}
```

### 要素説明

#### System Prompt

```
役割と背景を LLM に与える

例1（専門家として）：
"You are an expert Python developer with 15+ years of experience..."

例2（トーン指定）：
"Respond in a professional, technical manner. Use JSON format exclusively."

例3（制約指定）：
"You must respond in valid JSON format. Do not include markdown formatting."
```

#### Template

```
ユーザー入力を埋め込むテンプレート

変数置換：
{code_snippet} → ユーザーが入力したコード
{language} → "python", "javascript" 等

フィルタ関数（オプション）：
{focusAreas|join(', ')} → ["readability", "security"] → "readability, security"
{text|uppercase} → "hello world" → "HELLO WORLD"
{code|escape} → コード内の特殊文字をエスケープ
```

### テンプレート作成のベストプラクティス

```
❌ 悪い例：
"Analyze the code:\n{code_snippet}"

✅ 良い例：
"You are analyzing {language} code.

Code to analyze:
{code_snippet}

Analysis focus areas: {focusAreas|join(', ')}
Detail level: {detailLevel}

Provide your analysis in the following JSON format:
{
  'overallScore': <number 0-100>,
  'categories': [
    {'name': <category>, 'score': <number 0-100>, 'issues': [<string>]}
  ]
}"

なぜ良いか：
1. 言語を明示的に指定
2. 出力形式を詳細に説明
3. JSON 形式の例を示す
4. パースが容易
```

### Advanced Options

```json
{
  "advancedOptions": {
    "temperature": 0.3,      // 0-2: 低いほど決定的、高いほど創造的
    "topP": 0.9,             // 0-1: 核サンプリングの多様性
    "frequencyPenalty": 0.0, // -2-2: 繰り返し単語のペナルティ
    "presencePenalty": 0.0,  // -2-2: 新しい単語の奨励
    "maxTokens": 2000        // 最大出力トークン数
  }
}
```

**推奨値：**
```
分析的・正確性重視のタスク：
  temperature: 0.2-0.5
  topP: 0.8-0.9
  
創造的・多様性重視のタスク：
  temperature: 0.7-1.0
  topP: 0.9-1.0
```

---

## 4. 出力フォーマット（outputFormat）

### 概要

**LLM からの応答が期待スキーマに従っているか検証** する定義です。

### 完全な例

```json
{
  "outputFormat": {
    "type": "json",
    
    "schema": {
      "$schema": "http://json-schema.org/draft-07/schema#",
      
      "type": "object",
      
      "title": "CodeQualityAnalysis",
      
      "description": "Analysis result for code quality",
      
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
              "score": {
                "type": "number",
                "minimum": 0,
                "maximum": 100
              },
              "issues": {
                "type": "array",
                "items": { "type": "string" }
              },
              "severity": {
                "type": "array",
                "items": {
                  "type": "string",
                  "enum": ["HIGH", "MEDIUM", "LOW"]
                }
              }
            },
            
            "required": ["name", "score", "issues"],
            "additionalProperties": false
          },
          
          "minItems": 1,
          "maxItems": 10
        },
        
        "recommendations": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Actionable improvement suggestions"
        }
      },
      
      "required": ["overallScore", "categories", "recommendations"],
      "additionalProperties": false
    },
    
    "examples": [
      {
        "overallScore": 75,
        "categories": [
          {
            "name": "readability",
            "score": 85,
            "issues": [],
            "severity": []
          },
          {
            "name": "security",
            "score": 60,
            "issues": ["SQL injection risk detected"],
            "severity": ["HIGH"]
          }
        ],
        "recommendations": ["Use parameterized queries for SQL statements"]
      }
    ]
  }
}
```

### JSON Schema の重要な制約

| キーワード | 説明 | 例 |
|----------|------|-----|
| **type** | データ型を指定 | "string", "number", "object", "array" |
| **properties** | オブジェクトのフィールドを定義 | { "name": { "type": "string" } } |
| **required** | 必須フィールドを指定 | ["name", "score"] |
| **enum** | 選択可能な値を限定 | ["HIGH", "MEDIUM", "LOW"] |
| **minimum/maximum** | 数値の範囲制約 | { "minimum": 0, "maximum": 100 } |
| **minItems/maxItems** | 配列サイズ制約 | { "minItems": 1, "maxItems": 10 } |
| **additionalProperties** | オブジェクトに追加フィールドを許可 | true / false |

### 出力フォーマットの検証フロー

```
LLM が出力を生成
   ↓
JSON パースが可能か？
   ├─ No → エラー、リトライ
   └─ Yes ↓
Schemaに適合しているか？
   ├─ No → エラー、リトライ
   └─ Yes ↓
ユーザーに返却
```

---

## 5. 検証（validation）

### 概要

**スキル実行時の制約や動作ルール** を定義します。

### 完全な例

```json
{
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
    
    "authentication": {
      "required": true,
      "scope": ["read:code", "write:analysis"]
    },
    
    "costControl": {
      "maxTokensPerRequest": 2000,
      "estimatedCostPerRequest": 0.01,
      "dailyBudget": 100
    }
  }
}
```

### 各フィールドの説明

#### Timeout

```
スキル実行の最大待機時間（秒）

timeout: 30
  → LLM が 30 秒以内に応答しなければエラー
  
推奨値：
  - 高速タスク（スタイルチェック）：10-15秒
  - 中程度（分析・生成）：20-30秒
  - 複雑タスク（ドキュメント生成）：30-60秒
```

#### MaxRetries

```
失敗時の再試行回数

maxRetries: 2
  → 失敗時に最大 2 回リトライ
  → 合計 3 回試行
  
推奨値：2-3回
```

#### Caching

```
同じ入力に対する結果をキャッシュ

caching:
  enabled: true
  ttl: 3600  // 1 時間有効

メリット：
  - 応答時間が 99%+ 高速化（キャッシュヒット時）
  - LLM API 呼び出し削減
  - コスト削減
  
キャッシュキーの生成：
  MD5(skill_id + version + parameters_json)
```

#### RateLimit

```
API 呼び出し頻度の制限

rateLimit:
  requestsPerMinute: 30   // 1分間に30回まで
  requestsPerHour: 1000   // 1時間に1000回まで
  requestsPerDay: 10000   // 1日に10000回まで
```

#### Authentication

```
実行権限・スコープの定義

authentication:
  required: true
  scope: ["read:code", "write:analysis"]
  
スコープの例：
  - read:code       : コード読み取り権限
  - write:analysis  : 分析結果書き込み権限
  - read:private    : プライベートコード読み取り
```

#### CostControl

```
API 使用料金の制御

maxTokensPerRequest: 2000
  → 1回のリクエストで最大 2000 トークン使用

estimatedCostPerRequest: 0.01
  → 1回あたりの推定料金：$0.01

dailyBudget: 100
  → 1日の最大料金：$100
```

---

## スキル定義ファイル全体の例

```json
{
  "id": "analyze-code-quality",
  "version": "1.0.0",
  "name": "コード品質分析",
  "description": "Python, JavaScript, Java, Go コードの品質分析スキル",
  
  "metadata": {
    "author": "AI Engineering Team",
    "created": "2026-03-07",
    "lastUpdated": "2026-03-07",
    "category": "code-analysis",
    "tags": ["python", "javascript", "typescript", "java", "go", "quality"],
    "documentation": "https://docs.example.com/skills/code-quality",
    "license": "MIT"
  },
  
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "分析対象のコード",
      "required": true,
      "maxLength": 5000
    },
    "language": {
      "type": "string",
      "required": true,
      "enum": ["python", "javascript", "typescript", "java", "go"]
    },
    "focusAreas": {
      "type": "array",
      "items": { "type": "string", "enum": ["readability", "performance", "security", "testability"] },
      "default": ["readability", "performance", "security", "testability"]
    }
  },
  
  "prompt": {
    "system": "You are an expert code reviewer...",
    "template": "Analyze the {language} code:\n{code_snippet}\n\nFocus: {focusAreas|join(', ')}"
  },
  
  "outputFormat": {
    "type": "json",
    "schema": {
      "type": "object",
      "properties": {
        "overallScore": { "type": "number", "minimum": 0, "maximum": 100 },
        "categories": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "score": { "type": "number" },
              "issues": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      },
      "required": ["overallScore", "categories"]
    }
  },
  
  "validation": {
    "timeout": 30,
    "maxRetries": 2,
    "caching": { "enabled": true, "ttl": 3600 }
  }
}
```

---

## 次へ進む

→ [Part 3-3: サンプルスキル #1 - コード分析](03-sample-code-analysis.md)
