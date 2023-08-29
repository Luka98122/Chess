#include "pch.h"
#include <iostream>
#include <stdio.h>
#include <string>

using namespace std;


class vec2 {
	public:
		int x;
		int y;
		vec2(int x=0, int y=0) {
			this->x = x;
			this->y = y;
		}
};

class CMove {
	public:
		vec2 from;
		vec2 to;
		CMove(const vec2 &from, const vec2 &to) {
			this->from = from;
			this->to = to;
		}
};



int add(int a, int b) {
	return a + b;
}

// ♜♞♝♛♚♟♖♘♗♕♔♙
string* debugMakeBoard() {
	string board[8];
	board[0] = "♜♞♝♛♚♝♞♜";
	board[1] = "♟♟♟♟♟♟♟♟";
	board[2] = "ፙፙፙፙፙፙፙፙ";
	board[3] = "ፙፙፙፙፙፙፙፙ";
	board[4] = "ፙፙፙፙፙፙፙፙ";
	board[5] = "ፙፙፙፙፙፙፙፙ";
	board[6] = "♙♙♙♙♙♙♙♙";
	board[7] = "♖♘♗♕♔♗♘♖";
	return board;
}

vector<vector<int>> testBoard = {
//   0 1  2  3 4 5 6 7
	{0,0,  0,0,0,0,0,0}, // 0
	{1,1,  1,1,1,1,1,1}, // 1
	{0,0, -2,0,0,0,1,0}, // 2
	{0,0,  0,0,0,0,0,1}, // 3
	{0,0,  0,0,2,0,0,0}, // 4
	{0,-1,-1,0,0,-2,0,0}, // 5
	{-1,0,0,-1,0,0,0,0}, // 6
	{0,0,  0,0,0,0,0,2}  // 7
};

vector<vector<int>> makeBoard() {
	vector<vector<int>> board = {
		{2,3,4,5,6,4,3,2},
		{1,1,1,1,1,1,1,1},
		{0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0},
		{-1,-1,-1,-1,-1,-1,-1,-1},
		{-2,-3,-4,-5,-6,-4,-3,-2}
	};
	return board;
}

int demos() {
	int num1;
	printf("Number a: ");
	scanf("%d", &num1);
	int num2;
	printf("Number b: ");
	scanf("%d", &num2);

	int number = add(num1, num2);

	string numberStr = to_string(number);

	printf(numberStr.c_str());
	return 0;
}

vector<CMove> pawnMoves(int y,int x, vector<vector<int>> board) {
	int dy = board[y][x];
	vector<CMove> moves;
	if (board[y + dy][x] == 0) {
		CMove move(vec2(x, y), vec2(x, y + dy));
		moves.push_back(move);
	}
	if (x - 1 >= 0 && x - 1 < 8 && y + dy > 0 && y + dy < 8) {
		if (board[y + dy][x - 1] != 0) {
			if (dy == -1 && board[y + dy][x - 1] < 0) {

			}
			else if (dy == 1 && board[y + dy][x - 1] > 0) {

			}
			else {
				CMove move(vec2(x, y), vec2(x - 1, y + dy));
				moves.push_back(move);
			}
		}
	}
	
	if (x + 1 >= 0 && x + 1 < 8 && y + dy > 0 && y + dy < 8) {
		if (board[y + dy][x + 1] != 0) {
			if (dy == -1 && board[y + dy][x + 1] < 0) {

			}
			else if (dy == 1 && board[y + dy][x + 1] > 0) {

			}
			else {
				CMove move(vec2(x, y), vec2(x + 1, y + dy));
				moves.push_back(move);
			}
		}
	}

	if (y + dy * 2 < 8 && y + dy * 2 > 0) {
		int startPos = -5;
		if (dy == 1)
			startPos = 1;
		if (dy == -1)
			startPos = 6;

		if (y == startPos) {
			if (board[y + dy * 2][x] == 0) {
				CMove move(vec2(x, y), vec2(x, y + dy * 2));
				moves.push_back(move);
			}
		}
	}

	return moves;
}

