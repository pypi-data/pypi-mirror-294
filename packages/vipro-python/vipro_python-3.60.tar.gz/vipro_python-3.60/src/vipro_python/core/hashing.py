import pandas as pd
import hashlib

class Hasher:
    """ takes a salt, pepper and input and hashes it """

    def __init__(self, salt: bytes, pepper: bytes):
        self.salt = salt
        self.pepper = pepper

    def sha256_map(self, df: pd.DataFrame, on: str):
        return df[on].map(self.sha256)

    def sha256(self, input: str):
      """ takes the input and hashes it using your static salt and pepper """
      # no input, no output
      if pd.isna(input):
          return None
      try:
          m = hashlib.sha256()
          m.update(self.salt)
          m.update(input.encode())
          m.update(self.pepper)
          return m.hexdigest()
      except Exception as ex:
          print('Hasher.sha256(self, input) unable to hash value {}'.format(input))
          raise ex
