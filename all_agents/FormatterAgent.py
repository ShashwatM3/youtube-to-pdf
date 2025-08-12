import requests
from agents import Agent, Runner, function_tool, trace
import re
import markdown
from markdown_pdf import MarkdownPdf, Section
import json
from pydantic import BaseModel
from io import BytesIO
import streamlit as st

pdf = MarkdownPdf(toc_level=2, optimize=True)

class MarkdownToPdfParams(BaseModel):
  md_string: str

def markdown_to_pdf_in_memory(md_string):
    try:
        pdf = MarkdownPdf(toc_level=2, optimize=True)
        pdf.add_section(Section(md_string))
        
        # Instead of saving to disk, save to a BytesIO object in memory
        pdf_bytes = BytesIO()
        pdf.save(pdf_bytes)
        pdf_bytes.seek(0)  # Rewind to the start so it can be read
        
        print(f"PDF object created, BytesIO size: {pdf_bytes.getbuffer().nbytes} bytes")
        return pdf_bytes
    except Exception as e:
        print(f"Error in markdown_to_pdf_in_memory: {e}")
        raise e

@function_tool
def markdown_to_pdf(params: MarkdownToPdfParams):
  """
  This function takes in a variable that contains markdown format of content in a string
  and then converts it into a readable PDF for the user
  """
  try:
    md_string = params.md_string
    print(f"Converting markdown to PDF, length: {len(md_string)} chars")
    
    pdf_file = markdown_to_pdf_in_memory(md_string)
    pdf_bytes = pdf_file.getvalue()
    
    print(f"PDF generated successfully, size: {len(pdf_bytes)} bytes")
    return pdf_bytes
  except Exception as e:
    print(f"Error in markdown_to_pdf: {e}")
    # Return a simple error message as bytes
    return f"PDF generation failed: {str(e)}".encode('utf-8')

transcript_agent = Agent(
    name="Formatter Agent",
    # instructions="Convert JSON transcript to Markdown, then call markdown_to_pdf tool. Output: PDF bytes.",
    instructions="Convert the entire JSON formatted provided transcript to a Markdown format representative of all the information and return it back to us. Use each key of the JSON as the title. Do not include any words like Transcript Summary, Transcript Markdown Format, or any word with Transcript. just stick with the keys as the section headers",
    model="gpt-4o",
)

async def formatting_agent(sectionized_transcript):
  formatted_input = json.dumps(sectionized_transcript, indent=2)
  st.write(f"Running formatting agent with input: {len(formatted_input)} chars")
  
  result = await Runner.run(transcript_agent,[
    {"role": "user", "content": formatted_input}
  ])

  if hasattr(result, 'final_output'):
    return result.final_output
  else:
    return str(result)
  
  # print(f"Agent result type: {type(result)}")
  # print(f"Agent result attributes: {dir(result)}")
  
  # # Try to get the tool result first
  # if hasattr(result, 'tool_results') and result.tool_results:
  #   print(f"Found tool_results: {len(result.tool_results)} items")
  #   tool_result = result.tool_results[0]
  #   print(f"Tool result type: {type(tool_result)}, length: {len(tool_result) if hasattr(tool_result, '__len__') else 'N/A'}")
  #   return tool_result
  # elif hasattr(result, 'final_output'):
  #   print(f"Found final_output: {len(result.final_output)} chars")
  #   # If no tool was called, the agent might have returned the markdown
  #   # We need to convert it to PDF ourselves
  #   markdown_content = result.final_output
  #   return markdown_to_pdf(MarkdownToPdfParams(md_string=markdown_content))
  # else:
  #   print("No tool_results or final_output found")
  #   # Fallback: try to access the result directly
  #   return result