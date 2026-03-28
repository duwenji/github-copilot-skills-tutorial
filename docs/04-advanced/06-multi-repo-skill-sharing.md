# Part 4-6: 複数リポでの SKILL 共通化（実装ガイド）

同一の SKILL を複数のリポジトリで共有・再利用するための実装パターンを解説します。

[Part 4-1: チーム内スキル共有戦略](01-team-sharing.md) の「戦略・方針」に対して、本章では **手を動かせる実装手順** を提供します。

---

## この章の進め方（再編版）

最短で理解したい場合は、次の順で読み進めてください。

1. 「5分クイック導線」で方式を決める
2. 「シナリオ別おすすめ」で採用理由を確認する
3. 採用した方式の実装手順を実行する
4. 「失敗駆動ハンズオン」で運用時の詰まりどころを先に潰す
5. 「運用ポリシー」でチームルールを固定する

---

## 5分クイック導線: どのパターンを選ぶか

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

## シナリオ別おすすめ（先に結論）

| 代表シナリオ | 推奨パターン | 理由 |
|---|---|---|
| まず 1 人で試したい | Personal Skills | 設定最小で検証速度が最も高い |
| 複数リポで同じ版を厳密管理したい | Git submodule | 参照コミットを明示して安全に更新できる |
| 利用側の clone / CI を単純化したい | Git subtree | 利用者側の追加設定が不要 |
| 共通スクリプトを複数リポで使い回したい | Config 駆動設計 + 上記いずれか | 差分を設定ファイルに分離できる |

---

## 実装パターン詳細

以下は方式ごとの実装手順です。採用方式だけ先に実装して問題ありません。

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
  .github/skills/shared-skills
git commit -m "feat: add shared-skills submodule"
git push
```

> 重要: `git submodule` はリポジトリ単位で取り込むため、`my-skill` のような個別スキルのみを選択して導入することはできません。導入対象は `shared-skills` リポジトリ全体です。

### 手順: 更新フロー（中央リポで更新 → 業務リポへ反映）

```bash
# 1. 中央リポでスキルを更新
cd shared-skills
# SKILL.md を編集...
git add . && git commit -m "fix: update procedure" && git push

# 2. 業務リポ側で同期
cd repo-A
git submodule update --remote --merge .github/skills/shared-skills
git add .github/skills/shared-skills
git commit -m "chore: update shared-skills to latest"
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

## 失敗駆動ハンズオン（submodule）

実運用で発生しやすい失敗を、意図的に再現して復旧手順を確認します。

### 演習A: clone 後に `.github/skills` が空になる

**症状**

- `git clone` 後に `.github/skills` が空、または期待ファイルが見えない

**確認**

```bash
git submodule status
```

**復旧**

```bash
git submodule update --init --recursive
```

**再発防止**

- 新規 clone は `git clone --recurse-submodules ...` を標準化する
- CI は `actions/checkout` に `submodules: recursive` を必須化する

### 演習B: 共有側を更新したのに利用側で反映されない

**症状**

- shared-skills 側は更新済みだが、業務リポに変更が現れない

**確認**

```bash
git submodule status
git diff -- .github/skills/shared-skills
```

**復旧**

```bash
git submodule update --remote --merge .github/skills/shared-skills
git add .github/skills/shared-skills
git commit -m "chore: update shared-skills submodule pointer"
```

**再発防止**

- 「共有リポ更新」と「利用リポのポインタ更新」を別タスクとして管理する
- PR テンプレートに「submodule pointer update 確認」チェックを追加する

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
# 業務リポに shared-skills 全体を subtree として追加
cd repo-A
git subtree add \
  --prefix=.github/skills/shared-skills \
  https://github.com/<org>/shared-skills.git main \
  --squash
git push
```

> `--squash` を付けると、中央リポの細かいコミット履歴を業務リポに持ち込まずに済みます。
>
> 重要: このコマンドは `shared-skills` リポジトリ全体を取り込みます。`my-skill` のような 1 つのスキルだけを直接 `.github/skills/my-skill` に配置するわけではありません。
>
> たとえば中央リポが次の構造なら:
>
> ```text
> shared-skills/
> ├── my-skill/
> │   └── SKILL.md
> └── another-skill/
>     └── SKILL.md
> ```
>
> 業務リポでは次のように展開されます:
>
> ```text
> .github/skills/shared-skills/my-skill/SKILL.md
> .github/skills/shared-skills/another-skill/SKILL.md
> ```

### 手順: 更新フロー（中央リポが更新されたとき）

```bash
cd repo-A
git subtree pull \
  --prefix=.github/skills/shared-skills \
  https://github.com/<org>/shared-skills.git main \
  --squash
