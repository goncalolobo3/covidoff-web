# covidoff-web

This repository contains the source code for the Web components of the covidoff system, which is a fundamental component for the system integration, consisting of a webportal front-end and the server backend. The server acts as the data collector for the mobile devices to send their information, and also for the web portal to send notifications to the mobile users. 

## Getting Started

Run docker and create an admin user. Use the credentials from that user to login.

```
docker-compose up
docker exec -it <container_id> python3 /srv/covidoff/manage.py createsuperuser
```
Now you can access the application at <https://localhost> and the admin site at <https://localhost/admin>.

The implementation either shows government- or healthcare-related views, depending on the settings. In order to switch between the two, change `COVIDOFF_HEALTHCARE_DEPLOY` and `COVIDOFF_GOVERNMENT_DEPLOY` to `True` or `False`, depending on which should be enabled. Notice that if the two are equal (e.g. both `True` or both `False`), the server will refuse to start.

### Setup

`Backend`, configure `AWS`

1. Run `aws config`
2. 

`Android`, configure `Firebase`

1. Go [here](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter Project name and click Continue
4. Choose whether you want analytics on your app, and, if so, what account to use
5. Finalize the setup by clicking "Create project"
6. Continue
7. Next to "Project overview", click the Settings wheel and then "Project settings"
8. Go to Cloud messaging
9. Find the setting Server key and copy it. Keep it. You'll need it later.

1. Go [here](https://sa-east-1.console.aws.amazon.com/sns/v3/home) and click "Start with an overview"
2. Under "Mobile", choose "Push notifications"
3. Click "Create platform application"
4. Enter your application name and select "Firebase Cloud Messaging (FCM)" from the "Push notification platform" menu
5. Paste the Firebase key you copied earlier on API Key
6. Click "Create platform application"
7. Select your `ARN` and keep it, for now. Example:
arn:aws:sns:sa-east-1:494854379016:app/GCM/covidoff-android

`iOS`, configure `Apple Push Notification Service`

1. Go to your Apple Developer account
2. Go to "Certificates, Identifiers & Profiles"
3. Select "Identifiers" from the left menu
4. Select your app from the Identifier list (create a new one if it's not listed)
5. Under "Capabilities", look for "Push notifications" and click "Edit"
6. Download the "Production SSL Certificate"
7. At the top of the page, look for `App ID Prefix` and keep that ID

(KeyChain)
7. Open the certificate with KeyChain, by clicking on it
8. When prompted to add the certificate, click "Add"
9. Copy the `App ID Prefix` from the previous step and enter it in the Search bar. You should see a single certificate on the list
10. Expand the certificate by clicking on the arrow
11. Select both lines
12. Right-click and select "Export 2 items..."
13. Make sure that the file format is `.p12`
14. Choose a password, if you want (it's optional)

1. Go [here](https://sa-east-1.console.aws.amazon.com/sns/v3/home) and click "Start with an overview"
2. Under "Mobile", choose "Push notifications"
3. Click "Create platform application"
4. Enter your application name and select "Apple iOS/VoIP/Mac" from the "Push notification platform" menu
5. Under "Push certificate type" select "iOS push certificate"
6. Click "Choose file" and look for the certificate the we downloaded on the previous step. Enter your password, if you set any.
7. Cick "Load credentials from file"
8. "Create platform application"
(Review process or link tutorial)
(Also setup Cognito)







## Server API

The server API is separated in three components:

* General purpose: views shared by all actors
* Government: views specific for governamental entities
* Healthcare: views specific for healthcare professionals

| Path                      | Verb | Login required | Endpoint                                                                  |
|---------------------------|------|----------------|---------------------------------------------------------------------------|
| /                         | GET  | No             | Redirects to the initial page, or the login page, if no session is active |
| admin/                    | GET  | No             | Shows the admin page                                                      |
| account/login/            | GET  | No             | Displays the login form                                                   |
| account/login/            | POST | No             | Submits a login form                                                      |
| account/logout/           | POST | No             | Logout, if a session is active                                            |
| account/recover/          | GET  | No             | Shows password recovery form                                              |
| account/recover/          | POST | No             | Submit a password recovery form                                           |
| account/recover/ok/       | GET  | No             | Displays a confirmation for a successful password recovery request        |
| account/recover/callback/ | GET  | No             | Password recovery email callback                                          |
| account/users/            | GET  | Yes            | Lists users, paginated                                                    |
| account/users/            | POST | Yes            | Send an invitation to a new user                                          |

All views return HTML, except `POST tracker/match/`, which both accepts and returns `application/json`. Currently, all views are exempt from CSRF verification, but only `POST tracker/match/` should be, since it's meant to accept AJAX requests.

### Government

| Path           | Verb | Login required | Endpoint                                           |
|----------------|------|----------------|----------------------------------------------------|
| broadcast/     | GET  | Yes            | Displays the broadcast message form                |
| broadcast/     | POST | Yes            | Broadcasts a message to all devices and stores it  |
| broadcast/ok/  | GET  | Yes            | Shows confirmation of a successful broadcast event |
| broadcast/log/ | GET  | Yes            | Lists previously broadcast messages                |


### Healtcare

| Path              | Verb | Login required | Endpoint                     |
|-------------------|------|----------------|------------------------------|
| tracker/          | GET  | Yes            | Displays the patient form    |
| tracker/match/    | POST | No             | Registers a new device match |
| tracker/find/<id> | POST | No             | Registers a new device match |

### AJAX endpoints

There are two AJAX enpoints, `POST tracker/match/` and `POST tracker/find/`. The former both accepts and returns `application/json`, the later takes only one argument in the URL, the user ID that we're looking to find.

Note: in the context of the app, this ID is what is given by the QR code. The return value is not specified yet.

These are to be called by the app and both accept and return `application/json`. All arguments are key-value pairs in a JSON object. No arrays for batch insertion are accepted yet.

`POST tracker/match`

| Argument     | Type         | Required  | Meaning                                                                 |
|--------------|--------------|-----------|-------------------------------------------------------------------------|
| matcher      | String       | Yes       | The device ID for the device that is reporting the match                |
| matchee      | String       | Yes       | The device ID for the device that was found                             |
| latitude     | Decimal(9,6) | No        | GPS latitude                                                            |
| longitude    | Decimal(9,6) | No        | GPS longitude                                                           |
| matcher_meta | String       | No        | Meta string for any optional relevant information regarding the matcher |
| matchee_meta | String       | No        | Meta string for any optional relevant information regarding the matchee |

Note: the absence of required arguments is accepted at this point, but it won't be in the future.

| Code | Return Value                                                                                                                                                                                                                                      | Meaning                            |
|------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|
| 400  | {"error": "<description>"}                                                                                                                                                                                                                        | JSON format is invalid             |
| 422  | {"longitude": ["Enter a number."]}                                                                                                                                                                                                                | JSON is valid, but the data is not |
| 200  | {<br>"id": 10,<br>"matcher": "id",<br>"matchee": "id",<br>"latitude": "114.2999353",<br>"longitude": "114.2999353",<br>"timestamp": "2020-03-23T22:33:57.692Z",<br>"matcher_meta": "meta information",<br>"matchee_meta": "meta information"<br>} | OK                                 |,
