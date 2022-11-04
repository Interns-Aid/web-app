from config import TestingConfig
from core.extensions import docs
from v1 import *


def add_docs(cfg):
    if not isinstance(cfg, TestingConfig):
        docs.register(UserProfile, blueprint="v1")
        docs.register(LogoutResource, blueprint="v1")
        docs.register(TokenRefreshResource, blueprint="v1")
        docs.register(LoginResource, blueprint="v1")
        docs.register(SignupResource, blueprint="v1")
        docs.register(EmailConfirmationResource, blueprint="v1")
