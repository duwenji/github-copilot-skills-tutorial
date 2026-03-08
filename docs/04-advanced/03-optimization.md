# Part 4-3: パフォーマンス最適化と監視

スキルのパフォーマンスを測定し、ボトルネックを特定して最適化する方法を学びます。

---

## パフォーマンスのキーメトリクス

### 実行時間の最適化

```
目標実行時間の設定：

スキルタイプ          目指すべき実行時間   最大許容時間
─────────────────────────────────────────────────
分析スキル            1-3秒              5秒
生成スキル            2-5秒              10秒
テストスキル          3-8秒              15秒
複雑な処理            5-10秒             20秒
```

### メトリクス追跡の例

```json
{
  "execution_time_metrics": {
    "min": 1.2,
    "max": 8.5,
    "avg": 3.4,
    "median": 3.1,
    "p99": 7.8,
    "p95": 6.2,
    "p90": 5.1,
    "trend": "stable"
  },
  "success_rate": 98.5,
  "error_types": {
    "timeout": 0.8,
    "invalid_input": 0.4,
    "api_error": 0.3
  },
  "throughput": {
    "requests_per_minute": 45,
    "concurrent_users": 12
  }
}
```

---

## 実行時間のプロファイリング

### プロンプト処理時間の分析

```
ユーザーリクエスト
    ↓ [100ms] 入力バリデーション
パラメータ解析
    ↓ [50ms] テンプレート変数展開
プロンプト構築
    ↓ [2000ms] LLM 処理 ★ ボトルネック
LLM レスポンセ
    ↓ [100ms] 出力フォーマット
ユーザーへの返却

合計時間: 約2250ms

最適化の機会:
1. LLM処理 (40% → 30%): プロンプト簡潔化
2. テンプレート処理 (2% → 1%): キャッシング
3. 入力バリデーション (4% → 2%): 最適化
```

---

## パフォーマンス計測スクリプト

### performance-profiler.py（推奨実装）

以下は、スキルのパフォーマンスを包括的に計測・分析するPythonスクリプトの例です。

```python
#!/usr/bin/env python3
\"\"\"Performance profiler for Copilot Skills\"\"\"

import time
import json
from functools import wraps
from datetime import datetime
from typing import Dict, Any

class PerformanceProfiler:
    \"\"\"各段階のパフォーマンスを計測・分析\"\"\"
    
    def __init__(self, skill_name: str, target_exec_time_ms: float = 5000):
        self.skill_name = skill_name
        self.target_time = target_exec_time_ms / 1000  # 秒に変換
        self.measurements = {}
    
    def measure(self, func):
        \"\"\"デコレータで実行時間を計測\"\"\"
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            
            func_name = func.__name__
            if func_name not in self.measurements:
                self.measurements[func_name] = []
            self.measurements[func_name].append(elapsed)
            
            return result
        return wrapper
    
    def generate_report(self) -> Dict[str, Any]:
        \"\"\"詳細レポート生成\"\"\"
        report = {\"skill\": self.skill_name, \"stages\": {}, \"summary\": {}}
        total = sum(sum(t) for t in self.measurements.values())
        
        for stage, timings in self.measurements.items():
            avg = sum(timings) / len(timings)
            report[\"stages\"][stage] = {
                \"count\": len(timings),
                \"avg_ms\": avg * 1000,
                \"min_ms\": min(timings) * 1000,
                \"max_ms\": max(timings) * 1000,
                \"pct\": (sum(timings) / total * 100) if total > 0 else 0
            }
        
        report[\"summary\"][\"total_ms\"] = total * 1000
        report[\"summary\"][\"status\"] = (
            \"Excellent\" if total < self.target_time * 0.7 else
            \"Good\" if total < self.target_time else
            \"Needs Optimization\"
        )
        
        return report
    
    def print_report(self):
        \"\"\"見やすいレポート表示\"\"\"
        report = self.generate_report()
        print(f\"\\n{'='*60}\\n📊 {report['skill']}\\n{'='*60}\")
        
        for stage, metrics in report[\"stages\"].items():
            print(f\"{stage}: {metrics['avg_ms']:.1f}ms avg \"\n                  f\"({metrics['pct']:.1f}%) - Min: {metrics['min_ms']:.1f}ms, \"\n                  f\"Max: {metrics['max_ms']:.1f}ms\")
        
        summary = report[\"summary\"]
        print(f\"\\n⏱️  Total: {summary['total_ms']:.1f}ms | Status: {summary['status']}\")
        print(f\"{'='*60}\\n\")

# 使用例
if __name__ == \"__main__\":
    profiler = PerformanceProfiler(\"analyze-code-quality\")
    
    @profiler.measure
    def validate(): time.sleep(0.1)
    
    @profiler.measure  
    def build_prompt(): time.sleep(0.05)
    
    @profiler.measure
    def call_llm(): time.sleep(2.0)
    
    @profiler.measure
    def format(): time.sleep(0.1)
    
    # 実行＆レポート
    validate()
    build_prompt()
    call_llm()
    format()
    profiler.print_report()
```

