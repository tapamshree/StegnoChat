CARRIERS = [
    '\u200B',  # Zero-Width Space         → 00
    '\u200C',  # Zero-Width Non-Joiner    → 01
    '\u200D',  # Zero-Width Joiner        → 10
    '\uFEFF',  # Zero-Width No-Break Sp.  → 11
]

def encode(message: str, cover: str = "👋") -> str:
    if not message:
        return cover
    raw = message.encode('utf-8')
    bits = ''.join(f'{b:08b}' for b in raw)
    hidden = ''.join(
        CARRIERS[int(bits[i:i+2], 2)]
        for i in range(0, len(bits), 2)
    )
    return cover + hidden

def decode(text: str) -> str | None:
    if not text:
        return None
    bits = ''.join(
        f'{CARRIERS.index(ch):02b}'
        for ch in text
        if ch in CARRIERS
    )
    if not bits:
        return None  # no hidden content
    
    # Ensure bits length is a multiple of 8
    bits = bits[:len(bits) - (len(bits) % 8)]
    if not bits:
        return None
        
    raw = bytearray(
        int(bits[i:i+8], 2)
        for i in range(0, len(bits), 8)
    )
    
    # decode utf-8 but ignore errors
    result = raw.decode('utf-8', errors='ignore')
    # Filter out null characters and empty results that might occur from partial strings
    result = result.replace('\x00', '')
    if not result:
        return None
        
    return result
