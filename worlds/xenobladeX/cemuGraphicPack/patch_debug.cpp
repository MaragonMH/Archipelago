extern int* _menuBasePtr;
void writeSystemLog(int* menuBasePtr, char* str1, char* str2);

void writeDebug(char* output){
	writeSystemLog(_menuBasePtr, "Debug Message", output);
}