vector<CMove> rookMoves(int y, int x, vector<vector<int>> board) {
	vector<CMove> moves;
	int color = board[y][x]/abs(board[y][x]);
	vector<vec2> directions{ {-1,0},{0,-1}, {1,0},{1,1} };
	for (int i = 0; i<4;i++) {
		vec2 direction = directions[i];
		for (int j = 1; j < 9;j++) {
			int newX = x+direction.x*j;
			int newY = y+direction.y*j;

			if (newX >= 0 && newX < 8 && newY >= 0 && newY < 8) {
				if (board[newY][newX] == 0) {
					CMove move(vec2(x, y), vec2(newX, newY));
					moves.push_back(move);

				}
				else {
					if (color == 1) {
						if (board[newY][newX] < 0) {
							CMove move(vec2(x, y), vec2(newX, newY));
							moves.push_back(move);
						}
						break;
					}
					
					if (color == -1) {
						if (board[newY][newX] > 0) {
							CMove move(vec2(x, y), vec2(newX, newY));
							moves.push_back(move);
						}
						break;
					}

				}
			}
			else {
				break;
			}

		}
	}
	return moves;
}

vector<CMove> knightMoves(int y, int x, vector<vector<int>> board) {
	vector<CMove> moves;
	vector<vec2> directions = { {-2,-1}, {-1,-2}, {1,-2}, {2,-1}, {2,1}, {1,2}, {-1,2}, {-2,1} };
	int color = board[y][x] / abs(board[y][x]);
	for (int i = 0; i < directions.size();i++) {
		int newX = x + directions[i].x;
		int newY = y + directions[i].y;
		if (newX >= 0 && newX < 8 && newY >= 0 && newY < 8) {
			if (board[newY][newX] == 0) {
				CMove move(vec2(x, y), vec2(newX, newY));
				moves.push_back(move);
			}
			else {
				if (color == 1) {
					if (board[newY][newX] < 0) {
						CMove move(vec2(x, y), vec2(newX, newY));
						moves.push_back(move);
					}
				}

				if (color == -1) {
					if (board[newY][newX] > 0) {
						CMove move(vec2(x, y), vec2(newX, newY));
						moves.push_back(move);
					}
				}

			}
		}
	}
	return moves;
}
vector<CMove> getMoves(vector<vector<int>> board) {
	vector<CMove> moves;
	for (int i = 0;i < size(board);i++) {
		printf("Hi\n");
		for (int j = 0; j < size(board); j++) { // Pawn
			/*
			if (abs(board[i][j]) == 1) {
				vector<CMove> subMoves;
				subMoves = pawnMoves(i, j, board);
				for (int i = 0; i < size(subMoves);i++) {
					moves.push_back(subMoves[i]);
				}
			}
			if (abs(board[i][j]) == 2) { // Rook
				vector<CMove> subMoves;
				subMoves = rookMoves(i, j, board);
				for (int k = 0; k < size(subMoves);k++) {
					CMove curMove = subMoves[k];
					moves.push_back(curMove);
				}
			}
			*/
			if (abs(board[i][j]) == 3) { // Knight
				vector<CMove> subMoves;
				subMoves = knightMoves(i, j, board);
				for (int k = 0; k < size(subMoves);k++) {
					CMove curMove = subMoves[k];
					moves.push_back(curMove);
				}
			}
		}
	}
	return moves;
}


int main()
{
	printf("Hello World!\n");
	vec2 v(3, 4);

	CMove m(v, vec2(7, 8));
	vector<CMove> moves;
	vector<vector<int>> board = makeBoard();
	moves = getMoves(board);
	int a = moves.size();
	//printf(to_string(a).c_str());

	for (int i = 0;i < 8;i++) {
		for (int j = 0; j < 8; j++) {
			testBoard[i][j] = 0;
		}
	}

	for (int i = 0; i < moves.size();i++) {
		vec2 from = moves[i].from;
		vec2 to = moves[i].to;

		testBoard[from.y][from.x] = 5;
		testBoard[to.y][to.x] = 4;

	}

	for (int i = 0;i < 8;i++) {
		string row = "";
		for (int j = 0; j < 8; j++) {
			row += to_string(testBoard[i][j]);
		}
		row = row + "\n";
		printf(row.c_str());
		row = "";
	}

	return 0;
}

