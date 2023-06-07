import asyncio  
from datetime import datetime
from pytz import timezone
from xtravision import XtraVision
import traceback

credentials = {
    "orgId": "Add your data",
    "appSecret": "Add your data",
    "appId": "Add your data"
}

async def register_user():
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
        return await xtra_obj.register_user(user_obj)
    except Exception as e:
        error_handler(e)

async def do_some_operation(user_id):
    xtra_obj = XtraVision({**credentials, "userId": user_id}, {"expiresIn": "2h"})
    auth_token = xtra_obj.get_auth_token()
    print(f"Auth token for user ID {user_id}: {auth_token}")

    session_data = await xtra_obj.get_session_id()
    print("Session data:", session_data)

    current_date = datetime.now(timezone("America/New_York"))
    current_month_first_day = str(datetime(current_date.year, current_date.month, 1))
    limit = 5
    offset = 0
    is_required_stats = True

    assessment_results = await xtra_obj.get_user_assessment_results(
        limit,
        offset,
        {
            "startDate": current_month_first_day,
            "endDate": str(current_date),
            "isRequiredStats": is_required_stats
        }
    )

    print("User assessment results:", assessment_results)
    if "userAssessmentResult" in assessment_results:
        if assessment_results['userAssessmentResult']:
            print("First result of assessment results:", assessment_results['userAssessmentResult'][0]['results'])

def error_handler(e):
    print("ErrorHandler:", e)
    print("Error Object:", e.__dict__)

async def start():
    try:
        user_details = await register_user()
        print("User details:", user_details)

        await do_some_operation(user_details["id"])

    except Exception as e:
        print(traceback.format_exc())
        error_handler(e)

asyncio.run(start())  

