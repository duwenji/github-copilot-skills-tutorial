# Contributing

このリポジトリへの改善提案や修正は歓迎します。

## 基本方針
- 再利用しやすい Skill 設計と説明を優先してください。
- サンプルは学習者がすぐ試せる形を意識してください。
- 大きな構成変更は `Issue` で背景共有してから進めてください。

## 推奨フロー
1. `Issue` を作成する
2. branch を切る
3. `docs/`、`assets/`、`samples/` を必要に応じて更新する
4. `./.github/skills-config/ebook-build/invoke-build.ps1` を実行する
5. `VALIDATION_CHECKLIST.md` を確認する
6. `Pull Request` を作成する

## レビュー観点
- Skill の考え方やフォルダ構成の説明が明確か
- サンプルが再現可能か
- リンク切れや構成崩れがないか
- チーム導入時の運用観点が十分か
