# CipherCraft
CipherCraft is a versatile and secure password generator designed to help you create strong, memorable passwords with ease. With a range of customizable features and unique tools, CipherCraft ensures your passwords are not only secure but also tailored to your needs.

- For detailed documentation and usage instructions, please visit our [Read the Docs page](https://cipher-craftt.readthedocs.io).
- You can also explore the source code and contribute to the project on our [GitHub repository](https://github.com/jarvismayur/cipher-craftt).

## Features
CipherCraft offers a wide range of features to help you securely generate, manage, and share passwords and passphrases:

1. **Password and Passphrase Generation**
- **Random Password Generator**: Generate strong, random passwords with customizable options such as length, inclusion/exclusion of uppercase letters, lowercase letters, digits, and special characters.
- **Context-Aware Password Generator**: Generate passwords tailored to specific contexts, such as finance, social media, or work environments.
- **Mnemonic Password Generator**: Create mnemonic-based passwords using a custom wordlist, making them easier to remember.
- **Passphrase Generator**: Generate secure passphrases composed of random words from a user-defined wordlist, with customizable separators.
2. **Password Strength and Entropy**
- **Password Strength Checker**: Evaluate the strength of a given password to ensure its robustness against attacks.
- **Entropy Calculator**: Calculate the entropy of a password, giving you an indication of its unpredictability and security level.
3. **Password History Management**
- **Password History Checker**: Verify if a password has been used before, helping to prevent reuse of old passwords.
- **Password Expiry Checker**: Check if a password has expired based on a specified number of days.
- **Password Creation Recorder**: Record the creation date of a new password for tracking and expiry purposes.
- **Limit Password History**: Set a limit on the number of stored passwords in history to maintain a clean and secure password management process.
4. **Obfuscation and Pronunciation Guide**
- **Password Obfuscator**: Obfuscate your password to different levels (1, 2, or 3) for enhanced security.
- **Pronunciation Guide**: Generate a pronunciation guide for a given password to make it easier to recall.
5. **Secure Sharing and Breach Detection**
- **Secure Password Sharing**: Encrypt and securely share passwords using a generated key.
- **Password Decryption**: Decrypt a shared password using the provided key.
- **Data Breach Checker**: Check if your password has been involved in any known data breaches, ensuring its safety.
6. **Time-Based One-Time Password (TOTP)**
- **TOTP Generation**: Generate a Time-Based One-Time Password (TOTP) using a provided secret, for use in two-factor authentication.
- **TOTP Verification**: Verify the validity of a TOTP using the provided secret and OTP.
7. **Advanced Customization**
- **Salting**: Apply passphrase-based salting to generated passwords for added security.
- **Personalization**: Incorporate personalized inputs (e.g., names, favorite numbers) into password generation for more tailored security.
- **Common Words Filtering**: Exclude common words from the password using a custom dictionary file to enhance password security.

  
## Installation
You can install CipherCraft via PyPI:

```bash
pip install cipher-craftt
```

## Updating the Package
To ensure you have the latest features and improvements, you can easily update the CipherCraft package using pip. Open your command line interface and run the following command:

```bash
pip install --upgrade cipher-craftt
```
This command will update your CipherCraft package to the latest version available on [PyPI](https://pypi.org/project/cipher-craftt/).

## Basic Usage
To use the CLI, run the following command:

```bash
python cli.py [options]
```
## Available Options
1. **Password Generation**
- `--generate-password`: Generates a random password.

```bash
python cli.py --generate-password
```
Options:

- `-l, --length`: Length of the generated password (default: 12).
- `-u, --no-upper`: Exclude uppercase letters.
- `-lo, --no-lower`: Exclude lowercase letters.
- `-d, --no-digits`: Exclude digits.
- `-s, --no-special`: Exclude special characters.
- `--exclude-chars`: Characters to exclude from the password.
- `--min-digits`: Minimum number of digits required (default: 0).
- `--min-special`: Minimum number of special characters required (default: 0).
- `--salting`: Apply passphrase-based salting to the password.
- `--personalization`: Personalized input to include in the password.
- `--file_path`: Path to a file containing common words (e.g., common_words.txt).
- `--obfuscate`: Apply obfuscation to the password (level 1, 2, or 3).

2. **Passphrase Generation**
-  `--generate-passphrase`: Generates a passphrase based on a word list.

```bash
python cli.py --generate-passphrase 
```
Options:

- `--num-words`: Number of words in the passphrase (default: 4).
- `--separator`: Separator between words in the passphrase (default: '-').
- `--obfuscate`: Apply obfuscation to the passphrase (level 1, 2, or 3).
- `--wordlist` : Your custom wordlist can also be used.
- `--language`: Multiple language wordlist available.
  - `da` : Danish
  - `de` : German
  - `en` : Enlish ( default )
  - `es` : Spanish 
  - `fr` : French
  - `it` : Italian
  - `nl` : Dutch 
  - `no` : Norwegian 
  - `pl` : Polish 
  - `pt` : Portuguese 
  - `sv` : Swedish 
  - `tr` : Turkish 

1. **Password Entropy**
- `--calculate-entropy`: Calculate the entropy of a given password.

```bash
python cli.py --calculate-entropy your_password
```
4. **Password Expiry Check**
- `--check-expiry`: Check if a password has expired.

```bash
python cli.py --check-expiry your_password
```
Options:

- `--expiry-days`: Number of days before a password expires (default: 90).
5. **Password History Management**
- `--record-password`: Record the creation date of a new password.

```bash
python cli.py --record-password your_password
```
- `--check-history`: Check if a password has been used before.

```bash
python cli.py --check-history your_password
```
- `--max-history`: Limit the number of stored passwords in history.

```bash
python cli.py --max-history 100
```
6. **Data Breach Check**
- `--check-breach`: Check if a password has been involved in a data breach.

```bash
python cli.py --check-breach your_password
```
7. **Secure Password Sharing**
- `--share-password`: Encrypt and share a password securely.

```bash
python cli.py --share-password your_password
```
- `--decrypt-password`: Decrypt a shared password.

```bash
python cli.py --decrypt-password encrypted_password key
```
8. **Pronunciation Guide**
- `--pronunciation-guide`: Generate a pronunciation guide for a password.

```bash
python cli.py --pronunciation-guide your_password
```
9. **Password Strength Check**
- `--check-strength`: Check the strength of the given password.

```bash
python cli.py --check-strength your_password
```
10. **Mnemonic Password Generation**
- `--generate-mnemonic`: Generate a mnemonic-based password.

```bash
python cli.py --generate-mnemonic --wordlist path/to/wordlist.txt
```
Options:

- `--num-words`: Number of words in the mnemonic password (default: 4).
- `--separator`: Separator between words in the mnemonic password (default: '-').
- `--length`: Length of the mnemonic password.
11. **Context-Aware Password Generation**
- `--context`: Specify the context for the password generation (e.g., finance, social, work).

```bash
python cli.py --generate-password --context finance
```
12. TOTP (Time-based One-Time Password)
- `--generate-totp`: Generate a TOTP using the provided secret.

```bash
python cli.py --generate-totp your_secret
```
- `--verify-totp`: Verify a TOTP using the provided secret and OTP.

```bash
python cli.py --verify-totp your_secret your_otp
```
## Examples
- Generate a password with specific constraints:

```bash
python cli.py --generate-password -l 16 --no-special --min-digits 2 --personalization "MySecret!"
```
- Generate a passphrase with a custom word list and separator:

```bash
python cli.py --generate-passphrase --wordlist path/to/wordlist.txt --separator "_"
```
- Check if a password has expired:

```bash
python cli.py --check-expiry your_password --expiry-days 60
```
- Encrypt and share a password securely:

```bash
python cli.py --share-password your_password
```
- Generate a TOTP:

```bash
python cli.py --generate-totp your_secret
```


## License
CipherCraft is licensed under the MIT [License](https://github.com/jarvismayur/Cipher_Craftt/blob/main/LICENSE). See the LICENSE file for details.

## Contact and Issues
If you have any questions, suggestions, or encounter issues, please feel free to [open an issue](https://github.com/yourusername/cipher-craftt/issues) on the GitHub repository. For direct communication, you can reach out to Mayur Tembhare via [email](mailto:tembharemayur@gmail.com) .
