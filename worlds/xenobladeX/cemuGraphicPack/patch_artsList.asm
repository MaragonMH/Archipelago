[XCX_Archipelago_artsList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_formatArtsText:
        .string "AT Id=%02x Lv=%01x:"
_postArtsList:
        stwu r1,-48(r1)
        mflr r0
        stw r0,52(r1)
        stw r31,44(r1)
        mr r31,r1
        stw r3,24(r31)
        stw r4,28(r31)
        stw r5,32(r31)
        stw r6,36(r31)
        li r9,0
        stw r9,8(r31)
        b _Arts_L2
_Arts_L6:
        lwz r3,8(r31)
        bl GetCharaDataPtr
        mr r9,r3
        stw r9,16(r31)
        li r9,1
        stw r9,12(r31)
        b _Arts_L3
_Arts_L5:
        lwz r9,12(r31)
        addi r9,r9,888
        lwz r10,16(r31)
        add r9,r10,r9
        lbz r9,0(r9)
        stw r9,20(r31)
        lwz r10,36(r31)
        lwz r7,20(r31)
        lwz r6,12(r31)
        lis r9,_formatArtsText@ha
        addi r5,r9,_formatArtsText@l
        mr r4,r10
        lwz r3,28(r31)
        crxor 6,6,6
        lis r12, after_Arts__sprintf_s@ha
		addi r12,r12,after_Arts__sprintf_s@l
		mtlr r12
		lis r12,__sprintf_s@ha
		addi r12,r12,__sprintf_s@l
		mtctr r12
		bctr
after_Arts__sprintf_s:
        mr r9,r3
        mr r10,r9
        lwz r9,28(r31)
        add r9,r9,r10
        stw r9,28(r31)
        lwz r10,28(r31)
        lwz r9,32(r31)
        cmplw cr0,r10,r9
        ble cr0,_Arts_L4
        lwz r3,24(r31)
        bl _postCurl
        lwz r9,24(r31)
        stw r9,28(r31)
_Arts_L4:
        lwz r9,12(r31)
        addi r9,r9,1
        stw r9,12(r31)
_Arts_L3:
        lwz r9,12(r31)
        cmpwi cr0,r9,156
        ble cr0,_Arts_L5
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
_Arts_L2:
        lwz r9,8(r31)
        cmpwi cr0,r9,0
        ble cr0,_Arts_L6
        lwz r9,28(r31)
        mr r3,r9
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################################

[XCX_Archipelago_artsList_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

GetCharaDataPtr = 0x027f70ac # ::Util

##################################################################################
[XCX_Archipelago_artsList_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

##################################################################################
[XCX_Archipelago_artsList_V100U]
moduleMatches = 0xAB97DE6B, 0x676EB33E # 1.0.1U, 1.0.0U

##################################################################################
[XCX_Archipelago_artsList_V102J]
moduleMatches = 0x7672271D # 1.0.2J

##################################################################################
[XCX_Archipelago_artsList_V100J]
moduleMatches = 0x785CA8A9 # 1.0.0J
