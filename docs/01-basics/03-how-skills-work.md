# Part 1-3: スキルの仕組み理解

## スキルの内部構造

### 概要図

```
User Interface
      ↓
┌─────────────────────────────────────┐
│  スキル実行リクエスト                  │
│  (スキル名 + パラメータ)              │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Copilot Agent Skills                │
│  - メタデータの検証                   │
│  - パラメータの処理                   │
│  - プロンプトテンプレートの展開      │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  LLM（言語モデル）                    │
│  - 生成 API に送信                    │
│  - 応答を生成                         │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  出力処理                             │
│  - フォーマットの検証                 │
│  - 返却形式の変換                     │
└────────────┬────────────────────────┘
             │
             ↓
        出力結果
```

## スキル定義ファイルの構成

### JSON形式の例

```json
{
  "id": "analyze-code-quality",
  "version": "1.0.0",
  "name": "コード品質分析",
  "description": "Pythonコードのコード品質を複合的に分析し、改善点を提案します",
  
  "metadata": {
    "author": "Copilot Team",
    "created": "2026-01-15",
    "lastUpdated": "2026-03-07",
    "category": "code-analysis",
    "tags": ["python", "quality", "analysis"]
  },
  
  "parameters": {
    "code_snippet": {
      "type": "string",
      "description": "分析対象のPythonコード",
      "required": true,
      "maxLength": 5000
    },
    "language": {
      "type": "string",
      "description": "プログラミング言語",
      "enum": ["python", "javascript", "typescript", "java"],
      "required": true
    },
    "focusAreas": {
      "type": "array",
      "description": "重点分析エリア",
      "items": { "enum": ["readability", "performance", "security", "testability"] },
      "required": false,
      "default": ["readability", "performance", "security", "testability"]
    }
  },
  
  "prompt": {
    "system": "You are an expert code reviewer with deep knowledge of best practices...",
    "template": "Analyze the following {language} code for quality issues...",
    "variables": ["{code_snippet}", "{focusAreas}"]
  },
  
  "outputFormat": {
    "type": "json",
    "schema": {
      "readability": {
        "score": "number (0-100)",
        "issues": "array of strings"
      },
      "performance": {
        "score": "number (0-100)",
        "issues": "array of strings"
      },
      "security": {
        "score": "number (0-100)",
        "issues": "array of strings"
      },
      "testability": {
        "score": "number (0-100)",
        "issues": "array of strings"
      },
      "overallScore": "number (0-100)",
      "recommendations": "array of strings"
    }
  },
  
  "validation": {
    "timeout": 30,
    "maxRetries": 2
  }
}
```

### 各要素の説明

| 要素 | 説明 | 例 |
|------|------|------|
| **id** | スキルの一意な識別子（ハイフン区切り） | `analyze-code-quality` |
| **version** | セマンティックバージョニング | `1.0.0` |
| **name** | ユーザーが目にする名前（日本語可） | `コード品質分析` |
| **description** | スキルの説明（複数行可） | 「Pythonコードの...」 |
| **metadata** | スキルのメタ情報 | 作成者、作成日、カテゴリ等 |
| **parameters** | 入力パラメータの定義 | 型、必須性、制約等 |
| **prompt** | LLMに渡す指示文 | システムプロンプト + テンプレート |
| **outputFormat** | 出力の形式・スキーマ | JSON, CSV, Markdown等 |
| **validation** | 実行時の制約 | タイムアウト、リトライ回数等 |

---

## スキルの実行フロー

### Step-by-Step実行

```
ステップ 1: ユーザーが指示を入力
│
├─ 【方法A】明示的なスキル指定
│   └─ "スキル: analyze-code-quality で、このコードを分析"
│
├─ 【方法B】自然言語による自動選択 ← Copilot エージェント機能
│   └─ "このコードの品質を分析してください"
│       ↓
│       Copilot が自動的にスキルを選択
│
▼ どちらのケースもこのステップへ
ステップ 1.5: スキルの選択（自動選択時）
│
├─ ["analyze-code-quality", {
│     "code_snippet": "def foo():\n  pass",
│     "language": "python"
│  }]
│
▼
ステップ 2: Copilotがスキル定義ファイルをロード
│
├─ metrics.json内の「analyze-code-quality」を検索
├─ メタデータ、パラメータ定義を読み込む
│
▼
ステップ 3: パラメータの検証
│
├─ ✓ code_snippet が存在、5000文字以内
├─ ✓ language が enum 値のいずれか
├─ ✓ 必須パラメータが全て指定されている
│
▼
ステップ 4: プロンプトテンプレートの展開
│
├─ システムプロンプト：「You are an expert code reviewer...」
├─ テンプレート：「Analyze the following {language} code...」
├─ 変数置換：「Analyze the following python code...」
│
▼
ステップ 5: LLM（Claude等）に送信
│
├─ システムプロンプト + 展開済みテンプレート
├─ リクエスト送信
│
▼
ステップ 6: LLM が応答を生成
│
├─ JSON形式で結果を返却
│
▼
ステップ 7: 出力の検証とフォーマット
│
├─ outputSchema に基づいて検証
├─ 型チェック、必須フィールド等を確認
├─ エラーがあれば再試行またはエラー返却
│
▼
ステップ 8: ユーザーに結果を返却
│
└─ {"readability": {...}, "performance": {...}, ...}
```

