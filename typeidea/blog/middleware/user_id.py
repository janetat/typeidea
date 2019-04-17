import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # 所有请求会经过此中间件，在后面的流程中request多了一个uid属性，用来标识用户。
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)

        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
