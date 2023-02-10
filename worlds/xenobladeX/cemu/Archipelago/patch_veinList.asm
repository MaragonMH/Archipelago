[XCX_archipelago_veinList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_formatVeinsText:
        .string "VN Id=%02x Bc=%02x:"
_postVeinList:
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
        b _veinList_L2
_veinList_L4:
        lis r9,fnetBasePtr@ha
        lwz r9,fnetBasePtr@l(r9)
        addi r9,r9,8
        lwz r9,0(r9)
        lwz r4,8(r31)
        mr r3,r9
        bl _getBeacon
        mr r9,r3
        stw r9,12(r31)
        lwz r10,36(r31)
        lwz r7,12(r31)
        lwz r6,8(r31)
        lis r9,_formatVeinsText@ha
        addi r5,r9,_formatVeinsText@l
        mr r4,r10
        lwz r3,28(r31)
        crxor 6,6,6
        lis r12, after_veinList__sprintf_s@ha
		addi r12,r12,after_veinList__sprintf_s@l
		mtlr r12
		lis r12,__sprintf_s@ha
		addi r12,r12,__sprintf_s@l
		mtctr r12
		bctr
after_veinList__sprintf_s:
        mr r9,r3
        mr r10,r9
        lwz r9,28(r31)
        add r9,r9,r10
        stw r9,28(r31)
        lwz r10,28(r31)
        lwz r9,32(r31)
        cmplw cr0,r10,r9
        ble cr0,_veinList_L3
        lwz r3,24(r31)
        bl _postCurl
        lwz r9,24(r31)
        stw r9,28(r31)
_veinList_L3:
        lwz r9,8(r31)
        addi r9,r9,1
        stw r9,8(r31)
_veinList_L2:
        lwz r9,8(r31)
        cmpwi cr0,r9,109
        ble cr0,_veinList_L4
        lwz r9,28(r31)
        mr r3,r9
        addi r11,r31,48
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################################

[XCX_archipelago_veinList_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

_getBeacon = 0x027d00f8 # ::fnet::FnetData

##################################################################################
[XCX_archipelago_veinList_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

##################################################################################
[XCX_archipelago_veinList_V100U]
moduleMatches = 0xAB97DE6B, 0x676EB33E # 1.0.1U, 1.0.0U

##################################################################################
[XCX_archipelago_veinList_V102J]
moduleMatches = 0x7672271D # 1.0.2J

##################################################################################
[XCX_archipelago_veinList_V100J]
moduleMatches = 0x785CA8A9 # 1.0.0J