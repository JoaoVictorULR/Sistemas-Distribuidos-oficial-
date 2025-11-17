from fastapi import FastAPI, HTTPException
import httpx
from schemas import ClimaRequest, ClimaResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "6d8a6d06f4344b8f98c152320251711"
URL = "http://api.weatherapi.com/v1/current.json"



@app.post("/clima", response_model=ClimaResponse)
async def obter_clima(dados: ClimaRequest):

    params = {
        "key": API_KEY,
        "q": dados.cidade,
        "lang": "pt"
    }

    async with httpx.AsyncClient() as client:
        resposta = await client.get(URL, params=params)

    if resposta.status_code != 200:
        raise HTTPException(status_code=400, detail="Cidade não encontrada")

    info = resposta.json()

    return ClimaResponse(
        cidade=info["location"]["name"],
        temperatura=info["current"]["temp_c"],
        condicao=info["current"]["condition"]["text"]
    )
