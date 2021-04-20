@Echo off
cd %~dp0
mkdir build
cd build
cmake ..
make
