
FROM python:3.5-alpine3.10
RUN apk add texlive-full
RUN apk add make
RUN date

ARG DUMMY=unknown
#RUN DUMMY=${DUMMY}
#RUN echo $DUMMY>lol.txt
RUN mkdir test
RUN mkdir test/usr
ADD mdtex test/mdtex

ADD readme-tex test/readme-tex
RUN ls test

#ENTRYPOINT ["sh","-c","test/readme-tex"]

WORKDIR /test/usr
ENTRYPOINT ["python3","/test/mdtex/mdtex.py"]