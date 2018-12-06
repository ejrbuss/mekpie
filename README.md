![](/resources/logo.svg)

# Make Building C as Simple as Pie

Mekpie is an opinionated build system for small scale C projects. The core premise of Mekpie is that you should be spending little to no time worrying about make files, compiler arguments, or build times when working on a small scale C project. By enforcing a simple directory structure Mekpie saves you time and effort. For added convenience MEKPIE takes notes from tools like [Rust's cargo](https://doc.rust-lang.org/cargo/guide/index.html) and [Node's npm](https://www.npmjs.com/) in providing options for building, running, cleaning, and testing your current project.

Mekpie is a small scale project and is not supposed to replace tools like [CMake](https://cmake.org/) or provide any sort of package management capabilities. Use Mekpie when the alternative is a shoddy Make file or manually compiling.

## Installing

*Coming soon*

Use pip to install Mekpie

```bash
$ pip install mekpie
```

## Getting Started

You can create a new project by running

```bash
$ mekpie new "project-name"
project-name created succesfully!
```

Navigating into the project you will find the following file structure

```python
project/               # the project directory
    target/            # managed automatically by mekpie, stores binaries
    includes/          # stores all project .h files
    src/               # stores all project .c files
        project-name.c # should contain `main`
    tests/             # should contain all test files
    mek.py             # used to configure mekpie
```

You can run your project with

```bash
$ mekpie run
Project succesfully cleaned.
Project succesfully built.
Hello, World!
```

You will note that Mekpie provides a clean build every time you run your code. This is a key decision that keeps Mekpie simple and lightweight, but may not make it appropriate for your project if your build times are on the longer side.

## [Read More](https://ejrbuss.net/mekpie)

## Contact

Feel free to send be bug reports or feature requests. If you are interested in my other work, checkout my [website](https://ejrbuss.net).

Email ejrbuss@gmail.com