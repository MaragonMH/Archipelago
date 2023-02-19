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
extern int disableGroundArmor, disableGroundWeapons, disableSkellArmor, disableSkellWeapons, disableGroundAugments, disableSkellAugments;
extern int* _menuBasePtr;
int _hasPreciousItem(int id);
void _openHudTelop(int* menuBasePtr, int errorIdx);
int _chkLvl(int p1, int p2);

int _IsPermit(){
	return _hasPreciousItem(24 + 3 - 1);
}

int _assignDollCheck(int p1, int p2){
	if(!_hasPreciousItem(24 + 1 - 1)){
		// display error message for missing skell license
		// check https://xenoblade.github.io/xbx/bdat/common_local_us/MNU_CommonTelop.html
		// -> https://xenoblade.github.io/xbx/bdat/common_ms/MNU_CommonTelop_ms.html
		_openHudTelop(_menuBasePtr, 12);
		return 0;
	}
	if(_chkLvl(p1,p2) == 0){	
		_openHudTelop(_menuBasePtr, 0x1ae);
		return 0;
	}
	return 1;
}

// keep in mind that you need to reload your skell to trigger this
// best way is to go into active members and press confirm once
int _loadSkyUnit(){
	return _hasPreciousItem(24 + 2 - 1);
}

int _loadFNet(){
	return _hasPreciousItem(24 + 4 - 1) * 3001;
}

int _checkType(int type){
	// use this for now, but use options later
	if(type >= 0x1 && type <= 0x5) return disableGroundArmor;
	if(type >= 0x6 && type <= 0x7) return disableGroundWeapons;
	if(type >= 0xa && type <= 0xe) return disableSkellArmor;
	if(type >= 0xf && type <= 0x13) return disableSkellWeapons;
	if(type >= 0x14 && type <= 0x15) return disableGroundAugments;
	if(type >= 0x16 && type <= 0x18) return disableSkellAugments;
	if(type >= 0x18 && type != 0x1c) return 1;
	return 0;
}

int _addItemEquipment(int type, int id, int* data, int flag);
int _addRewardItemEquipment(int type, int id, int* data, int flag){
	if(_checkType(type)){
		return _addItemEquipment(type, id, data, flag);
	}
	return 0;
}

int _getItemNum(int* ptr, int enemies, int boxes);
int* _getItem(int* ptr, int enemies, int boxes, int items);
int _getItemNumAdjusted(int* ptr, int enemies, int boxes){
	int count = 0;
	int num = _getItemNum(ptr, enemies, boxes);
	for(int i = 0; i < num; i++){
		int itemType = *(char*)_getItem(ptr, enemies, boxes, i);
		if(_checkType(itemType)) count++;
	}
	return count;
}
int _itemLoopAdjustment(int* ptr, int enemies, int boxes, int idx, int offset){
	int type = *(char*)_getItem(ptr, enemies, boxes, idx);
	if(_checkType(type)) offset += 0x1c;
	return offset;
}
int _itemLoopContinue(int* ptr, int enemies, int boxes, int idx){
	int num = _getItemNum(ptr, enemies, boxes);
	if(idx < num) return 1;
	return 0;
}

extern int _bladeTerminalScenarioFlagPtr, _shopTerminalScenarioFlagPtr;
void _prepareBladeTerminal(){
	if(_bladeTerminalScenarioFlagPtr == 3001){
		if(_hasPreciousItem(24 + 5 - 1)) _bladeTerminalScenarioFlagPtr = 0;
		else _bladeTerminalScenarioFlagPtr = 0x7fffff;
	}
	if(_shopTerminalScenarioFlagPtr == 2001){
		if(_hasPreciousItem(24 + 5 - 1)) _shopTerminalScenarioFlagPtr = 0;
		else _shopTerminalScenarioFlagPtr = 0x7fffff;
	}
}

int __strcmp (const char* str1, const char* str2);
int _beginScript(int** scriptPtr);
int _prepareRentalCharTerminal(int** scriptPtr){
	int* fldConsoleParamPtr = scriptPtr[0x29];
	if(__strcmp((char*)fldConsoleParamPtr,"fld_console.sb")) return _beginScript(scriptPtr);
	int fldConsoleScriptId = fldConsoleParamPtr[9];
	if(fldConsoleScriptId == 2) return _beginScript(scriptPtr + 0x98);
	if(fldConsoleScriptId == 0xb) return _beginScript(scriptPtr - 0x98);
	return _beginScript(scriptPtr);
}
