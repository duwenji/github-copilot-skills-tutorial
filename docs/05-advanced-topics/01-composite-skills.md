# Part 5「高度な活用」: 複合スキルと高度なパターン

複数のスキルを組み合わせてより強力な機能を実現する高度なパターンを学びます。

---

## Part 5-1: 複合スキル（Composite Skills）

### 複合スキルとは

複数の基本スキルを組み合わせて、より高度な処理を実現するスキル：

```
例：「コード品質向上パイプライン」

Input: コード
  ↓
[Skill 1] analyze-code-quality
  → 問題点抽出
  ↓
[Skill 2] generate-fixes
  → 修正コード提案
  ↓
[Skill 3] generate-unit-tests
  → テストコード生成
  ↓
Output: 修正済みコード + テスト

これらを順序立てて実行する複合スキル
```

### 複合スキル 例1: コード品質改善パイプライン

```json
{
  "id": "improve-code-quality-pipeline",
  "version": "1.0.0",
  "name": "コード品質改善パイプライン",
  "description": "コード分析→修正提案→テスト生成を一度に実行",
  
  "dependencies": [
    {"id": "analyze-code-quality", "version": ">=1.0.0", "required": true},
    {"id": "generate-fixes", "version": ">=1.0.0", "required": true},
    {"id": "generate-unit-tests", "version": ">=1.0.0", "required": true}
  ],
  
  "parameters": {
    "code": {
      "type": "string",
      "description": "改善対象のコード",
      "maxLength": 10000
    },
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "typescript", "java"],
      "required": true
    },
    "focusAreas": {
      "type": "array",
      "description": "重点改善領域",
      "items": {"type": "string"},
      "enum": ["readability", "performance", "security", "testability"]
    },
    "autoApply": {
      "type": "boolean",
      "description": "推奨修正を自動適用",
      "default": false
    }
  },
  
  "compositeDefinition": {
    "workflow": "sequential",  // sequential または parallel
    "steps": [
      {
        "id": "step1",
        "skill": "analyze-code-quality",
        "inputs": {
          "code": "${code}",
          "language": "${language}",
          "focusAreas": "${focusAreas}"
        },
        "outputs": ["analysis_result"]
      },
      {
        "id": "step2",
        "skill": "generate-fixes",
        "dependsOn": ["step1"],
        "inputs": {
          "code": "${code}",
          "analysis": "${step1.analysis_result}",
          "language": "${language}"
        },
        "outputs": ["fixed_code", "explanation"]
      },
      {
        "id": "step3",
        "skill": "generate-unit-tests",
        "dependsOn": ["step2"],
        "condition": "${autoApply}",  // autoApplyがtrueの場合のみ実行
        "inputs": {
          "function_signature": "${step2.fixed_code}",
          "language": "${language}",
          "coverage": "comprehensive"
        },
        "outputs": ["test_code"]
      }
    ]
  },
  
  "outputFormat": {
    "type": "object",
    "schema": {
      "properties": {
        "analysis": {
          "description": "初期分析結果",
          "type": "object"
        },
        "fixed_code": {
          "description": "改修されたコード",
          "type": "string"
        },
        "fixes_explanation": {
          "description": "修正内容の説明",
          "type": "string"
        },
        "test_code": {
          "description": "生成されたテストコード（autoApply: trueの場合のみ）",
          "type": "string"
        },
        "summary": {
          "description": "処理全体のサマリー",
          "type": "object",
          "properties": {
            "issues_found": {"type": "number"},
            "fixes_applied": {"type": "number"},
            "tests_generated": {"type": "number"},
            "total_time": {"type": "string"}
          }
        }
      }
    }
  }
}
```

### 複合スキル実装例（Python）

