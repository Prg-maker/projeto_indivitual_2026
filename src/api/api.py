from fastapi import FastAPI
from src.ingeston.monitor import MRVMonitor
app = FastAPI()



@app.get("/api/processar/{ano}")
def processar(ano:int):
    monitor = MRVMonitor(
        ano=ano
    )
    monitor.executar()
    
