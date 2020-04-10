from graphql_client import gql, client

def register_user(emailId, firstName, lastName, password):
    insert_users = gql('''
        mutation {
            insert_Users (
                objects:{
                    EmailId: "''' + emailId + '''",
                    FirstName: "''' + firstName + '''",
                    LastName: "''' + lastName + '''",
                    Password: "''' + password + '''"
                }
            ) {
                returning {
                    Id
                }
            }
        }
    ''')

    try:
        mutation_result = client.execute(insert_users)
        print (mutation_result)
    except Exception as e:
        print (e)

if __name__ == "__main__":
    emailId = "bhavi.dhingra@students.iiit.ac.in"
    firstName = "Bhavi"
    lastName = "Dhingra"
    password = "bhavi"
    register_user(emailId, firstName, lastName, password)