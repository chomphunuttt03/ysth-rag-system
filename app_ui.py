# from email.mime import message
# import time
# from dotenv import load_dotenv
# load_dotenv()

# import gradio as gr
# from src.ingest import get_embed_model, load_or_build_index
# from src.query import create_query_engine
# from src.app import get_llm

# embed_model = get_embed_model()
# llm = get_llm()

# index = load_or_build_index(embed_model)
# engine = create_query_engine(index, llm)

# def chat_fn(message, history):

#     print(f"[DEBUG] user query: {message}")

#     if not message.strip():
#         return "Please enter a question."
    
#     start = time.time()
#     answer = engine.ask(message)
#     end = time.time()
    
#     return f"{answer}\n\n⏱ {end - start:.2f}s"



# custom_theme = gr.themes.Soft(primary_hue="blue")


# with gr.Blocks(theme=custom_theme) as demo:
#     gr.Markdown("## 🏦 Thai Securities Intelligence System")

#     gr.Markdown(
#         "ระบบผู้ช่วยอัจฉริยะสำหรับค้นหาข้อมูลด้านตลาดทุนและหลักทรัพย์ "
#         "โดยใช้ฐานข้อมูลภายในองค์กร"
#     )

#     gr.ChatInterface(
#         fn=chat_fn,
#         chatbot=gr.Chatbot(height=420),
#         textbox=gr.Textbox(
#             placeholder="พิมพ์คำถามเกี่ยวกับหุ้น, งบการเงิน หรือข้อมูลตลาดทุน..."
#         ),
#         description="สามารถถามข้อมูลเช่น ราคาหุ้น, อัตราส่วนทางการเงิน, และบทวิเคราะห์",
#         examples=[
#             "What is the market cap of Bangkok Bank?",
#             "What is the NPL ratio of KBANK?",
#             "Which stocks have Buy rating above 100 THB?",
#         ],
#     )

# if __name__ == "__main__":
#     demo.launch()

import time
from dotenv import load_dotenv
load_dotenv()

import gradio as gr
from src.ingest import get_embed_model, load_or_build_index
from src.query import create_query_engine
from src.app import get_llm

embed_model = get_embed_model()
llm = get_llm()

index = load_or_build_index(embed_model)
engine = create_query_engine(index, llm)

def chat_fn(message, history):
    
    print(f"[DEBUG] user query: {message}")

    if not message.strip():
        return "Please enter a question."

    start = time.time()

    result = engine.ask(message)

    end = time.time()

    print(f"[DEBUG] response time: {end - start:.2f}s")

    sources_text = "\n".join(result['sources']) if result['sources'] else "No sources found"

    return f"""
🧠 Answer:
{result['answer']}

📚 Sources:
{sources_text}

⏱ Time: {end - start:.2f}s
"""

custom_theme = gr.themes.Soft(primary_hue="blue")


with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown("## 🏦 Thai Securities Intelligence System")

    gr.Markdown(
        "ระบบผู้ช่วยอัจฉริยะสำหรับค้นหาข้อมูลด้านตลาดทุนและหลักทรัพย์ "
        "โดยใช้ฐานข้อมูลภายในองค์กร"
    )

    gr.ChatInterface(
        fn=chat_fn,
        chatbot=gr.Chatbot(height=420),
        textbox=gr.Textbox(
            placeholder="พิมพ์คำถามเกี่ยวกับหุ้น, งบการเงิน หรือข้อมูลตลาดทุน..."
        ),
        description="สามารถถามข้อมูลเช่น ราคาหุ้น, อัตราส่วนทางการเงิน, และบทวิเคราะห์",
        examples=[
            "What is the current recommendation for PTT stock?",
            "Which stocks have a 'Buy' rating with target price above 100 THB?",
            "What is the P/E ratio of Bangkok Bank?",
        ],
    )

if __name__ == "__main__":
    demo.launch()
