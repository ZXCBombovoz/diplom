from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from app.db.session import engine, Base, get_db, SessionLocal
from app.db.models import Course

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    if db.query(Course).count() == 0:
        db.add_all([
            Course(id=1, title="Public Course", owner_id=1, secret_flag=None),
            Course(id=2, title="Private Course", owner_id=2, secret_flag="FLAG{IDOR_SUCCESS}")
        ])
        db.commit()
    db.close()

seed()


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, user_id: int = Form(...)):
    if user_id not in [1, 2]:
        return RedirectResponse("/login", status_code=302)

    request.session["user_id"] = user_id
    return RedirectResponse("/dashboard", status_code=302)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user_id": request.session["user_id"]}
    )


@app.get("/a01", response_class=HTMLResponse)
def a01_page(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse("a01.html", {"request": request})


@app.post("/a01", response_class=HTMLResponse)
def a01_vulnerable(
    request: Request,
    course_id: int = Form(...),
    db: Session = Depends(get_db)
):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        result = "Course not found"
    else:
        result = f"Title: {course.title}<br>Owner: {course.owner_id}<br>Flag: {course.secret_flag}"

    return templates.TemplateResponse(
        "a01.html",
        {"request": request, "result": result}
    )


@app.get("/a01/secure", response_class=HTMLResponse)
def a01_secure_page(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse("a01_secure.html", {"request": request})


@app.post("/a01/secure", response_class=HTMLResponse)
def a01_secure(
    request: Request,
    course_id: int = Form(...),
    db: Session = Depends(get_db)
):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=302)

    user_id = request.session["user_id"]
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        result = "Course not found"
    elif course.owner_id != user_id:
        result = "Forbidden — access denied"
    else:
        result = f"Title: {course.title}"

    return templates.TemplateResponse(
        "a01_secure.html",
        {"request": request, "result": result}
    )