```python
import asyncio
import json
from typing import Dict, Any
from datetime import datetime

class CompositeSkillOrchestrator:
    """複合スキルのオーケストレーター"""
    
    def __init__(self, skill_executor):
        self.executor = skill_executor
        self.results = {}
        self.start_time = None
    
    async def execute_composite_skill(self, 
                                      code: str,
                                      language: str,
                                      focus_areas: list,
                                      auto_apply: bool = False) -> Dict[str, Any]:
        """複合スキルを順序実行"""
        
        self.start_time = datetime.now()
        
        try:
            # Step 1: コード分析
            print("Step 1: Analyzing code quality...")
            analysis = await self.executor.execute(
                skill_id="analyze-code-quality",
                parameters={
                    "code_snippet": code,
                    "language": language,
                    "focusAreas": focus_areas,
                    "detailLevel": "detailed"
                }
            )
            self.results['step1_analysis'] = analysis
            
            # Step 2: 修正コード生成
            print("Step 2: Generating fixes...")
            fixes = await self.executor.execute(
                skill_id="generate-fixes",
                parameters={
                    "code": code,
                    "issues": analysis['issues'],
                    "language": language
                }
            )
            self.results['step2_fixes'] = fixes
            
            # Step 3: テスト生成（条件付き）
            test_code = None
            if auto_apply:
                print("Step 3: Generating unit tests...")
                tests = await self.executor.execute(
                    skill_id="generate-unit-tests",
                    parameters={
                        "function_signature": fixes['fixed_code'],
                        "language": language,
                        "coverage": "comprehensive"
                    }
                )
                self.results['step3_tests'] = tests
                test_code = tests['test_code']
            
            # 結果を集約
            duration = (datetime.now() - self.start_time).total_seconds()
            
            return {
                "analysis": analysis,
                "fixed_code": fixes['fixed_code'],
                "fixes_explanation": fixes['explanation'],
                "test_code": test_code,
                "summary": {
                    "issues_found": len(analysis.get('issues', [])),
                    "fixes_applied": len(fixes.get('fixes', [])),
                    "tests_generated": 1 if test_code else 0,
                    "total_time": f"{duration:.2f}s"
                }
            }
        
        except Exception as e:
            return {
                "error": str(e),
                "failed_step": self._get_failed_step(),
                "partial_results": self.results
            }
    
    def _get_failed_step(self):
        """失敗したステップを特定"""
        if 'step1_analysis' not in self.results:
            return "analyze-code-quality"
        elif 'step2_fixes' not in self.results:
            return "generate-fixes"
        elif 'step3_tests' not in self.results:
            return "generate-unit-tests"
        return "unknown"

# 使用例
async def main():
    orchestrator = CompositeSkillOrchestrator(executor)
    
    result = await orchestrator.execute_composite_skill(
        code="""
def merge_lists(a, b):
    return a + b  # ★ 品質問題あり
        """,
        language="python",
        focus_areas=["readability", "performance"],
        auto_apply=True
    )
    
    print(json.dumps(result, indent=2))

# asyncio.run(main())
```

---

## 複合スキルの設計パターン

### パターン1: Sequential（順序実行）

```
入力 → [Skill A] → [Skill B] → [Skill C] → 出力

特徴：
- 前のスキルの出力が次のスキルの入力
- シンプルで予測可能
- スキル間の依存関係が明確

使用例：
- パイプライン処理
- 段階的な変換
- エラーハンドリングが簡単
```

### パターン2: Parallel（並列実行）

```
入力 ┌→ [Skill A] ┐
     ├→ [Skill B] ├→ 結果統合 → 出力
     ├→ [Skill C] ┘
     └→ [Skill D] ┘

特徴：
- 独立したスキルを同時実行
- 処理時間が短縮
- 複雑な同期が必要

使用例：
- 複数観点の同時分析
- リソース利用の最適化
```

### パターン3: Conditional（条件付き実行）

```
[Skill A] の結果
    ↓
┌─ if condition
│  └→ [Skill B]
└─ else
   └→ [Skill C]
    ↓
 [Skill D]

特徴：
- 条件に応じて異なるパス
- 柔軟な処理フロー
- ロジック複雑化の可能性
```

### パターン4: Loop（反復実行）

```
入力 → [初期化]
      ↓
    ┌→ [処理スキル]
    │  ↓
    └─ [終了条件] ─N→ 出力
           ↓Y
        [結果統合]

特徴：
- 複数の同じ処理を繰り返し
- 累積結果の処理
- バッチ処理向け

使用例：
- バッチコード分析
- 複数ファイルの処理
```

