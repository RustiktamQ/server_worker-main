from models.ldap_config import LDAPConfig
from models.user import User
# from ldap3 import Server, Connection, ALL
from typing import Optional


class LDAPService:
    def __init__(self, config: LDAPConfig):
        self.config = config
        # self.server = Server(config.server_url, get_info=ALL)

    # def authenticate(self, username: str, password: str) -> Optional[User]:
    #     try:
    #         conn = Connection(
    #             self.server, user=username, password=password, auto_bind=True
    #         )
    #         if conn.bind():
    #             return User
    #         else:
    #             return None
    #     except Exception as e:
    #         return None
