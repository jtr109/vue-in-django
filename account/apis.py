import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View


class LoginView(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        body = json.loads(request.body)  # TODO: request validation
        user = authenticate(**body)
        if user is None:
            return JsonResponse(dict(status='error', message='wrong password'))
        login(request, user)
        return JsonResponse(dict(status='success'))


class GetUserInfoView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse(dict(status='error', message='not login'))
        return JsonResponse(dict(status='success',data=dict(username=user.username)))


class LogoutView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse(dict(status='error', message='not login'))

        logout(request)
        return JsonResponse(dict(status='success'))
