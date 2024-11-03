## Backend folder

The backend uses the `core` folder for executing core functionality, some core function examples:  
- Running forward pass on TTS model  
- Using text processors to pre-processes text before passing it to TTS model  
- Parsing text from documents  

Using an ASGI (e,g, Hypercorn, Uvicorn) framework alongside FastAPI or extension of Django, the backend interacts with the frontend through *REST API requests*. The backend should process requests from clients and returns useful responses based on the request.