git push
```

### 1 つのスキルだけを取り込みたい場合

`git subtree` 単体では、相手リポジトリの一部ディレクトリだけを直接取り込む運用には向きません。`shared-skills` が複数スキルを持つ単一リポジトリである場合、1 スキルだけを `.github/skills/my-skill` に置きたいなら、先にそのディレクトリを独立ブランチとして切り出します。

```bash
# shared-skills 側: my-skill ディレクトリだけの履歴を切り出す
cd shared-skills
git subtree split --prefix=my-skill -b my-skill-branch
git push origin my-skill-branch
```

```bash
# repo-A 側: 切り出したブランチを 1 スキルとして取り込む
cd repo-A
git subtree add \
  --prefix=.github/skills/my-skill \
  https://github.com/<org>/shared-skills.git my-skill-branch \
  --squash
git push
```

この方式なら、業務リポ側の配置は次のようにシンプルになります。

```text
.github/skills/my-skill/SKILL.md
.github/skills/my-skill/scripts/...
```

更新時も同じブランチを pull します。

```bash
cd repo-A
git subtree pull \
  --prefix=.github/skills/my-skill \
  https://github.com/<org>/shared-skills.git my-skill-branch \
  --squash
git push
```

> 補足: 1 スキルごとに独立リポジトリを作れるなら、その方が `submodule` / `subtree` ともに運用は単純です。`subtree split` は「中央では 1 リポにまとめたいが、利用側では個別導入したい」場合の折衷案です。

### URL を毎回書かないための設定（任意）

`remote` として別名を登録しておくと便利です。

```bash
git remote add shared-skills https://github.com/<org>/shared-skills.git

# shared-skills 全体を取り込む場合
git subtree pull --prefix=.github/skills/shared-skills shared-skills main --squash

# 1 スキル用に split 済みブランチを使う場合
git subtree pull --prefix=.github/skills/my-skill shared-skills my-skill-branch --squash
```

### メリット・デメリット

| 項目 | 内容 |
|------|------|
| ✅ クローン設定不要 | 通常の `git clone` でそのまま使える |
| ✅ 平坦な履歴 | 業務リポの `git log` に自然に溶け込む |
| ✅ サブモジュール知識不要 | チームの git スキル差を吸収しやすい |
| ✅ 個別導入にも拡張可能 | `subtree split` 用ブランチを作れば 1 スキル単位にもできる |
| ❌ 逆方向の push が複雑 | 業務リポから中央リポへの反映は `git subtree push` が必要 |
| ❌ そのままでは個別導入できない | 単一リポに複数スキルがある場合はリポ全体を取り込む |
| ❌ 衝突時の解決が煩雑 | 大きな変更が重なると難しくなる場合がある |

**推奨シーン:** CI 設定をシンプルに保ちたい・チームの git スキルレベルが混在している

---

## パターン4: Config 駆動設計（スクリプト共通 + リポ別設定）

**パターン1〜3 と組み合わせる設計原則。**  
スクリプト本体を共通化しつつ、リポジトリ固有の値（パス・出力先・メタデータ等）は設定ファイル（JSON / YAML）に切り出します。

### 先に結論: 配置先は 2 パターンある

リポ固有設定の置き場所は、次のどちらでも構成できます。

1. 共通リポ配置版
   共通スクリプトと設定ファイルを同じ shared-skills 側で管理する方式です。
2. 利用側リポ配置版
   共通スクリプトは shared-skills 側に置き、各リポ固有の設定だけを業務リポ側に置く方式です。

一般には、リポ固有の値が多いほど「利用側リポ配置版」のほうが責務分離が明確です。逆に、設定ファイルも含めて中央管理したいなら「共通リポ配置版」が向いています。

### 方式A: 共通リポ配置版

設定ファイルも shared-skills 側に置く構成です。複数リポの設定を 1 箇所で見渡せます。

#### ディレクトリ構造

```
shared-skills/
└── my-skill/
    ├── SKILL.md
    ├── scripts/
    │   └── invoke.ps1          ← スクリプトは共通（リポ差分なし）
    ├── configs/
  │   ├── repo-A.build.json   ← repo-A 用設定
  │   └── repo-B.build.json   ← repo-B 用設定
    └── assets/
        └── style.css
