from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_tasks():
    response = supabase.table("tasks").select("*").order(
        "created_at",
        desc=True
    ).execute()

    return response.data


def add_task(title, description=""):
    supabase.table("tasks").insert(
        {
            "title": title,
            "description": description
        }
    ).execute()


def delete_task(task_id):
    supabase.table("tasks").delete().eq(
        "id",
        task_id
    ).execute()


def update_status(task_id, status):
    supabase.table("tasks").update(
        {
            "status": status
        }
    ).eq(
        "id",
        task_id
    ).execute()