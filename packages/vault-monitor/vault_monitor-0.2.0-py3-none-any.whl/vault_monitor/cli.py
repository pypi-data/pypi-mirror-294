""" Core module with cli """
import click
import os
import time
import hvac


@click.group()
def main():
    """
    This is a cli for monitoring Vault lockouts

    Example:

    "$> vault-monitor read-locks $VAULT_ADDR $USERNAME $PASSWORD"

    """


@main.command("read-locks", short_help="Read the current locks")
@click.argument("vault-address")
@click.argument("ldap-username")
@click.argument("ldap-password")
def read_locks(vault_address, ldap_username, ldap_password):
    """ Reads the locks in /sys/locked-users in Vault"""
    sleep_delay = 10
    print(f"This will check for locked users every {sleep_delay} seconds.")
    vault_url = vault_address
    client = hvac.Client(url=vault_url)
    login_response = client.auth.ldap.login(
        username=ldap_username,
        password=ldap_password,
    )
    #auth_result = client.is_authenticated()
    #print(f"The result of the call to is_authenticateed is {auth_result}")
    #token = login_response['auth']['client_token']
    #print(f'The client token returned from the LDAP auth method is: {token}')

    while True:
        locked = (client.read('sys/locked-users')['data'])['by_namespace']
        if len(locked) > 0:
            print(f'The locked users are: {locked}')
            time.sleep(sleep_delay)
        else:
            print("No users are locked out at the moment")
            time.sleep(sleep_delay)
