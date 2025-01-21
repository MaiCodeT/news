"""
ニューススクレイピング＆データ分析の練習ツール
犯罪関連のニュースの傾向を分析とグラフ化します。
"""
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 利用可能なフォント一覧から日本語対応フォントを探す（グラフ用）
available_fonts = [f.name for f in fm.fontManager.ttflist]
japanese_fonts = [f for f in available_fonts if "Gothic" in f or "Mincho" in f]

if japanese_fonts:
    plt.rcParams["font.family"] = japanese_fonts[0]  # 最初に見つかった日本語フォントを使用
else:
    print("日本語フォントが見つかりません。デフォルトのフォントを使用します。")


def scrape_news():
    """
    複数のニュースカテゴリから記事の情報を取得して、CSVへ保存する。
    Returns:
        なし
    """
    # urlを指定
    categories = ["eco", "dom", "world"]
    headers = {"User-Agent": "Mozilla/5.0"}  # User-Agentを指定
    all_news_data = []  # 全カテゴリのニュースを保存するリスト

    for category in categories:
        # 例としてライブドアニュースのURL
        BASE_URL = f"https://news.livedoor.com/topics/category/{category}/"
        news_data = []  # 全ページの保存リスト

        # 1〜７ページ分取得する
        for page in range(1, 9):
            URL = f"{BASE_URL}?p={page}"  # ページ番号を含むURL作成
            print(f"取得中: {URL}")
            try:
                response = requests.get(
                    URL, headers=headers, timeout=10)  # タイムアウト10秒
                response.raise_for_status()

            except requests.exceptions.Timeout:
                print("タイムアウトしました。")
                continue
            except requests.exceptions.RequestException as e:
                print(f"記事の処理中にエラーが発生しました (カテゴリ: {
                      category}, ページ: {page}, URL: {URL}): {e}")
                continue

            # htmlを取得
            soup = BeautifulSoup(response.text, "html.parser")

            # タイトルとリンクを取得
            articles = soup.find_all("a")

            # 記事が１つもみつからない場合
            if not articles:
                print(f"記事が見つかりませんでした:{URL}")
                continue  # 次のページへ進む

            for article in articles:
                try:
                    link = article.get("href")
                    title_tag = article.find("h3")  # タイトルのタグを取得
                    time_tag = article.find("time", class_="articleListDate")
                    if not title_tag or not link:
                        # タイトルやリンクが存在しない場合
                        continue

                    # 両方が存在する場合
                    title = title_tag.text.strip()  # タイトルを取得
                    if time_tag:
                        original_date = time_tag.text.strip()
                        published_date = datetime.strptime(
                            original_date, "%Y年%m月%d日 %H時%M分").strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        published_date = "不明"
                    if not link.startswith("http"):  # 相対パスなら絶対にパス変換
                        link = "https://news.livedoor.com" + link

                    news_data.append({
                        "title": title,
                        "link": link,
                        "published_date": published_date  # 公開日
                    })
                except Exception as e:  # 記事取得時エラー
                    print(f"記事の処理中にエラーが発生しました(カテゴリ: {
                          category}, ページ:{page}, URL:{URL}):{e}")

        # カテゴリごとのデータを全体リストに追加
        print(f"{category}カテゴリの記事数:{len(news_data)}")
        all_news_data.extend(news_data)

    # CSVに保存する。
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 現在の日時をフォーマット
    filename = f"news_title_{timestamp}.csv"  # ファイル名に日時を付ける
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["title", "link", "published_date"])
        writer.writeheader()
        writer.writerows(all_news_data)  # 列名"title""link""published_date"

    # CSV出力処理終了
    print(f"CSV出力完了({len(all_news_data)}件): {
          datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return filename


def analyze_news(filename):
    """
    Pandasを使用して、CSVファイルを読み込み、指定したキーワードに基づいて件数を集計し、グラフ化する関数。
    Args:
        filename (string): 保存されたCSVファイルのパス
    Returns:なし。
    """
    # PandasでCSV読み込み
    df = pd.read_csv(filename)
    # 検索するキーワードをlistで保持する
    keywords = ["事件", "犯罪", "窃盗", "暴行", "詐欺", "闇バイト", "殺人", "死亡", "強盗"]
    counts = {}  # 空の辞書を作成
    for keyword in keywords:
        # 各キーワードがtitle列に何回含まれるかをカウントする
        count = df["title"].str.contains(keyword).sum()
        counts[keyword] = count

    # コンソールに件数を表示
    print("キーワードごとの件数")
    for keyword, count in counts.items():
        print(f"{keyword}: {count}件")

    # グラフ化
    plt.bar(counts.keys(), counts.values(), color="skyblue")
    plt.xlabel("犯罪の種類")
    plt.ylabel("件数")
    plt.title("犯罪種類ごとのニュース件数")
    plt.xticks(rotation=45)

    # 棒グラフの上に件数を表示する
    for i, v in enumerate(counts.values()):
        # 中央揃え、棒の上部に表示
        plt.text(i, v, str(v), ha='center', va='bottom')

    plt.tight_layout()

    # グラフをpng形式で保存する
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 現在の日時をフォーマット
    plt.savefig(f"crime_trends_{timestamp}.png")
    print("グラフを保存しました")


# ニュース情報の取得
csv_file = scrape_news()

# 件数表示、グラフ化
analyze_news(csv_file)
