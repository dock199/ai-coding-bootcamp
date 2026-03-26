# ai-coding-bootcamp

日報自動生成アプリの開発用リポジトリです。

## ローカル開発（バックエンド）

### 前提ツール

- Python 3.12
- `pip`

### 必要な環境変数

`<project-root>/server/.env` を作成し、以下を設定します。

```env
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

テンプレートは `<project-root>/server/.env.example` を参照してください。

### 依存関係のインストール

```bash
cd <project-root>
python -m pip install -r server/requirements.txt
```

### 起動コマンド

```bash
cd <project-root>
python -m uvicorn server.main:app --reload --port 8000
```

### アクセス先 URL

- API ベース URL: `http://localhost:8000`
- ヘルスチェック: `http://localhost:8000/api/health`

### テスト実行

```bash
cd <project-root>
python -m pytest server/tests
```
