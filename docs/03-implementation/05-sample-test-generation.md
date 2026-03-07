# Part 3-5: サンプルスキル #3 - テスト生成【応用的なスキル】

このセクションでは、**関数・メソッドのユニットテストコードを自動生成するスキル** を SKILL.md フォーマットで実装します。

難度は最も高く、複数のテストフレームワーク対応、複数ケース生成を含みます。

---

## スキル概要

```
スキル名：generate-unit-tests
目的：ユニットテストコードを自動生成
難度：★★★★☆（上級）
実装時間：1～2時間
対応言語：Python, JavaScript/TypeScript, Java, Go
対応フレームワーク：pytest, unittest, Jest, Mocha, JUnit, Go testing
特徴：正常系・異常系・エッジケースをカバー
推奨形式：SKILL.md
```

---

## SKILL.md フォーマット（推奨）

### ファイル：`.github/skills/test-generator.md`

```markdown
---
id: generate-unit-tests
version: 1.0.0
name: ユニットテスト自動生成
description: 関数・メソッドのユニットテストコードを複数のテストフレームワーク形式で自動生成します
author: QA and Testing Team
tags: [testing, unit-test, pytest, jest, junit, quality-assurance]
category: testing
---

# ユニットテスト自動生成スキル

## 概要

このスキルは以下のテスト種別をカバーしたユニットテストを自動生成します：

- **正常系テスト**: 期待される入力に対する結果の検証
- **境界値テスト**: 最小値・最大値・境界条件の検証
- **異常系テスト**: エラーハンドリング、例外発生の検証
- **エッジケーステスト**: null、空配列など特殊な入力の検証

対応するテストフレームワーク：
- **Python**: pytest、unittest
- **JavaScript/TypeScript**: Jest、Mocha + Chai
- **Java**: JUnit 4/5
- **Go**: Go testing

## 使い方

1. 関数またはメソッド定義を選択
2. Copilot に「ユニットテスト自動生成スキルを実行」と指示
3. テストコードが選択したフレームワーク形式で生成されます

## パラメータ

### codeSnippet (必須)
テスト対象のコード（関数またはクラスメソッド）
- 5～200 行まで対応

### language (必須)
ソースコード言語
- `python`
- `javascript`
- `typescript`
- `java`
- `go`

### testFramework (必須)
使用するテストフレームワーク
- Python: `pytest` / `unittest`
- JS/TS: `jest` / `mocha`
- Java: `junit4` / `junit5`
- Go: `testing`

### coverageTarget (オプション)
テストカバレッジ目標（%）
- デフォルト: `80`
- 範囲: 50～100

### includeDocumentation (オプション)
テストコード内にコメント・説明を含めるか
- `true`: 含める（学習向け）
- `false`: 含めない（本番向け）

デフォルト: `true`

## 出力フォーマット

```json
{
  "testCode": "...",
  "framework": "pytest|jest|junit|testing",
  "language": "...",
  "testCases": [
    {
      "name": "test_normal_case_1",
      "type": "normal|boundary|error|edge",
      "description": "..." 
    }
  ],
  "estimatedCoverage": 0.85,
  "runInstructions": "pytest test_function.py -v",
  "suggestions": [
    "統合テストの追加を検討してください",
    "パフォーマンステストの追加をお勧めします"
  ]
}
```

## 実装例

### Example 1: Python 関数（pytest）

入力コード:
```python
def divide(a, b):
    if b == 0:
        raise ValueError("0で除算することはできません")
    return a / b
```

生成されるテストコード:
```python
import pytest
from math_utils import divide

class TestDivide:
    """divide 関数のテストスイート"""
    
    def test_normal_case_positive_numbers(self):
        """正常系: 正の数同士の除算"""
        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5
    
    def test_normal_case_negative_numbers(self):
        """正常系: 負の数を含む除算"""
        assert divide(-10, 2) == -5.0
        assert divide(10, -2) == -5.0
        assert divide(-10, -2) == 5.0
    
    def test_boundary_case_zero_numerator(self):
        """境界値: 分子が 0"""
        assert divide(0, 5) == 0.0
    
    def test_boundary_case_small_denominator(self):
        """境界値: 分母が 1"""
        assert divide(42, 1) == 42.0
    
    def test_error_case_zero_denominator(self):
        """異常系: 分母が 0（例外発生）"""
        with pytest.raises(ValueError):
            divide(10, 0)
    
    def test_error_case_invalid_type_numerator(self):
        """異常系: 分子が数値でない"""
        with pytest.raises(TypeError):
            divide("10", 2)
    
    def test_edge_case_float_division(self):
        """エッジケース: 浮動小数点演算"""
        result = divide(1, 3)
        assert abs(result - 0.333333) < 0.0001
