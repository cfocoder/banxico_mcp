# Banxico SIE API: USD/MXN Exchange Rate Endpoints

This document explains two Banxico SIE API endpoints for retrieving the daily exchange rate of USD vs MXN.

---

## 1. Series Data Endpoint (All Data)

**Endpoint:**
```
GET /series/SF63528/datos
```
**Full URL Example:**
```
https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528/datos?token=YOUR_TOKEN
```
**Description:**
Returns all available daily exchange rate data points for USD/MXN.

**HTTP Method:**
- GET

**Parameters:**
| Name   | Type   | Required | Description                  |
|--------|--------|----------|------------------------------|
| token  | string | Yes      | Your API access token        |

---

## 2. Latest Value Endpoint

**Endpoint:**
```
GET /series/SF63528/datos/oportuno
```
**Full URL Example:**
```
https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528/datos/oportuno?token=YOUR_TOKEN
```
**Description:**
Returns only the most recent (latest) daily exchange rate value for USD/MXN.

**HTTP Method:**
- GET

**Parameters:**
| Name   | Type   | Required | Description                  |
|--------|--------|----------|------------------------------|
| token  | string | Yes      | Your API access token        |

---

## How to Call These Endpoints

1. Replace `YOUR_TOKEN` with your valid Banxico API token.
2. Use the GET method to request the endpoint URL.
3. The response will be in JSON format.

**Example using curl:**
```sh
curl "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528/datos?token=YOUR_TOKEN"
curl "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF63528/datos/oportuno?token=YOUR_TOKEN"
```

---

For more details, see the [Banxico SIE API documentation](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/ejemplos).
