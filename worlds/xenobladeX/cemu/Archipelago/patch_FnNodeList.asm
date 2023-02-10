[XCX_Archipelago_FnNodeList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_formatFnNodeText:
        .string "FN Id=%03x Fg=%01x AId=%02x:"
_postFnNodeList:
        stwu r1,-64(r1)
        mflr r0
        stw r0,68(r1)
        stw r31,60(r1)
        mr r31,r1
        stw r3,40(r31)
        stw r4,44(r31)
        stw r5,48(r31)
        stw r6,52(r31)
        lis r9,segmentBasePtr@ha
        lwz r9,segmentBasePtr@l(r9)
        stw r9,8(r31)
        lwz r9,8(r31)
        addi r9,r9,16
        stw r9,8(r31)
        li r9,0
        stw r9,12(r31)
        b _FnNode_L2
_FnNode_L7:
        lwz r9,8(r31)
        addi r9,r9,16
        stw r9,16(r31)
        b _FnNode_L3
_FnNode_L6:
        lwz r9,16(r31)
        addi r9,r9,8
        lwz r9,0(r9)
        extsh r9,r9
        stw r9,20(r31)
        lwz r9,20(r31)
        extsh r9,r9
        mr r3,r9
        bl checkDP
        mr r9,r3
        stw r9,24(r31)
        lwz r9,16(r31)
        addi r9,r9,4
        lwz r9,0(r9)
        srawi r9,r9,24
        stw r9,28(r31)
        lwz r9,28(r31)
        cmpwi cr0,r9,1
        bne cr0,_FnNode_L9
        lwz r10,52(r31)
        lwz r8,12(r31)
        lwz r7,24(r31)
        lwz r6,20(r31)
        lis r9,_formatFnNodeText@ha
        addi r5,r9,_formatFnNodeText@l
        mr r4,r10
        lwz r3,44(r31)
        crxor 6,6,6
        lis r12, after_FnNode__sprintf_s@ha
		addi r12,r12,after_FnNode__sprintf_s@l
		mtlr r12
		lis r12,__sprintf_s@ha
		addi r12,r12,__sprintf_s@l
		mtctr r12
		bctr
after_FnNode__sprintf_s:
        mr r9,r3
        mr r10,r9
        lwz r9,44(r31)
        add r9,r9,r10
        stw r9,44(r31)
        lwz r10,44(r31)
        lwz r9,48(r31)
        cmplw cr0,r10,r9
        ble cr0,_FnNode_L5
        lwz r3,40(r31)
        bl _postCurl
        lwz r9,40(r31)
        stw r9,44(r31)
        b _FnNode_L5
_FnNode_L9:
        nop
_FnNode_L5:
        lwz r9,16(r31)
        addi r9,r9,28
        stw r9,16(r31)
_FnNode_L3:
        lwz r9,16(r31)
        lwz r9,0(r9)
        cmpwi cr0,r9,0
        bne cr0,_FnNode_L6
        lwz r9,8(r31)
        addi r9,r9,8156
        stw r9,8(r31)
        lwz r9,12(r31)
        addi r9,r9,1
        stw r9,12(r31)
_FnNode_L2:
        lwz r9,12(r31)
        cmpwi cr0,r9,20
        ble cr0,_FnNode_L7
        lwz r9,44(r31)
        mr r3,r9
        addi r11,r31,64
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr
		
# VERSION SPECIFIC ###############################################################

[XCX_Archipelago_FnNodeList_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

checkDP = 0x027d346c

##################################################################################
[XCX_Archipelago_FnNodeList_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

##################################################################################
[XCX_Archipelago_FnNodeList_V100U]
moduleMatches = 0xAB97DE6B, 0x676EB33E # 1.0.1U, 1.0.0U

##################################################################################
[XCX_Archipelago_FnNodeList_V102J]
moduleMatches = 0x7672271D # 1.0.2J

##################################################################################
[XCX_Archipelago_FnNodeList_V100J]
moduleMatches = 0x785CA8A9 # 1.0.0J
