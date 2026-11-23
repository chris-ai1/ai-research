# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
import re, sys, zlib
data = open(sys.argv[1], 'rb').read()
# collect decompressed streams
out = []
for m in re.finditer(rb'stream\r?\n', data):
    start = m.end()
    end = data.find(b'endstream', start)
    chunk = data[start:end]
    try:
        out.append(zlib.decompress(chunk))
    except Exception:
        try:
            out.append(zlib.decompressobj().decompress(chunk))
        except Exception:
            pass
blob = b'\n'.join(out) + data
# hyperref anchors
anchors = sorted(set(re.findall(rb'theorem\.(\d+)', blob)), key=lambda s: int(s))
print('theorem anchors:', [a.decode() for a in anchors])
# Try to find text runs "Theorem" in content streams (TJ arrays)
txt = []
for s in out:
    for tj in re.findall(rb'\[(.*?)\]\s*TJ', s, flags=re.S):
        parts = re.findall(rb'\(((?:\\.|[^\\)])*)\)', tj)
        txt.append(b''.join(parts))
    for t in re.findall(rb'\(((?:\\.|[^\\)])*)\)\s*Tj', s):
        txt.append(t)
joined = b' | '.join(txt)
for pat in [rb'Theorem', rb'Theor']:
    hits = [joined[max(0,h.start()-5):h.end()+12] for h in re.finditer(pat, joined)]
    print(pat, len(hits), hits[:30])
