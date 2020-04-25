from graphql_client import gql, get_gql_client


def register_user (emailId, firstName, lastName, password):
    client = get_gql_client()

    insert_users = gql('''
        mutation {
            createUser
            (
                EmailId: "''' + emailId + '''",
                FirstName: "''' + firstName + '''",
                LastName: "''' + lastName + '''",
                Password: "''' + password + '''"
            ) 
            {
                user 
                {
                    Id
                }
            }
        }
    ''')
    mutation_result = client.execute(insert_users)
    # print (mutation_result)

if __name__ == "__main__":
    emailId = "surbhi.sharma@students.iiit.ac.in"
    firstName = "Surbhi"
    lastName = "Sharma"
    password = "Surbhi"
    register_user(emailId, firstName, lastName, password)