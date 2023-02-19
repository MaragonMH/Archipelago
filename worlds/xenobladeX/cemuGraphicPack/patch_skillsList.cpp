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
// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_SkillClass.html to match the ids
#include <cstddef>
char _formatSkillsText[] = "SK Id=%02x Lv=%01x:";  // First %05x Second %05x Third %05x Fourth %05x Fifth %05x Sixth %05x Seventh %05x:";

// Start
// declare the required functions here. These need to be located inside your game
// IMPORTANT: If you get the "target NAME out of range" exception, use two leading "_"

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

int * GetCharaDataPtr(int charaId); //::Util
// End

void _postCurl(char[]);

char* _postSkillsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	// Do this only for main character for now
    for(int characterId = 0; characterId < 0x1; characterId++){
		char* characterBasePtr = (char*)GetCharaDataPtr(characterId);

		for(int skillId = 1; skillId < 95; skillId++){

			int level = *(characterBasePtr + skillId + 0x478); // from GetSkillsLevel::Menu::MenuSkillSet
			// option to log character name with characterBasePtr and %s in format string
			// option to log character id with characterId and %02x in format string
			stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatSkillsText, skillId, level);

			// Reset buffer
			if(stringCurrentPtr > stringEndPtr){
				_postCurl(stringStartPtr);
				stringCurrentPtr = stringStartPtr;
			}
		}

    }
	return stringCurrentPtr;
}