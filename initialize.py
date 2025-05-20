"""
このファイルは、最初の画面読み込み時にのみ実行される初期化処理が記述されたファイルです。
"""

# 課題4のため
from langchain_community.document_loaders import PyMuPDFLoader

class PageAwarePDFLoader(PyMuPDFLoader):
    def load(self):
        docs = super().load()
        for i, doc in enumerate(docs):
            if "page" not in doc.metadata:
                doc.metadata["page"] = i
        return docs


############################################################
# ライブラリの読み込み
############################################################
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from uuid import uuid4
import sys
import unicodedata
from dotenv import load_dotenv
import streamlit as st
from docx import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma　steamlitで使えないので下記コードに書き換え
from langchain_community.vectorstores import FAISS #FAISSに書き換えたコード’
import constants as ct


############################################################
# 設定関連
############################################################
# 「.env」ファイルで定義した環境変数の読み込み
load_dotenv()


############################################################
# 関数定義
############################################################

def initialize():
    """
    画面読み込み時に実行する初期化処理
    """
    # 初期化データの用意
    initialize_session_state()
    # ログ出力用にセッションIDを生成
    initialize_session_id()
    # ログ出力の設定
    initialize_logger()
    # RAGのRetrieverを作成
    initialize_retriever()


def initialize_logger():
    """
    ログ出力の設定
    """
    # 指定のログフォルダが存在すれば読み込み、存在しなければ新規作成
    os.makedirs(ct.LOG_DIR_PATH, exist_ok=True)
    
    # 引数に指定した名前のロガー（ログを記録するオブジェクト）を取得
    # 再度別の箇所で呼び出した場合、すでに同じ名前のロガーが存在していれば読み込む
    logger = logging.getLogger(ct.LOGGER_NAME)

    # すでにロガーにハンドラー（ログの出力先を制御するもの）が設定されている場合、同じログ出力が複数回行われないよう処理を中断する
    if logger.hasHandlers():
        return

    # 1日単位でログファイルの中身をリセットし、切り替える設定
    log_handler = TimedRotatingFileHandler(
        os.path.join(ct.LOG_DIR_PATH, ct.LOG_FILE),
        when="D",
        encoding="utf8"
    )
    # 出力するログメッセージのフォーマット定義
    # - 「levelname」: ログの重要度（INFO, WARNING, ERRORなど）
    # - 「asctime」: ログのタイムスタンプ（いつ記録されたか）
    # - 「lineno」: ログが出力されたファイルの行番号
    # - 「funcName」: ログが出力された関数名
    # - 「session_id」: セッションID（誰のアプリ操作か分かるように）
    # - 「message」: ログメッセージ
    formatter = logging.Formatter(
        f"[%(levelname)s] %(asctime)s line %(lineno)s, in %(funcName)s, session_id={st.session_state.session_id}: %(message)s"
    )

    # 定義したフォーマッターの適用
    log_handler.setFormatter(formatter)

    # ログレベルを「INFO」に設定
    logger.setLevel(logging.INFO)

    # 作成したハンドラー（ログ出力先を制御するオブジェクト）を、
    # ロガー（ログメッセージを実際に生成するオブジェクト）に追加してログ出力の最終設定
    logger.addHandler(log_handler)


def initialize_session_id():
    """
    セッションIDの作成
    """
    if "session_id" not in st.session_state:
        # ランダムな文字列（セッションID）を、ログ出力用に作成
        st.session_state.session_id = uuid4().hex

def initialize_retriever( chunk_size=500, top_k=20, chunk_overlap=50,): #課題2
    """
    画面読み込み時にRAGのRetriever（ベクターストアから検索するオブジェクト）を作成
    """
    # ロガーを読み込むことで、後続の処理中に発生したエラーなどがログファイルに記録される
    logger = logging.getLogger(ct.LOGGER_NAME)

    # すでにRetrieverが作成済みの場合、後続の処理を中断
    if "retriever" in st.session_state:
        return
    
    # RAGの参照先となるデータソースの読み込み
    docs_all = load_data_sources()


    # # OSがWindowsの場合、Unicode正規化と、cp932（Windows用の文字コード）で表現できない文字を除去
    # for doc in docs_all:
    #     doc.page_content = adjust_string(doc.page_content)
    #     for key in doc.metadata:
    #         doc.metadata[key] = adjust_string(doc.metadata[key])
    
    # 【修正①】OS依存の文字コード調整（元の処理）＋ メタ情報の補正
    for i, doc in enumerate(docs_all):
        doc.page_content = adjust_string(doc.page_content)
        for key in doc.metadata:
            doc.metadata[key] = adjust_string(doc.metadata[key])

        # 【修正②】pageメタデータがない場合に補正する
        if "page" not in doc.metadata:
            doc.metadata["page"] = 0  # ← 仮に0ページを設定（本来は正確なページ番号を維持）

        # 【修正③】sourceがない場合にfile_pathから補完する
        if "source" not in doc.metadata and "file_path" in doc.metadata:
            doc.metadata["source"] = doc.metadata["file_path"]

