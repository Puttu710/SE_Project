from graphql_client import gql, client

def post_answer(qId, aBody, userId):
    insert_answer = gql('''
        mutation {
            insert_Answers(
                objects: {
                    QuestionId: ''' + str(qId) + ''',
                    Body: "''' + aBody + '''",
                    UserId: ''' + str(userId) + '''
                }
            ) {
                returning {
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
    qId = 8
    aBody = "This is an answer #1 for question #8."
    userId = 30
    post_answer(qId, aBody, userId)