```

### Example 2: JavaScript 関数（Jest）

入力コード:
```javascript
function fetchUserData(userId) {
    if (!userId) {
        throw new Error("User ID is required");
    }
    return api.get(`/users/${userId}`);
}
```

生成されるテストコード:
```javascript
import { fetchUserData } from './userService';
import * as api from './api';

jest.mock('./api');

describe('fetchUserData', () => {
    afterEach(() => {
        jest.clearAllMocks();
    });
    
    test('正常系: 有効なユーザーIDでデータを取得', async () => {
        const userData = { id: '123', name: 'John Doe' };
        api.get.mockResolvedValue(userData);
        
        const result = await fetchUserData('123');
        
        expect(result).toEqual(userData);
        expect(api.get).toHaveBeenCalledWith('/users/123');
    });
    
    test('異常系: ユーザーID未指定で例外発生', () => {
        expect(() => fetchUserData(null)).toThrow('User ID is required');
        expect(() => fetchUserData('')).toThrow('User ID is required');
    });
    
    test('異常系: API呼び出し失敗時のエラーハンドリング', async () => {
        api.get.mockRejectedValue(new Error('API Error'));
        
        await expect(fetchUserData('123')).rejects.toThrow('API Error');
    });
    
    test('境界値: 最小限のユーザーIDでリクエスト', async () => {
        api.get.mockResolvedValue({});
        
        await fetchUserData('a');
        
        expect(api.get).toHaveBeenCalledWith('/users/a');
    });
});
```

---

## JSON フォーマット（参考：内部管理向け）

```json
{
  "id": "generate-unit-tests",
  "version": "1.0.0",
  "name": "ユニットテスト自動生成",
  "description": "関数・メソッドのユニットテストコードを自動生成するスキル。複数のテストフレームワークに対応し、正常系・異常系・エッジケースを包括的にカバーしたテストを生成します。",
  
  "metadata": {
    "author": "QA/Testing Team",
    "authorEmail": "qa@example.com",
    "created": "2026-03-07",
    "lastUpdated": "2026-03-07",
    "category": "testing",
    "subcategory": "unit-testing",
    "tags": [
      "testing",
      "unit-test",
      "pytest",
      "jest",
      "junit",
      "python",
      "javascript",
      "typescript",
      "java",
      "go"
    ],
    "documentation": "https://docs.example.com/skills/generate-unit-tests",
    "license": "MIT"
  },
  
  "parameters": {
    "function_signature": {
      "type": "string",
      "description": "テスト対象の関数・メソッドの完全なシグネチャと通常は関数本体を含む（またはシグネチャのみでも可）",
      "required": true,
      "minLength": 20,
      "maxLength": 5000,
      "example": "def merge_sorted_lists(list1: List[int], list2: List[int]) -> List[int]:"
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
      ]
    },
    
    "testFramework": {
      "type": "string",
      "description": "テストフレームワーク（言語に応じて選択）",
      "enum": [
        "pytest",
        "unittest",
        "jest",
        "mocha",
        "chai",
        "junit",
        "testng",
        "gotest"
      ],
      "default": "pytest"
    },
    
    "coverage": {
      "type": "string",
      "description": "テストカバレッジレベル",
      "enum": [
        "basic",
        "standard",
        "comprehensive"
      ],
      "default": "standard",
      "example": "comprehensive"
    },
    
    "includeNormalCases": {
      "type": "boolean",
      "description": "正常系テストを含める",
      "default": true
    },
    
    "includeEdgeCases": {
      "type": "boolean",
      "description": "エッジケーステストを含める",
      "default": true
    },
    
    "includeErrorCases": {
      "type": "boolean",
      "description": "エラーケース・例外テストを含める",
      "default": true
    },
    
    "mockExternalDependencies": {
      "type": "boolean",
      "description": "外部依存関係をモックする",
      "default": true
    },
    
    "includePerformanceTests": {
      "type": "boolean",
      "description": "パフォーマンステストを含める（オプション）",
      "default": false
    }
  },
  
  "prompt": {
    "system": "You are an expert quality assurance engineer and test architect. Your task is to generate comprehensive, professional unit tests that cover normal cases, edge cases, and error scenarios. Tests should be clear, maintainable, and follow industry best practices. Use appropriate assertions and test structures for the specified framework.",
    
    "template": "Generate professional unit tests for the following {language} function.\n\nFunction to test:\n{function_signature}\n\nTest framework: {testFramework}\nCoverage level: {coverage}\n\nInclude:\n{coverageInstructions}\n\nRequirements:\n1. Generate {coverage} coverage tests\n2. Follow {testFramework} conventions and best practices\n3. Use descriptive test names (test_<scenario> format)\n4. Include setup/teardown if needed\n5. Add comments explaining complex test logic\n6. Group related tests in test classes/suites\n7. Use appropriate assertions for {language}\n{mockingInstructions}\n\n{coverageDetails}\n\nGenerate the complete test file content in {language} syntax:",
    
    "advancedOptions": {
      "temperature": 0.3,
      "topP": 0.9,
      "maxTokens": 3000
    }
  },
  
  "outputFormat": {
    "type": "object",
    
    "schema": {
      "type": "object",
      "properties": {
        "test_code": {
          "type": "string",
          "description": "The generated test code (complete and runnable)"
        },
        "language": {
          "type": "string",
          "description": "Programming language"
        },
        "framework": {
          "type": "string",
          "description": "Test framework used"
        },
        "test_cases": {
          "type": "array",
          "description": "List of generated test cases",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "description": "Test case name"
              },
              "type": {
                "type": "string",
                "enum": ["normal", "edge_case", "error_case", "performance"],
                "description": "Type of test"
              },
              "description": {
                "type": "string",
                "description": "What this test validates"
              }
            }
          }
        },
        "imports": {
          "type": "array",
          "description": "Required imports/dependencies",
          "items": { "type": "string" }
        },
        "setup_instructions": {
          "type": "string",
          "description": "Setup instructions (dependencies, configs, etc.)"
        },
        "run_instructions": {
          "type": "string",
          "description": "How to run the tests"
        }
      },
      "required": [
        "test_code",
        "language",
        "framework"
      ]
    },
    
    "examples": [
      {
        "test_code": "import pytest\nfrom typing import List\n\n\nclass TestMergeSortedLists:\n    \"\"\"Test suite for merge_sorted_lists function.\"\"\"\n    \n    # Normal cases\n    def test_merge_two_non_empty_lists(self):\n        \"\"\"Test merging two non-empty sorted lists.\"\"\"\n        result = merge_sorted_lists([1, 3, 5], [2, 4, 6])\n        assert result == [1, 2, 3, 4, 5, 6]\n    \n    # Edge cases\n    def test_merge_with_empty_first_list(self):\n        \"\"\"Test merging when first list is empty.\"\"\"\n        result = merge_sorted_lists([], [1, 2, 3])\n        assert result == [1, 2, 3]\n    \n    def test_merge_with_empty_second_list(self):\n        \"\"\"Test merging when second list is empty.\"\"\"\n        result = merge_sorted_lists([1, 2, 3], [])\n        assert result == [1, 2, 3]\n    \n    def test_merge_both_empty_lists(self):\n        \"\"\"Test merging two empty lists.\"\"\"\n        result = merge_sorted_lists([], [])\n        assert result == []\n    \n    # Error cases\n    def test_merge_with_unsorted_input(self):\n        \"\"\"Test behavior with unsorted input lists.\"\"\"\n        # Should still produce sorted result if function handles it\n        result = merge_sorted_lists([3, 1], [4, 2])\n        # Verify result is sorted\n        assert result == sorted(result)",
        "language": "python",
        "framework": "pytest",
        "test_cases": [
          {
            "name": "test_merge_two_non_empty_lists",
            "type": "normal",
            "description": "Merge two non-empty sorted lists"
          },
          {
            "name": "test_merge_with_empty_first_list",
            "type": "edge_case",
            "description": "Handle empty first list"
          },
          {
            "name": "test_merge_with_empty_second_list",
            "type": "edge_case",
            "description": "Handle empty second list"
          },
          {
            "name": "test_merge_both_empty_lists",
            "type": "edge_case",
            "description": "Handle both lists empty"
          },
          {
            "name": "test_merge_with_unsorted_input",
            "type": "error_case",
            "description": "Handle unsorted input"
          }
        ],
        "imports": [
          "pytest",
          "from typing import List"
        ],
        "run_instructions": "Run with: pytest test_merge_sorted_lists.py -v"
      }
    ]
  },
  
  "validation": {
    "timeout": 40,
    "maxRetries": 2,
    "caching": {
      "enabled": true,
      "ttl": 7200
    },
    "rateLimit": {
      "requestsPerMinute": 20,
      "requestsPerHour": 600
    },
    "costControl": {
      "maxTokensPerRequest": 3000,
      "estimatedCostPerRequest": 0.025
    }
  }
}
```

---

## 補助説明テンプレート変数

スキル内部で生成される動的な説明文：

```python
def generate_coverage_instructions(coverage_level):
    if coverage_level == "basic":
        return "- Happy path (normal operation)\n- At least 1 edge case\n- Essential error cases"
    elif coverage_level == "standard":
        return "- Multiple normal scenario paths\n- All edge cases (empty, null, boundary values)\n- All specified error conditions"
    elif coverage_level == "comprehensive":
        return "- All normal scenario variations\n- All edge cases and boundary conditions\n- All error types and recovery paths\n- Integration with related functions if applicable"

