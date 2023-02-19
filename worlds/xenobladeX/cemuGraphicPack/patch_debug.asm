[XCX_Archipelago_debug]
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x7672271D, 0x218F6E07, 0xAB97DE6B, 0x676EB33E, 0x785CA8A9 ; 1.0.1E, 1.0.2U, 1.0.2J, 1.0.0E, 1.0.1U, 1.0.0U, 1.0.0J
.origin = codecave

_debug_LC0:
        .string "Debug Message"
writeDebug:
        stwu r1,-32(r1)
        mflr r0
        stw r0,36(r1)
        stw r31,28(r1)
        mr r31,r1
        stw r3,8(r31)
        lis r9,_menuBasePtr@ha
        lwz r10,_menuBasePtr@l(r9)
        lwz r5,8(r31)
        lis r9,_debug_LC0@ha
        addi r4,r9,_debug_LC0@l
        mr r3,r10
        bl writeSystemLog
        nop
        addi r11,r31,32
        lwz r0,4(r11)
        mtlr r0
        lwz r31,-4(r11)
        mr r1,r11
        blr

# VERSION SPECIFIC ###############################################################

[XCX_Archipelago_debug_V101E] ; ###############################################
moduleMatches = 0xF882D5CF, 0x218F6E07 ; 1.0.1E, 1.0.0E

##################################################################################
[XCX_Archipelago_debug_V102U]
moduleMatches = 0x30B6E091 # 1.0.2U

##################################################################################
[XCX_Archipelago_debug_V100U]
moduleMatches = 0xAB97DE6B, 0x676EB33E # 1.0.1U, 1.0.0U

##################################################################################
[XCX_Archipelago_debug_V102J]
moduleMatches = 0x7672271D # 1.0.2J

##################################################################################
[XCX_Archipelago_debug_V100J]
moduleMatches = 0x785CA8A9 # 1.0.0J
