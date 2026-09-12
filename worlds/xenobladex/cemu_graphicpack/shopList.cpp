#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef ALL
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

GetKnowledgePtr = 0x027fb934
GetBlueprintPtr = 0x027fbae4
#endif

char _formatShopText[] = "SH Id=%03x Tp=%01x:";

char* GetKnowledgePtr();
char* GetBlueprintPtr();

// Use https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ItemSkill_inner.html +
// https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ItemSkill_doll.html to match the ids
// use the embedded remaining bits of the "new" item in savedata
char* _postShopList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	for(int id = 1; id < 200; id++){
		// 0=disabled, 1=visible, 2=new, 3=crafted
		char* blueprintPtr = GetBlueprintPtr();
		int blueprintFlag = (int)*(blueprintPtr + id);

		if (blueprintFlag == 3)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0x6);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
	}
	
    for(int id = 1; id < 4000; id++){
		char* knowledgePtr = GetKnowledgePtr();
		int dollOffset = 0x4ba4;  // type 0x4d
		int groundOffset = 0x3c04; // type 0x4c
		int dollFlag = (int)*(knowledgePtr + dollOffset + id);
		int groundFlag = (int)*(knowledgePtr + groundOffset + id);
		// Augments 0x02
		int dollAugmentFlag = dollFlag & 0x02;
		int groundAugmentFlag = groundFlag & 0x02;
		// Weapons 0x04
		int dollWeaponFlag = dollFlag & 0x04;
		int groundWeaponFlag = groundFlag & 0x04;
		// Armor 0x08
		int dollArmorFlag = dollFlag & 0x08;
		int groundArmorFlag = groundFlag &= 0x8;
		// Frame 0x10
		int dollFrameFlag = dollFlag & 0x10;


		if (groundArmorFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0x7);
		if (groundWeaponFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0x8);
		if (groundAugmentFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0x9);
		if (dollArmorFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0xa);
		if (dollWeaponFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0xb);
		if (dollAugmentFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0xc);
		if (dollFrameFlag != 0)
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatShopText, id, 0xd);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
    }
	return stringCurrentPtr;
}