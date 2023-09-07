#include "pch.h"
#include "Helpers.h"

bool areMovesEqual(CMove move1, CMove move2) {
	if (move1.from.x == move2.from.x && move1.from.y == move2.from.y && move1.to.x == move2.to.x && move1.to.y == move2.to.y) {
		return true;
	}
	return false;
}
