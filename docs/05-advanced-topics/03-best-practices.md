# Part 5-3: ベストプラクティスと推奨パターン

GitHub Copilot Agent Skills の設計・実装・運用における最良の実践をまとめます。

---

## スキル設計の黄金法則

### 原則1: 単一責任の原則（Single Responsibility）

```
❌ 悪い例：
スキル ID: all-in-one-code-helper
説明: "コード分析、修正提案、テスト生成、ドキュメント作成を全てやる"

問題:
- テストが複雑になる
- 1つ失敗すると全体が停止
- 再利用が困難
- 保守が難しい

✓ 良い例：
スキル1: analyze-code-quality
スキル2: generate-code-fixes
スキル3: generate-unit-tests
スキル4: generate-documentation

利点:
- 各スキルが明確な責務を持つ
- 独立してテスト・改善可能
- 他のスキルと組み合わせ可能
- 保守が容易
```

### 原則2: 明確な入出力契約

```json
例: analyze-code-quality スキル

✓ 明確な入力定義：
{
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "Python, JavaScript, TypeScript, Java, Go のコード",
      "minLength": 10,
      "maxLength": 10000,
      "required": true
    },
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "typescript", "java", "go"],
      "description": "プログラミング言語の明示的な指定",
      "required": true
    }
  }
}

✓ 明確な出力定義：
{
  "outputFormat": {
    "type": "object",
    "schema": {
      "type": "object",
      "properties": {
        "issues": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "line_number": {"type": "integer"},
              "severity": {"enum": ["critical", "high", "medium", "low"]},
              "category": {"type": "string"},
              "description": {"type": "string"},
              "suggestion": {"type": "string"}
            },
            "required": ["line_number", "severity", "description"]
          }
        }
      },
      "required": ["issues"]
    }
  }
}
```

### 原則3: エラーに強い設計

```python
# ❌ エラーハンドリング不足
def analyze_code(code, language):
    prompt = f"Analyze {language} code: {code}"
    return call_llm(prompt)

# ✓ エラー処理を含む
def analyze_code(code: str, language: str) -> Dict[str, Any]:
    """コード分析（エラーハンドリング付き）"""
    
    try:
        # 入力バリデーション
        validate_inputs(code, language)
        
        # プロンプト構築
        prompt = build_prompt(code, language)
        
        # LLM呼び出し（タイムアウト設定）
        response = call_llm(prompt, timeout=10)
        
        # 出力バリデーション
        output = validate_output(response)
        
        return {
            "status": "success",
            "result": output
        }
    
    except ValueError as e:
        # 入力エラー
        return {
            "status": "error",
            "error_type": "invalid_input",
            "message": str(e)
        }
    
    except TimeoutError:
        return {
            "status": "error",
            "error_type": "timeout",
            "message": "Analysis took too long"
        }
    
    except Exception as e:
        # 予期しないエラーをログして、ユーザーフレンドリーなメッセージを返す
        logger.error(f"Unexpected error: {e}")
        return {
            "status": "error",
            "error_type": "internal_error",
            "message": "An error occurred during analysis"
        }
```

---

## スキル実装のパターン

### パターン1: ストレートスルー（Simple Pass-Through）

最もシンプルで共通なパターン。ユーザー入力をそのまま LLM に渡し、結果をフォーマット：

```python
def execute_simple_skill(code: str, language: str) -> Dict:
    """シンプルなスキル（パイプラインなし）"""
    
    prompt = f"""
    Analyze this {language} code:
    
    {code}
    
    Return analysis as JSON:
    {{
      "readability": <score>,
      "performance": <score>,
      "security": <score>
    }}
    """
    
    response = call_llm(prompt)
    return parse_json(response)
```

**使用例:** analyze-code-quality, generate-documentation

### パターン2: エンリッチメント（Enrichment）

入力に情報を追加して、より文脈豊かなプロンプトを構築：

```python
def execute_enriched_skill(code: str, language: str, context: str = None) -> Dict:
    """コンテキスト情報で拡張したスキル"""
    
    # 追加情報を収集
    imports = extract_imports(code)
    complexity = measure_complexity(code)
    
    # コンテキストと共に LLM に渡す
    prompt = f"""
    Analyze this {language} code:
    
    Metadata:
    - Complexity: {complexity}
    - Imports: {imports}
    - Context: {context or 'None'}
    
    Code:
    {code}
    
    Provide detailed analysis...
    """
    
    return call_llm(prompt)
```

