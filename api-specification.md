## API仕様

### あおり運転判定API
画像を送信して、あおり運転を判定する

#### URL
/api/reckless_driving/analyze

#### Method
POST

#### Content Type
application/json

#### Request 

```
{
  "current_time": "2018-00-00 00:00:00",
  "images": [
   "dGVzdGV0c3Q=", // base64
   "dGVzdGV0c3Q=",
   "dGVzdGV0c3Q=",
   "dGVzdGV0c3Q=",
   "dGVzdGV0c3Q="
  ]
}
```

#### Response
##### Status code: 200
```
{
  "status": true,
  "current_time": "2018-00-00 00:00:00",
  "reckless_level": 5 // 0-5
}

```
### あおり運転通報API
画像を送信して、あおり運転を通報する

#### URL
/api/reckless_driving/report

#### Method
POST

#### Content Type
application/json

#### Request 

```
{
  "images": [
   "dGVzdGV0c3Q=", // base64
  ]
}
```

#### Response
##### Status code: 200

```
{
  "status": true
}
```
