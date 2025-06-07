from supabase import create_client, Client
from utils.getsecret import get

url: str = get("SUPABASE_URL")
key: str = get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def add_user(username,phone,chat_id):
    response = (supabase.table('telegram_user').insert(
        {'username':username,
        'phone':phone,
        'chat_id':chat_id}
    )).execute()

def add_record(chat_id,query,response):
    try:
      supabase.table('telegram_messages').insert(
        {"chat_id":chat_id,
        "query":query,
        "response":response}
        ).execute()
      return 1
    except Exception as e:
      return 0

def check_user_exhists(chat_id):
  response = supabase.table('telegram_user').select('*').eq('chat_id',chat_id).execute()
  return len(response.data) == 1

def remove_user(chat_id):
  supabase.table('telegram_user').delete().eq('chat_id',chat_id).execute()

