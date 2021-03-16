FROM python:3.8-buster

# Install necessary packages
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends locales-all unzip ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# TEMP
RUN wget -L http://tmp.kiwix.org/wheels/libzim-1.0.0.dev0-cp38-cp38-linux_x86_64.whl http://tmp.kiwix.org/wheels/zimscraperlib-1.3.6.dev0-py3-none-any.whl
RUN pip3 install libzim-1.0.0.dev0-cp38-cp38-linux_x86_64.whl && rm libzim-1.0.0.dev0-cp38-cp38-linux_x86_64.whl
RUN pip3 install zimscraperlib-1.3.6.dev0-py3-none-any.whl && rm zimscraperlib-1.3.6.dev0-py3-none-any.whl

COPY requirements.txt /src/
RUN pip3 install -r /src/requirements.txt
COPY kolibri2zim /src/kolibri2zim
COPY setup.py *.md get_js_deps.sh MANIFEST.in /src/
RUN cd /src/ && python3 ./setup.py install

RUN mkdir -p /output
WORKDIR /output
CMD ["kolibri2zim", "--help"]
