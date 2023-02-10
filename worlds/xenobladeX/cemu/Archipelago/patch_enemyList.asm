[XCX_Archipelago_enemyList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_formatEnemyText:
        .string "EN Id=%03x Dc=%01x:"
_postEnemyList:
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        stw r5,32(r31)
        stw r6,36(r31)
        li r9,1
        stw r9,8(r31)
        b _Enemy_L2
_Enemy_L4:
        lwz r3,8(r31)
        bl getEnBookDiscovery
        mr r9,r3
        stw r9,12(r31)
        lwz r10,36(r31)
        lwz r7,12(r31)
        lwz r6,8(r31)
        lis r9,_formatEnemyText@ha
        addi r5,r9,_formatEnemyText@l
        mr r4,r10
        lwz r3,28(r31)
        crxor 6,6,6
        lis r12, after_Enemy__sprintf_s@ha
		addi r12,r12,after_Enemy__sprintf_s@l
		mtlr r12
		lis r12,__sprintf_s@ha
		addi r12,r12,__sprintf_s@l
		mtctr r12
		bctr
after_Enemy__sprintf_s:
        mr r9,r3
        mr r10,r9
        lwz r9,28(r31)
        add r9,r9,r10
        stw r9,28(r31)
        lwz r10,28(r31)
        lwz r9,32(r31)
        cmplw cr0,r10,r9
        ble cr0,_Enemy_L3
        lwz r3,24(r31)
        bl _postCurl
        lwz r9,24(r31)
        stw r9,28(r31)
_Enemy_L3:
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
_Enemy_L2:
        lwz r9,8(r31)
        cmpwi cr0,r9,1403
        ble cr0,_Enemy_L4
        lwz r9,28(r31)
        mr r3,r9
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################################

[XCX_Archipelago_enemyList_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

getEnBookDiscovery = 0x027fcab4 # ::Util

##################################################################################
[XCX_Archipelago_enemyList_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

##################################################################################
[XCX_Archipelago_enemyList_V100U]
moduleMatches = 0xAB97DE6B, 0x676EB33E # 1.0.1U, 1.0.0U

##################################################################################
[XCX_Archipelago_enemyList_V102J]
moduleMatches = 0x7672271D # 1.0.2J

##################################################################################
[XCX_Archipelago_enemyList_V100J]
moduleMatches = 0x785CA8A9 # 1.0.0J
