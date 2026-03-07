# Part 3-4: サンプルスキル #2 - ドキュメント自動生成

このセクションでは、**コード内のDocstring を自動生成するスキル** を SKILL.md フォーマットで実装します。

難度は Part 3-3 より少し高く、複数の出力フォーマット対応です。

---

## スキル概要

```
スキル名：generate-documentation
目的：関数・クラスのドキュメント（docstring）を自動生成
難度：★★★☆☆（中級）
実装時間：1～1.5時間
対応言語：Python, JavaScript/TypeScript, Java, Go
対応フォーマット：Google Style, NumPy Style, JSDoc, JavaDoc
推奨形式：SKILL.md
```

---

## SKILL.md フォーマット（推奨）

### ファイル：`.github/skills/doc-generator.md`

```markdown
---
id: generate-documentation
version: 1.0.0
name: ドキュメント自動生成
description: 関数・メソッド・クラスのDocstring を複数形式で自動生成します
author: Documentation Engineers
tags: [documentation, docstring, productivity, python, javascript, java, go]
category: documentation
---

# ドキュメント自動生成スキル

## 概要

このスキルは以下の種類のドキュメント（Docstring）を自動生成します：

- **Google Style**: Python で一般的
- **NumPy Style**: 科学計算向け
- **JSDoc**: JavaScript/TypeScript 向け
- **JavaDoc**: Java 向け
- **Go Doc**: Go 向け

生成されるドキュメントは：
- 関数の目的を明確に説明
- パラメータの型と説明を記載
- 戻り値の説明
- 使用例（オプション）
- 例外情報（該当時）

## 使い方

1. 関数またはクラスを選択
2. Copilot に「ドキュメント自動生成スキルを実行」と指示
3. 選択したドキュメント形式で Docstring が生成されます

## パラメータ

### codeSnippet (必須)
ドキュメント対象のコード（関数またはクラス）
- 5～500 行

### language (必須)
ソースコード言語
- `python`
- `javascript`
- `typescript`
- `java`
- `go`

### docStyle (必須)
ドキュメント形式
- `google`: Google 形式（Python 推奨）
- `numpy`: NumPy 形式（科学計算向け）
- `jsdoc`: JSDoc 形式（JavaScript/TypeScript）
- `javadoc`: JavaDoc 形式（Java）
- `godoc`: Go Doc 形式（Go）

### includeExamples (オプション)
使用例を含めるか
- `true`: 含める（詳細）
- `false`: 含めない（簡潔）

デフォルト: `true`

### includeTypeHints (オプション)
型ヒント情報を含めるか
- `true`: 含める
- `false`: 含めない

デフォルト: `true`

## 出力フォーマット

```json
{
  "generatedDocstring": "...",
  "format": "google|numpy|jsdoc|javadoc|godoc",
  "language": "...",
  "insertionPoint": {
    "lineNumber": 5,
    "position": "above|inside"
  },
  "estimatedReadabilityIncrease": 0.25,
  "suggestions": [
    "より詳細な説明を追加できます",
    "例外処理について記載することをお勧めします"
  ]
}
```

## 実装例

### Example 1: Python 関数（Google Style）

入力コード:
```python
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)
```

生成される Docstring:
```python
def calculate_average(numbers):
    """
    数値リストの平均値を計算します。
    
    Args:
        numbers (list): 数値のリスト。最低でも1つの要素が必要です。
        
    Returns:
        float: 計算された平均値。
        
    Raises:
        ValueError: リストが空の場合。
        TypeError: 数値以外の値がリストに含まれている場合。
        
    Examples:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
        >>> calculate_average([10, 20])
        15.0
    """
    if not numbers:
        raise ValueError("リストは空にできません")
    total = sum(numbers)
    return total / len(numbers)
```

### Example 2: TypeScript クラス（JSDoc）

入力コード:
```typescript
class UserService {
    constructor(database) {
        this.database = database;
    }
    
