import fastapi
from pydantic import BaseModel
from model import DelayModel 

app = fastapi.FastAPI()

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

class PredictionRequest(BaseModel):
    # Define los campos necesarios para la entrada de datos de predicción
    feature1: float
    feature2: float
    # Agrega más campos según sea necesario

class PredictionResponse(BaseModel):
    prediction: int  # Define el formato de la respuesta de predicción

@app.post("/predict", response_model=PredictionResponse, status_code=200)
async def post_predict(request: PredictionRequest) -> dict:
    # Procesa los datos de entrada y realiza la predicción con tu modelo
    features = [request.feature1, request.feature2]  # Ajusta la extracción de características según tu modelo
    prediction = model.predict(features)  # Reemplaza 'model' por una instancia de tu modelo
    return {"prediction": prediction}

if __name__ == "__main__":
    import uvicorn
    model = DelayModel()  # Crea una instancia de tu modelo
    uvicorn.run(app, host="0.0.0.0", port=8000)
