import faiss
import numpy as np

def create_new_faiss_index(representative_embeddings, metadata_dict, docstore):
    embedding_dimension = list(representative_embeddings.values())[0].shape[0]
    new_index = faiss.IndexFlatL2(embedding_dimension)
    new_metadata = {}

    embeddings_matrix = []
    for column_value, embedding in representative_embeddings.items():
        embeddings_matrix.append(embedding)
        correct_uuid = find_correct_uuid(metadata_dict, docstore, column_value)
        if correct_uuid:
            new_metadata[column_value] = {
                'id': column_value,
                'name': docstore._dict[correct_uuid].metadata.get('name'),
                'year': docstore._dict[correct_uuid].metadata.get('year')
            }

    new_index.add(np.array(embeddings_matrix))
    return new_index, new_metadata

def find_correct_uuid(metadata_dict, docstore, column_value):
    for key, uuid in metadata_dict.items():
        document = docstore._dict.get(uuid)
        if document and document.metadata.get('id') == column_value:
            return uuid
    return None