def generate_mocking_instructions(mock_enabled):
    if mock_enabled:
        return "Mock external dependencies using appropriate mocking library."
    else:
        return "Assume all dependencies are available."

def generate_coverage_details(coverage_level):
    details = {
        "basic": "Aim for 60-70% code coverage",
        "standard": "Aim for 80-85% code coverage",
        "comprehensive": "Aim for 95%+ code coverage"
    }
    return details.get(coverage_level, "")
```

---

## 使用例

### 例1: Python (pytest) - 標準的なテスト生成

```json
リクエスト：
{
  "skill": "generate-unit-tests",
  "parameters": {
    "function_signature": "def validate_email(email: str) -> bool:",
    "language": "python",
    "testFramework": "pytest",
    "coverage": "standard",
    "includeErrorCases": true
  }
}

レスポンス（一部）：
{
  "test_code": "import pytest\n\nclass TestValidateEmail:\n    \"\"\"Test suite for validate_email function.\"\"\"\n    \n    # Normal cases\n    def test_valid_email_simple(self):\n        \"\"\"Test with a simple valid email.\"\"\"\n        assert validate_email('user@example.com') == True\n    \n    def test_valid_email_with_subdomain(self):\n        \"\"\"Test with valid email containing subdomain.\"\"\"\n        assert validate_email('user@mail.example.co.uk') == True\n    \n    # Edge cases\n    def test_empty_string(self):\n        \"\"\"Test with empty string.\"\"\"\n        assert validate_email('') == False\n    \n    def test_email_without_domain(self):\n        \"\"\"Test email with no domain.\"\"\"\n        assert validate_email('user@') == False\n    \n    def test_email_without_local_part(self):\n        \"\"\"Test email with no local part.\"\"\"\n        assert validate_email('@example.com') == False\n    \n    # Error cases\n    def test_none_input(self):\n        \"\"\"Test with None input.\"\"\"\n        with pytest.raises(TypeError):\n            validate_email(None)\n    \n    def test_numeric_input(self):\n        \"\"\"Test with numeric input.\"\"\"\n        with pytest.raises(TypeError):\n            validate_email(12345)",
  "language": "python",
  "framework": "pytest",
  "test_cases": [
    {"name": "test_valid_email_simple", "type": "normal", "description": "Valid simple email"},
    {"name": "test_valid_email_with_subdomain", "type": "normal", "description": "Valid email with subdomain"},
    {"name": "test_empty_string", "type": "edge_case", "description": "Empty string input"},
    {"name": "test_email_without_domain", "type": "edge_case", "description": "Missing domain"},
    {"name": "test_email_without_local_part", "type": "edge_case", "description": "Missing local part"},
    {"name": "test_none_input", "type": "error_case", "description": "None input"},
    {"name": "test_numeric_input", "type": "error_case", "description": "Non-string input"}
  ],
  "imports": ["pytest"],
  "run_instructions": "pytest test_validate_email.py -v"
}
```

### 例2: JavaScript (Jest) - 包括的テスト生成

```json
リクエスト：
{
  "skill": "generate-unit-tests",
  "parameters": {
    "function_signature": "async function fetchUser(userId) { ... }",
    "language": "javascript",
    "testFramework": "jest",
    "coverage": "comprehensive",
    "mockExternalDependencies": true,
    "includePerformanceTests": true
  }
}

