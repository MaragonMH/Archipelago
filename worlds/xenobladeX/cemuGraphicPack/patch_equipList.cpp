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
// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/TWN_FriendRank.html to match the ids
// Ranges from 0 to 50, but 32 is already 5 hearts???
#include <cstddef>
char _formatEquipText[]="EQ CId=%03x Id=%03x Ix=%01x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x:"; // First %05x Second %05x Third %05x Fourth %05x Fifth %05x Sixth %05x Seventh %05x:";

// Start
// declare the required functions here. These need to be located inside your game
// IMPORTANT: If you get the "target NAME out of range" exception, use two leading "_"

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

int * _getInnerEquipmentData(char* characterPtr, int equipPosition); // ::menu::MenuEquipUtil::PCData
int * GetCharaDataPtr(int charaId); //::Util
// End

void _postCurl(char[]);

char* _postEquipList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	// Do this only for main character for now
    for(int characterId = 0; GetCharaDataPtr(characterId) != 0; characterId++){
		char* characterPtr = (char*)GetCharaDataPtr(characterId);
		 
		for(int equipPosition = 0; equipPosition < 0xc; equipPosition++){
			unsigned int* equipPtr = (unsigned int*)_getInnerEquipmentData(characterPtr, equipPosition);
			if(*equipPtr == 0) continue;
			unsigned int itemId =  ((unsigned short*)equipPtr)[0];

			unsigned int skillId1 = ((unsigned short*)equipPtr)[1] >> 4;
			unsigned int skillId2 = ((unsigned short*)equipPtr)[2] >> 4;
			unsigned int skillId3 = ((unsigned short*)equipPtr)[3] >> 4;

			unsigned int upgradeCount1 = ((unsigned short*)equipPtr)[1] << 0x1C >> 0x1C;
			unsigned int upgradeCount2 = ((unsigned short*)equipPtr)[2] << 0x1C >> 0x1C;
			unsigned int upgradeCount3 = ((unsigned short*)equipPtr)[3] << 0x1C >> 0x1C;

			unsigned int augmentId1 = ((unsigned short*)equipPtr)[4];
			unsigned int augmentId2 = ((unsigned short*)equipPtr)[5];
			unsigned int augmentId3 = ((unsigned short*)equipPtr)[6];

			// Be careful you need to rename the after label in the .asm
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatEquipText, characterId, itemId, equipPosition,
				skillId1, upgradeCount1, skillId2, upgradeCount2, skillId3, upgradeCount3, augmentId1, augmentId2, augmentId3);

			if(stringCurrentPtr > stringEndPtr){
				_postCurl(stringStartPtr);
				stringCurrentPtr = stringStartPtr;
			}
		}
    }
	return stringCurrentPtr;
}