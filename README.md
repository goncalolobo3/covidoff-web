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

| Path           | Verb | Login required | Endpoint                     |
|----------------|------|----------------|------------------------------|
| tracker/       | GET  | Yes            | Displays the patient form    |
| tracker/match/ | POST | No             | Registers a new device match |

The `POST tracker/match/` view accepts the following arguments, as key-value pairs in a JSON object.

## License

Copyright 2020 tech4COVID19

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

