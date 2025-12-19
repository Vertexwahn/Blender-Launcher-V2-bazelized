load("@rules_python//python:defs.bzl", "py_binary")
load("@blender_launcher_pip//:requirements.bzl", "requirement")

py_binary(
    name = "rcc",
    srcs = ["rcc.py"],
    data = ["//source/resources"],
    deps = [requirement("pyside6-essentials")],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "generate_resources_bazel",
    srcs = ["generate_resources_bazel.py"],
    data = ["//source/resources:resource_data"],
    deps = [requirement("pyside6-essentials")],
    visibility = ["//visibility:public"],
)
