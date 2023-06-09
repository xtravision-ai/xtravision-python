from datetime import datetime
from pytz import timezone
from xtravision import XtraVision
import traceback

credentials = {
    "orgId": "__ORG_ID__",
    "appId": "__APP-ID__",
    "appSecret": "__APP-SECRET-KEY__",
}

def register_user():
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
    try:
        return xtra_obj.register_user(user_obj)
    except Exception as e:
        error_handler(e)

def do_some_operation(user_id):
    xtra_obj = XtraVision({**credentials, "userId": user_id}, {"expiresIn": 2})
    auth_token = xtra_obj.get_auth_token()
    print(f"Auth token for user ID {user_id}: {auth_token}")

    session_data =  xtra_obj.get_session_id()
    print("Session data:", session_data)

    # current_date = datetime.now(timezone("America/New_York"))
    # current_month_first_day = str(datetime(current_date.year, current_date.month, 1))
    limit = 5
    offset = 0
    # is_required_stats = True
    # Update your required session-id
    session_id = "3dba0e32-a610-4dfc-89fe-5092b78241b7" # example of session-id

    assessment_results = xtra_obj.get_user_assessment_results(
        limit,
        offset,
        {
            # "startDate": current_month_first_day,
            # "endDate": str(current_date),
            # "isRequiredStats": is_required_stats, # Additional stats 
            "sessionId":  session_id   # Any specific session data required
         }
    )

    print("User assessment results:", assessment_results)
    if "userAssessmentResult" in assessment_results:
        if assessment_results['userAssessmentResult']:
            print("First result of assessment results:", assessment_results['userAssessmentResult'][0]['results'])

def error_handler(e):
    print("ErrorHandler:", e)
    print("Error Object:", e.__dict__)

def start():
    try:
        user_details = register_user()
        print("User details:", user_details)

        if user_details is None:
              raise Exception("User registration failed! Check above error")

        do_some_operation(user_details["id"])

        print("All done! Let's Start Integration. :) ")

    except Exception as e:
        print(traceback.format_exc())
        error_handler(e)


# Start demo testing
start()

