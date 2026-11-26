"""Stage 3: OCR Fallback with Word Confidence (SPEC §7.2 & agent.md §6.3)."""

import io

from PIL import Image
from pydantic import BaseModel


class OcrResult(BaseModel):
    text: str
    average_confidence: float
    is_low_quality: bool
    word_count: int


def perform_ocr(image_bytes: bytes) -> OcrResult:
    """Performs OCR on image bytes and computes per-word confidence scores."""
    try:
        import pytesseract  # type: ignore[import-untyped]

        image = Image.open(io.BytesIO(image_bytes))
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        words = []
        confidences = []

        n_boxes = len(data["text"])
        for i in range(n_boxes):
            word = data["text"][i].strip()
            conf = float(data["conf"][i])
            if word and conf > 0:
                words.append(word)
                confidences.append(conf)

        if not confidences:
            return OcrResult(
                text="",
                average_confidence=0.0,
                is_low_quality=True,
                word_count=0,
            )

        avg_conf = sum(confidences) / len(confidences)
        is_low_quality = avg_conf < 70.0  # Quality threshold per SPEC §14.3

        return OcrResult(
            text=" ".join(words),
            average_confidence=avg_conf,
            is_low_quality=is_low_quality,
            word_count=len(words),
        )
    except Exception:
        # Fallback if tesseract binary is not installed or image cannot be read
        return OcrResult(
            text="",
            average_confidence=0.0,
            is_low_quality=True,
            word_count=0,
        )