レスポンス（部分）：
{
  "test_code": "jest jest.mock('./api');\nconst { fetchUser } = require('./userService');\nconst api = require('./api');\n\ndescribe('fetchUser', () => {\n  beforeEach(() => {\n    jest.clearAllMocks();\n  });\n\n  describe('Normal cases', () => {\n    test('should fetch user data successfully', async () => {\n      const mockUser = { id: 1, name: 'John Doe' };\n      api.get.mockResolvedValue(mockUser);\n\n      const result = await fetchUser(1);\n\n      expect(result).toEqual(mockUser);\n      expect(api.get).toHaveBeenCalledWith('/users/1');\n    });\n  });\n\n  describe('Edge cases', () => {\n    test('should handle userId 0', async () => {\n      const mockUser = { id: 0, name: 'System User' };\n      api.get.mockResolvedValue(mockUser);\n\n      const result = await fetchUser(0);\n\n      expect(result).toEqual(mockUser);\n    });\n\n    test('should handle very large userId', async () => {\n      const largeId = Number.MAX_SAFE_INTEGER;\n      api.get.mockResolvedValue({ id: largeId });\n\n      const result = await fetchUser(largeId);\n\n      expect(api.get).toHaveBeenCalledWith(`/users/${largeId}`);\n    });\n  });\n\n  describe('Error cases', () => {\n    test('should throw on API failure', async () => {\n      api.get.mockRejectedValue(new Error('API Error'));\n\n      await expect(fetchUser(1)).rejects.toThrow('API Error');\n    });\n\n    test('should handle network timeout', async () => {\n      api.get.mockRejectedValue(new Error('TIMEOUT'));\n\n      await expect(fetchUser(1)).rejects.toThrow('TIMEOUT');\n    });\n  });\n\n  describe('Performance', () => {\n    test('should complete within 1 second', async () => {\n      api.get.mockResolvedValue({ id: 1 });\n\n      const startTime = Date.now();\n      await fetchUser(1);\n      const duration = Date.now() - startTime;\n\n      expect(duration).toBeLessThan(1000);\n    });\n  });\n});",
  "language": "javascript",
  "framework": "jest",
  "imports": ["jest", "require('./api')"]
}
```

### 例3: Java (JUnit) - エンタープライズグレード

```json
リクエスト：
{
  "skill": "generate-unit-tests",
  "parameters": {
    "function_signature": "public class UserService { public User getUser(String id) throws UserNotFoundException { ... } }",
    "language": "java",
    "testFramework": "junit",
    "coverage": "comprehensive"
  }
}

