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
int _itemListBase;
char* fieldSkillBasePtr;

void _reqMenuAddItemFromId(int type, int id, int count);
void _reqMenuSetArtsLevel(char* characterBasePtr, int id, int lvl, int filler);
void _reqMenuSetSkillsLevel(char* characterBasePtr, int id, int lvl, int filler);
void _SetFriendRank(int id, int lvl);
char* _getClassDataPtr(int id);
unsigned int** _getItemTypeInfo(int*, int);

int * GetCharaDataPtr(int charaId); //::Util
void _setLocal(int width, int position, int value); //::GameFlag
void _addGarage(int* idPtr); // ::CmdCommon::SceneCmdPrm


// 1 = Ground Armor Head			https://xenoblade.github.io/xbx/bdat/common_local_us/AMR_PcList.html
// 2 = Ground Armor Body
// 3 = Ground Armor Arm R
// 4 = Ground Armor Arm L
// 5 = Ground Armor Legs
// 6 = Ground Weapon Ranged			https://xenoblade.github.io/xbx/bdat/common_local_us/WPN_PcList.html
// 7 = Ground Weapon Melee
// 8 = Probably Avatar Creation 	// Don't use
// 9 = Skell Frame					https://xenoblade.github.io/xbx/bdat/common_local_us/DEF_DlList.html (FrameId) => https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_DlList.html
// a = Skell Armor Head				https://xenoblade.github.io/xbx/bdat/common_local_us/AMR_DlList.html
// b = Skell Armor Torso
// c = Skell Armor Arm R
// d = Skell Armor Arm L
// e = Skell Armor Legs
// f = Skell Weapon Back			https://xenoblade.github.io/xbx/bdat/common_local_us/WPN_DlList.html
// 10 = Skell Weapon Shoulder
// 11 = Skell Weapon Shield
// 12 = Skell Weapon Sidearm
// 13 = Skell Weapon Spare
// 14 = Augment Ground Weapon		https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ItemSkill_inner.html
// 15 = Augment Ground Armor
// 16 = Augment Skell Frame			https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ItemSkill_doll.html
// 17 = Augment Skell Weapon
// 18 = Augment Skell Armor
// 19 = Precious Ressources			https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_RareRscList.html
// 1a = Materials					https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_MaterialList.html
// 1b = Collectable					https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_CollectList.html
// 1c = Data Probes					https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_BeaconList.html
// 1d = Important Items				https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_PreciousList.html
// 1e = Appendage Fragments			https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_PieceList.html
// 1f = Consumeable Items			https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_BattleItem.html
void _addItem(int type, int id){
	if(type != 9){
		_reqMenuAddItemFromId(type, id, 1);
	} else {
		_addGarage(&id);
	}
}

int _hasPreciousItem(int id){
	int * basePtr = &_itemListBase;
	unsigned int* itemListPtr = *_getItemTypeInfo(basePtr, 0x1d);
	for(int idx = 0; idx < 300; idx++){
		unsigned int itemType = itemListPtr[0] << 13 >> 26;
		if(itemType != 0x1d) break;
		unsigned int itemId = itemListPtr[0] >> 19;
		if(id == itemId) return 1;
		itemListPtr += 3;
	}
	return 0;
}

// https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_ArtsList.html
void _addArt(int id, int lv){
	int mainCharacterId = 0;
	_reqMenuSetArtsLevel((char*)GetCharaDataPtr(mainCharacterId), id, lv, 0);
}

// https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_SkillClass.html
void _addSkill(int id, int lv){
	int mainCharacterId = 0;
	_reqMenuSetSkillsLevel((char*)GetCharaDataPtr(mainCharacterId), id, lv, 0);
}

// https://xenoblade.github.io/xbx/bdat/common_local_us/DEF_PcList.html
void _addFriend(int id, int lv){
	_SetFriendRank(id, lv);
}

// 1 = Mechanical, 2 = Biological, 3 = Archeological
void _addFieldSkill(int id, int lv){
	char* fieldSkillOffset = fieldSkillBasePtr;
	fieldSkillOffset += 0x48b18; // from updateStatus::menu::MenuTotalSimpleStatus line 413
	fieldSkillOffset += id - 1;
	*fieldSkillOffset = (char)lv;
}

// 1 = Skell License, 2 = Flight Module, 3 = Overdrive, 4 = FNet, 5=Blade
// Some important unlocks are tied to the scenario flag, which is not desired
// Replace all functions with a call to our own for these items
// To anchor them in the savedata we use unused items from the "Important Items" Category
// Specifically 24-31 from https://xenoblade.github.io/xbx/bdat/common_local_us/ITM_PreciousList.html
void _addKey(int id, int flag){
	switch(id){
		case 0:
		// just for debugging purposes
		_setLocal(0x10, 1, flag);
		break;

		case 1:
		// only checked if you buy a doll and not if you assign it
		_setLocal(1, 0x5e5b, flag);
		break;

		case 2:
		// does not work
		_setLocal(1, 0x7610, flag);
		break;

		case 3:
		// only for ground and not for skell
		_setLocal(1, 0x6bc3, flag);
		break;

		case 4:
		// from initialize::fnet::FnetTask where param_1 + 0xe must be 2
		// to accomplish this you need to set the scenerio flag to at least 3001=0xbb9
		// https://xenoblade.github.io/xbx/bdat/common_local_us/FnetVeinConfig.html value at idx 8
		// the game is unable to unload during runtime so you need to save and restart to unset
		_addItem(0x1d, 24);
		break;

		case 5:
		// same as FNet
		// but here you need at least 3002
		_addItem(0x1d, 25);
		break;
	}
}

// https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_ClassInfo.html
void _addClass(int id, int lv){
	*_getClassDataPtr(id) = (char)lv;
}
