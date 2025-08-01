from agents import RunContextWrapper, function_tool
from context import UserContext


@function_tool
async def refund_user(wrapper: RunContextWrapper[UserContext]):
    """Issue a refund(premium users only)"""
    if wrapper.context.is_premium_user:
        return f"✅ Issue a refund to {wrapper.context.name}"
    return f"❌ refund are only available for premium users"

@function_tool
async def restart_service(wrapper: RunContextWrapper[UserContext]):
    """Restart services technical issues only"""
    if wrapper.context.issue_type == "Technical":
        return f"🔁 services restarted successfully"
    return "⚠️ Restart not applicable for this issue type."

@function_tool
async def greet_user(wrapper: RunContextWrapper[UserContext]):
    """Generic greeting tool"""
    return f"👋 Hello {wrapper.context.name}. How can i help you today?"

    