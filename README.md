# YubiKey TOTP Generator

If you want to use your YubiKey to generate TOTP codes for your accounts in case the service does not support security keys, you can use this tool to easily generate TOTP codes using your YubiKey and type them into the active field.

## Description

This tool enables the generation of One-Time Passwords (OTPs) using YubiKey TOTP credentials globally on your computer using keyboard shortcuts. It utilizes the `ykman` and `pynput` libraries to communicate with the YubiKey and register global hotkeys, respectively, allowing users to trigger TOTP generation with keyboard shortcuts. The code is simple and easy to understand, you can ensure for yourself that your YubiKey is not being misused.

## Requirements

- Python 3.11 or later.
- YubiKey with TOTP credentials set up.
- Libraries: `ykman`, `pynput`.

Install the required Python packages using:
```bash
poetry install
```

If you got an error during the installation go to the [Troubleshooting](#troubleshooting) section.

## Configuration

Before using the tool, prepare a `config.toml` file in the same directory as the tool (or specify the path to the configuration file using the `--config` argument). You can find example of the configuration file in the `config.example.toml` file.

```toml
# Path: config.example.toml
[hotkeys.google]
hotkey = "<ctrl>+<cmd>+e"
name = "google-work"

[hotkeys.github]
hotkey = "<ctrl>+<cmd>+r"
name = "github-personal"
```

- `hotkey`: The keyboard shortcut to trigger the TOTP generation. All supported keys can be found [here](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key).
- `name`: The name of the YubiKey TOTP credential. The TOTP credential can be added using the `ykman` CLI tool.
```bash
ykman oath accounts add --touch <name> <secret_key>
```

Where `<name>` is the name of the credential and `<secret_key>` is the secret key.

## Usage
Insert the YubiKey to your computer and run the tool:
```bash
python main.py
```

Optionally, you can specify the path to a different configuration file:
```bash
python main.py --config /path/to/your/config.toml
```

Once running, use the defined hotkeys, touch the YubiKey, and the tool will automatically type the generated OTP into the active field.

## Troubleshooting

If you face an error during the installation of the `pyscard` library, you can try the following steps (for MacOS):
```bash
brew install pcsc-lite
```

Then, rerun terminal and try to install the `pyscard` library again.

If you have another operating system, you can try to find a solution [here](https://github.com/LudovicRousseau/pyscard/issues/78).

## Roadmap
- [ ] Configure bundles for every operating system (using `nuitka`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
