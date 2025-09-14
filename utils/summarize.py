# import os, json, requests

# OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434/api/generate')
# MODEL_NAME = os.environ.get('LLM_MODEL', 'llama3.1:8b-instruct')

# # SYSTEM_PROMPT = (
# #     'You are a concise, accurate meeting scribe. Return STRICT JSON with keys: '
# #     "'key_points' (list of short bullets), 'decisions' (list), 'action_items' (list of objects with owner, task, due_date, priority). '"
# #     'If information is missing, use "unknown" for that field.'
# # )


# # SYSTEM_PROMPT = f"""
# # You are an AI meeting assistant. 
# # Summarize the following transcript into JSON with these exact fields:
# # - key_points: list of strings
# # - decisions: list of strings
# # - action_items: list of objects with fields [owner, task, due_date, priority]

# # Transcript:

# # """


# SYSTEM_PROMPT = """
# You are a precise meeting summarizer. 
# Return ONLY a JSON object, with this exact structure:
# {
#   "key_points": ["point 1", "point 2", ...],
#   "decisions": ["decision 1", "decision 2", ...],
#   "action_items": [
#     {"owner": "name or 'unknown'", "task": "string", "due_date": "YYYY-MM-DD or 'unknown'", "priority": "high/medium/low/unknown"}
#   ]
# }
# If information is missing, fill with "unknown". 
# Do not include any text before or after the JSON.
# """


# def build_prompt(transcript_text, kb_hits):
#     ctx_lines = []
#     for i, hit in enumerate(kb_hits, 1):
#         ctx_lines.append(f"[KB#{i} source={hit['source']}]\n{hit['text']}")
#     context = '\n\n'.join(ctx_lines) if ctx_lines else '(no kb)'
#     user = f"CONTEXT:\n{context}\n\nTRANSCRIPT:\n{transcript_text}\n\nReturn strict JSON only."
#     return SYSTEM_PROMPT + '\n\n' + user

# # def generate_summary(transcript_text, kb_hits):
# #     prompt = build_prompt(transcript_text, kb_hits)
# #     data = { 'model': MODEL_NAME, 'prompt': prompt, 'stream': False }
# #     try:
# #         r = requests.post(OLLAMA_URL, json=data, timeout=120)
# #         r.raise_for_status()
# #         text = r.json().get('response', '')
# #     except Exception as e:
# #         # Fallback: return empty structure if Ollama not available
# #         return { 'key_points': [], 'decisions': [], 'action_items': [] }
# #     # Extract JSON from the response if possible
# #     try:
# #         return json.loads(text)
# #     except Exception:
# #         # attempt simple parse: find first { and last }
# #         s = text.find('{'); e = text.rfind('}')
# #         if s!=-1 and e!=-1:
# #             try:
# #                 return json.loads(text[s:e+1])
# #             except Exception:
# #                 pass
# #         return { 'key_points': [], 'decisions': [], 'action_items': [] }


# def generate_summary(transcript_text, kb_hits):
#     prompt = build_prompt(transcript_text, kb_hits)
#     data = { 'model': MODEL_NAME, 'prompt': prompt, 'stream': False }

#     try:
#         r = requests.post(OLLAMA_URL, json=data, timeout=300)
#         r.raise_for_status()
#         response = r.json()
#         text = response.get("response", "").strip()
        
#         print("=== RAW LLM RESPONSE ===")
#         print(text)

#         # Try strict JSON parse first
#         try:
#             return json.loads(text)
#         except json.JSONDecodeError:
#             # Fallback: extract JSON between first { and last }
#             s = text.find("{")
#             e = text.rfind("}")
#             if s != -1 and e != -1:
#                 return json.loads(text[s:e+1])
#     except Exception as e:
#         print("Error in summarizer:", e)

#     # Always return skeleton instead of empty
#     return {
#         "key_points": ["unknown"],
#         "decisions": ["unknown"],
#         "action_items": [{"owner": "unknown", "task": "unknown", "due_date": "unknown", "priority": "unknown"}]
#     }



# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# groq_api_key = os.getenv("GROQ_API_KEY")
# client = Groq(api_key=groq_api_key)

# def summarize_text(  transcript: str, kb_hits=None) -> dict:
#     """
#     Sends transcript to Groq LLM and returns structured summary:
#     key_points, decisions, and action_items.
#     """
#     prompt = f"""
#     You are a meeting assistant. Summarize the following transcript into:

#     1. Key Points (short bullet points)
#     2. Decisions (clear and concise)
#     3. Action Items (with owner, task, due_date, and priority)

#     Transcript:
#     {transcript}

#     Return the result strictly in JSON format like this:
#     {{
#       "key_points": ["point1", "point2"],
#       "decisions": ["decision1", "decision2"],
#       "action_items": [
#         {{"owner": "Alice", "task": "Prepare slides", "due_date": "2025-09-10", "priority": "High"}},
#         {{"owner": "Bob", "task": "Send follow-up email", "due_date": "2025-09-12", "priority": "Medium"}}
#       ]
#     }}
#     """

#     response = client.chat.completions.create(
#         model="llama3-8b-8192",   # or "mixtral-8x7b-32768" if you want longer context
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2
#     )