---

## 複合スキルの実装例2: API 統合パイプライン

```json
{
  "id": "api-documentation-generator",
  "name": "API ドキュメント生成パイプライン",
  "compositeDefinition": {
    "workflow": "sequential",
    "steps": [
      {
        "id": "parse_api",
        "skill": "parse-api-spec",
        "inputs": {"spec": "${openapi_spec}"},
        "outputs": ["endpoints", "models"]
      },
      {
        "id": "analyze_endpoints",
        "skill": "analyze-api-endpoints",
        "dependsOn": ["parse_api"],
        "inputs": {"endpoints": "${parse_api.endpoints}"},
        "outputs": ["endpoint_analysis"]
      },
      {
        "id": "generate_docs",
        "skill": "generate-api-docs",
        "dependsOn": ["analyze_endpoints"],
        "parallelize": [
          {
            "skill": "generate-usage-examples",
            "inputs": {"endpoints": "${parse_api.endpoints}"}
          },
          {
            "skill": "generate-error-docs",
            "inputs": {"endpoints": "${parse_api.endpoints}"}
          }
        ]
      }
    ]
  }
}
```

---

## 複合スキルのテスト

```python
def test_composite_skill_improvement_pipeline():
    """複合スキルのテスト"""
    
    test_code = """
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    return total
    """
    
    # テストケース1: 正常系
    result = execute_composite_skill(
        code=test_code,
        language="python",
        focus_areas=["performance", "readability"]
    )
    
    assert 'analysis' in result
    assert 'fixed_code' in result
    assert result['summary']['issues_found'] > 0
    
    # テストケース2: auto_apply = True
    result_with_tests = execute_composite_skill(
        code=test_code,
        language="python",
        focus_areas=["readability"],
        auto_apply=True
    )
    
    assert result_with_tests['test_code'] is not None
    
    # テストケース3: エラーハンドリング
    result_error = execute_composite_skill(
        code="invalid",
        language="invalid_language"  # 無効な言語
    )
    
    assert "error" in result_error or result_error['summary']['issues_found'] == 0
```

---

## 複合スキルのベストプラクティス

```
1. 依存関係を明確に
   □ 各ステップの出力が明示的
   □ 次のステップの入力と一致
   □ 失敗時の代替手段を用意

2. エラーハンドリング
   □ 各ステップでエラーをキャッチ
   □ 部分的な失敗時の対応を定義
   □ ロールバック機構を用意

3. パフォーマンス
   □ 並列化できる部分は並列実行
   □ スキム間の矛盾を解決
   □ キャッシング機構を検討

4. 監視・トレーサビリティ
   □ 各ステップの実行時間を計測
   □ 中間結果をログに記録
   □ エラーの根本原因を特定可能に

5. バージョン管理
   □ 依存スキルのバージョンを指定
   □ 互換性マトリックスを管理
   □ 破壊的変更時の対応を計画
```

---

## チェックリスト（複合スキル実装）

```
設計フェーズ：
□ 個別スキルでテスト
□ ワークフローを図示
□ 各ステップの入力/出力を定義
□ エラーケースを想定

実装フェーズ：
□ ステップを1つずつ実装
□ 中間状態のテスト
□ エラーハンドリング実装
□ ロギング・計測実装

テストフェーズ：
□ 単体テスト（各ステップ）
□ 統合テスト（全体フロー）
□ エッジケーステスト
□ パフォーマンステスト
□ 失敗シナリオテスト

配備フェーズ：
□ ドキュメント完成
□ 依存スキルの準備確認
□ 段階的なロールアウト
□ 監視・アラート設定
```

---

## まとめ

複合スキルは：

| 側面 | ポイント |
|------|---------|
| **威力** | 単独スキルより大きな価値を提供 |
| **設計** | 明確な依存関係と明示的な入力/出力 |
| **エラー** | 各ステップでの堅牢なハンドリング |
| **パフォーマンス** | 可能な限り並列化 |
| **テスト** | 統合テストが特に重要 |
| **保守** | 依存スキルの更新に注意 |

→ 次へ: [Part 5-2: API統合と外部ツール連携](02-api-integration.md)
