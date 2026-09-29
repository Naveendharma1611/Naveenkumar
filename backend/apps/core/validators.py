"""Upload validation: extension allow-lists, size caps, and a basic content sniff for images/PDFs."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "avif", "gif", "svg"]
DOCUMENT_EXTENSIONS = ["pdf"]
VIDEO_EXTENSIONS = ["mp4", "webm", "mov"]
MODEL_3D_EXTENSIONS = ["glb", "gltf", "obj"]
CODE_EXTENSIONS = ["py", "ipynb", "sql", "txt", "md", "js", "ts", "c", "cpp", "java", "csv", "json", "zip"]
STUDY_FILE_EXTENSIONS = DOCUMENT_EXTENSIONS + IMAGE_EXTENSIONS + VIDEO_EXTENSIONS + CODE_EXTENSIONS + ["pptx", "docx", "xlsx"]

_SIGNATURES = {
    "pdf": [b"%PDF"],
    "png": [b"\x89PNG"],
    "jpg": [b"\xff\xd8\xff"],
    "jpeg": [b"\xff\xd8\xff"],
    "gif": [b"GIF8"],
    "glb": [b"glTF"],
}


@deconstructible
class MaxFileSizeValidator:
    def __init__(self, max_mb: int | None = None):
        self.max_mb = max_mb

    def __call__(self, file):
        limit = self.max_mb or settings.MAX_UPLOAD_SIZE_MB
        if file.size > limit * 1024 * 1024:
            raise ValidationError(f"File too large. Maximum size is {limit} MB.")

    def __eq__(self, other):
        return isinstance(other, MaxFileSizeValidator) and self.max_mb == other.max_mb


@deconstructible
class FileSignatureValidator:
    """Rejects files whose leading bytes don't match their extension (for formats with magic numbers)."""

    def __call__(self, file):
        ext = file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
        signatures = _SIGNATURES.get(ext)
        if not signatures:
            return
        pos = file.tell() if hasattr(file, "tell") else 0
        head = file.read(8)
        file.seek(pos)
        if not any(head.startswith(sig) for sig in signatures):
            raise ValidationError("File content does not match its extension.")

    def __eq__(self, other):
        return isinstance(other, FileSignatureValidator)


def file_validators(extensions: list[str], max_mb: int | None = None):
    return [FileExtensionValidator(extensions), MaxFileSizeValidator(max_mb), FileSignatureValidator()]


image_validators = file_validators(IMAGE_EXTENSIONS, 10)
pdf_validators = file_validators(DOCUMENT_EXTENSIONS, 25)
video_validators = file_validators(VIDEO_EXTENSIONS, 200)
model_3d_validators = file_validators(MODEL_3D_EXTENSIONS, 50)
study_file_validators = file_validators(STUDY_FILE_EXTENSIONS, 100)
