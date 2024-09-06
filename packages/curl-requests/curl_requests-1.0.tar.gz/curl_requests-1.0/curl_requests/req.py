import ctypes
import os
import platform
import subprocess
import sys
import json

file = __file__.replace(r"req.py", "")

def library_exists():
    current_dir = os.path.abspath(file)
    
    if platform.system() == "Windows":
        lib_ext = "dll"
    elif platform.system() == "Linux":
        lib_ext = "so"
        

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
        print("vcpkg install...")
        clone_command = [
            "git", "clone", "https://github.com/microsoft/vcpkg.git", vcpkg_path
        ]
        result = subprocess.run(clone_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            sys.exit(1)

        
        # Bootstrap vcpkg
        bootstrap_script = "bootstrap-vcpkg.sh" if platform.system() != "Windows" else "bootstrap-vcpkg.bat"
        bootstrap_command = [os.path.join(vcpkg_path, bootstrap_script)]

        result = subprocess.run(bootstrap_command, cwd=vcpkg_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        if result.returncode != 0:
            sys.exit(1)

        print("vcpkg bootstrapped successfully.")

        print("Installing curl using vcpkg...")
        install_command = [os.path.join(vcpkg_path, "vcpkg"), "install", "curl"]
        result = subprocess.run(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            sys.exit(1)

        print("curl installed successfully.")

def run_cmake():
    if library_exists(): return

    current_dir = os.path.dirname(os.path.abspath(__file__))
    vcpkg_path = os.path.join(current_dir, "vcpkg")
    build_dir = os.path.join(current_dir, "build")

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    cmake_command = [
        "cmake", "..",
        f"-DCMAKE_TOOLCHAIN_FILE={os.path.join(vcpkg_path, 'scripts', 'buildsystems', 'vcpkg.cmake')}"
    ]

    result = subprocess.run(cmake_command, cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        sys.exit(1)

def build_cpp():
    if library_exists(): return

    build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")

    build_command = ["cmake", "--build", "."]
    result = subprocess.run(build_command, cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        sys.exit(1)

def find_main_cpp():
    for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(file))):
        if "main.cpp" in files:
            return os.path.join(root, "main.cpp")
    return None

def create_cpp():
    file_path = __file__.replace("req.py", "main.cpp")
    
    cpp_code = '''\
#include <curl/curl.h>
#include <string>
#include <cstring>

extern "C" {

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s) {
    size_t newLength = size * nmemb;
    try {
        s->append((char*)contents, newLength);
    } catch (std::bad_alloc&) {
        return 0; 
    }
    return newLength;
}

__attribute__((visibility("default"))) const char* zapros(const char* url, const char* method, const char* body, const char* headers) {
    CURL* curl;
    CURLcode res;
    static std::string readBuffer;
    static std::string result;

    readBuffer.clear();
    result.clear();

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        
        if (strcmp(method, "post") == 0) {
            curl_easy_setopt(curl, CURLOPT_POST, 1L);
            if (strlen(body) > 0) {
                curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body);
            }
        }

        struct curl_slist *chunk = nullptr;
        if (strlen(headers) > 0) {
            chunk = curl_slist_append(chunk, headers);
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
        }

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

        res = curl_easy_perform(curl);
        
        long http_code = 0;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);

        curl_easy_cleanup(curl);

        if (!readBuffer.empty() && readBuffer.back() == '\\n') {
            readBuffer.pop_back();
        }

        result = std::to_string(http_code) + "|" + readBuffer;
    }

    return result.c_str();
}
}
'''

    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            file.write(cpp_code)

def set_so():
    file_path = file.replace("req.py", "")
    command = [
        'g++',
        '-shared',
        '-fPIC',
        f"{file_path}main.cpp",
        '-o', f"{file_path}my_library.so",
        '-lcurl'
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)

class CurlRequest:
    def __init__(self):

        if platform.system() != "Linux": 

            install_vcpkg()
            run_cmake()
            build_cpp()
        
        else:
            if not library_exists():

                find_main_cpp()
                create_cpp()
                set_so()

        
        lib_ext = "build/Debug/my_library.dll" if platform.system() == "Windows" else "my_library.so"
        lib_path = os.path.join(os.path.abspath(file), lib_ext)
        
        try:
            self.lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise e

        self.lib.zapros.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.lib.zapros.restype = ctypes.c_char_p

    def convert_json(self, text):
        try:
            return json.loads(text)
        except:
            return None

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
