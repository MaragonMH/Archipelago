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
#include <cstddef>
int* _menuBasePtr;
int changeTime(int hour, int minute);
void writeSystemLog(int* menuBasePtr, char* str1, char* str2);

void* __malloc (size_t size);
void __free (void* ptr);
long int __strtol (const char* str, char** endptr, int base);

void _initCurl();
void _postCurl(char[]);
char* _getCurl();
void _cleanupCurl();

void _addItem(int type, int id);
void _addArt(int id, int lv);
void _addSkill(int id, int lv);
void _addFriend(int id, int lv);
void _addFieldSkill(int id, int lv);
void _addKey(int id, int flag);
void _addClass(int id, int lv);

char* _postArtsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postClassList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postCollepediaList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postEnemyList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postFieldSkillsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postFnNodeList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postFriendList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postItemList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postLocationList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postSegmentList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postSkillsList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postKeyList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postEquipList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postDollList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);
char* _postVeinList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize);

void _free(void * ptr){
	__free(ptr);
}
long int _strtol(const char* str, char** endptr, int base){
	return __strtol(str, endptr, base);
}

void _postArchipelago(){
	int allocBufferSize = 0xFFFF;
	int maxEntrySize = 0x100;

    char* stringStartPtr = (char*)__malloc(allocBufferSize);
    char* stringCurrentPtr = stringStartPtr;
	char* stringEndPtr = stringStartPtr + allocBufferSize - maxEntrySize;

	stringCurrentPtr[0] = '^';
	stringCurrentPtr++;

	stringCurrentPtr = _postArtsList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postClassList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postCollepediaList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postEnemyList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postFieldSkillsList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postFnNodeList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postFriendList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postItemList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postLocationList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postSegmentList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postSkillsList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postKeyList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postEquipList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postDollList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);
	stringCurrentPtr = _postVeinList(stringStartPtr, stringCurrentPtr, stringEndPtr, maxEntrySize);

	stringCurrentPtr[0] = '$';
	stringCurrentPtr[1] = 0;

	_postCurl(stringStartPtr);

    _free(stringStartPtr);
}

void _getArchipelago(){
	char* outputPtr = _getCurl();
	if (outputPtr == nullptr) return;

	char* outputCurrentPtr = outputPtr;
	while(*outputCurrentPtr != 0){
		switch(*outputCurrentPtr){
			case 'I': // Item
			// Identification Character + Prefix + Type + Prefix + Id
			{
				outputCurrentPtr += 1 + 4;
				int itemType = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8 + 4;
				int itemId = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8;
				_addItem(itemType, itemId);
			}
			break;

			case 'A': // Art
			// Identification Character + Prefix + Id + Prefix + Lvl
			{
				outputCurrentPtr += 1 + 4; 
				int artId = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8 + 4;
				int artLv = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8;
				_addArt(artId, artLv);
			}
			break;

			case 'S': // Skill
			// Identification Character + Prefix + Id + Prefix + Lvl
			{
				outputCurrentPtr += 1 + 4; 
				int skillId = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8 + 4;
				int skillLv = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8;
				_addSkill(skillId, skillLv);
			}
			break;

			case 'F': // Friend
			// Identification Character + Prefix + Id + Prefix + Rank
			{
				outputCurrentPtr += 1 + 4; 
				int friendId = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8 + 4;
				int friendRk = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8;
				_addFriend(friendId, friendRk);
			}
			break;

			case 'D': // Debris Skill (Field Skill)
			// Identification Character + Prefix + Id + Prefix + Lvl
			{
				outputCurrentPtr += 1 + 4; 
				int fieldSkillId = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8 + 4;
				int fieldSkillLv = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8;
				_addFieldSkill(fieldSkillId, fieldSkillLv);
			}
			break;

			case 'K': // Key Items
			// Identification Character + Prefix + Id + Prefix + Flag
			{
				outputCurrentPtr += 1 + 4; 
				int keyId = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8 + 4;
				int keyFlag = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8;
				_addKey(keyId, keyFlag);
			}
			break;

			case 'C': // Class
			// Identification Character + Prefix + Id + Prefix + Lvl
			{
				outputCurrentPtr += 1 + 4; 
				int classId = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8 + 4;
				int classLv = (int)_strtol(outputCurrentPtr, NULL, 16);
				outputCurrentPtr += 8;
				_addClass(classId, classLv);
			}
			break;

			case 'M': // Message
			{
				outputCurrentPtr += 1 + 1;
				char* messageHead = outputCurrentPtr;
				while(*outputCurrentPtr != '\n') outputCurrentPtr++;
				*outputCurrentPtr = 0;
				outputCurrentPtr++;
				char* messageBody = outputCurrentPtr;
				while(*outputCurrentPtr != '\n') outputCurrentPtr++;
				*outputCurrentPtr = 0;
				outputCurrentPtr++;
				writeSystemLog(_menuBasePtr, messageHead, messageBody);
			}
			break;

			case '\n':
			outputCurrentPtr++;
			break;

			default:
			_free(outputPtr);
			return;
		}
	}
	_free(outputPtr);
}

int _mainArchipelago(int hour, int minute) {
	if(minute % 3 != 0) return changeTime(hour, minute);
	
	_initCurl();

	_getArchipelago();
	_postArchipelago();

    _cleanupCurl();

	return changeTime(hour, minute);
}