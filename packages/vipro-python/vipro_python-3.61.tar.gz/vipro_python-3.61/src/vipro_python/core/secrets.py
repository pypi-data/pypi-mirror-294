from google.cloud import secretmanager

class SecretReader:
  def __init__(self, gcp_project: str, auth_instance: str):
    self.sm = secretmanager.SecretManagerServiceClient()
    self.proj = gcp_project
    self.auth = auth_instance

  def shared(gcp_project: str = "vipro-core-services"):
    """ static for shared secrets """
    return SecretReader(gcp_project, 'shared')
  
  def read(self, secret_name: str, version: str = 'latest', encoding: str = 'UTF-8'):
    uri = f"projects/{self.proj}/secrets/{self.auth}-{secret_name}/versions/{version}"
    response = self.sm.access_secret_version(request={"name": uri})
    data = response.payload.data
    return data if encoding is None else data.decode(encoding)

def read_secret(gcp_project: str, auth_instance: str, secret_name: str, version: str = 'latest', encoding: str = 'UTF-8'):
  return SecretReader(gcp_project, auth_instance).read(secret_name, version, encoding)
