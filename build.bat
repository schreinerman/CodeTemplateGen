@Echo off
set PATH=%PATH%;C:\MinGW\bin;C:\Program Files\CMake\bin
cd %~dp0
mkdir build
cd build
cmake .. -G "MinGW Makefiles"
mingw32-make
pause
