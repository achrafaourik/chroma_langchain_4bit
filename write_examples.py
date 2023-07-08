from utils.functions import *
from dotenv import load_dotenv; load_dotenv()
import re
from glob import glob

def extract_dialogues(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    # Use regex to find User and Airi dialogues
    pattern = re.compile(r'User: (.*?)\nAiri: (.*?)\n')
    matches = pattern.findall(data)

    # Combine User and Airi dialogues, with a newline after the 'User' turn
    dialogues = ['User: ' + m[0] + '\nAiri: ' + m[1] for m in matches]

    return dialogues

client = get_chroma_client()
instructor_ef = InstructorEmbeddings().get_embedding_function()
collection = client.get_or_create_collection(name="examples",
                                             embedding_function=instructor_ef)
collection.delete()
collection.get()

text_files = glob('./utils/examples/*.txt')
list_examples = []

for text_file in text_files:
    list_examples.extend(extract_dialogues(text_file))

collection.add(
        documents=list_examples,
        ids=[generate_unique_id() for _ in range(len(list_examples))])
