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

# VERSION SPECIFIC ###############################################################

[XCX_Archipelago_keyChanges_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

0x021b70bc = bl _IsPermit # replace getLocal inside IsPermit with new check
0x02b051a4 = bl _assignDollCheck # replace lvlCheck with dollLicense + lvlCheck
0x02b051c4 = nop # remove original error message
0x022e9920 = nop # restructure online skell flight module check to always use this one
0x022e9934 = bl _loadSkyUnit # replace online skell flight module call with own
0x027d6da0 = bl _loadFNet # replace getScenarioFlag for initial load
0x027d5748 = blr # return original call to changeScenarioFlag Fnet

_menuBasePtr = 0x1038ae50 # from error::menu::BladeHomeMenu
_openHudTelop = 0x02c91f3c # ::MenuTask
_chkLvl = 0x02af8e7c # ::menu::MenuDollGarage

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
