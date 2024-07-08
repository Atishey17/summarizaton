from newspaper import Article
from googletrans import Translator
import nltk
import gradio as gr
import os
from datetime import datetime

nltk.download('punkt')

def translate_and_summarize(url, language):
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        translator = Translator()
        art_title = translator.translate(article.title, dest=language)
        article_sum = translator.translate(article.summary, dest=language)

        output = f"Article Title:\n{art_title.text}\n\n"
        output += f"Article Summary:\n{article_sum.text}\n\n"
        output += f"Article Publish Date:\n{article.publish_date}\n\n"
        output += f"Article Image Link:\n{article.top_image}"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"news_summary_{timestamp}"

        txt_filename = f"{base_filename}.txt"
        with open(txt_filename, "w", encoding="utf-8") as txt_file:
            txt_file.write(output)

        html_filename = f"{base_filename}.html"
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>News Summary</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    padding: 30px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .section-title {{
                    font-weight: bold;
                    color: #2980b9;
                    margin-bottom: 5px;
                }}
                .content {{
                    background-color: #ecf0f1;
                    padding: 10px;
                    border-radius: 4px;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                @media (max-width: 600px) {{
                    body {{
                        padding: 10px;
                    }}
                    .container {{
                        padding: 15px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>News Summary</h1>
                <div class="section">
                    <div class="section-title">Article Title</div>
                    <div class="content">{art_title.text}</div>
                </div>
                <div class="section">
                    <div class="section-title">Article Summary</div>
                    <div class="content">{article_sum.text}</div>
                </div>
                <div class="section">
                    <div class="section-title">Article Publish Date</div>
                    <div class="content">{article.publish_date}</div>
                </div>
                <div class="section">
                    <div class="section-title">Article Image Link</div>
                    <div class="content"><a href="{article.top_image}" target="_blank">{article.top_image}</a></div>
                </div>
            </div>
        </body>
        </html>
        """
        with open(html_filename, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

        return f"Summary saved as {txt_filename} and {html_filename}\n\n{output}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

iface = gr.Interface(
    fn=translate_and_summarize,
    inputs=[
        gr.Textbox(label="URL"),
        gr.Radio(["en", "hi"], label="Language", value="en")
    ],
    outputs="text",
    title="News Article Summary",
    description="Enter a news article URL and select a language to get a translated summary. The summary will be saved as both a text file and an HTML file."
)

iface.launch()