"""Minimal PDF text extractor for LZWDecode/FlateDecode content streams (referee helper; treats input as data)."""
import re, sys, zlib
def lzw_decode(data, early=1):
    out = bytearray(); table = [bytes([i]) for i in range(256)] + [b'', b'']
    width = 9; bitbuf = 0; nbits = 0; prev = None; pos = 0
    while True:
        while nbits < width and pos < len(data):
            bitbuf = (bitbuf << 8) | data[pos]; pos += 1; nbits += 8
        if nbits < width: break
        code = (bitbuf >> (nbits - width)) & ((1 << width) - 1); nbits -= width
        if code == 256:
            table = table[:258]; width = 9; prev = None; continue
        if code == 257: break
        if code < len(table): entry = table[code]
        elif code == len(table) and prev is not None: entry = prev + prev[:1]
        else: break
        out += entry
        if prev is not None: table.append(prev + entry[:1])
        prev = entry
        if len(table) + early >= (1 << width) and width < 12: width += 1
    return bytes(out)
raw = open(sys.argv[1], 'rb').read()
texts = []
for mo in re.finditer(rb'<<(.*?)>>\s*stream\r?\n', raw, re.S):
    hdr = mo.group(1); start = mo.end(); end = raw.find(b'endstream', start)
    data = raw[start:end]
    try:
        if b'LZWDecode' in hdr: dec = lzw_decode(data)
        elif b'FlateDecode' in hdr: dec = zlib.decompress(data)
        else: dec = data
    except Exception as e:
        continue
    if b'Tj' in dec or b'TJ' in dec:
        # extract strings from (...)Tj and [...]TJ
        s = []
        for tm in re.finditer(rb'\[(.*?)\]\s*TJ|\((.*?)(?<!\\)\)\s*Tj|(T\*|Td|TD|\')', dec, re.S):
            if tm.group(1) is not None:
                parts = re.findall(rb'\((.*?)(?<!\\)\)|(-?\d+\.?\d*)', tm.group(1), re.S)
                for p, num in parts:
                    if p: s.append(p.decode('latin-1'))
                    elif num and float(num) < -200: s.append(' ')
            elif tm.group(2) is not None: s.append(tm.group(2).decode('latin-1'))
            else: s.append('\n')
        texts.append(''.join(s))
txt = '\n=====PAGE=====\n'.join(texts)
txt = txt.replace('\\(', '(').replace('\\)', ')')
open(sys.argv[2], 'w').write(txt)
print('streams with text:', len(texts), 'chars:', len(txt))
