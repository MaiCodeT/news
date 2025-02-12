# ニューススクレイピング＆データ分析ツール


## 概要
このツールは、pythonのスクレイピング学習のために作成したものです。
指定したニュースカテゴリから記事情報をスクレイピングし、
キーワードごとに犯罪関連ニュースの傾向を分析・可視化します。 
得られたデータはCSVファイルに保存し、分析結果は棒グラフとして保存します。

---

## 使用技術
- **Pythonライブラリ**:
  - `requests` : WebページからHTMLを取得。
  - `BeautifulSoup` : HTMLを解析して必要なデータを抽出。
  - `pandas` : データの集計と分析。
  - `matplotlib` : グラフの作成と保存。

---

## 主な機能
### **ニュース記事のスクレイピング**:
   - カテゴリ: 経済（eco）、国内（dom）、国際（world）。
     ※犯罪ニュースが含まれていそうなところをピックアップ
   - 記事タイトル、リンク、公開日を収集し、CSVで保存。
　　　※作成された棒グラフの画像は、スクリプトと同じディレクトリに保存されます

### **犯罪関連キーワードの集計**:
   - キーワード: 「事件」「犯罪」「窃盗」など。
   - 各キーワードがタイトルに含まれる件数を計算。

### **結果の可視化**:
   - 犯罪キーワードごとの件数を棒グラフを作成し、png形式で保存。
     ※作成された棒グラフの画像は、スクリプトと同じディレクトリに保存されます
---
## 実行方法
### 以下のコマンドで必要なライブラリをインストールしてください:
   ```bash
   pip install requests beautifulsoup4 pandas matplotlib
   ```
### ツールの実行
   ```bash
   python news.py
   ```

## 注意点
### 日本語フォント:
　日本語対応フォントが必要です。
　システムにインストールされていない場合はエラーやグラフが正しく表示されない可能性があります。
### インターネット接続:
　スクレイピング時にネットワーク環境が必要です。

   

## ライセンス
このツールは学習目的で作成されています。商業利用や公開ニュースへの過剰なリクエストは避けてください。

