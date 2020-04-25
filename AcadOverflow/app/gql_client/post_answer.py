from graphql_client import gql, get_gql_client, process_entry_for_gql

def post_answer(qId, aBody, userId):
    client = get_gql_client()
    
    aBody = process_entry_for_gql(aBody)

    insert_answer = gql('''
        mutation {
            createAnswer (
                UserId: ''' + str(userId) + ''',
                Body: "''' + aBody + '''",
                QuestionId: ''' + str(qId) + '''
            ) {
                answer {
                    Id
                }
            }
        }
    ''')

    try:
        mutation_result = client.execute(insert_answer)
        print ("Answer Id: ", mutation_result)
    except Exception as e:
        print (e)

if __name__ == "__main__":
    qId = 1
    aBody = "This is an answer #1 for question #8."
    userId = 1
    post_answer(qId, aBody, userId)