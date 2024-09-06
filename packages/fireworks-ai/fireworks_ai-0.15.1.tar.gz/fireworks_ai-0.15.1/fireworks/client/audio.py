from typing import List, Optional, Union

from .audio_api import (
    TranscriptionRequest,
    TranslationRequest,
    TranscriptionResponse,
    TimestampGranularity,
    TranscriptionVerboseResponse,
)
from .api_client import FireworksClient

import httpx
import os
import asyncio


class AudioInference(FireworksClient):
    """
    Main client class for the Fireworks Audio Generation APIs.
    """

    def __init__(
        self,
        model: str = "whisper-v3",
        vad_model: str = "silero",
        alignment_model: str = "mms_fa",
        request_timeout=600,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(request_timeout, api_key=api_key, base_url=base_url, **kwargs)
        self.model = model
        self.vad_model = vad_model
        self.alignment_model = alignment_model

    @staticmethod
    def _audio_to_bytes(audio: Union[str, os.PathLike, bytes]) -> bytes:
        # Normalize all forms of `audio` into a `bytes` object
        if isinstance(audio, (str, os.PathLike)):
            with open(audio, "rb") as f:
                audio = f.read()
        return audio

    def transcribe(
        self,
        audio: Union[str, os.PathLike, bytes],
        model: str = None,
        vad_model: str = None,
        alignment_model: str = None,
        prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        temperature: Optional[float] = None,
        language: Optional[str] = None,
        timestamp_granularities: List[TimestampGranularity] = None,
    ) -> TranscriptionResponse:
        """
        Transcribe an audio into text using ASR (audio speech recognition).
        See the OpenAPI spec (https://docs.fireworks.ai/api-reference/audio-transcriptions)
        for the most up-to-date description of the supported parameters

        Parameters:
        - audio (Union[str, os.PathLike, bytes]): An audio to transcribe.
        - model (str, optional): The ASR model name to call. If not present, defaults to `self.model` on the AudioInference object.
        - vad_model (str, optional): The VAD model name to call. If not present, defaults to `self.vad_model` on the AudioInference object.
        - alignment_model (str, optional): The alignment model name to call. If not present, defaults to `self.alignment_model` on the AudioInference object.
        - prompt (str, optional): The input prompt with which to prime transcription. This can be used, for example, to continue a prior transcription given new audio data.
        - response_format (str): The format in which to return the response. Can be one of "json", "text", "srt", "verbose_json", or "vtt". If not present, defaults to "json".
        - temperature (str): Sampling temperature to use when decoding text tokens during transcription. If not present, defaults to "0.0".
        - language (str, optional): The target language for transcription. The set of supported target languages can be found at https://tinyurl.com/bdz3y63b.
        - timestamp_granularities (List[TimestampGranularity]): The timestamp granularities to populate for this transcription. `response_format` must be set "verbose_json" to use timestamp granularities. Either or both of these options are supported: "word", or "segment". If not present, defaults to "segment".

        Returns:
        TranscriptionResponse: An object with transcription.

        Raises:
        RuntimeError: If there is an error in the audio transcription process.
        """
        return asyncio.run(
            self.transcribe_async(
                audio,
                model,
                vad_model,
                alignment_model,
                prompt,
                response_format,
                temperature,
                language,
                timestamp_granularities,
            )
        )

    async def transcribe_async(
        self,
        audio: Union[str, os.PathLike, bytes],
        model: str = None,
        vad_model: str = None,
        alignment_model: str = None,
        prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        temperature: Optional[float] = None,
        language: Optional[str] = None,
        timestamp_granularities: List[TimestampGranularity] = None,
    ) -> Union[TranscriptionResponse, TranscriptionVerboseResponse, str]:
        """
        Transcribe an audio into text using ASR (audio speech recognition).
        See the OpenAPI spec (https://docs.fireworks.ai/api-reference/audio-transcriptions)
        for the most up-to-date description of the supported parameters

        Parameters:
        - audio (Union[str, os.PathLike, bytes]): An audio to transcribe.
        - model (str, optional): The ASR model name to call. If not present, defaults to `self.model` on the AudioInference object.
        - vad_model (str, optional): The VAD model name to call. If not present, defaults to `self.vad_model` on the AudioInference object.
        - alignment_model (str, optional): The alignment model name to call. If not present, defaults to `self.alignment_model` on the AudioInference object.
        - prompt (str, optional): The input prompt with which to prime transcription. This can be used, for example, to continue a prior transcription given new audio data.
        - response_format (str): The format in which to return the response. Can be one of "json", "text", "srt", "verbose_json", or "vtt". If not present, defaults to "json".
        - temperature (str): Sampling temperature to use when decoding text tokens during transcription. If not present, defaults to "0.0".
        - language (str, optional): The target language for transcription. The set of supported target languages can be found at https://tinyurl.com/bdz3y63b.
        - timestamp_granularities (List[TimestampGranularity]): The timestamp granularities to populate for this transcription. `response_format` must be set "verbose_json" to use timestamp granularities. Either or both of these options are supported: "word", or "segment". If not present, defaults to "segment".

        Returns:
        TranscriptionResponse: An object with transcription.

        Raises:
        RuntimeError: If there is an error in the audio transcription process.
        """
        request = TranscriptionRequest(
            model=model or self.model,
            vad_model=vad_model or self.vad_model,
            alignment_model=alignment_model or self.alignment_model,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            language=language,
            timestamp_granularities=timestamp_granularities,
        )
        data = {
            **request.to_multipart(),
        }
        files = {
            "file": self._audio_to_bytes(audio),
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        async with httpx.AsyncClient(
            headers=headers,
            timeout=self.request_timeout,
            **self.client_kwargs,
        ) as client:
            endpoint_base_uri = f"{self.base_url}/v1/audio/transcriptions"
            response = await client.post(endpoint_base_uri, data=data, files=files)
            self._error_handling(response)

            if response_format in [None, "json"]:
                return TranscriptionResponse(**response.json())
            elif response_format == "verbose_json":
                return TranscriptionVerboseResponse(**response.json())
            else:
                return response.text

    def translate(
        self,
        audio: Union[str, os.PathLike, bytes],
        model: str = None,
        vad_model: str = None,
        alignment_model: str = None,
        prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> TranscriptionResponse:
        """
        Translate an audio into english text using ASR (audio speech recognition).
        See the OpenAPI spec (https://docs.fireworks.ai/api-reference/audio-translations)
        for the most up-to-date description of the supported parameters

        Parameters:
        - audio (Union[str, os.PathLike, bytes]): An audio to translate.
        - model (str, optional): The ASR model name to call. If not present, defaults to `self.model` on the AudioInference object.
        - vad_model (str, optional): The VAD model name to call. If not present, defaults to `self.vad_model` on the AudioInference object.
        - alignment_model (str, optional): The alignment model name to call. If not present, defaults to `self.alignment_model` on the AudioInference object.
        - prompt (str, optional): The input prompt with which to prime transcription. This can be used, for example, to continue a prior transcription given new audio data.
        - response_format (str): The format in which to return the response. Can be one of "json", "text", "srt", "verbose_json", or "vtt". If not present, defaults to "json".
        - temperature (str): Sampling temperature to use when decoding text tokens during transcription. If not present, defaults to "0.0".

        Returns:
        TranscriptionResponse: An object with english transcription.

        Raises:
        RuntimeError: If there is an error in the audio transcription process.
        """
        return asyncio.run(
            self.translate_async(
                audio,
                model,
                vad_model,
                alignment_model,
                prompt,
                response_format,
                temperature,
            )
        )

    async def translate_async(
        self,
        audio: Union[str, os.PathLike, bytes],
        model: str = None,
        vad_model: str = None,
        alignment_model: str = None,
        prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        temperature: Optional[float] = None,
        language: Optional[str] = None,
        timestamp_granularities: List[TimestampGranularity] = None,
    ) -> Union[TranscriptionResponse, TranscriptionVerboseResponse, str]:
        """
        Translate an audio into english text using ASR (audio speech recognition).
        See the OpenAPI spec (https://docs.fireworks.ai/api-reference/audio-translations)
        for the most up-to-date description of the supported parameters

        Parameters:
        - audio (Union[str, os.PathLike, bytes]): An audio to translate.
        - model (str, optional): The ASR model name to call. If not present, defaults to `self.model` on the AudioInference object.
        - vad_model (str, optional): The VAD model name to call. If not present, defaults to `self.vad_model` on the AudioInference object.
        - alignment_model (str, optional): The alignment model name to call. If not present, defaults to `self.alignment_model` on the AudioInference object.
        - prompt (str, optional): The input prompt with which to prime transcription. This can be used, for example, to continue a prior transcription given new audio data.
        - response_format (str): The format in which to return the response. Can be one of "json", "text", "srt", "verbose_json", or "vtt". If not present, defaults to "json".
        - temperature (str): Sampling temperature to use when decoding text tokens during transcription. If not present, defaults to "0.0".
        - language (str, optional): The target language for transcription. The set of supported target languages can be found at https://tinyurl.com/bdz3y63b.
        - timestamp_granularities (List[TimestampGranularity]): The timestamp granularities to populate for this transcription. `response_format` must be set "verbose_json" to use timestamp granularities. Either or both of these options are supported: "word", or "segment". If not present, defaults to "segment".

        Returns:
        TranscriptionResponse: An object with english transcription.

        Raises:
        RuntimeError: If there is an error in the audio transcription process.
        """
        request = TranslationRequest(
            model=model or self.model,
            vad_model=vad_model or self.vad_model,
            alignment_model=alignment_model or self.alignment_model,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
        )
        data = {
            **request.to_multipart(),
        }
        files = {
            "file": self._audio_to_bytes(audio),
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        async with httpx.AsyncClient(
            headers=headers,
            timeout=self.request_timeout,
            **self.client_kwargs,
        ) as client:
            endpoint_base_uri = f"{self.base_url}/v1/audio/translations"
            response = await client.post(endpoint_base_uri, data=data, files=files)
            self._error_handling(response)

            if response_format in [None, "json"]:
                return TranscriptionResponse(**response.json())
            elif response_format == "verbose_json":
                return TranscriptionVerboseResponse(**response.json())
            else:
                return response.text
