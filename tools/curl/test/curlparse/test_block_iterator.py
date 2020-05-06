import gurl.curlparse as cp
import uuid


def test_none():
    inp = None
    res = cp.curl_trace_block_iterator(inp)

    assert len(list(res)) == 0


def test_empty():
    inp = ""
    res = cp.curl_trace_block_iterator(inp)

    assert len(list(res)) == 0


def test_one_of_kind():
    send_ssl_data = str(uuid.uuid4())
    send_header = str(uuid.uuid4())
    recv_ssl_data = str(uuid.uuid4())
    send_data = str(uuid.uuid4())
    recv_header = str(uuid.uuid4())
    recv_data = str(uuid.uuid4())

    imp = f"""
== Meta info block
=> Send SSL data, 5 bytes (0x5)
{send_ssl_data}
<= Recv SSL data, 5 bytes (0x5)
{recv_ssl_data}
=> Send header, 78 bytes (0x4e)
{send_header}
=> Send data, 78 bytes (0x4e)
{send_data}
<= Recv header, 17 bytes (0x11)
{recv_header}
<= Recv data, 2044 bytes (0x7fc)
{recv_data}
    """

    expected = [
b"== Meta info block",
bytes(f"=> Send SSL data, 5 bytes (0x5)\n{send_ssl_data}", encoding="utf-8"),
bytes(f"<= Recv SSL data, 5 bytes (0x5)\n{recv_ssl_data}", encoding="utf-8"),
bytes(f"=> Send header, 78 bytes (0x4e)\n{send_header}", encoding="utf-8"),
bytes(f"=> Send data, 78 bytes (0x4e)\n{send_data}", encoding="utf-8"),
bytes(f"<= Recv header, 17 bytes (0x11)\n{recv_header}", encoding="utf-8"),
bytes(f"<= Recv data, 2044 bytes (0x7fc)\n{recv_data}", encoding="utf-8")
    ]

    res = cp.curl_trace_block_iterator(bytes(imp, encoding="utf-8"))

    assert list(res) == expected