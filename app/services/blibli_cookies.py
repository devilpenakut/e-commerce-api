import couchdb
import random
import datetime

couch = couchdb.Server("http://admin:admin@103.175.216.100:5984")

# Buat database jika belum ada
if "blibli_cookies_db" not in couch:
    db = couch.create("blibli_cookies_db")
else:
    db = couch["blibli_cookies_db"]


def get_blibli_cookies():
    """Ambil cookie string Blibli secara acak dari CouchDB. Hapus yang sudah expired."""
    all_cookies = []
    for doc_id in db:
        doc = db[doc_id]
        if datetime.datetime.now() < datetime.datetime.fromisoformat(doc["expire"]):
            all_cookies.append(doc)
        else:
            db.delete(doc)

    if not all_cookies:
        return None

    random_doc = random.choice(all_cookies)
    return random_doc["cookie_string"]


def add_blibli_cookies(cookie_string):
    """Simpan cookie string Blibli baru ke CouchDB dengan expiry 3 hari."""
    date_expire = datetime.datetime.now() + datetime.timedelta(days=3)
    db.save({"cookie_string": cookie_string, "expire": date_expire.isoformat()})
