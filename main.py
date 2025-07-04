import os
import uvicorn
from app import app  
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
