from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BaseAuthenticatedMixin:
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    authentication_classes = (
        TokenAuthentication,
    )
