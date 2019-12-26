## REST key-val store
#### Built with [fastapi](https://fastapi.tiangolo.com/ "fastapi") + MongoDB
An API with the following endpoints to create a key-value store. The purpose of the API is to store any arbitrary length value in a persistent store with respect to a key and later fetch these values by keys. These values will have a TTL (for example 5 minutes) and after the TTL is over, the values will be removed from the store.

## Run the application
```bash
sudo docker-compose up
```


## Endpoints

### ```GET /values```
Get all the values of the store.

response: ```{key1: value1, key2: value2, key3: value3...}```

### ```GET /values?keys=key1,key2```
Get one or more specific values from the store and also reset the TTL of those keys.

response: ```{key1: value1, key2: value2}```

### ```POST /values```
Save a value in the store.

request: ```{key1: value1, key2: value2..}```
response: whatever’s appropriate

### ```PATCH /values```
Update a value in the store and also reset the TTL.

request: ```{key1: value1, key2: value2..}```
response: whatever’s appropriate

## Constraints
- ### Must be done
    - [x] Use appropriate status codes with all the responses.
    - [x] Values can be of arbitrary length
    - [x] Remove all values stored over more than 5 minutes. Set a TTL.
    - [x] Has to be FAST
- ### Good to have
    - [x] Reset TTL on every GET Request.
    - [x] Must be fault-tolerant, persistent
    - [x] It's a plus if you can run the service with single command
    - [ ] writing test case is also encourged if possible

