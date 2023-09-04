#include "pch.h"
#include <iostream>
#include <stdio.h>
#include <string>

#include <cstdio>
#include <windows.h>
#include <string>

#define MAX_INPUT_LENGTH 255

std::string readSpecialInput() {
	wchar_t wstr[MAX_INPUT_LENGTH];
	char mb_str[MAX_INPUT_LENGTH * 3 + 1];

	unsigned long read;
	void* con = GetStdHandle(STD_INPUT_HANDLE);

	ReadConsole(con, wstr, MAX_INPUT_LENGTH, &read, NULL);
	int size = WideCharToMultiByte(CP_UTF8, 0, wstr, read, mb_str, sizeof(mb_str), NULL, NULL);
	mb_str[size] = 0;

	return std::string(mb_str);
}

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
		CMove(const vec2 &from = {0,0}, const vec2& to = {0,0}) {
			this->from = from;
			this->to = to;
		}
};

class ScoredMove {
public:
	CMove move;
	float score;
};



int add(int a, int b) {
	return a + b;
}


void debugMove(CMove move) {
	printf("%dFrom x\n", move.from.x);
	printf("%dFrom y\n", move.from.y);
	printf("%dTo x\n", move.to.x);
	printf("%dTo y\n", move.to.y);
}

// ♜♞♝♛♚♟♖♘♗♕♔♙
void debugMakeBoard(vector<vector<int>> board) {
	/*
	string board[8];
	board[0] = "♜♞♝♛♚♝♞♜";
	board[1] = "♟♟♟♟♟♟♟♟";
	board[2] = "ፙፙፙፙፙፙፙፙ";
	board[3] = "ፙፙፙፙፙፙፙፙ";
	board[4] = "ፙፙፙፙፙፙፙፙ";
	board[5] = "ፙፙፙፙፙፙፙፙ";
	board[6] = "♙♙♙♙♙♙♙♙";
	board[7] = "♖♘♗♕♔♗♘♖";
	*/
	vector<string> boardic = {};
	for (int i = 0; i < 8;i++) {
		boardic.push_back("");
		for (int j = 0; j < 8; j++) {
			if (board[i][j] == 1)
				boardic[i] += "♟";
			else if (board[i][j] == 2)
				boardic[i] += "♜";
			else if (board[i][j] == 3)
				boardic[i] += "♞";
			else if (board[i][j] == 4)
				boardic[i] += "♝";
			else if (board[i][j] == 5)
				boardic[i] += "♛";
			else if (board[i][j] == 6)
				boardic[i] += "♚";
			// Other
			else if (board[i][j] == -1)
				boardic[i] += "♙";
			else if (board[i][j] == -2)
				boardic[i] += "♖";
			else if (board[i][j] == -3)
				boardic[i] += "♘";
			else if (board[i][j] == -4)
				boardic[i] += "♗";
			else if (board[i][j] == -5)
				boardic[i] += "♕";
			else if (board[i][j] == -6)
				boardic[i] += "♔";
			else if (board[i][j] == 0)
				boardic[i] += "ፙ";

		}
	}

	for (int i = 0;i < 8;i++) {
		printf((boardic[i]+"\n").c_str());
	}

}

vector<vector<int>> emptyTestBoard = {
	//   0 1  2  3 4 5 6 7
		{0,0,  0,0,0,0,0,0}, // 0
		{1,1,  1,1,1,1,1,1}, // 1
		{0,0,  0,0,0,0,0,0}, // 2
		{0,0,  0,0,0,0,0,0}, // 3
		{0,0,  0,0,0,0,0,0}, // 4
		{0,0,  0,0,0,0,0,0}, // 5
		{0,0,  0,0,0,0,0,0}, // 6
		{0,0,  0,0,0,0,0,0}  // 7
};

