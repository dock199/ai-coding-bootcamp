# 日報自動生成アプリ — 実装タスク一覧

## 凡例

| 記号 | 意味 |
|------|------|
| ⬜ | 未着手 |
| 🔄 | 進行中 |
| ✅ | 完了 |

**依存関係の読み方:** `[A-1, A-2]` = タスク A-1 と A-2 が完了してから着手  
**並列可:** 他の指定タスクと同時に着手できる

---

## Phase A: プロジェクト基盤セットアップ

| ID | ステータス | タスク | 成果物 | 依存 | 備考 |
|----|-----------|--------|--------|------|------|
| A-1 | ✅ | `server/` ディレクトリ作成・初期構成 | `server/main.py`, `server/config.py`, `server/requirements.txt`, `server/.env.example`, `server/models/schemas.py`, `server/services/openai_service.py` | なし | A-2と並列可 |
| A-2 | ⬜ | `client/` ディレクトリ作成・Vite + React + TypeScript 初期化 | `client/` 配下全体（`npm create vite@latest` で生成） | なし | A-1と並列可 |
| A-3 | ⬜ | CORS設定・Vite proxy設定 | `server/main.py`（CORSMiddleware追加）、`client/vite.config.ts`（proxy追加） | [A-1, A-2] | — |
| A-4 | ✅ | `.gitignore` 更新 | `.gitignore`（`.env`, `node_modules/`, `__pycache__/` 等追加） | [A-1, A-2] | A-3と並列可 |
| A-5 | ✅ | `README.md` にローカル開発起動手順を記載 | `README.md` | [A-1, A-2] | A-3と並列可 |

### Phase A 完了条件
- `cd server && pip install -r requirements.txt && uvicorn main:app --reload --port 8000` でサーバー起動成功
- `cd client && npm install && npm run dev` でフロントエンド起動成功（localhost:3000）
- `GET /api/health` が `{"status": "ok"}` を返す

---

## Phase B: バックエンド実装

| ID | ステータス | タスク | 成果物 | 依存 | 備考 |
|----|-----------|--------|--------|------|------|
| B-1 | ✅ | Pydanticスキーマ定義 | `server/models/schemas.py`（`ReportResponse`, `HealthResponse`） | [A-1] | B-2と並列可 |
| B-2 | ✅ | 環境変数管理実装 | `server/config.py`（`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`, `AZURE_OPENAI_API_VERSION` を読み込み） | [A-1] | B-1と並列可 |
| B-3 | ✅ | Azure OpenAI サービス実装 | `server/services/openai_service.py`（画像Base64エンコード、プロンプト構築、API呼び出し） | [B-1, B-2] | — |
| B-4 | ✅ | `POST /api/generate-report` エンドポイント実装 | `server/main.py`（複数画像受信、バリデーション、サービス呼び出し） | [B-3] | — |
| B-5 | ✅ | `GET /api/health` エンドポイント実装 | `server/main.py` | [A-1] | B-1〜B-4と並列可 |
| B-6 | ✅ | バックエンド単体テスト | `server/tests/test_main.py`, `server/tests/test_openai_service.py` | [B-4] | — |

### Phase B 完了条件
- `POST /api/generate-report` に画像送信で日報マークダウンが返る（Azure OpenAI API接続時）
- APIモック使用でエンドポイントテストが全件パス
- 不正リクエスト時に適切なエラーレスポンスが返る

---

## Phase C: フロントエンド実装

