import streamlit as st
from utils.supabase_client import get_supabase_client
from config import TIER_LIMITS
from datetime import datetime

supabase = get_supabase_client()


def get_current_month() -> str:
    """Returns current month as string e.g. '2026-03'"""
    return datetime.now().strftime("%Y-%m")

def get_usage(user_id: str) -> dict | None:
    """
    Fetch the usage record for this user for the current month.
    Returns the row dict, or None if no record exists yet.
    """
    try:
        response = (
            supabase.table("usage_tracking")
            .select("*")
            .eq("user_id", user_id)
            .eq("month", get_current_month())
            .execute()
        )
        return response.data[0] if response.data else None
    except Exception:
        return None
    
def check_rate_limit(user_id: str, tier: str = "free") -> tuple[bool, int, int]:
    """
    Check if user is allowed to make a generation.

    Returns a tuple of 3 values:
      - allowed (bool): True if they can proceed
      - used (int): how many generations they've used this month
      - limit (int): their monthly limit
    """
    limit = TIER_LIMITS.get(tier, TIER_LIMITS["free"])
    usage = get_usage(user_id)
    used = usage["count"] if usage else 0

    allowed = used < limit
    return allowed, used, limit

def increment_usage(user_id: str, tier: str = "free"):
    """
    Increment the generation count for this user this month.
    Creates the row if it doesn't exist yet (upsert).
    """
    try:
        month = get_current_month()
        usage = get_usage(user_id)

        if usage is None:
            # First generation this month — create row
            supabase.table("usage_tracking").insert({
                "user_id": user_id,
                "month": month,
                "count": 1,
                "tier": tier
            }).execute()
        else:
            # Increment existing row
            supabase.table("usage_tracking").update({
                "count": usage["count"] + 1
            }).eq("user_id", user_id).eq("month", month).execute()

    except Exception as e:
        st.warning(f"Usage tracking error: {e}")