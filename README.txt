ずけいのアトリエ ver.01

使い方
1. GitHubの新しいリポジトリに app_ver.01.py と requirements.txt を配置。
   app.pyへ名前を変えても動きます。追加のHTMLファイルは不要です。
2. SupabaseのSQL Editorで setup_supabase.sql を実行。
   末尾の確認結果: RLS=true / server_can_read=true / server_can_insert=true / anon_can_read=false。
3. Streamlit Community Cloudでリポジトリ・Pythonファイルを指定して作成。
4. StreamlitのSecretsに secrets.toml.example のURLとサーバー用キーを設定。
   既存のそろばん用URL・SERVICE_ROLE_KEYも利用できます。
   キーはGitHubやブラウザのコードへ書かないでください。
5. アプリ下部の「Supabaseと同期済み」を確認。

ローカル起動
  pip install -r requirements.txt
  streamlit run app_ver.01.py
  Secretsは .streamlit/secrets.toml に配置、または環境変数で指定。

機能
・学習モード: 等積変形／切って移す／補助線、各12問、合計36問。
  数値違いを含みます。独立した36種類の解法ではありません。
・スライダー、三角形の頂点ドラッグ、低速移動、補助線の表示。
・チャレンジ: 選択分野からランダム6問。静止図から考える。
  ヒントを見ると図形操作が開き、その回答を「ヒントあり」で記録。
・苦手克服: チャレンジまたは復習で、最後に不正解／ヒント使用だった問題。
・定着: チャレンジ／復習で、同じ問題をヒントなしで2回連続正解。
  学習モードの正解を定着判定へ加えません。
・学習記録、階級、JSON書き出し、端末ごとの保存。
・音声ON/OFF。正解は「せいかい！」のみ、不正解は解説も読む。
  自動で次へ進みません。音声品質はOS・ブラウザの日本語音声に依存します。

保存の仕組み
・このブラウザのlocalStorageに記録と未同期回答を保存。
・Supabaseへの送信は起動時・回答時・再同期ボタンのみ。図形操作ごとの通信はありません。
・送信失敗時は端末に残し、次回起動や再同期で再送します。回答UUIDで二重登録を防ぎます。
・表示・定着判定は直近1,000回答。DBの古い記録は削除しません。
・Supabase未設定でも端末保存で利用できます。未設定の表示が出ます。
・端末IDは暗号学的にランダムなUUID。IDを持つブラウザだけが同じ記録を取得します。
  ログインはありません。IDを共有すれば同じ記録へアクセスできる設計です。
  氏名や連絡先は保存しません。閲覧データ削除・別ブラウザ・別端末では別記録になります。
・DBのRLSを有効化し、anon/authenticatedには権限を与えません。
  Streamlit側のサーバー用キーで、端末IDを固定してアクセスします。

参考
・参照したそろばんファイル: app(20261028-151425).py / CLEAN-V135。
  モード選択、苦手復習、階級、ローカル保存、音声設定の構成を参考にしました。
・初版は図形学習専用。BGMや既存そろばんの画像素材は含めません。
・Streamlit components v1を使い、検証版1.51.0へ固定しています。
  将来Streamlitの版を更新する場合はコンポーネント互換性を確認してください。
・公式仕様: https://docs.streamlit.io/develop/concepts/custom-components/components-v1/intro
  https://supabase.com/docs/guides/getting-started/api-keys
  https://supabase.com/docs/guides/database/postgres/row-level-security

検証について
確認済み: Streamlit実起動、ブラウザ上の図形移動・補助線・判定・手動次へ・静止図チャレンジ、再読み込み後の端末保存、320pxで36問すべての図形ラベルの収まり。
確認済み: Supabase送受信処理はHTTPモックで端末別検索、重複防止、失敗時の未同期維持、サーバー再判定、入力検証を確認。
未確認: 実Supabaseプロジェクトへの接続・SQL実行、実スマホの音声再生とタッチドラッグ。接続先は未指定のため、既存DBには変更していません。
