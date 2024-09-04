# LAKERIDERS ALERT


## DESCRIPTION

This is a Python script that scrapes the website of LakeRiders Geneva to search for available spots for a wakeboard session. It alerts the user of available sessions through a Telegram bot

## LOGIC

* The script scrapes the calendar of upcoming sessions in the website every 2 minutes.
* It compares the reserved sessions with the ones from the previous session, which are stored in a LiteSQL DB.
* In case a session has become available (because of cancellation by a member), the script sends a message to a Telegram private group through a Telegram bot.

## PREREQUISITES

To run the script, a series of "secrets" are needed. Namely you need:
* An account at LakeRiders Geneva, characterized by an email and a password
* A Telegram bot, characterized by a bot token.
* A chat with the Telegram bot, characterized by a chat id. One way of obtaining the chat id is by running
```
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
```
The chat id is available in the response.

## RUNNING LAKE RIDERS ALERT

From the root directory:
```
pip install -e .
lakeridersalert
```
The first step installs the required dependencies and creates the `lakeridersalert` comman that launches the script.

### ENTERING YOUR SECRETS

Unless you have defined your secrets as environment variables, when launching LakeRiders Alert you will be prompted to enter the secrets mentioned in the prerequisites section above.

If you want to use the env variables approach, define the secrets as
```
export LOGIN_EMAIL=<YOUR_LOGIN_EMAIL>
export LOGIN_PASSWORD=<YOUR_LOGIN_PASSWORD>
export BOT_TOKEN=<YOUR_BOT_TOKEN>
export CHAT_ID=<YOUR_CHAT_ID>
```
Also, if you want LakeRidersAlert to print log messages in the console, set the environment variable `RUN_WITH_LOGS` to a truthy value before starting the script.


## RUNNING TESTS

From the root directory:
```
python -m unittest discover
```