    async getUserById(id) {
        return this.database.query('users', id);
    }
}
```

生成される JSDoc:
```typescript
/**
 * ユーザー情報を管理するサービスクラス
 * @class UserService
 */
class UserService {
    /**
     * UserService を初期化します
     * @param {Database} database - データベースインスタンス
     */
    constructor(database) {
        this.database = database;
    }
    
    /**
     * ID でユーザーを取得します
     * @async
     * @param {string} id - ユーザー ID
     * @returns {Promise<User>} ユーザーオブジェクト
     * @throws {Error} ユーザーが見つからない場合
     * @example
     * const user = await userService.getUserById('user123');
     */
    async getUserById(id) {
        return this.database.query('users', id);
    }
}
```

---

## JSON フォーマット（参考：内部管理向け）

```json
{
  "id": "generate-documentation",
  "version": "1.0.0",
  "name": "ドキュメント自動生成",
  "description": "関数・メソッド・クラスのドキュメンテーション（docstring）を自動生成するスキル。複数のドキュメンテーションスタイル（Google, NumPy, JSDoc等）に対応。",
  
  "metadata": {
    "author": "Documentation Engineers",
    "authorEmail": "docs@example.com",
    "created": "2026-03-07",
    "lastUpdated": "2026-03-07",
    "category": "documentation",
    "subcategory": "code-documentation",
    "tags": [
      "documentation",
      "docstring",
      "python",
      "javascript",
      "typescript",
      "java",
      "go",
      "productivity"
    ],
    "documentation": "https://docs.example.com/skills/generate-documentation",
    "license": "MIT"
  },
  
  "parameters": {
    "code_element": {
      "type": "string",
      "description": "ドキュメント化する関数・メソッド・クラスの定義（署名を含む）",
      "required": true,
      "minLength": 20,
      "maxLength": 3000,
      "example": "def calculate_fibonacci(n: int, memo: dict = None) -> int:"
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
    
    "docstyle": {
      "type": "string",
      "description": "ドキュメンテーションスタイル（言語に応じて自動選択されます）",
      "enum": [
        "google",
        "numpy",
        "sphinx",
        "jsdoc",
        "javadoc",
        "godoc"
      ],
      "default": "google",
      "example": "google"
    },
    
    "includeSummary": {
      "type": "boolean",
      "description": "1行概要を含める",
      "default": true
    },
    
    "includeArgs": {
      "type": "boolean",
      "description": "引数の説明を含める",
      "default": true
    },
    
    "includeReturns": {
      "type": "boolean",
      "description": "戻り値の説明を含める",
      "default": true
    },
    
    "includeRaises": {
      "type": "boolean",
      "description": "発生する例外の説明を含める",
      "default": true
    },
    
    "includeExamples": {
      "type": "boolean",
      "description": "使用例を含める",
      "default": true
    },
    
    "detailLevel": {
      "type": "string",
      "description": "ドキュメントの詳細度",
      "enum": [
        "brief",
        "standard",
        "detailed"
      ],
      "default": "standard"
    }
  },
  
  "prompt": {
    "system": "You are an expert technical documentation writer with extensive experience in API documentation, code documentation, and developer experience. Your documentation should be clear, concise, professional, and immediately useful to developers. Always include practical information and avoid vague descriptions.",
    
    "template": "Generate professional documentation for the following {language} code element.\n\nCode element:\n{code_element}\n\nDocumentation style: {docstyle}\nDetail level: {detailLevel}\n\nInclude:\n{includeSection_summary}{includeSection_args}{includeSection_returns}{includeSection_raises}{includeSection_examples}\n\nRequirements:\n1. Use ONLY the specified documentation style ({docstyle})\n2. Make the documentation precise and immediately useful\n3. Include type hints where applicable\n4. Use professional, clear language\n5. Avoid redundancy\n6. Return ONLY the documentation block without any code before/after\n\nReturn the complete documentation block in the appropriate format:",
    
    "advancedOptions": {
      "temperature": 0.2,
      "topP": 0.9,
      "maxTokens": 1500
    }
  },
  
  "outputFormat": {
    "type": "text",
    
    "schema": {
      "type": "object",
      "properties": {
        "documentation": {
          "type": "string",
          "description": "The generated documentation block (docstring/comment)"
        },
        "language": {
          "type": "string",
          "description": "The programming language"
        },
        "style": {
          "type": "string",
          "description": "Documentation style used"
        },
        "sections": {
          "type": "object",
          "properties": {
            "summary": { "type": "string" },
            "args": { "type": "array", "items": { "type": "string" } },
            "returns": { "type": "string" },
            "raises": { "type": "array", "items": { "type": "string" } },
            "examples": { "type": "string" }
          }
        }
      },
      "required": [
        "documentation",
        "language",
        "style"
      ]
    }
  },
  
  "validation": {
    "timeout": 25,
    "maxRetries": 2,
    "caching": {
      "enabled": true,
      "ttl": 7200
    },
    "rateLimit": {
      "requestsPerMinute": 40,
      "requestsPerHour": 1200
    },
    "costControl": {
      "maxTokensPerRequest": 1500,
      "estimatedCostPerRequest": 0.012
    }
  }
}
```

---

## 拡張テンプレート変数の生成

スキル内で動的に生成される変数：

```python
# スキル内部で生成される補助変数

# includeSection_summary
if includeSummary:
    includeSection_summary = "- Summary/Description: A brief 1-3 sentence description"
else:
    includeSection_summary = ""

# includeSection_args
if includeArgs:
    includeSection_args = "- Arguments/Parameters: Description of each argument with types"
else:
    includeSection_args = ""

# ... 同様に他のセクションも生成
```

---

## 使用例

### 例1: Python 関数のドキュメント（Google Style）

```json
リクエスト：
{
  "skill": "generate-documentation",
  "parameters": {
    "code_element": "def calculate_factorial(n: int) -> int:",
    "language": "python",
    "docstyle": "google",
    "detailLevel": "standard"
  }
}

レスポンス：
{
  "documentation": "\"\"\"Calculate the factorial of a non-negative integer.\n\n    Args:\n        n: A non-negative integer.\n\n    Returns:\n        The factorial of n.\n\n    Raises:\n        ValueError: If n is negative.\n\n    Examples:\n        >>> calculate_factorial(5)\n        120\n        >>> calculate_factorial(0)\n        1\n    \"\"\"",
  "language": "python",
  "style": "google",
  "sections": {
    "summary": "Calculate the factorial of a non-negative integer.",
    "args": ["n: A non-negative integer."],
    "returns": "The factorial of n.",
    "raises": ["ValueError: If n is negative."],
    "examples": ">>> calculate_factorial(5)\n120\n>>> calculate_factorial(0)\n1"
  }
}
```

### 例2: JavaScript 関数のドキュメント（JSDoc）

```json
リクエスト：
{
  "skill": "generate-documentation",
  "parameters": {
    "code_element": "async function fetchUserData(userId, options = {}) {",
    "language": "javascript",
    "docstyle": "jsdoc",
    "detailLevel": "detailed",
    "includeExamples": true
  }
}

レスポンス：
{
  "documentation": "/**\n * Fetches user data from the server asynchronously.\n * Retrieves comprehensive user information including profile, preferences, and settings.\n *\n * @async\n * @function fetchUserData\n * @param {number} userId - The unique identifier of the user to fetch\n * @param {Object} [options={}] - Optional configuration object\n * @param {boolean} [options.includePreferences=false] - Whether to include user preferences\n * @param {boolean} [options.includeSettings=false] - Whether to include user settings\n * @param {number} [options.timeout=5000] - Request timeout in milliseconds\n *\n * @returns {Promise<Object>} A promise that resolves to an object containing:\n *   - {number} id - User ID\n *   - {string} name - User's full name\n *   - {string} email - User's email address\n *   - {Object} [preferences] - User preferences (if requested)\n *   - {Object} [settings] - User settings (if requested)\n *\n * @throws {Error} If userId is not a valid number\n * @throws {NetworkError} If the network request fails\n * @throws {TimeoutError} If the request exceeds the timeout duration\n *\n * @example\n * // Basic usage\n * const user = await fetchUserData(123);\n * console.log(user.name);\n *\n * @example\n * // With options\n * const user = await fetchUserData(123, {\n *   includePreferences: true,\n *   timeout: 10000\n * });\n */",
  "language": "javascript",
  "style": "jsdoc"
}
```

### 例3: Java クラスのドキュメント（JavaDoc）

```json
リクエスト：
{
  "skill": "generate-documentation",
  "parameters": {
    "code_element": "public class UserAuthenticationService {",
    "language": "java",
    "docstyle": "javadoc",
    "detailLevel": "detailed"
  }
}

レスポンス：
{
  "documentation": "/**\n * Service class for handling user authentication and authorization.\n * \n * This class provides methods for user login, token validation, and permission checking.\n * It handles both basic authentication and OAuth2 flows.\n * \n * <p>Thread-safe and designed for use in concurrent environments.\n * \n * @author Development Team\n * @version 1.0\n * @since 2026-03-07\n * \n * @see AuthToken\n * @see UserRepository\n * @see PermissionChecker\n * \n * @example\n * UserAuthenticationService authService = new UserAuthenticationService();\n * AuthToken token = authService.authenticate(username, password);\n * if (authService.isTokenValid(token)) {\n *     // Proceed with authenticated request\n * }\n */",
  "language": "java",
  "style": "javadoc"
}
```

---

## カスタマイズガイド

### カスタマイズ1: スタイルガイドの詳細化

```json
// prompt のテンプレートを言語・スタイル別に最適化

for Python + Google Style:
"Follow Google's Python style guide for docstrings:
- Use triple double quotes
- Start with a summary line ending with period
- Use Args:, Returns:, Raises:, Examples: sections
- Type hints in the function signature, not in docstring"

for JavaScript + JSDoc:
"Follow JSDoc 3 standards:
- Use /** */ format
- Use @param, @returns, @throws, @example tags
- Include type information in curly braces {type}
- Use @async tag for async functions"
```

### カスタマイズ2: エクスポート フォーマット

```json
// レスポンス形式をカスタマイズ

// Option 1: ドキュメント文字列のみ（シンプル）
{
  "documentation": "\"\"\"...\"\"\""
}

// Option 2: セクション分割（詳細）
{
  "documentation": "\"\"\"...\"\"\""
  "sections": {
    "summary": "...",
    "args": [...],
    "returns": "..."
  }
}

// Option 3: 埋め込みコード形式（実装例）
{
  "code_with_documentation": "def func():\n    \"\"\"...\"\"\"\n    pass"
}
```

### カスタマイズ3:言語別ドキュメント生成

言語によって自動でスタイルを選択：

```json
language_style_mapping: {
  "python": ["google", "numpy", "sphinx"],
  "javascript": ["jsdoc"],
  "typescript": ["jsdoc"],
  "java": ["javadoc"],
  "go": ["godoc"]
}
```

---

## 実装技法： includeSection 変数の出力

```
こちらはサーバーサイドで実装される機能のため、
スキル定義ファイルには含まれませんが、
実装時は以下のロジックが必要です：

テンプレート変数の動的生成：

def generate_prompt(parameters):
    include_sections = []
    
    if parameters['includeSummary']:
        include_sections.append("- Summary/Description")
    
    if parameters['includeArgs']:
        include_sections.append("- Arguments/Parameters")
    
    if parameters['includeReturns']:
        include_sections.append("- Return value/type")
    
    if parameters['includeRaises']:
        include_sections.append("- Exceptions/Errors")
    
    if parameters['includeExamples']:
        include_sections.append("- Usage examples")
    
    sections_text = "\n".join(include_sections)
    
    # テンプレート内の {includeSection_*} を置換
    template = template.replace("{includeSection_text}", sections_text)
    
    return template
```

---

## トラブルシューティング

### 問題1: ドキュメンテーションスタイルが混在

**症状：** Google Style を指定したはずなのに、他のスタイルが混在している

**原因：** プロンプトの指示が不明確

**修正：**

```json
"prompt": {
  "template": "...IMPORTANT: Use ONLY {docstyle} style. No other styles. If docstyle is 'google', use ONLY Google style docstring format. If 'jsdoc', use ONLY JSDoc format..."
}
```

### 問題2: 型情報が不正確

**症状：** 戻り値の型が `Any` や曖昧な説明になっている

**原因：** 入力コードに型ヒントがない

**修正：**

```json
"code_element": "def process(data: dict, timeout: int = 30) -> Optional[Result]:",
// 型ヒントを含めることで、より正確なドキュメント生成が可能
```

### 問題3: 生成が遅い

**症状：** detailLevel を "detailed" にするとタイムアウトが頻繁に発生

**修正：**

```json
"validation": {
  "timeout": 35,  // 25から35に増加
  "maxTokens": 2000  // トークン上限を増加
}
```

---

## テストケース

### テストケース1: 単純な関数（Python）

```bash
入力：
{
  "code_element": "def add(a, b):",
  "language": "python",
  "docstyle": "google"
}

期待される出力：
✓ triple double quotes で囲まれている
✓ Args: セクションを含む
✓ Returns: セクションを含む
✓ 言語は "python"
```

### テストケース2: 複雑なクラス（Java）

```bash
入力：
{
  "code_element": "public class DatabaseConnection implements AutoCloseable {",
  "language": "java",
  "docstyle": "javadoc",
  "detailLevel": "detailed"
}

期待される出力：
✓ JavaDoc 形式（/** */ で囲まれた）
✓ @since, @author タグを含む
✓ @see タグで関連クラスを参照している
```

### テストケース3: モダンな JavaScript（JSDoc）

```bash
入力：
{
  "code_element": "async function* streamData(url, options = {}) {",
  "language": "javascript",
  "docstyle": "jsdoc"
}

期待される出力：
✓ @async タグを含む
✓ @generator または @yields タグを含む
✓ @param で options オブジェクトを説明している
```

---

## 実装チェックリスト

```
□ スキル定義ファイルが有効な JSON か確認
□ すべての docstyle（google, numpy, jsdoc等）でテスト
□ 複数の言語でテスト
□ detailLevel（brief, standard, detailed）でそれぞれテスト
□ includeSummary, includeArgs等の boolean オプションでテスト
□ 複雑なシグネチャ（デフォルト値、可変長引数等）をテスト
□ ジェネリック型（Java の List<String> など）に対応しているか確認
□ 非同期関数（async/await）に正しくタグを付けているか確認
□ ドキュメント出力がコードに貼り付け可能か確認
□ リポジトリに登録、ドキュメント完備
```

---

## 実装のバリエーション

### マルチステップワークフロー：コード + ドキュメント生成

このスキルと Part 3-3 のコード品質分析スキルを組み合わせ：

```
ワークフロー：
1. code-quality-analyze スキルで品質分析
2. 出力から改善提案を抽出
3. コードを改善（ユーザーが実施）
4. generate-documentation スキルで改善後のコードをドキュメント化

結果：
- 品質が良く
- 十分にドキュメント化されたコード
```

---

## 次へ進む

→ [Part 3-5: サンプルスキル #3 - テスト生成](05-sample-test-generation.md)

テスト生成スキルは、さらに複雑で実用的な例として、
複数の出力ファイル、複数のテストフレームワーク対応を示します。
