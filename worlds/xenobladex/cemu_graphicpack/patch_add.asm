[Archipelago_add]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
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
	bl reqMenuAddItemFromId
	b _add_L4
_add_L2:
	addi r9,r31,12
	mr r3,r9
	bl addGarage
_add_L4:
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_addGear:
	stwu r1,-80(r1)
	mflr r0
	stw r0,84(r1)
	stw r31,76(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	stw r5,48(r31)
	stw r6,52(r31)
	stw r7,56(r31)
	stw r8,60(r31)
	lwz r9,44(r31)
	slwi r10,r9,19
	lwz r9,40(r31)
	slwi r9,r9,13
	add r10,r10,r9
	addi r9,r31,12
	addi r10,r10,8
	stw r10,0(r9)
	lwz r9,48(r31)
	slwi r9,r9,4
	sth r9,24(r31)
	lwz r9,52(r31)
	slwi r9,r9,4
	sth r9,26(r31)
	lwz r9,56(r31)
	slwi r9,r9,4
	sth r9,28(r31)
	li r9,0
	stw r9,8(r31)
	b _add_L6
_add_L9:
	lwz r10,8(r31)
	lwz r9,60(r31)
	cmpw cr0,r10,r9
	bge cr0,_add_L7
	lwz r9,8(r31)
	addi r9,r9,9
	slwi r9,r9,1
	addi r10,r31,8
	add r9,r10,r9
	addi r9,r9,4
	li r10,0
	sth r10,0(r9)
	b _add_L8
_add_L7:
	lwz r9,8(r31)
	addi r9,r9,9
	slwi r9,r9,1
	addi r10,r31,8
	add r9,r10,r9
	addi r9,r9,4
	li r10,-1
	sth r10,0(r9)
_add_L8:
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_add_L6:
	lwz r9,8(r31)
	cmpwi cr0,r9,2
	ble cr0,_add_L9
	addi r9,r31,12
	li r4,1
	mr r3,r9
	bl reqMenuAddItemFromInfo
	nop
	addi r11,r31,80
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
	lis r9,itemListBase@ha
	addi r9,r9,itemListBase@l
	stw r9,16(r31)
	li r4,29
	lwz r3,16(r31)
	bl getItemTypeInfo
	mr r9,r3
	lwz r9,0(r9)
	stw r9,8(r31)
	li r9,0
	stw r9,12(r31)
	b _add_L11
_add_L16:
	lwz r9,8(r31)
	lwz r9,0(r9)
	slwi r9,r9,13
	srwi r9,r9,26
	stw r9,20(r31)
	lwz r9,20(r31)
	cmpwi cr0,r9,29
	bne cr0,_add_L17
	lwz r9,8(r31)
	lwz r9,0(r9)
	srwi r9,r9,19
	stw r9,24(r31)
	lwz r9,40(r31)
	lwz r10,24(r31)
	cmpw cr0,r10,r9
	bne cr0,_add_L14
	li r9,1
	b _add_L15
_add_L14:
	lwz r9,8(r31)
	addi r9,r9,12
	stw r9,8(r31)
	lwz r9,12(r31)
	addi r9,r9,1
	stw r9,12(r31)
_add_L11:
	lwz r9,12(r31)
	cmpwi cr0,r9,299
	ble cr0,_add_L16
	b _add_L13
_add_L17:
	nop
_add_L13:
	li r9,0
_add_L15:
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
	b _add_L19
_add_L20:
	lwz r3,8(r31)
	bl GetCharaDataPtr
	mr r9,r3
	li r6,0
	lwz r5,28(r31)
	lwz r4,24(r31)
	mr r3,r9
	bl reqMenuSetArtsLevel
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_add_L19:
	lwz r9,8(r31)
	cmpwi cr0,r9,18
	ble cr0,_add_L20
	nop
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
	b _add_L22
_add_L23:
	lwz r3,8(r31)
	bl GetCharaDataPtr
	mr r9,r3
	li r6,0
	lwz r5,28(r31)
	lwz r4,24(r31)
	mr r3,r9
	bl reqMenuSetSkillLevel
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_add_L22:
	lwz r9,8(r31)
	cmpwi cr0,r9,18
	ble cr0,_add_L23
	nop
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
	bl SetFriendRank
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
	lis r9,_fieldSkillOffset@ha
	lwz r9,_fieldSkillOffset@l(r9)
	mr r10,r9
	lwz r9,8(r31)
	add r9,r9,r10
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
	bne cr0,_add_L27
	lwz r5,28(r31)
	li r4,1
	li r3,16
	bl setLocal
	b _add_L28
_add_L27:
	lwz r9,24(r31)
	cmpwi cr0,r9,6
	bne cr0,_add_L29
	li r4,0
	addi r9,r31,8
	mr r3,r9
	bl getCharaHandle
	addi r9,r31,8
	mr r4,r9
	li r3,0
	bl SetDead
	b _add_L28
_add_L29:
	lwz r9,24(r31)
	cmpwi cr0,r9,7
	bne cr0,_add_L30
	li r3,0
	bl _reqForceDamagePlayerTargetGoner
	b _add_L28
_add_L30:
	lwz r9,24(r31)
	cmpwi cr0,r9,8
	bne cr0,_add_L31
	lis r9,fnetBasePtr@ha
	lwz r9,fnetBasePtr@l(r9)
	lwz r4,28(r31)
	mr r3,r9
	bl changeScenarioFlag
	b _add_L28
_add_L31:
	lwz r9,24(r31)
	cmpwi cr0,r9,9
	bne cr0,_add_L32
	li r5,1
	lwz r4,28(r31)
	li r3,1
	bl setLocal
	b _add_L28
_add_L32:
	lwz r9,24(r31)
	addi r9,r9,23
	mr r4,r9
	li r3,29
	bl _addItem
_add_L28:
	lwz r9,24(r31)
	cmpwi cr0,r9,1
	bne cr0,_add_L33
	lwz r5,28(r31)
	li r4,24155
	li r3,1
	bl setLocal
	b _add_L38
_add_L33:
	lwz r9,24(r31)
	cmpwi cr0,r9,2
	bne cr0,_add_L35
	lwz r5,28(r31)
	li r4,30224
	li r3,1
	bl setLocal
	b _add_L38
_add_L35:
	lwz r9,24(r31)
	cmpwi cr0,r9,3
	bne cr0,_add_L36
	lwz r5,28(r31)
	li r4,27587
	li r3,1
	bl setLocal
	b _add_L38
_add_L36:
	lwz r9,24(r31)
	cmpwi cr0,r9,4
	bne cr0,_add_L37
	lis r9,fnetBasePtr@ha
	lwz r10,fnetBasePtr@l(r9)
	lwz r9,28(r31)
	mulli r9,r9,3001
	mr r4,r9
	mr r3,r10
	bl changeScenarioFlag
	b _add_L38
_add_L37:
	lwz r9,24(r31)
	cmpwi cr0,r9,5
	bne cr0,_add_L38
	li r5,3
	li r4,4742
	li r3,2
	bl setLocal
	li r5,3
	li r4,4744
	li r3,2
	bl setLocal
_add_L38:
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
	bl GetClassDataPtr
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


[Archipelago_add_V101E]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

reqMenuAddItemFromId = 0x0234f1a8 # ::CmdReq
reqMenuAddItemFromInfo = 0x0234f5ec # ::CmdReq
reqMenuSetArtsLevel = 0x02347c1c # ::CmdReq
reqMenuSetSkillLevel = 0x02348b0c # ::CmdReq
SetFriendRank = 0x027faee0 # ::Util
GetClassDataPtr = 0x027fa7a0 # ::Util

_reqForceDamagePlayerTargetGoner = 0x021a88e4
SetDead = 0x0298f2f0
getCharaHandle = 0x02373b9c

GetCharaDataPtr = 0x027f70ac # ::Util
setLocal = 0x0228f008 # ::GameFlag
changeScenarioFlag = 0x027d5638 # ::FNet
addGarage = 0x0234c620 # ::CmdCommon::SceneCmdPrm


