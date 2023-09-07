#pragma once

class vec2 {
public:
	int x;
	int y;
	vec2(int x = 0, int y = 0) {
		this->x = x;
		this->y = y;
	}
};

class CMove {
public:
	vec2 from;
	vec2 to;
	CMove(const vec2& from = { 0,0 }, const vec2& to = { 0,0 }) {
		this->from = from;
		this->to = to;
	}
};

class ScoredMove {
public:
	CMove move;
	float score;
};

bool areMovesEqual(CMove move1, CMove move2);