vector<vector<int>> testBoard = {
	//   0 1  2  3 4 5 6 7
		{0,0,  0,0,0,0,0,0}, // 0
		{1,1,  1,1,1,1,1,1}, // 1
		{0,0,  0,0,0,0,1,0}, // 2
		{0,0,  0,0,-6,0,0,1}, // 3
		{0,0,  0,0,0,0,0,0}, // 4
		{0,0,  0,0,6,0,0,0}, // 5
		{0,0,  0,0,0,0,0,0}, // 6
		{0,0,  0,2,0,2,0,0}  // 7
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


int pieceValue(int piece) {
	piece = abs(piece);
	if (piece == 1)
		return 1;
	if (piece == 2)
		return 5;
	if (piece == 3)
		return 3;
	if (piece == 4)
		return 3;
	if (piece == 5)
		return 9;
	if (piece == 6)
		return 0;
}



vector<float> xPosWeights = { 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 };
vector<float> yPosWeights = { 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 };







float scoreBoard(vector<vector<int>> board, int ourColor) {
	float ourScore = 0;
	float enemyScore = 0;

	for (int i = 0; i < size(board); i++) {
		for (int j = 0; j < size(board); j++) {
			if (board[i][j] == 0)
				continue;
			int color = board[i][j] / abs(board[i][j]);
			if (color == 1) {
				float pieceScore = pieceValue(board[i][j]);
				pieceScore *= yPosWeights[i];
				pieceScore *= xPosWeights[j];

				if (color == ourColor)
					ourScore += pieceScore;
				else
					enemyScore += pieceScore;
			}
			if (color == -1) {
				float pieceScore = pieceValue(board[i][j]);
				pieceScore *= yPosWeights[yPosWeights.size() - (i+1)];
				pieceScore *= xPosWeights[j];

				if (color == ourColor)
					ourScore += pieceScore;
				else
					enemyScore += pieceScore;
			}

		}
	}
	return ourScore - enemyScore;
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


vector<vector<int>> makeMove(vector<vector<int>> board, CMove move) {
	vector<vector<int>> newBoard;

	for (int i = 0;i<size(board);i++) {
		newBoard.push_back(board[i]);
	}

	newBoard[move.to.y][move.to.x] = board[move.from.y][move.from.x];
	newBoard[move.from.y][move.from.x] = 0;
	return newBoard;
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

vector<CMove> bishopMoves(int y, int x, vector<vector<int>> board) {
	vector<CMove> moves;
	int color = board[y][x] / abs(board[y][x]);
	vector<vec2> directions{ {-1,-1},{1,-1}, {1,1},{-1,1} };
	for (int i = 0; i < 4;i++) {
		vec2 direction = directions[i];
		for (int j = 1; j < 9;j++) {
			int newX = x + direction.x * j;
			int newY = y + direction.y * j;

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

vector<CMove> queenMoves(int y, int x, vector<vector<int>> board) {
	vector<CMove> moves = rookMoves(y, x, board);
	vector<CMove> moves1 = bishopMoves(y, x, board);
	for (int i = 0; i < size(moves1); i++) {
		moves.push_back(moves1[i]);
	}
	return moves;

}

vector<vec2> controlledSpots(int controller, vector<vector<int>> board) {
	vector<vec2> coordinates;
	for (int i = 0;i < size(board);i++) {
		for (int j = 0; j < size(board); j++) {
			if (controller == 1) {
				if (board[i][j] > 0) {
					if (abs(board[i][j]) == 1) { // Pawn
						vector<CMove> subMoves;
						subMoves = pawnMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);
						}
					}
					if (abs(board[i][j]) == 2) { // Rook
						vector<CMove> subMoves;
						subMoves = rookMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);
						}
					}

					if (abs(board[i][j]) == 3) { // Knight
						vector<CMove> subMoves;
						subMoves = knightMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);
						}
					}
					
					if (abs(board[i][j]) == 4) { // Bishop
						vector<CMove> subMoves;
						subMoves = bishopMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);
						}
					}
					if (abs(board[i][j]) == 5) {
						vector<CMove> subMoves;
						subMoves = queenMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);
						}
					}
					if (abs(board[i][j]) == 6) {
						vector<vec2> subMoves = { {j - 1,i - 1},{j,i - 1},{j + 1,i - 1},{j + 1,i},{j + 1,i + 1},{j,i + 1},{j - 1,i + 1},{j - 1,i} };
						for (int k = 0; k < size(subMoves);k++) {
							coordinates.push_back(subMoves[k]);
						}
					}
				}
			}
			if (controller == -1) {
				if (board[i][j] == 2)
					int a = 5;
				if (board[i][j] < 0) {
					if (abs(board[i][j]) == 1) { // Pawn
						vector<CMove> subMoves;
						subMoves = pawnMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);

						}
					}
					if (abs(board[i][j]) == 2) { // Rook
						vector<CMove> subMoves;
						subMoves = rookMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);

						}
					}

					if (abs(board[i][j]) == 3) { // Knight
						vector<CMove> subMoves;
						subMoves = knightMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);

						}
					}

					if (abs(board[i][j]) == 4) { // Bishop
						vector<CMove> subMoves;
						subMoves = bishopMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);
						}
					}
					if (abs(board[i][j]) == 5) {
						vector<CMove> subMoves;
						subMoves = queenMoves(i, j, board);
						for (int k = 0; k < size(subMoves);k++) {
							vec2 coords = subMoves[k].to;
							coordinates.push_back(coords);
						}
					}
					if (abs(board[i][j]) == 6) {
						vector<vec2> subMoves = { {j - 1,i - 1},{j,i - 1},{j + 1,i - 1},{j + 1,i},{j + 1,i + 1},{j,i + 1},{j - 1,i + 1},{j - 1,i} };
						for (int k = 0; k < size(subMoves);k++) {
							coordinates.push_back(subMoves[k]);
						}
					}

				}
			}
		}
	}
	return coordinates;
}