レスポンス（部分）：
{
  "test_code": "import org.junit.jupiter.api.Test;\nimport org.junit.jupiter.api.BeforeEach;\nimport static org.junit.jupiter.api.Assertions.*;\nimport static org.mockito.Mockito.*;\n\nclass UserServiceTest {\n    private UserService userService;\n    private UserRepository mockRepository;\n\n    @BeforeEach\n    void setUp() {\n        mockRepository = mock(UserRepository.class);\n        userService = new UserService(mockRepository);\n    }\n\n    @Test\n    void testGetUserWithValidId() throws UserNotFoundException {\n        // Arrange\n        String userId = \"123\";\n        User expectedUser = new User(\"123\", \"John Doe\");\n        when(mockRepository.findById(userId)).thenReturn(expectedUser);\n\n        // Act\n        User result = userService.getUser(userId);\n\n        // Assert\n        assertEquals(expectedUser, result);\n        verify(mockRepository).findById(userId);\n    }\n\n    @Test\n    void testGetUserWithNullId() {\n        assertThrows(IllegalArgumentException.class, () -> {\n            userService.getUser(null);\n        });\n    }\n\n    @Test\n    void testGetUserWithInvalidId() throws UserNotFoundException {\n        when(mockRepository.findById(\"invalid\")).thenThrow(new UserNotFoundException());\n\n        assertThrows(UserNotFoundException.class, () -> {\n            userService.getUser(\"invalid\");\n        });\n    }\n}",
  "language": "java",
  "framework": "junit"
}
```

---

## 高度なカスタマイズ

### カスタマイズ1: テストカバレッジの詳細設定

```json
// coverageLevel を拡張して、より細かい制御を可能にする例

