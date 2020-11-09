#ifndef TERM_MANAGER_H
#define TERM_MANAGER_H

#include <string>

/*
 * This class will help to process the message
 * fetched from the message queue.
 * The fetch condition is the current time bigger less than
 * or equal to bidding end time.
*/
class TermManager
{
    static TermManager instance;
    TermManager();
public:
    TermManager(const TermManager&) = delete;
    static TermManager& Get();
    float findHighestPrice(std::string bidding_id);
    std::string findWinner(std::string bidding_id);
    int sendEmail(std::string user_id, bool seller);
    void UpdateBiddingResult(std::string bidding_id, float highestPrice,
                             std::string winner);
};

#endif