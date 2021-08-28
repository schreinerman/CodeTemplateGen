const char* strBuildWindows = 
"@Echo off\r\n"
"set PATH=\%PATH\%;C:\MinGW\bin;C:\Program Files\CMake\bin\r\n"
"cd \%~dp0\r\n"
"mkdir build\r\n"
"cd build\r\n"
"cmake .. -G \"MinGW Makefiles\"\r\n"
"mingw32-make\r\n"
"pause\r\n";

