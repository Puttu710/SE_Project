from graphql_client import gql, get_gql_client, process_entry_for_gql

import requests

def post_question_with_ML(qTitle, post_corpus, qBody, qURL, tags_list, overall_scores, \
                          sentiment_polarity, sentiment_subjectivity, userId):
    client = get_gql_client()

    if len(tags_list) != 0:
        tags = ""
        for tag in tags_list:
            tags += tag + "|"
        tags = tags[:-1]    # remove the last '|'

    qTitle = process_entry_for_gql(qTitle)
    post_corpus = process_entry_for_gql(post_corpus)
    qBody = process_entry_for_gql(qBody)
    qURL = process_entry_for_gql(qURL)

    insert_question = gql('''
        mutation {
            createQuestion(
                Title: "''' + qTitle + '''",
                postCorpus: "''' + post_corpus + '''",
                Body: "''' + qBody + '''",
                questionUrl: "''' + qURL + '''",
                Tags: "''' + tags + '''",
                overallScores: ''' + str(overall_scores) + ''',
                sentimentPolarity: ''' + str(sentiment_polarity) + ''',
                sentimentSubjectivity: ''' + str(sentiment_subjectivity) + ''',
                UserId: ''' + str(userId) + '''
            ) {
                question {
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
    qtitle = "question24123254"
    qbody = "This is question #1232.\n trying multi-line!234!"
    tags_list = ["tag1", "tag2", "tag3"]
    userId = 3
    post_question_with_ML(qtitle, "", qbody, "", tags_list, 0.0, 0.0, 0.0, userId)