**使用例:** classify-code-issues, recommend-refactoring

### パターン3: アグリゲーション（Aggregation）

複数の部分結果を集約して最終結果を生成：

```python
def execute_aggregated_skill(code: str) -> Dict:
    """複数の観点から分析して集約"""
    
    # 並列で複数の分析を実行
    analyses = asyncio.gather(
        analyze_readability(code),
        analyze_performance(code),
        analyze_security(code)
    )
    
    # 結果を集約
    return aggregate_results(analyses)
```

**使用例:** comprehensive-code-review, multi-dimensional-analysis

### パターン4: フィルタリング（Filtering）

大量のデータから重要な部分を抽出：

```python
def execute_filtered_skill(logs: str, error_type: str) -> Dict:
    """ログから特定エラーをフィルタ"""
    
    # ログから関連部分のみ抽出
    relevant_lines = filter_logs(logs, error_type)
    
    # 抽出した部分のみを LLM で分析
    prompt = f"""
    Analyze these {error_type} errors:
    
    {relevant_lines}
    
    Provide root cause analysis and solutions.
    """
    
    return call_llm(prompt)
```

**使用例:** error-log-analyzer, trace-debugger

---

## テストのベストプラクティス

### テスト構造

```python
import pytest
from skill import AnalyzeCodeQualitySkill

class TestAnalyzeCodeQualitySkill:
    """スキルの包括的テスト"""
    
    @pytest.fixture
    def skill(self):
        return AnalyzeCodeQualitySkill()
    
    # カテゴリー1: 正常系テスト
    def test_valid_python_code(self, skill):
        """有効な Python コードの分析"""
        code = "def hello():\n    print('Hello')"
        result = skill.execute(code, "python")
        
        assert result['status'] == 'success'
        assert 'issues' in result
        assert isinstance(result['issues'], list)
    
    # カテゴリー2: エッジケーステスト
    def test_empty_code(self, skill):
        """空のコード"""
        result = skill.execute("", "python")
        assert result['status'] == 'error'
        assert 'code_too_short' in result['error_type']
    
    def test_very_large_code(self, skill):
        """非常に大きなコード"""
        large_code = "x = 1\n" * 5000
        result = skill.execute(large_code, "python")
        
        # タイムアウトのテスト
        assert 'timeout' not in result.get('error_type', '')
    
    # カテゴリー3: エラー処理テスト
    def test_invalid_language(self, skill):
        """サポートされない言語"""
        code = "print('hello')"
        result = skill.execute(code, "cobol")
        
        assert result['status'] == 'error'
        assert result['error_type'] == 'unsupported_language'
    
    def test_malformed_code(self, skill):
        """文法エラーのあるコード"""
        code = "def hello(\n    print('hi')"  # 括弧閉じ忘れ
        result = skill.execute(code, "python")
        
        # 文法エラーも分析対象
        assert result['status'] == 'success'
        assert len(result['issues']) > 0
    
    # カテゴリー4: パフォーマンステスト
    def test_response_time_sla(self, skill):
        """SLA: 3秒以内"""
        code = "x = 1\n" * 100
        
        import time
        start = time.time()
        skill.execute(code, "python")
        duration = time.time() - start
        
        assert duration < 3.0
    
    # カテゴリー5: 出力形式テスト
    def test_output_schema_validation(self, skill):
        """出力スキーマの検証"""
        code = "x = 1"
        result = skill.execute(code, "python")
        
        # スキーマ検証
        assert isinstance(result, dict)
        assert 'issues' in result
        
        for issue in result['issues']:
            assert 'line_number' in issue
            assert 'severity' in issue
            assert issue['severity'] in ['critical', 'high', 'medium', 'low']
```

---

## ドキュメンテーションの標準

### README テンプレート

