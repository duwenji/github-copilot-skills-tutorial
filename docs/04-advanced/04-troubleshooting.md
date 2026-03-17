# Part 4-4: トラブルシューティングと問題解決

実運用で発生しやすい問題と解決方法を実装例付きで解説します。

## 現場運用でよく使う用語

| 用語 | 意味（本教材での定義） |
|------|------------------------|
| runbook | 現場向けの作業手順書 |
| remediation | 不具合の是正対応 |
| gate | 次に進むための確認ポイント |
| evidence / trace | 作業証跡 |
| scope | 対象範囲 |
| rollout | 横展開 |

### 運用フローの要点

runbookに沿って、確認ポイント（gate）を通過しながら、証跡（evidence/trace）を残して、対象範囲（scope）を漏れなく是正（remediation）し、最後に横展開（rollout）する。

詳細な手法・テンプレートは以下を参照:

- [Part 4-6: 運用手法（Runbook / Gate / Evidence / Scope / Rollout）](06-operations-methodology.md)

---

## よくある問題と解決策

### 問題カテゴリ

```
スキル開発者向け (Development Issues)
  ├─ スキル定義エラー
  ├─ プロンプトの精度不足
  ├─ パフォーマンス問題
  └─ テスト失敗

ユーザー向け (Usage Issues)
  ├─ スキルが見つからない
  ├─ 使い方がわからない
  ├─ 予期しない結果
  └─ エラーが発生

運用チーム向け (Operations Issues)
  ├─ 依存スキルの問題
  ├─ 互換性破損
  ├─ スケーリング問題
  └─ セキュリティ懸念
```

---

## 問題1: スキル定義エラー

### 問題: JSONスキーマが無効

```
エラーメッセージ：
"InvalidSkillDefinition: JSON validation failed"

❌ 原因の例：

{
  "parameters": {
    "code": {
      "type": "string",
      "required": true    // ❌ "required" は parameters.codeプロパティではなく、
                          //   parameters配列で指定すべき
    }
  }
}

✓ 正しい定義：

{
  "parameters": {
    "code": {
      "type": "string",
      "description": "Code to analyze"
    }
  },
  "requiredParameters": ["code"]  // または jsonschemaの "required"
}
```

### 解決方法

```python
# JSONスキーマの検証ツール

import json
import jsonschema

def validate_skill_definition(skill_json_path):
    """スキル定義を検証"""
    
    with open(skill_json_path, 'r') as f:
        skill = json.load(f)
    
    # 必須フィールドの確認
    required_fields = ['id', 'version', 'name', 'parameters', 'prompt', 'outputFormat']
    for field in required_fields:
        if field not in skill:
            raise ValueError(f"Missing required field: {field}")
    
    # JSONスキーマの検証
    skill_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
            "version": {"type": "string", "pattern": "^[0-9]+\.[0-9]+\.[0-9]+$"},
            "parameters": {"type": "object"}
        },
        "required": required_fields
    }
    
    try:
        jsonschema.validate(skill, skill_schema)
        print("✓ Skill definition is valid")
        return True
    except jsonschema.ValidationError as e:
        print(f"❌ Validation error: {e.message}")
        return False

# 使用
validate_skill_definition('skill-definition.json')
```

---

### 問題: 不正なパラメータ定義

```
❌ 悪い例：

{
  "parameters": {
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "java"],
      "default": "c++"  // ❌ enum に c++ が含まれていない
    }
  }
}

✓ 修正：

{
  "parameters": {
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "java", "c++"],
      "default": "python"  // enum に含まれる値に変更
    }
  }
}
```

### チェックリスト（スキル定義の検証）

```
□ JSON 形式が正しい（JSONLint等で確認）
□ 全ての必須フィールドが存在
  ├─ id (英数字とハイフンのみ)
  ├─ version (X.Y.Z形式)
  ├─ name
  ├─ parameters
  ├─ prompt (system + template)
  └─ outputFormat
□ 補助リソース（スクリプト等）のチェック
  ├─ scripts/ ディレクトリが存在するか
  ├─ 各スクリプトが実行可能か（chmod +x）
  ├─ スクリプト言語がドキュメント化されているか
  └─ 依存パッケージがrequirements.txt等で指定されているか
□ templates/ フォルダが存在する場合
  ├─ 各テンプレートが有効な形式か
  └─ パス参照が正しいか
```

### 補助スクリプト：自動検証ツール（skill-validator.py）

スキル定義と補助リソースを自動で検証するツール：