---

## メタデータの役割

### メタデータとは

スキル自体ではなく、**スキルについての情報**

```
スキル定義ファイル
│
├─ [メタデータ] ← スキルについての情報
│  ├─ id
│  ├─ version
│  ├─ name
│  ├─ description
│  ├─ author
│  ├─ tags
│  └─ ...
│
├─ [実装] ← スキル本体
│  ├─ parameters
│  ├─ prompt
│  ├─ outputFormat
│  └─ ...
```

### メタデータの利用場面

| 場面 | 利用方法 |
|------|---------|
| **検索・ディスカバリー** | `tags: ["python", "quality"]` で検索可能 |
| **バージョン管理** | `version: 1.0.0` でバージョン追跡 |
| **保守性** | `author`, `lastUpdated` で責任者を特定 |
| **分類** | `category: "code-analysis"` でカテゴリ分類 |
| **アクセス制御** | 将来的に `visibility: "private"` 等で制御可能 |

---

## パラメータの定義

### パラメータの型

```json
{
  "parameters": {
    
    "string_param": {
      "type": "string",
      "description": "テキスト入力",
      "required": true,
      "pattern": "^[a-z]+$",      // 正規表現による制約
      "minLength": 1,
      "maxLength": 100
    },
    
    "number_param": {
      "type": "number",
      "description": "数値入力",
      "minimum": 0,
      "maximum": 100
    },
    
    "boolean_param": {
      "type": "boolean",
      "description": "真偽値",
      "default": true
    },
    
    "array_param": {
      "type": "array",
      "description": "配列",
      "items": {"type": "string"},
      "minItems": 1,
      "maxItems": 10
    },
    
    "enum_param": {
      "type": "string",
      "description": "選択肢（複数値から1つ選択）",
      "enum": ["option1", "option2", "option3"]
    }
  }
}
```

### パラメータの検証例

```
入力パラメータ：
{
  "code_snippet": "def foo():\n  x = 1\n  return x",
  "language": "python",
  "focusAreas": ["readability", "security"]
}

検証ルール：
✓ code_snippet: string型、5000文字以内 → OK
✓ language: enum ["python", ...] → OK
✓ focusAreas: enum要素の配列 → OK

全て合格！ → 次のステップへ
```

---

## プロンプトテンプレート

### テンプレートの変数置換

```json
{
  "prompt": {
    "template": "Analyze the following {language} code for {focusAreas}:\n\n{code_snippet}"
  }
}
```

**実行時に以下のように展開される：**

```
入力：
{
  "code_snippet": "def foo():\n  pass",
  "language": "python",
  "focusAreas": ["readability", "performance"]
}

展開後：
"Analyze the following python code for readability, performance:\n\nde
f foo():\n  pass"

↓ LLMに送信
```

### 複雑なテンプレート例

```json
{
  "prompt": {
    "template": "You are analyzing {language} code.\n\nContext: {context}\n\nFocus areas: {focusAreas|join(', ')}\n\nCode:\n{code_snippet|escape}\n\nProvide analysis in JSON format."
  }
}
```

**テンプレート関数（オプション）：**
- `|join(', ')` - 配列を指定の区切り文字で連結
- `|escape` - 特殊文字をエスケープ
- `|uppercase` - 大文字化
- など

---

## 出力形式の定義

### スキーマベースの出力検証

```json
{
  "outputFormat": {
    "type": "json",
    "schema": {
      "title": "CodeQualityAnalysis",
      "type": "object",
      "properties": {
        "readability": {
          "type": "object",
          "properties": {
            "score": {"type": "number", "minimum": 0, "maximum": 100},
            "issues": {"type": "array", "items": {"type": "string"}}
          },
          "required": ["score", "issues"]
        },
        "overallScore": {"type": "number"}
      },
      "required": ["readability", "overallScore"]
    }
  }
}
```

**LLMから返却されたJSONが、このスキーマに適合しているかを検証。**

不適合の場合：
- 再試行を実行
- または詳細なエラーをユーザーに返却

---

## Copilotとの相互作用

### Copilot API との連携

