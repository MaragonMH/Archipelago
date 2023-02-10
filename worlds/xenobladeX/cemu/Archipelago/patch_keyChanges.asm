[XCX_Archipelago_keyChanges]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_IsPermit:
        stwu r1,-16(r1)
        mflr r0
        stw r0,20(r1)
        stw r31,12(r1)
        mr r31,r1
        li r3,26
        bl _hasPreciousItem
        mr r9,r3
        mr r3,r9
        addi r11,r31,16
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_assignDollCheck:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        stw r4,12(r31)
        li r3,24
        bl _hasPreciousItem
        mr r9,r3
        cntlzw r9,r9
        srwi r9,r9,5
        cmpwi cr0,r9,0
        beq cr0,_keyChanges_L4
        lis r9,_menuBasePtr@ha
        lwz r9,_menuBasePtr@l(r9)
        li r4,12
        mr r3,r9
        bl _openHudTelop
        li r9,0
        b _keyChanges_L5
_keyChanges_L4:
        lwz r4,12(r31)
        lwz r3,8(r31)
        bl _chkLvl
        mr r9,r3
        cntlzw r9,r9
        srwi r9,r9,5
        cmpwi cr0,r9,0
        beq cr0,_keyChanges_L6
        lis r9,_menuBasePtr@ha
        lwz r9,_menuBasePtr@l(r9)
        li r4,430
        mr r3,r9
        bl _openHudTelop
        li r9,0
        b _keyChanges_L5
_keyChanges_L6:
        li r9,1