```python
#!/usr/bin/env python3
"""Skill definition validator with auxiliary resource checks"""

import json
import os
import re
import sys
from pathlib import Path

class SkillValidator:
    """スキル定義と補助リソースを検証"""
    
    REQUIRED = ['id', 'version', 'name', 'description', 'parameters', 'prompt', 'outputFormat']
    ID_PATTERN = re.compile(r'^[a-z0-9-]+$')
    VERSION_PATTERN = re.compile(r'^\d+\.\d+\.\d+$')
    
    def __init__(self, skill_dir: str):
        self.skill_dir = Path(skill_dir)
        self.skill_file = self.skill_dir / 'SKILL.md.json'
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """検証実行"""
        if not self.skill_file.exists():
            self.errors.append(f"❌ Skill file not found: {self.skill_file}")
            return False
        
        try:
            with open(self.skill_file) as f:
                self.skill = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"❌ Invalid JSON: {e}")
            return False
        
        # 各検証を実行
        self._validate_required_fields()
        self._validate_id_format()
        self._validate_version_format()
        self._validate_auxiliary_resources()
        
        return len(self.errors) == 0
    
    def _validate_required_fields(self):
        """必須フィールド確認"""
        for field in self.REQUIRED:
            if field not in self.skill:
                self.errors.append(f"❌ Missing field: {field}")
    
    def _validate_id_format(self):
        """ID形式確認"""
        skill_id = self.skill.get('id', '')
        if not self.ID_PATTERN.match(skill_id):
            self.errors.append(f"❌ Invalid ID format: {skill_id}")
    
    def _validate_version_format(self):
        """バージョン形式確認"""
        version = self.skill.get('version', '')
        if not self.VERSION_PATTERN.match(version):
            self.errors.append(f"❌ Invalid version format: {version}")
    
    def _validate_auxiliary_resources(self):
        """補助リソース確認"""
        aux = self.skill.get('auxiliaryResources', {})
        if not aux:
            return
        
        # スクリプト確認
        scripts = aux.get('scripts', [])
        scripts_dir = self.skill_dir / 'scripts'
        
        for script in scripts:
            script_name = script.get('name')
            script_path = scripts_dir / script_name
            
            if not script_path.exists():
                self.warnings.append(f"⚠️  Script not found: {script_path}")
            elif not os.access(script_path, os.X_OK):
                self.warnings.append(f"⚠️  Script not executable: {script_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python skill-validator.py <skill-directory>")
        sys.exit(1)
    
    validator = SkillValidator(sys.argv[1])
    is_valid = validator.validate()
    print(f"Valid: {is_valid} (Errors: {len(validator.errors)}, Warnings: {len(validator.warnings)})")
    sys.exit(0 if is_valid else 1)
```

**使用例：**

```bash
python3 skill-validator.py skills/analyze-code-quality/
```

□ パラメータの定義が正しい
  ├─ type が正当な値
  ├─ required フラグが正しい
  ├─ default 値が型と一致
  ├─ enum 時に default が enum に含まれる
  └─ minLength/maxLength 等の制約が論理的

□ プロンプトテンプレートの変数名が全て有効
  └─ {variable_name} がパラメータに対応

□ 出力スキーマが実装と整合
  └─ required フィールドが全て出力される
```

---

## 問題2: プロンプト精度の問題

### 問題: 出力形式が指定通りでない

```
期待：JSON形式
{
  "result": "success",
  "score": 85
}

実際：テキスト形式
"The analysis shows a score of 85 and is successful."

❌ 原因：プロンプトが曖昧

"Return your analysis."  // 何形式でかが不明

✓ 修正：明確な指示

"Return your analysis as valid JSON with this exact structure:
{
  \"result\": \"<success|failure>\",
  \"score\": <0-100>
}

Example:
{
  \"result\": \"success\",
  \"score\": 85
}"
```

### 出力フォーマット検証の実装

```python
import json
import re
from typing import Union

