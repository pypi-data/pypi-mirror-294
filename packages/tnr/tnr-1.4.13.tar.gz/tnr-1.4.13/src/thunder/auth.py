import click
import webbrowser
import os
import platform
from thunder import api
from thunder import auth_helper

# Don't remove! For some reason Mac terminal only allows 1024 characters unless
# this is imported
if platform.system() == 'Darwin':
    import readline

OAUTH_URL = "https://console.thundercompute.com/login"

def open_browser(url):
    try:
        if "WSL_DISTRO_NAME" in os.environ:
            # Running in WSL
            os.system(f"powershell.exe /c start {url}")
        else:
            webbrowser.open(url, new=2)
    except:
        click.echo(f"Please open the following URL in your browser: {url}")

def get_token_from_user():
    hide_input = platform.system() != 'Darwin'
    return click.prompt("Token", type=str, hide_input=hide_input)

def login():
    click.echo(f"Please generate a token in the Thunder Compute console. If the browser does not open automatically, please click the link: {OAUTH_URL}")
    open_browser(OAUTH_URL)

    # Wait for user to input the token
    token = get_token_from_user()

    credentials_file_path = auth_helper.get_credentials_file_path()
    with open(credentials_file_path, "w", encoding="utf-8") as f:
        f.write(token)
    return token

def logout():
    auth_helper.delete_data()
    click.echo("Logged out successfully.")

def handle_token_refresh(refresh_token: str) -> tuple:
    new_id_token, new_refresh_token, uid = api.refresh_id_token(refresh_token)
    if new_id_token and new_refresh_token:
        auth_helper.save_tokens(new_id_token, new_refresh_token, uid)
        return new_id_token, new_refresh_token, uid
    return None, None, None

def load_tokens() -> tuple:
    credentials_file_path = auth_helper.get_credentials_file_path()
    try:
        with open(credentials_file_path, "r", encoding="utf-8") as file:
            encrypted_id_token = file.readline().strip()
            encrypted_refresh_token = file.readline().strip()
            uid = file.readline().strip()
            if encrypted_id_token and encrypted_refresh_token:
                return (
                    auth_helper.decrypt_data(encrypted_id_token),
                    auth_helper.decrypt_data(encrypted_refresh_token),
                    uid,
                )
            else:
                return None, None, None
    except FileNotFoundError:
        return None, None, None

if __name__ == "__main__":
    login()
