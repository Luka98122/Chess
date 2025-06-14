﻿#include "pch.h"
#include "dllmain.h"
#include "Helpers.h"
#include "TestCases.h"
#include <sstream>
using namespace std;


vector<string> split(const string& s, char delimiter) {
	vector<string> tokens;
	string token;
	istringstream tokenStream(s);
	while (getline(tokenStream, token, delimiter)) {
		tokens.push_back(token);
	}
	return tokens;
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
	wstring myWString = L"";
	for (int i = 0; i < 8;i++) {
		for (int j = 0; j < 8; j++) {
			if (board[i][j] == 1)

				myWString += L"♟";
			else if (board[i][j] == 2)
				myWString += L"♜";
			else if (board[i][j] == 3)
				myWString += L"♞";
			else if (board[i][j] == 4)
				myWString += L"♝";
			else if (board[i][j] == 5)
				myWString += L"♛";
			else if (board[i][j] == 6)
				myWString += L"♚";
			// Other
			else if (board[i][j] == -1)
				myWString += L"♙";
			else if (board[i][j] == -2)
				myWString += L"♖";
			else if (board[i][j] == -3)
				myWString += L"♘";
			else if (board[i][j] == -4)
				myWString += L"♗";
			else if (board[i][j] == -5)
				myWString += L"♕";
			else if (board[i][j] == -6)
				myWString += L"♔";
			else if (board[i][j] == 0)
				myWString += L"ፙ";

		}
		myWString += L"\n";
	}
	OutputDebugStringW(myWString.c_str());

	std::ofstream outFile("hello_world.txt");
	/*
	for (int i = 0;i < 8;i++) {
		printf((myWString[i]+"\n").c_str());
 		if (outFile.is_open()) {
			outFile << myWString[i]+"\n";
		}
	}
	outFile.close();
	*/
	
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


// No dependency helpers
vector<vector<int>> makeMove(vector<vector<int>> board, CMove move) {
	vector<vector<int>> newBoard;

	for (int i = 0;i < size(board);i++) {
		newBoard.push_back(board[i]);
	}

	newBoard[move.to.y][move.to.x] = board[move.from.y][move.from.x];
	newBoard[move.from.y][move.from.x] = 0;
	return newBoard;
}


// End of no denependy helpers




//Basic Piece Moves

vector<CMove> pawnMoves(int y, int x, vector<vector<int>> board) {
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

		if (y == startPos && board[y + dy][x] == 0) {
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
	int color = board[y][x] / abs(board[y][x]);
	vector<vec2> directions{ {-1,0},{0,-1}, {1,0},{0,1} };
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

//Basic Piece Moves End.

//King moves
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

vector<CMove> kingMoves(int y, int x, vector<vector<int>>board) {
	vector<CMove> moves;
	vector<vec2> directions = { {-1,-1}, {0,-1}, {1,-1}, {1,0}, {1,1}, {0,1}, {-1,1}, {-1,0} };
	int color = board[y][x] / abs(board[y][x]);
	if (color == -1)
		color = 1;
	else
		color = -1;
	if (y == 0 && x == 0 && board[0][7] == 2) {
		int b = 3;
	}
	vector<vec2> controlSpots = controlledSpots(color, board);
	color *= -1;
	int lever = 0;
	for (int i = 0;i < 8;i++) {
		lever = 0;
		int newX = x + directions[i].x;
		int newY = y + directions[i].y;



		if (newX >= 0 && newX < 8 && newY >= 0 && newY < 8) {
			vec2 newPos = { newX,newY };

			if (board[newY][newX] != 0) {

				if ((board[newY][newX] / abs(board[newY][newX])) == color) {
					continue;
				}
			}

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
	//printf("Debug %d\n",size(moves));
	return moves;
}

bool isKingInCheck(vector<vector<int>> board, int color, int a, int b) {
	vector<vec2> controlSpots = controlledSpots(color * -1, board);
	int x;
	int y;
	int found = 0;
	for (int i = 0; i < size(board); i++) {
		for (int j = 0;j < size(board);j++) {
			if (board[i][j] == 6 * color) {
				y = i;
				x = j;
				found = 1;
			}
		}
	}
	vec2 kingPos = { x,y };

	for (int i = 0; i < size(controlSpots);i++) {
		if (kingPos.x == controlSpots[i].x and kingPos.y == controlSpots[i].y) {
			return true;
		}
	}
	return false;

}



//	GET MOVES
vector<CMove> checkMoves(vector<CMove> moves, vector<vector<int>> board, int color) {
	int x;
	int y;
	int found = 0;
	for (int i = 0; i < size(board); i++) {
		for (int j = 0;j < size(board);j++) {
			if (board[i][j] == 6 * color) {
				y = i;
				x = j;
				found = 1;
			}
		}
	}

	if (found == 0)
		return moves;

	vector<CMove> realMoves;
	for (int i = 0;i < size(moves);i++) {
		vector<vector<int>> newBoard = makeMove(board, moves[i]);
		if (isKingInCheck(newBoard, color, x, y) == false)
			realMoves.push_back(moves[i]);
	}
	return realMoves;
}

vector<CMove> getMoves(vector<vector<int>> board, int color) {
	vector<CMove> moves;
	for (int i = 0;i < size(board);i++) {
		//printf("Hi\n");
		for (int j = 0; j < size(board); j++) {
			if ((color == -1 && board[i][j] < 0) || (color == 1 && board[i][j] > 0)) {
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

	moves = checkMoves(moves, board, color);

	return moves;
}

//	GET MOVES





bool isCheckmate(vector<vector<int>> board, int color) {
	int x;
	int y;
	int found = 0;
	for (int i = 0; i < size(board); i++) {
		for (int j = 0;j < size(board);j++) {
			if (board[i][j] == 6 * color) {
				y = i;
				x = j;
				found = 1;
			}
		}
	}

	if (found == 0)
		return false;

	if (isKingInCheck(board, color, x, y) == true) {
		vector<CMove> moves = getMoves(board, color);
		if (size(moves) == 0)
			return true;
	}
	return false;
}



float scoreBoard(vector<vector<int>> board, int ourColor, vector<float> yPosWeights,vector<float> xPosWeights) {
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

	if (isCheckmate(board, ourColor * -1)) {
		ourScore = ourScore + 20000;
	}

	if (isCheckmate(board, ourColor)) {
		enemyScore = enemyScore + 20000;
	}



	return ourScore - enemyScore;
}

vector<vec2> controlledSpotsForKing(int controller, vector<vector<int>> board) {
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

ScoredMove chooseMove(vector<CMove> moves, vector<vector<int>> board, int forWho, vector<float> xPosWeights, vector<float> yPosWeights) {
	float highestScore = 0;
	CMove bestMove = { {0,0}, {0,0} };
	for (int i = 0; i < size(moves);i++) {
		if (areMovesEqual(moves[i], CMove{ {2,4}, {3,3} })) {
			int b = 3;		
		}
	
		if (i == 0) {
			vector<vector<int>> newBoard;
			newBoard = makeMove(board, moves[i]);
			highestScore = scoreBoard(newBoard, forWho, xPosWeights, yPosWeights);
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
		float curScore = scoreBoard(newBoard, forWho,{ 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 },
			{ 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 });
		if (curScore > 1000) {
			int c = 3;
		}
		if (curScore >= highestScore){
			highestScore = curScore;
			bestMove = moves[i];
		}
	}
	ScoredMove scoredMove = { bestMove,highestScore };
	return scoredMove;

}



void writeBoardStateToFile(vector<vector<int>> board) {
	ofstream myfile("target.txt");

	// Check if the file is open
	if (myfile.is_open()) {
		for (int i = 0;i < 8;i++) {
			string thisLine = "";
			for (int j = 0;j < 8;j++) {
				if (j == 7) {
					thisLine += to_string(board[i][j]);
				}
				else {
					thisLine += to_string(board[i][j])+";";
				}
			}
			thisLine += "\n";
			myfile << thisLine;
			printf(thisLine.c_str());
		}
		
		// Close the file
		myfile.close();
	}
	else {
		std::cout << "Unable to open file";
	}
}


ScoredMove layeredMoveChoice(vector<vector<int>> board, int color, int layers, int originalColor, int originalLayers, vector<float> xPosWeights = { 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 }, vector<float> yPosWeights = { 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 }) {
	vector<CMove> moves = getMoves(board, color);
	ScoredMove move;
	float highScore = -100;
	ScoredMove bestMove;
	if (layers % 2 != 0) {
		highScore = 100;
	}
	for (int i = 0;i < size(moves);i++) {
		if (layers == 0) {
			bestMove = chooseMove(moves, board, originalColor, xPosWeights, yPosWeights);
			return bestMove;
		}
		else {
			if (layers == originalLayers)
				int a = 3;
			if (areMovesEqual(moves[i], CMove(vec2(7, 1), vec2(0, 1))) == true && layers == originalLayers) {
				int a = 2;
			}
			vector<vector<int>> newBoard = makeMove(board, moves[i]);
			if (layers % 2 == 0)
				if (isCheckmate(newBoard, color * -1)) {
					bool a = isCheckmate(newBoard, color * -1);
					return ScoredMove{ moves[i], 20000 };
				}
			color *= -1;
			move = layeredMoveChoice(newBoard, color, layers - 1, originalColor, originalLayers, xPosWeights, yPosWeights);
			color *= -1;
			if (layers % 2 != 0) {
				if (move.score <= highScore) {
					bestMove = { moves[i], move.score };
					highScore = move.score;
					if (layers == originalLayers) {
						bestMove = { moves[i], move.score };
						//debugMove(move.move);
					}
				}
			}
			else if (move.score >= highScore) {
				bestMove = move;
				highScore = bestMove.score;
				if (layers == originalLayers) {
					bestMove = { moves[i], move.score };
					//debugMove(move.move);
				}
			}
		}
	}
	if (layers == originalLayers) {
		int a = 2;
	}
	if (layers % 2 != 0) {
		vector<vector<int>> newBoard = makeMove(board, bestMove.move);
		vector<CMove> moves = getMoves(newBoard, originalColor);
		bestMove = chooseMove(moves, newBoard, originalColor, { 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 }, { 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 });
		if (size(moves) == 0) {
			bestMove.score = -100;
			return bestMove;
		}
	}
	return bestMove;
}

extern "C" {
	__declspec(dllexport) const char* pick_move(const char* input) {
		std::string str(input);
		int length = str.length();
		std::string result = std::to_string(length);
		char* output = new char[result.length() + 1];
		strcpy(output, result.c_str());

		char delimiter = ';';

		vector<string> res = split(input, delimiter);

		string output_str = "";
		vector<vector<int>> board;

		// Convert to board

		for (int i = 0;i < 8;i++) {
			board.push_back({});
			for (int j = 0;j < 8;j++) {
				output_str += res[i * 8 + j];
				board[i].push_back(stoi(res[i * 8 + j]));
			}
			output_str += "\n";

		}

		ScoredMove bestMove = layeredMoveChoice(board, -1, 2, -1, 2);

		board = makeMove(board, bestMove.move);
		string res_str_board;
		output_str = "";
		for (int i = 0;i < 8;i++) {
			for (int j = 0;j < 8;j++) {
				output_str += to_string(board[i][j]) + ";";
				printf((output_str+"\n").c_str());
			}
		}

		return output_str.c_str();
	}

	__declspec(dllexport) const char* get_moves(const char* input) {
		vector<string> res = split(input, '<');


		string output_str = "";
		vector<vector<int>> board;

		// Convert to board
		vector<string> res2 = split(res[0], ';');
		for (int i = 0;i < 8;i++) {
			board.push_back({});
			for (int j = 0;j < 8;j++) {
				output_str += res2[i * 8 + j];
				board[i].push_back(stoi(res2[i * 8 + j]));
			}
			output_str += "\n";

		}

		vector<CMove> moves;

		if (res[1] == "-1") {
			int color = -1;
			moves = getMoves(board, color);
		}
		if (res[1] == "1") {
			int color = 1;
			moves = getMoves(board, color);
		}

		string outputStr = "";

		for (int i = 0;i < moves.size();i++) {
			int x1 = moves[i].from.x;
			int y1 = moves[i].from.y;
			int x2 = moves[i].to.x;
			int y2 = moves[i].to.y;

			outputStr = outputStr + to_string(x1) + ";" + to_string(y1) + ";" + to_string(x2) + ";" + to_string(y2) + ";M";


		}
		return outputStr.c_str();

	}

	__declspec(dllexport) const char* is_checkmate(const char* input) {
		vector<string> res = split(input, '<');


		string output_str = "";
		vector<vector<int>> board;

		// Convert to board
		vector<string> res2 = split(res[0], ';');
		for (int i = 0;i < 8;i++) {
			board.push_back({});
			for (int j = 0;j < 8;j++) {
				output_str += res2[i * 8 + j];
				board[i].push_back(stoi(res2[i * 8 + j]));
			}
			output_str += "\n";

		}

		int color = stoi(res[1]);

		if (isCheckmate(board,color)) {
			return "L";
		}

		if (isCheckmate(board, color*-1)) {
			return "W";
		}

		return "N";
	}
}


int main()
{
	SetConsoleOutputCP(CP_UTF8);

	locale::global(locale("en_US.UTF-8"));
	wcout.imbue(locale());

	string res = is_checkmate("2;3;4;5;6;4;3;2;1;1;1;1;1;1;1;1;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;-1;-1;-1;-1;-1;-1;-1;-1;-2;-3;-4;-5;-6;-4;-3;-2;<1");



	vector<vector<int>> board = makeBoard();
	int* myVec = new int[64];
	for (int i = 0; i < 8;i++) {
		for (int j = 0;j < 8;j++) {
			myVec[i*8+j] = board[i][j];
		}
	}
	//ScoredMove ThisRes = pickMove(myVec, 8, 8, -1, 2, -1, 2);
	runTests();

	printf("Hello World!\n");
	vec2 v(3, 4);

	CMove m(vec2(6, 0), vec2(5, 2));
	CMove m2(vec2(3, 1), vec2(3, 3));

	vector<CMove> moves;
	ScoredMove movic = layeredMoveChoice(testBoard, 1, 2, 1, 2);

	moves = getMoves(board, 1);
	vector<vector<int>> newBoard = makeMove(board, moves[0]);
	//printf(to_string(scoreBoard(board, 1)).c_str());
	ScoredMove bestMove = chooseMove(moves, board, 1, { 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 },
		{ 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 });
	ScoredMove otherMove = layeredMoveChoice(board, 1, 2, 1, 2);
	int col = 1;
	for (int i = 0;i < 20;i++) {
		if (i == 2) {
			int a = 2;
		}
		ScoredMove moveToMake = layeredMoveChoice(board, col, 2, col, 2);
		board = makeMove(board, moveToMake.move);
		if (i == 2) {
			int a = 2;
		}
		col *= -1;
		/*for (int i = 0;i < 8;i++) {
			string row = "";
			for (int j = 0; j < 8; j++) {
				if (board[i][j] >= 0) {
					row += " " + to_string(board[i][j]);
				}
				else {
					row += to_string(board[i][j]);
				}
			}
			row = row + "\n";
			OutputDebugStringA(row.c_str());
			row = "";
		}
		*/
		OutputDebugStringA("====================\n");
		debugMakeBoard(board);
		OutputDebugStringA("====================\n");
		float ourJustPlayedScore = scoreBoard(board, col * -1,{ 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 },
			{ 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 });
		OutputDebugStringA((to_string(ourJustPlayedScore)+"\n").c_str());
		OutputDebugStringA("====================\n");
	}
	writeBoardStateToFile(board);
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