"coverageLevel": "custom",
"customCoverage": {
  "normalCases": 3,      // 正常系テストを最低3つ生成
  "edgeCases": 5,        // エッジケース最低5つ
  "errorCases": 3,       // エラーケース最低3つ
  "targetCoverage": 90   // コードカバレッジ 90% を目指す
}
```

### カスタマイズ2: テストデータ生成戦略

```json
"testDataGeneration": {
  "strategy": "use_fixtures",  // or "use_factories", "use_builders"
  "fixturesPath": "./tests/fixtures",
  "generateFactories": true,
  "generateBuilders": true
}
```

### カスタマイズ3: CI/CD 統合

```json
"cicdIntegration": {
  "generateGitHubActions": true,
  "generateGitLabCI": true,
  "generateJenkins": false,
  "includeCodeCoverageBadge": true
}
```

---

## トラブルシューティング

### 問題1: 生成されたテストが実行できない

**原因：** インポートやモック設定が不正

**修正：**

```json
"setup_instructions": "Run: pip install pytest pytest-mock\n npm install jest @testing-library/react"
```

### 問題2: エッジケースが不足

**原因：** 関数シグネチャから推測できない領域域がある

**修正：** function_signature に追加情報を含める

```json
"function_signature": "def process_payment(amount: float, currency: str, retry_count: int = 3) -> bool:\n    '''Process payment. Raises InsufficientFunds, NetworkError.'''"
```

### 問題3: 外部依存のモック化が複雑

**原因：** 多層の依存関係

**修正：**

```json
"mockExternalDependencies": true,
"mockingStrategy": "use_factories"  // より高度なモック戦略を指定
```

---

## テストコード品質イ評価チェックリスト

生成されたテストを評価して、品質が十分か確認：

```
✓ 明確な Arrange-Act-Assert パターン
✓ 各テストが1つの動作のみを検証
✓ テスト名が何をテストしているか明確
✓ 正常系、エッジケース、エラーケースの均衡
✓ 外部依存がモックされている
✓ 重複するテストがない
✓ 実行が速い（各テスト < 100ms）
✓ ランダムな順序で実行しても成功
✓ セットアップ/クリーンアップが適切
✓ アサーション が具体的（assertFalse() より assertEqual()）
```

---

## 実装チェックリスト

```
□ スキル定義ファイルが有効な JSON か確認
□ 全言語でテスト（Python, JS, Java, Go）
□ 全テストフレームワークでテスト（pytest, jest, junit等）
□ 全 coverage レベルでテスト（basic, standard, comprehensive）
□ 各テストが実際に実行可能か確認
□ モック設定が正しいか確認
□ エラーハンドリングをテスト
□ パフォーマンステストが実現可能か確認
□ ドキュメント完備（使用方法、セットアップ手順）
□ リポジトリに登録
```

---

## Part 3 の総括

```
実装した3つのサンプルスキル：

1. 【初級】analyze-code-quality
   - シンプルな入力・出力
   - 単一の出力形式（JSON）
   - 分析的なタスク

2. 【中級】generate-documentation
   - 複数のドキュメント形式対応
   - テキスト出力
   - セクション分割

3. 【上級】generate-unit-tests
   - 複数のテストフレームワーク対応
   - 複雑なテンプレート展開
   - 多段階の出力
   - エラーハンドリングが豊富

これらのパターンを学ぶことで、
あらゆるスキルを設計・実装できるようになります。
```

---

## 次へ進む

→ [Part 4: 活用編](../04-advanced/01-team-sharing.md) - チーム内でのスキル共有と運用

Part 3 の実装編が完了しました。
次は Part 4 で、これらのスキルをチーム全体で活用する方法を学びます。
