from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello", "world": "!"}


@app.get("/name/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/calculate/{number}")
def calculate_square(number: float):
    result = number ** 2
    return {"number": number, "square": result}
