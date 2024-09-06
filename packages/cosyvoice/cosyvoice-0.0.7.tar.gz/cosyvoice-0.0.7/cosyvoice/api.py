import json
import os
from cosyvoice.utils.file_utils import load_wav
from modelscope import snapshot_download
from loguru import logger
import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice
import torch
from huggingface_hub import snapshot_download as hf_snapshot_download


class CosyVoiceTTS:

    def __init__(
        self,
        model_cache_dir="checkpoints/cosyvoice",
        device="cuda",
        model_type="instruct",
    ) -> None:
        if not os.path.exists(model_cache_dir):
            logger.info(f"downloading cosyvoice from modelscope.")
            snapshot_download(
                "iic/CosyVoice-300M", local_dir=f"{model_cache_dir}/CosyVoice-300M"
            )
            snapshot_download(
                "iic/CosyVoice-300M-SFT",
                local_dir=f"{model_cache_dir}/CosyVoice-300M-SFT",
            )
            snapshot_download(
                "iic/CosyVoice-300M-Instruct",
                local_dir=f"{model_cache_dir}/CosyVoice-300M-Instruct",
            )
            snapshot_download(
                "iic/CosyVoice-ttsfrd", local_dir=f"{model_cache_dir}/CosyVoice-ttsfrd"
            )
            logger.info("cosyvoice model downloaded.")

        self.voice_pk_root = f"{model_cache_dir}/CosyVoice-voice-pkg"
        if not os.path.exists(self.voice_pk_root):
            hf_snapshot_download(
                repo_id="lucasjin/voice-pkg",
                local_dir=f"{model_cache_dir}/CosyVoice-voice-pkg",
            )

        if os.path.exists(os.path.join(self.voice_pk_root, "voices.json")):
            voices = json.load(
                open(os.path.join(self.voice_pk_root, "voices.json"), "r")
            )
            self.voices_map = {
                i["name"]: {"wav": i["wav"], "text": i["text"]} for i in voices
            }
            logger.info(f"loaded voices map: {self.voices_map}")
        else:
            self.voices_map

        self.model_type = model_type
        if self.model_type == "instruct":
            self.model = CosyVoice(
                f"{model_cache_dir}/CosyVoice-300M-Instruct",
                load_jit=torch.cuda.is_available(),
                device=device,
            )
        elif self.model_type == "sft":
            self.model = CosyVoice(
                f"{model_cache_dir}/CosyVoice-300M-SFT",
                load_jit=torch.cuda.is_available(),
                device=device,
            )
        elif self.model_type == "base":
            self.model = CosyVoice(
                f"{model_cache_dir}/CosyVoice-300M",
                load_jit=torch.cuda.is_available(),
                device=device,
            )

    def tts_instruct(
        self,
        text,
        spk_id="中文男",
        prompt="Theo 'Crimson', is a fiery, passionate rebel leader. Fights with fervor for justice, but struggles with impulsiveness.",
        return_format="wav",
        stream=False,
    ):
        if self.model_type == "instruct":
            a = self.model.inference_instruct(
                text,
                # "中文男",
                spk_id,
                prompt,
                stream=stream,
            )
        else:
            a = self.model.inference_sft(
                text,
                spk_id,
                stream=stream,
            )

        if return_format == "wav":
            if stream:
                for itm in a:
                    yield itm["tts_speech"]
            else:
                a = next(a)
                yield a["tts_speech"]
        elif return_format == "bytes":
            if stream:
                for itm in a:
                    yield itm["tts_speech"]
            else:
                a = next(a)
                yield a["tts_speech"]
        elif return_format == "file" and not stream:
            out_f = "out.wav"
            a = next(a)
            torchaudio.save(out_f, a["tts_speech"], 22050)
            yield out_f
        else:
            ValueError(
                f"unsupported combination of stream and return_format: {stream} {return_format}"
            )

    def tts_cross_lan(
        self,
        text,
        prompt_speech_id="jarvis",
        zero_shot=False,
        return_format="wav",
        stream=False,
    ):
        # load the one shot prompt
        if self.voices_map is not None:
            if prompt_speech_id not in self.voices_map:
                prompt_speech_id = "cn_male"

            if "wav_values" in self.voices_map[prompt_speech_id]:
                prompt_speech_16k = self.voices_map[prompt_speech_id]["wav_values"]
            else:
                prompt_speech_16k = load_wav(
                    os.path.join(
                        self.voice_pk_root,
                        self.voices_map[prompt_speech_id]["wav"].replace("data/", ""),
                    ),
                    16000,
                )
                self.voices_map[prompt_speech_id]["wav_values"] = prompt_speech_16k
            prompt_speech_text = self.voices_map[prompt_speech_id]["text"]
            if zero_shot:
                logger.info("start zero-shot cross lingual infer..")
                a = self.model.inference_zero_shot(
                    text,
                    prompt_speech_text,
                    prompt_speech_16k,
                    stream=stream,
                )
            else:
                logger.info("start cross lingual infer..")
                a = self.model.inference_cross_lingual(
                    text,
                    prompt_speech_16k,
                    stream=stream,
                )
        else:
            if self.model_type == "instruct":
                a = self.model.inference_instruct(
                    text,
                    # "中文男",
                    stream=stream,
                )
            else:
                a = self.model.inference_sft(
                    text,
                    stream=stream,
                )

        if return_format == "wav":
            if stream:
                for itm in a:
                    yield itm["tts_speech"]
            else:
                a = next(a)
                yield a["tts_speech"]
        elif return_format == "bytes":
            if stream:
                for itm in a:
                    yield itm["tts_speech"]
            else:
                a = next(a)
                yield a["tts_speech"]
        elif return_format == "file" and not stream:
            out_f = "out.wav"
            a = next(a)
            torchaudio.save(out_f, a["tts_speech"], 22050)
            yield out_f
        else:
            ValueError(
                f"unsupported combination of stream and return_format: {stream} {return_format}"
            )

    def tts_test(self, text):
        a = self.model.inference_instruct(
            text,
            # "中文男",
            "日语男",
            "Theo 'Crimson', is a fiery, passionate rebel leader. Fights with fervor for justice, but struggles with impulsiveness.",
            stream=False,
        )
        out_f = "out.wav"
        a = next(a)
        print(a)
        torchaudio.save(out_f, a["tts_speech"], 22050)
        return out_f
