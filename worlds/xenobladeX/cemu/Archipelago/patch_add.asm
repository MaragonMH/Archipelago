[XCX_Archipelago_Add]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_addItem:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        stw r4,12(r31)
        lwz r9,8(r31)
        cmpwi cr0,r9,9
        beq cr0,_add_L2
        lwz r9,12(r31)
        li r5,1
        mr r4,r9
        lwz r3,8(r31)
        bl _reqMenuAddItemFromId
        b _add_L4
_add_L2:
        addi r9,r31,12
        mr r3,r9
        bl _addGarage
_add_L4:
        nop
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_hasPreciousItem:
        stwu r1,-64(r1)
        mflr r0
        stw r0,68(r1)
        stw r31,60(r1)
        mr r31,r1
        stw r3,40(r31)
        lis r9,_itemListBase@ha
        addi r9,r9,_itemListBase@l
        stw r9,16(r31)
        li r4,29
        lwz r3,16(r31)
        bl _getItemTypeInfo
        mr r9,r3
        lwz r9,0(r9)
        stw r9,8(r31)
        li r9,0
        stw r9,12(r31)
        b _add_L6
_add_L11:
        lwz r9,8(r31)
        lwz r9,0(r9)
        slwi r9,r9,13
        srwi r9,r9,26
        stw r9,20(r31)
        lwz r9,20(r31)
        cmpwi cr0,r9,29
        bne cr0,_add_L12
        lwz r9,8(r31)
        lwz r9,0(r9)
        srwi r9,r9,19
        stw r9,24(r31)
        lwz r9,40(r31)
        lwz r10,24(r31)
        cmpw cr0,r10,r9
        bne cr0,_add_L9
        li r9,1
        b _add_L10
_add_L9:
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        lwz r9,12(r31)
        addi r9,r9,1
        stw r9,12(r31)
_add_L6:
        lwz r9,12(r31)
        cmpwi cr0,r9,299
        ble cr0,_add_L11
        b _add_L8
_add_L12:
        nop
_add_L8:
        li r9,0
_add_L10:
        mr r3,r9
        addi r11,r31,64
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
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        lwz r9,24(r31)
        cmpwi cr0,r9,0
        bne cr0,_add_L18
        lwz r5,28(r31)
        li r4,1
        li r3,16
        bl _setLocal
        b _add_L19
_add_L18:
        lwz r9,24(r31)
        cmpwi cr0,r9,6
        bne cr0,_add_L20
        li r4,0
        addi r9,r31,8
        mr r3,r9
        bl _getCharaHandle
        addi r9,r31,8
        mr r4,r9
        li r3,0
        bl _SetDead
        b _add_L19
_add_L20:
        lwz r9,24(r31)
        cmpwi cr0,r9,7
        bne cr0,_add_L21
        li r3,0
        bl _reqForceDamagePlayerTargetGoner
        b _add_L19
_add_L21:
        lwz r9,24(r31)
        addi r9,r9,23
        mr r4,r9
        li r3,29
        bl _addItem
_add_L19:
        lwz r9,24(r31)
        cmpwi cr0,r9,4
        bne cr0,_add_L23
        lis r9,fnetBasePtr@ha
        lwz r10,fnetBasePtr@l(r9)
        lwz r9,28(r31)
        mulli r9,r9,3001
        mr r4,r9
        mr r3,r10
        bl _changeScenarioFlagFNet
_add_L23:
        nop
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_addClass:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r30,24(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        stw r4,12(r31)
        lwz r9,12(r31)
        mr r30,r9
        lwz r3,8(r31)
        bl _getClassDataPtr
        mr r9,r3
        stb r30,0(r9)
        nop
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r30,-8(r11)
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################################

[XCX_Archipelago_Add_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

_reqMenuAddItemFromId = 0x0234f1a8 # ::CmdReq
_addGarage = 0x0234c620 # ::CmdCommon::SceneCmdPrm
_reqMenuSetArtsLevel = 0x02347c1c # ::CmdReq
_reqMenuSetSkillsLevel = 0x02348b0c # ::CmdReq
_SetFriendRank = 0x027faee0 # ::Util
_getClassDataPtr = 0x027fa7a0 # ::Util

_setLocal = 0x0228f008 # ::GameFlag
_changeScenarioFlagFNet = 0x027d5638
_reqForceDamagePlayerTargetGoner = 0x021a88e4
_SetDead = 0x0298f2f0
_getCharaHandle = 0x02373b9c

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
