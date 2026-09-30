from fastapi import FastAPI

app = FastAPI(title="RainCast Inference")


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {"status": "ok", "modelLoaded": False}
