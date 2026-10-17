FROM ubuntu:24.04 AS build

ENV DEBIAN_FRONTEND=noninteractive \
    GIT_TERMINAL_PROMPT=0 \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bison \
        bzip2 \
        ca-certificates \
        flex \
        gcc \
        git \
        libfdt-dev \
        libglib2.0-dev \
        libpixman-1-dev \
        ninja-build \
        pkg-config \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-venv \
        python3-wheel \
    && rm -rf /var/lib/apt/lists/*

ARG QEMU_PIN=4fc49f46dc95d4a27de2509e7fceb2931e91faeb
ARG QEMU_TAG=v11.1.2

WORKDIR /src
RUN set -eux; \
    ok=0; \
    for attempt in 1 2 3; do \
      if git clone --depth 1 --branch "${QEMU_TAG}" https://github.com/qemu/QEMU.git qemu; then \
        ok=1; \
        break; \
      fi; \
      rm -rf qemu; \
      sleep 8; \
    done; \
    test "${ok}" = 1; \
    cd qemu; \
    HEAD="$(git rev-parse HEAD)"; \
    case "${HEAD}" in \
      "${QEMU_PIN}"*) ;; \
      *) \
        git fetch --depth 1 origin "${QEMU_PIN}"; \
        git checkout "${QEMU_PIN}"; \
        ;; \
    esac; \
    HEAD="$(git rev-parse HEAD)"; \
    echo "qemu-head=${HEAD}"; \
    case "${HEAD}" in \
      "${QEMU_PIN}"*) ;; \
      *) echo "unexpected qemu pin ${HEAD}" >&2; exit 1 ;; \
    esac

WORKDIR /src/qemu
RUN ./configure \
        --prefix=/opt/qemu \
        --target-list=x86_64-softmmu \
        --enable-colo-proxy \
        --enable-replication \
        --enable-asan \
        --enable-tcg \
        --enable-fdt=system \
        --disable-docs \
        --disable-user \
        --disable-tools \
        --disable-guest-agent \
        --disable-sdl \
        --disable-gtk \
        --disable-vnc \
        --disable-spice \
        --disable-usb-redir \
        --disable-libusb \
        --disable-brlapi \
        --disable-curl \
        --disable-gnutls \
        --disable-nettle \
        --disable-gcrypt \
        --disable-kvm \
        --disable-whpx \
        --disable-xen \
        --disable-werror \
        --disable-libnfs \
        --disable-vde \
        --disable-capstone \
        --disable-slirp \
        --disable-linux-aio \
        --disable-linux-io-uring \
        --disable-seccomp \
        --disable-rbd \
        --disable-libiscsi \
        --disable-tpm \
        --disable-rust \
    && ninja -C build -j"$(nproc)" qemu-system-x86_64 \
    && mkdir -p /opt/qemu/bin /opt/qemu/share/qemu \
    && cp -a build/qemu-system-x86_64 /opt/qemu/bin/qemu-system-x86_64 \
    && cp -a pc-bios/*.bin /opt/qemu/share/qemu/ \
    && test -x /opt/qemu/bin/qemu-system-x86_64 \
    && /opt/qemu/bin/qemu-system-x86_64 -version

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    QEMU_AUDIO_DRV=none \
    WITNESS=QEMU-COLO-L4-OOB-WITNESS \
    ASAN_OPTIONS=abort_on_error=1:halt_on_error=1:detect_leaks=0:allocator_may_return_null=1:detect_odr_violation=0 \
    PATH="/opt/qemu/bin:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        libasan8 \
        libfdt1 \
        libpixman-1-0 \
        python3 \
    && (apt-get install -y --no-install-recommends libglib2.0-0t64 \
        || apt-get install -y --no-install-recommends libglib2.0-0) \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 65532 --user-group --create-home \
        --home-dir /home/lab --shell /usr/sbin/nologin lab \
    && mkdir -p /lab /tmp/lab

COPY --from=build /opt/qemu /opt/qemu
COPY poc.py /lab/poc.py

RUN chmod 0755 /lab/poc.py \
    && test -x /opt/qemu/bin/qemu-system-x86_64 \
    && chown -R lab:lab /lab /tmp/lab /home/lab

USER lab
WORKDIR /lab
EXPOSE 18770 18771
CMD ["sleep", "infinity"]
