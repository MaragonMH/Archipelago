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
// The Equip Item with Ix(Index)=A is the frameId 
// https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_DlList.html
#include <cstddef>
char _formatDollText[]="DL GIx=%02x Id=%03x Ix=%01x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x Na=%s:"; // First %05x Second %05x Third %05x Fourth %05x Fifth %05x Sixth %05x Seventh %05x:";

// Start
// declare the required functions here. These need to be located inside your game
// IMPORTANT: If you get the "target NAME out of range" exception, use two leading "_"

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

int GetGarageDollData(int idx, char* result); // ::Util::DollData
// End

void _postCurl(char[]);

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

				// Be careful you need to rename the after label in the .asm
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