from app.api.api_v1.endpoints import analyse
api_router.include_router(analyse.router, tags=["analyse"])
