# Keyboard shortcut: Ctrl + Alt + r
[XCX_Archipelago]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_free:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        lwz r3,8(r31)
        lis r12, after_archipelago__free@ha
		addi r12,r12,after_archipelago__free@l
		mtlr r12
		lis r12,__free@ha
		addi r12,r12,__free@l
		mtctr r12
		bctr
after_archipelago__free:
        nop
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_strtol:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        stw r4,12(r31)
        stw r5,16(r31)
        lwz r5,16(r31)
        lwz r4,12(r31)
        lwz r3,8(r31)
        lis r12, after_archipelago__strtol@ha
		addi r12,r12,after_archipelago__strtol@l
		mtlr r12
		lis r12,__strtol@ha
		addi r12,r12,__strtol@l
		mtctr r12
		bctr
after_archipelago__strtol:
        mr r9,r3
        mr r3,r9
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_postArchipelago:
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        li r9,0
        ori r9,r9,0xffff
        stw r9,8(r31)
        li r9,256
        stw r9,12(r31)
        lwz r9,8(r31)
        mr r3,r9
        lis r12, after_archipelago__malloc@ha
		addi r12,r12,after_archipelago__malloc@l
		mtlr r12
		lis r12,__malloc@ha
		addi r12,r12,__malloc@l
		mtctr r12
		bctr
