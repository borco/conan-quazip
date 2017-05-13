from conans import ConanFile, CMake, tools

class QuazipConan(ConanFile):
    name = "quazip"
    version = "0.7.3"
    license = "LGPL-2.1, zlib/png"
    description = "A Qt/C++ wrapper for Gilles Vollant's ZIP/UNZIP C package (minizip). Provides access to ZIP archives from Qt programs using QIODevice API."
    url = "https://github.com/borco/conan-quazip"
    settings = "os", "compiler", "build_type", "arch"
    requires = "zlib/1.2.11@lasote/stable"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):
        self.run("svn co https://svn.code.sf.net/p/quazip/code/tags/0.7.3/ quazip")
        tools.replace_in_file('quazip/CMakeLists.txt', 'project(QuaZip)', '''project(QuaZip)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake quazip %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/quazip", src="quazip/quazip")
        self.copy("*quazip.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["quazip5d"] if (self.settings.os == "Windows" and self.settings.build_type == "Debug") else ["quazip5"]
