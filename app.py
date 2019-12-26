import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# connect to mongodb
DB_CLIENT = AsyncIOMotorClient('mongodb://root:secretPassword@mongo:27017')
DB = DB_CLIENT['kv_store']
# add TTl
ttl = 60*5
DB.item.create_index("timestamp", expireAfterSeconds=ttl)

app = FastAPI(title="KV Store", version="0.1")


async def reset_ttl():
    await DB.item.drop_index("timestamp_1")
    await DB.item.create_index("timestamp", expireAfterSeconds=ttl)


# Get all Values
@app.get("/values/", tags=["values"])
async def get_all_values(limit: int = 0, skip: int = 0):
    """
    Get all the values of the store.
    """
    try:

        await reset_ttl()
        n = 0 if limit > 0 else await DB.item.count_documents({})
        items_cursor = DB.item.find()
        results = await items_cursor.to_list(n)
        print(results)
        values = {}
        for d in results:
            values.update({d['key']: d['value']})
        return values

    except Exception as e:
        print("Exception: \n", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Get values by keys
@app.get("/values", tags=["values"], status_code=200)
async def read_value(keys: str):
    """
    Get one or more specific values from the store and also reset the TTL of those keys.

    response: {key1: value1, key2: value2}
    """
    try:

        print('\nQuery Params:', keys, '\n')
        await reset_ttl()
        values = {}
        for k in keys.split(','):
            d = await DB.item.find_one({"key": k})
            values.update({d['key']: d['value']})
            return values

    except Exception as e:
        print("Exception: \n", e)
        if str(e).split()[0] == "'NoneType'":
            raise HTTPException(status_code=404, detail="Value not found")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Create Value
@app.post("/values", tags=["values"], status_code=201)
async def create_value(request: Request):
    """
    Save a value in the store.

    request: {key1: value1, key2: value2..}
    """
    try:

        items = await request.json()
        print(items)
        for key in items:
            d = {
                'key': key,
                'value': items[key],
                'timestamp': datetime.utcnow()
            }
            await DB.item.insert_one(d)
        return {'detail': 'key-values stored'}

    except Exception as e:
        print("Exception: \n", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Update values by keys
@app.patch("/values", tags=["values"])
async def update_value(request: Request):
    """
    Update a value in the store and also reset the TTL.

    request: {key1: value1, key2: value2..}
    """
    try:

        await reset_ttl()
        items = await request.json()
        print(items)
        for key in items:
            d = {
                'key': key,
                'value': items[key],
                'timestamp': datetime.utcnow()
            }
            await DB.item.update_one({"key": key}, {"$set": d})
        return {'detail': 'Values Updated'}

    except Exception as e:
        print("Exception: \n", e)
        raise HTTPException(status_code=304, detail="Not Modified")


@app.on_event("startup")
async def app_startup():
    print('\nApi running...\n')


@app.on_event("shutdown")
async def app_shutdown():
    # close connection to DB
    DB_CLIENT.close()


if __name__ == '__main__':
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=5000,
        reload=True
    )
