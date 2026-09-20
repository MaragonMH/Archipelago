[Archipelago_keyChanges]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07, 0xF882D5CF, 0x218F6E07, 0x30B6E091 # 1.0.1E, 1.0.2U, 1.0.0E, 1.0.1E, 1.0.0E, 1.0.2U
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
disableImportantItems:
	.int    $disableImportantItems
disableBlueprints:
	.int    $disableBlueprints
drifterRangedWeapon:
	.int    $drifterRangedWeapon
drifterMeleeWeapon:
	.int    $drifterMeleeWeapon
includeShopBlueprints:
	.int    $includeShopBlueprints
includeShopArmor:
	.int    $includeShopArmor
includeShopWeapons:
	.int    $includeShopWeapons
includeShopAugments:
	.int    $includeShopAugments
includeShopSkellArmor:
	.int    $includeShopSkellArmor
includeShopSkellWeapons:
	.int    $includeShopSkellWeapons
includeShopSkellAugments:
	.int    $includeShopSkellAugments
includeShopSkellFrames:
	.int    $includeShopSkellFrames
fastRunSpeedFloat:
	.float    $fastRunSpeedFloat
fasterRunSpeedFloat:
	.float    $fasterRunSpeedFloat
fastRunningState:
	.int    0
fasterRunPlaySound:
	.int    0
fasterRunningState:
	.int    0
_augmentMenuType:
	.int    0
