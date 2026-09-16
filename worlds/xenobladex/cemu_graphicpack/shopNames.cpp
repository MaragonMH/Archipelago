#include <cstddef>

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

#endif

#ifdef V102U
moduleMatches = 0x30B6E091 ; 1.0.2U

#endif

extern char** _shopArmorNames;
extern char ** _shopWeaponNames;
extern char ** _shopDollArmorNames;
extern char ** _shopDollWeaponNames;
extern char ** _shopDollFrameNames;
extern char ** _shopAugmentNames;
extern char ** _shopDollAugmentNames;
extern char ** _shopBlueprintNames;

char* _getShopArmorName(){
    register int id asm("r5");
    return _shopArmorNames[id];
}
char* _getShopWeaponName(){
    register int id asm("r5");
    return _shopWeaponNames[id];
}
char* _getShopDollFrameName(){
    register int id asm("r5");
    return _shopDollFrameNames[id];
}
char* _getShopAugmentName(){
    register int id asm("r5");
    return _shopAugmentNames[id];
}
char* _getShopDollArmorName(){
    register int id asm("r5");
    return _shopDollArmorNames[id];
}
char* _getShopDollWeaponName(){
    register int id asm("r5");
    return _shopDollWeaponNames[id];
}
char* _getShopDollAugmentName(){
    register int id asm("r5");
    return _shopDollAugmentNames[id];
}
char* _getShopBlueprintName(){
    register int id asm("r5");
    return _shopBlueprintNames[id];
}