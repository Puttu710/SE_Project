from graphql_client import gql, get_gql_client
import sys

def get_login_details(emailId):
    client = get_gql_client()
    
    query_user = gql('''
        query {
            userEmailId (EmailId: "''' + emailId + '''") {
                Id
                FirstName,
                LastName,
                EmailId,
                Password
            }
        }
    ''')
    user = client.execute(query_user)
    if len(user["userEmailId"]) == 0:
        return None
    return user["userEmailId"]

if __name__ == "__main__":
    emailId = "bhavi.dhingra@students.iiit.ac.in"
    user = get_login_details(emailId)
    print (user)