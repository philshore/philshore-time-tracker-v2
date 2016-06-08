from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

headers = settings.RESP_HEADERS


def resp_ok(dataset):
    return Response(dataset,
                    headers=headers,
                    status=status.HTTP_200_OK)


def resp_error(errorset):
    return Response(errorset,
                    headers=headers,
                    status=status.HTTP_400_BAD_REQUEST)


def resp_error_none():
    return Response(None,
                    headers=headers,
                    status=status.HTTP_400_BAD_REQUEST)


def resp_create(dataset):
    return Response(dataset,
                    headers=headers,
                    status=status.HTTP_201_CREATED)
