import brotli

MODE_TYPE_MAP = {
    "html": brotli.MODE_TEXT,
    "js": brotli.MODE_TEXT,
    "css": brotli.MODE_TEXT,
    "jpg": brotli.MODE_GENERIC,
}
