#!/usr/bin/env python3
import glob
import pathlib
import re
import subprocess
import sys
from typing import List

import toml

# constants
CONFIG_FILENAME: str = 'goat.toml'
BUILD_FLAGS_TAG: str = 'compilation'
SOURCE_DIRECTORY: str = 'src'
OBJ_DIRECTORY: str = 'obj'
TEST_DIRECTORY: str = 'test'
BIN_DIRECTORY: str = 'bin'
INCLUDE_DIRECTORY: str = 'include'
OBJ_EXTENSION: str = '.o'
REGEX_LINE_START: str = '^'
REGEX_LINE_END: str = '$'
CC_FILE_EXTENSION: str = '.cc'
GOAT_TOML_TEMPLATE: str = """[compilation]
TARGET = 'App'
CXX = 'g++'
CXXFLAGS = ['-std=c++17', '-Wall', '-Werror', '-O3']
INCLUDES = ['src', 'include']

[packages]
"""

MAIN_TEMPLATE: str = """#include <iostream>

int main(void) {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""

TEST_TEMPLATE: str = """#include "gtest/gtest.h"

TEST(SquareRootTest, PositiveNos) {
    EXPECT_EQ(18.0, 18);
    EXPECT_EQ(25.7, 26);
    EXPECT_EQ(50.3321, 50);
}
"""

GTEST_LDLIBS: List[str] = [
    '-L./lib/x86_64-linux-gnu', '-lgtest', '-lgtest_main']


def find(rootdir: str, regex: str):
    return glob.glob(rootdir + '/**/' + regex, recursive=True)


def flatten(items: List):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


def source_to_object(source: str):
    # src/* -> obj/*
    o = re.sub(REGEX_LINE_START + SOURCE_DIRECTORY, OBJ_DIRECTORY, source)
    # *.cc -> *.o
    o = re.sub(CC_FILE_EXTENSION + REGEX_LINE_END, OBJ_EXTENSION, o)
    return o


def generate_objects(compiler: str, flags: List[str], includes: List[str],
                     source_files: List[str]):
    pathlib.Path(OBJ_DIRECTORY).mkdir(parents=True, exist_ok=True)
    for source in source_files:
        command = flatten([compiler, flags, '-c',
                           includes, source, '-o',
                           source_to_object(source)])
        subprocess.Popen(command).wait()


def generate_binary(compiler: str, flags: List[str], includes: str,
                    sources: List[str], target: str):
    pathlib.Path(BIN_DIRECTORY).mkdir(parents=True, exist_ok=True)
    command = flatten([compiler, flags,
                       includes, sources, '-o', BIN_DIRECTORY + '/' + target])
    subprocess.Popen(command).wait()


def compile_sources(compiler, flags, includes, sources, target):
    # TODO: compile only the required shit
    includes_flags: List[str] = ['-I'+include for include in includes]
    generate_objects(compiler, flags, includes_flags, sources)
    objects: List[str] = find(OBJ_DIRECTORY, '*.o')
    generate_binary(compiler, flags, includes_flags, objects, target)


def clean_project(target: str):
    for f in find(OBJ_DIRECTORY, '*.o'):
        pathlib.Path(f).unlink()
    for f in find(BIN_DIRECTORY, '*'):
        pathlib.Path(f).unlink()


def create_file_with_data(filename: str, data: str):
    with open(filename, 'w+') as f:
        f.write(data)


def create_new_project(command: List[str]):
    project_name = command[0]
    # Create directories
    pathlib.Path(project_name).mkdir(parents=False, exist_ok=False)
    pathlib.Path(project_name+'/' +
                 SOURCE_DIRECTORY).mkdir(parents=False, exist_ok=False)
    pathlib.Path(project_name+'/include').mkdir(parents=False, exist_ok=False)
    pathlib.Path(project_name+'/' +
                 TEST_DIRECTORY).mkdir(parents=False, exist_ok=False)

    # Create files
    create_file_with_data(project_name+'/goat.toml', GOAT_TOML_TEMPLATE)
    create_file_with_data(project_name+'/' +
                          SOURCE_DIRECTORY+'/main.cc', MAIN_TEMPLATE)
    create_file_with_data(project_name+'/' +
                          TEST_DIRECTORY+'/test.cc', TEST_TEMPLATE)


def build_tests(compiler: str, flags: List[str], includes: List[str],
                sources: List[str]):
    pathlib.Path(BIN_DIRECTORY).mkdir(parents=True, exist_ok=True)
    sources.remove(SOURCE_DIRECTORY+'/'+'main.cc')
    includes_flags: List[str] = ['-I'+include for include in includes]
    for test_file in find(TEST_DIRECTORY, '*.cc'):
        test_name = test_file.rsplit('/')[1].rsplit('.')[0]
        command = flatten(
            [compiler, flags, includes_flags, test_file, sources,
             '-o', BIN_DIRECTORY + '/' + test_name, GTEST_LDLIBS])
        subprocess.Popen(command).wait()


def handle_existing_project(command: List[str]):
    conf = toml.load(CONFIG_FILENAME)

    build_flags: dict = conf[BUILD_FLAGS_TAG]
    sources: List[str] = find(SOURCE_DIRECTORY, '*.cc')
    flags: List[str] = build_flags['CXXFLAGS']
    includes: List[str] = build_flags['INCLUDES']
    compiler: str = build_flags['CXX']
    target: str = build_flags['TARGET']
    keyword = command[0]

    match keyword:
        case 'run':
            compile_sources(compiler, flags, includes, sources, target)
            return subprocess.Popen('./'+target).wait()
        case 'build':
            return compile_sources(compiler, flags, includes, sources, target)
        case 'clean':
            print('Cleaning binary and object files...')
            return clean_project(target)
        case 'test':
            print('Building and running tests')
            build_tests(compiler, flags, includes, sources)
        case _:
            print_help()
            return 1


def print_help():
    print('Welcome to goat!')
    print('Commands: build               - build this project')
    print('          test                - run tests')
    print('          run                 - run program')
    print('          clean               - clean existing binary and .o files')
    print('          new <PROJECT NAME>  - create a new goat project')
    print('          help                - show this message')


def main():
    if len(sys.argv) < 2:
        print_help()
        return 1

    goat_toml = pathlib.Path(CONFIG_FILENAME)

    if (goat_toml.exists()):
        return handle_existing_project(sys.argv[1:])

    keyword = sys.argv[1]
    match keyword:
        case 'new':
            create_new_project(sys.argv[2:])
        case 'help':
            print_help()
        case _:
            print_help()


if __name__ == '__main__':
    main()
