from rest_framework.pagination import LimitOffsetPagination


class CommentLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 30