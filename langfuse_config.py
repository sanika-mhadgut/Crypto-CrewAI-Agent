import os
from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://us.cloud.langfuse.com"),
)

# Disable all interactive or CLI prompts
os.environ["LANGFUSE_INTERACTIVE"] = "0"
os.environ["LANGFUSE_NO_PROMPT"] = "true"