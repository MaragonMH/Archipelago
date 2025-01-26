[Archipelago_keyChanges]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
.origin = codecave

disableGroundArmor:
	.int    $disableGroundArmor
disableGroundWeapons:
	.int    $disableGroundWeapons
disableSkellArmor:
	.int    $disableSkellArmor
disableSkellWeapons:
	.int    $disableSkellWeapons
disableGroundAugments:
	.int    $disableGroundAugments
disableSkellAugments:
	.int    $disableSkellAugments
_IsPermit:
	stwu r1,-16(r1)
	mflr r0
	stw r0,20(r1)
	stw r31,12(r1)
	mr r31,r1
	li r3,26
	bl _hasPreciousItem
	mr r9,r3
	mr r3,r9
	addi r11,r31,16
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_assignDollCheck:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	li r3,24
	bl _hasPreciousItem
	mr r9,r3
	cntlzw r9,r9
	srwi r9,r9,5
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L4
	lis r9,menuBasePtr@ha
	lwz r9,menuBasePtr@l(r9)
	li r4,12
	mr r3,r9
	bl openHudTelop
	li r9,0
	b _keyChanges_L5
_keyChanges_L4:
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl chkLv
	mr r9,r3
	cntlzw r9,r9
	srwi r9,r9,5
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L6
	lis r9,menuBasePtr@ha
	lwz r9,menuBasePtr@l(r9)
	li r4,430
	mr r3,r9
	bl openHudTelop
	li r9,0
	b _keyChanges_L5
_keyChanges_L6:
	li r9,1
_keyChanges_L5:
	mr r3,r9
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_keyChanges_LC0:
	.string "CHR_ClassInfo"
_keyChanges_LC1:
	.string "ClassType"
_keyChanges_LC2:
	.string "%sWeapon"
