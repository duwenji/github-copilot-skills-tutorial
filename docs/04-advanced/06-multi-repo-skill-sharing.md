# Part 4-6: 複数リポでの SKILL 共通化（実装ガイド）

同一の SKILL を複数のリポジトリで共有・再利用するための実装パターンを解説します。

[Part 4-1: チーム内スキル共有戦略](01-team-sharing.md) の「戦略・方針」に対して、本章では **手を動かせる実装手順** を提供します。

---

## どのパターンを選ぶか

```
個人利用のみ？
  │
  YES → パターン1: Personal Skills（最短・設定不要）
  │
  NO
  │
チームで使う？（複数メンバー）
  │
  YES
  │
  ├─ 更新を中央リポジトリで一元管理したい？
  │    YES → パターン2: Git submodule（版を固定して配布）
  │    NO  → パターン3: Git subtree（クローン設定不要でシンプル）
  │
  └─ さらに: スクリプト共通 × リポ別設定に分離したい？
           → パターン4: Config 駆動設計（上 3 つと組み合わせ可）
```

### submodule と subtree のコンセプト早見表

| 観点 | Git submodule | Git subtree |
|------|----------------|-------------|
| 正体 | 別リポジトリを「参照（特定コミット）」として保持 | 別リポジトリの内容を親リポジトリの履歴に取り込む |
| 親リポに保存されるもの | 子リポジトリの参照先コミット | 取り込まれたファイルとコミット |
| clone 時の挙動 | 追加取得が必要（`--recurse-submodules`） | 通常 clone でそのまま使える |
| バージョン固定 | 強い（参照コミットで明示） | pull タイミングで反映 |
| 運用の主な難所 | 初期化忘れ、同期忘れ | 履歴・競合解消の理解 |

この章では、submodule を「厳密な版管理」、subtree を「導入簡便性」として使い分けます。

---

## パターン1: Personal Skills（個人・全リポ共通）

**最短。設定不要。自分のマシン上の全リポジトリから同一 SKILL を参照できる。**

### 配置場所

| OS | パス |
|----|------|
| Windows | `%USERPROFILE%\.copilot\skills\<skill-name>\SKILL.md` |
| macOS / Linux | `~/.copilot/skills/<skill-name>/SKILL.md` |

### 手順

```powershell
# Windows の例
$skillName = "my-skill"
$skillDir  = "$env:USERPROFILE\.copilot\skills\$skillName"

New-Item -ItemType Directory -Force -Path $skillDir
Copy-Item .\path\to\SKILL.md "$skillDir\SKILL.md"
# スクリプトや補助ファイルもここに置く
Copy-Item .\path\to\scripts "$skillDir\scripts" -Recurse
```

```bash
# macOS / Linux の例
SKILL_NAME="my-skill"
mkdir -p ~/.copilot/skills/$SKILL_NAME
cp ./path/to/SKILL.md ~/.copilot/skills/$SKILL_NAME/SKILL.md
cp -r ./path/to/scripts ~/.copilot/skills/$SKILL_NAME/scripts
```

スクリプトや参照ファイルも同フォルダ配下に置き、SKILL.md からは `./scripts/...` の相対パスで参照します。

### 動作確認

VS Code Copilot Chat でチャット入力欄に `/` を入力し、スキル名が表示されることを確認します。表示されない場合はフォルダ名と SKILL.md の `name` フィールドが一致しているか確認してください。

### メリット・デメリット

| 項目 | 内容 |
|------|------|
| ✅ 設定不要 | git や submodule の設定が一切不要 |
| ✅ 即時反映 | リポジトリをまたいで自動参照される |
| ✅ 試しやすい | プロトタイプを素早く検証できる |
| ❌ 個人マシン限定 | チームメンバーには届かない |
| ❌ バージョン管理外 | 変更履歴を git で追いにくい |

**推奨シーン:** 個人の生産性向上スキル、まず動かして試すプロトタイプ

---

## パターン2: Git submodule（チーム共有・中央管理）

**SKILL 専用リポジトリを 1 つ作成し、各業務リポに submodule として取り込む。**  
更新は中央リポジトリで行い、各業務リポは `git submodule update --remote` で同期します。

### コンセプト（先にここだけ理解する）

submodule は「フォルダそのものを共有」する方式ではなく、親リポジトリが「別リポジトリのどのコミットを参照するか」を持つ方式です。

```
中央リポを更新
  ↓
業務リポは自動追従しない
  ↓
必要なタイミングで update --remote して追従
```

この性質により、業務リポごとに異なるバージョンを安全に運用できます。

