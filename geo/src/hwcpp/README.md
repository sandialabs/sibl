# Getting Started with C/C++ for Visual Studio Code

## Install

### Visual Studio Code

* In VS Code, install the C/C++ by Microsoft extension
  * Also install
    * C/C++ Extension Pack
    * C/C++ Themes

### Compiler

```bash
g++ --version  # for g++
clang -- version ## for clang

g++ --version
Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/4.2.1
Apple clang version 12.0.0 (clang-1200.0.32.29)
Target: x86_64-apple-darwin19.6.0
Thread model: posix
InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin

> clang --version
Apple clang version 12.0.0 (clang-1200.0.32.29)
Target: x86_64-apple-darwin19.6.0
Thread model: posix
InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin
```

Assure the binaries are in the `$PATH`:

```bash
> echo $PATH
/Users/chovey/opt/miniconda3/envs/siblenv/bin /Users/chovey/opt/miniconda3/condabin 
/Users/sparta/tools/nvim-osx64/bin 
/usr/local/bin 
/usr/bin 
/bin 
/usr/sbin 
/sbin 
/Library/Apple/usr/bin 
/Library/TeX/texbin

> pwd
/usr/bin
> ls -flt g++
-rwxr-xr-x  1 root  wheel  31488 Sep 21  2020 g++*
> ls -flt clang
-rwxr-xr-x  1 root  wheel  31488 Sep 21  2020 clang*
```

### Debugger

We will use `lldb` since `gdb` is not installed on the Mac yet.

```bash
which lldb                                                             (siblenv)
/usr/bin/lldb
which gdb                                                              (siblenv)
>
```

* Run menu, Add Configuration... item

For Linux and Mac, use the `GDB` debugger.  
[Configure](https://code.visualstudio.com/docs/cpp/launch-json-reference) VS Code 
for C/C++ debugging.

## References

* [VS Code docs](https://code.visualstudio.com/docs/languages/cpp)
* [VS Code debugger](https://code.visualstudio.com/docs/cpp/cpp-debug)
* [Debug a C++ project in VS Code](https://youtu.be/G9gnSGKYIg4)
* [Config `clang` on Mac](https://code.visualstudio.com/docs/cpp/config-clang-mac)
