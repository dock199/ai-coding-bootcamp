/**
 * Playwrightを使用したWebアプリケーションテスト用ヘルパーユーティリティ
 */

/**
 * 条件が真になるまでタイムアウト付きで待機する
 * @param {Function} condition - 真偽値を返す関数
 * @param {number} timeout - タイムアウト（ミリ秒）
 * @param {number} interval - チェック間隔（ミリ秒）
 */
async function waitForCondition(condition, timeout = 5000, interval = 100) {
  const startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    if (await condition()) {
      return true;
    }
    await new Promise(resolve => setTimeout(resolve, interval));
  }
  throw new Error('タイムアウト内に条件が満たされませんでした');
}

/**
 * ブラウザのコンソールログを取得する
 * @param {Page} page - PlaywrightのPageオブジェクト
 * @returns {Array} コンソールメッセージの配列
 */
function captureConsoleLogs(page) {
  const logs = [];
  page.on('console', msg => {
    logs.push({
      type: msg.type(),
      text: msg.text(),
      timestamp: new Date().toISOString()
    });
  });
  return logs;
}

/**
 * 自動命名でスクリーンショットを取得する
 * @param {Page} page - PlaywrightのPageオブジェクト
 * @param {string} name - スクリーンショットのベース名
 */
async function captureScreenshot(page, name) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `${name}-${timestamp}.png`;
  await page.screenshot({ path: filename, fullPage: true });
  console.log(`スクリーンショットを保存しました: ${filename}`);
  return filename;
}

module.exports = {
  waitForCondition,
  captureConsoleLogs,
  captureScreenshot
};