### 段階別の最適化

```python
# 実装例：パフォーマンス計測

import time
from functools import wraps

def measure_performance(func):
    """デコレータで各段階のパフォーマンスを計測"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__}: {duration:.3f}s")
        return result
    return wrapper

# 各段階の計測
@measure_performance
def validate_input(params):
    # 入力バリデーション
    pass

@measure_performance
def build_prompt(template, variables):
    # プロンプト構築
    pass

@measure_performance
def call_llm(prompt):
    # LLM呼び出し
    pass

@measure_performance
def format_output(raw_output):
    # 出力フォーマット
    pass
```

---

## プロンプト最適化による高速化

### テクニック1: プロンプト圧縮

```
最適化前（2000トークン）:
─────────────────────
"You are an expert code reviewer. Your role is to analyze 
Python code and provide detailed feedback on multiple dimensions. 
You should consider code readability, performance issues, 
security vulnerabilities, and testability. For each issue found, 
provide the line number, issue type, severity level (critical, 
high, medium, low), detailed explanation, and recommended fix. 
Format your response as a JSON..."

処理時間: 2500ms

最適化後（800トークン）:
──────────────────────
"Review Python code across: readability, performance, security, 
testability. For each issue list: line number, type (critical/
high/medium/low), explanation, fix. Output as JSON with 
structure: {issues: [{line, type, severity, explanation, fix}]}"

処理時間: 800ms
→ 68% の処理時間削減
```

### テクニック2: 条件付き処理

```python
def generate_prompt(template, variables, detail_level):
    """detail_levelに応じてプロンプトサイズを調整"""
    
    base_prompt = f"Your task: {template}\n"
    
    if detail_level == "brief":
        # 必須情報のみ
        prompt = base_prompt + f"Input: {variables['code']}\nOutput: JSON"
        
    elif detail_level == "standard":
        # 一般的な詳細度
        prompt = base_prompt + f"""
Input code:
{variables['code']}

Focus areas: {variables['focus_areas']}
Output format: JSON with issues and recommendations
"""
        
    elif detail_level == "comprehensive":
        # 詳細な指示
        prompt = base_prompt + f"""
Input code:
{variables['code']}

Analyze these dimensions:
{variables['dimensions']}

For each issue provide:
- Line number and code snippet
- Type and severity
- Explanation and fix
- Testing strategy

Output: JSON with full details
"""
    return prompt
```

### テクニック3: キャッシング

```json
キャッシング戦略

静的なプロンプト部分をキャッシュ:
{
  "cache": {
    "system_prompt": false,  // システムプロンプトは毎回
    "parameter_definitions": true,  // パラメータ定義は再利用可
    "output_schema": true,    // 出力スキーマは再利用可
    "examples": true,         // 使用例は再利用可
    "ttl": 3600               // 1時間のキャッシュ
  }
}

キャッシュキーの生成:
hash(language + output_format + detail_level + focus_areas)

例：
Input 1: Python, JSON, standard, [readability, security]
  → Cache Key: abc123 (初回キャッシュ)

Input 2: Python, JSON, standard, [readability, security]
  → Cache Key: abc123 (キャッシュヒット!)
  → 処理時間削減: 2500ms → 100ms
```

