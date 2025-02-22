[Archipelago_enemyList]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07, 0xF882D5CF, 0x218F6E07, 0x30B6E091 # 1.0.1E, 1.0.2U, 1.0.0E, 1.0.1E, 1.0.0E, 1.0.2U
.origin = codecave

_formatEnemyText:
	.string "EN Id=%03x Fg=%01x:"
_enemyList_LC0:
	.string "CHR_EnList"
_enemyList_LC1:
	.string "BTL_EnBook"
_enemyList_LC2:
	.string "BaseEnemyID"
_enemyList_LC3:
	.string "mBoss"
_enemyList_LC4:
	.string "Flag"
_enemyList_LC5:
	.string "Named"
_postEnemyList:
	stwu r1,-64(r1)
	mflr r0
	stw r0,68(r1)
	stw r31,60(r1)
	mr r31,r1
	stw r3,40(r31)
	stw r4,44(r31)
	stw r5,48(r31)
	stw r6,52(r31)
	li r9,1404
	stw r9,16(r31)
	lis r9,_enemyList_LC0@ha
	addi r3,r9,_enemyList_LC0@l
	bl getFP
	mr r9,r3
	stw r9,20(r31)
	lis r9,_enemyList_LC1@ha
	addi r3,r9,_enemyList_LC1@l
	bl getFP
	mr r9,r3
	stw r9,24(r31)
	li r9,1
	stw r9,8(r31)
	b _enemyList_L2
_enemyList_L8:
	lwz r3,8(r31)
	bl GetEnBookDefeat
	mr r9,r3
	stw r9,12(r31)
	lwz r9,12(r31)
	cmpwi cr0,r9,0
	ble cr0,_enemyList_L3
	lwz r5,8(r31)
	lis r9,_enemyList_LC2@ha
	addi r4,r9,_enemyList_LC2@l
	lwz r3,24(r31)
	bl getVal
	mr r9,r3
	srawi r9,r9,16
	stw r9,28(r31)
	lis r9,_enemyList_LC3@ha
	addi r6,r9,_enemyList_LC3@l
	lwz r5,28(r31)
	lis r9,_enemyList_LC4@ha
	addi r4,r9,_enemyList_LC4@l
	lwz r3,20(r31)
	bl getFlagVal
	mr r9,r3
	stw r9,32(r31)
	lis r9,_enemyList_LC5@ha
	addi r6,r9,_enemyList_LC5@l
	lwz r5,28(r31)
	lis r9,_enemyList_LC4@ha
	addi r4,r9,_enemyList_LC4@l
	lwz r3,20(r31)
	bl getFlagVal
	mr r9,r3
	stw r9,36(r31)
	lwz r9,12(r31)
	cmpwi cr0,r9,2
	bgt cr0,_enemyList_L4
	lwz r9,32(r31)
	cmpwi cr0,r9,0
	bne cr0,_enemyList_L4
	lwz r9,36(r31)
	cmpwi cr0,r9,0
	beq cr0,_enemyList_L5
_enemyList_L4:
	li r9,1
	stw r9,12(r31)
	b _enemyList_L3
_enemyList_L5:
	li r9,0
	stw r9,12(r31)
_enemyList_L3:
	lwz r10,52(r31)
	lwz r7,12(r31)
	lwz r6,8(r31)
	lis r9,_formatEnemyText@ha
	addi r5,r9,_formatEnemyText@l
	mr r4,r10
	lwz r3,44(r31)
	crxor 6,6,6
	lis r12,_after_enemyList_1__sprintf_s@ha
	addi r12,r12,_after_enemyList_1__sprintf_s@l
	mtlr r12
	lis r12,__sprintf_s@ha
	addi r12,r12,__sprintf_s@l
	mtctr r12
	bctr
_after_enemyList_1__sprintf_s:
	mr r9,r3
	mr r10,r9
	lwz r9,44(r31)
	add r9,r9,r10
	stw r9,44(r31)
	lwz r10,44(r31)
	lwz r9,48(r31)
	cmplw cr0,r10,r9
	ble cr0,_enemyList_L7
	lwz r3,40(r31)
	bl _postCurl
	lwz r9,40(r31)
	stw r9,44(r31)
_enemyList_L7:
	lwz r9,8(r31)
	addi r9,r9,1
	stw r9,8(r31)
_enemyList_L2:
	lwz r10,8(r31)
	lwz r9,16(r31)
	cmpw cr0,r10,r9
	blt cr0,_enemyList_L8
	lwz r9,44(r31)
	mr r3,r9
	addi r11,r31,64
	lwz r0,4(r11)
	mtlr r0
	lwz r31,-4(r11)
	mr r1,r11
	blr


[Archipelago_enemyList_ALL]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 # 1.0.1E, 1.0.2U, 1.0.0E

GetEnBookDefeat = 0x027fcb70 # ::Util


[Archipelago_enemyList_V101E]
moduleMatches = 0xF882D5CF, 0x218F6E07 # 1.0.1E, 1.0.0E

getVal = 0x029c2120 # ::bdat
getFlagVal = 0x029c254c # ::bdat


[Archipelago_enemyList_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

getVal = 0x029c2110 # ::bdat
getFlagVal = 0x029c253c # ::bdat