ScoredMove chooseMove(vector<CMove> moves, vector<vector<int>> board, int forWho) {
	float highestScore = 0;
	CMove bestMove = { {0,0}, {0,0} };
	for (int i = 0; i < size(moves);i++) {
		if (i == 0) {
			vector<vector<int>> newBoard;
			newBoard = makeMove(board, moves[i]);
			highestScore = scoreBoard(newBoard, forWho);
			bestMove.from.x = moves[i].from.x;
			bestMove.from.y = moves[i].from.y;
			bestMove.to.x = moves[i].to.x;
			bestMove.to.y = moves[i].to.y;
			//debugMove(bestMove);

			continue;
		}
		vector<vector<int>> newBoard;
		newBoard = makeMove(board, moves[i]);
		//printf("%d\n", size(newBoard));
		float curScore = scoreBoard(newBoard, forWho);
		if (curScore >= highestScore){
			highestScore = curScore;
			bestMove = moves[i];
		}
	}
	ScoredMove scoredMove = { bestMove,highestScore };
	return scoredMove;

}


vector<CMove> kingMoves(int y, int x, vector<vector<int>>board) {
	vector<CMove> moves;
	vector<vec2> directions = { {-1,-1}, {0,-1}, {1,-1}, {1,0}, {1,1}, {0,1}, {-1,1}, {-1,0} };
	int color = board[y][x] / abs(board[y][x]);
	if (color == -1)
		color = 1;
	else
		color = -1;
	vector<vec2> controlSpots = controlledSpots(color, board);
	int lever = 0;
	for (int i = 0;i < 8;i++) {
		lever = 0;
		int newX = x + directions[i].x;
		int newY = y + directions[i].y;
		if (newX >= 0 && newX < 8 && newY >= 0 && newY < 8) {
			vec2 newPos = { newX,newY };
			for (int j = 0; j < size(controlSpots);j++) {
				if (controlSpots[j].x == newX && controlSpots[j].y == newY) {
					lever = 1;
					break;
				}
			}
			if (lever == 0) {
				CMove move = { {x,y}, {newX,newY} };
				moves.push_back(move);
			}
		}
	}
	return moves;
}



