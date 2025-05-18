"""
このファイルは、Webアプリのメイン処理が記述されたファイルです。
"""

############################################################
# 1. ライブラリの読み込み
############################################################
# 追加分
import os
# 「.env」ファイルから環境変数を読み込むための関数
from dotenv import load_dotenv
load_dotenv() # 加筆箇所/環境変数の読み込み
# ログ出力を行うためのモジュール
import logging
# streamlitアプリの表示を担当するモジュール
import streamlit as st

# set_page_config 移動
st.set_page_config(
    page_title="社内文書検索アプリ" , # ct.APP_NAME でもOK。仮の文字列を直接入れても可
    layout="wide" #課題3で追加したもの
    )

# （自作）画面表示以外の様々な関数が定義されているモジュール
import utils
# （自作）アプリ起動時に実行される初期化処理が記述された関数
from initialize import initialize
# （自作）画面表示系の関数が定義されているモジュール
import components as cn
# （自作）変数（定数）がまとめて定義・管理されているモジュール
import constants as ct

# 追加部分 streamlitでのログを見るためのもの
st.write("✅ Streamlit アプリ起動中")
st.write("🔍 その他の環境変数:")
st.json({
    "CHROMA_HOST": os.getenv("CHROMA_HOST"),
    "CHROMA_PORT": os.getenv("CHROMA_PORT"),
    "LANGCHAIN_TRACING_V2": os.getenv("LANGCHAIN_TRACING_V2"),
    "LANGCHAIN_API_KEY": os.getenv("LANGCHAIN_API_KEY")
})

############################################################
# 2. 設定関連
############################################################
# ブラウザタブの表示文言を設定 setamlit実行時のエラーのため、ライブラリの直後に移動
# st.set_page_config(
#     page_title=ct.APP_NAME
# )

# ログ出力を行うためのロガーの設定
logger = logging.getLogger(ct.LOGGER_NAME)


############################################################
# 3. 初期化処理
############################################################
# 3. 初期化処理（エラー詳細も画面に表示するよう修正）
try:
    initialize()
except Exception as e:
    logger.error(f"{ct.INITIALIZE_ERROR_MESSAGE}\n{e}")
    # 変更点：詳細なエラーも画面に出す
    st.error(f"{ct.INITIALIZE_ERROR_MESSAGE}\n\nエラー内容: {e}", icon=ct.ERROR_ICON)
    st.stop()

# アプリ起動時のログファイルへの出力
if not "initialized" in st.session_state:
    st.session_state.initialized = True
    logger.info(ct.APP_BOOT_MESSAGE)


############################################################
# 4. 初期表示
############################################################
# cn.display_app_title()

#　課題3で統一表示
# # モード表示
# cn.display_select_mode()

# # AIメッセージの初期表示
# cn.display_initial_ai_message()


# 課題3 左右カラムのレイアウトで「利用目的（ラジオボタン）」とAIメッセージ初期表示
cn.display_interface()


############################################################
# 5. 会話ログの表示
############################################################
try:
    # 会話ログの表示
    cn.display_conversation_log()
except Exception as e:
    # エラーログの出力
    logger.error(f"{ct.CONVERSATION_LOG_ERROR_MESSAGE}\n{e}")
    # エラーメッセージの画面表示
    st.error(utils.build_error_message(ct.CONVERSATION_LOG_ERROR_MESSAGE), icon=ct.ERROR_ICON)
    # 後続の処理を中断
    st.stop()


############################################################
# 6. チャット入力の受け付け
############################################################
# chat_message = st.chat_input(ct.CHAT_INPUT_HELPER_TEXT)　修正
# 課題3メインカラムの下に検索窓を「横幅制限つき」で配置
# chat_input を右側のカラム内で表示（左側のサイドバーに影響されず中央揃え）

# レイアウト用の空行（ログがない時に空白行を生成）
st.write("")
st.write("")

# 2カラム構成にして、右カラムだけにチャット欄を表示
col_left, col_right = st.columns([1, 2])

with col_right:
    st.markdown("""
        <style>
        [data-testid="stChatInputContainer"] {
            max-width: 800px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        </style>
    """, unsafe_allow_html=True)

    chat_message = st.chat_input(ct.CHAT_INPUT_HELPER_TEXT)

############################################################
# 7. チャット送信時の処理
############################################################
if chat_message:
    # ==========================================
    # 7-1. ユーザーメッセージの表示
    # ==========================================
    # ユーザーメッセージのログ出力
    logger.info({"message": chat_message, "application_mode": st.session_state.mode})

    # ユーザーメッセージを表示
    with st.chat_message("user"):
        st.markdown(chat_message)

    # ==========================================
    # 7-2. LLMからの回答取得
    # ==========================================
    # 「st.spinner」でグルグル回っている間、表示の不具合が発生しないよう空のエリアを表示
    res_box = st.empty()
    # LLMによる回答生成（回答生成が完了するまでグルグル回す）
    with st.spinner(ct.SPINNER_TEXT):
        try:
            # 画面読み込み時に作成したRetrieverを使い、Chainを実行
            llm_response = utils.get_llm_response(chat_message)
        except Exception as e:
            # エラーログの出力
            logger.error(f"{ct.GET_LLM_RESPONSE_ERROR_MESSAGE}\n{e}")
            # エラーメッセージの画面表示
            st.error(utils.build_error_message(ct.GET_LLM_RESPONSE_ERROR_MESSAGE), icon=ct.ERROR_ICON)
            # 後続の処理を中断
            st.stop()
    
    # ==========================================
    # 7-3. LLMからの回答表示
    # ==========================================
    with st.chat_message("assistant"):
        try:
            # ==========================================
            # モードが「社内文書検索」の場合
            # ==========================================
            if st.session_state.mode == ct.ANSWER_MODE_1:
                # 入力内容と関連性が高い社内文書のありかを表示
                content = cn.display_search_llm_response(llm_response)

            # ==========================================
            # モードが「社内問い合わせ」の場合
            # ==========================================
            elif st.session_state.mode == ct.ANSWER_MODE_2:
                # 入力に対しての回答と、参照した文書のありかを表示
                content = cn.display_contact_llm_response(llm_response)
            
            # AIメッセージのログ出力
            logger.info({"message": content, "application_mode": st.session_state.mode})
        except Exception as e:
            # エラーログの出力
            logger.error(f"{ct.DISP_ANSWER_ERROR_MESSAGE}\n{e}")
            # エラーメッセージの画面表示
            st.error(utils.build_error_message(ct.DISP_ANSWER_ERROR_MESSAGE), icon=ct.ERROR_ICON)
            # 後続の処理を中断
            st.stop()

    # ==========================================
    # 7-4. 会話ログへの追加
    # ==========================================
    # 表示用の会話ログにユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": chat_message})
    # 表示用の会話ログにAIメッセージを追加
    st.session_state.messages.append({"role": "assistant", "content": content})