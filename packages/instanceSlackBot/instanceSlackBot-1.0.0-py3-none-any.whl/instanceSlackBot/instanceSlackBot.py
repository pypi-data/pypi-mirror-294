import datetime
import slack_sdk
from slack_sdk import WebClient


class SlackBotSet:
    """
    SlackBotによる操作をインスタンス内にて行うことで、
    複数のチャンネルの作成やメッセージの送信時に管理しやすくするライブラリ
    

    Raises:
        UserNotFound: ユーザーIDが未定義、見当たらない場合の例外
        OtherError: 未定義の例外に対する例外
        ChannelIsDuplicated: チャンネルの重複に対する例外
        ChannelNotFound: チャンネルがみつからない、未定義の際の例外
        UserExists: すでにユーザーが参加済みの場合の例外
        TimeIsPast: 過去の日時が指定された場合の例外
        MessageIsEmpty: メッセージが未定義・空白の場合の例外
    """

    # エラー出力
    class MyException(Exception):
        def __init__(self, arg=""):
            self.arg = arg

    class ChannelNotFound(MyException):
        def __str__(self):
            return "チャンネルが作成される前に関数が実行されました。"

    class ChannelIsDuplicated(MyException):
        def __str__(self):
            return "チャンネル名が重複しています"

    class OtherError(MyException):
        def __init__(self, arg):
            self.arg = arg

        def __str__(self):
            if self.arg.response["error"] == "invalid_auth":
                return "認証が無効です。APIトークンを確認してください。"
            else:
                return "不明なエラーで続行が不可能となりました。"

    class UserNotFound(MyException):
        def __str__(self):
            return "メールアドレス、またはユーザーIDが一致するユーザーが見つかりませんでした。"

    class MessageIsEmpty(MyException):
        def __str__(self) -> str:
            return "メッセージがセットされていません。"

    class TimeIsPast(MyException):
        def __str__(self) -> str:
            return "過去の時間は指定できません。"

    class UserExists(MyException):
        def __init__(self, arg):
            self.arg = arg

        def __str__(self):
            message = "ユーザーの招待に失敗しました。\n"
            for data in self.arg.response["errors"]:
                message += f"ユーザーID: {data['user']}\n理由: {data['error']}"
            return message

    def __init__(self, api_token: str):
        self._user_id_list = []
        self.channel_id = ""
        self._channel_name_init = datetime.datetime.now().strftime("%Y-%m-%d")
        self._channel_name = ""
        self._channel_name_default = (
            self._channel_name_init + "created_by_slack_bot"
            )

        self._is_channel_name_is_set = False
        self._message = ""
        self._client = WebClient(token=api_token)

    def add_user_id_list_by_email(self, mailaddr: str):
        """
        SlackのIDをメールアドレスから取得してリストに保管する
        """
        try:
            user_id = self._client.users_lookupByEmail(
                email=mailaddr
                )["user"]["id"]

            self._user_id_list.append(user_id)
            print(f"{mailaddr}: {user_id}")
        except slack_sdk.errors.SlackApiError as e:
            if e.response["error"] == "users_not_found":
                raise self.UserNotFound
            raise self.OtherError(e)

    def add_user_id_list_by_id(self, id: str):
        try:
            self._client.users_info(
                user=id
            )
            self._user_id_list.append(id)
        except slack_sdk.errors.SlackApiError as e:
            if e.response["error"] == "users_not_found":
                raise self.UserNotFound
            raise self.OtherError(e)
        print("User has been added to the list")

    def create_channel(self):
        """
        フォーマットを元にチャンネルを自動作成
        チャンネルIDもリターンされる。
        インスタンスにも保存される
        """
        try:
            channel_name = self._channel_name_default
            if self._is_channel_name_is_set:
                channel_name = self._channel_name
            channel_id = self._client.conversations_create(
                name=channel_name
                )["channel"]["id"]
            print(f"{channel_name} is created. as {channel_id}")
            self.channel_id = channel_id
            return channel_id

        except slack_sdk.errors.SlackApiError as e:
            if e.response["error"] == "name_taken":
                raise self.ChannelIsDuplicated(e)
            raise self.OtherError(e)

    def show_user_id_list(self):
        """
        インスタンスに設定されたユーザー一覧を表示
        """
        print(self._user_id_list)

    def invite_users(self):
        """インスタンス内で作成されたチャンネルにユーザーをすべて招待
        """
        if self.channel_id.strip() == "":
            raise self.ChannelNotFound
        try:
            self._client.conversations_invite(
                channel=self.channel_id,
                users=self._user_id_list
            )
            print("users are invited.")
        except slack_sdk.errors.SlackApiError as e:
            if e.response["error"] == "already_in_channel":
                raise self.UserExists(e)

    def post_bot_message_by_instance(self):
        """botがメッセージを送信します。
        事前に、セットされたインスタンスでチャンネルIDが発番されている必要があります。
        また、インスタンスにメッセージがセットされている必要があります。
         = create_channel(), set_message() が実行された後のみ呼び出し可能

        Raises:
            self.ChannelNotFound: チャンネルが見つからない際の例外
        """
        if self.channel_id.strip() == "":
            raise self.ChannelNotFound
        if self._message.strip() == "":
            raise self.MessageIsEmpty

        self._client.chat_postMessage(
            channel=self.channel_id,
            text=self._message
        )
        print("message is send.")

    def edit_channel_name(self, name: str):
        """インスタンスに設定されたチャンネル名をデフォルトから変更します

        Args:
            name (str:必須): チャンネルの名称
            デフォルトで指定されている値に追記されます。
        """
        self._channel_name = f"{self._channel_name_init}_{name}"
        print(self._channel_name)
        self._is_channel_name_is_set = True

    def set_channel_name_default(self):
        """インスタンスに設定されたチャンネル名をデフォルトに戻します
        """
        self._is_channel_name_is_set = False

    def close_channel(self):
        """
        チャンネルを閉じる
        """
        self._client.conversations_close(
            channel=self.channel_id
        )

    def set_message(self, message: str):
        self._message = message

    def post_bot_message_by_channel_id(self, channel_id: str):
        """botがメッセージを送信します。
        インスタンスにメッセージがセットされている必要があります。
        = set_message()が実行された後に実行可能

        Args:
            channel_id (str:必須): 送信先のチャンネルのID

        Raises:
            self.ChannelNotFound: チャンネルIDが見つからない際の例外
        """
        if channel_id.strip() == "":
            raise self.ChannelNotFound
        if self._message.strip() == "":
            raise self.MessageIsEmpty
        self._client.chat_postMessage(
            channel=channel_id,
            text=self._message
        )
        print("message is send.")

    def post_bot_schedule_message_by_instance(self, time: datetime.datetime):
        """インスタンス内に定義されたチャンネルID, メッセージなどを元に時刻指定のメッセージを送信します。
        = create_channel(), set_message() が実行された後のみ呼び出し可能
        Args:
            time (datetime.datetime): 送信日時。現在時刻よりも未来であることが必要

        Raises:
            self.ChannelNotFound: チャンネルが未定義
            self.MessageIsEmpty: メッセージが未定義
            self.TimeIsPast: 過去の時間が指定された
        """
        if self.channel_id.strip() == "":
            raise self.ChannelNotFound
        if self._message.strip() == "":
            raise self.MessageIsEmpty
        unixtime = int(time.timestamp())
        if datetime.datetime.now().timestamp() > unixtime:
            raise self.TimeIsPast

        self._client.chat_scheduleMessage(
            channel=self.channel_id,
            text=self._message,
            post_at=unixtime
        )
        print(f"message will send at {time}.")

    def post_bot_schedule_message_by_channel_id(
            self, channel_id: str, time: datetime.datetime
            ):
        """指定されたチャンネルへ, インスタンス内のメッセージを元に時刻指定のメッセージを送信します。

        Args:
            channel_id (str): 送信先のチャンネルID
            time (datetime.datetime): 送信日時。現在時刻よりも未来であることが必要

        Raises:
            self.ChannelNotFound: チャンネルが未定義
            self.MessageIsEmpty: メッセージが未定義
            self.TimeIsPast: 過去の時間が指定された
        """
        if channel_id.strip() == "":
            raise self.ChannelNotFound
        if self._message.strip() == "":
            raise self.MessageIsEmpty
        unixtime = int(time.timestamp())
        if datetime.datetime.now().timestamp() > unixtime:
            raise self.TimeIsPast

        self._client.chat_scheduleMessage(
            channel=channel_id,
            text=self._message,
            post_at=unixtime
        )
        print(f"message will send at {time}.")
