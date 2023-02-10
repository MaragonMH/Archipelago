[XCX_Archipelago_itemList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_formatItemText:
        .string "IT Id=%03x Tp=%02x:"
_formatItemGearText:
        .string "IT Id=%03x Tp=%02x S1Id=%03x U1=%01x S2Id=%03x U2=%01x S3Id=%03x U3=%01x A1Id=%04x A2Id=%04x A3Id=%04x:"
_postItemList:
        stwu r1,-128(r1)
        mflr r0
        stw r0,132(r1)
        stw r31,124(r1)
        mr r31,r1
        stw r3,96(r31)
        stw r4,100(r31)
        stw r5,104(r31)
        stw r6,108(r31)
        li r9,1
        stw r9,32(r31)
        b _Item_L2
_Item_L11:
        lwz r9,32(r31)
        cmpwi cr0,r9,8
        beq cr0,_Item_L13
        lwz r9,32(r31)
        cmpwi cr0,r9,9
        beq cr0,_Item_L13
        lis r9,_itemListBase@ha
        addi r9,r9,_itemListBase@l
        stw r9,40(r31)
        lwz r4,32(r31)
        lwz r3,40(r31)
        bl _getItemTypeInfo
        mr r9,r3
        lwz r9,0(r9)
        stw r9,36(r31)
        b _Item_L6
_Item_L10:
        lwz r9,36(r31)
        lwz r9,0(r9)
        srwi r9,r9,19
        stw r9,44(r31)
        lwz r9,32(r31)
        cmpwi cr0,r9,7
        ble cr0,_Item_L7
        lwz r9,32(r31)
        cmpwi cr0,r9,9
        ble cr0,_Item_L8
        lwz r9,32(r31)
        cmpwi cr0,r9,19
        bgt cr0,_Item_L8
_Item_L7:
        lwz r9,36(r31)
        addi r9,r9,12
        lhz r9,0(r9)
        srwi r9,r9,4
        stw r9,48(r31)
        lwz r9,36(r31)
        addi r9,r9,14
        lhz r9,0(r9)
        srwi r9,r9,4
        stw r9,52(r31)
        lwz r9,36(r31)
        addi r9,r9,16
        lhz r9,0(r9)
        srwi r9,r9,4
        stw r9,56(r31)
        lwz r9,36(r31)
        addi r9,r9,12
        lhz r9,0(r9)
        slwi r9,r9,28
        srawi r9,r9,28
        stw r9,60(r31)
        lwz r9,36(r31)
        addi r9,r9,14
        lhz r9,0(r9)
        slwi r9,r9,28
        srawi r9,r9,28
        stw r9,64(r31)
        lwz r9,36(r31)
        addi r9,r9,16
        lhz r9,0(r9)
        slwi r9,r9,28
        srawi r9,r9,28
        stw r9,68(r31)
        lwz r9,36(r31)
        addi r9,r9,18
        lhz r9,0(r9)
        stw r9,72(r31)
        lwz r9,36(r31)
        addi r9,r9,20
        lhz r9,0(r9)
        stw r9,76(r31)
        lwz r9,36(r31)
        addi r9,r9,22
        lhz r9,0(r9)
        stw r9,80(r31)
        lwz r4,108(r31)
        lwz r9,80(r31)
        stw r9,28(r1)
        lwz r9,76(r31)
        stw r9,24(r1)
        lwz r9,72(r31)
        stw r9,20(r1)
        lwz r9,68(r31)
        stw r9,16(r1)
        lwz r9,56(r31)
        stw r9,12(r1)
        lwz r9,64(r31)
        stw r9,8(r1)
        lwz r10,52(r31)
        lwz r9,60(r31)
        lwz r8,48(r31)
        lwz r7,32(r31)
        lwz r6,44(r31)
        lis r5,_formatItemGearText@ha
        addi r5,r5,_formatItemGearText@l
        lwz r3,100(r31)
        crxor 6,6,6
        lis r12, after_Item__sprintf_s@ha
		addi r12,r12,after_Item__sprintf_s@l
		mtlr r12
		lis r12,__sprintf_s@ha
		addi r12,r12,__sprintf_s@l
		mtctr r12
		bctr
after_Item__sprintf_s:
        mr r9,r3
        mr r10,r9
        lwz r9,100(r31)
        add r9,r9,r10
        stw r9,100(r31)
        b _Item_L9
_Item_L8:
        lwz r10,108(r31)
        lwz r7,32(r31)
        lwz r6,44(r31)
        lis r9,_formatItemText@ha
        addi r5,r9,_formatItemText@l
        mr r4,r10
        lwz r3,100(r31)
        crxor 6,6,6
        lis r12, after_Item1__sprintf_s@ha
		addi r12,r12,after_Item1__sprintf_s@l
		mtlr r12
		lis r12,__sprintf_s@ha
		addi r12,r12,__sprintf_s@l
		mtctr r12
		bctr
after_Item1__sprintf_s:
        mr r9,r3
        mr r10,r9
        lwz r9,100(r31)
        add r9,r9,r10
        stw r9,100(r31)
_Item_L9:
        lwz r9,36(r31)
        addi r9,r9,96
        stw r9,36(r31)
        lwz r10,100(r31)
        lwz r9,104(r31)
        cmplw cr0,r10,r9
        ble cr0,_Item_L6
        lwz r3,96(r31)
        bl _postCurl
        lwz r9,96(r31)
        stw r9,100(r31)
_Item_L6:
        lwz r9,36(r31)
        lwz r9,0(r9)
        cmpwi cr0,r9,0
        bne cr0,_Item_L10
        b _Item_L5
_Item_L13:
        nop
_Item_L5:
        lwz r9,32(r31)
        addi r9,r9,1
        stw r9,32(r31)
_Item_L2:
        lwz r9,32(r31)
        cmpwi cr0,r9,31
        ble cr0,_Item_L11
        lwz r9,100(r31)
        mr r3,r9
        addi r11,r31,128
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################

[XCX_Archipelago_itemList_V101E] ; ########################################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

_getItemTypeInfo = 0x02361830
_itemListBase = 0x10399be8
