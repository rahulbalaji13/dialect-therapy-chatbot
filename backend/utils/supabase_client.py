from supabase import create_client, Client
from config import Config

def init_supabase() -> Client:
    if Config.SUPABASE_URL and Config.SUPABASE_KEY:
        return create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    else:
        # Mock client missing settings
        return None

supabase_client = init_supabase()
