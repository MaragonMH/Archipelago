// Use https://godbolt.org/ with power gcc.
// Use vscode with https://marketplace.visualstudio.com/items?itemName=OGoodness.powerpc-syntax
// and https://marketplace.visualstudio.com/items?itemName=bhughes339.replacerules
// Adjust your settings:
// "replacerules.rules": {
//     "Replace invalid Labels": {
//         "find": "[.](LC?[0-9]+)",
//         "replace": "_NAME_$1",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Remove all function brackets": {
//         "find": "[(](?!r?[1-3]?[0-9]).*[)]",
//         "replace": "",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Add register prefix to all easy numbers": {
//         "find": "(?<=[ ,(])([1-3]?[0-9])(?=[),])",
//         "replace": "r$1",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Add register prefix to all complex numbers": {
//         "find": "(?<!^.*i.*,)(?<=[, ])([1-3]?[0-9])(?=[\n])",
//         "replace": "r$1",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Remove prefix from crxor": {
//         "find": "crxor r([0-9]+),r([0-9]+),r([0-9]+)",
//         "replace": "crxor $1,$2,$3",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Restructure la instructions": {
//         "find": "la (r[1-3]?[0-9]),(.*)[(](r[1-3]?[0-9])[)]",
//         "replace": "addi $1,$3,$2",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Restructure condition instructions": {
//         "find": "(cmp[a-z]*|b[a-z]*) (r[0-7])",
//         "replace": "$1 c$2",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Handle target out of range error for internal functions": {
//         "find": "bl (__.*)",
//         "replace": "lis r12, after$1@ha\n\t\taddi r12, r12, after$1@l\n\t\tmtlr r12\n\t\tlis r12, $1@ha\n\t\taddi r12, r12, $1@l\n\t\tmtctr r12\n\t\tbctr\nafter$1:",
//         "languages": [
//             "asm"
//         ]
//     },
//     "Remove rlwinm, this could lead to errors": {
//         "find": ".*rlwinm .*[\n]",
//         "replace": "",
//         "languages": [
//             "asm"
//         ]
//     },
// },
// "replacerules.rulesets": {
//     "Convert PPC Assembly to format for Cemu Graphic Packs": {
//         "rules": [
//             "Replace invalid Labels",
//             "Remove all function brackets",
//             "Add register prefix to all easy numbers",
//             "Add register prefix to all complex numbers",
//             "Remove prefix from crxor",
//             "Restructure la instructions",
//             "Restructure condition instructions",
//             "Handle target out of range error for internal functions",
//             "Remove rlwinm, this could lead to errors",
//         ]
//     }
// },
// Run the new ruleset to adjust your .asm code
// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/SEG_NormalList.html to match the ids
#include <cstddef>
int* segmentBasePtr; // from another file
char _formatFnNodeText[] = "FN Id=%03x Fg=%01x AId=%02x:";  // First %08x Second %05x Third %05x Fourth %05x Fifth %05x Sixth %05x Seventh %05x:";

// Start
// declare the required functions here. These need to be located inside your game
// IMPORTANT: If you get the "target NAME out of range" exception, use two leading "_"

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

int checkDP(short id); // ::FNetDataAccessor
// End

void _postCurl(char[]);

char* _postFnNodeList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
    int* areaOffset = segmentBasePtr;
    areaOffset += 0x4;
    for(int areaId = 0; areaId < 0x15; areaId++){
        for(int* fnNodeOffset = areaOffset + 0x4; *fnNodeOffset != 0; fnNodeOffset += 0x7){
            int nodeId = (short)fnNodeOffset[2];
            int flag = checkDP(nodeId);
			int type = fnNodeOffset[1] >> 0x18;

            if(type != 1) continue;

            stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatFnNodeText, nodeId, flag, areaId);

            // Reset buffer
            if(stringCurrentPtr > stringEndPtr){
                _postCurl(stringStartPtr);
                stringCurrentPtr = stringStartPtr;
            }
        }
        areaOffset += 0x7f7;
    }
    return stringCurrentPtr;
}