#     text = response.choices[0].message.content.strip()

#     # Try to parse JSON safely
#     import json
#     try:
#         summary = json.loads(text)
#     except json.JSONDecodeError:
#         summary = {"key_points": [], "decisions": [], "action_items": []}

#     return summary





# import os
# import json
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize Groq client
# groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def summarize_text(transcript: str, kb_hits=None):
#     """
#     Summarize meeting transcript + optional KB context using Groq LLM.
#     Returns dict with key_points, decisions, action_items.
#     """
#     context = ""
#     if kb_hits:
#         context = "\n\nKnowledge Base Context:\n"
#         for h in kb_hits:
#             context += f"- {h['text']}\n"

#     prompt = f"""
# You are an AI meeting assistant.
# Summarize the following meeting transcript into JSON with three sections:
# 1. key_points (list of strings)
# 2. decisions (list of strings)
# 3. action_items (list of objects: owner, task, due_date, priority)

# Transcript:
# {transcript}

# {context}

# Respond ONLY with valid JSON:
# {{
#   "key_points": [...],
#   "decisions": [...],
#   "action_items": [
#     {{"owner": "...", "task": "...", "due_date": "...", "priority": "..."}}
#   ]
# }}
#     """

#     response = groq_client.chat.completions.create(
#         model="openai/gpt-oss-120b",   # fast Groq model
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0,
#         max_tokens=1000,
#     )

#     text = response.choices[0].message.content.strip()

#     try:
#         return json.loads(text)
#     except json.JSONDecodeError:
#         # Fallback if Groq outputs extra text
#         start = text.find("{")
#         end = text.rfind("}")
#         if start != -1 and end != -1:
#             return json.loads(text[start:end+1])
#         return {
#             "key_points": ["Parse error"],
#             "decisions": [],
#             "action_items": []
#         }



# -----------------------------------------------------

# import os
# import json
# import re
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()
# groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def clean_json(text: str) -> str:
#     """
#     Attempt to clean malformed JSON from LLM output.
#     - Extract JSON block between { ... }
#     - Remove trailing commas
#     """
#     start = text.find("{")
#     end = text.rfind("}")
#     if start == -1 or end == -1:
#         return text
#     json_str = text[start:end+1]

#     # Remove trailing commas before } or ]
#     json_str = re.sub(r",\s*([}\]])", r"\1", json_str)

#     return json_str

# def summarize_text(transcript: str, kb_hits=None):
#     context = ""
#     if kb_hits:
#         context = "\n\nKnowledge Base Context:\n"
#         for h in kb_hits:
#             context += f"- {h['text']}\n"

#     prompt = f"""
# You are an AI meeting assistant.
# Summarize the following meeting transcript into JSON with three sections:
# 1. key_points (list of strings)
# 2. decisions (list of strings)
# 3. action_items (list of objects: owner, task, due_date, priority)

# Transcript:
# {transcript}

# {context}

# Respond ONLY with valid JSON:
# {{
#   "key_points": [...],
#   "decisions": [...],
#   "action_items": [
#     {{"owner": "...", "task": "...", "due_date": "...", "priority": "..."}}
#   ]
# }}
#     """

#     response = groq_client.chat.completions.create(
#         model="mixtral-8x7b-32768",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0,
#         max_tokens=1500,
#     )

#     text = response.choices[0].message.content.strip()
#     print("=== RAW LLM RESPONSE ===")
#     print(text)

#     try:
#         return json.loads(text)
#     except Exception:
#         try:
#             cleaned = clean_json(text)
#             return json.loads(cleaned)
#         except Exception as e:
#             print("JSON parse failed:", e)
#             return {
#                 "key_points": ["Parse error"],
#                 "decisions": [],
#                 "action_items": []
#             }
# -----------------------------------------------------




import os, json, re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def clean_json(text: str) -> str:
    start = text.find("{"); end = text.rfind("}")
    if start == -1 or end == -1:
        return text
    json_str = text[start:end+1]
    return re.sub(r",\s*([}\]])", r"\1", json_str)

def chunk_text(text: str, max_words=2000):
    parts, current = [], ""
    for sentence in text.split('. '):
        if len(current.split()) + len(sentence.split()) > max_words:
            parts.append(current.strip())
            current = sentence
        else:
            current += " " + sentence
    if current.strip():
        parts.append(current.strip())
    return parts

def summarize_chunk(chunk: str, hits: list) -> str:
    context = "\n\n".join([hit["text"] for hit in hits])
    prompt = f"""
    Summarize the transcript chunk into JSON:
    {{
      "key_points": [...],
      "decisions": [...],
      "action_items": [...]
    }}
    Transcript Chunk:
    {chunk}

    KB Context:
    {context}
    """
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def summarize_text(transcript: str, hits: list) -> dict:
    chunks = chunk_text(transcript, max_words=2000)
    merged = {"key_points": [], "decisions": [], "action_items": []}

    for chunk in chunks:
        raw = summarize_chunk(chunk, hits)
        try:
            js = json.loads(raw)
        except json.JSONDecodeError:
            cleaned = clean_json(raw)
            js = json.loads(cleaned) if cleaned else {}
        for field in merged:
            merged[field].extend(js.get(field, []))

    return merged
