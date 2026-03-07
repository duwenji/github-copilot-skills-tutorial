# Part 5-2: API統合と外部ツール連携

Agent Skills で外部 API やツールと統合し、より強力な機能を実現する方法を学びます。

---

## 外部 API 統合パターン

### パターン1: LLM API への直接統合

Agent Skills は Copilot の内部 LLM を利用していますが、さらに外部 LLM API を活用することも可能です：

```json
{
  "id": "multi-llm-analysis",
  "name": "複数LLMによる分析",
  "description": "OpenAI, Claude, Gemini など複数 LLM を使用して、より信頼性の高い分析を実施",
  
  "externalAPIs": [
    {
      "id": "openai-api",
      "type": "llm",
      "endpoint": "https://api.openai.com/v1/chat/completions",
      "authenticationType": "bearer_token",
      "requiredToken": "OPENAI_API_KEY"
    },
    {
      "id": "anthropic-api",
      "type": "llm",
      "endpoint": "https://api.anthropic.com/v1/messages",
      "authenticationType": "bearer_token",
      "requiredToken": "ANTHROPIC_API_KEY"
    }
  ],
  
  "parameters": {
    "code": {
      "type": "string",
      "description": "分析対象のコード"
    },
    "useLLMs": {
      "type": "array",
      "description": "使用するLLMサービス",
      "items": {"type": "string"},
      "enum": ["copilot", "openai", "anthropic"],
      "default": ["copilot"]
    }
  },
  
  "outputFormat": {
    "type": "object",
    "schema": {
      "properties": {
        "analyses": {
          "type": "array",
          "items": {
            "properties": {
              "llm": {"type": "string"},
              "result": {"type": "object"},
              "confidence": {"type": "number"}
            }
          }
        },
        "consensus": {
          "type": "object",
          "description": "複数LLMの結果をマージした最終結果"
        }
      }
    }
  }
}
```

### 複数 LLM 統合の実装例

```python
import asyncio
from typing import List, Dict, Any

class MultiLLMAnalyzer:
    """複数 LLM による分析"""
    
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.analyzers = {
            "openai": OpenAIAnalyzer(api_keys.get("OPENAI_API_KEY")),
            "anthropic": AnthropicAnalyzer(api_keys.get("ANTHROPIC_API_KEY")),
            "copilot": CopilotAnalyzer()  # 内部LLM
        }
    
    async def analyze_with_multiple_llms(self, 
                                        code: str,
                                        llms: List[str]) -> Dict[str, Any]:
        """複数のLLMで並列分析"""
        
        tasks = []
        for llm_name in llms:
            if llm_name in self.analyzers:
                task = self._analyze_with_llm(llm_name, code)
                tasks.append(task)
        
        # 並列実行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 結果を統合
        return self._aggregate_results(results, llms)
    
    async def _analyze_with_llm(self, llm_name: str, code: str) -> Dict[str, Any]:
        """単一のLLMで分析"""
        
        analyzer = self.analyzers[llm_name]
        
        try:
            result = await analyzer.analyze(code)
            return {
                "llm": llm_name,
                "status": "success",
                "result": result,
                "confidence": self._calculate_confidence(result)
            }
        except Exception as e:
            return {
                "llm": llm_name,
                "status": "error",
                "error": str(e)
            }
    
    def _aggregate_results(self, 
                          results: List[Dict],
                          llms: List[str]) -> Dict[str, Any]:
        """複数の分析結果を統合"""
        
        successful_results = [r for r in results 
                             if r.get("status") == "success"]
        
        if not successful_results:
            return {
                "error": "All LLM analyses failed",
                "details": results
            }
        
        # コンセンサスを計算
        consensus = self._calculate_consensus(successful_results)
        
        return {
            "analyses": results,
            "consensus": consensus,
            "success_rate": len(successful_results) / len(results),
            "recommendation": self._generate_recommendation(consensus)
        }
    
    def _calculate_consensus(self, results: List[Dict]) -> Dict[str, Any]:
        """複数結果からコンセンサスを生成"""
        # スコアの平均化、投票ベースの判定等
        scores = [r['result'].get('score', 0) for r in results]
        
        return {
            "average_score": sum(scores) / len(scores),
            "high_confidence_findings": self._find_common_issues(results)
        }
    
    def _find_common_issues(self, results: List[Dict]) -> List[str]:
        """複数LLMが指摘した共通の問題"""
        # 複数LLMが同じ問題を指摘した場合、信頼度が高い
        all_issues = []
        for r in results:
            all_issues.extend(r['result'].get('issues', []))
        
        # カウント して、複数回指摘された問題をフィルタ
        from collections import Counter
        issue_counts = Counter(all_issues)
        return [issue for issue, count in issue_counts.items() 
                if count >= len(results) // 2]  # 過半数が指摘した問題
```

