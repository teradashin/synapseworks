import streamlit as st
from openai import OpenAI
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd
import plotly.express as px

#test
# OpenAI クライアントの初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# 感情分析サービス
class SentimentAnalysisService(AIService):
    @property
    def name(self) -> str:
        return "テキスト感情分析"
    
    @property
    def description(self) -> str:
        return "入力されたテキストの感情（ポジティブ/ネガティブ）を分析します。"
    
    @property
    def icon(self) -> str:
        return "😊"
    
    def render(self):
        st.subheader("テキスト感情分析")
        
        # テキスト入力
        text = st.text_area("分析したいテキストを入力してください", height=150)
        
        # 分析ボタン
        if st.button("感情を分析"):
            if not text:
                st.error("テキストを入力してください")
                return
            
            with st.spinner("感情を分析中..."):
                try:
                    # 新しいOpenAI APIの形式
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system", 
                                "content": "あなたは感情分析の専門家です。テキストのポジティブさ/ネガティブさを0から10のスケールで評価し、簡単な説明をJSON形式で返してください。" +
                                           "例: {\"score\": 7, \"sentiment\": \"positive\", \"explanation\": \"理由の説明\"}"
                            },
                            {"role": "user", "content": text}
                        ]
                    )
                    
                    analysis_text = response.choices[0].message.content
                    # ここでは簡易的な実装のため、本来であればJSON解析をしっかり行う
                    import json
                    try:
                        analysis = json.loads(analysis_text)
                        
                        # 結果表示
                        sentiment = analysis.get("sentiment", "neutral")
                        score = analysis.get("score", 5)
                        explanation = analysis.get("explanation", "分析結果がありません")
                        
                        # 感情スコアの視覚化
                        if sentiment.lower() == "positive":
                            color = "green"
                            emoji = "😊"
                        elif sentiment.lower() == "negative":
                            color = "red"
                            emoji = "😔"
                        else:
                            color = "gray"
                            emoji = "😐"
                        
                        st.markdown(f"### 分析結果 {emoji}")
                        st.markdown(f"**感情傾向:** {sentiment}")
                        st.markdown(f"**スコア:** {score}/10")
                        
                        # プログレスバーで表示
                        st.progress(score/10)
                        
                        st.markdown(f"**分析の説明:**")
                        st.markdown(explanation)
                        
                    except json.JSONDecodeError:
                        # JSONとして解析できない場合は生のテキストを表示
                        st.markdown("### 分析結果")
                        st.markdown(analysis_text)
                        
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")

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
        self.service_manager.register_service(SentimentAnalysisService())
        
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
        st.title("🌟 AI Web サービス プラットフォーム")
        st.markdown("""
        OpenAI APIを活用した多機能Webサービスへようこそ！
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
        
        # 利用統計（デモ用）
        st.markdown("## 📊 利用統計")
        
        # デモ用のデータ
        data = {
            'サービス': ['AI文章生成', '画像説明生成', 'テキスト感情分析'],
            '利用回数': [154, 89, 112]
        }
        df = pd.DataFrame(data)
        
        # グラフの表示
        fig = px.bar(df, x='サービス', y='利用回数', color='サービス',
                    title='サービス別利用回数')
        st.plotly_chart(fig, use_container_width=True)

# アプリ実行
if __name__ == "__main__":
    # ページ設定
    st.set_page_config(
        page_title="AI Web Services",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
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