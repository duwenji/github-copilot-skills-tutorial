---
name: test-generator
description: 関数・メソッドのユニットテストコードを自動生成するスキル。複数のテストフレームワークに対応し、正常系・異常系・エッジケースを包括的にカバーしたテストを生成
license: MIT
---

# Unit Test Generator

## 概要

このスキルは、関数やメソッドのユニットテストコードを自動生成します。正常系、異常系、エッジケースを包括的にカバーし、複数のテストフレームワークに対応しています。

## 対応言語

- Python
- JavaScript
- TypeScript
- Java
- Go

## 対応テストフレームワーク

| フレームワーク | 言語 | 説明 |
|--------|------|------|
| pytest | Python | Python標準のテストフレームワーク |
| unittest | Python | Python組み込みのテストフレームワーク |
| jest | JavaScript/TypeScript | JavaScript/TypeScriptのテストフレームワーク |
| mocha + chai | JavaScript/TypeScript | JavaScript/TypeScriptのテストスイート |
| junit | Java | Javaの標準テストフレームワーク |
| testng | Java | Java向けの高度なテストフレームワーク |
| gotest | Go | Go言語組み込みのテストフレームワーク |

## 入力パラメータ

### 必須

| パラメータ | 型 | 説明 | 例 |
|---------|-----|------|-----|
| `function_signature` | string | テスト対象の関数・メソッドの完全なシグネチャと通常は関数本体 | `def merge_sorted_lists(list1: List[int], list2: List[int]) -> List[int]:` |
| `language` | string | プログラミング言語 | `python` |

### オプション

| パラメータ | 型 | デフォルト | 説明 |
|---------|-----|----------|------|
| `testFramework` | string | `pytest` | テストフレームワーク |
| `coverage` | string | `standard` | カバレッジレベル：`basic`, `standard`, `comprehensive` |
| `includeNormalCases` | boolean | `true` | 正常系テストを含める |
| `includeEdgeCases` | boolean | `true` | エッジケーステストを含める |
| `includeErrorCases` | boolean | `true` | エラーケース・例外テストを含める |
| `mockExternalDependencies` | boolean | `true` | 外部依存関係をモックする |
| `includePerformanceTests` | boolean | `false` | パフォーマンステストを含める |

## 使用例

### Python (pytest)

```
User: "このPython関数の包括的なユニットテストをpytestで生成してください"

function_signature: |
  def merge_sorted_lists(list1: List[int], list2: List[int]) -> List[int]:
      """2つのソート済みリストをmergeします"""
      result = []
      i = j = 0
      while i < len(list1) and j < len(list2):
          if list1[i] <= list2[j]:
              result.append(list1[i])
              i += 1
          else:
              result.append(list2[j])
              j += 1
      result.extend(list1[i:])
      result.extend(list2[j:])
      return result

language: python
testFramework: pytest
coverage: comprehensive
```

### TypeScript (Jest)

```
User: "このTypeScript関数の包括的なテストをJestで生成"

function_signature: |
  async function fetchUserWithRetry(
    userId: string, 
    maxRetries: number = 3
  ): Promise<User>

language: typescript
testFramework: jest
coverage: comprehensive
includePerformanceTests: true
```

## 出力形式

完全に実行可能なテストコードを返却します：

### Python (pytest) の例

```python
import pytest
from typing import List

def merge_sorted_lists(list1: List[int], list2: List[int]) -> List[int]:
    """実装コード..."""

class TestMergeSortedLists:
    """merge_sorted_lists関数のテストスイート"""
    
    def test_merge_normal_case(self):
        """正常系：2つのソート済みリストをマージ"""
        assert merge_sorted_lists([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
        assert merge_sorted_lists([1, 2], [3, 4]) == [1, 2, 3, 4]
    
    def test_merge_edge_case_empty_list(self):
        """エッジケース：空のリスト"""
        assert merge_sorted_lists([], [1, 2, 3]) == [1, 2, 3]
        assert merge_sorted_lists([1, 2, 3], []) == [1, 2, 3]
        assert merge_sorted_lists([], []) == []
    
    def test_merge_edge_case_single_element(self):
        """エッジケース：単一要素"""
        assert merge_sorted_lists([1], [2]) == [1, 2]
        assert merge_sorted_lists([2], [1]) == [1, 2]
    
    def test_merge_error_case_none(self):
        """エラーケース：Noneが渡された場合"""
        with pytest.raises(TypeError):
            merge_sorted_lists(None, [1, 2, 3])
    
    def test_merge_performance(self):
        """パフォーマンステスト：大規模リスト"""
        large_list1 = list(range(0, 10000, 2))
        large_list2 = list(range(1, 10000, 2))
        
        import time
        start = time.time()
        result = merge_sorted_lists(large_list1, large_list2)
        elapsed = time.time() - start
        
        assert len(result) == len(large_list1) + len(large_list2)
        assert elapsed < 0.1  # 100ms以内に完了
```

## テストケースの分類

### Normal Cases（正常系）
入力・出力が期待通りに動作するケース

### Edge Cases（エッジケース）
- 空の入力
- 単一要素
- 最小値・最大値
- 境界値

### Error Cases（エラーケース）
- Noneまたは無効な入力
- 型エラー
- 予期される例外

### Performance Tests（パフォーマンステスト）
- 大規模入力での実行時間
- メモリ使用量
- スケーラビリティ

## 実行オプション

| 設定 | 値 |
|------|-----|
| Temperature | 0.3（精度重視） |
| Top P | 0.9 |
| Max Tokens | 3000 |

## ベストプラクティス

- **テスト名**: `test_<機能>_<シナリオ>` フォーマット
- **Arrange-Act-Assert**: テストの構造を明確に
- **1テスト1アサーション**: 単一の検証に集中
- **モック**: 外部依存を適切に隔離
- **ドキュメント**: テストの意図をコメントで説明

