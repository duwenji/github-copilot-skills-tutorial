# Part 3-6: スキル評価フレームワーク（evals）

スキルが意図したとおりに機能しているかを測定し、改善するための **評価駆動開発（EDD）** アプローチです。

---

## 概要：なぜ評価が必要か？

開発したスキルが本当に良いのか、を客観的に確認する必要があります。

```
問題：
└─ スキルを作成 → 試した → 「これでいいでしょう」？

リスク：
├─ 実は他のプロンプトでは失敗している
├─ 追加要件で改善が難しくなる
├─ エッジケースで崩れる
└─ ユーザーが望んでいない結果を生んでいる

解決策：
└─ 評価駆動開発（EDD）
    ├─ テストケースを定義
    ├─ with-skill と without-skill で比較実行
    ├─ 結果を採点・集計
    └─ データに基づいて改善
```

---

## Phase 1: テストケース設計

### evals.json 構造

スキルのテストケースを `evals/evals.json` に記録します。

```json
{
  "skill_name": "pdf-processing",
  "evals": [
    {
      "id": 1,
      "prompt": "実際のユーザープロンプト",
      "expected_output": "成功の定義",
      "files": ["evals/files/sample.pdf"],
      "assertions": ["検証可能なステートメント"]
    }
  ]
}
```

### テストケースの設計方針

#### 1. 最初は3つのテストケースから開始

**理由**
- リソース効率（時間・トークン節約）
- 反復が容易
- 大量のテストで圧倒されない

```
Week 1: 3個のテストケース設計 & 実行
Week 2: 結果評価 & 改善
Week 3: テストケース追加（必要に応じて）
```

#### 2. 現実的なプロンプトを使う

```json
{
  "id": 1,
  "prompt": "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?",
  "expected_output": "A bar chart image showing top 3 months by revenue with labeled axes and values.",
  "files": ["evals/files/sales_2025.csv"]
}
```

**ポイント**
- ファイルパスを含める（ユーザーは常にファイルを参照する）
- 個人的な文脈を含める（「data/...」など）
- 自然な言い回し

#### 3. バリエーションを含める

**良い例**
```json
{
  "id": 1,
  "prompt": "Hey, can you clean up this CSV? customers.csv has some missing emails."
},
{
  "id": 2,
  "prompt": "Parse the CSV at data/input.csv, drop rows where column B is null, and save to data/output.csv"
},
{
  "id": 3,
  "prompt": "I have a corrupted CSV with mixed delimiters. Can you fix it?"
}
```

**理由**
- カジュアルな言い回し（id: 1）
- 技術的で詳細（id: 2）
- エッジケース（id: 3）
- 異なる文脈で動作確認

#### 4. エッジケースを最低1つ含める

```json
{
  "id": 3,
  "prompt": "This CSV file is smaller than usual and has missing headers. Can you analyze it anyway?",
  "expected_output": "Analysis that handles missing headers gracefully",
  "files": ["evals/files/malformed.csv"]
}
```

### 実装例：完全な evals.json

```json
{
  "skill_name": "csv-analyzer",
  "evals": [
    {
      "id": 1,
      "name": "basic-sales-analysis",
      "prompt": "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?",
      "expected_output": "A bar chart image showing the top 3 months by revenue, with labeled axes and values.",
      "files": ["evals/files/sales_2025.csv"],
      "assertions": [
        "The output includes a bar chart image file",
        "The chart shows exactly 3 months",
        "Both axes are labeled",
        "The chart title or caption mentions revenue"
      ]
    },
    {
      "id": 2,
      "name": "data-cleaning",
      "prompt": "There's a CSV in my downloads called customers.csv with some rows having missing emails — can you clean it up and tell me how many were missing?",
      "expected_output": "A cleaned CSV with missing emails handled, plus a count of how many were missing.",
      "files": ["evals/files/customers.csv"],
      "assertions": [
        "Output file is valid CSV format",
        "Missing email rows are removed",
        "Count of removed rows is reported",
        "No data corruption in remaining rows"
      ]
    },
    {
      "id": 3,
      "name": "edge-case-malformed",
      "prompt": "This CSV file has mixed delimiters and some missing headers. Can you parse it and tell me what you found?",
      "expected_output": "Analysis of the CSV structure identifying delimiters, missing headers, and an assessment of data quality.",
      "files": ["evals/files/malformed.csv"],
      "assertions": [
        "Parsing completes without error",
        "Missing headers are identified",
        "Data quality assessment is provided",
        "Recommendations for fixing are included"
      ]
    }
  ]
}
```

