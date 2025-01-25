#include <cstddef>

int __sprintf_s(char *buffer, size_t sizeOfBuffer, const char *format, ...);

void _postCurl(char[]);

#ifdef V101E
moduleMatches = 0xF882D5CF, 0x30B6E091, 0x218F6E07 ; 1.0.1E, 1.0.2U, 1.0.0E

GetEnBookDiscovery = 0x027fcab4 # ::Util
#endif

char _formatEnemyText[] = "EN Id=%03x Dc=%01x:";

int GetEnBookDiscovery(int id);


// Use  https://xenoblade.github.io/xbx/bdat/common_local_us/BTL_EnBook.html to match the ids
// Defeat: Number of enemies you defeated
// Discovery(Dc): 0, 1, 2. 0 = Not discovered yet (will appear as ??? in menu), 
// 1 = encountered in combat, 2 = fully researched (white dot in menu)
char* _postEnemyList(char* stringStartPtr, char* stringCurrentPtr, char* stringEndPtr, int maxEntrySize) {
	int enemyCount = 1404;
    for(int enemyId = 1; enemyId < enemyCount; enemyId++){
		int discovery = GetEnBookDiscovery(enemyId);
		// optional: int defeat = getEnBookDefeat(enemyId);
		stringCurrentPtr += __sprintf_s(stringCurrentPtr, maxEntrySize, _formatEnemyText, enemyId, discovery);

		// Reset buffer
		if(stringCurrentPtr > stringEndPtr){
			_postCurl(stringStartPtr);
			stringCurrentPtr = stringStartPtr;
		}
    }
	return stringCurrentPtr;
}