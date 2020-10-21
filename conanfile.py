from conans import ConanFile, CMake


class Gateway(ConanFile):
    name = "Gateway"
    settings = "os", "compiler", "build_type", "arch"
    exports = "*"
    build_policy = "missing"
    requires = (
        "redis-plus-plus/1.2.1"
    )
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        self.run(f"cmake --build . {cmake.build_config} -j8")
