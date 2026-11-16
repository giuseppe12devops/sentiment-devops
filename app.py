import pickle
import time

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

# Carico il modello una sola volta
with open("sentiment_analysis_model.pkl", "rb") as file:
    model = pickle.load(file)

# Metriche usate da Prometheus
request_time = Histogram("http_request_duration_seconds", "Tempo delle richieste a predict")
prediction_errors = Counter("prediction_errors_total", "Errori durante le previsioni")
prediction_total = Counter("prediction_total", "Previsioni eseguite", ["sentiment"])


class Review(BaseModel):
    review: str


@app.middleware("http")
async def measure_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)

    if request.url.path == "/predict":
        request_time.observe(time.time() - start)

    return response


@app.post("/predict")
def predict(data: Review):
    # Controllo che il testo non sia vuoto
    if not data.review.strip():
        raise HTTPException(status_code=400, detail="Inserisci una recensione")

    try:
        # Chiedo al modello il sentiment e la probabilità
        sentiment = str(model.predict([data.review])[0])
        confidence = float(max(model.predict_proba([data.review])[0]))
        prediction_total.labels(sentiment=sentiment).inc()
        return {"sentiment": sentiment, "confidence": round(confidence, 4)}
    except Exception:
        prediction_errors.inc()
        raise HTTPException(status_code=500, detail="Errore durante la previsione")


@app.get("/metrics")
def metrics():
    # Prometheus legge le metriche da questo indirizzo
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
