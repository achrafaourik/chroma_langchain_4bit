import os
import chromadb
from chromadb.config import Settings
import uuid
from . import instructor_embeddings


def get_chroma_client():
    chroma_client = chromadb.Client(
        Settings(chroma_api_impl="rest",
                 chroma_server_host=os.environ.get('CHROMA_SERVER_HOST', '165.22.84.221'),
                 chroma_server_http_port="8000"))
    return chroma_client

def convert_to_multiline_string(string_variable):
    """
    Converts a regular string to a multiline string.

    Args:
        string_variable (str): The regular string to be converted.

    Returns:
        str: The converted multiline string.
    """
    multiline_string = f"""{string_variable}"""
    return multiline_string


def generate_unique_id():
    return str(uuid.uuid4())

def get_related_history(user_email, current_input):
    """
    Returns the related history of interactions between the given user and the chatbot
    """
    client = get_chroma_client()

    instructor_ef = instructor_embeddings.InstructorEmbeddings().get_embedding_function()

    collection = client.get_or_create_collection(name="user_embeddings", embedding_function=instructor_ef)

    res = collection.query(
        query_texts=[current_input],
        n_results=int(os.environ.get('N_RELATED_INTERACTIONS', 5)),
        where={"email": user_email})

    related_interactions = res['documents'][0]
    related_history ="\n".join(related_interactions)
    print('-' * 60)
    print(f'user input: {current_input}')
    print(f'related history of the client:\n{related_history}')

    return related_history

def write_current_interaction(user_email, current_interaction):
    client = get_chroma_client()
    instructor_ef = instructor_embeddings.InstructorEmbeddings().get_embedding_function()

    collection = client.get_or_create_collection(name="user_embeddings", embedding_function=instructor_ef)

    collection.add(
        documents=[current_interaction],
        metadatas=[{'email': user_email}],
        ids=generate_unique_id())
