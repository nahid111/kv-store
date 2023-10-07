import redis
from fastapi import APIRouter

r = redis.Redis(host='redis', port=6379, db=0)

router = APIRouter(tags=[""])


@router.get("/")
def read_item(keys: str = None):
    res = {}
    if keys:
        keys = keys.split(",")
    else:
        keys = r.keys()
    for k in keys:
        res[k] = r.get(k)
        r.expire(k, 300)
    return res


@router.post("/")
def create_item(payload: dict):
    for k, v in payload.items():
        cache = r.get(k)
        if cache:
            print(f"Cache hit for {k}:{v}")
        else:
            print(f"Cache miss for {k}:{v}")
            r.set(k, v)
            r.expire(k, 300)
    return


@router.put("/")
def update_items(payload: dict):
    for k, v in payload.items():
        r.set(k, v)
        r.expire(k, 300)
    return


@router.delete("/{key}")
def delete_item(key):
    r.delete(key)
    return "item deleted"
