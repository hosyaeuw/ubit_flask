from models import Users


def authenticate(username, password):
    # print(username, password)
    # user = username_table.get(username, None)
    # print(user)
    # if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
    #     return user
    # return user
    print(username)
    print(password)
    user = Users.query.filter(Users.login == username).first()
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    print(user_id)
    return 1
#     return userid_table.get(user_id, None)
