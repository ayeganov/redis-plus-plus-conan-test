import os
from conans import ConanFile, CMake, tools


class RedisPlusPlusConan(ConanFile):
    name = "redis-plus-plus"
    version = "1.2.1"
    description = "Redis client written in C++"
    topics = ("conan", "redis")
    homepage = "https://github.com/sewenew/redis-plus-plus"
    author = "Zinnion <mauro@zinnion.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]

    generators = "cmake", "cmake_find_package"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "with_ssl": [True, False]
    }
    default_options = {
        "shared": False,
        "with_ssl": True
    }

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        self.requires("hiredis/1.0.0")

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self.options["hiredis"].with_ssl = self.options.with_ssl
        self.options["hiredis"].shared = self.options.shared
        self._cmake.definitions['CMAKE_BUILD_TYPE'] = 'Release'
        self._cmake.definitions['CMAKE_PREFIX_PATH'] = self.deps_cpp_info['hiredis'].rootpath
        self._cmake.definitions["REDIS_PLUS_PLUS_BUILD_TEST"] = "OFF"
        self._cmake.definitions["REDIS_PLUS_PLUS_BUILD_STATIC"] = not self.options.shared
        self._cmake.definitions["REDIS_PLUS_PLUS_BUILD_SHARED"] = self.options.shared
        self._cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return self._cmake

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
