from graphql_client import gql, client

def post_question(qtitle, qbody, tags_list, userId):
    if len(tags_list) != 0:
        tags = "{" + tags_list[0]
        for tag in tags_list[1:]:
            tags += ", " + tag
        tags += "}"
 
    insert_question = gql('''
        mutation {
            insert_Questions(
                objects: {
                    Title: "''' + qtitle + '''",
                    Body: "''' + qbody + '''",
                    Tags: "''' + tags + '''",
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
        mutation_result = client.execute(insert_question)
        print ("Question Id: ", mutation_result)
    except Exception as e:
        print (e)

if __name__ == "__main__":
    qtitle = "question6"
    qbody = "This is question #6."
    tags_list = ["tag1", "tag2", "tag3", "tag4"]
    userId = 1
    post_question(qtitle, qbody, tags_list, userId)