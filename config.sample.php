<?php
/**
 * このファイルを config.php にコピーして値を入れ、index.html と同じ場所に置いてください。
 *   cp config.sample.php config.php
 * config.php は Git / デプロイに含めない想定です（.gitignore 済み）。
 * LINE・メールのどちらか片方でもフォームが有効になります。
 */
return [

  /* ===== LINE 公式アカウントに通知する場合 =====
   * LINE Developers で Messaging API チャネルを作成し、
   *  - チャネルアクセストークン（長期）
   *  - 通知先アカウントの userId
   * を取得。公式アカウントを friend 追加しておくこと。
   */
  'line_token' => '',
  'line_to'    => '',

  /* ===== メールで通知する場合（LINE未設定でもOK。予備にもなる） ===== */
  'mail_to'    => '',          // 店舗が注文を受け取るアドレス（必須：ここがメール機能のスイッチ）

  /* ===== お客さまへの自動確認メール ===== */
  // mail_to が設定されていて、フォームにメールアドレスが入力されたら自動返信します。
  'mail_from'  => '',          // 自動返信の差出人（空なら mail_to を使用）。例: 'order@お店のドメイン'
  'shop_name'  => 'haruta bakery',  // 自動返信の差出人名・件名に使用

  /* 同一IPあたり 10 分間の送信上限 */
  'rate_limit' => 5,
];
