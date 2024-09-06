#include <curl/curl.h>
#include <string>
#include <cstring>

extern "C" {

// Callback function for writing data to a string
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* s) {
    size_t newLength = size * nmemb;
    try {
        s->append((char*)contents, newLength);
    } catch (std::bad_alloc&) {
        return 0; // Handle memory problem
    }
    return newLength;
}

// Main request function
__declspec(dllexport) const char* zapros(const char* url, const char* method, const char* body, const char* headers) {
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

        // Perform the request
        res = curl_easy_perform(curl);
        
        // Get the HTTP status code
        long http_code = 0;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);

        // Cleanup
        curl_easy_cleanup(curl);

        // Trim any trailing newline characters from the response
        if (!readBuffer.empty() && readBuffer.back() == '\n') {
            readBuffer.pop_back();
        }

        // Combine the status code and the response body into a single string
        result = std::to_string(http_code) + "|" + readBuffer;
    }

    return result.c_str();
}
}
