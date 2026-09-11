from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """健康检查端点"""
    return {"status": "ok"}
