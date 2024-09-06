#include <curl/curl.h>
#include <string>
#include <cstring>

#ifdef _WIN32
    #define EXPORT_FUNCTION __declspec(dllexport)
#else
    #define EXPORT_FUNCTION
#endif

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s) {
    size_t newLength = size * nmemb;
    try {
        s->append((char*)contents, newLength);
    } catch (std::bad_alloc&) {
        return 0;
    }
    return newLength;
}

extern "C" EXPORT_FUNCTION const char* zapros(const char* url, const char* method, const char* body, const char* headers) {
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

        if (!readBuffer.empty() && readBuffer.back() == '\n') {
            readBuffer.pop_back();
        }

        result = std::to_string(http_code) + "|" + readBuffer;
    }

    return result.c_str();
}
