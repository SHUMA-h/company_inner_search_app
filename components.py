"""
このファイルは、画面表示に特化した関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import streamlit as st
import utils
import constants as ct


############################################################
# 関数定義
############################################################

def display_app_title():
    """
    タイトル表示
    """
    st.markdown(f"## {ct.APP_NAME}")

#課題3　以下二つの関数をdef display_interface()に統合
# # def display_select_mode():
#     """
#     回答モードのラジオボタンを表示#
#     """
#     # タイトル表示（ラジオボタンの上）
#     st.markdown("### **利用目的**")  # 課題3
#     # 回答モードを選択する用のラジオボタンを表示
#     col1, col2 = st.columns([100, 1])
#     with col1:
#         # 「label_visibility="collapsed"」とすることで、ラジオボタンを非表示にする
#         st.session_state.mode = st.radio(
#             label="",
#             options=[ct.ANSWER_MODE_1, ct.ANSWER_MODE_2],
#             label_visibility="collapsed"
#         )


# def display_initial_ai_message():
#     """
#     AIメッセージの初期表示
#     """
#     with st.chat_message("assistant"):
#         # 「st.success()」とすると緑枠で表示される
#         st.markdown("こんにちは。私は社内文書の情報をもとに回答する生成AIチャットボットです。上記で利用目的を選択し、画面下部のチャット欄からメッセージを送信してください。")

#         # 「社内文書検索」の機能説明
#         st.markdown("**【「社内文書検索」を選択した場合】**")
#         # 「st.info()」を使うと青枠で表示される
#         st.info("入力内容と関連性が高い社内文書のありかを検索できます。")
#         # 「st.code()」を使うとコードブロックの装飾で表示される
#         # 「wrap_lines=True」で折り返し設定、「language=None」で非装飾とする
#         st.code("【入力例】\n社員の育成方針に関するMTGの議事録", wrap_lines=True, language=None)

#         # 「社内問い合わせ」の機能説明
#         st.markdown("**【「社内問い合わせ」を選択した場合】**")
#         st.info("質問・要望に対して、社内文書の情報をもとに回答を得られます。")
#         st.code("【入力例】\n人事部に所属している従業員情報を一覧化して", wrap_lines=True, language=None)

#課題3
# display_interface 関数の完全修正版
# シンプルかつ再現性が高い layout + 明示的にStreamlit標準APIだけで構成

# components.py －－ display_interface だけ貼り替えれば OK
# components.py   --- display_interface だけ差し替えれば OK
import streamlit as st
import constants as ct

# components.py  ─ display_interface 完全版
# components.py  ─ display_interface 完全版
import streamlit as st
import constants as ct


