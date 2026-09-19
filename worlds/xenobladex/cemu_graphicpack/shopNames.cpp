#include <cstddef>

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

0x02a2d2c8 = bl _getShopWeaponName
0x02a2e260 = bl _getShopArmorName
0x02a2f8f0 = bl _getShopDollArmorName
0x02a2eef8 = bl _getShopDollWeaponName
#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

0x02a2d2b8 = bl _getShopWeaponName
0x02a2e250 = bl _getShopArmorName
0x02a2f8e0 = bl _getShopDollArmorName
0x02a2eee8 = bl _getShopDollWeaponName
#endif

extern char** _shopArmorNames;
extern char ** _shopWeaponNames;
extern char ** _shopDollArmorNames;
extern char ** _shopDollWeaponNames;
extern char ** _shopDollFrameNames;
extern char ** _shopAugmentNames;
extern char ** _shopDollAugmentNames;
extern char ** _shopBlueprintNames;

extern int includeShopBlueprints;
extern int includeShopArmor;
extern int includeShopWeapons;
extern int includeShopAugments;
extern int includeShopSkellArmor;
extern int includeShopSkellWeapons;
extern int includeShopSkellAugments;
extern int includeShopSkellFrames;

int _getShopIdx(const char* bdat_name, int itemId, bool dropLastColumn = false);
int getVal(int* bdatPtr, const char* columnName, int id);

char* _getShopName(char** shopPtr, int id, int enabled){
    if(!enabled) return nullptr;
    if(shopPtr == nullptr || shopPtr[id] == nullptr) return nullptr;
    return shopPtr[id];
}

char* _getShopArmorName(int* bdatPtr, const char* columnName, int id){
    register int itemId asm("r22");
    char* name = _getShopName(_shopArmorNames, _getShopIdx("SHP_AmrPC", itemId), includeShopArmor);
    if (name == nullptr)
        return (char *)getVal(bdatPtr, columnName, id);
    return name;
}
char* _getShopWeaponName(int* bdatPtr, const char* columnName, int id){
    register int itemId asm("r23");
    char* name = _getShopName(_shopWeaponNames, _getShopIdx("SHP_WpnPC", itemId, true), includeShopWeapons);
    if (name == nullptr)
        return (char *)getVal(bdatPtr, columnName, id);
    return name;
}
char* _getShopDollFrameName(int* bdatPtr, const char* columnName, int id){
    register int itemId asm("r5");
    char* name = _getShopName(_shopDollFrameNames, itemId, includeShopSkellFrames);
    if (name == nullptr)
        return (char *)getVal(bdatPtr, columnName, id);
    return name;
}
char* _getShopAugmentName(int* bdatPtr, const char* columnName, int id){
    register int itemId asm("r5");
    char* name = _getShopName(_shopAugmentNames, itemId, includeShopAugments);
    if (name == nullptr)
        return (char *)getVal(bdatPtr, columnName, id);
    return name;
}
char* _getShopDollArmorName(int* bdatPtr, const char* columnName, int id){
    register int itemId asm("r21");
    char* name = _getShopName(_shopDollArmorNames, _getShopIdx("SHP_AmrDL", itemId), includeShopSkellArmor);
    if (name == nullptr)
        return (char *)getVal(bdatPtr, columnName, id);
    return name;
}
char* _getShopDollWeaponName(int* bdatPtr, const char* columnName, int id){
    register int itemId asm("r25");
    char* name = _getShopName(_shopDollWeaponNames, _getShopIdx("SHP_WpnDL", itemId), includeShopSkellWeapons);
    if (name == nullptr)
        return (char *)getVal(bdatPtr, columnName, id);
    return name;
}
char* _getShopDollAugmentName(int* bdatPtr, const char* columnName, int id){
    register int itemId asm("r5");
    char* name = _getShopName(_shopDollAugmentNames, itemId, includeShopSkellAugments);
    if (name == nullptr)
        return (char *)getVal(bdatPtr, columnName, id);
    return name;
}
char* _getShopBlueprintName(int* bdatPtr, const char* columnName, int id){
    register int itemId asm("r5");
    char* name = _getShopName(_shopBlueprintNames, itemId, includeShopBlueprints);
    if (name == nullptr)
        return (char *)getVal(bdatPtr, columnName, id);
    return name;
}