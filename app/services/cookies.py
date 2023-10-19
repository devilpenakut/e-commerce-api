import couchdb
import random
import datetime

couch = couchdb.Server("http://admin:admin@103.175.216.100:5984")

db = couch["cookies_db"]


def get_cookies():
    all_cookies = []
    for id in db:
        doc = db[id]
        # chek expire first
        if datetime.datetime.now() < datetime.datetime.fromisoformat(doc["expire"]):
            all_cookies.append(doc)
        else:
            # delete expired cookies
            db.delete(doc)

    # pick random cookies
    random_cookies = random.choice(all_cookies)
    return random_cookies["cookies"]


def addCookies(cookies):
    date_expire = datetime.datetime.now() + datetime.timedelta(days=3)

    date_expire = date_expire.isoformat()
    # loop all and replace all "true" to "True" and "false" to "False"
    new_cookies = []
    for cookie in cookies:
        new_cookie = {}
        for key, value in cookie.items():
            if value == "true":
                new_cookie[key] = True
            elif value == "false":
                new_cookie[key] = False
            else:
                new_cookie[key] = value
        new_cookies.append(new_cookie)
    db.save({"cookies": new_cookies, "expire": date_expire})
