[Archipelago_shopList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

_formatShopText:
	.string "SH Id=%03x Tp=%01x:"
_postShopList:
	stwu r1,-96(r1)
	mflr r0
	stw r0,100(r1)
	stw r31,92(r1)
	mr r31,r1
	stw r3,72(r31)
	stw r4,76(r31)
	stw r5,80(r31)
	stw r6,84(r31)
	li r9,1
	stw r9,8(r31)
	b _shopList_L2
_shopList_L5:
	bl GetBlueprintPtr
	mr r9,r3
	stw r9,64(r31)
	lwz r9,8(r31)
	lwz r10,64(r31)
	add r9,r10,r9
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	stw r9,68(r31)
	lwz r9,68(r31)
	cmpwi cr0,r9,3
	bne cr0,_shopList_L3
	lwz r10,84(r31)
	li r7,6
	lwz r6,8(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_1__sprintf_s@ha
	addi r12,r12,_after_shopList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L3:
	lwz r10,76(r31)
	lwz r9,80(r31)
	cmplw cr0,r10,r9
	ble cr0,_shopList_L4
	lwz r3,72(r31)
	bl _postCurl
	lwz r9,72(r31)
	stw r9,76(r31)
_shopList_L4:
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_shopList_L2:
	lwz r9,8(r31)
	cmpwi cr0,r9,199
	ble cr0,_shopList_L5
	li r9,1
	stw r9,12(r31)
	b _shopList_L6
_shopList_L15:
	bl GetKnowledgePtr
	mr r9,r3
	stw r9,16(r31)
	li r9,19364
	stw r9,20(r31)
	li r9,15364
	stw r9,24(r31)
	lwz r10,20(r31)
	lwz r9,12(r31)
	add r9,r10,r9
	lwz r10,16(r31)
	add r9,r10,r9
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	stw r9,28(r31)
	lwz r10,24(r31)
	lwz r9,12(r31)
	add r9,r10,r9
	lwz r10,16(r31)
	add r9,r10,r9
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	stw r9,32(r31)
	lwz r9,28(r31)
	rlwinm r9,r9,0,30,30
	stw r9,36(r31)
	lwz r9,32(r31)
	rlwinm r9,r9,0,30,30
	stw r9,40(r31)
	lwz r9,28(r31)
	rlwinm r9,r9,0,29,29
	stw r9,44(r31)
	lwz r9,32(r31)
	rlwinm r9,r9,0,29,29
	stw r9,48(r31)
	lwz r9,28(r31)
	rlwinm r9,r9,0,28,28
	stw r9,52(r31)
	lwz r9,32(r31)
	rlwinm r9,r9,0,28,28
	stw r9,32(r31)
	lwz r9,32(r31)
	stw r9,56(r31)
	lwz r9,28(r31)
	rlwinm r9,r9,0,27,27
	stw r9,60(r31)
	lwz r9,56(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L7
	lwz r10,84(r31)
	li r7,7
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_2__sprintf_s@ha
	addi r12,r12,_after_shopList_2__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_2__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L7:
	lwz r9,48(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L8
	lwz r10,84(r31)
	li r7,8
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_3__sprintf_s@ha
	addi r12,r12,_after_shopList_3__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_3__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L8:
	lwz r9,40(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L9
	lwz r10,84(r31)
	li r7,9
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_4__sprintf_s@ha
	addi r12,r12,_after_shopList_4__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_4__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L9:
	lwz r9,52(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L10
	lwz r10,84(r31)
	li r7,10
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_5__sprintf_s@ha
	addi r12,r12,_after_shopList_5__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_5__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L10:
	lwz r9,44(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L11
	lwz r10,84(r31)
	li r7,11
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_6__sprintf_s@ha
	addi r12,r12,_after_shopList_6__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_6__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L11:
	lwz r9,36(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L12
	lwz r10,84(r31)
	li r7,12
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_7__sprintf_s@ha
	addi r12,r12,_after_shopList_7__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_7__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L12:
	lwz r9,60(r31)
	cmpwi cr0,r9,0
	beq cr0,_shopList_L13
	lwz r10,84(r31)
	li r7,13
	lwz r6,12(r31)
	lis r9,_formatShopText@ha
	addi r5,r9,_formatShopText@l
	mr r4,r10
	lwz r3,76(r31)
	crxor cr6,cr6,cr6
	lis r12,_after_shopList_8__sprintf_s@ha
	addi r12,r12,_after_shopList_8__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_shopList_8__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,76(r31)
	add r9,r9,r10
	stw r9,76(r31)
_shopList_L13:
	lwz r10,76(r31)
	lwz r9,80(r31)
	cmplw cr0,r10,r9
	ble cr0,_shopList_L14
	lwz r3,72(r31)
	bl _postCurl
	lwz r9,72(r31)
	stw r9,76(r31)
_shopList_L14:
	lwz r9,12(r31)
	addi r9,r9,1
	stw r9,12(r31)
_shopList_L6:
	lwz r9,12(r31)
	cmpwi cr0,r9,3999
	ble cr0,_shopList_L15
	lwz r9,76(r31)
	mr r3,r9
	addi r11,r31,96
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
setKnowledgeBit:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	stw r5,48(r31)
	bl GetKnowledgePtr
	mr r9,r3
	stw r9,12(r31)
	li r9,19364
	stw r9,16(r31)
	li r9,15364
	stw r9,20(r31)
	lwz r9,16(r31)
	stw r9,8(r31)
	lwz r9,48(r31)
	cmpwi cr0,r9,0
	bne cr0,_shopList_L18
	lwz r9,20(r31)
	stw r9,8(r31)
_shopList_L18:
	lwz r10,8(r31)
	lwz r9,40(r31)
	add r9,r10,r9
	lwz r10,12(r31)
	add r9,r10,r9
	stw r9,24(r31)
	lwz r9,24(r31)
	lbz r9,0(r9)
	mr r10,r9
	lwz r9,44(r31)
	or r9,r10,r9
	mr r10,r9
	lwz r9,24(r31)
	stb r10,0(r9)
	nop
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_shopList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

GetKnowledgePtr = 0x027fb934
GetBlueprintPtr = 0x027fbae4


