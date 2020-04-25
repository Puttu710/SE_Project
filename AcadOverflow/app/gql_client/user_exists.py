from graphql_client import gql, get_gql_client
import sys

def user_exists(emailId):
    client = get_gql_client()
    
    query_user = gql('''
        query {
            userEmailId (EmailId: "''' + emailId + '''") {
                EmailId
            }
        }
    ''')
    user = client.execute(query_user)
    print (user["userEmailId"])
    if not user["userEmailId"]:
        return False
    if emailId != user["userEmailId"]["EmailId"]:
        return False
    return True

if __name__ == "__main__":
    emailId = "bhavi.dhingra@students.iiit.ac.in"
    if user_exists(emailId):
        print ("User already has an account!!")
    else:
        print ("New Registration!!")