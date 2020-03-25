cp -R ../mdtex .
cp ../readme-tex readme-tex
docker build --build-arg DUMMY=`date +%s` -t tex .
