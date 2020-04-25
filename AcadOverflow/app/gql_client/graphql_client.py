from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def get_transport(igraphql_url):
    transport=RequestsHTTPTransport(
            url=igraphql_url,
            use_json=True,
            headers={
                "Content-type": "application/json",
            },
            verify=False
        )
    return transport

def get_gql_client():
    transport = get_transport('http://127.0.0.1:5005/graphql')
    client = Client(
        retries=3,
        transport=transport,
        fetch_schema_from_transport=True,
    )
    return client

def process_single_quotes(sEntry):
    temp_entry = ""
    for i in range(len(sEntry)):
        if sEntry[i] == '\'':   
            bwdslash_count = 1
            len_temp_entry = len(temp_entry)
            while bwdslash_count <= len_temp_entry and temp_entry[-bwdslash_count] == '\\':
                bwdslash_count += 1
            bwdslash_count -= 1
            if bwdslash_count % 2:
                temp_entry = temp_entry[:-1] + " "
            elif bwdslash_count:
                temp_entry += ' '
        temp_entry += sEntry[i]
    return temp_entry

def process_entry_for_gql(sEntry):
    sEntry = repr(sEntry)                           # for '\n' character, converting into raw string
    sEntry = process_single_quotes(sEntry)
    sEntry = sEntry.replace("\\xa0", "")            # Error: Invalid character escape sequence: \x.
    # sEntry = sEntry.replace("\\\\'", "\\\\ '")      # test case - '\\' failed
    sEntry = sEntry.replace("\"", "\\\"")           # put escape character before "
    # sEntry = sEntry.replace("\\'", "'")             # replace \' with '
    return sEntry