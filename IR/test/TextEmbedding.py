from sentence_transformers import SentenceTransformer

class TextEmbedding:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text):
        # Encode the input text
        embedding = self.model.encode([text])
        return embedding[0]

if __name__ == '__main__':
    # Usage
    model_name = 'all-MiniLM-L6-v2'
    embedding = TextEmbedding(model_name)

    # Get the embedding of a text
    text = 'This is a sample sentence.'
    text_embedding = embedding.get_embedding(text)

    # Print the embedding
    print(len(text_embedding))
    print(text_embedding)
    print(type(text_embedding))

