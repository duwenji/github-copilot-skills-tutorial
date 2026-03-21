# Copilot Instructions

このリポジトリでは、クイズ生成と電子書籍生成を shared-copilot-skills 経由で実行する。

## Quiz Generator
- 入口: `.github/skills-config/quiz-generator/invoke-validate.ps1`
- 設定: `.github/skills-config/quiz-generator/quiz-generator.config.json`
- 推奨モード: `-Mode all`
- 生成物配置: `quiz-output/`

## Ebook Build
- 入口: `.github/skills-config/ebook-build/invoke-build.ps1`
- 設定: `.github/skills-config/ebook-build/github-copilot-skills-tutorial.build.json`
- メタデータ: `.github/skills-config/ebook-build/github-copilot-skills-tutorial.metadata.yaml`

## Shared skill discovery order
1. `.github/skills/shared-copilot-skills/*`
2. `.github/skills/*`
3. `../shared-copilot-skills/*`
