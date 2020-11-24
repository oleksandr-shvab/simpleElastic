import elasticsearch
from elasticsearch import Elasticsearch
from datetime import datetime
from pprint import pprint


def create_index(es):
    print("Enter index name")
    index_name = input(">>> ")
    # If we have index with the same name rewrite it
    es.indices.create(index=index_name, ignore=400)


def delete_index(es):
    print("Enter index name")
    index_name = input(">>> ")
    es.indices.delete(index=index_name)


def find_all_indices(es):
    all_indices = sorted(es.indices.get_alias("*"))
    for index in all_indices:
        print(index)
    return all_indices


def find_all_document(es, index_name):
    query_all = {"size": 300, "query": {"match_all": {}}}
    # get a response using the Search API
    response = es.search(index=index_name, body=query_all)
    all_documents = response['hits']['hits']
    for doc in response['hits']['hits']:
        print(doc['_id'], doc['_source'])
    return all_documents


def add_document(es):
    body = {}
    print("All available indices:")
    find_all_indices(es)
    print("For witch index you want create document?:")
    index_name = input(">>> ")
    while True:
        print("If you want to finish enter 'exit' in 'field_name' field")
        field_name = str(input("Enter field name: "))
        if field_name == 'exit':
            break
        data = input("Enter value: ")
        body[field_name] = data
        print(body)

    # Add last_update field with current data
    body["last_update"] = datetime.now()
    result = es.index(index=index_name, body=body)
    print(result)


def reindex(es):
    """ Reindex all with wildcard """
    tasks = elasticsearch.client.TasksClient(es)
    all_indices = find_all_indices(es)
    wildcard = input("Enter from which word index mast start:  ")
    wildcard_length = len(wildcard)
    destination_index = input("Enter word to reindex: ")

    for i, source_index in enumerate(all_indices):
        if source_index.startswith(wildcard):
            sufix = str(source_index[wildcard_length:])
            # Index mast be not empty before reindex
            result = es.reindex({
                "source": {"index": source_index},
                "dest": {"index": destination_index + sufix}
            },  request_timeout=30, wait_for_completion=True)
            # Manage tasks
            # pprint(tasks.list())
            if result['total'] and result['took'] and not result['timed_out']:
                print("Index: ", source_index, " Seems reindex was successful, going to delete the old index!")
                es.indices.delete(source_index, timeout='300s')
            else:
                print("Seems there is some trouble with reindex, please make sure the index has documents")



def update_documents(es):
    tasks = elasticsearch.client.TasksClient(es)
    index_name = input("Enter index name: ")
    all_documents = find_all_document(es, index_name)
    # put them all into an empty list
    documents = []
    for num, doc in enumerate(all_documents):
        documents += [doc['_id']]

    # Iterate over the list of documents
    for num, doc_id in enumerate(documents):
        # Generate data to change
        date = datetime.now()
        source_to_update = {"doc": {"last_update": date}}
        try:
            # Update document with prepared data
            response = es.update(index=index_name, doc_type="_doc", id=doc_id,
                                 body=source_to_update, request_timeout=30)
            # Manage tasks
            # pprint(tasks.list())
            print(response, '\n')
            if response['result'] == "updated":
                print("result: ", response['result'])
                print("Update was a success for ID: ", response['_id'])
                print("New data: ", source_to_update)
            else:
                print("result: ", response['result'])
                print("Response failed: ", response['_shards']['failed'])
        except Exception as err:
            print('Elasticsearch Update API error:', err)




def main():
    es = Elasticsearch(host='localhost', port=9200, timeout=600)
    while True:
        print("""Chose what are you want to do:
        1. Create index
        2. Add data to index
        3. Reindex all indices with wildcard ( !Only for index with documents)
        4. Update all documents with last updated fields
        5. Show all indices
        6. Shaw all documents in index
        7. Delete index
        All else: Exit""")
        operation = int(input(">>> "))
        if operation == 1:
            create_index(es)
        elif operation == 2:
            add_document(es)
        elif operation == 3:
            reindex(es)
        elif operation == 4:
            update_documents(es)
        elif operation == 5:
            find_all_indices(es)
        elif operation == 6:
            index_name = input("Enter index name: ")
            find_all_document(es, index_name)
        elif operation == 7:
            delete_index(es)
        else:
            break



if __name__ == "__main__":
    main()
