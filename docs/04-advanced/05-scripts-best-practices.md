# Part 4-5: スクリプト設計ベストプラクティス

スキルに含める実行可能なスクリプト（Python、Bash、JavaScript等）を効果的に設計するガイドです。

---

## 概要

スキルには単なる指示（Markdown）だけでなく、実行可能なスクリプトを同梱できます。

```
SKILL.md（指示文）
└─ エージェントが読んで理解

scripts/（実行可能）
├─ validate.py      ← エージェントが実行
├─ process.sh       ← 結果をエージェントに返す
└─ analyze.py
```

スクリプト設計の原則を守ることで、エージェントが確実に実行でき、結果を正しく解釈できます。

---

## 原則1: 非インタラクティブ設計（必須）

### エージェント環境の制限

エージェントが実行する環境は **非インタラクティブシェル** です。

```
❌ 動作しない
$ python scripts/deploy.py
Target environment: _  # ← 入力待ち → エージェントが応答不可 → ハング

✅ 動作する
$ python scripts/deploy.py --env production
[実行開始]
```

### 実装パターン

#### パターン1：コマンドラインフラグ

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--env', required=True, choices=['dev', 'staging', 'prod'])
parser.add_argument('--tag', default='latest')
args = parser.parse_args()

print(f"Deploying {args.tag} to {args.env}")
```

**使用方法**
```bash
python scripts/deploy.py --env prod --tag v1.2.3
```

#### パターン2：環境変数

```python
import os

env = os.getenv('TARGET_ENV')
if not env:
    raise ValueError("TARGET_ENV environment variable required")

print(f"Deploying to {env}")
```

**使用方法**
```bash
TARGET_ENV=production python scripts/deploy.py
```

#### パターン3：標準入力（複数値）

```bash
#!/bin/bash
# stdin から CSV データを読む
while IFS=, read -r id name email; do
    process_user "$id" "$name" "$email"
done
```

**使用方法**
```bash
echo "1,Alice,alice@example.com
2,Bob,bob@example.com" | bash scripts/process_users.sh
```

---

## 原則2: 明確なエラーメッセージ

### 悪い例

```python
if not validate_input():
    print("Error")  # ← これでなぜ失敗したか不明
    sys.exit(1)
```

**エージェントの反応**
```
エージェント「エラーが出た。何が悪いのかわからない。
どう修正すればいいの？」
→ 次のステップに進めない
```

### 良い例

```python
import sys

def validate_input(data):
    if not data:
        raise ValueError("Input data is empty. Provide CSV content via stdin or --input")
    if ',' not in data:
        raise ValueError("Input format error: expected CSV. Column separator ',' not found.")
    return True

try:
    process_data(input_data)
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    print("\nUsage: python scripts/process.py [--input FILE]", file=sys.stderr)
    sys.exit(1)
```

**エージェントの反応**
```
Error: Input format error: expected CSV. Column separator ',' not found.

エージェント「',' がないんだ。CSVじゃない形式で来たのか。
ユーザーの入力を修正するか、別の形式で試そう」
→ 次のステップが明確
```

### パターン：`--help` の充実

```bash
$ python scripts/analyze.py --help

Usage: analyze.py [OPTIONS] INPUT_FILE

Analyze text data and generate statistics.

Options:
  --format FORMAT     Output format: json, csv, markdown (default: json)
  --output FILE       Save output to FILE (default: stdout)
  --verbose           Print progress to stderr
  --help              Show this message

Examples:
  analyze.py data.txt
  analyze.py --format csv --output report.csv data.txt
  analyze.py --verbose --output results.json large_file.txt

Error codes:
  0: Success
  1: Input file not found
  2: Invalid format option
  3: Permission denied on output file
```

**メリット**
- エージェントが `--help` でスクリプトの使い方を理解
- ユーザーもドキュメント参照不要
- トラブル時の参照資料

---

## 原則3: 構造化出力

### 出力形式の選択

```
テキスト出力：人向け
├─ ❌ 機械解析困難
└─ ❌ 他スクリプトとの連携困難

構造化出力：機械解析向け
├─ ✅ JSON
├─ ✅ CSV
└─ ✅ TSV
```

### 悪い例（自由形式テキスト）

```python
# ❌ 自由形式
print("Results:")
print(f"  Successfully processed: {success_count}")
print(f"  Failed: {failed_count}")
print(f"  Total time: {elapsed_time:.2f}s")
```

**問題**
- 別のスクリプトで解析しにくい
- フォーマットが変わると他のツール が破綻
- エージェントが「成功数は何個か」を抽出するのに力を使う

### 良い例（JSON）

```python
# ✅ JSON 構造化
import json
result = {
    "status": "success",
    "summary": {
        "processed": success_count,
        "failed": failed_count,
        "elapsed_seconds": elapsed_time
    }
}
print(json.dumps(result))
```

**メリット**
- `jq` で簡単にフィルタ可能
- 別スクリプトと連携容易
- エージェントが構造を理解可能

#### データと診断の分離

```python
# ✅ データは stdout、診断は stderr
print(json.dumps(results), file=sys.stdout)  # 構造化データ
print(f"Processed {count} items in {elapsed}s", file=sys.stderr)  # 進捗情報
```

**効果**
- エージェント：stdout を次のステップに渡す
- ユーザー：stderr で進捗を確認

---

## 原則4：べき等性（Idempotency）

### エージェントは再試行する

スクリプトが失敗した場合、エージェントは同じコマンドを再実行する可能性があります。

```
実行1: create_backup.py
  → ディスク満杯でエラー

