

def curl_trace_block_iterator(curl_content):
    if not curl_content or curl_content == '':
        yield from ()
        return
    content = []
    yil = False
    for line in curl_content.strip().split(b'\n'):
        if line.startswith(b'=') or line.startswith(b'<'): # any block
            if content:
                yield b'\n'.join(content)
                content = []
            content.append(line)
        else: # append to block
            content.append(line)
    if content:
        yield b'\n'.join(content)