---

## Phase 2: ベースライン実行

### with-skill vs without-skill 比較

**ディレクトリ構造**

```
csv-analyzer-workspace/
└── iteration-1/
    ├── eval-1-sales-analysis/
    │   ├── with_skill/
    │   │   ├── outputs/          # スキル実行後の出力ファイル
    │   │   ├── timing.json       # 実行時間・トークン数
    │   │   └── grading.json      # Assertion評点
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    ├── eval-2-data-cleaning/
    │   ├── with_skill/
    │   └── without_skill/
    ├── eval-3-edge-case/
    │   ├── with_skill/
    │   └── without_skill/
    └── benchmark.json            # 統計集約
```

### 実行方法

#### 1. with-skill 実行（スキル使用）

**指示**
```
Execute this task:
- Skill path: /path/to/csv-analyzer
- Task: "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?"
- Input files: evals/files/sales_2025.csv
- Save outputs to: csv-analyzer-workspace/iteration-1/eval-1-sales-analysis/with_skill/outputs/
```

**期待値**
```
実行結果：
├─ outputs/ に出力ファイル（chart.png等）
├─ timing.json に実行統計
└─ grading.json に評価結果
```

#### 2. without-skill 実行（ベースライン）

**指示**
```
Execute this task WITHOUT any skills:
- Task: "I have a CSV of monthly sales data in data/sales_2025.csv. Can you find the top 3 months by revenue and make a bar chart?"
- Input files: evals/files/sales_2025.csv  
- Save outputs to: csv-analyzer-workspace/iteration-1/eval-1-sales-analysis/without_skill/outputs/
```

---

## Phase 3: Assertions 定義

### Assertions とは

検証可能で、客観的に判定できるステートメント。

```
✅ 良い Assertion
├─ "Output includes a valid JSON file"（ファイル存在・形式チェック可能）
├─ "Chart has labeled axes"（視覚的に確認可能）
└─ "Count of records is exactly 150"（数値チェック可能）

❌ 悪い Assertion
├─ "Output is good"（曖昧）
├─ "Uses the exact phrase 'Total Revenue: $X'"（脆弱、文言変更で失敗）
└─ "Feels right"（主観的）
```

### Assertions 設計のコツ

#### 1. 実装後に追加（最初は期待値のみでOK）

```json
{
  "id": 1,
  "prompt": "...",
  "expected_output": "A bar chart...",
  "files": ["..."],
  "assertions": []  // 最初は空で良い
}

// 実行後、結果を見てから assertions を追加
"assertions": [
  "The output includes a bar chart image file",
  "The chart shows exactly 3 months",
  "Both axes are labeled"
]
```

**理由**
- 実際の出力を見ないと「良い」assertionが書けない
- 実装前の想定と実装後の現実は異なる

#### 2. 数値や構造で検証

```json
{
  "assertions": [
    "Output file size > 50KB",
    "JSON has exactly 3 root-level keys",
    "All required fields present: id, name, score",
    "No null values in critical fields"
  ]
}
```

#### 3. 客観的な証拠を求める

```
❌ 弱い評価方法
「これはいいですね」

✅ 強い評価方法
「Found chart.png (87KB) in outputs/」← ファイル証拠
「Title text: 'Top 3 Months by Revenue'」← 実内容
「X-axis labels: January, July, November」← 具体的データ
```

---

## Phase 4: Grading（採点）

### grading.json 構造

各 assertion に対して PASS/FAIL を記録。

