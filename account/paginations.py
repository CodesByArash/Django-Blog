from rest_framework.pagination import (
    LimitOffsetPagination,
)




class UserLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10