エージェント「失敗した。もう一度試そう」

実行2: create_backup.py  
  ← 前回のバックアップは？重複する？
```

### 悪い実装（非べき等）

```python
# ❌ 2回実行すると2つのバックアップができる
def backup_database():
    timestamp = datetime.now().isoformat()
    backup_file = f"backup_{timestamp}.sql"
    create_backup(backup_file)
    print("Backup created")
```

### 良い実装（べき等）

```python
# ✅ 何度実行しても同じ結果
def backup_database():
    backup_file = "latest_backup.sql"
    
    # 既に存在していたら上書き
    if os.path.exists(backup_file):
        os.remove(backup_file)
    
    create_backup(backup_file)
    print(f"Backup saved to {backup_file}")
```

### パターン：「create if not exists」

```python
def ensure_config():
    config_file = ".config/settings.json"
    
    if os.path.exists(config_file):
        # 既存設定を使用
        with open(config_file) as f:
            config = json.load(f)
        print(f"Using existing config: {config_file}")
    else:
        # 新規作成
        config = create_default_config()
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f)
        print(f"Created new config: {config_file}")
    
    return config
```

---

## 原則5：明示的なパラメータ

### 「魔法の数字」を避ける

```python
# ❌ なぜ 47？
TIMEOUT = 47
MAX_RETRIES = 5
BATCH_SIZE = 100

# ✅ 理由を説明
# HTTP リクエストは通常 30 秒以内に完了
# より長いタイムアウトは低速接続対応
REQUEST_TIMEOUT = 30

# 3 リトライが大多数の一時的エラーを解決
# 3 回以上は時間の無駄
MAX_RETRIES = 3

# バッチ処理：メモリ使用とスループッドのバランス
# 100 件でメモリ効率と処理速度のベストバランス
BATCH_SIZE = 100
```

---

## 原則6：明確な出力形式定義

### SKILL.md での説明

```markdown
## 補助スクリプト

Run these scripts to perform specific tasks:

### validate_input.py

Validates data format and structure.

**Usage:**
\`\`\`bash
python scripts/validate_input.py input.csv
\`\`\`

**Output format (JSON):**
\`\`\`json
{
  "valid": true,
  "rows": 1000,
  "columns": ["id", "name", "email"],
  "encoding": "utf-8",
  "issues": []
}
\`\`\`

**Exit codes:**
- 0: Valid
- 1: Invalid format
- 2: File not found
- 3: Encoding error
```

**例**
```markdown
### process_data.py

Processes CSV and outputs cleaned result.

**Usage:**
\`\`\`bash
python scripts/process_data.py --input raw.csv --output clean.csv --strict
\`\`\`

**Output:**
- Cleaned CSV file
- Summary printed to stdout:
  \`\`\`json
  {"processed": 1000, "removed": 23, "warnings": 5}
  \`\`\`
```

---

## 原則7：入力制約の明示

### 許可・禁止を明確に

```python
def process_image(image_path):
    ALLOWED_EXTENSIONS = ['.jpg', '.png', '.gif', '.webp']
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported image format: {ext}\n"
            f"Supported: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    if os.path.getsize(image_path) > 50_000_000:  # 50MB
        raise ValueError(
            f"Image too large: {os.path.getsize(image_path)} bytes\n"
            "Maximum file size: 50MB"
        )
    
    return process(image_path)
```

---

## 原則8：ドライラン（事前確認）

### 破壊的な操作に対して

```python
parser.add_argument('--dry-run', action='store_true',
                    help='Show what would be done without making changes')

if args.dry_run:
    print("DRY RUN MODE - No changes will be made\n")
    print(f"Would delete: {files_to_delete}")
    print(f"Would modify: {files_to_modify}")
    sys.exit(0)

# 実際の削除・修正処理
apply_changes(files_to_delete, files_to_modify)
```

---

## 原則9：意味のある終了コード

```python
#!/usr/bin/env python3

try:
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)  # File not found
    
    if not validate_format(input_file):
        print(f"Error: Invalid format", file=sys.stderr)
        sys.exit(2)  # Invalid format
    
    if not has_permission(output_dir):
        print(f"Error: Permission denied: {output_dir}", file=sys.stderr)
        sys.exit(3)  # Permission error
    
    result = process(input_file)
    save_result(result, output_dir)
    
    sys.exit(0)  # Success
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(255)  # Unexpected error
```

