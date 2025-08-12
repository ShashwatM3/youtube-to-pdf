# YouTube Transcript to PDF Converter

A powerful AI-powered tool that automatically converts YouTube video transcripts into well-formatted, professional PDF documents. Perfect for content creators, researchers, students, and anyone who wants to escape tutorial hell, get a portable version of videos, or make their content creation workflows wayy simpler.

## 🚀 What This Tool Does

This tool transforms YouTube videos into readable PDF documents by:

1. **Extracting Transcripts**: Automatically retrieves the full transcript from any YouTube video
2. **AI-Powered Processing**: Uses GPT-4o to intelligently sectionize and refine the transcript content
3. **Smart Content Organization**: Breaks down long transcripts into logical, well-structured sections
4. **Professional Formatting**: Converts raw transcript text into clean, readable markdown with proper headings
5. **PDF Generation**: Creates high-quality PDF documents ready for reading, sharing, or printing

## ✨ Why You Should Use This Tool

### For Content Creators
- **Content Repurposing**: Turn your YouTube videos into blog posts, articles, or documentation
- **Accessibility**: Make your content accessible to people who prefer reading over watching
- **SEO Benefits**: Extract text content for better search engine optimization

### For Researchers & Students
- **Study Materials**: Convert educational videos into study guides and reference materials
- **Note-Taking**: Get clean, organized text instead of manually transcribing
- **Research Analysis**: Easily search and analyze video content in text format

### For Professionals
- **Meeting Documentation**: Convert recorded presentations into shareable documents
- **Training Materials**: Transform video tutorials into reference guides
- **Compliance**: Create written records of video content for legal or regulatory purposes

### For General Users
- **Reading Instead of Watching**: Enjoy content at your own pace
- **Offline Access**: Download PDFs for offline reading
- **Content Sharing**: Easily share video content in document format

## 🏗️ How It Works

The tool uses a sophisticated pipeline:

1. **Transcript Extraction**: Fetches the complete transcript from YouTube using the video ID
2. **Content Splitting**: Intelligently divides long transcripts into manageable chunks
3. **AI Processing**: Each chunk is processed by a specialized AI agent that:
   - Identifies logical sections
   - Refines grammar and clarity
   - Maintains the original meaning and intent
4. **Content Aggregation**: Combines all processed chunks into a cohesive document
5. **Markdown Conversion**: Transforms the structured content into clean markdown format
6. **PDF Generation**: Converts the final markdown into a professional PDF document

## 🛠️ Features

- **Smart Content Splitting**: Automatically handles transcripts of any length
- **AI-Powered Sectioning**: Intelligent content organization based on context
- **Grammar Refinement**: Improves readability while preserving original meaning
- **Professional Output**: Clean, structured PDFs with proper formatting
- **Batch Processing**: Handles multiple transcript parts efficiently
- **Memory Optimization**: Processes large transcripts without memory issues
- **Error Handling**: Robust fallback mechanisms for reliable operation

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (for GPT-4o access)
- YouTube transcript access (the tool handles this automatically)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ShashwatM3/youtube-to-pdf.git
cd PDFYOUTUBE
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
# Edit .env with your actual API keys
OPENAI_API_KEY=your_openai_api_key_here
YOUTUBE_TRANSCRIPT_API_TOKEN=your_youtube_transcript_api_token_here
```

**Required Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4o access
- `YOUTUBE_TRANSCRIPT_API_TOKEN`: Your YouTube Transcript API token

**How to get the YouTube Transcript API token:**
1. Visit [youtube-transcript.io](https://www.youtube-transcript.io/api)
2. Sign up for an account
3. Get your API token from the dashboard

## 🎯 Usage

### Quick Start
1. Ensure your `.env` file is properly configured with both API keys
2. Run the Streamlit application:
   ```bash
   streamlit run orchestration.py
   ```

2. Open your browser and navigate to the provided URL

3. Enter a YouTube video URL

4. Click "Generate PDF" and wait for processing

5. Download your generated PDF

### Command Line Usage
You can also use the tool programmatically:
```python
from orchestration import run_pipeline
import asyncio

# Run the pipeline with a YouTube video ID
asyncio.run(run_pipeline("VIDEO_ID_HERE"))
```

## 🔍 How the AI Agents Work

### TranscriptAgent
- **Purpose**: Processes raw transcript chunks into structured JSON
- **Function**: Identifies logical sections, refines grammar, maintains coherence
- **Output**: JSON object with section titles and refined content

### FormatterAgent
- **Purpose**: Converts structured JSON into readable markdown
- **Function**: Creates professional formatting, proper headings, clean structure
- **Output**: Well-formatted markdown ready for PDF conversion

## 🚨 Troubleshooting

### Common Issues

1. **Context Length Exceeded**
   - The tool automatically handles this by splitting content
   - If issues persist, reduce the chunk size in the splitting functions

2. **PDF Generation Fails**
   - Check that all dependencies are properly installed
   - Ensure the markdown content is valid

3. **Transcript Extraction Fails**
   - Verify the YouTube video has available transcripts
   - Check your internet connection

### Debug Mode
Enable detailed logging by modifying the agent instructions or adding print statements in the pipeline functions.

## 🤝 Contributing

Contributions are welcome! Here are some areas where you can help:

- **Performance Optimization**: Improve the transcript processing pipeline
- **UI Enhancements**: Better Streamlit interface and user experience
- **Additional Formats**: Support for other output formats (Word, HTML, etc.)
- **Language Support**: Multi-language transcript processing
- **Testing**: Add comprehensive test coverage

## 🙏 Acknowledgments

- Built with OpenAI's GPT-4o model
- Uses the YouTube Transcript API for automatic content extraction
- Powered by Streamlit for the web interface
- Leverages markdown-pdf for PDF generation

---

**Happy converting!**