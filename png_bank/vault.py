from getpass import getpass
from PIL import Image
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
import os

import stega
import menus

# Terminator
TERMINATOR = "ENDMESSAGEPNG"
# Check Value
CHECK_VALUE = "By all known laws of aviation..."
# break characters
B_CHAR = [';', '/', '>', '&', ':']
NOT_ALLOWED = [CHECK_VALUE].extend(B_CHAR)


class PBank:

    def __init__(self, password, loc, salt=None, pdict=None, name="Vault", cvalue=None):
        if pdict is None:
            pdict = {}
        if salt is None:
            salt = os.urandom(16)
        self.salt = salt
        self.loc = loc
        self.key = self.init_key(password)
        self.name = name
        self.pass_dict = pdict
        if cvalue is not None:
            self.verify_pass(cvalue)

    def __del__(self):
        self.to_image()

    @classmethod
    def from_path(cls, path, password):
        itext = stega.extract_message(path, TERMINATOR)
        print(itext)
        salt, name, cvalue, ptext = itext.split(B_CHAR[4])
        return cls(password, path, bytes.fromhex(salt), cls.dict_from_ptext(ptext), name=name, cvalue=cvalue)

    def run(self):
        functions = ['Find Password', 'Add Password', 'Remove Password', 'Options', 'Exit']
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"---{self.name}---")
            func = menus.list_menu(functions)
            match func:
                case 'Find Password':
                    if not self.pass_dict:
                        print("No Passwords Stored")
                    else:
                        print(self.get_pass())
                    input()
                case 'Add Password':
                    service = input("Website/Service: ").strip().lower()
                    while service == "":
                        service = input("Service name cannot be whitespace, please try again: ").strip().lower()
                    user = input("Username: ").strip()
                    if user == "":
                        user = service
                    pw = getpass("Password: ").strip()
                    while pw == "":
                        pw = getpass("You must enter a password, please try again (enter 'x' to go back): ").strip()
                    if pw == "x":
                        continue
                    self.add_pass(service, user, pw)
                case 'Remove Password':
                    if not self.pass_dict:
                        input("No Passwords Stored")
                        continue
                    self.remove_pass()
                case 'Config':
                    # self.config_menu()
                    pass
                case 'Exit':
                    self.to_image()
                    return

    def to_image(self):
        if self.loc.split('.')[-1] != 'png':
            print("Non-png format detected, issues may occur if you continue...")
            print("Would you like to convert the image to png?")
            if menus.yn():
                self.reformat_image()
        d_str = self.ptext_from_dict()
        c_enc = self.encrypt(CHECK_VALUE)
        o_str = B_CHAR[4].join([self.salt.hex(), self.name, c_enc, d_str])
        stega.embed_message(self.loc, o_str, TERMINATOR)

    def ptext_from_dict(self) -> str:
        if self.pass_dict == {}:
            return "x"
        final = []
        for s, np_arr in self.pass_dict.items():
            nps = []
            for np in np_arr:
                nps.append(np[0] + B_CHAR[2] + np[1])
            final.append(f'{s}/{B_CHAR[3].join(nps)}')
        print(B_CHAR[0].join(final))
        return B_CHAR[0].join(final)

    def init_key(self, password) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def encrypt(self, password) -> str:
        iv = os.urandom(16)  # Initialization vector for AES
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(password.encode()) + padder.finalize()
        ct = iv + encryptor.update(padded_data) + encryptor.finalize()

        return ct.hex()

    def decrypt(self, enc_password) -> str:
        ct = bytes.fromhex(enc_password)
        iv = ct[:16]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypting the ciphertext and unpadding
        decrypted_data = decryptor.update(ct[16:]) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data.decode()

    def verify_pass(self, c_enc):
        # If password is incorrect, check value will not decrypt correctly, and will typically throw an error
        try:
            # If it doesn't raise an error, check it with the known check value to validate
            print(self.decrypt(c_enc))
            if CHECK_VALUE != self.decrypt(c_enc):
                raise ValueError()
        except ValueError as e:
            print("Password failed to validate.", e)
            exit(0)

    def reformat_image(self):
        img = Image.open(self.loc)
        self.loc = '.'.join(self.loc.split('.')[0:-1]) + '.png'
        try:
            img.save(self.loc)
        except (OSError, ValueError):
            print("Image failed to format, make sure an extension exists")
            img.close()
            exit(0)
        img.close()

    def add_pass(self, service, user, password):
        p_enc = self.encrypt(password)
        if service in self.pass_dict:
            self.pass_dict[service].append((user, p_enc))
        else:
            self.pass_dict[service] = [(user, p_enc)]

    def get_pass(self):
        password = menus.get_pass_from_vault(self.pass_dict)
        return self.decrypt(password)

    def remove_pass(self):
        pw = menus.get_pass_from_vault(self.pass_dict)
        for ser, logins in self.pass_dict.items():
            for i, login in enumerate(logins):
                if login[1] == pw:
                    self.pass_dict[ser].pop(i)
                    if not self.pass_dict[ser]:
                        self.pass_dict.pop(ser)
                    return
        print("Password not found, something went wrong")

    # def config_menu(self):
    #     options = ['Change Vault Name', 'Set Current Vault as Default', 'Change Vault Password', 'Clear Vault']
        # This is so much fucking work I'll do it another time
    @staticmethod
    def dict_from_ptext(ptext) -> dict:
        if ptext == 'x':
            return {}
        return {
            s: [(n, p) for n, p in (pair.split(B_CHAR[2]) for pair in np.split(B_CHAR[3]))]
            for snp in ptext.split(B_CHAR[0])
            for s, np in [snp.split(B_CHAR[1])]
        }
