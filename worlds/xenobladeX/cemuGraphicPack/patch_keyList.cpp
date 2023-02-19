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
// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_EnBook.html to match the ids
// Defeat: Number of enemies you defeated
// Discovery(Dc): 0, 1, 2. 0 = Not discovered yet (will appear as ??? in menu), 1 = encountered in combat, 2 = fully researched (white dot in menu)
#include <cstddef>
extern int** fnetBasePtr;
extern int* _menuBasePtr;
extern int _charaHasDied;

// Start
// declare the required functions here. These need to be located inside your game
// IMPORTANT: If you get the "target NAME out of range" exception, use two leading "_"

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

// bool IsDollLicense(); // ::menu::MenuArmsCompany
// bool IsPermit(); // ::Gear::Gear // Overdrive
int getLocal(int width, int position);
int _hasPreciousItem(int id);
// End

void _postCurl(char[]);

char* _postKeyList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    for(int keyId = 0; keyId < 6; keyId++){
		int flag = 0;

		// just for debugging purposes
		if(keyId == 0) flag = getLocal(0x10, 1);
		else if(keyId == 6){
			if (_charaHasDied) _charaHasDied = 0;
			else continue;
		}
		// 1: flag = IsDollLicense();
		// 2: flag = getLocal(1, 0x7610); // from int getFlightUnitFlag(); // ::SquadUtil
		// 3: flag = IsPermit();
		else _hasPreciousItem(24 + keyId - 1);

		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, "KY Id=%01x Fg=%01x:", keyId, flag);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
    }
	return stringCurrentPtr;
}

int _request(int* requestCtrlPtr, int code, int placeholder);
void writeDebug(char* output);
int _notifyDead(int* requestCtrlPtr, int code, int placeholder){
	int* backupRequestCtrlPtr = requestCtrlPtr;
	asm("stw 29,24(31)");
	if(code == 0x2e && *requestCtrlPtr == 0x100){ 
		_charaHasDied = 1;
		writeDebug("Sending Death");
	}
	return _request(backupRequestCtrlPtr, code, placeholder);
}