import jwt, re, logging
import traceback
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.conf import LazySettings
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from urllib import parse
from rbac.models import UserProfile
from django.db import close_old_connections

warn_logger = logging.getLogger('warn')
settings = LazySettings()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        try:
            query = parse.parse_qs(scope['query_string'].decode("utf-8"))['token'][0]
            if query:
                try:
                    user_jwt = jwt.decode(
                        query,
                        settings.SECRET_KEY,
                    )
                    scope['user'] = UserProfile.objects.get(
                        id=user_jwt['user_id']
                    )
                except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
                    traceback.print_exc()
                    pass
                except Exception as e:  # NoQA
                    warn_logger.warning(scope)
                    traceback.print_exc()

            return self.inner(scope)
        except:
            scope['user']=AnonymousUser()
            return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))