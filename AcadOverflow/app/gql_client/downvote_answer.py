from graphql_client import gql, get_gql_client

def downvote_answer(aId):
    client = get_gql_client()
    
    downvote = gql('''
        mutation {
            updateAnswerVotecount (Id: ''' + str(aId) + ''', val: -1) {
                answer {
                    VoteCount
                }
            }
        }
    ''')

    try:
        mutation_result = client.execute(downvote)
        print (mutation_result)
    except Exception as e:
        print (e)

if __name__ == "__main__":
    aId = 2
    downvote_answer(aId)