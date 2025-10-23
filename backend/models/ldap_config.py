from pydantic import BaseModel

# TODO: узнать какие ещё свойства есть у LDAP


class LDAPConfig(BaseModel):
    server_url: str
    search_base: str
    search_filter: str
