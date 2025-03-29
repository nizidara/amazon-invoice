## 使い方
直近3カ月の領収書PDFデータを自動的に保存する

### chromedriverインストール
[ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)から，対象のOSのものをDL  
例：Win64の場合，Stableのchromedriver win64をDLする（動作確認済：https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/win64/chromedriver-win64.zip ）

### .envファイルの設定
.envファイルを作成し，環境変数に以下の4つを設定する

```env
DRIVER_PATH=C:\hogehoge\chromedriver.exe
INVOICE_DIR=C:\fugafuga\
EMAIL=your-email
PASSWORD=your-password
```

- DRIVER_PATH  
ChromeDriverをインストールした場所を

- INVOICE_DIR  
領収書を保存したいディレクトリ

- EMAIL  
Amazonのログイン用e-mail

- PASSWORD  
Amazonのログインパスワード

## Dockerによる実行
### Dockerイメージのビルド
```bash
docker build -t amazon-invoice .
```

### Dokcerコンテナの実行
```bash
docker run amazon-invoice
```

### 初回ログイン
`first_login.py`の実行
```bash
python .\first_login.py
```
2段階認証が求められる場合や日本語設定ではない場合は，手動でログイン・日本語設定を行う．  
2段階認証・日本語設定完了後，プロンプト上でEnterキーを押す（ブラウザは自動で閉じる）  

### main関数実行
`main.py`の実行
```bash
python .\main.py
```

実行が上手く行かない場合は，初回ログインを再度実行する．（新しくクッキーにユーザ認証用データを保存するため）  