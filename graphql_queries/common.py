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
