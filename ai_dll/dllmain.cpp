#include "pch.h"
#include <iostream>
#include <stdio.h>
#include <string>

using namespace std;



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

std::vector<std::vector<int>> makeBoard() {
	std::vector<std::vector<int>> board = {
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

std::vector<std::vector<std::vector<int>>> pawnMoves(int y,int x, std::vector<std::vector<int>> board) {
	int dy = board[y][x];
	std::vector<std::vector<std::vector<int>>> moves(4);
	if (board[y + dy][x] == 0) {
		std::vector<std::vector<int>> move;
		std::vector<int> subMove;
		std::vector<int> subMove1;
		// [[[0,1], [0,2]]]
		subMove.push_back(x);
		subMove.push_back(y);
		subMove1.push_back(x);
		subMove1.push_back(y+dy);
		move.push_back(subMove);
		move.push_back(subMove1);
		moves.push_back(move);
	}
	if (board[y + dy][x-1] != 0) {
		if (dy == -1 && board[y + dy][x - 1] > 0) {
		
		}
		else if (dy == 1 && board[y + dy][x - 1] < 0) {

		}
		else {
			std::vector<std::vector<int>> move;
			std::vector<int> subMove;
			std::vector<int> subMove1;

			subMove.push_back(x);
			subMove.push_back(y);
			subMove1.push_back(x-1);
			subMove1.push_back(y+dy);
			move.push_back(subMove);
			move.push_back(subMove1);
			moves.push_back(move);
		}
	}
	if (board[y + dy][x + 1] != 0) {
		if (dy == -1 && board[y + dy][x + 1] > 0) {

		}
		else if (dy == 1 && board[y + dy][x + 1] < 0) {

		}
		else {
			std::vector<std::vector<int>> move;
			std::vector<int> subMove;
			std::vector<int> subMove1;

			subMove.push_back(x);
			subMove.push_back(y);
			subMove1.push_back(x+1);
			subMove1.push_back(y+dy);
			move.push_back(subMove);
			move.push_back(subMove1);
			moves.push_back(move);
		}
	}
	return moves;
}


std::vector<std::vector<int>> getMoves(std::vector<std::vector<int>> board) {
	std::vector<std::vector<std::vector<int>>> moves;
	for (int i = 0;i < size(board);i++) {
		printf("Hi\n");
		for (int j = 0; j < size(board); j++) {
			if (abs(board[i][j]) == 1) {
				std::vector<std::vector<std::vector<int>>> subMoves;
				subMoves = pawnMoves(i, j, board);
				for (int i = 0; i < size(subMoves);i++) {
					moves.push_back(subMoves[i]);
				}
			}
		}
	}
	return board;
}


int main()
{
	printf("Hello World!\n");
	std::vector<std::vector<int>> board = makeBoard();
	getMoves(board);
	return 0;
}