```

#### 設定ファイルの例

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

  #### 呼び出し方

  ```powershell
  # repo-A 向け
  .\.github\skills\my-skill\scripts\invoke.ps1 `
    -ConfigFile .\.github\skills\my-skill\configs\repo-A.build.json

  # repo-B 向け
  .\.github\skills\my-skill\scripts\invoke.ps1 `
    -ConfigFile .\.github\skills\my-skill\configs\repo-B.build.json
  ```

  #### 向いているケース

  - 設定ファイルも中央でレビュー・配布したい
  - 利用側リポに設定ファイル配置ルールを増やしたくない
  - repo ごとの差分がまだ小さい

  #### 注意点

  - repo-A 専用設定が shared-skills に混ざるため、責務がやや曖昧になりやすい
  - 利用側リポから見て「自分専用設定の所在」が直感的でない場合がある

  ### 方式B: 利用側リポ配置版

  共通スクリプトは shared-skills に置き、repo 固有の設定は各業務リポジトリ側に置く構成です。通常はこちらのほうが設計意図が明確です。

  #### ディレクトリ構造

  ```text
  shared-skills/
  └── my-skill/
    ├── SKILL.md
    ├── scripts/
    │   └── invoke.ps1          ← スクリプトは共通
    └── assets/
      └── style.css

  repo-A/
  └── .github/
    ├── skills/
    │   └── my-skill/
    │       ├── SKILL.md
    │       ├── scripts/
    │       └── assets/
    └── skill-configs/
      └── my-skill/
        └── repo-A.build.json
  ```

  #### 設定ファイルの例

  ```json
  // .github/skill-configs/my-skill/repo-A.build.json
  {
    "sourceRoot":    ".",
    "outputDir":     "./output",
    "projectName":   "repo-a-product",
    "metadataFile":  "./.github/skill-configs/my-skill/repo-A.metadata.yaml",
    "styleFile":     "./.github/skills/my-skill/assets/style.css"
  }
  ```

  #### 呼び出し方

  ```powershell
  # repo-A 側に置いた設定を渡す
  .\.github\skills\my-skill\scripts\invoke.ps1 `
    -ConfigFile .\.github\skill-configs\my-skill\repo-A.build.json
  ```

  #### 向いているケース

  - リポごとのパスや出力先が大きく異なる
  - repo 固有設定をその repo の PR で閉じて管理したい
  - 共通リポに repo 個別事情を持ち込みたくない

  #### 注意点

  - 利用側リポごとに設定ファイル配置ルールをチームで統一する必要がある
  - SKILL.md や運用ドキュメントで、設定ファイルの想定配置先を明記する必要がある

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

エージェントから実行するときも、SKILL.md に「`-ConfigFile` を指定してください」と動作手順として明記しておくと自動実行精度が上がります。

### 設計のコツ

```
✅ DO   スクリプトにリポ名やパスをハードコードしない
✅ DO   設定ファイルに「何が違うか」だけを書く
✅ DO   配置先を決めたら命名規則を統一する
     例: shared 側なら configs/<repo-name>.build.json
     例: 利用側なら .github/skill-configs/<skill-name>/<repo-name>.build.json
✅ DO   スクリプトは引数なしで実行したときにヘルプを表示する

❌ AVOID if ($projectName -eq "repo-A") { ... } とスクリプト内で分岐する
❌ AVOID デフォルト値に特定リポのパスを埋め込む
❌ AVOID SKILL.md に環境依存の絶対パスを書く
```

---

## 運用ポリシー（実運用で迷わないために）

実運用ルールは次のドキュメントを正としてください。

- [shared-copilot-skills README](../../.github/skills/README.md)
- [OPERATIONS](../../.github/skills/docs/OPERATIONS.md)

最低限の統一ルール:

- shared 側の変更は shared リポジトリで先に確定する
- 利用側は submodule ポインタ更新を PR で明示する
- `.gitignore` で `.github/skills` の変更を隠して管理しない

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
  → shared 側の configs/ または利用側リポの設定ファイルに分離されている
□ チャットで / 入力時にスキル名が表示される
□ 自然文のリクエスト（「〇〇を△△したい」）で自動ロードされる
□ submodule の場合: CI/CD に submodules: recursive が設定されている
```

---

→ 前へ: [Part 4-5: スクリプト設計ベストプラクティス](05-scripts-best-practices.md)  
→ 次へ: [Part 5-1: 複合スキルと高度なパターン](../05-advanced-topics/01-composite-skills.md)
