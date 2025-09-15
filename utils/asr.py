# import os
# from faster_whisper import WhisperModel

# # ssdsdsd
# from pydub import AudioSegment

# DEFAULT_MODEL = os.environ.get('WHISPER_MODEL', 'small')

# class Transcriber:
#     def __init__(self, model_size=DEFAULT_MODEL, compute_type='int8', device='cpu'):
#         # device='cpu' or 'cuda' or 'auto'; compute_type='int8' helps on CPU
#         self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

#     def load_audio(self, path):
#         # convert to mono 16k wav for stability
#         audio = AudioSegment.from_file(path)
#         wav_path = path + '.wav'
#         audio = audio.set_frame_rate(16000).set_channels(1)
#         audio.export(wav_path, format='wav')
#         return wav_path
    
#     def split_audio(self, file_path, chunk_ms=30_000):  # 30s chunks
#         audio = AudioSegment.from_file(file_path)
#         return [audio[i:i+chunk_ms] for i in range(0, len(audio), chunk_ms)]


#     # def transcribe(self, path):
#     #     wav = self.load_audio(path)
#     #     segments, info = self.model.transcribe(wav, vad_filter=True)
#     #     segs = []
#     #     text_parts = []
#     #     for s in segments:
#     #         segs.append({'start': s.start, 'end': s.end, 'text': s.text.strip()})
#     #         text_parts.append(s.text.strip())
#     #     return {'language': info.language, 'segments': segs, 'text': ' '.join(text_parts)}
    
#     def transcribe(self, path):
#         chunks = self.split_audio(path)
#         all_text, all_segments = [], []
        
#         for idx, chunk in enumerate(chunks):
#             tmp_path = f"/mount/tmp/chunk_{idx}.wav"
#             chunk.export(tmp_path, format="wav")

#             segments, info = self.model.transcribe(tmp_path, vad_filter=True)
#             for s in segments:
#                 all_segments.append({'start': s.start, 'end': s.end, 'text': s.text.strip()})
#                 all_text.append(s.text.strip())

#             os.remove(tmp_path)

#         return {'language': info.language, 'segments': all_segments, 'text': ' '.join(all_text)}

import os
from faster_whisper import WhisperModel
from pydub import AudioSegment

DEFAULT_MODEL = os.environ.get("WHISPER_MODEL", "small")

class Transcriber:
    def __init__(self, model_size=DEFAULT_MODEL, compute_type="int8", device="cpu"):
        # device: "cpu" (Streamlit Cloud) | "cuda" | "auto"
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def split_audio(self, file_path, chunk_ms=30_000):
        """Split audio into fixed-size chunks (default: 30s)."""
        audio = AudioSegment.from_file(file_path)
        return [audio[i:i+chunk_ms] for i in range(0, len(audio), chunk_ms)]

    def transcribe(self, path, chunk_ms=30_000):
        """Stream transcription chunk by chunk to avoid memory blowup."""
        chunks = self.split_audio(path, chunk_ms)
        all_segments, all_text = [], []
        language = None

        for idx, chunk in enumerate(chunks):
            tmp_path = f"/mount/tmp/chunk_{idx}.wav"
            chunk.export(tmp_path, format="wav")

            segments, info = self.model.transcribe(tmp_path, vad_filter=True)

            if language is None:
                language = info.language

            for s in segments:
                all_segments.append({
                    "start": s.start + (idx * (chunk_ms / 1000)),  # shift timestamps
                    "end": s.end + (idx * (chunk_ms / 1000)),
                    "text": s.text.strip()
                })
                all_text.append(s.text.strip())

            os.remove(tmp_path)  # free disk space

        return {
            "language": language,
            "segments": all_segments,
            "text": " ".join(all_text)
        }