```json
{
  "assertion_results": [
    {
      "text": "The output includes a bar chart image file",
      "passed": true,
      "evidence": "Found chart.png (87KB) in outputs directory"
    },
    {
      "text": "The chart shows exactly 3 months",
      "passed": true,
      "evidence": "Chart displays bars for March, July, and November"
    },
    {
      "text": "Both axes are labeled",
      "passed": false,
      "evidence": "Y-axis labeled 'Revenue ($)' but X-axis has no label"
    },
    {
      "text": "The chart title mentions revenue",
      "passed": true,
      "evidence": "Chart title: 'Top 3 Months by Revenue'"
    }
  ],
  "summary": {
    "passed": 3,
    "failed": 1,
    "total": 4,
    "pass_rate": 0.75
  }
}
```

### 採点原則

1. **強い証拠を求める**
   - FAIL なら、FAIL の具体的な理由を
   - PASS なら、PASS を示す証拠を

2. **Assertion 自体も見直す**
   - 常に PASS している → 実質価値がない、削除または強化
   - 常に FAIL している → Assertion が要件に合致していない、修正

3. **スクリプトで検証可能なものはコード化**
   ```python
   # JSON 有効性チェック
   try:
       json.loads(output)
       return PASS
   except:
       return FAIL
   ```

---

## Phase 5: 集計（Benchmarking）

### benchmark.json 作成

全テストケースの統計を集約。

```json
{
  "run_summary": {
    "with_skill": {
      "pass_rate": {
        "mean": 0.83,
        "stddev": 0.06
      },
      "time_seconds": {
        "mean": 45.0,
        "stddev": 12.0
      },
      "tokens": {
        "mean": 3800,
        "stddev": 400
      }
    },
    "without_skill": {
      "pass_rate": {
        "mean": 0.33,
        "stddev": 0.10
      },
      "time_seconds": {
        "mean": 32.0,
        "stddev": 8.0
      },
      "tokens": {
        "mean": 2100,
        "stddev": 300
      }
    },
    "delta": {
      "pass_rate": 0.50,
      "time_seconds": 13.0,
      "tokens": 1700
    }
  }
}
```

### 解釈

```
delta.pass_rate = 0.50 (50ポイント改善)
delta.time_seconds = 13.0 (+13秒）
delta.tokens = 1700 (+1700トークン)

判断：
├─ Pass rate が 50 ポイント改善 → スキルの価値は大きい
├─ +13 秒の追加時間 → 許容範囲
└─ +1700 トークン → 50% の改善に見合う投資
→ ✅ スキルは有效
```

### パターン認識

#### パターン1：スキルが有効

```
with_skill：pass_rate 0.85、time +15秒、tokens +2000
without_skill：pass_rate 0.35、time 30秒、tokens 1500

分析：
├─ 50ポイント改善は大きい
├─ 時間・トークンの追加は許容範囲
└─ ✅ スキル採用すべき
```

#### パターン2：スキルが過度に複雑

```
with_skill：pass_rate 0.37、time +45秒、tokens +5000
without_skill：pass_rate 0.35、time 25秒、tokens 1000

分析：
├─ 2ポイント改善は微小
├─ +45秒は大きな追加コスト
├─ +5000トークンは過度
└─ ❌ スキル簡略化が必要、または破棄検討
```

#### パターン3：エッジケース未対応

```
Test 1-2：pass_rate 0.95 (with-skill)
Test 3  ：pass_rate 0.10 (with-skill エッジケースで失敗)

分析：
├─ 通常ケースは優秀
├─ エッジケースで脆弱
└─ → エッジケースハンドリングを改善
```

---

## Phase 6: 人間によるレビュー

### feedback.json 作成

採点だけでなく、人間の目で確認。

```json
{
  "eval-1-sales-analysis": {
    "comment": "Chart is missing X-axis labels and months are in alphabetical order, not chronological. Data accuracy is correct.",
    "rating": "PARTIAL_PASS"
  },
  "eval-2-data-cleaning": {
    "comment": "Output CSV is clean and correct. Count reporting is clear.",
    "rating": "PASS"
  },
  "eval-3-edge-case": {
    "comment": "Skill crashes on completely malformed CSV. Need better error handling.",
    "rating": "FAIL"
  }
}
```

### フィードバック要素

