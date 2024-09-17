from PIL import Image
from sentence_transformers import SentenceTransformer
import vecs
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

DB_CONNECTION = "postgresql://postgres.hlufptwhzkpkkjztimzo:bASRr8KHbwFhvuqN@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres"

def seed():
    # create vector store client
    vx = vecs.create_client(DB_CONNECTION)

    # create a collection of vectors with 3 dimensions
    images = vx.get_or_create_collection(name="image_vectors", dimension=512)

    # Load CLIP model
    model = SentenceTransformer('clip-ViT-B-32')

    # Encode an image:
    img_emb1 = model.encode(Image.open('./images/84238508_01.png'))
    img_emb2 = model.encode(Image.open('./images/84238508_02.png'))
    img_emb3 = model.encode(Image.open('./images/84238508_03.png'))
    img_emb4 = model.encode(Image.open('./images/84238508_04.png'))

    # add records to the *images* collection
    images.upsert(
        records=[
            (
                "cloud-one.png",        # the vector's identifier
                img_emb1,          # the vector. list or np.array
                {"type": "png"}   # associated  metadata
            ), (
                "cloud-two.png",
                img_emb2,
                {"type": "png"}
            ), (
                "cloud-three.png",
                img_emb3,
                {"type": "png"}
            ), (
                "cloud-four.png",
                img_emb4,
                {"type": "png"}
            )
        ]
    )
    print("Inserted images")

    # index the collection for fast search performance
    images.create_index()
    print("Created index")

def search():
    # create vector store client
    vx = vecs.create_client(DB_CONNECTION)
    images = vx.get_or_create_collection(name="image_vectors", dimension=512)

    # Load CLIP model
    model = SentenceTransformer('clip-ViT-B-32')
    # Encode text query
    query_string = "a white explosion" # because this is what the cloud data looks like :P
    text_emb = model.encode(query_string)

    # query the collection filtering metadata for "type" = "jpg"
    results = images.query(
        data=text_emb,                      # required
        limit=1,                            # number of records to return
        filters={"type": {"$eq": "jpg"}},   # metadata filters
    )
    result = results[0]
    print(result)
    plt.title(result)
    image = mpimg.imread('./images/' + result)
    plt.imshow(image)
    plt.show()