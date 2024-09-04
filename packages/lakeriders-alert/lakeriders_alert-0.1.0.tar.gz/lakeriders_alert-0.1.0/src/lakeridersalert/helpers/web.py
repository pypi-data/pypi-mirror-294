from datetime import datetime

from requests import Session

from ..constants import RUN_WITH_LOGS, TIMEOUT_GET_REQUEST

HOME_PAGE = "https://lakeridersclub.ch/index.php"
AUTHENTICATION_PAGE = "https://lakeridersclub.ch/membres/connexion.php"
CALENDAR_PAGE = "https://lakeridersclub.ch/membres/reservations.php"


class InvalidCredentialsError(Exception):
    pass


def create_browser_session():
    if RUN_WITH_LOGS:
        print("Creating browser session")
    session = Session()
    session.get(HOME_PAGE)
    return session


def get_session_authorized(session, email, password):
    if RUN_WITH_LOGS:
        print("Authenticating")

    session.post(
        url=AUTHENTICATION_PAGE,
        data={
            "adresse_electronique": email,
            "mot_de_passe": password,
            "rester_connecte": 1,
            "action": "se_connecter",
        },
    )


def _print_crawling_log():
    if RUN_WITH_LOGS:
        message = (
            f"Crawling lakeriders calendar on {datetime.now().strftime('%d %b, %H:%M')}"
        )
        print(f"{'-'*len(message)}\n{message}\n...\n..\n.")


def get_reservations_html(session, email, password):
    response = session.get(CALENDAR_PAGE, timeout=TIMEOUT_GET_REQUEST)
    if response.url == HOME_PAGE:
        # The session is not authenticated. Re-authenticate
        get_session_authorized(session=session, email=email, password=password)
        authenticated_response = session.get(CALENDAR_PAGE, timeout=TIMEOUT_GET_REQUEST)
        if authenticated_response.url == HOME_PAGE:
            raise InvalidCredentialsError("Invalid credentials")
        _print_crawling_log()
        return authenticated_response.text
    else:
        _print_crawling_log()
        return response.text