```
✅ 具体的で改善可能
├─ "Missing X-axis labels"
├─ "Months are alphabetical, not chronological"
└─ "Need error handling for complete malformation"

❌ 曖昧で改善困難
├─ "Looks bad"
├─ "Not quite right"
└─ "Could be better"
```

---

## Phase 7: 改善ループ

### 改善サイクル

```
1. テストケース & Assertion 実行
         ↓
2. 結果評価（数値 + 人間レビュー）
         ↓
3. 改善シグナル収集
   ├─ 失敗 Assertion = 実装ギャップ
   ├─ フィードバック = 品質問題
   └─ Transcript = デバッグ情報
         ↓
4. SKILL.md 改善提案（LLM利用）
         ↓
5. 改善実装
         ↓
6. 新しい iteration 実行（ iteration-2/）
         ↓
7. 改善されたか確認
```

### 改善の優先順位

```
優先度1：通常ケースの失敗
└─ 最も影響が大きい

優先度2：エッジケースの失敗
└─ 重要だけど頻度は低い

優先度3：品質・UX問題
└─ 機能は動くが改善の余地がある

優先度4：トークン最適化
└─ 動作は満足も、コスト削減の余地
```

### 改善指示（LLM 向け）

```
Analyze these eval results and propose improvements to the SKILL.md:

Current SKILL.md:
[SKILL.md 全文]

Failed assertions:
- Test 1: "X-axis labels missing" (but Y-axis is labeled)
- Test 3: Crashes on malformed CSV

Human feedback:
- "Months shown in alphabetical order, not chronological"
- "Need graceful error handling"

Execution transcript:
[LLM が何をしたか、どこで失敗したか]

Generalize from these failures. What broader instructions need to
improve to prevent this across many different prompts?
```

---

## 実装チェックリスト

### テストケース設計段階
- [ ] 少なくとも3つのテストケース定義
- [ ] evals/evals.json に記録
- [ ] カジュアル・技術的・エッジケースを混在
- [ ] 現実的なファイルパス・文脈を含める

### ベースライン実行
- [ ] with-skill 実行 → outputs/ に保存
- [ ] without-skill 実行 → baseline で比較
- [ ] timing.json に実行統計記録

### Assertion & Grading
- [ ] Assertion は実行後に追加（結果見てから）
- [ ] grading.json に具体的な証拠を記録
- [ ] 常に PASS/FAIL している Assertion を見直し

### 集計 & 分析
- [ ] benchmark.json に統計集約
- [ ] delta を解釈（改善ポイントと追加コスト）
- [ ] パターン認識（スキルの価値判定）

### 人間レビュー & 改善
- [ ] feedback.json に具体的コメント
- [ ] 失敗原因を特定
- [ ] 改善提案を SKILL.md に反映
- [ ] 新しい iteration で再実行

---

## よくある質問

### Q1. Assertion で LLM 判定 vs スクリプト判定、どちらを使う？

**A:** 両方を使い分ける

```
スクリプト検証（信頼性高）
├─ JSON 有効性
├─ ファイル存在・サイズ
├─ レコード数・カラム数
└─ 構造的検証

LLM 判定（柔軟性高）
├─ 内容品質「レポートは有用か」
├─ スタイル「書き方は適切か」
├─ ユーザビリティ「使いやすいか」
└─ 定性的判定
```

### Q2. 何個のテストケースが必要？

**A:** 段階的に増加

```
Phase 1（初期）：3-5個
Phase 2（安定化）：5-10個
Phase 3（本番化）：10-20+個

ただし「質 > 量」
├─ 1つの良いテストケース
└─ 10個の無駄なテストケースより価値がある
```

### Q3. スキルの改善をどこまで続ける？

**A:** これらの条件で停止

```
停止条件：
├─ Pass rate が target（例：85%）に達した
├─ 連続2 iteration で改善がない
├─ 時間・トークンコストが許容範囲
└─ フィードバックが「OK」に統一

それ以降は：
├─ 本番運用開始
├─ ユーザーフィードバック収集
└─ 定期レビュー（月1回等）
```

---

## 関連資料

- [agentskills.io - Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- Part 3-3: スキル品質分析（サンプル JSON 例）
- Part 4-2: スキル管理とライフサイクル（運用フェーズ）
