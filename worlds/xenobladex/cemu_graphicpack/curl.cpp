#include <cstddef>

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

__realloc = 0x03b1af20
#endif

int* _uploadHandle = nullptr;
int* _uploadMultiHandle = nullptr;
int* _downloadHandle = nullptr;
int* _downloadMultiHandle = nullptr;
char _hostUpload[] = "http://localhost:45872/locations";
char _hostDownload[] = "http://localhost:45872/items";

namespace import{
	namespace nlibcurl{
		void curl_easy_cleanup(int* handle);
		int* curl_easy_init();
		void curl_easy_setopt(int* handle, int code, ...);
		int* curl_multi_init();
		void curl_multi_add_handle(int* multiHandle, int* handle);
		void curl_multi_perform(int* multiHandle, int* left);
		void*curl_multi_info_read(int* multiHandle, int* left);
		void curl_multi_remove_handle(int* multiHandle, int* handle); 
		void curl_multi_cleanup(int* multiHandle);
	}
	namespace coreinit{
		void* memcpy( void* dest, const void* src, size_t count );
	}
}

void *__realloc(void *memblock, size_t size);


// Using https://curl.se/libcurl/c/ but with the multi flow
void _initCurl(){
	int curlOptUrl = 10002;

	_uploadHandle = import::nlibcurl::curl_easy_init();
	import::nlibcurl::curl_easy_setopt(_uploadHandle, curlOptUrl, _hostUpload);
	_uploadMultiHandle = import::nlibcurl::curl_multi_init();

	_downloadHandle = import::nlibcurl::curl_easy_init();
	import::nlibcurl::curl_easy_setopt(_downloadHandle, curlOptUrl, _hostDownload);
	_downloadMultiHandle = import::nlibcurl::curl_multi_init();
}

void _postCurl(char text[]){
	int curlOptPostFields = 10015;
	int curlOptPost = 47;
	int leftRunning = 1;

	import::nlibcurl::curl_multi_add_handle(_uploadMultiHandle, _uploadHandle);
	import::nlibcurl::curl_easy_setopt(_uploadHandle, curlOptPostFields, text);
	import::nlibcurl::curl_easy_setopt(_uploadHandle, curlOptPost, 1L);
	do{
		import::nlibcurl::curl_multi_perform(_uploadMultiHandle, &leftRunning);
	} while(leftRunning != 0);
	import::nlibcurl::curl_multi_remove_handle(_uploadMultiHandle, _uploadHandle);
}

struct memory {
	char *response;
	size_t size;
};

size_t _WriteCallback(void* data, size_t size, size_t nmemb, void* userp)
{
   size_t realsize = size * nmemb;
   struct memory *mem = (struct memory *)userp;
 
   char *ptr = (char*)__realloc(mem->response, mem->size + realsize + 1);
 
   mem->response = ptr;
   import::coreinit::memcpy(&(mem->response[mem->size]), data, realsize);
   mem->size += realsize;
   mem->response[mem->size] = 0;
 
   return realsize;
}

char* _getCurl(){
	memory result = { nullptr, 0};
	int leftRunning = 1;
	int curlOptWriteFunction = 20011;
	int curlOptWriteData = 10001;

	import::nlibcurl::curl_multi_add_handle(_downloadMultiHandle, _downloadHandle);
	import::nlibcurl::curl_easy_setopt(_downloadHandle, curlOptWriteFunction, _WriteCallback);
	import::nlibcurl::curl_easy_setopt(_downloadHandle, curlOptWriteData, &result);
	do{
		import::nlibcurl::curl_multi_perform(_downloadMultiHandle, &leftRunning);
	} while(leftRunning != 0);
	import::nlibcurl::curl_multi_remove_handle(_downloadMultiHandle, _downloadHandle);
	return result.response;
}

void _cleanupCurl(){
	import::nlibcurl::curl_easy_cleanup(_uploadHandle);
	import::nlibcurl::curl_multi_cleanup(_uploadMultiHandle);

	import::nlibcurl::curl_easy_cleanup(_downloadHandle);
	import::nlibcurl::curl_multi_cleanup(_downloadMultiHandle);

	_uploadHandle = nullptr;
	_uploadMultiHandle = nullptr;
	_downloadHandle = nullptr;
	_downloadMultiHandle = nullptr;
}