---

### パターン2: データベース / データソース統合

```json
{
  "id": "code-review-with-kb",
  "name": "ナレッジベース連携コードレビュー",
  "description": "組織のナレッジベースとコーディング標準を参照して、カスタマイズされたコードレビューを実施",
  
  "externalDataSources": [
    {
      "id": "knowledge-base",
      "type": "database",
      "connection": {
        "type": "rest_api",
        "baseUrl": "https://api.company.com/kb",
        "authentication": "api_key"
      },
      "queryTemplate": "/search?query={query}&limit=5"
    },
    {
      "id": "code-standards",
      "type": "configuration",
      "connection": {
        "type": "github_repo",
        "repo": "org/coding-standards",
        "branch": "main"
      }
    }
  ],
  
  "prompt": {
    "system": "You are a code reviewer with access to company knowledge base and coding standards.",
    "template": "Review this {language} code:\n{code}\n\nConsider:\n1. Company coding standards (from {coding_standards_content})\n2. Similar past issues (from knowledge base): {kb_results}\n\nProvide review with focus on: {focus_areas}"
  }
}
```

### ナレッジベース統合の実装例

```python
import aiohttp
import json
from typing import List, Dict

class KnowledgeBaseIntegration:
    """組織のナレッジベースと統合"""
    
    def __init__(self, kb_endpoint: str, api_key: str):
        self.kb_endpoint = kb_endpoint
        self.api_key = api_key
        self.kb_cache = {}
    
    async def search_knowledge_base(self, query: str, limit: int = 5) -> List[Dict]:
        """ナレッジベースで検索"""
        
        cache_key = f"{query}:{limit}"
        if cache_key in self.kb_cache:
            return self.kb_cache[cache_key]
        
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"{self.kb_endpoint}/search"
            params = {"query": query, "limit": limit}
            
            async with session.get(url, params=params, headers=headers) as resp:
                if resp.status == 200:
                    results = await resp.json()
                    self.kb_cache[cache_key] = results
                    return results
                else:
                    raise Exception(f"KB search failed: {resp.status}")
    
    async def fetch_coding_standards(self, language: str) -> str:
        """言語別のコーディング標準を取得"""
        
        cache_key = f"standards:{language}"
        if cache_key in self.kb_cache:
            return self.kb_cache[cache_key]
        
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            url = f"{self.kb_endpoint}/standards/{language}"
            
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    standards = await resp.text()
                    self.kb_cache[cache_key] = standards
                    return standards
                else:
                    return f"No standards found for {language}"
    
    async def enhance_prompt_with_knowledge(self, 
                                           template: str,
                                           code: str,
                                           language: str) -> str:
        """ナレッジベース情報を含むプロンプトを生成"""
        
        # 関連するナレッジ項目を検索
        relevant_kb = await self.search_knowledge_base(
            query=f"code review for {language}",
            limit=3
        )
        
        # コーディング標準を取得
        standards = await self.fetch_coding_standards(language)
        
        # プロンプトを拡張
        kb_text = "\n".join([
            f"- {item['title']}: {item['content'][:200]}"
            for item in relevant_kb
        ])
        
        enhanced_prompt = template.format(
            language=language,
            code=code,
            kb_results=kb_text,
            coding_standards_content=standards[:1000]
        )
        
        return enhanced_prompt
```

