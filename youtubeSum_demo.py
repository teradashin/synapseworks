import streamlit as st
import requests
import re
import json
from bs4 import BeautifulSoup

# アプリケーションのタイトルを設定
st.title("Youtube動画自動要約DEMO by Synapse Works")

# YouTubeのURLを検証する関数
def is_valid_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube\.com/watch\?v=|youtu\.be/)'
        r'([A-Za-z0-9_-]{11})'
    )
    match = re.match(youtube_regex, url)
    return bool(match)

# Webhookにデータを送信する関数
def send_to_webhook(data):
    webhook_url = "https://hook.us2.make.com/9seno4a0u2isb6ftq794m3wa0jt5ndsw"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # エラーがあれば例外を発生させる
        
        # レスポンスの内容を取得
        try:
            response_data = response.json()
            return True, "データが正常に送信されました！", response_data
        except ValueError:
            # HTMLかどうかの確認
            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' in content_type or response.text.strip().startswith(('<!DOCTYPE', '<html')):
                # HTMLの場合はそのまま返す
                return True, "データが正常に送信されました！", {"response_text": response.text, "content_type": "text/html"}
            else:
                # その他のテキストとして返す
                return True, "データが正常に送信されました！", {"response_text": response.text, "content_type": "text/plain"}
    except requests.exceptions.RequestException as e:
        return False, f"エラーが発生しました: {str(e)}", None

# フォームの作成
with st.form("youtube_form"):
    st.write("YouTubeのURLを入力してください")
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    # 送信ボタン
    submitted = st.form_submit_button("送信")
    
    if submitted:
        if not youtube_url:
            st.error("YouTubeのURLを入力してください。")
        elif not is_valid_youtube_url(youtube_url):
            st.error("有効なYouTube URLを入力してください。")
        else:
            # Webhookに送信するデータ
            data = {
                "youtubeURL": youtube_url
            }
            
            # Webhookにデータを送信
            success, message, response_data = send_to_webhook(data)
            
            if success:
                st.success(message)
                
                # サーバーからの返信を表示
                if response_data:
                    st.subheader("要約内容:")
                    
                    # JSON形式の場合
                    if isinstance(response_data, dict):
                        # 'response_text'キーがあり、HTML形式の場合
                        if 'response_text' in response_data and ('content_type' in response_data and 'text/html' in response_data['content_type'] or '<html' in response_data['response_text'].lower() or '<!doctype html' in response_data['response_text'].lower()):
                            html_content = response_data['response_text']
                            
                            # HTMLの表示と生コードの切り替えタブ
                            tab1, tab2 = st.tabs(["レンダリングされたHTML", "HTMLソースコード"])
                            
                            with tab1:
                                # HTMLをレンダリング
                                st.components.v1.html(html_content, height=600, scrolling=True)
                            
                            with tab2:
                                # HTMLのソースコードを表示
                                st.code(html_content, language="html")
                                
                                # フォームの外にダウンロードボタンを配置

                        else:
                            # 通常のJSONを表示
                            for key, value in response_data.items():
                                if isinstance(value, str) and ('<html' in value.lower() or '<!doctype html' in value.lower()):
                                    # HTMLの表示と生コードの切り替えタブ
                                    tab1, tab2 = st.tabs(["レンダリングされたHTML", "HTMLソースコード"])
                                    
                                    with tab1:
                                        st.components.v1.html(value, height=600, scrolling=True)
                                    
                                    with tab2:
                                        st.code(value, language="html")
                                        
                                        # フォームの外にダウンロードボタンを配置

                                else:
                                    st.write(f"**{key}**: {value}")
                    # テキスト形式でHTMLの場合
                    elif isinstance(response_data, str) and ('<html' in response_data.lower() or '<!doctype html' in response_data.lower()):
                        # HTMLの表示と生コードの切り替えタブ
                        tab1, tab2 = st.tabs(["レンダリングされたHTML", "HTMLソースコード"])
                        
                        with tab1:
                            st.components.v1.html(response_data, height=600, scrolling=True)
                        
                        with tab2:
                            st.code(response_data, language="html")
                            
                            # フォームの外にダウンロードボタンを配置

                    else:
                        st.write(response_data)
            else:
                st.error(message)

# 使用方法についての簡単な説明
st.markdown("""
### 使用方法
1. YouTube動画のURLを入力します。
2. 「送信」ボタンをクリックします。
""")

# アプリケーションの実行方法の説明
# st.sidebar.markdown("""
# ### アプリの実行方法
# ```
# pip install streamlit requests beautifulsoup4
# streamlit run app.py
# ```
# """)