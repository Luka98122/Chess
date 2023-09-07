#include "pch.h"
#include "Helpers.h"
#include "TestCases.h"
#include "dllmain.h"

using namespace std;

class testCase {
public:
	vector<vector<int>> board;
	ScoredMove expectedBestMove;
	int color;
};


void debugTestCaseWithPrintf(testCase tCase, ScoredMove gotMove) {
	printf("Expected score %f\n", tCase.expectedBestMove.score);
	printf("Expected x %d", tCase.expectedBestMove.move.to.x);
	printf(" Got x %d\n", gotMove.move.to.x);
	printf("Expected y %d", tCase.expectedBestMove.move.to.y);
	printf(" Got y %d\n", gotMove.move.to.y);


}





bool runTests() {
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


	//Init test cases
	CMove m(vec2(6, 0), vec2(5, 2));
	CMove m2(vec2(3, 1), vec2(3, 3));

	testCase case1 = { board, ScoredMove {m,10.1592045}, 1 };
	testCase case2 = { testBoard, ScoredMove {m2,22.9216003}, 1 };
	//debugTestCaseWithPrintf(case1, ScoredMove{ m,10.1592045 });
	vector<testCase> testCases = {case1,case2};
	// End of test cases



	// run them
	bool res = true;
	for (int i = 0;i < size(testCases);i++) {
		bool thisRes;
		ScoredMove gotMove = layeredMoveChoice(testCases[i].board, testCases[i].color, 2, testCases[i].color, 2);
		if (areMovesEqual(gotMove.move, testCases[i].expectedBestMove.move) == true &&
			testCases[i].expectedBestMove.score == gotMove.score) {
			thisRes = true;
		}
		else {
			thisRes = false;
			debugTestCaseWithPrintf(testCases[i], gotMove);
		}

	}


	// end of run
	return res;
}

