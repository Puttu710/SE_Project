from graphql_client import gql, get_gql_client, process_entry_for_gql

def post_question(qtitle, qbody, tags_list, userId):
    client = get_gql_client()

    if len(tags_list) != 0:
        tags = ""
        for tag in tags_list[1:]:
            tags += tag + "|"
        tags = tags[:-1]    # remove the last '|'

    qtitle = process_entry_for_gql(qtitle)     # for '\n' character, converting into raw string
    qbody = process_entry_for_gql(qbody)

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
    qtitle = "question2"
    qbody = "This is question #2.\n trying multi-line!!"
    tags_list = ["tag1", "tag2", "tag3"]
    userId = 31
    post_question(qtitle, qbody, tags_list, userId)