vector<CMove> getMoves(vector<vector<int>> board, int color) {
	vector<CMove> moves;
	for (int i = 0;i < size(board);i++) {
		//printf("Hi\n");
		for (int j = 0; j < size(board); j++) { 
			if ((color == -1 && board[i][j] < 0 ) || (color == 1 && board[i][j] > 0)) {
				if (abs(board[i][j]) == 1) { // Pawn
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

				if (abs(board[i][j]) == 3) { // Knight
					vector<CMove> subMoves;
					subMoves = knightMoves(i, j, board);
					for (int k = 0; k < size(subMoves);k++) {
						CMove curMove = subMoves[k];
						moves.push_back(curMove);
					}
				}

				if (abs(board[i][j]) == 4) { // Bishop
					vector<CMove> subMoves;
					subMoves = bishopMoves(i, j, board);
					for (int k = 0; k < size(subMoves);k++) {
						CMove curMove = subMoves[k];
						moves.push_back(curMove);
					}
				}

				if (abs(board[i][j]) == 5) {
					vector<CMove> subMoves;
					subMoves = queenMoves(i, j, board);
					for (int k = 0; k < size(subMoves);k++) {
						CMove curMove = subMoves[k];
						moves.push_back(curMove);
					}
				}

				if (abs(board[i][j]) == 6) {
					vector<CMove> subMoves;
					subMoves = kingMoves(i, j, board);
					for (int k = 0; k < size(subMoves);k++) {
						CMove curMove = subMoves[k];
						moves.push_back(curMove);
					}
				}
			}

		}
	}
	return moves;
}


ScoredMove layeredMoveChoice(vector<vector<int>> board, int color, int layers = 0, int originalColor=0, int originalLayers=0) {
	vector<CMove> moves = getMoves(board, color);
	ScoredMove move;
	float highScore = -100;
	ScoredMove bestMove;
	for (int i = 0;i < size(moves);i++) {
		if (layers == 0) {
			bestMove = chooseMove(moves, board, color);
			return bestMove;
		}
		else {
			vector<vector<int>> newBoard = makeMove(board, moves[i]);
			color *= -1;
			move = layeredMoveChoice(newBoard, color, layers - 1, originalColor, originalLayers);
			color *= -1;
			if (move.score >= highScore) {
				bestMove = move;
				if (layers == originalLayers) {
					bestMove = { moves[i], move.score };
				}
			}
		}
	}
	if (layers == originalLayers) {
		int a = 2;
	}
	return bestMove;
}



int main()
{
	locale::global(locale("en_US.UTF-8"));
	wcout.imbue(locale());
	printf("Hello World!\n");
	vec2 v(3, 4);

	CMove m(v, vec2(7, 8));
	vector<CMove> moves;
	vector<vector<int>> board = makeBoard();
	moves = getMoves(board, 1);
	vector<vector<int>> newBoard = makeMove(board, moves[0]);
	//printf(to_string(scoreBoard(board, 1)).c_str());
	ScoredMove bestMove = chooseMove(moves, board, 1);
	ScoredMove otherMove = layeredMoveChoice(board, 1, 2, 1, 2);
	int col = 1;
	for (int i = 0;i < 10;i++) {
		ScoredMove moveToMake = layeredMoveChoice(board, col, 2, col, 2);
		board = makeMove(board, moveToMake.move);
		col *= -1;
	}
	debugMakeBoard(board);
	//debugMove(otherMove);
	debugMove(otherMove.move);
	int a = moves.size();


	for (int i = 0;i < 8;i++) {
		string row = "";
		for (int j = 0; j < 8; j++) {
			row += to_string(board[i][j]);
		}
		row = row + "\n";
		printf(row.c_str());
		row = "";
	}
	int b = 3;

	//printf(to_string(a).c_str());

	/*
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
	*/



	return 0;
}

