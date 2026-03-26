# Plan: 日報自動生成アプリ MVP

PCの作業画面スクリーンショットからAzure OpenAI GPT-4.1（マルチモーダル）で日報を自動生成するWebアプリ。Vite + React + TypeScript（フロントエンド）と Python FastAPI（バックエンド）のモノレポ構成で `client/` と `server/` に分離し、DBなし・セッションベースのMVPとして構築する。

---

## 要件（EARS記法）

| ID | 種別 | 要件 |
|----|------|------|
| FR-01 | イベント駆動 | ユーザーが画像をドラッグ&ドロップまたはクリップボード貼り付けしたとき、システムは画像をアップロードエリアに表示すること |
| FR-02 | イベント駆動 | ユーザーが複数の画像をアップロードしたとき、システムはすべての画像を一覧表示し、個別に削除できること |
| FR-03 | イベント駆動 | ユーザーが「日報生成」ボタンを押したとき、システムはアップロードされた画像をバックエンドに送信し、日報を生成すること |
| FR-04 | 状態駆動 | 日報生成処理中の間、システムはローディングインジケーターを表示すること |
| FR-05 | イベント駆動 | 日報生成が完了したとき、システムはマークダウン形式で「作業内容」「進捗状況」「課題・問題点」の3セクション構成の日報を表示すること |
| FR-06 | イベント駆動 | ユーザーが「コピー」ボタンを押したとき、システムは日報テキストをクリップボードにコピーすること |
| FR-07 | イベント駆動 | ユーザーが日報を編集したとき、システムは編集内容をリアルタイムに反映すること |
| FR-08 | 望ましくない動作 | 画像未アップロードで「日報生成」が押された場合、システムは画像アップロードを促すメッセージを表示すること |
| FR-09 | 望ましくない動作 | APIエラーが発生した場合、システムはわかりやすいエラーメッセージを表示すること |
| FR-10 | イベント駆動 | バックエンドが画像を受信したとき、Azure OpenAI GPT-4.1 に画像を送信し日報テキストを生成すること |
| NF-01 | 普遍的 | モダンブラウザ（Chrome, Firefox, Safari, Edge最新版）で動作すること |
| NF-02 | 普遍的 | 画像のリサイズ・圧縮でAPIリクエストサイズを最適化すること |
| NF-03 | 普遍的 | 環境変数（`.env`）でAPIキー・エンドポイントを管理すること |
| NF-04 | 普遍的 | CORS設定でフロントエンドからのリクエストのみ受け付けること |
| NF-05 | 普遍的 | アップロード画像は永続保存せず処理後に破棄すること |

**スコープ外:** モバイル対応、IE11、DB永続化、ユーザー認証、テンプレートカスタマイズ、ファイルダウンロード

---

## APIエンドポイント設計

| メソッド | パス | リクエスト | レスポンス |
|---------|------|-----------|-----------|
| POST | `/api/generate-report` | multipart/form-data（複数画像） | `{ "report": "マークダウン日報テキスト" }` |
| GET | `/api/health` | なし | `{ "status": "ok" }` |

---

## ディレクトリ構成

```
client/                         # Vite + React + TypeScript
├── src/
│   ├── components/
│   │   ├── ImageUploader.tsx   # ドラッグ&ドロップ・貼り付け
│   │   ├── ImagePreview.tsx    # 画像一覧・削除
│   │   ├── GenerateButton.tsx  # 生成ボタン
│   │   ├── ReportEditor.tsx    # 日報表示・編集
│   │   ├── CopyButton.tsx      # クリップボードコピー
│   │   └── ErrorMessage.tsx    # エラー表示
│   ├── hooks/useReportGenerator.ts
│   ├── services/api.ts
│   ├── types/index.ts
│   ├── App.tsx / App.css / main.tsx
server/                         # Python FastAPI
├── main.py                     # アプリ・エンドポイント
├── services/openai_service.py  # Azure OpenAI連携
├── models/schemas.py           # Pydanticスキーマ
├── config.py                   # 環境変数管理
├── requirements.txt
├── .env.example
└── tests/
```

---

## Steps

### Phase A: プロジェクト基盤セットアップ

1. `server/` ディレクトリ作成 — `main.py`, `config.py`, `requirements.txt`, `.env.example` の初期構成 (*A-2と並列可*)
2. `client/` ディレクトリ作成 — `npm create vite@latest` で React + TypeScript プロジェクト初期化 (*A-1と並列可*)
3. CORS設定（FastAPI `CORSMiddleware`）と Vite `proxy` 設定 (*A-1, A-2に依存*)
4. `README.md` にローカル開発起動手順を記載 (*A-1, A-2に依存*)

