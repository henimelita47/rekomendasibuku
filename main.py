from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# =====================
# INIT APP
# =====================
app = FastAPI(title="Sistem Rekomendasi Buku")

# =====================
# CORS
# =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("dataset_buku.csv")

vectorizer = joblib.load("tfidf_vectorizer.pkl")
tfidf_matrix = vectorizer.transform(df["content"].fillna(""))

search_log = Counter()

# =====================
# ROOT HTML
# =====================
@app.get("/", response_class=HTMLResponse)
def home():
    return open("index.html", encoding="utf-8").read()

# =====================
# REQUEST MODEL
# =====================
class RequestRekomendasi(BaseModel):
    query: str
    genre: str
    mood: str

# =====================
# API REKOMENDASI
# =====================
@app.post("/recommend")
def recommend(data: RequestRekomendasi):

    query_text = f"{data.query} {data.genre} {data.mood}"
    query_vec = vectorizer.transform([query_text])

    similarity = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_idx = similarity.argsort()[-5:][::-1]

    hasil = []
    for i in top_idx:
        row = df.iloc[i]
        buku = {
            "judul": row["judul"],
            "pengarang": row["pengarang"],
            "klasifikasi": row["klasifikasi"],
           
        }
        hasil.append(buku)
        search_log[row["judul"]] += 1

    popular = [j for j, _ in search_log.most_common(5)]

    return {
        "recommendations": hasil,
        "popular": popular
    }