| ID | ステータス | タスク | 成果物 | 依存 | 備考 |
|----|-----------|--------|--------|------|------|
| C-1 | ⬜ | 型定義 | `client/src/types/index.ts`（`UploadedImage`, `ReportResponse`, `ApiError`） | [A-2] | C-2と並列可 |
| C-2 | ⬜ | APIクライアント | `client/src/services/api.ts`（`fetch` で `POST /api/generate-report` 呼び出し） | [A-2] | C-1と並列可 |
| C-3 | ⬜ | `ImageUploader` コンポーネント | `client/src/components/ImageUploader.tsx`（ドラッグ&ドロップ `onDrop`、クリップボード貼り付け `onPaste`） | [C-1] | C-4と並列可 |
| C-4 | ⬜ | `ImagePreview` コンポーネント | `client/src/components/ImagePreview.tsx`（画像一覧サムネイル表示・個別削除ボタン） | [C-1] | C-3と並列可 |
| C-5 | ⬜ | `useReportGenerator` カスタムフック | `client/src/hooks/useReportGenerator.ts`（ローディング・エラー・結果の状態管理） | [C-2] | — |
| C-6 | ⬜ | `GenerateButton` コンポーネント | `client/src/components/GenerateButton.tsx`（ローディング中は無効化、画像なし時も無効化） | [C-5] | — |
| C-7 | ⬜ | `ReportEditor` コンポーネント | `client/src/components/ReportEditor.tsx`（`textarea` で表示・編集） | [C-1] | C-3〜C-6と並列可 |
| C-8 | ⬜ | `CopyButton` コンポーネント | `client/src/components/CopyButton.tsx`（`navigator.clipboard.writeText()`） | [C-7] | — |
| C-9 | ⬜ | `ErrorMessage` コンポーネント | `client/src/components/ErrorMessage.tsx`（エラーメッセージ表示） | [C-1] | 他と並列可 |
| C-10 | ⬜ | `App.tsx` 統合 | `client/src/App.tsx`（全コンポーネントのレイアウト・状態連携） | [C-3, C-4, C-5, C-6, C-7, C-8, C-9] | — |
| C-11 | ⬜ | スタイリング | `client/src/App.css`（デスクトップ向けレイアウト） | [C-10] | — |

### Phase C 完了条件
- 画像をドラッグ&ドロップでアップロードしプレビュー表示される
- 複数画像のアップロード・個別削除が動作する
- 日報生成ボタンでローディング表示後に日報テキストが表示される
- 日報テキストの編集とコピーが動作する
- 画像なし時は生成ボタンが無効化されている

---

## Phase D: 統合・検証

| ID | ステータス | タスク | 成果物 | 依存 | 備考 |
|----|-----------|--------|--------|------|------|
| D-1 | ⬜ | フロントエンド↔バックエンド統合テスト | テスト結果レポート | [B-4, C-10] | — |
| D-2 | ⬜ | 各種画像パターンでの動作確認 | テスト結果レポート（複数画像、大サイズ画像、PNG/JPEG/GIF/WebP） | [D-1] | D-3, D-4と並列可 |
| D-3 | ⬜ | エラーケーステスト | テスト結果レポート（API未接続、不正画像、タイムアウト） | [D-1] | D-2, D-4と並列可 |
| D-4 | ⬜ | ブラウザ互換性確認 | テスト結果レポート（Chrome, Firefox, Safari, Edge） | [D-1] | D-2, D-3と並列可 |

### Phase D 完了条件
- フロント→バックエンド→Azure OpenAIの一気通貫で日報が生成される
- 各エラーケースで適切なエラーメッセージが表示される
- 主要ブラウザで基本機能が動作する

---

## Phase E: ドキュメント整備

| ID | ステータス | タスク | 成果物 | 依存 | 備考 |
|----|-----------|--------|--------|------|------|
| E-1 | ⬜ | `docs/spec/requirements.md` 作成 | `docs/spec/requirements.md` | — | E-2, E-3と並列可 |
| E-2 | ⬜ | `docs/spec/design.md` 作成 | `docs/spec/design.md` | — | E-1, E-3と並列可 |
| E-3 | ⬜ | `docs/spec/tasks.md` 作成 | `docs/spec/tasks.md`（本ドキュメント） | — | E-1, E-2と並列可 |
| E-4 | ⬜ | `README.md` 最終化 | `README.md`（起動手順、環境変数一覧、プロジェクト概要） | [D-1] | — |

### Phase E 完了条件
- 3つの仕様ドキュメントが最新状態で整備されている
- README.md にローカル開発の起動手順が記載されている

---

## 推奨実行順序

```
A-1, A-2（並列） → A-3, A-4, A-5（並列）
    ↓
B-1, B-2, B-5（並列） → B-3 → B-4 → B-6
    ↓ （B-4完了後にD開始可能）
C-1, C-2（並列） → C-3, C-4, C-7, C-9（並列） → C-5 → C-6, C-8（並列） → C-10 → C-11
    ↓ （C-10完了後にD開始可能）
D-1 → D-2, D-3, D-4（並列）
    ↓
E-4（README最終化）
```

**E-1, E-2, E-3**（仕様ドキュメント）は他のフェーズと独立して作成可能。

---

## 変更履歴

| 日付 | 変更内容 | 変更者 |
|------|---------|--------|
| 2025-08-28 | 初版作成 | - |
| 2026-03-26 | Phase B バックエンド実装状況を更新 | Copilot |
