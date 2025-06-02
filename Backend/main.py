from fastapi import FastAPI
from Backend.routers import user_router, problem_router, assignment_router, judge_router, auth_router
from Backend.database import engine, Base
from Backend.models import user, problem, assignment
from fastapi.middleware.cors import CORSMiddleware

# 初始化数据库（创建所有表）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Online Judge System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者指定具体的域名列表，例如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(problem_router.router, prefix="/problems", tags=["Problems"])
app.include_router(assignment_router.router, prefix="/assignments", tags=["Assignments"])
app.include_router(judge_router.router, prefix="/judge", tags=["Judge"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
