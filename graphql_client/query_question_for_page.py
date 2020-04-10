from graphql_client import gql, client
import pprint

def query_question_for_page(Id):
    query_question = gql('''{
            Questions_by_pk(Id: ''' + str(Id) + ''') {
                Title
                Body
                VoteCount
                Question_Answers(order_by: {VoteCount: desc}) {
                    Body
                    VoteCount
                    Answer_User {
                        Id
                        FirstName
                        LastName
                    }
                }
                Question_User {
                    Id
                    FirstName
                    LastName
                }
            }
        }
    ''')
    question = client.execute(query_question)
    question = question['Questions_by_pk']  # "by_pk" means to query an entry by the private key
    pprint.pprint (question)

if __name__ == "__main__":
    query_question_for_page(2)