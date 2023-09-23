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
	string name;
	vector<float> xWeights;
	vector<float> yWeights;

};


void debugTestCaseWithPrintf(testCase tCase, ScoredMove gotMove) {
	printf("Expected score %f\n", tCase.expectedBestMove.score);
	printf("Expected x %d", tCase.expectedBestMove.move.to.x);
	printf(" Got x %d\n", gotMove.move.to.x);
	printf("Expected y %d", tCase.expectedBestMove.move.to.y);
	printf(" Got y %d\n", gotMove.move.to.y);


}


// Test Case boards




















bool runTests() {

	vector<vector<int>> testBoard = {
		//   0 1  2  3 4 5 6 7
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 0
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 1
			{0 ,0 ,0 ,0 ,0 ,3 ,0 ,0 }, // 2
			{0 ,0 ,0 ,-3,0 ,0 ,0 ,0 }, // 3
			{0 ,0 ,0 ,0 ,-1,0 ,0 ,0 }, // 4
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 5
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 6
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }  // 7
	};

	vector<vector<int>> testBoard1 = {
		//   0 1  2  3 4 5 6 7
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 0
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 1
			{0 ,0 ,0 ,0 ,0 ,0 ,3 ,0 }, // 2
			{0 ,0 ,0 ,0 ,-4,0 ,0 ,0 }, // 3
			{0 ,0 ,0 ,0 ,0 ,-2,0 ,0 }, // 4
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 5
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 6
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }  // 7
	};

	vector<vector<int>> testBoard2 = {
		//   0 1  2  3 4 5 6 7
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 0
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 1
			{0 ,0 ,0 ,0 ,0 ,3 ,0 ,0 }, // 2
			{0 ,0 ,0 ,-3,0 ,0 ,0 ,0 }, // 3
			{0 ,0 ,0 ,0 ,-1,0 ,0 ,0 }, // 4
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 5
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 6
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }  // 7
	};

	vector<vector<int>> testBoard3 = {
		//   0 1  2  3 4 5 6 7
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 0
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,2 }, // 1
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 2
			{0 ,0 ,0 ,0 ,-6,0 ,0 ,0 }, // 3
			{0 ,0 ,0 ,0 ,-3,0 ,0 ,0 }, // 4
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 5
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 6
			{0 ,0 ,0 ,2 ,2 ,2 ,0 ,0 }  // 7
	};

	vector<vector<int>> testBoard4 = {
		//   0  1  2  3  4  5  6  7
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 0
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 1
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 2
			{0 ,0 ,0 ,0 ,-6,0 ,0 ,0 }, // 3
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 4
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 5
			{0 ,0 ,0 ,0 ,0 ,0 ,0 ,2 }, // 6
			{0 ,0 ,0 ,2 ,0 ,2 ,0 ,0 }  // 7

	};

	vector<vector<int>> testBoard5 = {
		//0 1  2  3  4  5  6  7
		{-6,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 0
		{0 ,0 ,0 ,0 ,0 ,0 ,0 ,2 }, // 1
		{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 2
		{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 3
		{0 ,0 ,4 ,0 ,0 ,0 ,0 ,0 }, // 4
		{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 5
		{0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 }, // 6
		{0 ,2 ,0 ,0 ,0 ,0 ,0 ,0 }  // 7

	};





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

	vector<vector<int>> board1 = {
	{2,3,4,5,6,4,0,2},
	{1,1,1,1,1,1,1,1},
	{0,0,0,0,0,3,0,0},
	{0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0},
	{0,0,0,-3,0,0,0,0},
	{-1,-1,-1,-1,-1,-1,-1,-1},
	{-2,-3,-4,-5,-6,-4,-3,-2}
	};

	vector<vector<int>> board2 = {
	{2, 3, 0, 5, 6, 4, 3, 2 },
	{1, 1, 1, 0, 1, 1, 1, 1 },
	{0, 0, 0, 0, 0, 0, 0, 0 },
	{0, 0, 0, 1,-3, 0, 0, 0 },
	{0, 0, 0, 0, 0, 0, 4, 0 },
	{0, 0, 0, 0, 0, 0, 0, 0 },
	{-1,-1,-1,-1,-1,-1,-1,-1},
	{-2,-3,-4,-5,-6,-4, 0,-2}
	};




	// TODO: Make weights be in test cases


	//Init test cases
	CMove m(vec2(6, 2), vec2(4, 3));
	CMove m2(vec2(5, 2), vec2(4, 4));
	CMove m3(vec2(4, 3), vec2(4, 2));
	CMove m4(vec2(7,6), vec2(4, 6));
	CMove m5(vec2(2, 4), vec2(3, 3));


	testCase case1 = { testBoard1, ScoredMove {m,0.0}, 1, "Knight fork choice",{ 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 },
{ 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 }
	};
	testCase case2 = { testBoard2, ScoredMove {m2, 0.0}, 1 ,"Knight fork pinned by pawn",{ 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 },
{ 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 } };
	testCase case3 = { testBoard3, ScoredMove {m3, 0.0}, -1, "Cant hang king", { 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 },
{ 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 } };
	testCase case4 = { testBoard4, ScoredMove {m4, 0.0}, 1, "Checkmate for color 1 via rook", { 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 },
{ 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 } };
	testCase case5 = { testBoard5, ScoredMove {m5, 0.0}, 1, "Checkmate for color 1 via bishop", { 1.0,1.02,1.04,1.08,1.08,1.04,1.02,1.0 },
{ 1.0,1.02,1.04,1.06,1.08,1.1,1.12,1.14 } };

	//debugTestCaseWithPrintf(case1, ScoredMove{ m,10.1592045 });
	vector<testCase> testCases = {case1,case2,case3,case4,case5};
	// End of test cases



	// run them

	printf("==========================\n");
	printf("Starting Test Case run!\n");

	bool res = true;
	for (int i = 0;i < size(testCases);i++) {
		bool thisRes;
		ScoredMove gotMove = layeredMoveChoice(testCases[i].board, testCases[i].color, 2, testCases[i].color, 2, testCases[i].xWeights, testCases[i].yWeights);
		if (areMovesEqual(gotMove.move, testCases[i].expectedBestMove.move) == true) {
			thisRes = true;
			printf("Test case %d, also know as %s : PASSED !\n", i, testCases[i].name.c_str());
		}
		else {
			thisRes = false;
			//debugTestCaseWithPrintf(testCases[i], gotMove);
			printf("Test case %d, also know as %s : FAILED !\n", i, testCases[i].name.c_str());
		}

	}

	printf("Ending Test Case run!\n");
	printf("==========================\n");



	// end of run
	return res;
}