_filterDevices:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r30,24(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r4,8(r31)
	mr r9,r30
	addi r9,r9,428
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,4
	bne cr0,_keyChanges_L2
	mr r9,r6
	cmpwi cr0,r9,0
	blt cr0,_keyChanges_L3
	mr r9,r6
	cmpwi cr0,r9,1
	bgt cr0,_keyChanges_L3
	lis r9,includeShopAugments@ha
	lwz r9,includeShopAugments@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L4
	lis r9,disableGroundAugments@ha
	lwz r9,disableGroundAugments@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L4
	li r9,485
	stw r9,8(r31)
	b _keyChanges_L3
_keyChanges_L4:
	lis r9,_augmentMenuType@ha
	li r10,0
	stw r10,_augmentMenuType@l(r9)
	bl _getArchipelagoShop
_keyChanges_L3:
	mr r9,r6
	cmpwi cr0,r9,1
	ble cr0,_keyChanges_L6
	mr r9,r6
	cmpwi cr0,r9,4
	bgt cr0,_keyChanges_L6
	lis r9,includeShopSkellAugments@ha
	lwz r9,includeShopSkellAugments@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L7
	lis r9,disableSkellAugments@ha
	lwz r9,disableSkellAugments@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L7
	li r9,485
	stw r9,8(r31)
	b _keyChanges_L6
_keyChanges_L7:
	lis r9,_augmentMenuType@ha
	li r10,1
	stw r10,_augmentMenuType@l(r9)
	bl _getArchipelagoShop
	b _keyChanges_L6
_keyChanges_L2:
	mr r9,r30
	addi r9,r9,428
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,3
	bne cr0,_keyChanges_L6
	lis r9,includeShopBlueprints@ha
	lwz r9,includeShopBlueprints@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L9
	li r9,485
	stw r9,8(r31)
	b _keyChanges_L6
_keyChanges_L9:
	bl _getArchipelagoShop
_keyChanges_L6:
	lwz r4,8(r31)
	cmpwi cr0, r4, 0
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r30,-8(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
makeWpnItemListAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lis r9,includeShopWeapons@ha
	lwz r9,includeShopWeapons@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L11
	lis r9,disableGroundWeapons@ha
	lwz r9,disableGroundWeapons@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L13
_keyChanges_L11:
	bl _getArchipelagoShop
	lwz r3,8(r31)
	bl makeWpnItemList
	b _keyChanges_L10
_keyChanges_L13:
	nop
_keyChanges_L10:
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
makeAmrItemListAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lis r9,includeShopArmor@ha
	lwz r9,includeShopArmor@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L15
	lis r9,disableGroundArmor@ha
	lwz r9,disableGroundArmor@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L17
_keyChanges_L15:
	bl _getArchipelagoShop
	lwz r3,8(r31)
	bl makeAmrItemList
	b _keyChanges_L14
_keyChanges_L17:
	nop
_keyChanges_L14:
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
makeDlWpnItemListAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lis r9,includeShopSkellWeapons@ha
	lwz r9,includeShopSkellWeapons@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L19
	lis r9,disableSkellWeapons@ha
	lwz r9,disableSkellWeapons@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L21
_keyChanges_L19:
	bl _getArchipelagoShop
	lwz r3,8(r31)
	bl makeDlWpnItemList
	b _keyChanges_L18
_keyChanges_L21:
	nop
_keyChanges_L18:
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
makeDlAmrItemListAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lis r9,includeShopSkellArmor@ha
	lwz r9,includeShopSkellArmor@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L23
	lis r9,disableSkellArmor@ha
	lwz r9,disableSkellArmor@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L25
_keyChanges_L23:
	bl _getArchipelagoShop
	lwz r3,8(r31)
	bl makeDlAmrItemList
	b _keyChanges_L22
_keyChanges_L25:
	nop
_keyChanges_L22:
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
makeDollItemListAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lis r9,includeShopSkellFrames@ha
	lwz r9,includeShopSkellFrames@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L29
	bl _getArchipelagoShop
	lwz r3,8(r31)
	bl makeDollItemList
	b _keyChanges_L26
_keyChanges_L29:
	nop
_keyChanges_L26:
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
reqMenuAddAugmentFromIdAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,20
	beq cr0,_keyChanges_L31
	lwz r9,8(r31)
	cmpwi cr0,r9,21
	bne cr0,_keyChanges_L32
_keyChanges_L31:
	lis r9,includeShopAugments@ha
	lwz r9,includeShopAugments@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L32
	li r5,0
	li r4,2
	lwz r3,12(r31)
	bl setKnowledgeBit
	b _keyChanges_L33
_keyChanges_L32:
	lwz r9,8(r31)
	cmpwi cr0,r9,21
	ble cr0,_keyChanges_L34
	lwz r9,8(r31)
	cmpwi cr0,r9,24
	bgt cr0,_keyChanges_L34
	lis r9,includeShopSkellAugments@ha
	lwz r9,includeShopSkellAugments@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L34
	li r5,1
	li r4,2
	lwz r3,12(r31)
	bl setKnowledgeBit
	b _keyChanges_L33
_keyChanges_L34:
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl reqMenuAddItemFromId
	nop
_keyChanges_L33:
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
reqMenuAddBlueprintFromIdAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	lis r9,includeShopBlueprints@ha
	lwz r9,includeShopBlueprints@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L37
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl reqMenuAddItemFromId
_keyChanges_L37:
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_getShopIdx:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	mr r9,r5
	stb r9,48(r31)
	lwz r3,40(r31)
	bl getFP
	mr r9,r3
	stw r9,20(r31)
	lwz r9,20(r31)
	addi r9,r9,14
	lhz r9,0(r9)
	extsh r9,r9
	stw r9,24(r31)
	lwz r9,20(r31)
	addi r9,r9,8
	lhz r9,0(r9)
	extsh r9,r9
	srawi r9,r9,1
	extsh r9,r9
	stw r9,28(r31)
	lwz r9,28(r31)
	addi r9,r9,-1
	stw r9,8(r31)
	lbz r9,48(r31)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L39
	lwz r9,8(r31)
	addi r9,r9,-1
	stw r9,8(r31)
_keyChanges_L39:
	li r9,0
	stw r9,12(r31)
_keyChanges_L44:
	li r9,0
	stw r9,16(r31)
	b _keyChanges_L40
_keyChanges_L43:
	lwz r10,12(r31)
	lwz r9,28(r31)
	mullw r10,r10,r9
	lwz r9,16(r31)
	add r9,r10,r9
	slwi r10,r9,1
	lwz r9,24(r31)
	add r9,r10,r9
	lwz r10,20(r31)
	add r9,r10,r9
	lhz r9,0(r9)
	extsh r9,r9
	stw r9,32(r31)
	lwz r10,44(r31)
	lwz r9,32(r31)
	cmpw cr0,r10,r9
	bne cr0,_keyChanges_L41
	lwz r10,12(r31)
	lwz r9,8(r31)
	mullw r10,r10,r9
	lwz r9,16(r31)
	add r9,r10,r9
	addi r9,r9,1
	b _keyChanges_L45
_keyChanges_L41:
	lwz r9,16(r31)
	addi r9,r9,1
	stw r9,16(r31)
_keyChanges_L40:
	lwz r10,16(r31)
	lwz r9,8(r31)
	cmpw cr0,r10,r9
	blt cr0,_keyChanges_L43
	lwz r9,12(r31)
	addi r9,r9,1
	stw r9,12(r31)
	b _keyChanges_L44
_keyChanges_L45:
	mr r3,r9
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_keyChanges_LC0:
	.string "SHP_AmrPC"
_keyChanges_LC1:
	.string "SHP_WpnPC"
_keyChanges_LC2:
	.string "SHP_AmrDL"
_keyChanges_LC3:
	.string "SHP_WpnDL"
reqMenuAddShopItemFromIdAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,0
	ble cr0,_keyChanges_L47
	lwz r9,8(r31)
	cmpwi cr0,r9,5
	bgt cr0,_keyChanges_L47
	lis r9,includeShopArmor@ha
	lwz r9,includeShopArmor@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L47
	li r5,0
	lwz r4,12(r31)
	lis r9,_keyChanges_LC0@ha
	addi r3,r9,_keyChanges_LC0@l
	bl _getShopIdx
	mr r9,r3
	li r5,0
	li r4,8
	mr r3,r9
	bl setKnowledgeBit
	b _keyChanges_L48
_keyChanges_L47:
	lwz r9,8(r31)
	cmpwi cr0,r9,5
	ble cr0,_keyChanges_L49
	lwz r9,8(r31)
	cmpwi cr0,r9,7
	bgt cr0,_keyChanges_L49
	lis r9,includeShopWeapons@ha
	lwz r9,includeShopWeapons@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L49
	li r5,1
	lwz r4,12(r31)
	lis r9,_keyChanges_LC1@ha
	addi r3,r9,_keyChanges_LC1@l
	bl _getShopIdx
	mr r9,r3
	li r5,0
	li r4,4
	mr r3,r9
	bl setKnowledgeBit
	b _keyChanges_L48
_keyChanges_L49:
	lwz r9,8(r31)
	cmpwi cr0,r9,9
	ble cr0,_keyChanges_L50
	lwz r9,8(r31)
	cmpwi cr0,r9,14
	bgt cr0,_keyChanges_L50
	lis r9,includeShopSkellArmor@ha
	lwz r9,includeShopSkellArmor@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L50
	li r5,0
	lwz r4,12(r31)
	lis r9,_keyChanges_LC2@ha
	addi r3,r9,_keyChanges_LC2@l
	bl _getShopIdx
	mr r9,r3
	li r5,1
	li r4,8
	mr r3,r9
	bl setKnowledgeBit
	b _keyChanges_L48
_keyChanges_L50:
	lwz r9,8(r31)
	cmpwi cr0,r9,14
	ble cr0,_keyChanges_L51
	lwz r9,8(r31)
	cmpwi cr0,r9,19
	bgt cr0,_keyChanges_L51
	lis r9,includeShopSkellWeapons@ha
	lwz r9,includeShopSkellWeapons@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L51
	li r5,0
	lwz r4,12(r31)
	lis r9,_keyChanges_LC3@ha
	addi r3,r9,_keyChanges_LC3@l
	bl _getShopIdx
	mr r9,r3
	li r5,1
	li r4,4
	mr r3,r9
	bl setKnowledgeBit
	b _keyChanges_L48
_keyChanges_L51:
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl reqMenuAddItemFromId
	nop
_keyChanges_L48:
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
BuyDollAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lis r9,includeShopSkellFrames@ha
	lwz r9,includeShopSkellFrames@l(r9)
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L54
	li r5,1
	li r4,16
	lwz r3,8(r31)
	bl setKnowledgeBit
_keyChanges_L54:
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
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
_IsReadyAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	li r3,26
	bl _hasPreciousItem
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L58
	lwz r3,8(r31)
	bl IsReady
	mr r9,r3
	b _keyChanges_L59
_keyChanges_L58:
	li r9,0
_keyChanges_L59:
	mr r3,r9
	addi r11,r31,32
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
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L61
	lis r9,menuBasePtr@ha
	lwz r9,menuBasePtr@l(r9)
	li r4,12
	mr r3,r9
	bl openHudTelop
	li r9,0
	b _keyChanges_L62
_keyChanges_L61:
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl chkLv
	mr r9,r3
	cntlzw r9,r9
	srwi r9,r9,5
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L63
	lis r9,menuBasePtr@ha
	lwz r9,menuBasePtr@l(r9)
	li r4,430
	mr r3,r9
	bl openHudTelop
	li r9,0
	b _keyChanges_L62
_keyChanges_L63:
	li r9,1
_keyChanges_L62:
	mr r3,r9
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_keyChanges_LC4:
	.string "CHR_ClassInfo"
_keyChanges_LC5:
	.string "ClassType"
_keyChanges_LC6:
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
	lis r9,_keyChanges_LC4@ha
	addi r3,r9,_keyChanges_LC4@l
	bl getFP
	mr r9,r3
	stw r9,8(r31)
	li r6,1
	lwz r5,64(r31)
	lis r9,_keyChanges_LC5@ha
	addi r4,r9,_keyChanges_LC5@l
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
	lis r9,_keyChanges_LC6@ha
	addi r5,r9,_keyChanges_LC6@l
	li r4,32
	mr r3,r10
	crxor cr6,cr6,cr6
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
_getDefaultSkellWeapon:
	stwu r1,-32(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	stw r6,20(r31)
	lwz r9,20(r31)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L67
	lis r9,0x2
	b _keyChanges_L68
_keyChanges_L67:
	lwz r9,20(r31)
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L69
	lis r9,0x1
	b _keyChanges_L68
_keyChanges_L69:
	li r9,0
_keyChanges_L68:
	mr r3,r9
	addi r11,r31,32
	lwz r31,-4(r11)
	mr r1,r11
	blr
_setRunSpeed:
	stwu r1,-16(r1)
	mflr r0
	stw r0,20(r1)
	stw r31,12(r1)
	mr r31,r1
	lis r9,fastRunSpeedFloat@ha
	lfs f0,fastRunSpeedFloat@l(r9)
	fmr f1,f0
	lis r9,fastRunningState@ha
	lwz r9,fastRunningState@l(r9)
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L72
	lis r9,fasterRunningState@ha
	lwz r9,fasterRunningState@l(r9)
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L72
	lis r9,fasterRunSpeedFloat@ha
	lfs f0,fasterRunSpeedFloat@l(r9)
	fmr f1,f0
	lis r9,fasterRunPlaySound@ha
	lwz r9,fasterRunPlaySound@l(r9)
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L72
	lis r9,fasterRunPlaySound@ha
	li r10,0
	stw r10,fasterRunPlaySound@l(r9)
	li r3,724
	bl _playSound
_keyChanges_L72:
	nop
	addi r11,r31,16
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_UpdateRunningState:
	stwu r1,-64(r1)
	stw r26,40(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	stw r26,8(r31)
	mr r10,r26
	lis r9,fastRunningState@ha
	stw r10,fastRunningState@l(r9)
	lis r9,fastRunningState@ha
	lwz r9,fastRunningState@l(r9)
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L74
	lis r9,fasterRunningState@ha
	li r10,0
	stw r10,fasterRunningState@l(r9)
_keyChanges_L74:
	lwz r26,8(r31)
	cmpwi cr0, r26, 0
	nop
	addi r11,r31,64
	lwz r26,-24(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
_ToggleSuperRunningState:
	stwu r1,-32(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	lis r9,fasterRunningState@ha
	lwz r9,fasterRunningState@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L76
	lis r9,fasterRunningState@ha
	li r10,1
	stw r10,fasterRunningState@l(r9)
	lis r9,fasterRunPlaySound@ha
	li r10,1
	stw r10,fasterRunPlaySound@l(r9)
	b _keyChanges_L77
_keyChanges_L76:
	lis r9,fasterRunningState@ha
	lwz r9,fasterRunningState@l(r9)
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L77
	lis r9,fasterRunningState@ha
	li r10,0
	stw r10,fasterRunningState@l(r9)
_keyChanges_L77:
	lwz r3,8(r31)
	cmpwi cr0, r3, 0
	nop
	addi r11,r31,32
	lwz r31,-4(r11)
	mr r1,r11
	blr
_FindSystemVariableByName:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	li r9,0
	stw r9,8(r31)
_keyChanges_L81:
	lwz r9,24(r31)
	addi r9,r9,12
	lwz r4,8(r31)
	mr r3,r9
	bl getValueName
	mr r9,r3
	mr r4,r9
	lwz r3,28(r31)
	lis r12,_after_keyChanges_2__strcmp@ha
	addi r12,r12,_after_keyChanges_2__strcmp@l
	mtlr r12
	lis r12,__strcmp@ha
	addi r12,r12,__strcmp@l
	mtctr r12
	bctr
_after_keyChanges_2__strcmp:
	mr r9,r3
	cntlzw r9,r9
	srwi r9,r9,5
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L79
	lwz r9,8(r31)
	b _keyChanges_L82
_keyChanges_L79:
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
	b _keyChanges_L81
_keyChanges_L82:
	mr r3,r9
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_keyChanges_LC7:
	.string "VF_MoveSpeedSwimRun"
_keyChanges_LC9:
	.string "VF_MoveSpeedSwimDash"
_InitCharaSystemVariables:
	stwu r1,-48(r1)
	mflr r0
	stw r0,52(r1)
	stw r30,40(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	lwz r9,24(r31)
	lwz r9,4(r9)
	stw r9,8(r31)
	lis r9,_keyChanges_LC7@ha
	addi r9,r9,_keyChanges_LC7@l
	stw r9,12(r31)
	lwz r9,8(r31)
	addi r30,r9,12
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl _FindSystemVariableByName
	mr r10,r3
	lis r9,_keyChanges_LC8@ha
	lfs f0,_keyChanges_LC8@l(r9)
	mr r4,r10
	mr r3,r30
	fmr f1,f0
	bl setValueFloat
	lis r9,_keyChanges_LC9@ha
	addi r9,r9,_keyChanges_LC9@l
	stw r9,12(r31)
	lwz r9,8(r31)
	addi r30,r9,12
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl _FindSystemVariableByName
	mr r10,r3
	lis r9,_keyChanges_LC10@ha
	lfs f0,_keyChanges_LC10@l(r9)
	mr r4,r10
	mr r3,r30
	fmr f1,f0
	bl setValueFloat
	nop
	addi r11,r31,48
	lwz r0,4(r11)
	mtlr r0
	lwz r30,-8(r11)
	lwz r31,-4(r11)
	mr r1,r11
	blr
_initImplCharaAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl _InitCharaSystemVariables
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl initImpl_EventCharacter
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_InitDollSystemVariables:
	stwu r1,-48(r1)
	stw r31,44(r1)
	mr r31,r1
	stw r3,24(r31)
	stw r4,28(r31)
	lwz r9,24(r31)
	lwz r9,4(r9)
	stw r9,8(r31)
	nop
	addi r11,r31,48
	lwz r31,-4(r11)
	mr r1,r11
	blr
_initImplDollAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl _InitDollSystemVariables
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl initImpl_UnitCharacter
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_SetBdatValue:
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
	lwz r3,40(r31)
	bl getFP
	mr r9,r3
	stw r9,8(r31)
	lwz r4,44(r31)
	lwz r3,8(r31)
	bl getMember
	mr r9,r3
	stw r9,12(r31)
	lwz r9,12(r31)
	lhz r9,0(r9)
	sth r9,16(r31)
	lwz r9,8(r31)
	addi r9,r9,14
	lhz r9,0(r9)
	extsh r9,r9
	stw r9,20(r31)
	lwz r9,8(r31)
	addi r9,r9,8
	lhz r9,0(r9)
	extsh r9,r9
	addi r10,r9,2
	lwz r9,48(r31)
	addi r9,r9,-1
	mullw r9,r10,r9
	stw r9,24(r31)
	lhz r9,16(r31)
	extsh r9,r9
	addi r9,r9,2
	lwz r10,8(r31)
	add r9,r10,r9
	lhz r9,0(r9)
	extsh r9,r9
	stw r9,28(r31)
	lwz r10,20(r31)
	lwz r9,24(r31)
	add r10,r10,r9
	lwz r9,28(r31)
	add r9,r10,r9
	lwz r10,8(r31)
	add r9,r10,r9
	stw r9,32(r31)
	lwz r9,56(r31)
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L88
	lwz r9,52(r31)
	mr r10,r9
	lwz r9,32(r31)
	stb r10,0(r9)
	b _keyChanges_L91
_keyChanges_L88:
	lwz r9,56(r31)
	cmpwi cr0,r9,2
	bne cr0,_keyChanges_L90
	lwz r9,52(r31)
	mr r10,r9
	lwz r9,32(r31)
	sth r10,0(r9)
	b _keyChanges_L91
_keyChanges_L90:
	lwz r9,56(r31)
	cmpwi cr0,r9,4
	bne cr0,_keyChanges_L91
	lwz r9,32(r31)
	lwz r10,52(r31)
	stw r10,0(r9)
_keyChanges_L91:
	nop
	addi r11,r31,80
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_keyChanges_LC11:
	.string "NearWeapon"
_keyChanges_LC12:
	.string "FarWeapon"
_keyChanges_LC13:
	.string "defNear"
_keyChanges_LC14:
	.string "defFar"
_Create_DataInit_Adjusted:
	stwu r1,-16(r1)
	mflr r0
	stw r0,20(r1)
	stw r31,12(r1)
	mr r31,r1
	lis r9,drifterMeleeWeapon@ha
	lwz r9,drifterMeleeWeapon@l(r9)
	li r7,1
	mr r6,r9
	li r5,1
	lis r9,_keyChanges_LC11@ha
	addi r4,r9,_keyChanges_LC11@l
	lis r9,_keyChanges_LC4@ha
	addi r3,r9,_keyChanges_LC4@l
	bl _SetBdatValue
	lis r9,drifterRangedWeapon@ha
	lwz r9,drifterRangedWeapon@l(r9)
	li r7,1
	mr r6,r9
	li r5,1
	lis r9,_keyChanges_LC12@ha
	addi r4,r9,_keyChanges_LC12@l
	lis r9,_keyChanges_LC4@ha
	addi r3,r9,_keyChanges_LC4@l
	bl _SetBdatValue
	lis r9,drifterMeleeWeapon@ha
	lwz r9,drifterMeleeWeapon@l(r9)
	li r7,2
	mr r6,r9
	li r5,1
	lis r9,_keyChanges_LC13@ha
	addi r4,r9,_keyChanges_LC13@l
	lis r9,_keyChanges_LC4@ha
	addi r3,r9,_keyChanges_LC4@l
	bl _SetBdatValue
	lis r9,drifterRangedWeapon@ha
	lwz r9,drifterRangedWeapon@l(r9)
	li r7,2
	mr r6,r9
	li r5,1
	lis r9,_keyChanges_LC14@ha
	addi r4,r9,_keyChanges_LC14@l
	lis r9,_keyChanges_LC4@ha
	addi r3,r9,_keyChanges_LC4@l
	bl _SetBdatValue
	bl Create_DataInit
	nop
	addi r11,r31,16
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_isUnlock:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	lwz r3,8(r31)
	bl getMyUnionNo
	mr r9,r3
	cntlzw r9,r9
	srwi r9,r9,5
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L94
	li r4,1
	lwz r3,8(r31)
	bl EntryUnion
_keyChanges_L94:
	li r3,28
	bl _hasPreciousItem
	mr r9,r3
	mr r3,r9
	addi r11,r31,32
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
	ble cr0,_keyChanges_L101
	lwz r9,8(r31)
	cmpwi cr0,r9,5
	bgt cr0,_keyChanges_L101
	lis r9,disableGroundArmor@ha
	lwz r9,disableGroundArmor@l(r9)
	b _keyChanges_L102
_keyChanges_L101:
	lwz r9,8(r31)
	cmpwi cr0,r9,5
	ble cr0,_keyChanges_L103
	lwz r9,8(r31)
	cmpwi cr0,r9,7
	bgt cr0,_keyChanges_L103
	lis r9,disableGroundWeapons@ha
	lwz r9,disableGroundWeapons@l(r9)
	b _keyChanges_L102
_keyChanges_L103:
	lwz r9,8(r31)
	cmpwi cr0,r9,9
	ble cr0,_keyChanges_L104
	lwz r9,8(r31)
	cmpwi cr0,r9,14
	bgt cr0,_keyChanges_L104
	lis r9,disableSkellArmor@ha
	lwz r9,disableSkellArmor@l(r9)
	b _keyChanges_L102
_keyChanges_L104:
	lwz r9,8(r31)
	cmpwi cr0,r9,14
	ble cr0,_keyChanges_L105
	lwz r9,8(r31)
	cmpwi cr0,r9,19
	bgt cr0,_keyChanges_L105
	lis r9,disableSkellWeapons@ha
	lwz r9,disableSkellWeapons@l(r9)
	b _keyChanges_L102
_keyChanges_L105:
	lwz r9,8(r31)
	cmpwi cr0,r9,19
	ble cr0,_keyChanges_L106
	lwz r9,8(r31)
	cmpwi cr0,r9,21
	bgt cr0,_keyChanges_L106
	lis r9,disableGroundAugments@ha
	lwz r9,disableGroundAugments@l(r9)
	b _keyChanges_L102
_keyChanges_L106:
	lwz r9,8(r31)
	cmpwi cr0,r9,21
	ble cr0,_keyChanges_L107
	lwz r9,8(r31)
	cmpwi cr0,r9,24
	bgt cr0,_keyChanges_L107
	lis r9,disableSkellAugments@ha
	lwz r9,disableSkellAugments@l(r9)
	b _keyChanges_L102
_keyChanges_L107:
	lwz r9,8(r31)
	cmpwi cr0,r9,29
	bne cr0,_keyChanges_L108
	lis r9,disableImportantItems@ha
	lwz r9,disableImportantItems@l(r9)
	b _keyChanges_L102
_keyChanges_L108:
	lwz r9,8(r31)
	cmpwi cr0,r9,65
	bne cr0,_keyChanges_L109
	lis r9,disableBlueprints@ha
	lwz r9,disableBlueprints@l(r9)
	b _keyChanges_L102
_keyChanges_L109:
	lwz r9,8(r31)
	cmpwi cr0,r9,23
	ble cr0,_keyChanges_L110
	lwz r9,8(r31)
	cmpwi cr0,r9,28
	beq cr0,_keyChanges_L110
	li r9,1
	b _keyChanges_L102
_keyChanges_L110:
	li r9,0
_keyChanges_L102:
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
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L112
	lwz r6,20(r31)
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl addItemEquipment
	mr r9,r3
	b _keyChanges_L113
_keyChanges_L112:
	li r9,0
_keyChanges_L113:
	mr r3,r9
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_addNumAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	stw r6,20(r31)
	lwz r3,12(r31)
	bl _checkType
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L117
	lwz r6,20(r31)
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl addNum
	nop
_keyChanges_L117:
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_addItemAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	lwz r3,8(r31)
	bl _checkType
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L119
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl addItem
	mr r9,r3
	b _keyChanges_L120
_keyChanges_L119:
	li r9,0
_keyChanges_L120:
	mr r3,r9
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_addInnerExpAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	lis r9,characterLevel@ha
	lwz r9,characterLevel@l(r9)
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L123
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl addInnerExp
_keyChanges_L123:
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_getFlagValAdjusted:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r30,24(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	stw r5,16(r31)
	stw r6,20(r31)
	mr r9,r30
	cmpwi cr0,r9,2
	bne cr0,_keyChanges_L125
	lwz r9,16(r31)
	cmpwi cr0,r9,246
	beq cr0,_keyChanges_L126
	lwz r9,16(r31)
	cmpwi cr0,r9,251
	beq cr0,_keyChanges_L126
	lwz r9,16(r31)
	cmpwi cr0,r9,256
	bne cr0,_keyChanges_L125
_keyChanges_L126:
	li r9,1
	b _keyChanges_L127
_keyChanges_L125:
	mr r9,r30
	cmpwi cr0,r9,7
	bne cr0,_keyChanges_L128
	lwz r9,16(r31)
	cmpwi cr0,r9,26
	beq cr0,_keyChanges_L129
	lwz r9,16(r31)
	cmpwi cr0,r9,27
	beq cr0,_keyChanges_L129
	lwz r9,16(r31)
	cmpwi cr0,r9,28
	bne cr0,_keyChanges_L128
_keyChanges_L129:
	li r9,1
	b _keyChanges_L127
_keyChanges_L128:
	mr r9,r30
	cmpwi cr0,r9,7
	bne cr0,_keyChanges_L130
	lwz r9,16(r31)
	cmpwi cr0,r9,32
	beq cr0,_keyChanges_L131
	lwz r9,16(r31)
	cmpwi cr0,r9,33
	beq cr0,_keyChanges_L131
	lwz r9,16(r31)
	cmpwi cr0,r9,34
	bne cr0,_keyChanges_L130
_keyChanges_L131:
	li r9,1
	b _keyChanges_L127
_keyChanges_L130:
	mr r9,r30
	cmpwi cr0,r9,7
	bne cr0,_keyChanges_L132
	lwz r9,16(r31)
	cmpwi cr0,r9,287
	beq cr0,_keyChanges_L133
	lwz r9,16(r31)
	cmpwi cr0,r9,288
	beq cr0,_keyChanges_L133
	lwz r9,16(r31)
	cmpwi cr0,r9,289
	bne cr0,_keyChanges_L132
_keyChanges_L133:
	li r9,1
	b _keyChanges_L127
_keyChanges_L132:
	mr r9,r30
	cmpwi cr0,r9,7
	bne cr0,_keyChanges_L134
	lwz r9,16(r31)
	cmpwi cr0,r9,550
	beq cr0,_keyChanges_L135
	lwz r9,16(r31)
	cmpwi cr0,r9,551
	beq cr0,_keyChanges_L135
	lwz r9,16(r31)
	cmpwi cr0,r9,552
	bne cr0,_keyChanges_L134
_keyChanges_L135:
	li r9,1
	b _keyChanges_L127
_keyChanges_L134:
	mr r9,r30
	cmpwi cr0,r9,7
	bne cr0,_keyChanges_L136
	lwz r9,16(r31)
	cmpwi cr0,r9,810
	beq cr0,_keyChanges_L137
	lwz r9,16(r31)
	cmpwi cr0,r9,811
	beq cr0,_keyChanges_L137
	lwz r9,16(r31)
	cmpwi cr0,r9,812
	bne cr0,_keyChanges_L136
_keyChanges_L137:
	li r9,1
	b _keyChanges_L127
_keyChanges_L136:
	mr r9,r30
	cmpwi cr0,r9,6
	bne cr0,_keyChanges_L138
	lwz r9,16(r31)
	cmpwi cr0,r9,1587
	beq cr0,_keyChanges_L139
	lwz r9,16(r31)
	cmpwi cr0,r9,1588
	beq cr0,_keyChanges_L139
	lwz r9,16(r31)
	cmpwi cr0,r9,1589
	bne cr0,_keyChanges_L138
_keyChanges_L139:
	li r9,1
	b _keyChanges_L127
_keyChanges_L138:
	mr r9,r30
	cmpwi cr0,r9,6
	bne cr0,_keyChanges_L140
	lwz r9,16(r31)
	cmpwi cr0,r9,1590
	beq cr0,_keyChanges_L141
	lwz r9,16(r31)
	cmpwi cr0,r9,1591
	beq cr0,_keyChanges_L141
	lwz r9,16(r31)
	cmpwi cr0,r9,1592
	bne cr0,_keyChanges_L140
_keyChanges_L141:
	li r9,1
	b _keyChanges_L127
_keyChanges_L140:
	lwz r6,20(r31)
	lwz r5,16(r31)
	lwz r4,12(r31)
	lwz r3,8(r31)
	bl getFlagVal
	mr r9,r3
	nop
_keyChanges_L127:
	mr r3,r9
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r30,-8(r11)
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
	b _keyChanges_L143
_keyChanges_L145:
	lwz r6,12(r31)
	lwz r5,32(r31)
	lwz r4,28(r31)
	lwz r3,24(r31)
	bl getItem
	mr r9,r3
	lbz r9,0(r9)
	rlwinm r9,r9,0,24,31
	stw r9,20(r31)
	lwz r3,20(r31)
	bl _checkType
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L144
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_keyChanges_L144:
	lwz r9,12(r31)
	addi r9,r9,1
	stw r9,12(r31)
_keyChanges_L143:
	lwz r10,12(r31)
	lwz r9,16(r31)
	cmpw cr0,r10,r9
	blt cr0,_keyChanges_L145
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
	rlwinm r9,r9,0,24,31
	stw r9,8(r31)
	lwz r3,8(r31)
	bl _checkType
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L148
	lwz r9,40(r31)
	addi r9,r9,28
	stw r9,40(r31)
_keyChanges_L148:
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
	bge cr0,_keyChanges_L151
	li r9,1
	b _keyChanges_L152
_keyChanges_L151:
	li r9,0
_keyChanges_L152:
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
	bne cr0,_keyChanges_L154
	li r3,28
	bl _hasPreciousItem
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L155
	lis r9,bladeTerminalScenarioFlagPtr@ha
	li r10,0
	stw r10,bladeTerminalScenarioFlagPtr@l(r9)
	b _keyChanges_L154
_keyChanges_L155:
	lis r9,bladeTerminalScenarioFlagPtr@ha
	lis r10,0x7f
	ori r10,r10,0xffff
	stw r10,bladeTerminalScenarioFlagPtr@l(r9)
_keyChanges_L154:
	lis r9,shopTerminalScenarioFlagPtr@ha
	lwz r9,shopTerminalScenarioFlagPtr@l(r9)
	cmpwi cr0,r9,2001
	bne cr0,_keyChanges_L158
	li r3,28
	bl _hasPreciousItem
	mr r9,r3
	addic r10,r9,-1
	subfe r9,r10,r9
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L157
	lis r9,shopTerminalScenarioFlagPtr@ha
	li r10,0
	stw r10,shopTerminalScenarioFlagPtr@l(r9)
	b _keyChanges_L158
_keyChanges_L157:
	lis r9,shopTerminalScenarioFlagPtr@ha
	lis r10,0x7f
	ori r10,r10,0xffff
	stw r10,shopTerminalScenarioFlagPtr@l(r9)
_keyChanges_L158:
	nop
	addi r11,r31,16
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
	bne cr0,_keyChanges_L160
	lis r9,_itemLoopEnd@ha
	addi r9,r9,_itemLoopEnd@l
	mtctr r9
	bctr
_keyChanges_L160:
	lis r9,_itemLoopStart@ha
	addi r9,r9,_itemLoopStart@l
	mtctr r9
	bctr
_setLocal:
	stwu r1,-32(r1)
	mflr r0
	stw r0,36(r1)
	stw r31,28(r1)
	mr r31,r1
	stw r3,8(r31)
	stw r4,12(r31)
	lwz r9,8(r31)
	cmpwi cr0,r9,2
	bne cr0,_keyChanges_L162
	mr r9,r5
	cmpwi cr0,r9,1
	bne cr0,_keyChanges_L162
	lis r9,_collepediaFlag@ha
	lwz r9,_collepediaFlag@l(r9)
	lwz r10,12(r31)
	cmpw cr0,r10,r9
	beq cr0,_keyChanges_L163
	lis r9,_bladeFlag@ha
	lwz r9,_bladeFlag@l(r9)
	lwz r10,12(r31)
	cmpw cr0,r10,r9
	bne cr0,_keyChanges_L164
_keyChanges_L163:
	li r3,28
	bl _hasPreciousItem
	mr r9,r3
	cmpwi cr0,r9,0
	bne cr0,_keyChanges_L164
	li r9,1
	b _keyChanges_L165
_keyChanges_L164:
	li r9,0
_keyChanges_L165:
	rlwinm r9,r9,0,24,31
	cmpwi cr0,r9,0
	beq cr0,_keyChanges_L162
	li r5,0
_keyChanges_L162:
	lis r9, 0x103a
	nop
	addi r11,r31,32
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr
_keyChanges_LC8:
	.long   1077936128
_keyChanges_LC10:
	.long   1092616192


[Archipelago_keyChanges_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E
0x021b70bc = bl _IsPermit # replace getLocal inside IsPermit with new check
0x022e9920 = nop # restructure online skell flight module check to always use this one
0x022e9934 = bl _loadSkyUnit # replace online skell flight module call with own
0x027d6da0 = bl _loadFNet # replace getScenarioFlag for initial load
0x027d5748 = blr # return original call to changeScenarioFlag Fnet

# doll overdrive
IsReady = 0x021ccdec
0x024bf00c = bl _IsReadyAdjusted

# affinity quests no longer lock you out of other quests
0x022ce6c4 = li r3,0

# disable lock party from affinity quests
0x02296518 = nop
0x02290ca4 = nop

# max out fuel for doll with one refill
0x025ce838 = nop

# division points disable until KEY Blade license
0x02847ef8 = bl _isUnlock
0x02847fbc = bl _isUnlock
# join division only if you get blade license, otherwise not
EntryUnion = 0x0288e3f4
getMyUnionNo = 0x0288d380
0x0288e418 = nop

0x022e2c24 = nop # dont set all the arts/skills/classes if you change your Class
0x020c48c4 = blr # disable Class exp
0x020c63d8 = blr # disable friend exp
# disable character exp
addInnerExp = 0x020c395c
0x022953b4 = b _addInnerExpAdjusted
0x02562504 = bl _addInnerExpAdjusted

# remove all equipment for new playable characters
0x027e43d0 = nop # replace setupPcArmor
0x027e4474 = nop 
0x027e44e8 = bl _getDefaultWeapon
0x027e4558 = bl _getDefaultWeapon

# remove arts/skills for new playable characters
0x026a52e8 = blr # disable OpenArts::CharacterData
0x026a5308 = blr # disable OpenSkills::CharacterData
0x027e41f8 = b 0x027e4334 # disable automatic skill asignment
# remove reequip of assault hammer and flame granade for drifter
0x022736ec = lis r3, 0
0x02273734 = lis r3, 0
# set drifter weapon types
Create_DataInit = 0x27e2388
0x027e4768 = bl _Create_DataInit_Adjusted

# remove all equipment for new skells
# replace setupDollArmor
0x027ea5f0 = nop
0x027ea664 = nop
0x027ea6d8 = nop
0x027ea74c = nop
0x027ea7c0 = nop
# replace setupDollWeapon
0x027ea834 = bl _getDefaultSkellWeapon
0x027ea8ac = bl _getDefaultSkellWeapon
0x027ea94c = nop
0x027ea9c4 = nop
0x027eaa3c = nop

# filter quest rewards
addNum = 0x02779870
0x0229572c = bl _addRewardItemEquipment
0x022957c4 = bl _addRewardItemEquipment
0x0229585c = bl _addRewardItemEquipment
0x022958f4 = bl _addRewardItemEquipment
# filter treasure box rewards
0x022d8d50 = bl _addRewardItemEquipment
# disable itembox full message for the above
0x022d8dc4 = nop
# filter mission event rewards
# important items
0x027a3f28 = bl _addNumAdjusted 
0x027a3fb8 = bl _addNumAdjusted
# pop items
addItem = 0x02365934
0x02389ef0 = bl _addItemAdjusted
# collectables
# 0x027a4008 = bl _addNumAdjusted
# 0x027a4098 = bl _addNumAdjusted
# materials
# 0x027a40e8 = bl _addNumAdjusted
# 0x027a4178 = bl _addNumAdjusted
# 0x42 unkown probably info
# 0x027a41c8 = bl _addNumAdjusted
# 0x027a4258 = bl _addNumAdjusted
# data probes
0x027a42a8 = bl _addNumAdjusted
0x027a4338 = bl _addNumAdjusted
# ground weapons
0x027a4410 = bl _addNumAdjusted
# 0x44 unkown
# 0x027a45ac = bl _addNumAdjusted
# 0x027a463c = bl _addNumAdjusted

# disable field skills
0x0238e138 = nop

0x02814cf4 = b _prepareBladeTerminal # in loadEnd::ScriptManager

# overwrite setLocal for blade flag
0x0228f018 = bl _setLocal

# add new run speed
0x0264332c = bl _setRunSpeed
0x0240ab90 = stw r0, +0x14(r1) # swap order with following instruction
0x0240ab94 = bl _ToggleSuperRunningState
0x025051ec = bl _UpdateRunningState

# set movement variables
setValueFloat = 0x02003148
setValueBool = 0x02003178
setValueInt = 0x0200a5d0
getMappedId = 02007f90
getValueName = 0x020030e0
0x0263b660 = bl _initImplCharaAdjusted # innerChara
initImpl_EventCharacter = 0x02635b80
0x02617f04 = bl _initImplDollAdjusted # doll
initImpl_UnitCharacter = 0x02612524


addItemEquipment = 0x02366cf0 # ::ItemBox::ItemType::Type::ItemHandle
getItem = 0x021ab180 # ::ItemDrop::ItemDropManager
getItemNum = 0x021ab164 # ::ItemDrop::ItemDropManager


[Archipelago_keyChanges_V101E]
moduleMatches = 0xF882D5CF, 0x218F6E07 # 1.0.1E, 1.0.0E

0x02b051a4 = bl _assignDollCheck # replace lvlCheck with dollLicense + lvlCheck
0x02b051c4 = nop # remove original error message

# join division only if you get blade license
0x02c20118 = nop

# disable getting skell after skell license quest in doll_present
0x029cc078 = nop # disable doll creation
0x029cc088 = nop # disable doll assign

# bdat changes at startup
getMember = 0x029c1ddc

# required quest items from equipment disallow sell
0x02b73a20 = bl _getFlagValAdjusted

# filter enemy rewards
0x02b07540 = bl _getItemNumAdjusted
0x02b076d4 = b _preItemLoopAdjustment
_itemLoopStart = 0x02b07584
_itemLoopEnd = 0x02b076e8

# disable affinity quest arts reward
0x029c7dc0 = li r3,0

__strcmp = 0x03b16c50

# reconfigure BladeTerminal Locks
bladeTerminalScenarioFlagPtr = 0x20343604
shopTerminalScenarioFlagPtr = 0x20343634

# mandatory disable shops
0x02a79100 = bl _filterDevices  # blueprints + augments
0x02a7ced4 = nop  # doll blueprints
# optional shops # need paramaterization
makeWpnItemList = 0x02a2ca6c
0x02a326d0 = bl makeWpnItemListAdjusted
makeAmrItemList = 0x02a2da48
0x02a326f8 = bl makeAmrItemListAdjusted
makeDlWpnItemList = 0x02a2e608
0x02a32720 = bl makeDlWpnItemListAdjusted
makeDlAmrItemList = 0x02a2f088
0x02a32748 = bl makeDlAmrItemListAdjusted
makeDollItemList = 0x02a2fc78
0x02a32770 = bl makeDollItemListAdjusted
# shop equip no longer upgrades but rather adds the new tiers
0x02a2ca08 = nop  # ground
0x02a2e5a4 = nop  # doll

# mark shop locations
0x02a8334c = bl reqMenuAddAugmentFromIdAdjusted
0x02a7ccfc = bl reqMenuAddBlueprintFromIdAdjusted
0x02a40c00 = bl BuyDollAdjusted  # doll frame shop
0x02a402a4 = bl reqMenuAddShopItemFromIdAdjusted

# disable items from collepedia
0x02a0acf4 = nop

# miranium get not decreased after lshop upgrade
0x02a40ecc = nop

# extend system log duration
0x02c04440 = li r9, 0xff

openHudTelop = 0x02c91f3c # ::MenuTask
chkLv = 0x02af8e7c # ::menu::MenuDollGarage


[Archipelago_keyChanges_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

0x02b05194 = bl _assignDollCheck # replace lvlCheck with dollLicense + lvlCheck
0x02b051b4 = nop # remove original error message

# join divison only if blade license
0x02c20124 = nop

# disable getting skell after skell license quest in doll_present
0x029cc068 = nop # disable doll creation
0x029cc078 = nop # disable doll assign

# bdat changes at startup
getMember = 0x029c1dcc

# required quest items from equipment disallow sell
0x02b73a10 = bl _getFlagValAdjusted

# filter enemy rewards
0x02b07530 = bl _getItemNumAdjusted
0x02b076c4 = b _preItemLoopAdjustment
_itemLoopStart = 0x02b07574
_itemLoopEnd = 0x02b076d8

# disable affinity quest arts reward
0x029c7db0 = li r3,0

__strcmp = 0x03b16bd0

# reconfigure BladeTerminal Locks
bladeTerminalScenarioFlagPtr = 0x20343604-0xB821D
shopTerminalScenarioFlagPtr = 0x20343634-0xB821D

# mandatory disable shops
0x02a790f0 = bl _filterDevices
0x02a7cec4 = nop  # doll blueprints
# optional shops # need paramaterization
makeWpnItemList = 0x02a2ca5c
0x02a326c0 = bl makeWpnItemListAdjusted
makeAmrItemList = 0x02a2da38
0x02a326e8 = bl makeAmrItemListAdjusted
makeDlWpnItemList = 0x02a2e5f8
0x02a32710 = bl makeDlWpnItemListAdjusted
makeDlAmrItemList = 0x02a2f078
0x02a32738 = bl makeDlAmrItemListAdjusted
makeDollItemList = 0x02a2fc68
0x02a32760 = bl makeDollItemListAdjusted
# shop equip no longer upgrades but rather adds the new tiers
0x02a2c9f8 = nop  # ground
0x02a2e594 = nop  # doll

# mark shop locations
0x02a8333c = bl reqMenuAddAugmentFromIdAdjusted
0x02a7ccec = bl reqMenuAddBlueprintFromIdAdjusted
0x02a40bf0 = bl BuyDollAdjusted  # doll frame shop
0x02a40294 = bl reqMenuAddShopItemFromIdAdjusted

# disable items from collepedia
0x02a0ace4 = nop

# miranium get not decreased after lshop upgrade
0x02a40ebc = nop

# extend system log duration
0x02c04430 = li r9, 0xff

openHudTelop = 0x02c91edc # ::MenuTask
chkLv = 0x02af8e6c # ::menu::MenuDollGarage


