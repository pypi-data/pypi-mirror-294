import ctypes
import os
import platform
import subprocess
import sys

from tqdm import tqdm
import json

def library_exists():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if platform.system() == "Windows":
        lib_ext = "dll"
    elif platform.system() == "Linux":
        lib_ext = "so"
    else:
        sys.exit(1)

    lib_path = os.path.join(current_dir, "build/Debug", f"my_library.{lib_ext}")
    return os.path.isfile(lib_path)


lib = library_exists()

class Response:
    def __init__(self, status_code, text, json):
        self.status_code = status_code
        self.text = text
        self.json = json

def install_vcpkg():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vcpkg_path = os.path.join(current_dir, "vcpkg")

    if not os.path.exists(vcpkg_path):

        print("Cloning vcpkg...")
        clone_command = [
            "git", "clone", "https://github.com/microsoft/vcpkg.git", vcpkg_path
        ]

        result = subprocess.run(clone_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0: sys.exit(1)

        bootstrap_script = "bootstrap-vcpkg.bat" if platform.system() == "Windows" else "bootstrap-vcpkg.sh"
        bootstrap_command = [os.path.join(vcpkg_path, bootstrap_script)]

        result = subprocess.run(bootstrap_command, cwd=vcpkg_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0: sys.exit(1)
        install_command = [os.path.join(vcpkg_path, "vcpkg"), "install", "curl"]

        print("Install curl...")

        result = subprocess.run(install_command, cwd=vcpkg_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0: sys.exit(1)

def run_cmake():
    if bool(lib) is True:
        return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    vcpkg_path = os.path.join(current_dir, "vcpkg")
    build_dir = os.path.join(current_dir, "build")

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    cmake_command = [
        "cmake", "..",
        f"-DCMAKE_TOOLCHAIN_FILE={os.path.join(vcpkg_path, 'scripts', 'buildsystems', 'vcpkg.cmake')}",
        "-DCMAKE_BUILD_TYPE=Debug"
    ]


    result = subprocess.run(cmake_command, cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        sys.exit(1)

def build_cpp():
    if bool(lib) is True:
        return

    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")

    build_command = ["cmake", "--build", ".", "--config", "Debug"]
    result = subprocess.run(build_command, cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        sys.exit(1)


class CurlRequest:

    if platform.system() != "Linux": 

        install_vcpkg()
        run_cmake()
        build_cpp()
    
    else:
        if not os.path.exists("my_library.so"):
            os.system("g++ -fPIC -shared -o my_library.so main.cpp -lcurl")

    def convert_json(self, text):

        try:
            return json.loads(text)
        except: return None

    def __init__(self):
        
        Linux = r"build\Debug\my_library."
        if platform.system() == "Windows":
            lib_ext = "dll"
        elif platform.system() == "Linux":
            Linux = "my_library."
            lib_ext = "so"
        else:
            raise OSError("Unsupported operating system.")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(current_dir, f"{Linux}{lib_ext}")

        try:
            self.lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise e

        self.lib.zapros.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.lib.zapros.restype = ctypes.c_char_p


    def make_request(self, url, method="get", body=None, headers=None):

        if isinstance(body, dict):
            body = json.dumps(body)
        
        if isinstance(headers, dict):
            headers = "\r\n".join([f"{key}: {value}" for key, value in headers.items()])

        body = body if body else ""
        headers = headers if headers else ""

        url_bytes = url.encode('utf-8')
        method_bytes = method.lower().encode('utf-8')
        body_bytes = body.encode('utf-8')
        headers_bytes = headers.encode('utf-8')

        response = self.lib.zapros(url_bytes, method_bytes, body_bytes, headers_bytes)
        combined_response = response.decode('utf-8')

        status_code, response_body = combined_response.split('|', 1)
        return Response(int(status_code), response_body, self.convert_json(response_body))
        
    def get(self, url, headers=None):
        return self.make_request(url, "get", headers=headers)
    
    def post(self, url, body=None, headers=None):
        return self.make_request(url, "post", body=body, headers=headers)