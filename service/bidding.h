#ifndef BIDDING_H
#define BIDDING_H

#include <vector>
#include <string>

/*
 * Bidding manager class helps to place orders
 * it is a view controller class for order managerment.
*/
class BiddingManager
{
    static BiddingManager instance;
    BiddingManager();
public:
    BiddingManager(const BiddingManager&) = delete;
    static BiddingManager& Get();
    int placeOrder(std::string user_id, std::string item_id);
    int cancelOrder(std::string user_id, std::string order_id);
    int runBidding(std::string bidding_id);
    std::vector<std::string> viewOrders(std::string urser_id);
};

#endif