import streamlit as st
import requests
import json

def main():
    # アプリケーションのタイトル設定
    st.title("SNS自動投稿DEMO by Synapse Works")
    st.write("SNSに投稿したい内容と関連するキーワードを入力してください。")
    
    # キーワードの入力フォーム
    keyword = st.text_input("キーワード", help="必須項目です")
    
    # 送信ボタン
    if st.button("送信"):
        if not keyword:
            st.error("キーワードを入力してください")
        else:
            # Webhookに送信するデータを準備
            data = {
                "keyword": keyword
            }
            
            # Webhook URLの設定
            webhook_url = "https://hook.us2.make.com/bygwi3rthep6sv5tla5jqgqu7xuoyqhe"
            
            try:
                # POSTリクエスト送信
                response = requests.post(
                    webhook_url,
                    data=json.dumps(data),
                    headers={"Content-Type": "application/json"}
                )
                
                # レスポンスのチェック
                if response.status_code == 200:
                    st.success("データが正常に送信されました")
                    st.json(data)  # 送信されたデータを表示
                else:
                    st.error(f"エラーが発生しました: ステータスコード {response.status_code}")
                    st.text(response.text)  # エラーメッセージを表示
            
            except requests.exceptions.RequestException as e:
                st.error(f"リクエスト中にエラーが発生しました: {e}")

if __name__ == "__main__":
    main()