#include <cstddef>

extern int* segmentBasePtr;

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

checkDP = 0x027d346c # ::fnet::FnetDataAccesor
#endif

char _formatFnNodeText[] = "FN Id=%03x Fg=%01x AId=%02x:";

int checkDP(short id);


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/SEG_NormalList.html to match the ids
char* _postFnNodeList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    int* areaOffset = segmentBasePtr;
    areaOffset += 0x4;
    for(int areaId = 0; areaId < 0x15; areaId++){
        for(int* fnNodeOffset = areaOffset + 0x4; *fnNodeOffset != 0; fnNodeOffset += 0x7){
            int nodeId = (short)fnNodeOffset[2];
            int flag = checkDP(nodeId);
			int type = fnNodeOffset[1] >> 0x18;

            if(type != 1) continue;

            stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatFnNodeText, nodeId, flag, areaId);

            // Reset buffer
            if(stringCurrentPtr > stringEndPtr){
                _postCurl(stringStartPtr);
                stringCurrentPtr = stringStartPtr;
            }
        }
        areaOffset += 0x7f7;
    }
    return stringCurrentPtr;
}