### ディレクトリ構造

```
shared-skills/              ← SKILL 専用リポジトリ（中央管理）
├── my-skill/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── invoke.ps1
│   └── assets/
└── another-skill/
    └── SKILL.md

repo-A/                     ← 業務リポジトリ A
├── .github/
│   └── skills/
│       └── my-skill/       ← submodule として取り込み
├── src/
└── ...

repo-B/                     ← 業務リポジトリ B
├── .github/
│   └── skills/
│       └── my-skill/       ← 同じ submodule（独立したポインタで版管理）
└── ...
```

### 手順: 初回セットアップ

```bash
# Step 1: 専用リポジトリを作成（一度だけ）
mkdir shared-skills && cd shared-skills
git init
mkdir -p my-skill/scripts

# SKILL.md を作成して...
git add .
git commit -m "feat: add my-skill"
git remote add origin https://github.com/<org>/shared-skills.git
git push -u origin main
```

```bash
# Step 2: 各業務リポにサブモジュールとして追加（リポごとに一度だけ）
cd repo-A
git submodule add \
  https://github.com/<org>/shared-skills.git \
  .github/skills/my-skill
git commit -m "feat: add shared my-skill as submodule"
git push
```

### 手順: 更新フロー（中央リポで更新 → 業務リポへ反映）

```bash
# 1. 中央リポでスキルを更新
cd shared-skills
# SKILL.md を編集...
git add . && git commit -m "fix: update procedure" && git push

# 2. 業務リポ側で同期
cd repo-A
git submodule update --remote --merge .github/skills/my-skill
git add .github/skills/my-skill
git commit -m "chore: update my-skill to latest"
git push
```

### 注意: クローン時の設定

submodule を含むリポジトリをクローンした人は以下が必要です。

```bash
# 最初から submodule を含めてクローン
git clone --recurse-submodules https://github.com/<org>/repo-A.git

# または既存クローン後に初期化
git submodule update --init --recursive
```

CI/CD（GitHub Actions 等）でも `actions/checkout` に `submodules: recursive` を追加してください。

```yaml
- uses: actions/checkout@v4
  with:
    submodules: recursive
```

### メリット・デメリット

| 項目 | 内容 |
|------|------|
| ✅ バージョン固定 | 業務リポで使う版を明示的にピン留めできる |
| ✅ 中央管理 | 更新は専用リポ 1 箇所で行える |
| ✅ CI/CD 統合 | GitHub Actions 等と組み合わせやすい |
| ❌ クローン設定が必要 | `--recurse-submodules` を忘れると空フォルダになる |
| ❌ 手動同期 | 各リポで `update --remote` の実行が必要 |

**推奨シーン:** バージョンを厳密に管理したい組織・大規模チーム・CI/CD 統合が必要

---

## パターン3: Git subtree（チーム共有・シンプル）

**`git subtree` で SKILL ファイルを業務リポジトリの歴史として直接取り込む。**  
submodule と異なり、クローンする人に特別な設定が不要なのが最大のメリットです。

### コンセプト（先にここだけ理解する）

subtree は「参照」ではなく「取り込み」です。親リポジトリにファイル実体と履歴を取り込むため、利用側は通常の clone だけで利用できます。

```
中央リポを更新
  ↓
業務リポで subtree pull
  ↓
取り込みコミットとして反映
```

この性質により、導入時のハードルは下がりますが、履歴の扱いと競合解消はやや重くなります。

### 手順: 初回セットアップ

```bash
# 業務リポに shared-skills の内容を subtree として追加
cd repo-A
git subtree add \
  --prefix=.github/skills/my-skill \
  https://github.com/<org>/shared-skills.git main \
  --squash
git push
```

> `--squash` を付けると、中央リポの細かいコミット履歴を業務リポに持ち込まずに済みます。

### 手順: 更新フロー（中央リポが更新されたとき）

```bash
cd repo-A
git subtree pull \
  --prefix=.github/skills/my-skill \
  https://github.com/<org>/shared-skills.git main \
  --squash
git push
```

### URL を毎回書かないための設定（任意）

`remote` として別名を登録しておくと便利です。

```bash
git remote add shared-skills https://github.com/<org>/shared-skills.git

# 以後はこれだけで済む
git subtree pull --prefix=.github/skills/my-skill shared-skills main --squash
```

### メリット・デメリット

