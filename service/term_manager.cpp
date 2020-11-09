#include "term_manager.h"
#include <iostream>

TermManager::TermManager(){};

TermManager &TermManager::Get()
{
    return instance;
}

float TermManager::findHighestPrice(std::string bidding_id)
{
    // TODO: find hight price from DB
    return 0.0;
}

std::string TermManager::findWinner(std::string bidding_id)
{
    // find winner
    std::cout << "find winner\n";
    std::cout << bidding_id << "\n";
    // TODO: query DB to find winner
    return 0;
}

int TermManager::sendEmail(std::string user_id, bool seller)
{
    // send email
    std::cout << "send email\n";
    std::cout << user_id << "\n";
    if (seller)
    {
        // send email to seller
    } else 
    {
        // send email to buyer
    }
    return 0;
}


void UpdateBiddingResult(std::string bidding_id,
                         float highestPrice,
                         std::string winner)
{
    // TODO: update the bidding result in DB
}