_getDefaultWeapon:
	stwu r1,-80(r1)
	mflr r0
	stw r0,84(r1)
	stw r31,76(r1)
	mr r31,r1
	stw r3,56(r31)
	stw r4,60(r31)
	stw r5,64(r31)
	stw r6,68(r31)
	lis r9,_keyChanges_LC0@ha
	addi r3,r9,_keyChanges_LC0@l
	bl getFP
	mr r9,r3
	stw r9,8(r31)
	li r6,1
	lwz r5,64(r31)
	lis r9,_keyChanges_LC1@ha
	addi r4,r9,_keyChanges_LC1@l
	lwz r3,56(r31)
	bl getValCheck
	mr r9,r3
	srawi r9,r9,24
	stw r9,12(r31)
	lwz r9,60(r31)
	addi r9,r9,6
	stw r9,16(r31)
	addi r10,r31,20
	lwz r6,16(r31)
	lis r9,_keyChanges_LC2@ha
	addi r5,r9,_keyChanges_LC2@l
	li r4,32
	mr r3,r10
	crxor 6,6,6
	lis r12,_after_keyChanges_1__sprintf_s@ha
	addi r12,r12,_after_keyChanges_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_keyChanges_1__sprintf_s:
	addi r9,r31,20
	li r6,1
	lwz r5,12(r31)
	mr r4,r9
	lwz r3,8(r31)
	bl getValCheck
	mr r9,r3
	srawi r9,r9,8
	mr r3,r9
	addi r11,r31,80
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_loadSkyUnit:
	stwu r1,-16(r1)
	mflr r0
	stw r0,20(r1)
	stw r31,12(r1)
	mr r31,r1
	li r3,25
	bl _hasPreciousItem
	mr r9,r3
	mr r3,r9
	addi r11,r31,16
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_loadFNet:
	stwu r1,-16(r1)
	mflr r0
	stw r0,20(r1)
	stw r31,12(r1)
	mr r31,r1
	li r3,27
	bl _hasPreciousItem
	mr r9,r3
	mulli r9,r9,3001
	mr r3,r9
	addi r11,r31,16
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_checkType:
	stwu r1,-32(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	ble cr0,_keyChanges_L14
	lwz r9,8(r31)
	cmpwi cr0,r9,5
	bgt cr0,_keyChanges_L14
	lis r9,disableGroundArmor@ha
	lwz r9,disableGroundArmor@l(r9)
	b _keyChanges_L15
_keyChanges_L14:
	lwz r9,8(r31)
	cmpwi cr0,r9,5
	ble cr0,_keyChanges_L16
	lwz r9,8(r31)
	cmpwi cr0,r9,7
	bgt cr0,_keyChanges_L16
	lis r9,disableGroundWeapons@ha
	lwz r9,disableGroundWeapons@l(r9)
	b _keyChanges_L15
_keyChanges_L16:
	lwz r9,8(r31)
	cmpwi cr0,r9,9
	ble cr0,_keyChanges_L17
	lwz r9,8(r31)
	cmpwi cr0,r9,14
	bgt cr0,_keyChanges_L17
	lis r9,disableSkellArmor@ha
	lwz r9,disableSkellArmor@l(r9)
	b _keyChanges_L15
_keyChanges_L17:
	lwz r9,8(r31)
	cmpwi cr0,r9,14
	ble cr0,_keyChanges_L18
	lwz r9,8(r31)
	cmpwi cr0,r9,19
	bgt cr0,_keyChanges_L18
	lis r9,disableSkellWeapons@ha
	lwz r9,disableSkellWeapons@l(r9)
	b _keyChanges_L15
_keyChanges_L18:
	lwz r9,8(r31)
	cmpwi cr0,r9,19
	ble cr0,_keyChanges_L19
	lwz r9,8(r31)
	cmpwi cr0,r9,21
	bgt cr0,_keyChanges_L19
	lis r9,disableGroundAugments@ha
	lwz r9,disableGroundAugments@l(r9)
	b _keyChanges_L15
_keyChanges_L19:
	lwz r9,8(r31)
	cmpwi cr0,r9,21
	ble cr0,_keyChanges_L20
	lwz r9,8(r31)
	cmpwi cr0,r9,24
	bgt cr0,_keyChanges_L20
	lis r9,disableSkellAugments@ha
	lwz r9,disableSkellAugments@l(r9)
	b _keyChanges_L15
_keyChanges_L20:
	lwz r9,8(r31)
	cmpwi cr0,r9,23
	ble cr0,_keyChanges_L21
	lwz r9,8(r31)
	cmpwi cr0,r9,28
	beq cr0,_keyChanges_L21
	li r9,1
	b _keyChanges_L15
_keyChanges_L21:
	li r9,0
_keyChanges_L15:
	mr r3,r9
	addi r11,r31,32
	lwz r31,-4(r11)
	mr r1,r11
	blr
_addRewardItemEquipment:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	stw r6,20(r31)
	lwz r3,8(r31)
	bl _checkType
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L23
	lwz r6,20(r31)
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl addItemEquipment
	mr r9,r3
	b _keyChanges_L24
_keyChanges_L23:
	li r9,0
_keyChanges_L24:
	mr r3,r9
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_getItemNumAdjusted:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	li r9,0
	stw r9,8(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getItemNum
	mr r9,r3
	stw r9,16(r31)
	li r9,0
	stw r9,12(r31)
	b _keyChanges_L26
_keyChanges_L28:
	lwz r6,12(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getItem
	mr r9,r3
	lbz r9,0(r9)
	stw r9,20(r31)
	lwz r3,20(r31)
	bl _checkType
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L27
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_keyChanges_L27:
	lwz r9,12(r31)
	addi r9,r9,1
	stw r9,12(r31)
_keyChanges_L26:
	lwz r10,12(r31)
	lwz r9,16(r31)
	cmpw cr0,r10,r9
	blt cr0,_keyChanges_L28
	lwz r9,8(r31)
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_itemLoopAdjustment:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	stw r6,36(r31)
	stw r7,40(r31)
	lwz r6,36(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getItem
	mr r9,r3
	lbz r9,0(r9)
	stw r9,8(r31)
	lwz r3,8(r31)
	bl _checkType
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L31
	lwz r9,40(r31)
	addi r9,r9,28
	stw r9,40(r31)
_keyChanges_L31:
	lwz r9,40(r31)
	mr r3,r9
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_itemLoopContinue:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r5,32(r31)
	stw r6,36(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getItemNum
	mr r9,r3
	stw r9,8(r31)
	lwz r10,36(r31)
	lwz r9,8(r31)
	cmpw cr0,r10,r9
	bge cr0,_keyChanges_L34
	li r9,1
	b _keyChanges_L35
_keyChanges_L34:
	li r9,0
_keyChanges_L35:
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_prepareBladeTerminal:
	stwu r1,-16(r1)
	mflr r0
	stw r0,20(r1)
	stw r31,12(r1)
	mr r31,r1
	lis r9,bladeTerminalScenarioFlagPtr@ha
	lwz r9,bladeTerminalScenarioFlagPtr@l(r9)
	cmpwi cr0,r9,3001
	bne cr0,_keyChanges_L37
	li r3,28
	bl _hasPreciousItem
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L38
	lis r9,bladeTerminalScenarioFlagPtr@ha
	li r10,0
	stw r10,bladeTerminalScenarioFlagPtr@l(r9)
	b _keyChanges_L37
_keyChanges_L38:
	lis r9,bladeTerminalScenarioFlagPtr@ha
	lis r10,0x7f
	ori r10,r10,0xffff
	stw r10,bladeTerminalScenarioFlagPtr@l(r9)
_keyChanges_L37:
	lis r9,shopTerminalScenarioFlagPtr@ha
	lwz r9,shopTerminalScenarioFlagPtr@l(r9)
	cmpwi cr0,r9,2001
	bne cr0,_keyChanges_L41
	li r3,28
	bl _hasPreciousItem
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L40
	lis r9,shopTerminalScenarioFlagPtr@ha
	li r10,0
	stw r10,shopTerminalScenarioFlagPtr@l(r9)
	b _keyChanges_L41
_keyChanges_L40:
	lis r9,shopTerminalScenarioFlagPtr@ha
	lis r10,0x7f
	ori r10,r10,0xffff
	stw r10,shopTerminalScenarioFlagPtr@l(r9)
_keyChanges_L41:
	nop
	addi r11,r31,16
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_keyChanges_LC3:
	.string "fld_console.sb"
_prepareRentalCharTerminal:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	lwz r9,24(r31)
	lwz r9,164(r9)
	stw r9,8(r31)
	lis r9,_keyChanges_LC3@ha
	addi r4,r9,_keyChanges_LC3@l
	lwz r3,8(r31)
	lis r12,_after_keyChanges_2__strcmp@ha
	addi r12,r12,_after_keyChanges_2__strcmp@l
	mtlr r12
	lis r12,__strcmp@ha
	addi r12,r12,__strcmp@l
	mtctr r12
	bctr
_after_keyChanges_2__strcmp:
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L43
	lwz r3,24(r31)
	bl beginScript
	mr r9,r3
	b _keyChanges_L44
_keyChanges_L43:
	lwz r9,8(r31)
	lwz r9,36(r9)
	stw r9,12(r31)
	lwz r9,12(r31)
	cmpwi cr0,r9,2
	bne cr0,_keyChanges_L45
	li r3,28
	bl _hasPreciousItem
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L46
	lwz r9,24(r31)
	addi r9,r9,608
	mr r3,r9
	bl beginScript
	mr r9,r3
	b _keyChanges_L44
_keyChanges_L46:
	lis r9,menuBasePtr@ha
	lwz r9,menuBasePtr@l(r9)
	li r4,52
	mr r3,r9
	bl openHudTelop
	li r9,0
	b _keyChanges_L44
_keyChanges_L45:
	lwz r9,12(r31)
	cmpwi cr0,r9,11
	bne cr0,_keyChanges_L47
	lwz r9,24(r31)
	addi r9,r9,-608
	mr r3,r9
	bl beginScript
	mr r9,r3
	b _keyChanges_L44
_keyChanges_L47:
	lwz r3,24(r31)
	bl beginScript
	mr r9,r3
	nop
_keyChanges_L44:
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_preItemLoopAdjustmentWrapper:
	stwu r1,-80(r1)
	mflr r0
	stw r0,84(r1)
	stw r18,24(r1)
	stw r20,32(r1)
	stw r22,40(r1)
	stw r23,44(r1)
	stw r31,76(r1)
	mr r31,r1
_preItemLoopAdjustment:
	mr r9,r31
	mr r10,r22
	mr r8,r20
	mr r6,r18
	mr r7,r23
	mr r5,r8
	mr r4,r10
	mr r3,r9
	bl _itemLoopAdjustment
	mr r9,r3
	mr r23,r9
	mr r9,r31
	mr r10,r22
	mr r8,r20
	mr r7,r18
	mr r6,r7
	mr r5,r8
	mr r4,r10
	mr r3,r9
	bl _itemLoopContinue
	mr r9,r3
	stw r9,8(r31)
	mr r9,r18
	addi r9,r9,1
	mr r18,r9
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L49
	lis r9,_itemLoopEnd@ha
	addi r9,r9,_itemLoopEnd@l
	mtctr r9
	bctr
_keyChanges_L49:
	lis r9,_itemLoopStart@ha
	addi r9,r9,_itemLoopStart@l
	mtctr r9
	bctr
_setLocal:
	stwu r1,-32(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,2
	bne cr0,_keyChanges_L51
	mr r9,r5
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L51
	lwz r9,12(r31)
	cmpwi cr0,r9,4744
	beq cr0,_keyChanges_L52
	lwz r9,12(r31)
	cmpwi cr0,r9,4742
	bne cr0,_keyChanges_L51
_keyChanges_L52:
	li r5,0
_keyChanges_L51:
	lis r9, 0x103a
	nop
	addi r11,r31,32
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_keyChanges_V101E]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
0x021b70bc = bl _IsPermit # replace getLocal inside IsPermit with new check
0x02b051a4 = bl _assignDollCheck # replace lvlCheck with dollLicense + lvlCheck
0x02b051c4 = nop # remove original error message
0x022e9920 = nop # restructure online skell flight module check to always use this one
0x022e9934 = bl _loadSkyUnit # replace online skell flight module call with own
0x027d6da0 = bl _loadFNet # replace getScenarioFlag for initial load
0x027d5748 = blr # return original call to changeScenarioFlag Fnet

0x022e2c24 = nop # dont set all the arts/skills/classes if you change your Class
0x020c48c4 = blr # disable Class exp
0x020c63d8 = blr # disable friend exp

# remove all equipment for new playable characters
0x027e2100 = blr # armor
0x027e44e8 = bl _getDefaultWeapon
0x027e4558 = bl _getDefaultWeapon

# remove arts/skills for new playable characters
0x026a52e8 = blr # disable OpenArts::CharacterData
0x026a5308 = blr # disable OpenSkills::CharacterData
0x027e41f8 = b 0x027e4334 # disable automatic skill asignment

# remove all equipment for new skells
0x027e2110 = blr # armor
0x027e2108 = blr # weapon

# filter quest rewards
0x0229572c = bl _addRewardItemEquipment
0x022957c4 = bl _addRewardItemEquipment
0x0229585c = bl _addRewardItemEquipment
0x022958f4 = bl _addRewardItemEquipment
# filter treasure box rewards
0x022d8d50 = bl _addRewardItemEquipment
# filter enemy rewards
0x02b07540 = bl _getItemNumAdjusted
0x02b076d4 = b _preItemLoopAdjustment
_itemLoopStart = 0x02b07584
_itemLoopEnd = 0x02b076e8

# disable field skills
0x0238e138 = nop

# disable affinity quest arts reward
0x029c7dc0 = li r3,0

# reconfigure BladeTerminal Locks
bladeTerminalScenarioFlagPtr = 0x20343604
shopTerminalScenarioFlagPtr = 0x20343634
0x02814cf4 = b _prepareBladeTerminal # in loadEnd::ScriptManager

# reconfigure rentalCharTerminal to LShop
__strcmp = 0x03b16c50
0x028eacc8 = bl _prepareRentalCharTerminal
beginScript = 0x028cb70c # ::Gimmick::GimmickMapObj

# mandatory disable shops
0x02a32770 = nop # skell frame
0x02a69954 = nop # augment menu
0x02a69968 = nop # develop menu
# optional shops # need paramaterization
0x02a326d0 = nop # ground weapon
0x02a326f8 = nop # ground armor
0x02a32720 = nop # skell weapon
0x02a32748 = nop # skell armor

# overwrite setLocal for blade flag
0x0228f018 = bl _setLocal

menuBasePtr = 0x1038ae50 # from error::menu::BladeHomeMenu
openHudTelop = 0x02c91f3c # ::MenuTask
chkLv = 0x02af8e7c # ::menu::MenuDollGarage
addItemEquipment = 0x02366cf0 # ::ItemBox::ItemType::Type::ItemHandle
getItem = 0x021ab180 # ::ItemDrop::ItemDropManager
getItemNum = 0x021ab164 # ::ItemDrop::ItemDropManager