def validate_output_format(output: str, expected_format: str) -> Union[dict, str, bool]:
    """出力形式を検証"""
    
    if expected_format == "json":
        # JSON形式の検証
        try:
            # JSONブロックを抽出（```json ... ``` に囲まれている可能性）
            json_match = re.search(r'```json\n(.*?)\n```', output, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = output
            
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON output: {e}")
    
    elif expected_format == "text":
        # テキスト形式（常に有効）
        return output
    
    elif expected_format == "boolean":
        # ブール値形式
        normalized = output.lower().strip()
        if normalized in ['true', 'yes', '1']:
            return True
        elif normalized in ['false', 'no', '0']:
            return False
        else:
            raise ValueError(f"Cannot parse as boolean: {output}")

# 使用例
def test_output_format():
    # テスト1: 正しいJSON
    valid_json = '{"result": "success", "score": 85}'
    assert validate_output_format(valid_json, "json") == {"result": "success", "score": 85}
    
    # テスト2: 不正なJSON
    invalid_json = '{"result": "success" score: 85}'  # コロン不足
    try:
        validate_output_format(invalid_json, "json")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"✓ Caught error: {e}")
    
    # テスト3: JSONブロック形式
    json_block = """
    ```json
    {"result": "success"}
    ```
    """
    assert validate_output_format(json_block, "json") == {"result": "success"}
```

### プロンプト改善のテンプレート

```
現在のプロンプト：
"Analyze this code and tell me about the quality."

改善されたプロンプト：
"Analyze the provided code for quality issues.

Focus on:
1. Readability (variable names, structure)
2. Performance (efficiency, complexity)
3. Security (vulnerabilities, best practices)
4. Testability (test coverage, structure)

Return results as JSON:
{
  \"readability\": {\"score\": <0-100>, \"issues\": [...]},
  \"performance\": {\"score\": <0-100>, \"issues\": [...]},
  \"security\": {\"score\": <0-100>, \"issues\": [...]},
  \"testability\": {\"score\": <0-100>, \"issues\": [...]}
}

Each issue should include:
- line_number: where in the code
- severity: critical, high, medium, low
- description: what's wrong
- suggestion: how to fix it"
```

---

## 問題3: スキルが見つからない（ユーザー側）

### 原因の特定

```yaml
診断フロー：

1. スキルレジストリに登録されているか？
   □ REGISTRY.md に listed されているか
   □ リポジトリのスキル一覧に含まれているか
   □ パッケージレジストリ（PyPI/npm）に公開されているか

2. ユーザーがアクセス権を持っているか？
   □ プライベートスキル か? → アクセス権の確認
   □ 組織内限定スキル か? → チームメンバーシップの確認

3. スキル名の問題か?
   □ 正しいスキル ID を使用しているか
   □ 大文字小文字の区別の有無

4. Copilot のセットアップが正しいか?
   □ Copilot がインストールされているか
   □ 最新版に更新されているか
   □ スキルローダーが有効か
```

### ユーザー向けトラブルシューティング

```markdown
# "スキルが見つからない"時の対応

1. **スキルが存在するか確認**
   ```
   スキルレジストリを確認:
   https://github.com/org/copilot-skills/blob/main/REGISTRY.md
   ```

2. **スキル ID が正しいか確認**
   ```
   スキル ID は小文字とハイフンのみ
   例: generate-unit-tests ✓
      GenerateUnitTests ✗
      generate_unit_tests ✗
   ```

3. **Copilot をインストール/更新**
   ```bash
   # VS Code の場合
   命令パレット > "Github Copilot: Check for updates"
   ```

4. **它の設定確認**
   - Copilot 拡張機能が有効か確認
   - チームのスキルカタログにアクセス権があるか確認

5. **サポートに連絡**
   - スキル名と ID を記載
   - Copilot バージョンを記載
   - エラーメッセージをコピー
```

---

## 問題4: 予期しない結果

### デバッグテクニック

```python
def debug_skill_output(skill_id, parameters, expected_pattern=None):
    """スキル実行をデバッグ"""
    
    import json
    from datetime import datetime
    
    # ログファイルに出力
    debug_log = {
        "timestamp": datetime.now().isoformat(),
        "skill_id": skill_id,
        "parameters": parameters,
        "steps": []
    }
    
    try:
        # Step 1: 入力検証
        debug_log["steps"].append({
            "name": "Input Validation",
            "status": "start"
        })
        validate_parameters(parameters)
        debug_log["steps"][-1]["status"] = "success"
        
        # Step 2: プロンプト構築
        debug_log["steps"].append({
            "name": "Prompt Building",
            "status": "start"
        })
        prompt = build_prompt(skill_id, parameters)
        debug_log["steps"][-1].update({
            "status": "success",
            "prompt_length": len(prompt),
            "prompt_preview": prompt[:500]  # 最初の500文字
        })
        
        # Step 3: LLM呼び出し
        debug_log["steps"].append({
            "name": "LLM Call",
            "status": "start"
        })
        output = call_llm(prompt)
        debug_log["steps"][-1].update({
            "status": "success",
            "output_length": len(output),
            "output_preview": output[:500]
        })
        
        # Step 4: 出力検証
        debug_log["steps"].append({
            "name": "Output Validation",
            "status": "start"
        })
        validate_output(output, skill_id)
        debug_log["steps"][-1]["status"] = "success"
        
        # パターンマッチング（オプション）
        if expected_pattern:
            import re
            if re.search(expected_pattern, output):
                debug_log["pattern_match"] = "matched"
            else:
                debug_log["pattern_match"] = "not_matched"
        
        debug_log["result"] = "success"
        
    except Exception as e:
        debug_log["result"] = "error"
        debug_log["error"] = str(e)
        debug_log["error_type"] = type(e).__name__
    
    # ログを保存・出力
    with open(f"debug_{skill_id}_{datetime.now().timestamp()}.json", 'w') as f:
        json.dump(debug_log, f, indent=2)
    
    print(json.dumps(debug_log, indent=2))
    return debug_log

