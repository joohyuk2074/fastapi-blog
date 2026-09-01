from fastapi import FastAPI

# Spring의 @SpringBootApplication + DispatcherServlet에 해당하는 ASGI 애플리케이션 객체.
# uvicorn/fastapi CLI가 "main:app" 형태로 이 변수를 찾아서 실행한다.
app = FastAPI()