```
Copilot Client
     │
     ├─► JSON-RPC over WebSocket
     │
Copilot Server
     │
     ├─► スキルマネージャー
     │   ├─► スキルの登録・更新・削除
     │   ├─► スキルメタデータの検索
     │   └─► スキルのバージョン管理
     │
     ├─► スキル実行エンジン
     │   ├─► パラメータ検証
     │   ├─► プロンプト展開
     │   └─► LLM呼び出し
     │
     └─► 出力プロセッサー
         ├─► 出力検証
         ├─► フォーマット変換
         └─► キャッシング
```

### スキル実行時のデータフロー

```
User Input
   ↓
┌──────────────────────────────────┐
│ Copilot Client                     │
│ (IDE extension, GitHub Copilot)   │
└─────────────────┬──────────────────┘
                  │
    リクエスト：{"skill": "analyze-code-quality", "params": {...}}
                  │
                  ▼
┌──────────────────────────────────┐
│ Copilot Server                     │
│ 1. スキルローダー                 │
│ 2. 検証エンジン                    │
│ 3. プロンプト生成                 │
└─────────────────┬──────────────────┘
                  │
    プロンプト：「Analyze the following python code...」
                  │
                  ▼
┌──────────────────────────────────┐
│ LLM (Claude / GPT-4 等)           │
│ - テキスト生成                     │
└─────────────────┬──────────────────┘
                  │
    応答：{"readability": {...}, ...}
                  │
                  ▼
┌──────────────────────────────────┐
│ Copilot Server                     │
│ - 出力検証                        │
│ - フォーマット変換                │
└─────────────────┬──────────────────┘
                  │
    結果：検証済みの構造化データ
                  │
                  ▼
┌──────────────────────────────────┐
│ Copilot Client                     │
│ (ユーザーに表示)                  │
└──────────────────────────────────┘
```

---

## スキルのキャッシング メカニズム

### キャッシュが有効な場合

```
同じパラメータでスキルを2回連続実行

実行 1回目：
  パラメータ検証 → プロンプト生成 → LLM呼び出し → キャッシュ保存

実行 2回目：
  パラメータ検証 → キャッシュ命中！ → LLM呼び出しをスキップ
  
  ※ 結果は即座に返却（高速化）
```

### キャッシュキーの生成

```json
キャッシュキー = MD5(skill_id + version + parameters_json)

例：
{
  "skill_id": "analyze-code-quality",
  "version": "1.0.0",
  "parameters": {
    "code_snippet": "def foo():\n  pass",
    "language": "python"
  }
}

↓

キャッシュキー: "a3f5b2c9e7d1..."
```

**キャッシュは有効期限付き**（例：1日、または無期限）

---

## スキルの自動選択メカニズム

### 自動選択とは

ユーザーが **スキル名を明示しなくても**、Copilot エージェントが自動的に最適なスキルを選択・実行する機能。

```
【明示的指定】
User: "analyze-code-quality スキルでこのコードを分析"
  ↓ ユーザーが指定
  → analyze-code-quality が実行

【自動選択】
User: "このコードの品質を分析してください"
  ↓ Copilot が候補スキルから選択
  → analyze-code-quality が実行（ユーザーは指定しない）
```

### 自動選択アルゴリズム

```
ユーザー入力：「このコード分析して」

↓ Step 1: ユーザー意図の抽出

Intent: "code_analysis"
Parameters: { code: ..., context: "code quality" }

↓ Step 2: スキル候補の検索

すべてのスキルメタデータを検索：
├─ analyze-code-quality  ← description: "コードの品質を分析"
├─ generate-documentation
├─ generate-unit-tests
└─ ... その他のスキル

↓ Step 3: 最適スキルのマッチング

スコアリング：
├─ analyze-code-quality  : 95点 ← 「品質」「分析」がヒット
├─ generate-unit-tests   : 30点 ← その他のスキル
└─ generate-documentation: 20点

↓ Step 4: 最高スコアスキルを実行

analyze-code-quality が選定 → 実行！

↓ Result: 結果返却
```

### スキルメタデータの活用

各スキルの **description** と **tags** が自動選択の鍵：

```json
{
  "id": "analyze-code-quality",
  "name": "コード品質分析",
  "description": "Python, JavaScript, TypeScript, Java, Go のコードの品質を多次元的に分析し、改善提案を提供するスキル",
  
  "metadata": {
    "category": "code-analysis",
    "tags": [
      "python", "javascript", "typescript", "java", "go",
      "code-quality",
      "code-review",
      "team-productivity"
    ]
  }
}
```

**ユーザー入力をこれらと照合：**