def display_interface():
    # ---------- ① CSS ----------
    st.markdown(
        """
        <style>
        /* sidebar 全面をグレーに */
        section[data-testid="stSidebar"] > div:first-child {
            background: #f0f2f6;
            padding: 2rem 1.5rem;
        }

        /* 背景：白 */
        .example-box-white {
            background: #ffffff !important;
            border-radius: 6px;
            padding: .6rem;
            margin: .4rem 0;
        }

        /* 背景：水色 */
        .example-box-blue {
            background: #E9F2FF !important;
            border-radius: 6px;
            padding: .6rem;
            margin: .4rem 0;
        }

        /* 見出し中央寄せ */
        h2.center-title {
            text-align: center;
            margin-top: 0.3rem;
            margin-bottom: 1.2rem;
        }

        /* チャット入力欄を中央に固定 */
        [data-testid="stChatInputContainer"] {
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- ② 左サイドバー ----------
    with st.sidebar:
        st.markdown("## 利用目的")

        st.session_state.mode = st.radio(
            label="利用目的",# 警告により修正
            options=[ct.ANSWER_MODE_1, ct.ANSWER_MODE_2],
            label_visibility="collapsed",
        )

        # ― 社内文書検索 ―
        st.markdown("**【「社内文書検索」を選択した場合】**")
        st.markdown(
            '<div class="example-box-blue">入力内容と関連性が高い社内文書のありかを検索できます。</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="example-box-white">【入力例】<br><br>社員の育成方針に関するMTGの議事録</div>',
            unsafe_allow_html=True,
        )

        # ― 社内問い合わせ ―
        st.markdown("**【「社内問い合わせ」を選択した場合】**")
        st.markdown(
            '<div class="example-box-blue">質問・要望に対して、社内文書の情報をもとに回答を得られます。</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="example-box-white">【入力例】<br><br>人事部に所属している従業員情報を一覧化して</div>',
            unsafe_allow_html=True,
        )

    # ---------- ③ 右メインエリア ----------
 # ③ 右メインエリア －－ ここを書き換え　アイコンを表示させるためにAIメッセージとしている
    st.markdown(
        '<h2 class="center-title">社内情報特化型生成AI検索アプリ</h2>',
        unsafe_allow_html=True,
    )

    # ▼ 変更点：with st.chat_message("assistant") を挟む
    with st.chat_message("assistant"):
        st.success(
            "こんにちは。私は社内文書の情報をもとに回答する生成AIチャットボットです。"
            "サイドバーで利用目的を選択し、画面下部のチャット欄からメッセージを送信してください。"
        )

    st.warning(
        "具体的に入力した方が期待通りの回答を得やすいです",
        icon=None   
    )

    st.markdown(
        """
        <style>
        /* -------------------------------
        ① すべての .stAlert に 48px
        ------------------------------- */
        .stAlert {
            margin-left:48px;
        }

        /* -------------------------------
        ② チャットバブル内 (.stChatMessage)
            の .stAlert だけ 0px に戻す
        ------------------------------- */
        .stChatMessage .stAlert {
            margin-left:0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )




def display_conversation_log():
    """
    会話ログの一覧表示
    """
    # 会話ログのループ処理
    for message in st.session_state.messages:
        # 「message」辞書の中の「role」キーには「user」か「assistant」が入っている
        with st.chat_message(message["role"]):

            # ユーザー入力値の場合、そのままテキストを表示するだけ
            if message["role"] == "user":
                st.markdown(message["content"])
            
            # LLMからの回答の場合
            else:
                # 「社内文書検索」の場合、テキストの種類に応じて表示形式を分岐処理
                if message["content"]["mode"] == ct.ANSWER_MODE_1:
                    
                    # ファイルのありかの情報が取得できた場合（通常時）の表示処理
                    if not "no_file_path_flg" in message["content"]:
                        # ==========================================
                        # ユーザー入力値と最も関連性が高いメインドキュメントのありかを表示
                        # ==========================================
                        # 補足文の表示
                        st.markdown(message["content"]["main_message"])

                        # 参照元のありかに応じて、適したアイコンを取得
                        icon = utils.get_source_icon(message['content']['main_file_path'])
                        # 参照元ドキュメントのページ番号が取得できた場合にのみ、ページ番号を表示
                        if "main_page_number" in message["content"]:
                            st.success(f"{message['content']['main_file_path']}", icon=icon)
                        else:
                            st.success(f"{message['content']['main_file_path']}", icon=icon)
                        
                        # ==========================================
                        # ユーザー入力値と関連性が高いサブドキュメントのありかを表示
                        # ==========================================
                        if "sub_message" in message["content"]:
                            # 補足メッセージの表示
                            st.markdown(message["content"]["sub_message"])

                            # サブドキュメントのありかを一覧表示
                            for sub_choice in message["content"]["sub_choices"]:
                                # 参照元のありかに応じて、適したアイコンを取得
                                icon = utils.get_source_icon(sub_choice['source'])
                                # 参照元ドキュメントのページ番号が取得できた場合にのみ、ページ番号を表示
                                if "page_number" in sub_choice:
                                    st.info(f"{sub_choice['source']}", icon=icon)
                                else:
                                    st.info(f"{sub_choice['source']}", icon=icon)
                    # ファイルのありかの情報が取得できなかった場合、LLMからの回答のみ表示
                    else:
                        st.markdown(message["content"]["answer"])
                
                # 「社内問い合わせ」の場合の表示処理
                else:
                    # LLMからの回答を表示
                    st.markdown(message["content"]["answer"])

                    # 参照元のありかを一覧表示
                    if "file_info_list" in message["content"]:
                        # 区切り線の表示
                        st.divider()
                        # 「情報源」の文字を太字で表示
                        st.markdown(f"##### {message['content']['message']}")
                        # ドキュメントのありかを一覧表示
                        for file_info in message["content"]["file_info_list"]:
                            # 参照元のありかに応じて、適したアイコンを取得
                            icon = utils.get_source_icon(file_info)
                            st.info(file_info, icon=icon)

def display_search_llm_response(llm_response):
    """
    「社内文書検索」モードの結果表示
    """
    # ❶ RAG が何も拾えなかった時
    if not llm_response["context"] or llm_response["answer"] == ct.NO_DOC_MATCH_ANSWER:
        st.markdown(ct.NO_DOC_MATCH_MESSAGE)
        return {"mode": ct.ANSWER_MODE_1,
                "answer": ct.NO_DOC_MATCH_MESSAGE,
                "no_file_path_flg": True}

    # ❷ メインドキュメント --------------------------------------------------
    main_doc     = llm_response["context"][0]
    main_path    = main_doc.metadata["source"]
    main_page    = main_doc.metadata.get("page")          # 0-indexed
    main_page_ui = f"（{main_page+1}ページ）" if main_page is not None else ""

    st.markdown("入力内容に関する情報は、以下のファイルに含まれている可能性があります。")
    st.success(f"{main_path}{main_page_ui}", icon=utils.get_source_icon(main_path))

    # ❸ サブドキュメント ----------------------------------------------------
    sub_choices, seen = [], set()

    for doc in llm_response["context"][1:]:
        path  = doc.metadata["source"]
        page  = doc.metadata.get("page")
        key   = (path, page)            # ファイル+ページの組で重複判定
        if key in seen:
            continue
        seen.add(key)

        choice = {"source": path}
        if page is not None:
            choice["page_number"] = page      # 0-indexed
        sub_choices.append(choice)

    if sub_choices:
        st.markdown("その他、ファイルありかの候補を提示します。")
        for ch in sub_choices:
            pg = f"（{ch['page_number']+1}ページ）" if "page_number" in ch else ""
            st.info(f"{ch['source']}{pg}", icon=utils.get_source_icon(ch["source"]))

    # ❹ 画面再描画用データ ----------------------------------------------------
    content = {
        "mode":            ct.ANSWER_MODE_1,
        "main_message":    "入力内容に関する情報は、以下のファイルに含まれている可能性があります。",
        "main_file_path":  main_path,
        "main_page_number": main_page,
    }
    if sub_choices:
        content["sub_message"] = "その他、ファイルありかの候補を提示します。"
        content["sub_choices"] = sub_choices
    return content


# 課題4丸ごと修正
# def display_search_llm_response(llm_response):
#     """
#     「社内文書検索」モードにおけるLLMレスポンスを表示

#     Args:
#         llm_response: LLMからの回答

#     Returns:
#         LLMからの回答を画面表示用に整形した辞書データ
#     """
#     # LLMからのレスポンスに参照元情報が入っており、かつ「該当資料なし」が回答として返された場合
#     if llm_response["context"] and llm_response["answer"] != ct.NO_DOC_MATCH_ANSWER:

#         # ==========================================
#         # ユーザー入力値と最も関連性が高いメインドキュメントのありかを表示
#         # ==========================================
#         # LLMからのレスポンス（辞書）の「context」属性の中の「0」に、最も関連性が高いドキュメント情報が入っている
#         main_file_path = llm_response["context"][0].metadata["source"]

#         # 補足メッセージの表示
#         main_message = "入力内容に関する情報は、以下のファイルに含まれている可能性があります。"
#         st.markdown(main_message)
        
#         # 参照元のありかに応じて、適したアイコンを取得
#         icon = utils.get_source_icon(main_file_path)
#         # ページ番号が取得できた場合のみ、ページ番号を表示（ドキュメントによっては取得できない場合がある）
#         if "page" in llm_response["context"][0].metadata:
#             # ページ番号を取得
#             main_page_number = llm_response["context"][0].metadata["page"]
#             st.success(f"{main_file_path}（{main_page_number}ページ）", icon=icon)
#             # 「メインドキュメントのファイルパス」と「ページ番号」を表示
#             st.success(f"{main_file_path}", icon=icon)
#         else:
#             # 「メインドキュメントのファイルパス」を表示
#             st.success(f"{main_file_path}", icon=icon)

#         # ==========================================
#         # ユーザー入力値と関連性が高いサブドキュメントのありかを表示
#         # ==========================================
#         # メインドキュメント以外で、関連性が高いサブドキュメントを格納する用のリストを用意
#         sub_choices = []
#         # 重複チェック用のリストを用意
#         duplicate_check_list = []

#         # ドキュメントが2件以上検索できた場合（サブドキュメントが存在する場合）のみ、サブドキュメントのありかを一覧表示
#         # 「source_documents」内のリストの2番目以降をスライスで参照（2番目以降がなければfor文内の処理は実行されない）
#         # for document in llm_response["context"][1:]:
#         #     # ドキュメントのファイルパスを取得
#         #     sub_file_path = document.metadata["source"]

#         #     # メインドキュメントのファイルパスと重複している場合、処理をスキップ（表示しない）
#         #     if sub_file_path == main_file_path:
#         #         continue
            
#         #     # 同じファイル内の異なる箇所を参照した場合、2件目以降のファイルパスに重複が発生する可能性があるため、重複を除去
#         #     if sub_file_path in duplicate_check_list:
#         #         continue

#         #     # 重複チェック用のリストにファイルパスを順次追加
#         #     duplicate_check_list.append(sub_file_path)

#         # 重複チェック用のセットを用意（ファイルパス＋ページ番号の組で判定）
#     duplicate_check_set = set()

#     for document in llm_response["context"][1:]:
#         sub_file_path = document.metadata["source"]
#         sub_page_number = document.metadata.get("page", None)

#         # メインドキュメントとファイル＋ページで完全一致したらスキップ
#         if sub_file_path == main_file_path and sub_page_number == main_page_number:
#             continue

#         # 同一ファイル・同一ページの重複をスキップ
#         key = f"{sub_file_path}:{sub_page_number}"
#         if key in duplicate_check_set:
#             continue
#         duplicate_check_set.add(key)

#         # 表示用データ作成
#         if sub_page_number is not None:
#             sub_choice = {"source": sub_file_path, "page_number": sub_page_number}
#         else:
#             sub_choice = {"source": sub_file_path}

#         sub_choices.append(sub_choice)

            
#             # ページ番号が取得できない場合のための分岐処理
#         if "page" in document.metadata:
#             # ページ番号を取得
#             sub_page_number = document.metadata["page"]
#             # 「サブドキュメントのファイルパス」と「ページ番号」の辞書を作成
#             sub_choice = {"source": sub_file_path, "page_number": sub_page_number}
#         else:
#             # 「サブドキュメントのファイルパス」の辞書を作成
#             sub_choice = {"source": sub_file_path}
            
#             # 後ほど一覧表示するため、サブドキュメントに関する情報を順次リストに追加
#         sub_choices.append(sub_choice)
        
#         # サブドキュメントが存在する場合のみの処理
#         if sub_choices:
#             # 補足メッセージの表示
#             sub_message = "その他、ファイルありかの候補を提示します。"
#             st.markdown(sub_message)

#             # サブドキュメントに対してのループ処理
#             for sub_choice in sub_choices:
#                 # 参照元のありかに応じて、適したアイコンを取得
#                 icon = utils.get_source_icon(sub_choice['source'])
#                 # ページ番号が取得できない場合のための分岐処理
#                 if "page_number" in sub_choice:
#                     # 「サブドキュメントのファイルパス」と「ページ番号」を表示
#                     st.info(f"{sub_choice['source']}", icon=icon)
#                 else:
#                     # 「サブドキュメントのファイルパス」を表示
#                     st.info(f"{sub_choice['source']}", icon=icon)
        
#         # 表示用の会話ログに格納するためのデータを用意
#         # - 「mode」: モード（「社内文書検索」or「社内問い合わせ」）
#         # - 「main_message」: メインドキュメントの補足メッセージ
#         # - 「main_file_path」: メインドキュメントのファイルパス
#         # - 「main_page_number」: メインドキュメントのページ番号
#         # - 「sub_message」: サブドキュメントの補足メッセージ
#         # - 「sub_choices」: サブドキュメントの情報リスト
#         content = {}
#         content["mode"] = ct.ANSWER_MODE_1
#         content["main_message"] = main_message
#         content["main_file_path"] = main_file_path
#         # メインドキュメントのページ番号は、取得できた場合にのみ追加
#         if "page" in llm_response["context"][0].metadata:
#             content["main_page_number"] = main_page_number
#         # サブドキュメントの情報は、取得できた場合にのみ追加
#         if sub_choices:
#             content["sub_message"] = sub_message
#             content["sub_choices"] = sub_choices
    
#     # LLMからのレスポンスに、ユーザー入力値と関連性の高いドキュメント情報が入って「いない」場合
#     else:
#         # 関連ドキュメントが取得できなかった場合のメッセージ表示
#         st.markdown(ct.NO_DOC_MATCH_MESSAGE)

#         # 表示用の会話ログに格納するためのデータを用意
#         # - 「mode」: モード（「社内文書検索」or「社内問い合わせ」）
#         # - 「answer」: LLMからの回答
#         # - 「no_file_path_flg」: ファイルパスが取得できなかったことを示すフラグ（画面を再描画時の分岐に使用）
#         content = {}
#         content["mode"] = ct.ANSWER_MODE_1
#         content["answer"] = ct.NO_DOC_MATCH_MESSAGE
#         content["no_file_path_flg"] = True
    
#     return content


def display_contact_llm_response(llm_response):
    """
    「社内問い合わせ」モードにおけるLLMレスポンスを表示

    Args:
        llm_response: LLMからの回答

    Returns:
        LLMからの回答を画面表示用に整形した辞書データ
    """
    # LLMからの回答を表示
    st.markdown(llm_response["answer"])

    # ユーザーの質問・要望に適切な回答を行うための情報が、社内文書のデータベースに存在しなかった場合
    if llm_response["answer"] != ct.INQUIRY_NO_MATCH_ANSWER:
        # 区切り線を表示
        st.divider()

        # 補足メッセージを表示
        message = "情報源"
        st.markdown(f"##### {message}")

        # 参照元のファイルパスの一覧を格納するためのリストを用意
        file_path_list = []
        file_info_list = []

        # LLMが回答生成の参照元として使ったドキュメントの一覧が「context」内のリストの中に入っているため、ループ処理
        for document in llm_response["context"]:
            # ファイルパスを取得
            file_path = document.metadata["source"]
            # ファイルパスの重複は除去
            if file_path in file_path_list:
                continue

            # ページ番号が取得できた場合のみ、ページ番号を表示（ドキュメントによっては取得できない場合がある）
            if "page" in document.metadata:
                # ページ番号を取得
                page_number = document.metadata["page"]
                # 「ファイルパス」と「ページ番号」
                file_info = f"{file_path}（{page_number+1}ページ）"
            else:
                # 「ファイルパス」のみ
                file_info = f"{file_path}"

            # 参照元のありかに応じて、適したアイコンを取得
            icon = utils.get_source_icon(file_path)
            # ファイル情報を表示
            st.info(file_info, icon=icon)

            # 重複チェック用に、ファイルパスをリストに順次追加
            file_path_list.append(file_path)
            # ファイル情報をリストに順次追加
            file_info_list.append(file_info)

    # 表示用の会話ログに格納するためのデータを用意
    # - 「mode」: モード（「社内文書検索」or「社内問い合わせ」）
    # - 「answer」: LLMからの回答
    # - 「message」: 補足メッセージ
    # - 「file_path_list」: ファイルパスの一覧リスト
    content = {}
    content["mode"] = ct.ANSWER_MODE_2
    content["answer"] = llm_response["answer"]
    # 参照元のドキュメントが取得できた場合のみ
    if llm_response["answer"] != ct.INQUIRY_NO_MATCH_ANSWER:
        content["message"] = message
        content["file_info_list"] = file_info_list

    return content