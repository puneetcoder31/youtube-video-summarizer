from youtube_transcript_api import YouTubeTranscriptApi
import re
from transformers import pipeline

# Ask user for YouTube link
url = input("Paste YouTube link:  ")

# Extract video ID using regex
match = re.search(r"(?:i=|be/)([a-zA-Z0-9_-]{11})", url)
if not match:
    print("❌ Invalid YouTube URL")
    exit()
video_id = match.group(1)

# Fetch transcript
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_text = " ".join([line["text"] for line in transcript])
    print("\n✅ Transcript fetched successfully.\n")
except Exception as e:
    print("❌ Error fetching transcript:", e)
    exit()

# Use Hugging Face transformer model for summarization
print("🔁 Summarizing using Hugging Face model...\n")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Limit long text to chunks (max 1024 tokens)
chunks = [full_text[i:i+1000] for i in range(0, len(full_text), 1000)]
summary = ""

for chunk in chunks:
    result = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
    summary += result[0]['summary_text'] + " "

# Show result
print("\n🎯 Final Summary:\n")
print(summary.strip())