# 使用例
debug_log = debug_skill_output(
    "analyze-code-quality",
    {"code": "def foo(): pass", "language": "python"},
    expected_pattern=r'"score":\s*\d+'
)
```

### ステップバイステップのデバッグ出力例

```
[2026-03-07 14:30:00] Debugging: generate-documentation

Step 1: Input Validation ✓
  - language: python ✓
  - docstyle: google ✓
  - code_element length: 245 chars ✓

Step 2: Prompt Building ✓
  - Template variables expanded: 8 ✓
  - Prompt length: 1,234 tokens
  - Sample: "Generate documentation in Google style for the following Python..."

Step 3: LLM Call ✓
  - Request time: 2.3s
  - Token usage: 2,100 tokens
  - Response length: 512 chars

Step 4: Output Validation ✓
  - Format: Text ✓
  - Contains expected sections:
    ├─ Summary: ✓
    ├─ Args: ✓
    ├─ Returns: ✓
    └─ Examples: ✓

Pattern Match: "Google style format" ✓

Status: SUCCESS ✓
```

---

## 問題5: パフォーマンス低下

### 症状別診断

```
症状: 実行時間が極端に長い（> 20秒）

診断フロー：

1. 単発テスト vs 継続的な低下
   □ 単発のみ → 一時的な LLM API 遅延
   □ 継続的 → スキル内のボトルネック

2. 特定の条件下のみか?
   □ 特定パラメータ値でのみ → パラメータ依存
   □ 入力サイズに依存 → 入力大きさが問題
   □ 常に → スキル自体の問題

3. 影響範囲
   □ このスキルのみ → スキル固有の問題
   □ 全スキル → インフラ/LLM側の問題

推奨対応：
  - 入力を小さくしてリトライ
  - キャッシュクリア
  - スキル version を確認（回帰がないか）
  - LLM API Status を確認
```

### パフォーマンス計測

```python
import time
import statistics

def measure_skill_performance(skill_id, test_cases, iterations=5):
    """スキルのパフォーマンス計測"""
    
    results = {
        "skill_id": skill_id,
        "test_cases": len(test_cases),
        "iterations": iterations,
        "measurements": []
    }
    
    for i, test_case in enumerate(test_cases):
        case_results = {
            "test_case": i,
            "times": []
        }
        
        for _ in range(iterations):
            start = time.time()
            try:
                output = execute_skill(skill_id, test_case["parameters"])
                elapsed = time.time() - start
                case_results["times"].append(elapsed)
            except Exception as e:
                case_results["error"] = str(e)
                break
        
        if case_results["times"]:
            case_results["stats"] = {
                "min": min(case_results["times"]),
                "max": max(case_results["times"]),
                "avg": statistics.mean(case_results["times"]),
                "median": statistics.median(case_results["times"]),
                "stdev": statistics.stdev(case_results["times"])
            }
        
        results["measurements"].append(case_results)
    
    # 統計
    all_times = [t for m in results["measurements"] if "times" in m for t in m["times"]]
    if all_times:
        results["overall"] = {
            "avg": statistics.mean(all_times),
            "median": statistics.median(all_times),
            "max": max(all_times),
            "p99": sorted(all_times)[int(len(all_times) * 0.99)]
        }
    
    return results