# 課題4追加
    for doc in docs_all:
        source = doc.metadata.get("source", "不明ファイル")
        page = doc.metadata.get("page", "不明ページ")
        doc.page_content = (
            f"【この情報はファイル「{source}」の{int(page)+1}ページに記載されています】\n\n"
            f"{doc.page_content}"
        )

    # 埋め込みモデルの用意
    embeddings = OpenAIEmbeddings()
    
    # チャンク分割用のオブジェクトを作成
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size, # 課題2
        chunk_overlap=chunk_overlap, #
        separator="\n"
    )

    # チャンク分割を実施
    splitted_docs = text_splitter.split_documents(docs_all)

    # ベクターストアの作成
    # db = Chroma.from_documents(splitted_docs, embedding=embeddings) 下記に書き換え
    db = FAISS.from_documents(splitted_docs, embedding=embeddings) #書き換えた場所

    # ベクターストアを検索するRetrieverの作成
    st.session_state.retriever = db.as_retriever(search_kwargs={"k": top_k}) #課題1,2

# 課題4追加
    print(f"✅ チャンク数: {len(splitted_docs)}")
    for i, doc in enumerate(splitted_docs[:5]):
        print(f"{i}: chars={len(doc.page_content)}, page={doc.metadata.get('page')}, source={doc.metadata.get('source')}")


def initialize_session_state():
    """
    初期化データの用意
    """
    if "messages" not in st.session_state:
        # 「表示用」の会話ログを順次格納するリストを用意
        st.session_state.messages = []
        # 「LLMとのやりとり用」の会話ログを順次格納するリストを用意
        st.session_state.chat_history = []


def load_data_sources():
    """
    RAGの参照先となるデータソースの読み込み

    Returns:
        読み込んだ通常データソース
    """
    # データソースを格納する用のリスト
    docs_all = []
    # ファイル読み込みの実行（渡した各リストにデータが格納される）
    recursive_file_check(ct.RAG_TOP_FOLDER_PATH, docs_all)

    web_docs_all = []
    # ファイルとは別に、指定のWebページ内のデータも読み込み
    # 読み込み対象のWebページ一覧に対して処理
    for web_url in ct.WEB_URL_LOAD_TARGETS:
        # 指定のWebページを読み込み
        loader = WebBaseLoader(web_url)
        web_docs = loader.load()
        # for文の外のリストに読み込んだデータソースを追加
        web_docs_all.extend(web_docs)
    # 通常読み込みのデータソースにWebページのデータを追加
    docs_all.extend(web_docs_all)

# 開発後なのでミュートに
# # 課題4追加
#     print("📄 読み込まれたファイル一覧:")
#     for doc in docs_all:
#         print(f"{doc.metadata.get('source')} | page={doc.metadata.get('page')} | chars={len(doc.page_content)}")

    return docs_all


def recursive_file_check(path, docs_all):
    """
    RAGの参照先となるデータソースの読み込み

    Args:
        path: 読み込み対象のファイル/フォルダのパス
        docs_all: データソースを格納する用のリスト
    """
    # パスがフォルダかどうかを確認
    if os.path.isdir(path):
        # フォルダの場合、フォルダ内のファイル/フォルダ名の一覧を取得
        files = os.listdir(path)
        # 各ファイル/フォルダに対して処理
        for file in files:
            # ファイル/フォルダ名だけでなく、フルパスを取得
            full_path = os.path.join(path, file)
            # フルパスを渡し、再帰的にファイル読み込みの関数を実行
            recursive_file_check(full_path, docs_all)
    else:
        # パスがファイルの場合、ファイル読み込み
        file_load(path, docs_all)


# def file_load(path, docs_all):
#     """
#     ファイル内のデータ読み込み

#     Args:
#         path: ファイルパス
#         docs_all: データソースを格納する用のリスト
#     """
#     # ファイルの拡張子を取得
#     file_extension = os.path.splitext(path)[1]
#     # ファイル名（拡張子を含む）を取得
#     file_name = os.path.basename(path)

#     # 課題4追加
#     if file_extension == ".pdf":
#         loader = PageAwarePDFLoader(path)

#     # 想定していたファイル形式の場合のみ読み込む
#     if file_extension in ct.SUPPORTED_EXTENSIONS:
#         # ファイルの拡張子に合ったdata loaderを使ってデータ読み込み
#         loader = ct.SUPPORTED_EXTENSIONS[file_extension](path)
#         docs = loader.load()
#         docs_all.extend(docs)

# 課題4のために差し替え
def file_load(path, docs_all):
    """
    ファイル内のデータ読み込み

    Args:
        path: ファイルパス
        docs_all: データソースを格納する用のリスト
    """
    # ファイルの拡張子を取得
    file_extension = os.path.splitext(path)[1]
    # ファイル名（拡張子を含む）を取得
    file_name = os.path.basename(path)

    # 対応ファイルでない場合はスキップ
    if file_extension not in ct.SUPPORTED_EXTENSIONS and file_extension != ".pdf":
        return

    # 課題4：.pdf の場合はカスタムローダーを使用
    if file_extension == ".pdf":
        loader = PageAwarePDFLoader(path)
    else:
        loader = ct.SUPPORTED_EXTENSIONS[file_extension](path)

    # データ読み込み
    docs = loader.load()
    docs_all.extend(docs)


def adjust_string(s):
    """
    Windows環境でRAGが正常動作するよう調整
    
    Args:
        s: 調整を行う文字列
    
    Returns:
        調整を行った文字列
    """
    # 調整対象は文字列のみ
    if type(s) is not str:
        return s

    # OSがWindowsの場合、Unicode正規化と、cp932（Windows用の文字コード）で表現できない文字を除去
    if sys.platform.startswith("win"):
        s = unicodedata.normalize('NFC', s)
        s = s.encode("cp932", "ignore").decode("cp932")
        return s
    
    # OSがWindows以外の場合はそのまま返す
    return s