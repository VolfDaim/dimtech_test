from sanic_jwt import exceptions


async def auth(request, *args, **kwargs):
    username = request.json['username']
    password = request.json['password']

    if not username:
        raise exceptions.AuthenticationFailed("Enter username")
    if not password:
        raise exceptions.AuthenticationFailed("Enter password")