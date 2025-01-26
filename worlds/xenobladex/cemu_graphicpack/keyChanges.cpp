#include <cstddef>

int _hasPreciousItem(int id);

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E
0x021b70bc = bl _IsPermit # replace getLocal inside IsPermit with new check
0x02b051a4 = bl _assignDollCheck # replace lvlCheck with dollLicense + lvlCheck
0x02b051c4 = nop # remove original error message
0x022e9920 = nop # restructure online skell flight module check to always use this one
0x022e9934 = bl _loadSkyUnit # replace online skell flight module call with own
0x027d6da0 = bl _loadFNet # replace getScenarioFlag for initial load
0x027d5748 = blr # return original call to changeScenarioFlag Fnet

0x022e2c24 = nop # dont set all the arts/skills/classes if you change your Class
0x020c48c4 = blr # disable Class exp
0x020c63d8 = blr # disable friend exp

# remove all equipment for new playable characters
0x027e2100 = blr # armor
0x027e44e8 = bl _getDefaultWeapon
0x027e4558 = bl _getDefaultWeapon

# remove arts/skills for new playable characters
0x026a52e8 = blr # disable OpenArts::CharacterData
0x026a5308 = blr # disable OpenSkills::CharacterData
0x027e41f8 = b 0x027e4334 # disable automatic skill asignment

# remove all equipment for new skells
0x027e2110 = blr # armor
0x027e2108 = blr # weapon

# filter quest rewards
0x0229572c = bl _addRewardItemEquipment
0x022957c4 = bl _addRewardItemEquipment
0x0229585c = bl _addRewardItemEquipment
0x022958f4 = bl _addRewardItemEquipment
# filter treasure box rewards
0x022d8d50 = bl _addRewardItemEquipment
# filter enemy rewards
0x02b07540 = bl _getItemNumAdjusted
0x02b076d4 = b _preItemLoopAdjustment
_itemLoopStart = 0x02b07584
_itemLoopEnd = 0x02b076e8

# disable field skills
0x0238e138 = nop

# disable affinity quest arts reward
0x029c7dc0 = li r3,0

# reconfigure BladeTerminal Locks
bladeTerminalScenarioFlagPtr = 0x20343604
shopTerminalScenarioFlagPtr = 0x20343634
0x02814cf4 = b _prepareBladeTerminal # in loadEnd::ScriptManager

# reconfigure rentalCharTerminal to LShop
__strcmp = 0x03b16c50
0x028eacc8 = bl _prepareRentalCharTerminal
beginScript = 0x028cb70c # ::Gimmick::GimmickMapObj

# mandatory disable shops
0x02a32770 = nop # skell frame
0x02a69954 = nop # augment menu
0x02a69968 = nop # develop menu
# optional shops # need paramaterization
0x02a326d0 = nop # ground weapon
0x02a326f8 = nop # ground armor
0x02a32720 = nop # skell weapon
0x02a32748 = nop # skell armor

# overwrite setLocal for blade flag
0x0228f018 = bl _setLocal

menuBasePtr = 0x1038ae50 # from error::menu::BladeHomeMenu
openHudTelop = 0x02c91f3c # ::MenuTask
chkLv = 0x02af8e7c # ::menu::MenuDollGarage
addItemEquipment = 0x02366cf0 # ::ItemBox::ItemType::Type::ItemHandle
getItem = 0x021ab180 # ::ItemDrop::ItemDropManager
getItemNum = 0x021ab164 # ::ItemDrop::ItemDropManager
#endif

// Parameters from rules.txt
int disableGroundArmor, disableGroundWeapons, disableSkellArmor, disableSkellWeapons, disableGroundAugments, disableSkellAugments;

extern int* menuBasePtr;
extern int bladeTerminalScenarioFlagPtr, shopTerminalScenarioFlagPtr;
extern void* _itemLoopStart;
extern void* _itemLoopEnd;

int __strcmp (const char* str1, const char* str2);
int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

int* getFP(const char* bdat);
int getValCheck(int* bdatPtr, const char* columnName, int id, int offset);

void openHudTelop(int* menuBasePtr, int errorIdx);
int chkLv(int p1, int p2);

int addItemEquipment(int type, int id, int* data, int flag);

int* getItem(int* ptr, int enemies, int boxes, int items);
int getItemNum(int* ptr, int enemies, int boxes);

int beginScript(int** scriptPtr);


int _IsPermit(){
	return _hasPreciousItem(24 + 3 - 1);
}

