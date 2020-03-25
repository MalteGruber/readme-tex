
FROM python:3.5-alpine3.10
RUN apk add texlive-dvi
RUN apk add make

ARG DUMMY=unknown
RUN DUMMY=${DUMMY}

RUN mkdir test
RUN mkdir test/usr
ADD mdtex test/mdtex

ADD readme-tex test/readme-tex
RUN ls test

WORKDIR /test/usr
ENTRYPOINT ["python3","/test/mdtex/mdtex.py"]