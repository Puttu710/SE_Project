from graphql_client import gql, get_gql_client

def upvote_question(qId):
    client = get_gql_client()
    
    upvote = gql('''
        mutation {
            updateQuestionVotecount (Id: ''' + str(qId) + ''', val: 1) {
                question {
                    VoteCount
                }
            }
        }
    ''')

    try:
        mutation_result = client.execute(upvote)
        print (mutation_result)
    except Exception as e:
        print (e)

if __name__ == "__main__":
    qId = 2
    upvote_question(qId)