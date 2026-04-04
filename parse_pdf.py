"""
Extract path/coordinate data from bronze-mean-patch.pdf
PDF files contain stream data with path commands (m=moveto, l=lineto, c=curveto, f=fill, S=stroke)
We want to find the unique polygon shapes (tile types) and their vertex coordinates.
"""
import re, struct, zlib

path = "C:/ifsdb.github.io/public/bronze-mean-patch.pdf"

with open(path, 'rb') as f:
    data = f.read()

# Find all compressed streams (FlateDecode)
# Also look at uncompressed PDF commands

# First, let's look at the raw text portions
text_portion = data.decode('latin-1', errors='replace')

# Look for color-set commands and path commands
# PDF path commands: m (moveto), l (lineto), c (curveto), h (close), f/F (fill), S (stroke), W (clip)
# Color commands: rg (RGB fill), RG (RGB stroke), g (gray fill), G (gray stroke)

# Extract streams
streams = []
stream_starts = [m.start() for m in re.finditer(b'stream\r?\n', data)]
stream_ends   = [m.start() for m in re.finditer(b'\r?\nendstream', data)]

print(f"Found {len(stream_starts)} streams")

# Try to decode each stream
decoded_streams = []
for i, (ss, se) in enumerate(zip(stream_starts, stream_ends)):
    raw = data[ss:se]
    # Find actual start after "stream\n"
    start_offset = raw.find(b'\n') + 1
    raw_content = raw[start_offset:]
    
    # Try zlib decompression
    try:
        decoded = zlib.decompress(raw_content)
        decoded_streams.append(decoded.decode('latin-1', errors='replace'))
        print(f"  Stream {i}: {len(raw_content)} bytes compressed -> {len(decoded)} bytes uncompressed")
    except:
        # Try as plain text
        try:
            text = raw_content.decode('latin-1', errors='replace')
            decoded_streams.append(text)
            print(f"  Stream {i}: {len(raw_content)} bytes plain text")
        except:
            decoded_streams.append("")
            print(f"  Stream {i}: failed to decode")

# Find the main drawing stream (largest)
if decoded_streams:
    largest_idx = max(range(len(decoded_streams)), key=lambda i: len(decoded_streams[i]))
    print(f"\nLargest stream: {largest_idx} ({len(decoded_streams[largest_idx])} chars)")
    
    # Show first 2000 chars
    content = decoded_streams[largest_idx]
    print("\nFirst 2000 chars:")
    print(content[:2000])
    print("\n...\nLast 500 chars:")
    print(content[-500:])
