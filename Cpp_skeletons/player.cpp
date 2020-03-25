#include "player.hpp"
#include <cstdlib>

namespace TICTACTOE3D
{

GameState Player::play(const GameState &pState,const Deadline &pDue)
{
    //std::cerr << "Processing " << pState.toMessage() << std::endl;

    std::vector<GameState> lNextStates;
    pState.findPossibleMoves(lNextStates);


    if (lNextStates.size() == 0) return GameState(pState, Move());

    /*
     * Here you should write your clever algorithms to get the best next move, ie the best
     * next state. This skeleton returns a random move instead.
     */
    
    // return lNextStates[rand() % lNextStates.size()];
    State bestState = nextMove(pState, 3, INT_MIN, INT_MAX);
    return bestState.bestState;
}

State Player::nextMove(const GameState &pState, int depth, int alpha, int beta) {
    int v;
    State state;

    std::vector<GameState> lNextStates;
    pState.findPossibleMoves(lNextStates);
    uint8_t player = pState.getNextPlayer();
    State newState;
    newState.value  = evaluate(pState, player);
    newState.bestState = pState;
    if (depth == 0 || lNextStates.size() == 0) return newState;
    else if (player == CELL_X) {
        GameState currState;
        v = INT_MIN;
        for (int i = 0; i < lNextStates.size(); i++) {
            currState = lNextStates[i];
            State bestState = nextMove(currState, depth-1, alpha, beta);
            if (bestState.value > v) {
                v = bestState.value;
                state.bestState = currState;
            }
            alpha = std::max(alpha, v);
            if (beta <= alpha) break;
        }
    } else {
        GameState currState;
        v = INT_MAX;
        for (int i = 0; i < lNextStates.size(); i++) {
            currState = lNextStates[i];
            State bestState = nextMove(currState, depth-1, alpha, beta);
            if (bestState.value < v) {
                v = bestState.value;
                state.bestState = currState;
            }
            beta = std::min(beta, v);
            if (beta <= alpha) break;
        }
    }
    state.value = v;
    return state;
}

int Player::evaluate(const GameState &pState, uint8_t currPlayer) {
    int sum;
    if (pState.isXWin()) return INT_MAX;
    if (pState.isOWin()) return INT_MIN;

    for (int i = 0; i < 64; i++)
    {
        if (pState.at(i) == currPlayer) sum += 2; // count both
    }

    for (int i = 0; i < 4; i++) 
    {
        if (pState.at(i, i, 0) == currPlayer) sum += 1; // count both
        if (pState.at(i, 3-i, 0) == currPlayer) sum += 1; // count both
        if (pState.at(i, 0, i) == currPlayer) sum += 1; // count both
        if (pState.at(i, 0, 3-i) == currPlayer) sum += 1; // count both
        if (pState.at(0, i, i) == currPlayer) sum += 1; // count both
        if (pState.at(0, i, 3-i) == currPlayer) sum += 1; // count both
        if (pState.at(i, i, 3) == currPlayer) sum += 1; // count both
        if (pState.at(i, 3-i, 3) == currPlayer) sum += 1; // count both
        if (pState.at(i, 3, i) == currPlayer) sum += 1; // count both
        if (pState.at(i, 3, 3-i) == currPlayer) sum += 1; // count both
        if (pState.at(3, i, i) == currPlayer) sum += 1; // count both
        if (pState.at(3, i, 3-i) == currPlayer) sum += 1; // count both

        if (pState.at(i, i, i) == currPlayer) sum += 1; // count both
        if (pState.at(i, i, 3 - i) == currPlayer) sum += 1; // count both
        if (pState.at(i, 3 - i, i) == currPlayer) sum += 1; // count both
        if (pState.at(3 - i, i, i) == currPlayer) sum += 1; // count both
    }

    if (currPlayer == CELL_O) return -1*sum;
    return sum;
}

// void Player::sortArray(std::vector<GameState> lNextStates) {
//     std::sort(lNextStates.begin(), lNextStates + lNextStates.size(), compareValue);
// }

// bool compareValue(State i1, State i2) 
// { 
//     return (i1.value < i2.value); 
// } 

/*namespace TICTACTOE*/ }
