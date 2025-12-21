from fastapi import FastAPI
from app.core.config import settings
from app.routers import project, test_case, execution, auth, admin
from app.core.database import engine, Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(project.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(test_case.router, prefix=f"{settings.API_V1_STR}/test-cases", tags=["test-cases"])
app.include_router(execution.router, prefix=f"{settings.API_V1_STR}/execution", tags=["execution"])

@app.on_event("startup")
async def startup():
    # Create tables (for development only, use Alembic in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to Rio Auto API"}