after_archipelago__malloc:
        mr r9,r3
        stw r9,16(r31)
        lwz r9,16(r31)
        stw r9,20(r31)
        lwz r10,8(r31)
        lwz r9,12(r31)
        subf r9,r9,r10
        lwz r10,16(r31)
        add r9,r10,r9
        stw r9,24(r31)
        lwz r9,20(r31)
        li r10,94
        stb r10,0(r9)
        lwz r9,20(r31)
        addi r9,r9,1
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postArtsList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postClassList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postCollepediaList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postEnemyList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postFieldSkillsList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postFnNodeList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postFriendList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postItemList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postLocationList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postSegmentList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postSkillsList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postKeyList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postEquipList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postDollList
        mr r9,r3
        stw r9,20(r31)
        lwz r6,12(r31)
        lwz r5,24(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _postVeinList
        mr r9,r3
        stw r9,20(r31)
        lwz r9,20(r31)
        li r10,36
        stb r10,0(r9)
        lwz r9,20(r31)
        addi r9,r9,1
        li r10,0
        stb r10,0(r9)
        lwz r3,16(r31)
        bl _postCurl
        lwz r3,16(r31)
        bl _free
        nop
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_getArchipelago:
        stwu r1,-112(r1)
        mflr r0
        stw r0,116(r1)
        stw r31,108(r1)
        mr r31,r1
        bl _getCurl
        mr r9,r3
        stw r9,12(r31)
        lwz r9,12(r31)
        cmpwi cr0,r9,0
        beq cr0,_archipelago_L26
        lwz r9,12(r31)
        stw r9,8(r31)
        b _archipelago_L8
_archipelago_L25:
        lwz r9,8(r31)
        lbz r9,0(r9)
        addi r9,r9,-10
        cmplwi cr0,r9,73
        bgt cr0,_archipelago_L9
        slwi r10,r9,2
        lis r9,_archipelago_L11@ha
        addi r9,r9,_archipelago_L11@l
        add r9,r10,r9
        lwz r10,0(r9)
        lis r9,_archipelago_L11@ha
        addi r9,r9,_archipelago_L11@l
        add r9,r10,r9
        mtctr r9
        bctr
_archipelago_L11:
        .long _archipelago_L20-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L19-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L18-_archipelago_L11
        .long _archipelago_L17-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L16-_archipelago_L11
        .long _archipelago_L15-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L14-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L13-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L12-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L9-_archipelago_L11
        .long _archipelago_L10-_archipelago_L11
_archipelago_L14:
        lwz r9,8(r31)
        addi r9,r9,5
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,40(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,44(r31)
        lwz r9,8(r31)
        addi r9,r9,8
        stw r9,8(r31)
        lwz r4,44(r31)
        lwz r3,40(r31)
        bl _addItem
        b _archipelago_L8
_archipelago_L15:
        lwz r9,8(r31)
        addi r9,r9,5
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,48(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,52(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,56(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,60(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,64(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,68(r31)
        lwz r9,8(r31)
        addi r9,r9,8
        stw r9,8(r31)
        lwz r8,68(r31)
        lwz r7,64(r31)
        lwz r6,60(r31)
        lwz r5,56(r31)
        lwz r4,52(r31)
        lwz r3,48(r31)
        bl _addGear
        b _archipelago_L8
_archipelago_L19:
        lwz r9,8(r31)
        addi r9,r9,5
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,96(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,100(r31)
        lwz r9,8(r31)
        addi r9,r9,8
        stw r9,8(r31)
        lwz r4,100(r31)
        lwz r3,96(r31)
        bl _addArt
        b _archipelago_L8
_archipelago_L10:
        lwz r9,8(r31)
        addi r9,r9,5
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,16(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,20(r31)
        lwz r9,8(r31)
        addi r9,r9,8
        stw r9,8(r31)
        lwz r4,20(r31)
        lwz r3,16(r31)
        bl _addSkill
        b _archipelago_L8
_archipelago_L16:
        lwz r9,8(r31)
        addi r9,r9,5
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,72(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,76(r31)
        lwz r9,8(r31)
        addi r9,r9,8
        stw r9,8(r31)
        lwz r4,76(r31)
        lwz r3,72(r31)
        bl _addFriend
        b _archipelago_L8
_archipelago_L17:
        lwz r9,8(r31)
        addi r9,r9,5
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,80(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,84(r31)
        lwz r9,8(r31)
        addi r9,r9,8
        stw r9,8(r31)
        lwz r4,84(r31)
        lwz r3,80(r31)
        bl _addFieldSkill
        b _archipelago_L8
_archipelago_L13:
        lwz r9,8(r31)
        addi r9,r9,5
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,32(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,36(r31)
        lwz r9,8(r31)
        addi r9,r9,8
        stw r9,8(r31)
        lwz r4,36(r31)
        lwz r3,32(r31)
        bl _addKey
        b _archipelago_L8
_archipelago_L18:
        lwz r9,8(r31)
        addi r9,r9,5
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,88(r31)
        lwz r9,8(r31)
        addi r9,r9,12
        stw r9,8(r31)
        li r5,16
        li r4,0
        lwz r3,8(r31)
        bl _strtol
        mr r9,r3
        stw r9,92(r31)
        lwz r9,8(r31)
        addi r9,r9,8
        stw r9,8(r31)
        lwz r4,92(r31)
        lwz r3,88(r31)
        bl _addClass
        b _archipelago_L8
_archipelago_L12:
        lwz r9,8(r31)
        addi r9,r9,2
        stw r9,8(r31)
        lwz r9,8(r31)
        stw r9,24(r31)
        b _archipelago_L21
_archipelago_L22:
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
_archipelago_L21:
        lwz r9,8(r31)
        lbz r9,0(r9)
        cmpwi cr0,r9,10
        bne cr0,_archipelago_L22
        lwz r9,8(r31)
        li r10,0
        stb r10,0(r9)
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
        lwz r9,8(r31)
        stw r9,28(r31)
        b _archipelago_L23
_archipelago_L24:
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
_archipelago_L23:
        lwz r9,8(r31)
        lbz r9,0(r9)
        cmpwi cr0,r9,10
        bne cr0,_archipelago_L24
        lwz r9,8(r31)
        li r10,0
        stb r10,0(r9)
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
        lis r9,_menuBasePtr@ha
        lwz r9,_menuBasePtr@l(r9)
        lwz r5,28(r31)
        lwz r4,24(r31)
        mr r3,r9
        bl writeSystemLog
        b _archipelago_L8
_archipelago_L20:
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
        b _archipelago_L8
_archipelago_L9:
        lwz r3,12(r31)
        bl _free
        b _archipelago_L5
_archipelago_L8:
        lwz r9,8(r31)
        lbz r9,0(r9)
        cmpwi cr0,r9,0
        bne cr0,_archipelago_L25
        lwz r3,12(r31)
        bl _free
        b _archipelago_L5
_archipelago_L26:
        nop
_archipelago_L5:
        addi r11,r31,112
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
_mainArchipelago:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        stw r4,12(r31)
        lwz r10,12(r31)
        lis r9,0x5555
        ori r9,r9,0x5556
        mulhw r8,r10,r9
        srawi r9,r10,31
        subf r9,r9,r8
        mulli r9,r9,3
        subf r9,r9,r10
        cmpwi cr0,r9,0
        beq cr0,_archipelago_L28
        lwz r4,12(r31)
        lwz r3,8(r31)
        bl changeTime
        mr r9,r3
        b _archipelago_L29
_archipelago_L28:
        bl _initCurl
        bl _getArchipelago
        bl _postArchipelago
        bl _cleanupCurl
        lwz r4,12(r31)
        lwz r3,8(r31)
        bl changeTime
        mr r9,r3
        nop
_archipelago_L29:
        mr r3,r9
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################

[XCX_Archipelago_V101E] ; ########################################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

changeTime = 0x022b36f4 #::GameManager
writeSystemLog = 0x02c74290 #::MenuTask

__sprintf_s = 0x03133354
__malloc = 0x03b1aeb0
__free = 0x03b1afe8
__strtol = 0x03b1b27c

0x022b3bbc = bl _mainArchipelago

##################################################################################
[XCX_Archipelago_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

##################################################################################
[XCX_Archipelago_V100U]
moduleMatches = 0xAB97DE6B, 0x676EB33E # 1.0.1U, 1.0.0U

##################################################################################
[XCX_Archipelago_V102J]
moduleMatches = 0x7672271D # 1.0.2J

##################################################################################
[XCX_Archipelago_V100J]
moduleMatches = 0x785CA8A9 # 1.0.0J
