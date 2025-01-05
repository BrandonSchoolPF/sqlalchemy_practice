from fastapi import FastAPI, Request, Response
from src.insert.insert_routes import insert_router
from src.select.select_route import get_data
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from typing import Dict


app = FastAPI()


app.include_router(insert_router, prefix='/insert')
app.include_router(get_data, prefix='/company')

class AdvancedMiddleware(BaseHTTPMiddleware):
    """_summary_

    Args:
        BaseHTTPMiddleware (_type_): _description_
    """
    def __init__(self, app):
        """_summary_

        Args:
            app (_type_): _description_
        """
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def log_message(self, message: str):
        print(message)
        
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        if current_time - self.rate_limit_records[client_ip] < 1:
            return Response(content='Rate limit exceeded', status_code = 429)

        self.rate_limit_records[client_ip] = current_time
        path = request.url.path
        
        await self.log_message(f'Request to {path}')
        
        if path != '/docs':
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time


            custom_headers = {"X-Process-Time" : str(process_time)}
            for header, value, in custom_headers.items():
                response.headers.append(header, value)
            
            await self.log_message(f"Response for {path} took {process_time} seconds")

            return response
        
        else: 
            return response

app.add_middleware(AdvancedMiddleware)

@app.get('/')
async def main():
    return {"message" : "Hello, World!"}