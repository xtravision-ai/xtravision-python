# xtravision-python
The official python library for the XtraVision API.

## For Demo Application:
1. Clone repo and install dependencies using below commands  
    ```sh
    git clone https://github.com/xtravision-ai/xtravision-python.git
    pip install -r requirements.txt
    ````

2. Update credentials in demo.py file

    ```python
    credentials = {
    "orgId": "__ORG-ID__",
    "appSecret": "__App-ID__",
    "appId": "__App-Secret-Key__",
    "userId": None
    }
    ```
    Kindly update your testing user details also in same file. (firstName, lastName and email).


3. Run using below command on root directory

    ```sh
    python demo.py
    ```

 Auth token and other response data will be printed in console log. 

## How to Use xtravision.py to register user, get auth token etc,. 
# A.Register User
1. Import XtraVision class

    ```python
    from xtravision import XtraVision
    ```
2. Intialize class with credentials

    ```python
    credentials = {
    "orgId": "__ORG-ID__",
    "appSecret": "__App-ID__",
    "appId": "__App-Secret-Key__",
    "userId": None # userId should be None while registering new user
    }
    xtra_obj = XtraVision(credentials)
    user_obj = {
        "email": "joesmith@yourdomain.com",
        "firstName": "Joe",
        "lastName": "Smith",
        "profileData": {
            "height": 179,
            "weight": 80
        },
        "timezone": "America/New_York"
    }
    ```
3. Call register_user

    ```python
    user_details = await xtra_obj.register_user(user_obj)
    ```

# B. Get Auth Token
1. Import XtraVision class

    ```python
    from xtravision import XtraVision
    ```
2. Intialize class with credentials

    ```python
    credentials = {
    "orgId": "__ORG-ID__",
    "appSecret": "__App-ID__",
    "appId": "__App-Secret-Key__",
    "userId": "__USER-ID__" # Use userId obtained while registering user
    }
    xtra_obj = XtraVision(credentials, {"expiresIn": 2})
    ```
3. Call get_auth_token

    ```python
    auth_token = xtra_obj.get_auth_token()
    ```
# C. Similarly Session ID (xtra_obj.get_session_id) & User Assessment result (xtra_obj.get_user_assessment_results) can be obtained by referring demo.py 


## SDK API: 

- For API reference, kindly check [XtraVision GraphQL API Portal](https://xtravision-ai.github.io/)


