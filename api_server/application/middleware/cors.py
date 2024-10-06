from fastapi.middleware.cors import CORSMiddleware
middleware = (
    CORSMiddleware, 
    dict(
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"]
        ), 
    )

