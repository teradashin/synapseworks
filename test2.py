import streamlit as st
from openai import OpenAI
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd
import plotly.express as px
import requests
import datetime
import json
from datetime import timedelta

#test
# OpenAI クライアントの初期化
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
webhookURL = st.secrets["WEBHOOK_URL"]

# サービスの基本クラス（抽象クラス）
class AIService(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """サービス名を返す"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """サービスの説明を返す"""
        pass
    
    @property
    @abstractmethod
    def icon(self) -> str:
        """サービスのアイコン（Emojis）を返す"""
        pass
    
    @abstractmethod
    def render(self):
        """Streamlitでサービスの内容をレンダリングする"""
        pass

# テキスト生成サービス
class TextGenerationService(AIService):
    @property
    def name(self) -> str:
        return "AI文章生成"
    
    @property
    def description(self) -> str:
        return "OpenAI GPTモデルを使用して、プロンプトに基づいた文章を生成します。"
    
    @property
    def icon(self) -> str:
        return "✍️"
    
    def render(self):
        st.subheader("AI文章生成")
        
        # モデル選択
        model = st.selectbox(
            "モデルを選択",
            ["gpt-4", "gpt-3.5-turbo"],
            index=1
        )
        
        # プロンプト入力
        prompt = st.text_area("プロンプトを入力してください", height=150)
        
        # 文章の長さ設定
        max_tokens = st.slider("最大トークン数", 50, 2000, 500)
        
        # 生成ボタン
        if st.button("文章を生成"):
            if not prompt:
                st.error("プロンプトを入力してください")
                return
            
            with st.spinner("文章を生成中..."):
                try:
                    # 新しいOpenAI APIの形式
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "あなたは役立つアシスタントです。"},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=max_tokens
                    )
                    generated_text = response.choices[0].message.content
                    
                    # 結果表示
                    st.success("文章が生成されました！")
                    st.markdown("### 生成された文章")
                    st.markdown(generated_text)
                    
                    # ダウンロードボタン
                    st.download_button(
                        label="テキストをダウンロード",
                        data=generated_text,
                        file_name="generated_text.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")

# 画像説明サービス
class ImageCaptioningService(AIService):
    @property
    def name(self) -> str:
        return "画像説明生成"
    
    @property
    def description(self) -> str:
        return "アップロードした画像に対して、AIが説明文を生成します。"
    
    @property
    def icon(self) -> str:
        return "🖼️"
    
    def render(self):
        st.subheader("画像説明生成")
        
        # 画像アップロード
        uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # 画像を表示
            st.image(uploaded_file, caption="アップロードされた画像", use_column_width=True)
            
            # 説明生成ボタン
            if st.button("画像の説明を生成"):
                with st.spinner("説明文を生成中..."):
                    try:
                        # ここは実際のAPIに合わせて調整が必要
                        # この例ではOpenAI Vision APIを想定していますが、実装が異なる場合は調整してください
                        # 実際のVision APIコードは以下のようになりますが、
                        # 本コードは概念的な実装例として提供しています
                        
                        # 画像のエンコードなどの前処理が必要
                        # response = client.chat.completions.create(
                        #     model="gpt-4-vision-preview",
                        #     messages=[
                        #         {
                        #             "role": "user",
                        #             "content": [
                        #                 {"type": "text", "text": "この画像について詳しく説明してください。"},
                        #                 {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
                        #             ]
                        #         }
                        #     ],
                        #     max_tokens=300
                        # )
                        # caption = response.choices[0].message.content
                        
                        # デモ用のキャプション例
                        caption = "これは美しい風景写真です。緑豊かな森と青い空が広がっています。自然の中で撮影されたこの写真は、季節は春または夏と思われます。木々の間から光が差し込んでおり、とても平和な雰囲気が伝わってきます。"
                        
                        st.success("説明文が生成されました！")
                        st.markdown("### 生成された説明文")
                        st.markdown(caption)
                        
                    except Exception as e:
                        st.error(f"エラーが発生しました: {str(e)}")

# ZOOMスケジュールサービス
class ZoomSchedulerService(AIService):
    @property
    def name(self) -> str:
        return "ZOOM会議スケジュール登録"
    
    @property
    def description(self) -> str:
        return "ZOOMの会議をスケジュールし、参加用のリンクを生成します。"
    
    @property
    def icon(self) -> str:
        return "📅"
    
    def render(self):
        st.subheader("ZOOM会議スケジュール登録")
        st.write("以下のフォームに入力して、ZOOM会議をスケジュールしてください。")
        
        # フォーム作成
        with st.form("zoom_scheduler_form"):
            # タイトル入力
            meeting_title = st.text_input("会議タイトル", placeholder="例: プロジェクト進捗会議")
            
            # 日付と時間の入力
            col1, col2 = st.columns(2)
            with col1:
                meeting_date = st.date_input(
                    "会議開催日",
                    value=datetime.date.today() + timedelta(days=1)
                )
            with col2:
                meeting_time = st.time_input(
                    "開始時間",
                    value=datetime.time(10, 0)
                )
            
            # 会議時間（分）
            duration = st.slider("会議時間（分）", min_value=15, max_value=180, value=60, step=15)
            
            # 送信ボタン
            submit_button = st.form_submit_button("会議をスケジュール")
        
        # Webhookへのデータ送信処理
        if submit_button:
            # 日時の結合
            meeting_datetime = datetime.datetime.combine(meeting_date, meeting_time)
            
            # Webhookに送信するデータ
            webhook_data = {
                "title": meeting_title,
                "startDate": meeting_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "duration": duration
            }
            
            # Webhookエンドポイント
            #webhook_url = "https://hook.us2.make.com/bygwi3rthep6sv5tla5jqgqu7xuoyqhe"
            webhook_url = webhookURL
            
            try:
                # POSTリクエストの送信
                with st.spinner("会議をスケジュール中..."):
                    response = requests.post(
                        webhook_url, 
                        data=json.dumps(webhook_data),
                        headers={"Content-Type": "application/json"}
                    )
                
                # レスポンスの処理
                if response.status_code == 200:
                    st.success("会議のスケジュールが完了しました！")
                    
                    # レスポンスのJSONデータを表示（Webhookからの返信がある場合）
                    try:
                        response_data = response.json()
                        st.write("## 会議情報")
                        st.json(response_data)
                        
                        # 会議URLがレスポンスに含まれている場合、表示する
                        if "join_url" in response_data:
                            st.write("## 会議URL")
                            st.markdown(f"[会議に参加する]({response_data['join_url']})")
                    except:
                        st.write("会議は正常にスケジュールされましたが、詳細情報は返されませんでした。")
                else:
                    st.error(f"エラーが発生しました。ステータスコード: {response.status_code}")
                    st.write("レスポンス内容:")
                    st.write(response.text)
            
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
        
        # フッター
        st.markdown("---")
        st.caption("© 2025 ZOOM会議スケジューラー")

# サービス管理クラス
class ServiceManager:
    def __init__(self):
        self.services: List[AIService] = []
    
    def register_service(self, service: AIService):
        """新しいサービスを登録"""
        self.services.append(service)
    
    def get_services(self) -> List[AIService]:
        """登録されているすべてのサービスを取得"""
        return self.services
    
    def get_service_by_name(self, name: str) -> Optional[AIService]:
        """名前でサービスを検索"""
        for service in self.services:
            if service.name == name:
                return service
        return None

# アプリケーションメインクラス
class AIServicesApp:
    def __init__(self):
        self.service_manager = ServiceManager()
        
        # サービスの登録
        self.service_manager.register_service(TextGenerationService())
        self.service_manager.register_service(ImageCaptioningService())
        self.service_manager.register_service(ZoomSchedulerService())
        
        # セッション状態の初期化
        if 'current_service' not in st.session_state:
            st.session_state.current_service = None
    
    def run(self):
        """アプリケーションを実行"""
        # サイドバーの設定
        self._setup_sidebar()
        
        # メインコンテンツ
        if st.session_state.current_service:
            service = self.service_manager.get_service_by_name(st.session_state.current_service)
            if service:
                service.render()
        else:
            self._render_home()
    
    def _setup_sidebar(self):
        """サイドバーのセットアップ"""
        with st.sidebar:
            st.title("AI Web Services")
            st.markdown("---")
            
            # ホームボタン
            if st.button("🏠 ホーム"):
                st.session_state.current_service = None
                st.rerun()
            
            st.markdown("## サービス一覧")
            
            # サービス一覧の表示
            for service in self.service_manager.get_services():
                if st.button(f"{service.icon} {service.name}"):
                    st.session_state.current_service = service.name
                    st.rerun()
    
    def _render_home(self):
        """ホーム画面のレンダリング"""
        st.title("🌟 AI Web サービス デモサイト by Synapse Works")
        st.markdown("""
        AIIを活用した多機能Webサービスへようこそ！
        サイドバーから利用したいサービスを選択してください。
        """)
        
        # サービスカードの表示
        services = self.service_manager.get_services()
        
        # 2列のレイアウト
        cols = st.columns(2)
        for i, service in enumerate(services):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: white;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                ">
                    <h3>{service.icon} {service.name}</h3>
                    <p>{service.description}</p>
                </div>
                """, unsafe_allow_html=True)

# アプリ実行
if __name__ == "__main__":
    # ページ設定
    st.set_page_config(
        page_title="AI Web Services",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None  # メニュー項目を非表示
    )
    
    # カスタムCSS
    st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7f9;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
        margin-bottom: 5px;
    }
    h1, h2, h3 {
        color: #1e3a8a;
    }
    .sidebar .stButton button {
        background-color: #f0f0f0;
        border: none;
        text-align: left;
        font-weight: normal;
    }
    .sidebar .stButton button:hover {
        background-color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # アプリ実行
    app = AIServicesApp()
    app.run()