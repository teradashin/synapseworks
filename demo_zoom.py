import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import time

def main():
    st.title("ZOOM予約Demo by Synapse Works")
    
    # フォームの作成
    with st.form("booking_form"):
        # タイトル（必須）
        name = st.text_input("タイトル *")
        
        # 希望日時（必須）
        start_date = st.date_input("希望日", min_value=datetime.now().date())
        start_time = st.time_input("希望時間", value=datetime.now().time())
        
        # 会議時間（必須、デフォルト60分）
        duration = st.number_input("会議時間（分）", min_value=15, max_value=240, value=60, step=15)
        
        # メールアドレス（任意）
        email = st.text_input("メールアドレス（任意）")
        
        # 送信ボタン
        submit_button = st.form_submit_button("送信")
        
        if submit_button:
            # 入力値の検証
            if not name:
                st.error("タイトルは必須項目です。入力してください。")
                return
            
            # 日時をフォーマット
            start_datetime = datetime.combine(start_date, start_time)
            start_datetime_str = start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            
            # JSONデータの作成
            data = {
                "name": name,
                "startDate": start_datetime_str,
                "duration": int(duration),
            }
            
            # メールアドレスが入力されている場合のみ追加
            if email:
                data["email"] = email
            
            # Webhookに送信
            try:
                webhook_url = "https://hook.us2.make.com/bygwi3rthep6sv5tla5jqgqu7xuoyqhe"
                headers = {"Content-Type": "application/json"}
                response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
                
                if response.status_code == 200:
                    st.success("予約情報が正常に送信されました。")
                    # 成功メッセージを表示するのみ
                    # 古い実験的APIは削除
                else:
                    st.error(f"エラーが発生しました。ステータスコード: {response.status_code}")
                    st.error(f"レスポンス: {response.text}")
            except Exception as e:
                st.error(f"送信中にエラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()