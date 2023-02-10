// Use https://godbolt.org/ with power gcc.
#include <cstddef>
int _itemListBase; // be especially careful here
char _formatItemText[] = "IT Id=%03x Tp=%02x:";
char _formatItemGearText[]="IT Id=%03x Tp=%02x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x:";

// Start
// declare the required functions here. These need to be located inside your game
int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);
unsigned int** _getItemTypeInfo(int*, int);

void _postCurl(char[]);
// End

char* _postItemList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    for(int type = 1; type < 0x20; type++){
        if(type == 8 || type == 9) continue;
        int * basePtr = &_itemListBase;
        unsigned int* itemListPtr = *_getItemTypeInfo(basePtr, type);
        while(*itemListPtr != 0){
            unsigned int itemId = itemListPtr[0] >> 19;
            if(type < 8 || (type > 9 && type < 0x14)){

                unsigned int skillId1 = ((unsigned short*)itemListPtr)[6] >> 4;
                unsigned int skillId2 = ((unsigned short*)itemListPtr)[7] >> 4;
                unsigned int skillId3 = ((unsigned short*)itemListPtr)[8] >> 4;

                unsigned int upgradeCount1 = ((unsigned short*)itemListPtr)[6] << 0x1C >> 0x1C;
                unsigned int upgradeCount2 = ((unsigned short*)itemListPtr)[7] << 0x1C >> 0x1C;
                unsigned int upgradeCount3 = ((unsigned short*)itemListPtr)[8] << 0x1C >> 0x1C;

                unsigned int augmentId1 = ((unsigned short*)itemListPtr)[9];
                unsigned int augmentId2 = ((unsigned short*)itemListPtr)[10];
                unsigned int augmentId3 = ((unsigned short*)itemListPtr)[11];

                // Be careful you need to rename the after label in the .asm
                stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatItemGearText, itemId, type,
                    skillId1, upgradeCount1, skillId2, upgradeCount2, skillId3, upgradeCount3, augmentId1, augmentId2, augmentId3);
            } else {
                stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatItemText, itemId, type);
            }
            itemListPtr += 0x18;
            if(stringCurrentPtr > stringEndPtr){
                _postCurl(stringStartPtr);
                stringCurrentPtr = stringStartPtr;
            }
        }

    }
    return stringCurrentPtr;
}