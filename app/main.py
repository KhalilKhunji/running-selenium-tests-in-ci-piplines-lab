from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, constr
from pathlib import Path

app = FastAPI()

# Define the static directory path
STATIC_DIR = Path(__file__).resolve().parent / "static"

# Serve files from the "static" folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Model for validating form input
class SignupForm(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr


@app.get("/signup", response_class=HTMLResponse)
def get_signup_form():
    html_path = STATIC_DIR / "newsletter_signup.html"
    return html_path.read_text()


@app.post("/signup")
def post_signup(
    name: str = Form(...),
    email: str = Form(...)
):
    form = SignupForm(name=name, email=email)
    return {"message": f"Thanks for subscribing, {form.name}!"}
