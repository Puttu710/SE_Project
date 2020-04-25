from graphql_client import gql, get_gql_client
import pprint

def query_question_for_page(Id):
    client = get_gql_client()
    
    query_question = gql('''
        query {
            questionWithId (Id: ''' + str(Id) + ''') {
                Title
                Body
                VoteCount
                answers {
                    edges {
                        node {
                            Id
                            Body
                            VoteCount
                            answerAuthor {
                                Id
                                FirstName
                                LastName
                            }
                        }
                    }
                }
                questionAuthor {
                    Id
                    FirstName
                    LastName
                }
            }
        }
    ''')
    question = client.execute(query_question)
    question = question['questionWithId']
    return question
    # pprint.pprint (question)

if __name__ == "__main__":
    question = query_question_for_page(2)
    pprint.pprint (question)