```markdown
# [Skill Name]

## 概要
1文で何をするスキルか説明。

## 使用例

### 基本的な使い方
```
コード例
```

### 応用例
```
高度な使用方法
```

## パラメータ

| パラメータ | 型 | 必須 | 説明 | 例 |
|----------|----|----|------|-----|
| param1 | string | ✓ | 説明 | example |

## 出力形式

```json
{
  "result": "...",
  "metadata": {...}
}
```

## 制限事項

- 最大入力: 10,000文字
- タイムアウト: 10秒
- 対応言語: Python, JavaScript

## よくある質問

### Q: 入力サイズの制限は?
A: ...

## トラブルシューティング

### エラー: "Invalid input"
A: ...

## 参考資料
- [スキル設計ガイド]
- [API ドキュメント]
```

---

## 運用のベストプラクティス

### モニタリングメトリクス

```yaml
Primary Metrics (見守るべき主要指標):
  Response Time:
    Target: < 3 秒
    Alert: > 5 秒
  
  Success Rate:
    Target: > 99%
    Alert: < 95%
  
  Error Rate by Type:
    Critical Errors: 0 件/日
    User Errors: < 1% of requests

Secondary Metrics (傾向把握):
  Adoption:
    Daily Active Users: 増加傾向？
    Usage Pattern: どのパラメータが人気？
  
  Quality:
    User Rating: 4.0以上？
    Support Tickets: 減少傾向？
```

### インシデント対応の流れ

```
1. 検出（Detection）
   └─ アラートが発火
   └─ 利用者からの報告

2. 応答（Response）
   └─ SLA確認・緊急度判定（1時間以内）
   └─ デバッグ開始
   └─ 利用者への対応報告

3. 修復（Mitigation）
   └─ ホットフィックス作成（4時間以内）
   └─ テスト実行
   └─ デプロイ・検証

4. 解決（Resolution）
   └─ 修復の確認・検証
   └─ 利用者への通知
   └─ Post-mortem 開催（24時間以内）

5. 学習（Learning）
   └─ 根本原因分析
   └─ 再発防止策の立案
   └─ 文書化・知識共有
```

---

## スキル開発フローチャート

```
START
  ↓
1. 要件定義
  □ 何を実現するか
  □ 誰が使うか
  □ 成功基準は
  ↓
2. 設計（低忠実度モックアップ）
  □ パラメータ定義
  □ 出力形式案
  □ プロンプトの大枠
  ↓
3. 実装
  □ スキル定義 JSON
  □ プロンプト最適化
  □ 基本テスト
  ↓
4. 内部テスト（作成者）
  □ 機能テスト
  □ エッジケーステスト
  └─ NO → 修正・改善 → テスト再実行
  ↓ YES
5. ベータテスト（限定ユーザー）
  □ 実運用での動作確認
  □ パフォーマンス計測
  □ UX フィードバック収集
  └─ NO → 改善 → 再テスト
  ↓ YES
6. ドキュメント完成
  □ README 作成
  □ トラブルシューティング
  □ 使用例充実
  ↓
7. リリース準備
  □ リリースノート作成
  □ 告知文準備
  □ SLA 文書化
  ↓
8. 公開・告知
  □ パッケージ公開
  □ ドキュメント公開
  □ チーム告知
  □ デモセッション（オプション）
  ↓
9. 運用開始
  □ メトリクス監視
  □ ユーザーサポート
  □ 定期レビュー
  ↓
10. 改善サイクル
  □ フィードバック収集
  □ 改善提案まとめ
  □ マイナー版更新
  ↓
END（継続監視）
```

---

## チェックリスト（スキル開発完了時）

### 設計フェーズ
```
□ ユースケースが明確
□ 他のスキルとの関係が定義
□ パラメータが直感的
□ 出力形式が明確
```

### 実装フェーズ
```
□ JSON スキーマが有効
□ プロンプトが最適化
□ エラーハンドリングが完全
□ API 呼び出しにタイムアウト設定
```

### テストフェーズ
```
□ 正常系テストが全て成功
□ エッジケーステストが全て成功
□ エラーケーステストが全て成功
□ パフォーマンスが SLA を満たす
□ 出力形式が定義通り
```

### ドキュメンテーション
```
□ README が完成（使用例含む）
□ パラメータが全て説明
□ FAQ / トラブルシューティングがある
□ よくあるエラーと対処法がある
```

