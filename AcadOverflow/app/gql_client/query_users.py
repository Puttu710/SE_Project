from graphql_client import gql, get_gql_client

def print_users():
    client = get_gql_client()

    query_users = gql('''
        query {
            allUsers {
                edges {
                    node {
                        Id
                        FirstName
                        LastName
                        EmailId
                    }
                }
            }
        }
    ''')
    users = client.execute(query_users)
    for user in users["allUsers"]["edges"]:
        print (user["node"])

if __name__ == "__main__":
    print_users()