| ユーザー入力 | マッチタグ | 結果 |
|-----------|----------|------|
| 「コード品質」 | "code-quality" ✓ | analyze-code-quality 選定 |
| 「レビュー」 | "code-review" ✓ | analyze-code-quality 選定 |
| 「テスト生成」 | "unit-test" ✓ | generate-unit-tests 選定 |
| 「ドキュメント」 | "documentation" ✓ | generate-documentation 選定 |

### マッチング戦略

#### 戦略1: キーワード マッチング（シンプル）

```
ユーザー入力：「このコードの品質を分析してください」

キーワード抽出：「品質」「分析」「コード」

スキルのtags/description から検索：
├─ "品質" → "code-quality" ✓
├─ "分析" → "code-analysis" ✓
└─ "コード" → 多くのスキルに該当

最高スコア: analyze-code-quality
```

#### 戦略2: セマンティック マッチング（高度）

```
ユーザー入力をEmbedding化：
  「このコードの品質を分析してください」
  → [0.23, 0.87, 0.45, ..., 0.92]

各スキルのdescription をEmbedding化：
  
  analyze-code-quality:
    「コードの品質を多次元的に分析し、改善提案を提供」
    → [0.22, 0.89, 0.43, ..., 0.94]  ← 類似度 97% ✓✓
  
  generate-unit-tests:
    「テストコードを自動生成」
    → [0.12, 0.34, 0.11, ..., 0.28]  ← 類似度 22%

最高スコア: analyze-code-quality
```

### 自動選択の利点・課題

#### 利点

| 利点 | 効果 |
|------|------|
| **UX向上** | ユーザーがスキル名を覚える必要がない |
| **生産性向上** | 入力が短く済む |
| **一貫性** | 同じ意図には常に同じスキルが選ばれる |

#### 課題と対策

| 課題 | 対策 |
|------|------|
| **誤選択** | ユーザー提示時に「このスキルを使います」と確認 |
| **複数候補同点** | ユーザーに選択肢を提示 |
| **言語の揺らぎ** | セマンティック検索 + フォールバック |

### 実装例（疑似コード）

```python
def auto_select_skill(user_input: str) -> Skill:
    """ユーザー入力から最適なスキルを自動選択"""
    
    # Step 1: 意図抽出
    intent = extract_intent(user_input)
    
    # Step 2: スキル候補を検索
    all_skills = load_all_skills()
    
    # Step 3: マッチングスコアを計算
    scores = {}
    for skill in all_skills:
        # キーワードマッチング
        keyword_score = calculate_keyword_match(
            user_input, 
            skill.description, 
            skill.tags
        )
        # セマンティックマッチング
        semantic_score = calculate_semantic_similarity(
            user_input,
            skill.description
        )
        
        # 総合スコア
        scores[skill.id] = (
            0.3 * keyword_score + 
            0.7 * semantic_score
        )
    
    # Step 4: 最高スコアスキルを返す
    best_skill_id = max(scores, key=scores.get)
    best_score = scores[best_skill_id]
    
    # Step 5: 信頼度チェック
    if best_score < 0.6:  # 閾値以下なら確認を取る
        return prompt_user_selection(scores)
    
    return load_skill(best_skill_id)


# 使用例
user_input = "このコードの品質を分析してください"
skill = auto_select_skill(user_input)
print(f"Selected: {skill.name}")  # → "Selected: コード品質分析"
```

### 複数スキルの組み合わせ

```
ユーザー入力：「コードを分析して、テストを生成して、ドキュメント書いて」

自動選択結果：
├─ Step 1: analyze-code-quality で分析
├─ Step 2: generate-unit-tests でテスト生成
└─ Step 3: generate-documentation でドキュメント生成

このような "複合スキル" 実行可能
（Part 5-1 参照: 複合スキルの詳細）
```

---

## エラーハンドリング


### エラーリトライ メカニズム

```
スキル実行
  │
  ├─► Attempt 1
  │   ├─ LLM に送信
  │   └─ タイムアウト／エラー発生
  │       │
  │       └─ リトライ回数 < 最大？
  │           └─ Yes → Attempt 2
  │               
  ├─► Attempt 2
  │   ├─ LLM に再送信
  │   └─ 成功 / エラー継続
  │       │
  │       └─ 成功？Yes → 結果返却
  │           No → Attempt 3
  │
  └─► Attempt 3 が失敗
      └─ ユーザーにエラーを返却
```

### エラー応答例

```json
{
  "success": false,
  "error": {
    "code": "LLM_TIMEOUT",
    "message": "Language model response timed out",
    "details": "The skill execution exceeded 30 seconds",
    "attempts": 3,
    "recommendation": "Try again with simpler input"
  }
}
```

---

## 次へ進む

→ [Part 2: 比較分析編](../02-comparison/01-vs-mcp.md) - MCPとの違いを詳しく学ぶ
