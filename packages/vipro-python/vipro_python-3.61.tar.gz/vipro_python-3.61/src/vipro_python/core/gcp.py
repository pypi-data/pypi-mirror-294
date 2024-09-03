from google.cloud.sql.connector import Connector

class CloudSQLConnector:
  def __init__(self):
    self._c = Connector()

  def open_with_secrets(self, sm, inst_secret: str, user: str, pwd_secret: str, db: str):
    inst = sm.read(inst_secret)
    pwd = sm.read(pwd_secret)
    return self.open(inst, user, pwd, db)

  def open(self, inst: str, user: str, pwd: str, db: str):
    print(f"connecting to Cloud SQL Instance: {inst} using password (len={len(pwd)})")
    conn = self._c.connect(
        inst,
        "pytds",
        user=user,
        password=pwd,
        db=db,
    )
    return conn