# 使用例
perf_results = measure_skill_performance(
    "analyze-code-quality",
    test_cases=[
        {"parameters": {"code": small_code}},
        {"parameters": {"code": medium_code}},
        {"parameters": {"code": large_code}}
    ],
    iterations=3
)

print("Performance Report:")
print(f"Average: {perf_results['overall']['avg']:.2f}s")
print(f"Median: {perf_results['overall']['median']:.2f}s")
print(f"P99: {perf_results['overall']['p99']:.2f}s")
```

---

## 問題6: 互換性破損

### スキル更新による破損

```
状況：
  - スキル generate-doc を v1.0 → v2.0 に更新
  - パラメータ "style" を "docstyle" に変更
  - v1 で動いていたスクリプトが break

❌ 破損例：
v1.0 で動いていたコード：
{
  "skill": "generate-doc",
  "parameters": {
    "style": "google"  // こういう呼び出し
  }
}

v2.0 にアップデート後：
エラー: "Unknown parameter: style"

✓ 修正（互換性レイヤー）：
v2.0 のスキル定義で:
{
  "parameters": {
    "docstyle": { ... },  // 新しい名前
    "_compat_v1_style": {
      "type": "string",
      "description": "DEPRECATED: use docstyle instead",
      "hidden": true
    }
  }
}

プロンプトテンプレート内：
"{{ docstyle if docstyle else _compat_v1_style }}"
```

### 移行ガイドの作成

```markdown
# v1.x → v2.0 移行ガイド

## 主な変更

### パラメータ名の変更
| v1.0 | v2.0 |
|------|------|
| `style` | `docstyle` |
| `code_input` | `code_element` |

### 出力形式の変更
v1.0: テキスト形式
```
def hello():
    """
    Hello world function.
    """
```

v2.0: JSON形式
```json
{
  "documentation": "...",
  "format": "google",
  "sections": {...}
}
```

## 移行ステップ

### 方法1: 自動に実行（v2.0の互換性モード）
アップデートするだけで動作（推奨）

### 方法2: 手動移行
1. パラメータ名を更新
2. 出力形式解析を変更
3. テストを再実行

## 問題が発生した場合
v1.0 のサポートは2026-06-01までです。
その後のアップデートでは互換性を保証しません。
```

---

## 実装チェックリスト

```
スキル検証：
□ JSONスキーマをバリデート
□ パラメータ定義をチェック
□ テンプレート変数を確認

プロンプト調整：
□ 出力形式を明確に指定
□ 例を含める
□ エッジケースを言及

デバッグ：
□ デバッグログを実装
□ ステップバイステップの追跡
□ 各段階の出力を確認

パフォーマンス：
□ ベースラインを計測
□ ボトルネックを特定
□ 改善を実装・検証

互換性：
□ CHANGELOG を更新
□ 互換性マトリックスを作成
□ 移行ガイドを提供
```

---

## サポート体制

### 問題報告のテンプレート

```
## Bug Report Template

**Skill:** [skill-id]
**Version:** [version number]
**OS/Environment:** [Windows/macOS/Linux, VS Code version]

**Description:**
[Clear description of the issue]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. ...

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Logs/Screenshots:**
[Include error messages, screenshots]

**Additional Context:**
[Any additional information]
```

### サポート優先度

```
Priority     Response Time    Fix Timeline
──────────────────────────────────────
Critical     1 hour          24 hours
High         4 hours         3 days
Medium       1 day           1 week
Low          2 days          2 weeks
```

---

## 実装チェックリスト

```
エラーハンドリング：
□ 全ての入力エラーをキャッチ
□ LLM エラーに対応
□ タイムアウト処理
□ ユーザーフレンドリーなエラーメッセージ

デバッグ機能：
□ ステップバイステップログ
□ パフォーマンスログ
□ パラメータ/出力のダンプ機能

テスト：
□ 正常系テスト
□ 異常系テスト
□ エッジケーステスト
□ パフォーマンステスト

ドキュメント：
□ トラブルシューティングガイド
□ FAQ
□ サンプルコード
□ よくあるエラーとその解決法
```

---

## まとめ

成功するスキル運用の鍵：

1. **予防** - 良い設計、包括的なテスト
2. **監視** - メトリクス追跡、早期検出
3. **対応** - SLA遵守、素早い修正
4. **学習** - postmortem, 知識共有

困ったときは：
→ [支援チャネル](https://github.com/org/copilot-skills/discussions)
→ [FAQ](FAQ.md)
→ [スキル作成者向けドキュメント](../docs/DEVELOPER_GUIDE.md)