_keyChanges_L5:
        mr r3,r9
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_loadSkyUnit:
        stwu r1,-16(r1)
        mflr r0
        stw r0,20(r1)
        stw r31,12(r1)
        mr r31,r1
        li r3,25
        bl _hasPreciousItem
        mr r9,r3
        mr r3,r9
        addi r11,r31,16
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_loadFNet:
        stwu r1,-16(r1)
        mflr r0
        stw r0,20(r1)
        stw r31,12(r1)
        mr r31,r1
        li r3,27
        bl _hasPreciousItem
        mr r9,r3
        mulli r9,r9,3001
        mr r3,r9
        addi r11,r31,16
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_checkType:
        stwu r1,-32(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        lwz r9,8(r31)
        cmpwi cr0,r9,24
        ble cr0,_keyChanges_L12
        lwz r9,8(r31)
        cmpwi cr0,r9,28
        beq cr0,_keyChanges_L12
        li r9,1
        b _keyChanges_L13
_keyChanges_L12:
        li r9,0
_keyChanges_L13:
        mr r3,r9
        addi r11,r31,32
        lwz r31,-4(r11)
        mr r1,r11
        blr
_addRewardItemEquipment:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        stw r4,12(r31)
        stw r5,16(r31)
        stw r6,20(r31)
        lwz r3,8(r31)
        bl _checkType
        mr r9,r3
        addic r10,r9,-1
        subfe r9,r10,r9
        cmpwi cr0,r9,0
        beq cr0,_keyChanges_L15
        lwz r6,20(r31)
        lwz r5,16(r31)
        lwz r4,12(r31)
        lwz r3,8(r31)
        bl _addItemEquipment
        mr r9,r3
        b _keyChanges_L16
_keyChanges_L15:
        li r9,0
_keyChanges_L16:
        mr r3,r9
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_getItemNumAdjusted:
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        stw r5,32(r31)
        li r9,0
        stw r9,8(r31)
        lwz r5,32(r31)
        lwz r4,28(r31)
        lwz r3,24(r31)
        bl _getItemNum
        mr r9,r3
        stw r9,16(r31)
        li r9,0
        stw r9,12(r31)
        b _keyChanges_L18
_keyChanges_L20:
        lwz r6,12(r31)
        lwz r5,32(r31)
        lwz r4,28(r31)
        lwz r3,24(r31)
        bl _getItem
        mr r9,r3
        lbz r9,0(r9)
        stw r9,20(r31)
        lwz r3,20(r31)
        bl _checkType
        mr r9,r3
        addic r10,r9,-1
        subfe r9,r10,r9
        cmpwi cr0,r9,0
        beq cr0,_keyChanges_L19
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
_keyChanges_L19:
        lwz r9,12(r31)
        addi r9,r9,1
        stw r9,12(r31)
_keyChanges_L18:
        lwz r10,12(r31)
        lwz r9,16(r31)
        cmpw cr0,r10,r9
        blt cr0,_keyChanges_L20
        lwz r9,8(r31)
        mr r3,r9
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_itemLoopAdjustment:
        stwu r1,-64(r1)
        mflr r0
        stw r0,68(r1)
        stw r31,60(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        stw r5,32(r31)
        stw r6,36(r31)
        stw r7,40(r31)
        lwz r6,36(r31)
        lwz r5,32(r31)
        lwz r4,28(r31)
        lwz r3,24(r31)
        bl _getItem
        mr r9,r3
        lbz r9,0(r9)
        stw r9,8(r31)
        lwz r3,8(r31)
        bl _checkType
        mr r9,r3
        addic r10,r9,-1
        subfe r9,r10,r9
        cmpwi cr0,r9,0
        beq cr0,_keyChanges_L23
        lwz r9,40(r31)
        addi r9,r9,28
        stw r9,40(r31)
_keyChanges_L23:
        lwz r9,40(r31)
        mr r3,r9
        addi r11,r31,64
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_itemLoopContinue:
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        stw r5,32(r31)
        stw r6,36(r31)
        lwz r5,32(r31)
        lwz r4,28(r31)
        lwz r3,24(r31)
        bl _getItemNum
        mr r9,r3
        stw r9,8(r31)
        lwz r10,36(r31)
        lwz r9,8(r31)
        cmpw cr0,r10,r9
        bge cr0,_keyChanges_L26
        li r9,1
        b _keyChanges_L27
_keyChanges_L26:
        li r9,0
_keyChanges_L27:
        mr r3,r9
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################################
# assumes that boxNum in r22, dropNum in r20, idx in r18, ptr in r31, offset in r23
_preItemLoopAdjustment:
        # call1
        mr r3, r31
        clrlwi r4,r22,24
        clrlwi r5,r20,16
        clrlwi r6,r18,16
        mr r7, r23
        bl _itemLoopAdjustment
        mr r23, r3
        # call2
        mr r3, r31
        clrlwi r4,r22,24
        clrlwi r5,r20,16
        clrlwi r6,r18,16
        bl _itemLoopContinue
        addi r18, r18, 1
        cmpwi r3,0
        beq _preItemLoopAdjustmentEnd
        b _itemLoopStart
_preItemLoopAdjustmentEnd:
        b _itemLoopEnd

[XCX_Archipelago_keyChanges_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

0x021b70bc = bl _IsPermit # replace getLocal inside IsPermit with new check
0x02b051a4 = bl _assignDollCheck # replace lvlCheck with dollLicense + lvlCheck
0x02b051c4 = nop # remove original error message
0x022e9920 = nop # restructure online skell flight module check to always use this one
0x022e9934 = bl _loadSkyUnit # replace online skell flight module call with own
0x027d6da0 = bl _loadFNet # replace getScenarioFlag for initial load
0x027d5748 = blr # return original call to changeScenarioFlag Fnet

0x022e2c24 = nop # don't set all the arts/skills/classes if you change your class
0x020c48c4 = blr # disable class exp
0x020c63d8 = blr # disable friend exp

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

#disable field skills
0x0238e138 = nop

#disable affinity quest arts reward
0x029c7dc0 = li r3,0

# mandatory disable shops
0x02a32770 = nop # skell frame
0x02a69954 = nop # augment menu
0x02a69968 = nop # develop menu
# optional shops # need paramaterization
0x02a326d0 = nop # ground weapon
0x02a326f8 = nop # ground armor
0x02a32720 = nop # skell weapon
0x02a32748 = nop # skell armor
0x029e8a70 = nop # lu shop for augment upgrades

# experimental code to integrate l shop into replaced develop menu
# _openLShop = 0x02c89a9c
# _isFinishLShop = 0x02c89c78
# _closeLShop = 0x02c89c00
# 0x02B83CB4 = bl _openLShop
# 0x02B83CCC = bl _openLShop
# 0x02B83C7C = bl _closeLShop
# 0x02B83C98 = bl _closeLShop

_menuBasePtr = 0x1038ae50 # from error::menu::BladeHomeMenu
_openHudTelop = 0x02c91f3c # ::MenuTask
_chkLvl = 0x02af8e7c # ::menu::MenuDollGarage
_addItemEquipment = 0x02366cf0 # ::ItemBox::ItemType::Type::ItemHandle
_getItem = 0x021ab180 # ::ItemDrop::ItemDropManager
_getItemNum = 0x021ab164 #::ItemDrop::ItemDropManager

##################################################################################
[XCX_Archipelago_keyChanges_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

##################################################################################
[XCX_Archipelago_keyChanges_V100U]
moduleMatches = 0xAB97DE6B, 0x676EB33E # 1.0.1U, 1.0.0U

##################################################################################
[XCX_Archipelago_keyChanges_V102J]
moduleMatches = 0x7672271D # 1.0.2J

##################################################################################
[XCX_Archipelago_keyChanges_V100J]
moduleMatches = 0x785CA8A9 # 1.0.0J
