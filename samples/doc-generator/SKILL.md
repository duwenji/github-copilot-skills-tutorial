---
name: doc-generator
description: 関数・メソッド・クラスのドキュメンテーション（docstring）を自動生成するスキル。複数のドキュメンテーションスタイル（Google, NumPy, JSDoc等）に対応
license: MIT
---

# Documentation Generator

## 概要

このスキルは、コード要素のドキュメンテーションを自動生成します。複数のドキュメンテーションスタイルに対応し、関数やメソッド、クラスの用途を明確に説明するdocstringを生成します。

## 対応言語

- Python
- JavaScript
- TypeScript
- Java
- Go

## 対応ドキュメンテーションスタイル

| スタイル | 言語 | 説明 |
|---------|------|------|
| Google | Python | Google スタイルガイドのdocstring形式 |
| NumPy | Python | NumPy スタイルのdocstring形式 |
| Sphinx | Python | Sphinx互換のReStructuredText形式 |
| JSDoc | JavaScript/TypeScript | JavaScriptドキュメンテーション標準 |
| JavaDoc | Java | Javaドキュメンテーション標準 |
| GoDoc | Go | Go言語ドキュメンテーション標準 |

## 入力パラメータ

### 必須

| パラメータ | 型 | 説明 | 例 |
|---------|-----|------|-----|
| `code_element` | string | ドキュメント化する関数・メソッド・クラスの定義（署名を含む） | `def calculate_fibonacci(n: int, memo: dict = None) -> int:` |
| `language` | string | プログラミング言語 | `python` |

### オプション

| パラメータ | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `docstyle` | string | `google` | ドキュメンテーション形式 |
| `detailLevel` | string | `standard` | 詳細度：`brief`, `standard`, `detailed` |
| `includeSummary` | boolean | `true` | 1行概要を含める |
| `includeArgs` | boolean | `true` | 引数の説明を含める |
| `includeReturns` | boolean | `true` | 戻り値の説明を含める |
| `includeRaises` | boolean | `true` | 発生する例外の説明を含める |
| `includeExamples` | boolean | `true` | 使用例を含める |

## 使用例

### Python (Google スタイル)

```
User: "この関数のdocstringをGoogle形式で高詳細度で生成してください"

code_element: |
  def calculate_fibonacci(n: int, memo: dict = None) -> int:

language: python
docstyle: google
detailLevel: detailed
```

### JavaScript (JSDoc)

```
User: "このメソッドのJSDocコメントを自動生成"

code_element: |
  async fetchUserData(userId: string, options?: RequestOptions): Promise<User>

language: typescript
docstyle: jsdoc
detailLevel: standard
```

## 出力形式

Markdownテキストで、以下を含むdocstringを返却します：

```python
def calculate_fibonacci(n: int, memo: dict = None) -> int:
    """
    フィボナッチ数列のn番目の値を計算します。

    メモ化を使用した効率的な実装で、大きなn値でも
    高速に計算できます。

    Args:
        n: 計算するフィボナッチ数列の索引（0以上の整数）
        memo: 計算結果のキャッシュ用辞書（内部用）

    Returns:
        n番目のフィボナッチ数

    Raises:
        ValueError: n が負の値の場合
        TypeError: n が整数でない場合

    Example:
        >>> calculate_fibonacci(10)
        55
        >>> calculate_fibonacci(0)
        0
    """
```

## ドキュメンテーション内容

### Summary（1行概要）
機能を簡潔に説明

### Args（引数）
- パラメータ名
- 型
- 説明
- デフォルト値（がある場合）

### Returns（戻り値）
- 戻り値の型
- 戻り値の説明
- 戻り値の例

### Raises（例外）
- 発生する例外の型
- 発生する条件

### Examples（使用例）
- 複数の使用パターン
- 出力例
- 注意点

## 実行オプション

| 設定 | 値 |
|------|-----|
| Temperature | 0.2（精度重視） |
| Top P | 0.9 |
| Max Tokens | 1500 |

## スタイルガイド

- **言語**: プロフェッショナルで明確な説明
- **型ヒント**: 可能な限り型情報を含める
- **冗長性**: 避け、必要な情報に絞る
- **専門用語**: 開発者向けの正確な用語使用

