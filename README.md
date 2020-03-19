# covidoff-web

This repository contains the source code for the Web components of the covidoff system, which is a fundamental component for the system integration, consisting of a webportal front-end and the server backend. The server acts as the data collector for the mobile devices to send their information, and also for the web portal to send notifications to the mobile users. 

## Getting Started

## Server API

| Path           | Verb | Description                                      |
|----------------|------|--------------------------------------------------|
| tracker/       | PUT  | Register an encounter between two devices.       |
| announcements/ | PUT  | Register and broadcast a message to all devices. |
| announcements/ | GET  | List previous announcements.                     |

### PUT tracker/

Endpoint for registering encounters (matches) between devices. It accepts and returns `application/json` content type. The input is a JSON object with the following key-value attributes:

| Key      | Type   | Description                |
|----------|--------|----------------------------|
| matcher  | String | Device reporting the match |
| matchee  | String | Device being matched       |

Return values:

| Code | Meaning             | Value           |
|------|---------------------|-----------------|
| 200  | Request OK          | {}              |
| 400  | Request is not JSON | Array of errors |
| 422  | Input is not valid  | Array of errors |

### PUT announcements/
### GET announcements/

## License 

Open source
