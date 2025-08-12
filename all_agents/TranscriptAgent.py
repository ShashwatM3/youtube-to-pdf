import requests
from agents import Agent, Runner, trace
import re
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API token from environment variable
apitoken = os.getenv("YOUTUBE_TRANSCRIPT_API_TOKEN")
if not apitoken:
    raise ValueError("YOUTUBE_TRANSCRIPT_API_TOKEN environment variable is required")

transcript_agent = Agent(
    name="Transcript Summarizer Agent",
    instructions=(
    """"
    You are a transcript summarizing assistant receiving only a chunk of a YouTube video transcript.

    Your task:
    1. Summarize and sectionize this chunk alone; do not assume other parts.
    2. Output a single valid JSON object with:
      - Keys as short, meaningful section titles taken from the content (never generic labels like “Transcript Overview” or “Transcript Summary” or anything to do with the word "Transcript" unless they appear in the text as actual headings)
      - Values as refined transcript text for those sections
    3. Correct grammar and phrasing for clarity in this chunk.
    4. Output only valid JSON, with:
      - Double quotes for all keys and values
      - No trailing commas
      - No extra text, headers, markdown, or explanations
      - Fully parseable by Python’s json.loads()

    Example output:
    {
      "Section 1": "Refined content here...",
      "Section 2": "Refined content here..."
    }

    Follow these rules strictly. Do not summarize beyond refining; only improve readability and coherence for knowledge gain.
    """
    ),
    model="gpt-4o",
)

def clean_code_fences(s: str):
    return re.sub(r"^```(?:json)?\n?|\n?```$", "", s.strip())

def get_transcript(id):
  response = requests.post(
  "https://www.youtube-transcript.io/api/transcripts",
    headers={
      "Authorization": f"Basic {apitoken}",
      "Content-Type": "application/json"
    },
    json={"ids": [id]}
  )

  transcript = []

  if response.status_code == 200:
      data = response.json()
      for dataItem in data:
        for i in dataItem["tracks"]:
          for transcript_segment in i["transcript"]:
              transcript.append(transcript_segment['text'])

      joined_text = " ".join(transcript)
      return [dataItem["title"], joined_text]
  else:
      return(f"Request failed with status code: {response.status_code}")

async def get_transcript_sections(part):
  with trace("Sectionizing the transcript!"):
    result = await Runner.run(transcript_agent, part)
    return clean_code_fences(result.final_output) # This returns the FINAL JSON which is STILL STRINGIFIED

# async def get_transcript_sections(id):
#   transcript_video = get_transcript(id)
#   parts = split_into_three_parts(transcript_video)
#   final_obj = {}

#   for part in parts:
#     with trace("Sectionizing the transcript!"):
#       result = await Runner.run(transcript_agent, part)
#       result = json.loads(clean_code_fences(result.final_output))
#       final_obj.update(result)
  
#   return final_obj