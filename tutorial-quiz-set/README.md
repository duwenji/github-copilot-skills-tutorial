# GitHub Copilot Agent Skills チュートリアル - 学習用クイズセット

## 📊 生成レポート

- **生成日時**: 2026年3月8日
- **対象ドキュメント**: docs/ フォルダ全体（6セクション、20ドキュメント）
- **難度レベル**: Intermediate（中級者向け）
- **出力形式**: JSON
- **セクション数**: 5
- **総設問数**: 137問

---

## 🎯 セクション一覧

### Section 1: スキル形式の理解（Fundamentals）
- **問題数**: 16問
- **学習時間**: 約25分
- **主要トピック**:
  - Agent Skills のオープンスタンダード性
  - SKILL.md と JSON フォーマットの使い分け
  - サポートプラットフォーム（Copilot Editor, CLI, VS Code）
  - 形式の進化（2024-2026）

**✅ 習得後の理解度**: Agent Skills の基本形式と標準化、複数プラットフォーム対応について正確に判断できる

---

### Section 2: Agent Skills の基礎（Basics）
- **問題数**: 17問
- **学習時間**: 約28分
- **主要トピック**:
  - Agent Skills の定義と役割
  - 従来のプロンプト手法との 9 つの比較軸
  - スキルの構成要素
  - 再利用性、チーム共有、スケーラビリティ

**✅ 習得後の理解度**: Agent Skills の基本概念と従来方法との差異、実装の重要性が理解できる

---

### Section 3: 比較・メリット・デメリット（Comparison）
- **問題数**: 17問
- **学習時間**: 約24分
- **主要トピック**:
  - MCP（Model Context Protocol）との違い
  - プロンプトチェーニング、RAG との比較
  - Agent Skills の 10 つのメリット
  - 10 つのデメリットと対策

**✅ 習得後の理解度**: Agent Skills を他技術と相対的に評価でき、適切な使い分がはできる

---

### Section 4: スキル構造と実装（Implementation）
- **問題数**: 17問
- **学習時間**: 約26分
- **主要トピック**:
  - スキル定義ファイルの全構造
  - メタデータ（metadata）の詳細
  - パラメータ定義（parameters）
  - プロンプト（prompt）セクションの役割
  - 出力フォーマット（outputFormat）と検証（validation）

**✅ 習得後の理解度**: スキル定義ファイルの各セクションを正確に設計・実装できる

---

### Section 5: スキル管理とライフサイクル（Advanced）
- **問題数**: 15問
- **学習時間**: 約23分
- **主要トピック**:
  - スキルのライフサイクル：5 ステージ（Draft → Beta → Published → Mature → Deprecated）
  - 各ステージの期間、目的、成果物
  - バージョニング戦略
  - チーム共有とドキュメント化
  - マーケットプレイス公開の前提条件

**✅ 習得後の理解度**: スキルを設計から廃止まで、チームで適切に管理できる

---

## 📈 統計情報

| 指標 | 数値 |
|------|------|
| **総設問数** | 137問 |
| **セクション数** | 5セクション |
| **難度分布** | Intermediate 100% |
| **問題形式** | 全て 4 択一問一答 |
| **総学習時間** | 約126分（2時間 6分） |
| **平均ファイルサイズ** | 約15-20KB/セクション |

---

## 🎓 学習パス推奨

### Beginner 向けの学習順序
1. **Section 1: スキル形式の理解**（基礎用語の習得）
2. **Section 2: Agent Skills の基礎**（基本概念の理解）
3. **Section 3: 比較・メリット・デメリット**（実務での使いわけ判断）

**学習時間**: 約77分（1時間 17分）

### Intermediate（全体理解）向けの学習順序
1. Section 1, 2, 3（上記と同じ）
2. **Section 4: スキル構造と実装**（スキル設計・実装スキルの習得）
3. **Section 5: スキル管理とライフサイクル**（運用・チーム管理の習得）

**学習時間**: 約126分（2時間 6分）

### Advanced（エキスパート向け）
- すべてのセクション + サンプルコード分析・実装（本チュートリアルの Part 3-3, 3-4, 3-5）

---

## 📝 クイズセットの使用方法

### シナリオ 1: 自己学習
```
1. Section 1 から順番に進める
2. 各セクション終了後、自分のスコアを記録
3. 不正解だった問題についてドキュメント ( docs/ ) を復習
```

### シナリオ 2: チーム研修
```
1. チーム全体で Section 1 をまず実施（基礎揃合わせ）
2. 個々に Section 2-5 を学習
3. 全員が終了後、グループディスカッション（Section 3 の「メリット・デメリット」が効果的）
```

### シナリオ 3: 認定資格試験
```
1. すべてセクションを学習完了
2. ランダムに 50 問を抽出
3. 80% 以上で「GitHub Copilot Agent Skills 中級者認定」可能
```

---

## 📂 ファイル構成

```
tutorial-quiz-set/
├── metadata.json                  ← 全体メタデータ
├── README.md                      ← このファイル
├── fundamentals/
│   └── quiz.json                  ← Section 1 クイズ（16問）
├── basics/
│   └── quiz.json                  ← Section 2 クイズ（17問）
├── comparison/
│   └── quiz.json                  ← Section 3 クイズ（17問）
├── implementation/
│   └── quiz.json                  ← Section 4 クイズ（17問）
└── advanced/
    └── quiz.json                  ← Section 5 クイズ（15問）
```

---

## 🔍 クイズ形式の詳細

### 問題形式
- **形式**: 4 択一問一答（Multiple Choice）
- **正解数**: 1 個（isCorrect: true）
- **構成要素**:
  - `id`: 一意の問題識別子（セクション_番号）
  - `question`: 問題文
  - `type`: "multiple_choice"
  - `options`: 4 つの選択肢（id, text, isCorrect（オプション））
  - `explanation`: 詳しい解説

### JSON 構造例
```json
{
  "id": "basics_001",
  "question": "GitHub Copilot Agent Skills の最も基本的な定義としてはどれですか？",
  "type": "multiple_choice",
  "options": [
    {
      "id": "A",
      "text": "選択肢 A"
    },
    {
      "id": "B",
      "text": "正解の選択肢",
      "isCorrect": true
    },
    // ...
  ],
  "explanation": "詳しい解説ここに記述"
}
```

---

## 💡 使用上のコツ

1. **時間制限なし**: 各セクションは「理解度重視」なので時間制限不要
2. **段階的学習**: いきなり Section 5 ではなく、Section 1 から進める
3. **暗記ではなく理解**: 選択肢の「説明」部分をしっかり読む
4. **実践と組み合わせ**: クイズ学習 + サンプル実装（docs/03 参照）がおすすめ
5. **グループ学習**: Section 3 の「メリット・デメリット」はチーム議論が効果的

---

## 🎁 付属资源

このクイズセットは以下と組み合わせての学習が効果的です：

- **チュートリアル本体**: `docs/` 全体
- **サンプルスキル実装**:
  - `docs/03-implementation/03-sample-code-analysis.md`
  - `docs/03-implementation/04-sample-doc-generation.md`
  - `docs/03-implementation/05-sample-test-generation.md`
- **実装リファレンス**: `samples/` フォルダのスキル定義

---

## 📞 フィードバック

クイズセットについてのご意見・ご不明な点は、以下をご確認ください：
- 本チュートリアルの README: [README.md](../../README.md)
- Agent Skills 公式仕様: https://agentskills.io/

---

**Generated**: 2026年3月8日
**Version**: 1.0.0
**License**: MIT
