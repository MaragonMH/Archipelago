[XCX_Archipelago_Add]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_addItem:
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        lwz r9,24(r31)
        cmpwi cr0,r9,9
        beq cr0,_add_L2
        lwz r9,28(r31)
        li r6,1
        addi r10,r31,8
        mr r5,r10
        mr r4,r9
        lwz r3,24(r31)
        bl _AddItemEquipment
        b _add_L4
_add_L2:
        addi r9,r31,28
        mr r3,r9
        bl _addGarage
_add_L4:
        nop
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_addArt:
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        li r9,0
        stw r9,8(r31)
        lwz r3,8(r31)
        bl GetCharaDataPtr
        mr r9,r3
        li r6,0
        lwz r5,28(r31)
        lwz r4,24(r31)
        mr r3,r9
        bl _reqMenuSetArtsLevel
        nop
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_addSkill:
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        li r9,0
        stw r9,8(r31)
        lwz r3,8(r31)
        bl GetCharaDataPtr
        mr r9,r3
        li r6,0
        lwz r5,28(r31)
        lwz r4,24(r31)
        mr r3,r9
        bl _reqMenuSetSkillsLevel
        nop
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_addFriend:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        stw r4,12(r31)
        lwz r4,12(r31)
        lwz r3,8(r31)
        bl _SetFriendRank
        nop
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_addFieldSkill:
        stwu r1,-48(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        lis r9,fieldSkillBasePtr@ha
        lwz r9,fieldSkillBasePtr@l(r9)
        stw r9,8(r31)
        lwz r9,8(r31)
        addis r9,r9,0x5
        addi r9,r9,-29928
        stw r9,8(r31)
        lwz r9,24(r31)
        addi r9,r9,-1
        lwz r10,8(r31)
        add r9,r10,r9
        stw r9,8(r31)
        lwz r9,28(r31)
        mr r10,r9
        lwz r9,8(r31)
        stb r10,0(r9)
        nop
        addi r11,r31,48
        lwz r31,-4(r11)
        mr r1,r11
        blr
_addKey:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        stw r4,12(r31)
        lwz r9,8(r31)
        cmpwi cr0,r9,4
        beq cr0,_add_L15
        lwz r9,8(r31)
        cmpwi cr0,r9,4
        bgt cr0,_add_L16
        lwz r9,8(r31)
        cmpwi cr0,r9,3
        beq cr0,_add_L12
        lwz r9,8(r31)
        cmpwi cr0,r9,3
        bgt cr0,_add_L16
        lwz r9,8(r31)
        cmpwi cr0,r9,1
        beq cr0,_add_L13
        lwz r9,8(r31)
        cmpwi cr0,r9,2
        beq cr0,_add_L14
        b _add_L16
_add_L13:
        lwz r5,12(r31)
        li r4,24155
        li r3,1
        bl _setLocal
        b _add_L11
_add_L14:
        lwz r5,12(r31)
        li r4,30224
        li r3,1
        bl _setLocal
        b _add_L11
_add_L12:
        lwz r5,12(r31)
        li r4,27587
        li r3,1
        bl _setLocal
        b _add_L11
_add_L15:
        nop
_add_L11:
_add_L16:
        nop
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_addClass:
        stwu r1,-48(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        lis r9,classBasePtr@ha
        lwz r9,classBasePtr@l(r9)
        stw r9,8(r31)
        lwz r9,24(r31)
        mulli r9,r9,30
        addis r9,r9,0x1
        addi r9,r9,-2468
        lwz r10,8(r31)
        add r9,r10,r9
        stw r9,8(r31)
        lwz r9,28(r31)
        mr r10,r9
        lwz r9,8(r31)
        stb r10,0(r9)
        nop
        addi r11,r31,48
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################################

[XCX_Archipelago_Add_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

classBasePtr = 0x10367638 # getClassLv::menu::MenuDataUtil

_AddItemEquipment = 0x02366cf0 # ::ItemBox::ItemType::ItemHandle
_addGarage = 0x0234c620 # ::CmdCommon::SceneCmdPrm
_reqMenuSetArtsLevel = 0x02347c1c # ::CmdReq
_reqMenuSetSkillsLevel = 0x02348b0c # ::CmdReq
_updateLevel = 0x02b42ffc # ::menu::MenuFieldSkill
_SetFriendRank = 0x027faee0 # ::Util

_setLocal = 0x0228f008 # ::GameFlag

##################################################################################
[XCX_Archipelago_Add_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

##################################################################################
[XCX_Archipelago_Add_V100U]
moduleMatches = 0xAB97DE6B, 0x676EB33E # 1.0.1U, 1.0.0U

##################################################################################
[XCX_Archipelago_Add_V102J]
moduleMatches = 0x7672271D # 1.0.2J

##################################################################################
[XCX_Archipelago_Add_V100J]
moduleMatches = 0x785CA8A9 # 1.0.0J