---

## 並列処理による高速化

### 複数スキルの並列実行

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def analyze_code_parallel(code_samples):
    """複数のコード分析を並列実行"""
    
    tasks = [
        asyncio.create_task(analyze_readability(code))
        for code in code_samples
    ]
    
    # すべてが完了するまで待機
    results = await asyncio.gather(*tasks)
    return results

# 実行時間の比較
# 順序実行: 5 samples × 2秒 = 10秒
# 並列実行: max(2秒, 2秒, 2秒, ...) = 2秒
# 高速化: 5倍!
```

### スキル内での並列処理

```json
複雑なテスト生成スキルの場合：

順序処理フロー:
正常系テスト生成 (3秒) → 
エッジケーステスト生成 (2秒) → 
エラーケーステスト生成 (2秒) → 
合計: 7秒

並列処理フロー:
正常系テスト生成 (3秒) ┐
エッジケーステスト生成 (2秒) ├→ max = 3秒
エラーケーステスト生成 (2秒) ┘
合計: 3秒

効果: 7秒 → 3秒 (57% 削減)
```

---

## メモリ効率の改善

### 大規模入力の処理

```python
# ❌ 非効率：全体をメモリに読み込む
def analyze_large_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()  # メモリオーバーフロー！
    return analyze(content)

# ✓ 効率的：チャンク処理
def analyze_large_file_chunked(file_path, chunk_size=1000):
    results = []
    with open(file_path, 'r') as f:
        chunk = ""
        for line in f:
            chunk += line
            if len(chunk) >= chunk_size:
                results.append(analyze_chunk(chunk))
                chunk = ""
        if chunk:
            results.append(analyze_chunk(chunk))
    return merge_results(results)
```

---

## スキルの監視と診断

### リアルタイム監視ダッシュボード

```
┌──────────────────────────────────────────┐
│   Copilot Skills Performance Dashboard   │
├──────────────────────────────────────────┤
│                                          │
│ Skill: analyze-code-quality              │
│                                          │
│ Status: ✓ Healthy                        │
│                                          │
│ Last 60 minutes:                         │
│ • Response time: 3.2s ± 0.8s (avg)       │
│ • Success rate: 98.2%                    │
│ • Requests: 1,245/min                    │
│ • Error rate: 1.8%                       │
│ • P99 latency: 5.1s                      │
│                                          │
│ Errors:                                  │
│ ├─ Timeout (0.8%)                        │
│ ├─ Invalid input (0.6%)                  │
│ └─ API error (0.4%)                      │
│                                          │
│ Recommendations:                         │
│ • Response time増加傾向 → キャッシュの確認
│ • エラー率わずかに上昇 → LLM APIの状態確認
│                                          │
└──────────────────────────────────────────┘
```

### ログとアラート

```yaml
monitoring:
  metrics:
    response_time:
      warning_threshold: 5.0s
      critical_threshold: 10.0s
      alert_message: "Skill response time exceeded threshold"
    
    error_rate:
      warning_threshold: 5%
      critical_threshold: 10%
      alert_message: "Error rate exceeds threshold"
    
    success_rate:
      warning_threshold: 95%
      critical_threshold: 90%
      alert_message: "Success rate fell below threshold"
  
  logging:
    format: "json"
    fields:
      - timestamp
      - skill_id
      - request_id
      - response_time
      - status_code
      - error_type (if any)
      - user_id
      - parameters_hash
```

---

## スケーリング戦略

### 段階的なスケーリング

```
Phase 1: 単一インスタンス（1-100 req/min）
┌─────────────────────┐
│  Copilot Skill API  │ (1インスタンス)
└─────────────────────┘
処理能力: 最大100 req/min

Phase 2: 複数インスタンス + ロードバランサー（100-500 req/min）
┌──────────────────────────────┐
│   Load Balancer              │
├──────────────────────────────┤
│ Instance 1 │ Instance 2 │ Instance 3
│ (50req/min)│ (50req/min)│ (50req/min) → 合計150 req/min
└──────────────────────────────┘

