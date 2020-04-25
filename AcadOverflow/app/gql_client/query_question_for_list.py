from graphql_client import gql, get_gql_client

def query_question_for_list(Id):
    client = get_gql_client()
    
    query_question = gql('''
        query {
            questionWithId (Id: ''' + str(Id) + ''') {
                Title
                Body
                VoteCount
            }
        }
    ''')
    question = client.execute(query_question)
    return question["questionWithId"]
    # print ("Title:", question['Title'])
    # print ("Body:", question['Body'])
    # print ("VoteCount:", question['VoteCount'])

if __name__ == "__main__":
    question = query_question_for_list(2)
    print (question)