| 項目 | 内容 |
|------|------|
| ✅ クローン設定不要 | 通常の `git clone` でそのまま使える |
| ✅ 平坦な履歴 | 業務リポの `git log` に自然に溶け込む |
| ✅ サブモジュール知識不要 | チームの git スキル差を吸収しやすい |
| ❌ 逆方向の push が複雑 | 業務リポから中央リポへの反映は `git subtree push` が必要 |
| ❌ 衝突時の解決が煩雑 | 大きな変更が重なると難しくなる場合がある |

**推奨シーン:** CI 設定をシンプルに保ちたい・チームの git スキルレベルが混在している

---

## パターン4: Config 駆動設計（スクリプト共通 + リポ別設定）

**パターン1〜3 と組み合わせる設計原則。**  
スクリプト本体を共通化しつつ、リポジトリ固有の値（パス・出力先・メタデータ等）は設定ファイル（JSON / YAML）に切り出します。

### ディレクトリ構造

```
shared-skills/
└── my-skill/
    ├── SKILL.md
    ├── scripts/
    │   └── invoke.ps1          ← スクリプトは共通（リポ差分なし）
    ├── configs/
    │   ├── repo-A.build.json   ← リポ A の設定のみ
    │   └── repo-B.build.json   ← リポ B の設定のみ
    └── assets/
        └── style.css
```

### 設定ファイルの例

```json
// configs/repo-A.build.json
{
  "sourceRoot":    "C:/dev/apps/repo-A",
  "outputDir":     "C:/dev/apps/repo-A/output",
  "projectName":   "repo-a-product",
  "metadataFile":  "./.github/skills/my-skill/configs/repo-A.metadata.yaml",
  "styleFile":     "./.github/skills/my-skill/assets/style.css"
}
```

### スクリプトでの受け取り方（PowerShell 例）

```powershell
param(
    [Parameter(Mandatory)][string]$ConfigFile
)

$config      = Get-Content $ConfigFile | ConvertFrom-Json
$sourceRoot  = $config.sourceRoot
$outputDir   = $config.outputDir
$projectName = $config.projectName

Write-Host "Building: $projectName from $sourceRoot"
# ... 以降は $config の値だけで処理する
```

### 呼び出し方

```powershell
# リポ A 向け
.\.github\skills\my-skill\scripts\invoke.ps1 `
    -ConfigFile .\.github\skills\my-skill\configs\repo-A.build.json

# リポ B 向け（スクリプトは同一）
.\.github\skills\my-skill\scripts\invoke.ps1 `
    -ConfigFile .\.github\skills\my-skill\configs\repo-B.build.json
```

エージェントから実行するときも、SKILL.md に「`-ConfigFile` を指定してください」と動作手順として明記しておくと自動実行精度が上がります。

### 設計のコツ

```
✅ DO   スクリプトにリポ名やパスをハードコードしない
✅ DO   設定ファイルに「何が違うか」だけを書く
✅ DO   configs/<repo-name>.build.json という命名規則に統一する
✅ DO   スクリプトは引数なしで実行したときにヘルプを表示する

❌ AVOID if ($projectName -eq "repo-A") { ... } とスクリプト内で分岐する
❌ AVOID デフォルト値に特定リポのパスを埋め込む
❌ AVOID SKILL.md に環境依存の絶対パスを書く
```

---

## パターン比較まとめ

| パターン | 対象 | git 設定 | 更新方法 | 難易度 |
|---------|------|---------|---------|-------|
| **Personal Skills** | 個人 | 不要 | 手動コピー | ★☆☆ |
| **Git submodule** | チーム | 必要（clone に `--recurse`）| `submodule update --remote` | ★★★ |
| **Git subtree** | チーム | 不要 | `subtree pull` | ★★☆ |
| **Config 駆動設計** | どちらでも | —（上 3 つと組み合わせ） | —（スクリプト共通） | ★★☆ |

---

## 共通チェックリスト

SKILL を共通化・配置する前に確認してください。

```
□ SKILL.md の name フィールドとフォルダ名が一致している
□ description に「いつ使うか」「検索されるキーワード」が入っている
□ スクリプト・参照ファイルの相対パスが ./scripts/... 形式になっている
□ リポ固有の値（パス・プロジェクト名等）を SKILL.md / スクリプトに書いていない
  → configs/<repo>.json / yaml に分離されている
□ チャットで / 入力時にスキル名が表示される
□ 自然文のリクエスト（「〇〇を△△したい」）で自動ロードされる
□ submodule の場合: CI/CD に submodules: recursive が設定されている
```

---

→ 前へ: [Part 4-5: スクリプト設計ベストプラクティス](05-scripts-best-practices.md)  
→ 次へ: [Part 5-1: 複合スキルと高度なパターン](../05-advanced-topics/01-composite-skills.md)