---

## GitHub / GitLab 統合

### スキルとGit統合の例

```json
{
  "id": "auto-code-review",
  "name": "自動コードレビュー",
  "description": "PRを自動的にレビューしてコメントを追加",
  
  "cicdIntegration": {
    "triggers": [
      "pull_request_opened",
      "pull_request_synchronize"
    ],
    "webhookEndpoint": "https://your-skill-server.com/webhook"
  },
  
  "gitIntegration": {
    "type": "github",
    "requiredScopes": [
      "pull_request:read",
      "pull_request:comment",
      "contents:read"
    ],
    "actions": [
      {
        "trigger": "changes_detected",
        "action": "post_review_comment",
        "format": "github_review"
      }
    ]
  }
}
```

### GitHub Actions ワークフロー統合

```yaml
# .github/workflows/copilot-skill-review.yml
name: Copilot Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Get changed files
        id: changed-files
        run: |
          git diff --name-only ${{ github.event.pull_request.base.sha }} HEAD > /tmp/changed_files.txt
          cat /tmp/changed_files.txt
      
      - name: Run Copilot Skill Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          COPILOT_API_KEY: ${{ secrets.COPILOT_API_KEY }}
        run: |
          python scripts/run_skill_review.py \
            --pr ${{ github.event.pull_request.number }} \
            --skill auto-code-review
      
      - name: Post review comments
        if: always()
        run: |
          python scripts/post_review_comments.py \
            --pr ${{ github.event.pull_request.number }}
```

### PR レビュー実装例

```python
import os
from github import Github

class AutoCodeReviewSkill:
    """GitHub PR への自動コードレビュー"""
    
    def __init__(self, github_token: str, skill_api: SkillAPI):
        self.github = Github(github_token)
        self.skill_api = skill_api
    
    async def review_pull_request(self, org: str, repo: str, pr_number: int):
        """プルリクエストをレビュー"""
        
        repo = self.github.get_repo(f"{org}/{repo}")
        pr = repo.get_pull(pr_number)
        
        # PR内の全てのファイルを取得
        files = pr.get_files()
        
        for file in files:
            if not self._should_review(file.filename):
                continue
            
            # ファイルのコンテンツを取得
            content = repo.get_contents(file.filename, ref=pr.head.sha).decoded_content
            
            # Skillで分析
            review_result = await self.skill_api.execute(
                skill_id="analyze-code-quality",
                parameters={
                    "code": content,
                    "language": self._detect_language(file.filename)
                }
            )
            
            # コメントを投稿
            for issue in review_result.get('issues', []):
                self._post_review_comment(
                    pr=pr,
                    filename=file.filename,
                    line=issue['line_number'],
                    comment=f"{issue['severity']}: {issue['description']}"
                )
    
    def _should_review(self, filename: str) -> bool:
        """review対象のファイルか判定"""
        skip_patterns = ['.md', '.txt', '.json', 'package-lock.json']
        return not any(filename.endswith(p) for p in skip_patterns)
    
    def _detect_language(self, filename: str) -> str:
        """ファイル拡張子から言語を判定"""
        ext_to_lang = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go'
        }
        for ext, lang in ext_to_lang.items():
            if filename.endswith(ext):
                return lang
        return 'unknown'
    
    def _post_review_comment(self, pr, filename: str, line: int, comment: str):
        """PR にコメントを投稿"""
        pr.create_review_comment(
            body=comment,
            commit=pr.head.commit,
            path=filename,
            line=line
        )
```

---

## Slack / Teams 統合

