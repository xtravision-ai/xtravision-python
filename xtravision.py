from datetime import datetime, timedelta
import requests
from jose import jwt

#  GraphQL Schema
REGISTER_USER_MUTATION = """
mutation registerUser(
  $firstName: String, 
  $lastName: String,  
  $profileData: JSON, 
  $timezone: String, 
  $email: String!
) {
  registerUser(
    firstName: $firstName, 
    lastName: $lastName, 
    email: $email, 
    profileData: $profileData, 
    timezone: $timezone
  ) {
    id
    firstName
    lastName
    email
    profileData
    timezone
  }
}
"""

USER_SESSION_CREATE_MUTATION = """
mutation createUserSession {
  createUserSession {
    id
    userId
    createdAt
  }
}
"""

REGISTER_TRAINER_MUTATION = """
mutation registerTrainer($firstName: String, $lastName: String, $email: String!) {
  registerTrainer(firstName: $firstName, lastName: $lastName, email: $email) {
    id
    firstName
    lastName
  }
}
"""

GET_USER_ASSESSMENT_RESULTS = """
query getUserAssessmentResults($limit: Int, $offset: Int, $userAssessmentFilter: userAssessmentFilter!) {
  getUserAssessmentResults(limit: $limit, offset: $offset, userAssessmentFilter: $userAssessmentFilter) {
    total
    userAssessmentResult {
      assessmentName
      id
      results
      savedDate
      sessionId
      stats {
        additionalStats
        tsStats
      }
    }
  }
}
"""

AUTHORIZED_REQUEST_DATA_QUERY = """
query getAuthorizedRequestData($reqData: AuthRequest) {
  getAuthorizedRequestData(reqData: $reqData) {
    orgAppUser{
      id
      email
      firstName
      lastName
      createdAt
    }
    orgApp{
      id
      name
      createdAt
    }
    userSession{
      id
      userId
      createdAt
    }
  }
}
"""


# url = 'https://saasstagingapi.xtravision.ai/api/v1/graphql'
# url = 'http://localhost:4000/api/v1/graphql'
url = 'https://saasapi.xtravision.ai/api/v1/graphql'

class XtraVision:
    def __init__(self, credentials, params={"expiresIn": 2}):
        self.userId = credentials['userId'] if "userId" in credentials else None
        self.appId = credentials['appId']
        self.orgId = credentials['orgId']
        self.token = jwt.encode(
            {
                'userId': self.userId,
                'appId': self.appId,
                'orgId': self.orgId,
            },
            credentials['appSecret'],
            algorithm='HS256',
            headers={'exp': str(datetime.utcnow() + timedelta(hours=params["expiresIn"]))},
        )

    def get_auth_token(self):
        return self.token

    async def register_user(self, user_obj):
        variables = {
            "email": user_obj['email']
        }
        if 'firstName' in user_obj:
            variables["firstName"] = user_obj['firstName']
        if 'lastName' in user_obj:
            variables["lastName"] = user_obj['lastName']
        if 'profileData' in user_obj:
            variables["profileData"] = user_obj['profileData']
        if 'timezone' in user_obj:
            variables["timezone"] = user_obj['timezone']
        

        # Make a GraphQL call to XTRA SaaS server and return the data
        response = await self.callGraphqlQuery(REGISTER_USER_MUTATION, variables)
        return response["data"]['registerUser']

    async def get_session_id(self):
        variables = {}

        # Make a GraphQL call to XTRA SaaS server and return the data
        response = await self.callGraphqlQuery(USER_SESSION_CREATE_MUTATION, variables)
        return response["data"]['createUserSession']

    async def get_authorized_data(self, auth_token, session_id, data):
        req_data = {'authToken': auth_token, 'sessionId': session_id, 'data': data}
        response = await self.callGraphqlQuery(AUTHORIZED_REQUEST_DATA_QUERY, {'reqData': req_data})
        return response

    async def get_user_assessment_results(self, limit, offset, user_assessment_filter):
        variables = {}
        if user_assessment_filter:
            variables['userAssessmentFilter'] = user_assessment_filter
        if limit:
            variables['limit'] = limit
        if offset is not None:
            variables['offset'] = offset

        # Make a GraphQL call to XTRA SaaS server
        response = await self.callGraphqlQuery(GET_USER_ASSESSMENT_RESULTS, variables)
        return response["data"]['getUserAssessmentResults']
    
    async def callGraphqlQuery(self, query, variables=None, get_raw_response=False):
        """
        Make graphql query/mutation
        """
        # print("callGraphqlQuery:: Request QueryString= %s, Request Data= %s", " ".join(query.split()), variables)

        response = None
        if variables:
            response = requests.post(
                url,
                json={"query": query, "variables": variables},
                headers={"Authorization": self.token},
            )
        else:
            response = requests.post(
                url,
                json={"query": query},
                headers={"Authorization": self.token},
            )
        
        if get_raw_response:
            return response

        if response.status_code == 200:
            return response.json()

        # print actual error
        # logger.error("Got error message from API Server: %s", response.json())
        raise Exception(
            "Query failed to run by returning code of {}. {}".format(
                response.status_code, query
            )
        )
