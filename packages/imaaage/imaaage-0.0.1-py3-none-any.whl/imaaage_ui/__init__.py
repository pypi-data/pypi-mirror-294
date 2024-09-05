import uvicorn
import gradio as gr
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.imaaage.log import temp_outputs_path
from src.imaaage_ui.webui import gradio_root

app = FastAPI()

app.mount("/history", StaticFiles(directory=temp_outputs_path), name="history")
app = gr.mount_gradio_app(app, gradio_root, path="/")

uvicorn.run(app, host="0.0.0.0", port=8010)
