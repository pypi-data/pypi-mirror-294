import click

from .helpers.run import run_in_loop


@click.command()
@click.option(
    "--email",
    prompt="Your LakeRiders email",
    envvar="LOGIN_EMAIL",
    type=str,
    help="Email of your LakeRiders account",
)
@click.option(
    "--password",
    prompt="Your LakeRiders password",
    envvar="LOGIN_PASSWORD",
    hide_input=True,
    type=str,
    help="Password of your LakeRiders account",
)
@click.option(
    "--bot-token",
    prompt="Your Telegram bot token",
    envvar="BOT_TOKEN",
    type=str,
    help="Token of your Telegram bot",
)
@click.option(
    "--chat-id",
    prompt="Your Telegram chat id",
    envvar="CHAT_ID",
    type=int,
    help="Chat ID of the chat where your Telegram bot alerts you",
)
def run_with_secrets(email, password, bot_token, chat_id):
    run_in_loop(email, password, bot_token, chat_id)


run_with_secrets()
