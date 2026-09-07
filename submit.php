<?php
declare(strict_types=1);
/**
 * haruta bakery ご注文（事前注文・外注）フォーム 受信スクリプト
 * - config.php（gitignore対象）に LINE / メールの設定を入れて有効化します
 * - 店舗の注文書にならい、会社名/店舗名・住所・お届け方法・時間帯も受け取ります
 */
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

if (function_exists('mb_language')) mb_language('uni');
if (function_exists('mb_internal_encoding')) mb_internal_encoding('UTF-8');

function out(int $code, array $body): void {
  http_response_code($code);
  echo json_encode($body, JSON_UNESCAPED_UNICODE);
  exit;
}

function sendUtf8Mail(string $to, string $subject, string $body, string $from, string $replyTo = ''): bool {
  $headers = "MIME-Version: 1.0\r\n";
  $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
  $headers .= "Content-Transfer-Encoding: 8bit\r\n";
  if ($from !== '') $headers .= "From: haruta bakery <{$from}>\r\n";
  if ($replyTo !== '') $headers .= "Reply-To: {$replyTo}\r\n";

  if (function_exists('mb_send_mail')) {
    return @mb_send_mail($to, $subject, $body, $headers);
  }
  return @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
  out(405, ['ok' => false, 'error' => 'method_not_allowed']);
}

/* ---------- 設定 ---------- */
$cfgPath = __DIR__ . '/config.php';
if (!is_file($cfgPath)) out(500, ['ok' => false, 'error' => 'server_not_configured']);
$cfg = require $cfgPath;
$cfg['mail_to'] = 'harutabakery@gmail.com';
$hasLine = is_array($cfg) && !empty($cfg['line_token']) && !empty($cfg['line_to']);
$hasMail = is_array($cfg) && !empty($cfg['mail_to']);
if (!$hasLine && !$hasMail) out(500, ['ok' => false, 'error' => 'server_not_configured']);

/* ---------- ハニーポット ---------- */
if (!empty($_POST['hp_url'])) out(200, ['ok' => true]);

/* ---------- レート制限 ---------- */
$ip    = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$limit = (int)($cfg['rate_limit'] ?? 5);
$rlDir = __DIR__ . '/.rate';
@mkdir($rlDir, 0700, true);
$rlFile = $rlDir . '/' . md5($ip) . '.json';
$now  = time();
$hits = is_file($rlFile) ? (json_decode((string)file_get_contents($rlFile), true) ?: []) : [];
$hits = array_values(array_filter($hits, static fn($t) => $t > $now - 600));
if (count($hits) >= $limit) {
  out(429, ['ok' => false, 'error' => 'rate_limited', 'message' => '短時間に送信が集中しています。少し時間をおいてお試しください。']);
}
$hits[] = $now;
@file_put_contents($rlFile, json_encode($hits), LOCK_EX);

/* ---------- 入力チェック ---------- */
$shop    = trim((string)($_POST['shop'] ?? ''));
$method  = trim((string)($_POST['method'] ?? ''));
$company = trim((string)($_POST['company'] ?? ''));
$addr    = trim((string)($_POST['addr'] ?? ''));
$date    = trim((string)($_POST['date'] ?? ''));
$time    = trim((string)($_POST['time'] ?? ''));
$name    = trim((string)($_POST['name'] ?? ''));
$email   = trim((string)($_POST['email'] ?? ''));
$tel     = trim((string)($_POST['tel']  ?? ''));
$note    = trim((string)($_POST['note'] ?? ''));

$err = [];
if (!in_array($shop, ['久留米店', '八女店'], true)) $err[] = '取扱店舗';
if (!in_array($method, ['配達希望', '店舗受取'], true)) $err[] = 'お届け方法';
if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) $err[] = 'お届け希望日';
if (!preg_match('/^\d{2}:\d{2}$/', $time)) $err[] = 'お届け希望時間帯';
if ($name === '' || mb_strlen($name) > 40) $err[] = 'ご担当者名';
if ($email === '' || mb_strlen($email) > 120 || !filter_var($email, FILTER_VALIDATE_EMAIL)) $err[] = 'メールアドレス';
if (!preg_match('/^[0-9+\-() 　]{9,20}$/u', $tel)) $err[] = 'お電話番号';
if ($company === '' || mb_strlen($company) > 60) $err[] = 'お届け先（会社名・店舗名）';
if ($addr === '' || mb_strlen($addr) > 120) $err[] = 'ご住所';
if (mb_strlen($note) > 500) $err[] = '備考';

$ts = strtotime($date . ' 00:00:00');
if ($ts === false || $ts < strtotime('+2 days 00:00:00') || $ts > strtotime('+60 days')) $err[] = 'お届け希望日（2日後〜60日先）';

