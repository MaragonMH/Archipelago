#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

GetGarageDollData = 0x027f7104 # ::Util::DollData
#endif

char _formatDollText[]="DL GIx=%02x Id=%03x Ix=%01x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x Na=%s:";

int GetGarageDollData(int idx, char* result);


// The Equip Item with Ix(Index)=A is the frameId 
// https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_DlList.html
char* _postDollList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	// Do this only for main character for now
    for(int garageIdx = 0; garageIdx < 0x3c; garageIdx++){
		char dollData[0x174];
		if(GetGarageDollData(garageIdx, dollData)){
			for(int equipIdx = 0; equipIdx < 16; equipIdx++){
				unsigned short* dollEquipPtr = (unsigned short*)(dollData + 0x24 + equipIdx * 14);
				if(*dollEquipPtr == 0) continue;
				unsigned int itemId =  dollEquipPtr[0];

				unsigned int skillId1 = dollEquipPtr[1] >> 4;
				unsigned int skillId2 = dollEquipPtr[2] >> 4;
				unsigned int skillId3 = dollEquipPtr[3] >> 4;

				unsigned int upgradeCount1 = dollEquipPtr[1] << 0x1C >> 0x1C;
				unsigned int upgradeCount2 = dollEquipPtr[2] << 0x1C >> 0x1C;
				unsigned int upgradeCount3 = dollEquipPtr[3] << 0x1C >> 0x1C;

				unsigned int augmentId1 = dollEquipPtr[4];
				unsigned int augmentId2 = dollEquipPtr[5];
				unsigned int augmentId3 = dollEquipPtr[6];

				stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatDollText, garageIdx, itemId, equipIdx, skillId1, 
					upgradeCount1, skillId2, upgradeCount2, skillId3, upgradeCount3, augmentId1, augmentId2, augmentId3, dollData);

				if(stringCurrentPtr > stringEndPtr){
					_postCurl(stringStartPtr);
					stringCurrentPtr = stringStartPtr;
				}
			}
		}
    }
	return stringCurrentPtr;
}