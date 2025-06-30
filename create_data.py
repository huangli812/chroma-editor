from chromadb.utils.embedding_functions import EmbeddingFunction,OpenAIEmbeddingFunction
import chromadb
import os
import openai
from pydantic import BaseModel

CHROMA_PERSIST_DIR = "chroma"

openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI client wrapper for Chroma
openai_ef = OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
            )

# Pydantic model for a fact
class Fact(BaseModel):
    id: str
    category: str
    content: str
    score: float = 0.0  # optional, will be used during query result mapping

# Initialize Chroma client and collection
client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
# client = chromadb.EphemeralClient()
collection = client.get_or_create_collection(
    name="facts_collection",
    embedding_function=openai_ef,
    # configuration={"hnsw":{"space":"ip"}}
)

def add_facts_to_collection(facts: list[Fact]):
    documents = [fact.content for fact in facts]
    ids = [str(fact.id) for fact in facts]
    metadatas = [{"category": fact.category} for fact in facts]
    collection.add(documents=documents, metadatas=metadatas, ids=ids)


rules = [
  {
    "chunk": "Yoichi Nap is a villa hotel located in 5 Chome-32 Okawacho, Yoichi, Yoichi District, Hokkaido 046-0004, Japan. [Google Map location](https://maps.app.goo.gl/7HyR1H2obCsQTzZj8) "
  },
  {"chunk": "The villa with 3 bedrooms, 2 living rooms, and 3 bathrooms."},
  {
    "chunk": "It comfortably accommodates 7 people, with a maximum occupancy of 10."
  },
  {
    "chunk": "There are 2 adult bedrooms, each with a king-size bed, and 1 bedroom with 3 full-size beds—ideal for kids but suitable for adults too."
  },
  {
    "chunk": "Amenities include a kitchen, minibar, TV, air conditioning, heating, garden, private parking, EV charging, WiFi-7, hot tub, washing machine, and cribs."
  },
  {
    "chunk": "The villa is smoke-free, child-friendly, and includes a bar."
  },
  {
    "chunk": "Check-in starts at 16:00 and check-out is by 11:00. later check-out may not available now. early check-in may available."
  },
  {
    "chunk": "Breakfast is not provided, but full kitchenware is available for homemade meals using ingredients from local markets."
  },
  {
    "chunk": "Pet policy : Pets are not allowed."
  },
  {
    "chunk": "The property is not wheelchair accessible and has no elevator."
  },
  {
    "chunk": "Free private parking is available along with EV charging."
  },
  {
    "chunk": "Guests enjoy free high-speed WiFi-7 internet."
  },
  {
    "chunk": "Nearby attractions include Hamanaka Moire Beach (19-minute walk), Otaru Station (12 miles), and Otaru Canal Park (12 miles)."
  },
  {
    "chunk": "Other notable locations nearby are Otarushi Zenibako City Center (22 miles) and Okadama Airport (35 miles)."
  },
  {
    "chunk": "The license number for the property is 後保生第187号令."
  },
  {
    "chunk": "The minimum stay is 1 night."
  },
  {
    "chunk": "Cancellation is free, but guests should confirm details before booking."
  },
  {
    "chunk": "Yoichi Nap is family-friendly and provides accommodations and amenities suitable for children."
  },{"chunk": "Hotel Website: https://yoichi-nap.com/"}
]
from typing import List
import uuid
x:List[Fact] = []
for r in rules:
    x.append(Fact(id=str(uuid.uuid4()),category="Rule",content=r["chunk"]))
add_facts_to_collection(x)