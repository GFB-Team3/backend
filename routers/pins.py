from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form, File
from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid, os

from database import get_db
from api.models import Pin, Like, Comment
import schemas

router = APIRouter(prefix="/pins", tags=["pins"])

# --- Routes ---
# 핀 생성
@router.post("/", response_model = schemas.PinResponse, status_code = status.HTTP_201_CREATED)
async def create_pin(
    user_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):  
    image_url: str | None = None
    # 이미지 저장 처리
    if image:
        # 확장자 추출
        ext = image.filename.split(".")[-1]
        
        # 파일명 생성
        filename = f"{uuid.uuid4()}.{ext}"

        #src 폴더에 저장
        save_dir = "src"
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        image_url = f"/src/{filename}"

    # DTO 생성  
    pin_data = schemas.PinCreate(
        user_id=user_id,
        title=title,
        content=content,
        image=image_url,
    )

    new_pin = Pin(**pin_data.model_dump())

    db.add(new_pin)
    db.commit()
    db.refresh(new_pin)

    return new_pin
    
# 핀 수정
@router.put("/{pin_id}", response_model = schemas.PinResponse)
async def update_pin(
    pin_id: int,
    user_id: int = Form(...),
    title: str | None = Form(None),
    content: str | None =  Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):  
    # 수정 대상 핀 조회
    pin = db.get(Pin, pin_id)
    if not pin:
        raise HTTPException(status_code=404, detail="Pin not found")
    
    # 이 핀의 주인인지 확인
    if pin.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this pin")
    
   
    if title is not None:
        pin.title = title
    if content is not None:
        pin.content = content
    
    if image:
        ext = image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        save_dir = "src"
        os.makedirs(save_dir, exist_ok=True)

        file_path = os.path.join(save_dir , filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        pin.image = f"/src/{filename}"

    db.commit()
    db.refresh(pin)

    return pin  
    
# 핀 삭제
@router.delete("/{pin_id}")
async def delete_pin(
    pin_id: int,
    payload: schemas.PinDelete,   
    db: Session = Depends(get_db),
):
    pin = db.get(Pin, pin_id)
    if not pin:
        raise HTTPException(status_code=404, detail="Pin not found")

    if pin.user_id != payload.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this pin")

    db.delete(pin)
    db.commit()

    return {"message": "Pin deleted successfully"}


#핀 검색
@router.get("/search", response_model = list[schemas.PinResponse])
async def search_pins(
    search: str,
    db: Session = Depends(get_db)
):
    if not search:
        raise HTTPException(status_code=400, detail="Search keyword is required")
    
    stmt = (
        select(Pin)
        .where(Pin.title.like(f"%{search}%"))
        .order_by(Pin.updated_at.desc())
    )

    pins = db.execute(stmt).scalars().all()
    return pins
    
# 핀 상세보기
@router.get("/{pin_id}", response_model = schemas.PinResponse)
async def get_pin_detail(
    pin_id: int,
    db: Session = Depends(get_db)
):
    pin = db.get(Pin, pin_id)

    if not pin:
        raise HTTPException(status_code=404, detail="Pin not found")
    
    return pin


    
# 전체 핀 조회
@router.get("/", response_model = list[schemas.PinResponse])
async def list_pins(db: Session = Depends(get_db)):
    stmt = select(Pin).order_by(Pin.updated_at.desc())
    pins = db.execute(stmt).scalars().all()
    return pins



# 즐겨찾기 등록
@router.post("/{pin_id}/likes", response_model=schemas.LikeOut)
async def create_like(
    pin_id: int,
    payload: schemas.LikeIn,        
    db: Session = Depends(get_db),
):
    # 핀 존재 여부 확인
    pin = db.get(Pin, pin_id)
    if not pin:
        raise HTTPException(status_code=404, detail="Pin not found")
    
    # 즐겨찾기 중복 체크
    existing_like = (
        db.query(Like)
        .filter(Like.user_id == user_id, Like.pin_id == pin_id)
        .first()
    )
    if existing_like:
        raise HTTPException(status_code=409, detail="Already liked")

    like_data = schemas.LikeIn(
        user_id=user_id,
        pin_id=pin_id,
    )

    new_like  = Like(**like_data.model_dump())

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return new_like
    

# 댓글 등록
@router.post("/{pin_id}/comments", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    pin_id: int,
    payload: schemas.CommentCreate,   
    db: Session = Depends(get_db),
):
    pin = db.get(Pin, pin_id)
    if not pin:
        raise HTTPException(status_code=404, detail="Pin not found")

    new_comment = Comment(
        user_id=payload.user_id,
        pin_id=pin_id,
        content=payload.content,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

# 댓글 불러오기
@router.get("/comments/{comment_id}", response_model=schemas.CommentResponse)
async def get_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment

# 댓글 수정
@router.put("/comments/{comment_id}", response_model=schemas.CommentResponse)
async def update_comment(
    comment_id: int,
    payload: schemas.CommentUpdate,   
    db: Session = Depends(get_db),
):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != payload.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")

    comment.content = payload.content

    db.commit()
    db.refresh(comment)

    return comment

    

# 댓글 삭제
@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    payload: schemas.CommentDelete,  
    db: Session = Depends(get_db),
):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != payload.user_id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}