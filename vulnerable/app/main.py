from fastapi import FastAPI
from app.db.session import Base, engine, SessionLocal
from app.db.models import Course
from app.tasks.a01_idor.router import router as a01_router
from app.core.routes_auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    if db.query(Course).count() == 0:
        db.add_all([
            Course(id=1, title="Public Course", owner_id=1, secret_flag=None),
            Course(id=2, title="Private Course", owner_id=2, secret_flag="FLAG{IDOR_SUCCESS}")
        ])
        db.commit()
    db.close()

seed_data()

app.include_router(a01_router)
app.include_router(auth_router)