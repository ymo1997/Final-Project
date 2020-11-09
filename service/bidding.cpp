#include "bidding.h"
#include <iostream>

BiddingManager::BiddingManager(){};

BiddingManager &BiddingManager::Get()
{
    return instance;
}

int BiddingManager::placeOrder(std::string user_id, std::string item_id)
{
    // send message to place a order
    std::cout << "placing the order\n";
    std::cout << user_id << "\n";
    // TODO: add the record to DB
    return 0;
}

int BiddingManager::cancelOrder(std::string user_id, std::string order_id)
{
    // send message to cancel a order
    std::cout << "canceling the order\n";
    std::cout << user_id << "\n";
    // TODO: remove the record from DB
    return 0;
}

int BiddingManager::runBidding(std::string bidding_id)
{
    // send message to run the bidding
    std::cout << "run a bidding\n";
    std::cout << bidding_id << "\n";
    // TODO: add start bidding to the message queue
    return 0;
}

std::vector<std::string> BiddingManager::viewOrders(std::string urser_id)
{
    // TODO: retrieve orders from DB
    std::vector<std::string> orderList; 
    return orderList;
}