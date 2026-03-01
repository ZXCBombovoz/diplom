from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Course
from app.core.auth import get_current_user

router = APIRouter(prefix="/a01", tags=["A01 Broken Access Control"])


@router.get("/courses/{course_id}")
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        return {"error": "Not found"}

    return {
        "id": course.id,
        "title": course.title,
        "owner_id": course.owner_id,
        "secret_flag": course.secret_flag
    }