haruta bakery サイト用 画像フォルダ
===================================

商品写真は SVG の仮イラスト。実写真ができたら実制作時に <img> を差し込みます。

■ ロゴ（ヘッダー ＋ Our Policy セクションで使用中）
  haruta-logo.png    … 店舗提供のロゴ画像（693x695 PNG・白背景）。
                       ※現在 index.html の :root に CSS 変数 --logo-img として base64 で
                         「1回だけ」埋め込み、ヘッダーの .brand-logo と
                         Our Policy の .pic-logo の両方が background-image で参照。
                       ※この PNG は差し替え用の元ファイルとして保管。
                         ロゴを変える場合はこの PNG を置き換え、index.html 内の
                         --logo-img:url("data:image/png;base64,...") を作り直す。
                       ※ヘッダーは縦組みロゴを小さく表示するため「bakery」「パンの図」が
                         小さくなる。横組みロゴの入稿があれば差し替え推奨。
                       ※ユーザー提供の店舗ロゴ。実制作時に使用可否・入稿データ形式を要確認。

■ 用意してもらえると良い写真（JPG／正方形推奨 1000x1000）
  hero.jpg            … 店先のパンの並び or 外観（横長 1200x900 でも可）
  ogp.jpg            … SNSシェア用（1200x630）
  bread_whit.jpg     … ウィット（断面が見えると◎）
  bread_mochi.jpg    … もちもち食パン
  bread_anbutter.jpg … あんバター
  bread_mentai.jpg   … 明太フランス
  bread_curry.jpg    … カレーパン
  bread_cream.jpg    … クリームパン
  bread_walnut.jpg   … くるみとレーズン
  bread_sausage.jpg  … ソーセージ
  bread_choco.jpg    … チョコマーブル食パン

【注意】
  ・他店・参考サイト・食べログ・ブログの写真は使えません。
  ・AI生成の「イメージ写真」を使う場合は「写真はイメージです」の注記を必ず残す。
  ・並ぶパンは日替わりのため「写真は一例」の注記も残す（サイトに記載済み）。
  ・いちばん良いのは実物を撮った写真への差し替えです。
