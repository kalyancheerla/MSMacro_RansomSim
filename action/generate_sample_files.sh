#!/bin/sh

mkdir -p tmp/folder1
mkdir -p tmp/folder2
mkdir -p tmp/folder3
mkdir -p tmp/folder4/folder5/folder6

cat > tmp/folder1/sample1.txt << EOF
Sample 1 file
idk wat to write in here...
EOF


cat > tmp/folder1/sample2.png << EOF
Sample 2 file
ok ok.. hmm..
thats enough..
EOF

cat > tmp/folder2/sample3.docx << EOF
Sample 3 file
VERY VERY IMP DOC this is!
EOF

cat > tmp/folder2/sample5.jpg << EOF
Sample 5 file
Family pic 1
EOF

cat > tmp/folder2/sample6.jpg << EOF
Sample 6 file
Family pic 2
EOF

cat > tmp/folder4/folder5/folder6/sample4.xlsx << EOF
Sample 4 file
EOF

