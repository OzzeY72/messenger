from .google import GoogleOAuth

PROVIDERS = {
    "google": GoogleOAuth
    # github, facebook ...
}

def get_oauth_provider(auth_provider: str):
    provider_class = PROVIDERS.get(auth_provider.lower())
    if not provider_class:
        raise ValueError(f"Unknown auth provider: {auth_provider}")
    return provider_class()