int _assignDollCheck(int p1, int p2){
	if(!_hasPreciousItem(24 + 1 - 1)){
		// display error message for missing skell license
		// check https://xenoblade.github.io/xbx/bdat/common_local_us/MNU_CommonTelop.html
		// -> https://xenoblade.github.io/xbx/bdat/common_ms/MNU_CommonTelop_ms.html
		openHudTelop(menuBasePtr, 12);
		return 0;
	}
	if(chkLv(p1,p2) == 0){	
		openHudTelop(menuBasePtr, 0x1ae);
		return 0;
	}
	return 1;
}

// overwrite starting weapon with default weapon
// from https://xenoblade.github.io/xbx/bdat/common_local_us/DEF_PcList.html for Weapon calls
// take class instead and match https://xenoblade.github.io/xbx/bdat/common_local_us/CHR_ClassInfo.html#30
// to get default weapon
int _getDefaultWeapon(int* DEF_PcList_bdat, char weaponColumn[], int charId, int offset){
	int* bdatPtr = getFP("CHR_ClassInfo");
	int classId = getValCheck(DEF_PcList_bdat, "ClassType", charId, 1) >> 0x18;
	// convert DefWpnFar -> FarWeapon
	char newWeaponColumn[0x20];
	char* weaponType = weaponColumn + 6; 
	__sprintf_s(newWeaponColumn, 0x20, "%sWeapon", weaponType);
	return getValCheck(bdatPtr, newWeaponColumn, classId, 1) >> 0x8;
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

int _addRewardItemEquipment(int type, int id, int* data, int flag){
	if(_checkType(type)){
		return addItemEquipment(type, id, data, flag);
	}
	return 0;
}

int _getItemNumAdjusted(int* ptr, int enemies, int boxes){
	int count = 0;
	int num = getItemNum(ptr, enemies, boxes);
	for(int i = 0; i < num; i++){
		int itemType = *(char*)getItem(ptr, enemies, boxes, i);
		if(_checkType(itemType)) count++;
	}
	return count;
}
int _itemLoopAdjustment(int* ptr, int enemies, int boxes, int idx, int offset){
	int type = *(char*)getItem(ptr, enemies, boxes, idx);
	if(_checkType(type)) offset += 0x1c;
	return offset;
}
int _itemLoopContinue(int* ptr, int enemies, int boxes, int idx){
	int num = getItemNum(ptr, enemies, boxes);
	if(idx < num) return 1;
	return 0;
}

void _prepareBladeTerminal(){
	if(bladeTerminalScenarioFlagPtr == 3001){
		if(_hasPreciousItem(24 + 5 - 1)) bladeTerminalScenarioFlagPtr = 0;
		else bladeTerminalScenarioFlagPtr = 0x7fffff;
	}
	if(shopTerminalScenarioFlagPtr == 2001){
		if(_hasPreciousItem(24 + 5 - 1)) shopTerminalScenarioFlagPtr = 0;
		else shopTerminalScenarioFlagPtr = 0x7fffff;
	}
}

int _prepareRentalCharTerminal(int** scriptPtr){
	int* fldConsoleParamPtr = scriptPtr[0x29];
	if(__strcmp((char*)fldConsoleParamPtr,"fld_console.sb")) return beginScript(scriptPtr);
	int fldConsoleScriptId = fldConsoleParamPtr[9];
	if(fldConsoleScriptId == 2){
		if(_hasPreciousItem(24 + 5 - 1)) return beginScript(scriptPtr + 0x98);
		else {
			openHudTelop(menuBasePtr, 52);
			return 0; // does not matter
		}
	} 
	if(fldConsoleScriptId == 0xb) return beginScript(scriptPtr - 0x98);
	return beginScript(scriptPtr);
}

// Do not call this function directly, but rather call the first label
// Intellisense works only properly with g++ as a compiler 
// https://code.visualstudio.com/docs/cpp/configure-intellisense-crosscompilation#_compiler-path
void _preItemLoopAdjustmentWrapper(){
	asm(".global _preItemLoopAdjustment:");
	asm ("_preItemLoopAdjustment:");
    register int boxNum asm("r22");
    register int dropNum asm("r20");
    register int idx asm("r18");
    register int* ptr asm("r31");
    register int offset asm("r23");
	offset = _itemLoopAdjustment(ptr, boxNum, dropNum, idx, offset);
	int value = _itemLoopContinue(ptr, boxNum, dropNum, idx);
	idx++;
	if(value == 0) goto *&_itemLoopEnd;
	goto *&_itemLoopStart;
}

// Overwrite the unlock BladeLvl flag from add.cpp
void _setLocal(const int width, const int position){
	register int value asm("r5");
	if(width == 2 && value == 1){
		if(position == 0x1288 || position == 0x1286)
			value = 0;
	}

	// original instruction from 0x0228f018
	asm("lis r9, 0x103a");
	return;
}
