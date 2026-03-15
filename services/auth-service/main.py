import os
import json
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    secret_key: str = os.getenv("SECRET_KEY", "super-secret-session-key")
    # OIDC Config
    oidc_client_id: str = os.getenv("OIDC_CLIENT_ID", "mock-client-id")
    oidc_client_secret: str = os.getenv("OIDC_CLIENT_SECRET", "mock-client-secret")
    oidc_issuer: str = os.getenv("OIDC_ISSUER", "https://accounts.google.com")
    
settings = Settings()

app = FastAPI(title="Auth Service", description="Handles OIDC Authentication")

# Required for authlib to store state during OAuth flow
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

oauth = OAuth()
oauth.register(
    name='oidc',
    server_metadata_url=f'{settings.oidc_issuer}/.well-known/openid-configuration',
    client_id=settings.oidc_client_id,
    client_secret=settings.oidc_client_secret,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.get("/auth/login", tags=["Auth"], summary="Initiate OIDC Login sequence", description="Constructs the Oauth URL to redirect the user to provider.")
async def login(request: Request):
    # Determine callback URL based on the request
    # In a real environment, this might need to use host headers or be hardcoded to an ingress
    redirect_uri = request.url_for('auth_callback')
    # Use https if not localhost (for production)
    if not "localhost" in str(redirect_uri) and not "127.0.0.1" in str(redirect_uri):
         redirect_uri = str(redirect_uri).replace("http://", "https://")
    return await oauth.oidc.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback", tags=["Auth"], summary="OIDC callback endpoint", description="Verifies the code from OIDC provider and sets login state/token.")
async def auth_callback(request: Request):
    try:
        # If we reach here in mock mode (no real provider), we can mock a token
        if settings.oidc_client_id == "mock-client-id":
            token = {
                "access_token": "mock_access_token",
                "id_token": "mock_id_token",
                "userinfo": {"email": "admin@example.com", "name": "Admin User"}
            }
        else:
            token = await oauth.oidc.authorize_access_token(request)
        
        # Parse the user info
        user = token.get('userinfo')
        if not user:
             user = await oauth.oidc.parse_id_token(request, token)
        
        # We redirect back to frontend with the token (e.g., as a URL fragment or query param)
        # Note: In production you might want to exchange this for your own JWT or set an HttpOnly cookie
        redirect_url = f"{settings.frontend_url}/auth/callback?token={token.get('id_token', token.get('access_token'))}"
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        print(f"Auth error: {e}")
        # Redirect to a generic error or handle explicitly
        redirect_url = f"{settings.frontend_url}/login?error=auth_failed"
        return RedirectResponse(url=redirect_url)

@app.get("/auth/user", tags=["Auth"], summary="Fetch current user", description="Gets the user information from current session")
async def get_user(request: Request):
    user = request.session.get('user')
    if user:
        return user
    raise HTTPException(status_code=401, detail="Not authenticated")

@app.get("/auth/logout", tags=["Auth"], summary="Logout", description="Clears user session and redirects to frontend")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url=settings.frontend_url)
