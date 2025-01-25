extern int* menuBasePtr;

void writeSystemLog(int* menuBasePtr, const char* str1, const char* str2);

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E
#endif

void _writeDebug(const char* output){
	writeSystemLog(menuBasePtr, "Debug Message", output);
}