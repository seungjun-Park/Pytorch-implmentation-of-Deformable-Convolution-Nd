import os
import glob

import torch

from torch.utils.cpp_extension import CUDA_HOME
from torch.utils.cpp_extension import CppExtension
from torch.utils.cpp_extension import CUDAExtension


from setuptools import find_packages
from setuptools import setup

requirements = ["torch", "torchvision"]


def get_extension():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    extensions_dir = os.path.join(this_dir, "src")

    main_file = glob.glob(os.path.join(extensions_dir, "*.cpp"))
    source_cpu = glob.glob(os.path.join(extensions_dir, "cpu", "*.cpp"))
    source_cuda = glob.glob(os.path.join(extensions_dir, "cuda", "*.cu"))

    sources = main_file + source_cpu
    extension = CppExtension
    extra_compile_args = {"cxx": []}
    define_macros = []

    if torch.cuda.is_available() and CUDA_HOME is not None:
        extension = CUDAExtension
        sources += source_cuda
        define_macros += [("WITH_CUDA", None)]
        extra_compile_args['nvcc'] = [
            "-DCUDA_HAS_FP16=1",
            "-D__CUDA_NO_HALF_OPERATOR__",
            "-D__CUDA_NO_HALF_CONVERSIONS__",
            "-D__CUDA_NO_HALF2_OPERATORS__",
        ]
    else:
        pass

    sources = [os.path.join(extensions_dir, s) for s in sources]
    include_dirs = [extensions_dir]
    ext_modules = [
        extension(
            "deform_conv.ext",
            sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
        )
    ]
    return ext_modules


setup(
    name="deform_conv",
    version="1.0",
    author="seungjun-Park",
    url="https://github.com/seungjun-Park/pytorch_cuda_tutorial",
    description="pytorch wrapper for n-dimensional deformable convolution",
    packages=find_packages("ops", "ops/functions", "ops/modules"),
    ext_modules=get_extension(),
    cmdclass={"build_ext": torch.utils.cpp_extension.BuildExtension},
)




















