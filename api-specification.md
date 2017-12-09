## API仕様

### あおり運転判定API
画像を送信して、あおり運転を判定する

#### URL
/api/reckless_driving/image_upload

#### Method
PUT

#### Content Type
application/json

#### Request 

```
{
  "current_time": "2018-00-00 00:00:00"
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

```
{
  "current_time": "2018-00-00 00:00:00"
  "reckless_level": 5 // 0-5
}
```