### スキル結果を Slack に通知

```python
import aiohttp
from typing import Dict, Any

class SlackNotifier:
    """Slack への通知"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_skill_result(self, 
                               skill_id: str,
                               result: Dict[str, Any],
                               channel: str = None):
        """スキルの実行結果を Slack に投稿"""
        
        message = self._format_result_as_slack_message(skill_id, result)
        
        payload = {
            "channel": channel,
            "blocks": message
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.webhook_url, json=payload) as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to post to Slack: {resp.status}")
    
    def _format_result_as_slack_message(self, 
                                       skill_id: str,
                                       result: Dict) -> List[Dict]:
        """実行結果を Slack メッセージ形式に変換"""
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"✓ Skill Executed: {skill_id}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\nSuccess"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Execution Time:*\n{result.get('execution_time', 'N/A')}"
                    }
                ]
            }
        ]
        
        # 結果に応じてブロックを追加
        if 'issues' in result:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Issues Found:* {len(result['issues'])}\n" +
                            "\n".join([f"• {issue['description']}" 
                                      for issue in result['issues'][:5]])
                }
            })
        
        return blocks
```

---

## 外部 API の認証とセキュリティ

### API キー管理

```python
import os
from typing import Dict
from cryptography.fernet import Fernet

class SecureAPIKeyManager:
    """API キーの安全な管理"""
    
    def __init__(self, master_key: str = None):
        # 環境変数から master key を取得
        self.master_key = master_key or os.getenv('MASTER_ENCRYPTION_KEY')
        self.cipher = Fernet(self.master_key.encode())
    
    def store_api_key(self, service: str, api_key: str):
        """API キーを暗号化して保存"""
        encrypted = self.cipher.encrypt(api_key.encode())
        
        # 環境変数として保存（本番環境では安全なシークレット管理サービスを使用）
        os.environ[f"{service.upper()}_API_KEY_ENCRYPTED"] = encrypted.decode()
    
    def retrieve_api_key(self, service: str) -> str:
        """API キーを取得"""
        encrypted_key = os.getenv(f"{service.upper()}_API_KEY_ENCRYPTED")
        
        if not encrypted_key:
            raise ValueError(f"API key for {service} not found")
        
        try:
            decrypted = self.cipher.decrypt(encrypted_key.encode())
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt API key: {e}")
    
    def validate_api_key_format(self, service: str, api_key: str) -> bool:
        """API キーの形式をバリデート"""
        patterns = {
            "openai": r"^sk-",
            "anthropic": r"^sk-ant-",
            "github": r"^ghp_"
        }
        
        pattern = patterns.get(service.lower())
        if not pattern:
            return True  # パターン不明な場合はスキップ
        
        import re
        return bool(re.match(pattern, api_key))
```

---

## チェックリスト（API統合実装）

```
設計フェーズ：
□ 外部 API の選定・評価
□ 認証方式の決定
□ フォールバック戦略の計画
□ セキュリティリスク評価

実装フェーズ：
□ API クライアントの実装
□ エラーハンドリング
□ リトライ・タイムアウト設定
□ キャッシング戦略

セキュリティ：
□ API キーの安全な保管
□ 通信の暗号化（HTTPS）
□ レート制限への対応
□ 入力バリデーション

テスト・監視：
□ API エラーのテスト
□ レート制限下での動作
□ パフォーマンステスト
□ アラート・監視の設定
```

---

## まとめ

| 統合タイプ | ポイント |
|----------|---------|
| **複数LLM** | 信頼性向上、多角的な分析 |
| **ナレッジベース** | 組織固有のコンテキスト追加 |
| **GitHub/GitLab** | 開発フローへの統合 |
| **ChatOps** | リアルタイムな通知・操作 |
| **セキュリティ** | API キーの安全管理が重要 |

→ 次へ: [Part 5-3:ベストプラクティスと推奨パターン](03-best-practices.md)