**エージェント側の処理**
```
成功（exit 0）
└─ 結果を解釈して次へ

ファイルなし（exit 1）
└─ ファイル名を修正して再実行

形式エラー（exit 2）
└─ 入力形式の修正を提案

権限エラー（exit 3）
└─ 権限の確認を提案

予期しないエラー（exit 255）
└─ エージェントに任せる
```

---

## 実装例：完全なスクリプト

```python
#!/usr/bin/env python3
"""
Process and validate CSV files.

More info: python scripts/csv_processor.py --help
"""

import argparse
import json
import sys
import os
from pathlib import Path

# 設定（理由付き）
# CSV の 1 行当たり平均 100 バイト程度、メモリ効率と処理速度のバランス
BATCH_SIZE = 1000

# CSV ファイルの最大サイズ。超える場合は事前フィルタを提案
MAX_FILE_SIZE = 500_000_000  # 500MB


def validate_input_file(filepath):
    """Input ファイルが有効か確認"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    if not filepath.endswith('.csv'):
        raise ValueError(f"Expected CSV file, got: {filepath}")
    
    size = os.path.getsize(filepath)
    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large ({size} bytes). "
            f"Maximum size: {MAX_FILE_SIZE} bytes. "
            f"Consider splitting the file."
        )
    
    if size == 0:
        raise ValueError("Input file is empty")


def process_csv(input_path, output_path, remove_duplicates=False):
    """CSV を処理"""
    validate_input_file(input_path)
    
    result = {
        "status": "success",
        "input_file": input_path,
        "output_file": output_path,
        "statistics": {
            "rows_processed": 0,
            "rows_removed": 0,
            "warnings": []
        }
    }
    
    try:
        # 処理実装（省略）
        with open(input_path) as f:
            lines = f.readlines()
        
        result["statistics"]["rows_processed"] = len(lines)
        
        # 結果を保存
        with open(output_path, 'w') as f:
            for line in lines:
                f.write(line)
        
        return result
    
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Process and validate CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/csv_processor.py data.csv
  python scripts/csv_processor.py --input raw.csv --output clean.csv --dedup
  python scripts/csv_processor.py --dry-run data.csv

Output format:
  JSON to stdout containing: status, statistics, errors (if any)
  Progress messages to stderr

Exit codes:
  0: Success
  1: File not found / Invalid input
  2: Format error / Invalid option
  3: Permission denied
  255: Unexpected error
        """
    )
    
    parser.add_argument('input', nargs='?', default=None, help='Input CSV file')
    parser.add_argument('--input', dest='input_arg', help='Input file (alternative)')
    parser.add_argument('--output', default=None, help='Output file (default: stdout)')
   parser.add_argument('--dedup', action='store_true', help='Remove duplicate rows')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    
    args = parser.parse_args()
    
    # 入力ファイルの確定
    input_file = args.input or args.input_arg
    if not input_file:
        parser.print_help()
        sys.exit(2)
    
    # ドライラン
    if args.dry_run:
        print(f"DRY RUN: Would process {input_file}", file=sys.stderr)
        result = {
            "status": "dry_run",
            "input_file": input_file,
            "would_output": args.output or "stdout"
        }
        print(json.dumps(result))
        sys.exit(0)
    
    try:
        validate_input_file(input_file)
        output_file = args.output or "-"  # "-" は stdout を意味する
        
        result = process_csv(input_file, output_file, remove_duplicates=args.dedup)
        
        # 結果をJSON で出力
        print(json.dumps(result))
        
        # 進捗・統計を stderr に出力
        print(f"Processed {result['statistics']['rows_processed']} rows", file=sys.stderr)
        
        sys.exit(0)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except PermissionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(255)


if __name__ == '__main__':
    main()
```

---

## チェックリスト

### スクリプト設計
- [ ] 非インタラクティブ（コマンドフラグ・環境変数のみ）
- [ ] `--help` が充実したドキュメント
- [ ] エラーメッセージが具体的・改善提案を含む
- [ ] 構造化出力（JSON/CSV）
- [ ] stdoutデータ・stderrログを分離
- [ ] べき等性（何度実行しても安全）
- [ ] 入力制約を明示（許可形式・サイズ制限）
- [ ] ドライラン対応（破壊的操作の場合）
- [ ] 意味のある終了コード（0=success、1-3=具体的エラー、255=予期外）

### SKILL.md での説明
- [ ] スクリプト一覧（available scripts セクション）
- [ ] 各スクリプトの使い方（bash コマンド例）
- [ ] 出力形式を明記（JSON/CSV 例+スキーマ）
- [ ] ワークフロー内でのスクリプト呼び出し順序
- [ ] エラーハンドリング（失敗時の対応）

---

## 関連資料

- [agentskills.io - Using scripts in skills](https://agentskills.io/skill-creation/using-scripts)
- [PEP 723 - Inline script metadata](https://peps.python.org/pep-0723/)
- Part 3-6: スキル評価フレームワーク（テスト実装例）
