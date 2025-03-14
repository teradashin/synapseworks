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

# ZOOMスケジュール登録サービス
class ZoomSchedulerService(AIService):
    @property
    def name(self) -> str:
        return "ZOOM会議スケジュール登録"
    
    @property
    def description(self) -> str:
        return "ZOOM会議の予約情報を入力し、Webhookを通じてスケジュールを登録します。"
    
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
                "start_datetime": meeting_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "duration_minutes": duration
            }
            
            # Webhookエンドポイント
            webhook_url = "https://hook.us2.make.com/bygwi3rthep6sv5tla5jqgqu7xuoyqhe"
            
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

        # 使用方法の説明
        with st.expander("使用方法"):
            st.write("""
            1. 会議タイトルを入力してください。
            2. 会議の開催日と開始時間を選択してください。
            3. 会議の所要時間を分単位で選択してください。
            4. 「会議をスケジュール」ボタンをクリックすると、情報がWebhookに送信されます。
            5. 処理が完了すると、会議の詳細情報が表示されます。
            """)

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