$items = json_decode((string)($_POST['items_json'] ?? '[]'), true);
$lines = [];
if (!is_array($items) || count($items) === 0 || count($items) > 200) {
  $err[] = 'ご注文内容';
} else {
  foreach ($items as $it) {
    $n = trim((string)($it['name'] ?? ''));
    $q = (int)($it['qty'] ?? 0);
    if ($n === '' || mb_strlen($n) > 60 || $q < 1 || $q > 99) { $err[] = 'ご注文内容'; break; }
    $lines[] = "・{$n} × {$q}";
  }
}
if ($err) out(422, ['ok' => false, 'error' => 'invalid', 'message' => '入力内容をご確認ください（' . implode('、', array_values(array_unique($err))) . '）']);

/* ---------- 通知メッセージ ---------- */
$msg  = "🥐 ご注文（事前注文）\n";
$msg .= "取扱店舗: {$shop}\n";
$msg .= "お届け方法: {$method}\n";
if ($company !== '') $msg .= "お届け先: {$company}\n";
if ($addr !== '') $msg .= "ご住所: {$addr}\n";
$msg .= "希望日時: {$date} {$time}\n";
$msg .= "ご担当者: {$name} 様\n";
$msg .= "メール: {$email}\n";
$msg .= "電話: {$tel}\n";
$msg .= "----\n" . implode("\n", $lines) . "\n";
if ($note !== '') $msg .= "----\n備考: {$note}\n";
$msg .= "(送信 " . date('Y-m-d H:i') . ")";

@file_put_contents(__DIR__ . '/orders.log', json_encode(['at'=>date('c'),'ip'=>$ip,'shop'=>$shop,'method'=>$method,'company'=>$company,'addr'=>$addr,'date'=>$date,'time'=>$time,'name'=>$name,'email'=>$email,'tel'=>$tel,'items'=>$items,'note'=>$note], JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);

/* ---------- LINE通知 ---------- */
$notified = false;
if ($hasLine && function_exists('curl_init')) {
  $ch = curl_init('https://api.line.me/v2/bot/message/push');
  curl_setopt_array($ch, [CURLOPT_POST=>true,CURLOPT_RETURNTRANSFER=>true,CURLOPT_TIMEOUT=>8,CURLOPT_HTTPHEADER=>['Content-Type: application/json','Authorization: Bearer ' . $cfg['line_token']],CURLOPT_POSTFIELDS=>json_encode(['to'=>$cfg['line_to'],'messages'=>[['type'=>'text','text'=>$msg]]], JSON_UNESCAPED_UNICODE)]);
  curl_exec($ch);
  $code = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
  curl_close($ch);
  if ($code >= 200 && $code < 300) $notified = true;
}

/* ---------- メール通知 ---------- */
$shopName = (string)($cfg['shop_name'] ?? 'haruta bakery');
$mailFrom = trim((string)($cfg['mail_from'] ?? ''));
if ($mailFrom === '') $mailFrom = 'no-reply@ciao-st.com';

if ($hasMail) {
  $subject = '【ご注文】' . $shop . ' ' . $method . ' ' . $date . ' ' . $time . ' / ' . ($company !== '' ? $company . ' ' : '') . $name;
  if (sendUtf8Mail($cfg['mail_to'], $subject, $msg, $mailFrom, $email)) $notified = true;
}

/* ---------- 自動確認メール ---------- */
$acked = false;
if ($hasMail && $email !== '') {
  $cSubject = '【' . $shopName . '】ご注文を受け付けました（' . $date . ' ' . $time . '）';
  $cBody = "{$name} 様\n\n{$shopName}です。このたびはご注文ありがとうございます。下記の内容で受け付けました。\n\n──────────\n取扱店舗: {$shop}\nお届け方法: {$method}\nお届け先: {$company}\nご住所: {$addr}\n希望日時: {$date} {$time}\nご担当者: {$name} 様\n電話: {$tel}\n──────────\n" . implode("\n", $lines) . "\n──────────\n";
  if ($note !== '') $cBody .= "備考: {$note}\n──────────\n";
  $cBody .= "\nお渡しまでに2日間いただきます（【2日前】までにご依頼ください）。\n担当より折り返しご確認のご連絡をさせていただきますのでお待ちください。\n\n※このメールは自動送信です。ご返信いただいても対応致しかねます。\n\n＜お問い合わせ＞\nharuta bakery 久留米店　TEL 0942-27-5959\nharuta bakery 八女店　TEL 0943-24-8001\n";
  $acked = sendUtf8Mail($email, $cSubject, $cBody, $mailFrom, $mailFrom);
}

$res = ['ok' => true];
if (!$notified) $res['warning'] = 'notify_failed';
if ($hasMail && $email !== '' && !$acked) $res['ack'] = 'ack_failed';
out(200, $res);
