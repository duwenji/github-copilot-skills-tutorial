# Copilot Instructions

このリポジトリでは、電子書籍生成を shared-copilot-skills 経由で実行する。

## Ebook Build
- 入口: `.github/skills-config/ebook-build/invoke-build.ps1`
- 設定: `.github/skills-config/ebook-build/github-copilot-skills-tutorial.build.json`
- メタデータ: `.github/skills-config/ebook-build/github-copilot-skills-tutorial.metadata.yaml`

## Shared skill discovery order
1. `.github/skills/shared-skills/*`
2. `.github/skills/*`
3. `../shared-copilot-skills/*`