### 運用準備
```
□ モニタリングが設定
□ アラート閾値が定義
□ SLA が文書化
□ サポート体制が整備
□ リリースノートが準備
```

---

## 年間キャパシティプランニング例

小規模チーム（10人）の場合：

```
Q1: インフラ / 基礎スキル整備
  - 3スキル開発・リリース
  - 既存スキル最適化 (2スキル)

Q2: 実務スキル充実
  - 4スキル開発・リリース
  - ベータプログラム運営

Q3: AI/ML統合
  - 2スキル開発（高度）
  - 既存スキル改善 (3スキル)

Q4: 運用効率化
  - 1スキル開発
  - モニタリング・運用体制改善
  - 年間レビュー・計画策定

年間合計: 10新規スキル + 8既存スキル改善
= チーム全体で20スキルのライフサイクル管理
```

---

## 業界別専門パターン

### FinTech（金融）

```
重視すべき側面：
- セキュリティ / コンプライアンス
- 精度 / 誤差管理
- 監査ログ

推奨スキル：
1. compliance-checker (規制要件チェック)
2. risk-analyzer (リスク分析)
3. audit-report-generator (監査レポート)
4. financial-code-reviewer (金融コードレビュー)
```

### Healthcare（医療）

```
重視すべき側面：
- プライバシー / HIPAA
- 精度（診断補助）
- 国際標準準拠

推奨スキル：
1. privacy-validator (プライバシー検証)
2. medical-code-analyzer (医療コード解析)
3. clinical-documentation-helper (臨床文書作成支援)
4. standards-compliance-checker (標準準拠チェック)
```

### Enterprise（エンタープライズ）

```
重視すべき側面：
- スケーラビリティ
- エンタープライズセキュリティ
- 統合（既存システムとの）

推奨スキル：
1. legacy-code-analyzer (レガシーコード分析)
2. api-migrator (API マイグレーション支援)
3. security-audit (セキュ
リティ監査)
4. performance-optimizer (パフォーマンス最適化)
```

---

## まとめ：スキル開発の黄金原則

```
1. 単一責任の原則を守る
   → 組み合わせやすく、テストしやすい

2. 明確な入出力契約
   → ユーザーが期待を持てる

3. エラーに強い設計
   → 本番で信頼されるスキル

4. 包括的なテスト
   → 品質の確保

5. 充実したドキュメント
   → ユーザー采用の促進

6. 継続的な監視・改善
   → 長期の成功を確保

7. ユーザーから学ぶ
   → フィードバック→改善のサイクル
```

---

## リソース

### 内部ドキュメント
- [スキル設計ガイド](../../docs/DESIGN_GUIDE.md)
- [実装テンプレート](../../samples/skill-template.json)
- [テストテンプレート](../../samples/test-template.py)

### 外部リソース
- [GitHub Copilot 公式ドキュメント](https://docs.github.com/copilot)
- [LLM ベストプラクティス](https://platform.openai.com/docs/guides/prompt-engineering)
- [API 設計ガイド](https://swagger.io/resources/articles/best-practices-in-api-design/)

### コミュニティ
- [Q&A フォーラム](#)
- [スキル共有レジストリ](#)
- [月1回のお疲れさま会](#)

---

🎉 **チュートリアル完了！**

ここまで学んだことで、あなたは GitHub Copilot Agent Skills について、
以下ができるようになっています：

✓ スキルの基本を理解している
✓ 複数の実装パターンの違いがわかる
✓ 本番対応のスキルを設計できる
✓ チーム内でスキルを共有できる
✓ パフォーマンスを最適化できる
✓ 問題が発生しても解決できる
✓ 複合スキルや API 統合ができる
✓ ベストプラクティスを実践できる

### 次のステップ

1. **独自スキルの開発**
   実際に自分たちの課題を解決するスキルを作ってみましょう

2. **チーム内での展開**
   スキルを共有し、チームの生産性を向上させましょう

3. **コミュニティへの貢献**
   良いスキルは公開し、他のチームの役に立てましょう

4. **先進的なパターンの探索**
   複合スキル、API 統合、カスタム運用など、
   より高度なパターンに挑戦しください

頑張ってください！ 🚀