Phase 3: オートスケーリング + キャッシュ（500+ req/min）
┌──────────────────────────────┐
│   Kubernetes Orchestration    │
│   (自動スケーリング)           │
├──────────────────────────────┤
│ Distributed Cache (Redis)    │
└──────────────────────────────┘
```

---

## トラブルシューティング

### 問題1: 急激な速度低下

```
診断ステップ：

1. メトリクス確認
   □ 平均応答時間が増加しているか
   □ エラー率が増加しているか
   □ メモリ使用率が高くなっているか

2. LLM側の問題確認
   □ LLM API のレイテンシをチェック
   □ レート制限に達しているか
   □ API status page を確認

3. スキル側の問題確認
   □ 最近の変更を確認
   □ プロンプットサイズが増加していないか
   □ 依存スキルの状態確認

4. 対応策
   □ キャッシュを有効化
   □ プロンプット圧縮
   □ インスタンス数を増加
   □ レート制限を調整
```

### 問題2: 高いエラー率

```
根本原因分析：

エラータイプ別対応：

Timeout エラー (> 20% of errors):
  原因: プロンプットが大きすぎる、LLMが遅い
  対応: 
    □ プロンプット簡潔化
    □ タイムアウト値調整
    □ リトライロジック追加

Invalid Input エラー:
  原因: ユーザー入力の検証不足
  対応:
    □ 入力検証を強化
    □ エラーメッセージを改善
    □ 使用例を充実

API エラー:
  原因: 外部API（LLM）の信頼性
  対応:
    □ リトライ戦略の導入
    □ フォールバック実装
    □ サーキットブレーカーパターン
```

---

## パフォーマンステスト

### ロードテストの実施

```python
import concurrent.futures
import time

def load_test_skill(skill_id, num_requests=1000, concurrency=10):
    """スキルのロードテスト"""
    
    results = {
        'total_requests': num_requests,
        'response_times': [],
        'errors': 0,
        'start_time': time.time()
    }
    
    def make_request():
        try:
            start = time.time()
            response = call_skill(skill_id, sample_params)
            elapsed = time.time() - start
            return elapsed, True
        except Exception as e:
            return None, False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        
        for future in concurrent.futures.as_completed(futures):
            elapsed, success = future.result()
            if success:
                results['response_times'].append(elapsed)
            else:
                results['errors'] += 1
    
    results['duration'] = time.time() - results['start_time']
    results['avg_response_time'] = sum(results['response_times']) / len(results['response_times'])
    results['error_rate'] = results['errors'] / num_requests * 100
    
    return results

# テスト結果
test_results = load_test_skill('analyze-code-quality', num_requests=100, concurrency=5)
print(f"Average Response Time: {test_results['avg_response_time']:.2f}s")
print(f"Error Rate: {test_results['error_rate']:.1f}%")
```

---

## 実装チェックリスト

```
パフォーマンス最適化：
□ キーメトリクスを定義（実行時間、成功率など）
□ プロンプト最適化（圧縮、条件付き処理）
□ キャッシング戦略を実装
□ 並列処理を導入（可能な場合）
□ メモリ効率を改善

監視・診断：
□ リアルタイムダッシュボードを構築
□ アラート機構を実装
□ ロギングを確立
□ SLA を定義

スケーリング：
□ ロードテスト計画を立案
□ スケーリングアーキテクチャを設計
□ オートスケーリング構成
□ キャッシュインフラ（Redis等）の検討
```

---

## ベストプラクティス

| 側面 | ポイント |
|------|---------|
| **計測** | 本番環境で継続的に計測、メトリクスベースの最適化 |
| **プロンプト** | シンプルで明確、不要な詳細は削除 |
| **キャッシング** | 静的部分を徹底的にキャッシュ |
| **並列化** | 独立した処理は並列実行 |
| **監視** | プロアクティブなアラート (反応的ではなく) |
| **段階的改善** | 一度にすべて最適化せず、優先順位を付けて改善 |

→ 次へ: [Part 4-4:トラブルシューティング](04-troubleshooting.md)
