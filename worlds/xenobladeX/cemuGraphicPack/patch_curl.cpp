// Use https://godbolt.org/ with power gcc.
// Use vscode with https://marketplace.visualstudio.com/items?itemName=OGoodness.powerpc-syntax
// and https://marketplace.visualstudio.com/items?itemName=bhughes339.replacerules
// Adjust your settings:
// "replacerules.rules": {
//     "Replace invalid Labels": {
//         "find": "[.](LC?[0-9]+)",
//         "replace": "_NAME_$1",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Remove all function brackets": {
//         "find": "[(](?!r?[1-3]?[0-9]).*[)]",
//         "replace": "",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Add register prefix to all easy numbers": {
//         "find": "(?<=[ ,(])([1-3]?[0-9])(?=[),])",
//         "replace": "r$1",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Add register prefix to all complex numbers": {
//         "find": "(?<!^.*i.*,)(?<=[, ])([1-3]?[0-9])(?=[\n])",
//         "replace": "r$1",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Remove prefix from crxor": {
//         "find": "crxor r([0-9]+),r([0-9]+),r([0-9]+)",
//         "replace": "crxor $1,$2,$3",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Restructure la instructions": {
//         "find": "la (r[1-3]?[0-9]),(.*)[(](r[1-3]?[0-9])[)]",
//         "replace": "addi $1,$3,$2",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Restructure condition instructions": {
//         "find": "(cmp[a-z]*|b[a-z]*) (r[0-7])",
//         "replace": "$1 c$2",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Handle target out of range error for internal functions": {
//         "find": "bl (__.*)",
//         "replace": "lis r12, after$1@ha\n\t\taddi r12, r12, after$1@l\n\t\tmtlr r12\n\t\tlis r12, $1@ha\n\t\taddi r12, r12, $1@l\n\t\tmtctr r12\n\t\tbctr\nafter$1:",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Remove rlwinm, this could lead to errors": {
//         "find": ".*rlwinm .*[\n]",
//         "replace": "",
//         "languages": [
//             "asm"
//         ]
//     },
// },
// "replacerules.rulesets": {
//     "Convert PPC Assembly to format for Cemu Graphic Packs": {
//         "rules": [
//             "Replace invalid Labels",
//             "Remove all function brackets",
//             "Add register prefix to all easy numbers",
//             "Add register prefix to all complex numbers",
//             "Remove prefix from crxor",
//             "Restructure la instructions",
//             "Restructure condition instructions",
//             "Handle target out of range error for internal functions",
//             "Remove rlwinm, this could lead to errors",
//         ]
//     }
// },
// Run the new ruleset to adjust your .asm code
#include <cstddef>
int* _uploadHandle = nullptr;
int* _uploadMultiHandle = nullptr;
int* _downloadHandle = nullptr;
int* _downloadMultiHandle = nullptr;
char hostUpload[] = "http://localhost:45872/locations";
char hostDownload[] = "http://localhost:45872/items";

void _curl_easy_cleanup(int* handle);
int* _curl_easy_init();
void _curl_easy_setopt(int* handle, int code, ...);
int* _curl_multi_init();
void _curl_multi_add_handle(int* multiHandle, int* handle);
void _curl_multi_perform(int* multiHandle, int* left);
void* curl_multi_info_read(int* multiHandle, int* left);
void _curl_multi_remove_handle(int* multiHandle, int* handle); 
void _curl_multi_cleanup(int* multiHandle);

void *__realloc(void *memblock, size_t size);
void* _memcpy( void* dest, const void* src, size_t count );

void _initCurl(){
	int curlOptUrl = 10002;

	_uploadHandle = _curl_easy_init();
	_curl_easy_setopt(_uploadHandle, curlOptUrl, hostUpload);
	_uploadMultiHandle = _curl_multi_init();

	_downloadHandle = _curl_easy_init();
	_curl_easy_setopt(_downloadHandle, curlOptUrl, hostDownload);
	_downloadMultiHandle = _curl_multi_init();
}

void _postCurl(char text[]){
	int curlOptPostFields = 10015;
	int leftRunning = 1;

	_curl_multi_add_handle(_uploadMultiHandle, _uploadHandle);
	_curl_easy_setopt(_uploadHandle, curlOptPostFields, text);
	_curl_multi_perform(_uploadMultiHandle, &leftRunning);
	_curl_multi_remove_handle(_uploadMultiHandle, _uploadHandle);
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
   _memcpy(&(mem->response[mem->size]), data, realsize);
   mem->size += realsize;
   mem->response[mem->size] = 0;
 
   return realsize;
}

char* _getCurl(){
	memory result = { nullptr, 0};
	int leftRunning = 1;
	int curlOptWriteFunction = 20011;
	int curlOptWriteData = 10001;

	_curl_multi_add_handle(_downloadMultiHandle, _downloadHandle);
	_curl_easy_setopt(_downloadHandle, curlOptWriteFunction, _WriteCallback);
	_curl_easy_setopt(_downloadHandle, curlOptWriteData, &result);
	do{
		_curl_multi_perform(_downloadMultiHandle, &leftRunning);
	} while(leftRunning != 0);
	_curl_multi_remove_handle(_downloadMultiHandle, _downloadHandle);
	return result.response;
}

void _cleanupCurl(){
	_curl_easy_cleanup(_uploadHandle);
	_curl_multi_cleanup(_uploadMultiHandle);

	_curl_easy_cleanup(_downloadHandle);
	_curl_multi_cleanup(_downloadMultiHandle);

	_uploadHandle = nullptr;
	_uploadMultiHandle = nullptr;
	_downloadHandle = nullptr;
	_downloadMultiHandle = nullptr;
}
