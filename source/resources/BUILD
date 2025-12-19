load("@rules_python//python:defs.bzl", "py_library")
load("@blender_launcher_pip//:requirements.bzl", "requirement")

# Expose CSS files
filegroup(
    name = "css_files",
    srcs = glob(["styles/*.css"]),
    visibility = ["//visibility:public"],
)

# Expose QRC file
filegroup(
    name = "qrc_file",
    srcs = ["resources.qrc"],
    visibility = ["//visibility:public"],
)

# Expose all resource files
filegroup(
    name = "resource_data",
    srcs = glob([
        "api/**/*",
        "certificates/**/*",
        "fonts/**/*",
        "icons/**/*",
        "styles/**/*",
    ]),
    visibility = ["//visibility:public"],
)

py_library(
    name = "resources",
    srcs = ["__init__.py"],
    data = glob([
        "api/**/*",
        "certificates/**/*",
        "fonts/**/*",
        "icons/**/*",
        "styles/**/*",
        "*.qrc",
    ]),
    visibility = ["//visibility:public"],
)
