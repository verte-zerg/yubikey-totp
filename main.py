import argparse
import tomllib
from functools import partial
from typing import Mapping

from pynput.keyboard import Controller, GlobalHotKeys
from ykman import scripting
from yubikit.core.smartcard import SmartCardConnection
from yubikit.oath import Code, Credential, OathSession


def find_credential(entries: Mapping[Credential, Code | None], name: str) -> Credential | None:
    """Find a credential by name in the list of credentials."""
    for cred in entries:
        if cred.name == name:
            return cred
    return None


def generate_otp(name: str) -> str:
    """Generate an OTP for a credential with the given name."""
    device = scripting.single()
    serial = device.info.serial
    if serial is None:
        print('No serial number, please insert a YubiKey')
        return ''

    with device.open_connection(SmartCardConnection) as connection:
        session = OathSession(connection)
        entries = session.calculate_all()
        cred = find_credential(entries, name)

        if cred is None:
            print(f'No credential found for "{name}"')
            return ''

        code = session.calculate_code(cred)

    return code.value


def parse_args() -> str:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate OTPs using YubiKey TOTP credentials.')
    parser.add_argument('--config', type=str, default='config.toml', help='Path to the configuration file.')
    return parser.parse_args().config


def parse_config(config_path: str) -> list[tuple[str, str]]:
    """Parse configuration file."""
    with open(config_path, 'rb') as f:
        config = tomllib.load(f)

    if 'hotkeys' not in config:
        raise ValueError('No hotkeys found in config file.')

    for item in config['hotkeys'].values():
        print(f"Registered hotkey: {item['name']} - {item['hotkey']}")

    return [(item['name'], item['hotkey']) for item in config['hotkeys'].values()]


def main():
    config_path = parse_args()
    config = parse_config(config_path)
    controller = Controller()

    def on_activate(name: str) -> None:
        totp = generate_otp(name)
        controller.type(totp)

    hotkeys_config = {
        hotkey: partial(on_activate, name) for name, hotkey in config
    }

    with GlobalHotKeys(hotkeys_config) as h:
        h.join()


if __name__ == '__main__':
    main()
