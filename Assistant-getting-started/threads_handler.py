def get_thread(client, thread_id):
    print("Getting thread with id: " + thread_id)
    thread = client.beta.threads.retrieve(thread_id)
    print(thread)
    return thread

def get_thread_messages(client, thread_id):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    return messages


