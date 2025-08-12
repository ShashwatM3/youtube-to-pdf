import asyncio
from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace
#Import all required libraries
from rich import *
from pydantic import BaseModel
from rich.panel import Panel
from agents import Agent, Runner, function_tool
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), 'all_agents'))
from all_agents.TranscriptAgent import get_transcript_sections
from all_agents.FormatterAgent import formatting_agent
from all_agents.TranscriptAgent import get_transcript
import json
import streamlit as st
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from markdown_pdf import MarkdownPdf, Section
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()

# Check for required environment variables
required_env_vars = ["OPENAI_API_KEY", "YOUTUBE_TRANSCRIPT_API_TOKEN"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    st.error("Please create a .env file with the required variables.")
    st.stop()

def split_into_3_parts(text):
  length = len(text)
  part_size = length // 3  # integer division

  part1 = text[:part_size]
  part2 = text[part_size:part_size*2]
  part3 = text[part_size*2:]

  return [part1, part2, part3]

def split_into_4_parts(text):
    length = len(text)
    part_size = length // 4

    part1 = text[:part_size]
    part2 = text[part_size:part_size*2]
    part3 = text[part_size*2:part_size*3]
    part4 = text[part_size*3:]

    return [part1, part2, part3, part4]

def split_into_5_parts(text):
    length = len(text)
    part_size = length // 5

    part1 = text[:part_size]
    part2 = text[part_size:part_size*2]
    part3 = text[part_size*2:part_size*3]
    part4 = text[part_size*3:part_size*4]
    part5 = text[part_size*4:]

    return [part1, part2, part3, part4, part5]

def split_into_6_parts(text):
    length = len(text)
    part_size = length // 6

    part1 = text[:part_size]
    part2 = text[part_size:part_size*2]
    part3 = text[part_size*2:part_size*3]
    part4 = text[part_size*3:part_size*4]
    part5 = text[part_size*4:part_size*5]
    part6 = text[part_size*5:]

    return [part1, part2, part3, part4, part5, part6]

def split_into_7_parts(text):
    length = len(text)
    part_size = length // 7

    part1 = text[:part_size]
    part2 = text[part_size:part_size*2]
    part3 = text[part_size*2:part_size*3]
    part4 = text[part_size*3:part_size*4]
    part5 = text[part_size*4:part_size*5]
    part6 = text[part_size*5:part_size*6]
    part7 = text[part_size*6:]

    return [part1, part2, part3, part4, part5, part6, part7]

def markdown_to_pdf_in_memory(md_string):
    pdf = MarkdownPdf(toc_level=0, optimize=True)
    pdf.add_section(Section(md_string))
    pdf_bytes = BytesIO()
    pdf.save(pdf_bytes)
    return pdf_bytes.getvalue()

async def run_pipeline(id):
  resTr = get_transcript(id)
  transcript = resTr[1]
  title = resTr[0]
  st.session_state["generated_pdf_title"] = title
  markdowns = []
  parts_transcript = split_into_4_parts(transcript)
  lengthTranscripts = len(parts_transcript)
  output_placeholder = col2.empty()
  for i in range(lengthTranscripts):
    part = parts_transcript[i]
    sectionized_part = await get_transcript_sections(part)
    sectionized_part = json.loads(sectionized_part)
    sectionized_markdown = await formatting_agent(sectionized_part)
    markdowns.append(sectionized_markdown)
    output_placeholder.write(f"Finished part {i+1} / {lengthTranscripts}")
  for markdown in markdowns:
     st.write(markdown)
  
  joined_markdown = ""
  for i, markdown in enumerate(markdowns):
      if i == 0:
          if not markdown.strip().startswith('# '):
              joined_markdown += f"# {st.session_state.get('generated_pdf_title', 'Document')}\n\n"
          joined_markdown += markdown
      else:
          joined_markdown += "\n\n---\n\n" + markdown
  
  pdf_file = markdown_to_pdf_in_memory(joined_markdown)
  st.session_state["generated_pdf"] = pdf_file
  output_placeholder.success("Markdown Generated!")

def extract_youtube_id(url: str) -> str:
    parsed_url = urlparse(url)
    
    if parsed_url.netloc in ("youtu.be", "www.youtu.be"):
        return parsed_url.path.lstrip("/")
    
    if parsed_url.netloc in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]
    
    return None

col1, col2 = st.columns(2)

def main():
    with col1:
      st.title("YouTube Transcript to PDF")

      video_url_input = st.text_input("Enter YouTube Video URL:")
      video_id = extract_youtube_id(video_url_input)

      if st.button("Generate PDF") and video_id:
          asyncio.run(run_pipeline(video_id))
    with col2:
      st.write("Waiting for markdown to be formed...")
      if "generated_pdf" and "generated_pdf_title" in st.session_state:
        st.download_button(
            label="Download PDF",
            data=st.session_state["generated_pdf"],
            file_name=f"{st.session_state["generated_pdf_title"]}.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
  main()