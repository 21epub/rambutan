cmake_minimum_required(VERSION 3.2)
project(pngquant_py)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    pngquant/lib/blur.c
    pngquant/lib/blur.h
    pngquant/lib/libimagequant.c
    pngquant/lib/libimagequant.h
    pngquant/lib/mediancut.c
    pngquant/lib/mediancut.h
    pngquant/lib/mempool.c
    pngquant/lib/mempool.h
    pngquant/lib/nearest.c
    pngquant/lib/nearest.h
    pngquant/lib/pam.c
    pngquant/lib/pam.h
    pngquant/lib/viter.c
    pngquant/lib/viter.h
    pngquant/pngquant.c
    pngquant/rwpng.c
    pngquant/rwpng.h
    pngquant_tiny.c)

add_executable(pngquant_py ${SOURCE_FILES})