### Phase B: バックエンド実装

5. Pydanticスキーマ定義 — `schemas.py` にレスポンスモデル (*B-6と並列可*)
6. 環境変数管理 — `config.py` で `python-dotenv` により `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT` を読み込み (*B-5と並列可*)
7. Azure OpenAI サービス — `openai_service.py` で画像Base64エンコード、プロンプト構築（3セクション構成指示）、API呼び出し (*5, 6に依存*)
8. `POST /api/generate-report` エンドポイント — 複数画像受信、バリデーション、サービス呼び出し (*7に依存*)
9. `GET /api/health` エンドポイント (*A-1に依存、他と並列可*)
10. バックエンド単体テスト — APIモック使用でエンドポイントと OpenAI サービスをテスト (*8に依存*)

### Phase C: フロントエンド実装

11. 型定義 `types/index.ts` — `UploadedImage`, `ReportResponse` 等 (*C-12と並列可*)
12. APIクライアント `services/api.ts` — `fetch` で `POST /api/generate-report` 呼び出し (*C-11と並列可*)
13. `ImageUploader` — ドラッグ&ドロップ(`onDrop`)、クリップボード貼り付け(`onPaste`)対応
14. `ImagePreview` — 画像一覧サムネイル表示・個別削除ボタン (*13と並列可*)
15. `useReportGenerator` カスタムフック — ローディング・エラー・結果の状態管理 (*12に依存*)
16. `GenerateButton` — ローディング中は無効化、画像なし時も無効化 (*15に依存*)
17. `ReportEditor` — `textarea` で表示・編集、マークダウンプレビューは将来拡張
18. `CopyButton` — `navigator.clipboard.writeText()` (*17に依存*)
19. `ErrorMessage` — エラーメッセージ表示
20. `App.tsx` 統合 — 全コンポーネントのレイアウト・状態連携 (*13-19に依存*)
21. スタイリング `App.css` — レスポンシブレイアウト（デスクトップ向け） (*20に依存*)

### Phase D: 統合・検証

22. フロントエンド↔バックエンド統合テスト (*8, 20に依存*)
23. 各種画像パターンでの動作確認（複数画像、大サイズ画像、PNG/JPEG） (*22に依存*)
24. エラーケーステスト（API未接続、不正画像、タイムアウト） (*22と並列可*)
25. ブラウザ互換性確認 (*22と並列可*)

### Phase E: ドキュメント整備

26. `docs/spec/requirements.md` 作成 (*他と並列可*)
27. `docs/spec/design.md` 作成 (*他と並列可*)
28. `docs/spec/tasks.md` 作成 (*他と並列可*)
29. `README.md` 最終化 — 起動手順、環境変数一覧、プロジェクト概要 (*D完了後*)

---

## 関連ファイル

- `docs/daily-report-app-meeting.md` — 議事録（要件の原典）
- `.devcontainer/devcontainer.json` — `postCreateCommand` で fastapi, uvicorn, python-dotenv インストール済み。ポート 3000, 8000 がフォワード設定済み
- `.github/instructions/python.instructions.md` — Pythonコーディング規約（PEP 8、型ヒント、docstring）
- `.github/instructions/reactjs.instructions.md` — React開発標準（関数コンポーネント、TypeScript、カスタムフック）

---

## 検証

1. `cd server && pip install -r requirements.txt && uvicorn main:app --reload --port 8000` → `GET /api/health` が `{"status": "ok"}` を返す
2. `cd client && npm install && npm run dev` → http://localhost:3000 にアクセスできる
3. 画像ドラッグ&ドロップ → プレビュー表示されること
4. 複数画像アップロード → 個別削除できること
5. 「日報生成」クリック → ローディング後に3セクション構成の日報が表示されること
6. 日報テキストを編集 → 画面上で反映されること
7. 「コピー」クリック → クリップボードにコピーされること
8. 画像なし時 → 「日報生成」ボタンが無効化されていること
9. `pytest server/tests/` → 全テストパス

---

## 決定事項

- フロントエンド: **Vite + React + TypeScript** / バックエンド: **Python FastAPI**
- ディレクトリ: `client/` と `server/`
- 複数画像を一括送信して1つの日報を生成
- 日報は画面表示 + クリップボードコピー（ファイルDLなし）
- 生成後の日報はブラウザ上で編集可能（`textarea`）
- DB不使用、画像は処理後に破棄
- Azure OpenAI GPT-4.1 マルチモーダルモデル利用
- 環境変数は `.env` + `python-dotenv` 管理、`.env.example` をリポジトリに含める
