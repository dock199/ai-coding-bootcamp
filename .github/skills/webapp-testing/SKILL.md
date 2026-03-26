---
name: webapp-testing
description: Playwrightを使用してローカルWebアプリケーションの操作とテストを行うツールキット。フロントエンド機能の検証、UIデバッグ、ブラウザのスクリーンショット取得、ブラウザログの確認をサポートします。
---

# Webアプリケーションテスト

このスキルは、Playwrightオートメーションを使用してローカルWebアプリケーションの包括的なテストとデバッグを可能にします。

## このスキルを使うタイミング

以下の場合にこのスキルを使用してください:
- 実際のブラウザでフロントエンド機能をテストする
- UIの動作とインタラクションを検証する
- Webアプリケーションの問題をデバッグする
- ドキュメントやデバッグ用にスクリーンショットを取得する
- ブラウザのコンソールログを確認する
- フォーム送信とユーザーフローを検証する
- ビューポートをまたいだレスポンシブデザインを確認する

## 前提条件

- システムにNode.jsがインストールされていること
- ローカルで動作しているWebアプリケーション（またはアクセス可能なURL）
- Playwrightは未インストールの場合、自動的にインストールされます

## 主な機能

### 1. ブラウザオートメーション
- URLへのナビゲーション
- ボタンやリンクのクリック
- フォームフィールドの入力
- ドロップダウンの選択
- ダイアログやアラートの処理

### 2. 検証
- 要素の存在確認
- テキストコンテンツの検証
- 要素の表示確認
- URLの検証
- レスポンシブ動作のテスト

### 3. デバッグ
- スクリーンショットの取得
- コンソールログの確認
- ネットワークリクエストの検査
- 失敗したテストのデバッグ

## 使用例

### 例1: 基本的なナビゲーションテスト
```javascript
// ページに移動してタイトルを確認する
await page.goto('http://localhost:3000');
const title = await page.title();
console.log('ページタイトル:', title);
```

### 例2: フォーム操作
```javascript
// フォームに入力して送信する
await page.fill('#username', 'testuser');
await page.fill('#password', 'password123');
await page.click('button[type="submit"]');
await page.waitForURL('**/dashboard');
```

### 例3: スクリーンショットの取得
```javascript
// デバッグ用にスクリーンショットを取得する
await page.screenshot({ path: 'debug.png', fullPage: true });
```

## ガイドライン

1. **アプリの動作確認を必ず行う** - テスト実行前にローカルサーバーにアクセスできることを確認する
2. **明示的な待機を使用する** - 操作前に要素やナビゲーションの完了を待つ
3. **失敗時にスクリーンショットを取得する** - 問題のデバッグを助けるためにスクリーンショットを撮る
4. **リソースを必ずクリーンアップする** - 終了後は必ずブラウザを閉じる
5. **タイムアウトを適切に処理する** - 処理が遅い操作には妥当なタイムアウトを設定する
6. **段階的にテストする** - 複雑なフローの前にシンプルな操作から始める
7. **セレクターを賢く使う** - CSSクラスよりも `data-testid` やロールベースのセレクターを優先する

## よく使うパターン

### パターン: 要素の待機
```javascript
await page.waitForSelector('#element-id', { state: 'visible' });
```

### パターン: 要素の存在確認
```javascript
const exists = await page.locator('#element-id').count() > 0;
```

### パターン: コンソールログの取得
```javascript
page.on('console', msg => console.log('ブラウザログ:', msg.text()));
```

### パターン: エラー処理
```javascript
try {
  await page.click('#button');
} catch (error) {
  await page.screenshot({ path: 'error.png' });
  throw error;
}
```

## 制約事項

- Node.js環境が必要
- ネイティブモバイルアプリのテストは不可（代わりにReact Native Testing Libraryを使用）
- 複雑な認証フローで問題が発生する場合がある
- 一部のモダンフレームワークでは特定の設定が必要な場合がある
